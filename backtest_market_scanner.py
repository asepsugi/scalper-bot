import argparse
import asyncio
import pandas as pd
import numpy as np
import time
import ccxt
from rich.console import Console

from config import CONFIG, LIVE_TRADING_CONFIG, API_KEYS, WHITELIST_ROTATION_CONFIG
from strategies import STRATEGY_CONFIG
from utils.backtester_engine import PortfolioBacktester # REVISI: Impor engine backtesting
from utils.common_utils import get_all_futures_symbols

console = Console()

async def run_scan(backtester, symbols, limit, start_date, end_date):
    """
    PERBAIKAN: Mengubah menjadi fungsi async.
    Memindai semua simbol, menemukan sinyal, dan mensimulasikan perdagangan secara konkuren.
    """
    all_signals = []
    all_data = {}

    # --- PERBAIKAN: Pengambilan data konkuren ---
    console.log(f"Starting concurrent data fetching for {len(symbols)} symbols...")
    
    # Buat loop event untuk menjalankan tugas-tugas async di dalam fungsi sync
    loop = asyncio.get_event_loop()
    
    # Buat daftar tugas, bungkus panggilan sinkron dalam executor
    tasks = [loop.run_in_executor(None, backtester.fetch_and_prepare_symbol_data, symbol, limit, start_date, end_date) for symbol in symbols]
    
    results = await asyncio.gather(*tasks)

    for i, (result_df, from_cache) in enumerate(results):
        symbol = symbols[i]
        if result_df is not None and not result_df.empty:
            all_data[symbol] = result_df
            console.log(f"({i+1}/{len(symbols)}) Successfully processed [bold cyan]{symbol}[/bold cyan] (from cache: {from_cache})")
        else:
            console.log(f"({i+1}/{len(symbols)}) [yellow]Skipping {symbol} due to data issues.[/yellow]")

    if not all_data:
        console.log("[bold red]Failed to prepare data for any symbol. Exiting.[/bold red]")
        return

    # --- PILAR 2: SIMULASI DYNAMIC WEEKLY WHITELIST ROTATION ---
    # Kita akan membuat whitelist untuk setiap minggu dalam periode backtest.
    weekly_whitelists = {}
    if WHITELIST_ROTATION_CONFIG.get("enabled", False):
        console.log("\n[bold cyan]ROTATION ENGINE (Backtest):[/bold cyan] Generating historical weekly whitelists...")
        
        # Dapatkan rentang tanggal dari data pertama yang dimuat
        first_symbol = next(iter(all_data))
        start_date_bt = all_data[first_symbol].index.min()
        end_date_bt = all_data[first_symbol].index.max()

        # Iterasi per minggu
        for week_start_date in pd.date_range(start=start_date_bt, end=end_date_bt, freq='W-MON'):
            week_end_date = week_start_date + pd.Timedelta(days=6)
            scores = []
            
            # Dapatkan Top N Market Cap pada awal minggu itu
            # (Simplifikasi: kita asumsikan top 10 tidak banyak berubah, jadi kita gunakan blacklist statis)
            blacklist_symbols = set(CONFIG.get("strategy_params", {}).get("AltcoinVolumeBreakoutHunter", {}).get("symbol_blacklist", []))

            for symbol, df_full in all_data.items():
                if symbol in blacklist_symbols:
                    continue
                
                # Ambil data 30 hari sebelum awal minggu untuk kalkulasi
                df_period = df_full.loc[:week_start_date].tail(37) # 30 hari MA + 7 hari gain
                if len(df_period) < 37: continue

                # Kalkulasi skor sama seperti di live_trader
                volume_7d = df_period['volume'].tail(7).mean()
                volume_30d_ma = df_period['volume'].rolling(30).mean().iloc[-1]
                close_7d_gain = (df_period['close'].iloc[-1] / df_period['close'].iloc[-8] - 1) if len(df_period) > 7 else 0
                
                ath_30_days = df_period['high'].tail(30).max()
                drawdown_from_ath = (ath_30_days - df_period['close'].iloc[-1]) / ath_30_days
                if drawdown_from_ath > WHITELIST_ROTATION_CONFIG.get("max_drawdown_from_ath_pct", 0.35):
                    continue

                if volume_30d_ma > 0:
                    score = (volume_7d / volume_30d_ma) * (close_7d_gain + 1)
                    scores.append({'symbol': symbol, 'score': score})
            
            sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
            weekly_whitelists[week_start_date.week] = {item['symbol'] for item in sorted_scores[:WHITELIST_ROTATION_CONFIG.get("top_n_coins", 20)]}

    console.log("\nGenerating signals from prepared data...")
    for symbol, base_data in all_data.items():
        if base_data is None: continue
        
        # --- SOLUSI DEFINITIF: Hapus .dropna() yang agresif ---
        # Pembersihan data yang terlalu agresif adalah akar masalah.
        # Kita akan membiarkan data mentah (termasuk NaN dari periode pemanasan)
        # diteruskan ke fungsi strategi. Fungsi di `strategies.py` sudah
        # cukup tangguh untuk menangani ini dan hanya akan menghasilkan sinyal `False`
        # jika data tidak valid, sama seperti pada live/demo trader.
        if base_data.empty:
            console.log(f"[yellow]Skipping {symbol}: No valid data remains after preparation. Increase data limit or check indicators.[/yellow]")
            continue

        strategy_signals = {}
        for strategy_name, config in STRATEGY_CONFIG.items():
            # PERBAIKAN: Teruskan nama simbol ke fungsi strategi
            long_s, short_s, _ = config["function"](base_data, symbol=symbol)
            # PERBAIKAN: Pastikan sinyal yang dikembalikan valid sebelum digunakan
            if isinstance(long_s, pd.Series) and isinstance(short_s, pd.Series):
                strategy_signals[strategy_name] = {'long': long_s, 'short': short_s, 'weight': config["weight"]}
            else:  # Jika strategi mengembalikan None atau tipe data yang salah, anggap tidak ada sinyal
                strategy_signals[strategy_name] = {'long': pd.Series(False, index=base_data.index), 'short': pd.Series(False, index=base_data.index), 'weight': config["weight"]}

        long_score = pd.Series(0.0, index=base_data.index)
        short_score = pd.Series(0.0, index=base_data.index)
        
        # Hitung skor dari sinyal yang valid
        for signals in strategy_signals.values():
            long_score = long_score.add(signals['long'].astype(int) * signals['weight'], fill_value=0)
            short_score = short_score.add(signals['short'].astype(int) * signals['weight'], fill_value=0)

        total_possible_score = sum(c['weight'] for c in STRATEGY_CONFIG.values())
        consensus_ratio = LIVE_TRADING_CONFIG.get('consensus_ratio', 0.4) # Gunakan rasio yang lebih longgar
        required_score = total_possible_score * consensus_ratio

        df_consensus = base_data.copy()
        # PERBAIKAN: Inisialisasi kolom dengan dtype 'object' untuk mencegah FutureWarning
        df_consensus['signal'] = pd.Series(np.nan, index=df_consensus.index, dtype='object')
        df_consensus.loc[long_score >= required_score, 'signal'] = 'LONG'
        df_consensus.loc[short_score >= required_score, 'signal'] = 'SHORT'

        # PERBAIKAN: Tambahkan logging skor konsensus untuk debug
        last_long_score = long_score.iloc[-1]
        last_short_score = short_score.iloc[-1]

        primary_strat = pd.Series(np.nan, index=base_data.index, dtype='object')
        for strat_name, signals in strategy_signals.items():
            primary_strat.loc[signals['long']] = primary_strat.loc[signals['long']].fillna(strat_name)
            primary_strat.loc[signals['short']] = primary_strat.loc[signals['short']].fillna(strat_name)
        df_consensus['strategy'] = primary_strat
        df_consensus['symbol'] = symbol

        signals_df = df_consensus.dropna(subset=['signal'])
        if not signals_df.empty:
            # --- PILAR 2: Filter sinyal berdasarkan whitelist mingguan ---
            if WHITELIST_ROTATION_CONFIG.get("enabled", False) and weekly_whitelists:
                def is_in_whitelist(row):
                    week_of_year = row.name.week # PERBAIKAN: Akses timestamp dari nama indeks baris
                    whitelist_for_week = weekly_whitelists.get(week_of_year, set())
                    return row['symbol'] in whitelist_for_week
                
                signals_df = signals_df[signals_df.apply(is_in_whitelist, axis=1)]

            all_signals.extend(signals_df.reset_index().to_dict('records'))
        else:
            # PERBAIKAN: Berikan log yang lebih informatif
            if last_long_score > 0 or last_short_score > 0:
                console.log(f"[grey50]No consensus for {symbol}: Score Long={last_long_score:.2f}, Short={last_short_score:.2f} (Required: {required_score:.2f}). Check debug skips.[/grey50]")
            else:
                console.log(f"[grey50]No individual signals for {symbol}. Check strategy filters or data integrity.[/grey50]")

    if not all_signals:
        console.log("[bold red]No signals found across any symbols.[/bold red]")
        return
    
    # --- PEROMBAKAN ARSITEKTUR: Gunakan logika simulasi kronologis yang benar ---
    # Logika sebelumnya yang menggabungkan semua data menjadi satu DataFrame besar
    # sangat tidak efisien dan berisiko lookahead bias.
    # Kita akan meniru arsitektur yang lebih baik dari `backtest_strategy_comparation.py`.

    # 1. Urutkan semua sinyal berdasarkan timestamp
    sorted_signals = sorted(all_signals, key=lambda x: x['timestamp'])
    # Dapatkan semua timestamp unik di mana ada sinyal
    all_timestamps = sorted(list(set(s['timestamp'] for s in sorted_signals)))

    console.log(f"Starting chronological simulation across {len(all_timestamps)} signal timestamps...")

    # 2. Lakukan iterasi dari satu timestamp sinyal ke timestamp sinyal berikutnya
    # PERBAIKAN: Hapus progress bar (track) untuk membuat log lebih bersih
    for i in range(len(all_timestamps) - 1):
        current_time = all_timestamps[i]
        next_time = all_timestamps[i+1]
        
        if not backtester.check_drawdown_and_cooldown(current_time):
            continue
        
        # --- PILAR 3: SIMULASI WEEKLY PERFORMANCE KILLSWITCH ---
        if not backtester.check_weekly_killswitch(current_time):
            continue

        # Temukan semua sinyal yang terjadi pada timestamp ini
        current_signals = [s for s in sorted_signals if s['timestamp'] == current_time]

        # Proses exit/entry antara candle saat ini dan candle berikutnya
        backtester.check_trades_and_orders_fixed(current_time, next_time, all_data)
        for signal in current_signals:
            backtester.process_new_signal(signal, all_data)

    backtester.close_remaining_trades(all_data)

async def main():
    parser = argparse.ArgumentParser(description="Binance Futures Market Scanner Backtester")
    parser.add_argument("--limit", type=int, default=1500, help="Number of 5m candles to backtest per symbol")
    parser.add_argument("--max_symbols", type=int, default=50, help="Maximum number of symbols to scan (sorted by volume)")
    parser.add_argument("--start_date", type=str, default=None, help="Start date for backtest in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, default=None, help="End date for backtest in YYYY-MM-DD format")
    parser.add_argument("--historical_ranking", action='store_true', help="Rank symbols by volume from the backtest period instead of current volume.")
    args = parser.parse_args()

    import asyncio # Impor asyncio di sini agar hanya digunakan saat skrip dijalankan
    # --- PERBAIKAN: Logika baru untuk mengambil simbol secara asinkron ---
    async def fetch_symbols_async():
        import ccxt.pro as ccxtpro # Impor ccxt.pro untuk koneksi async
        """
        Fungsi helper async yang terisolasi untuk mengambil daftar simbol.
        Ini membuat instance exchange async sendiri, mengambil data, lalu menutupnya.
        """
        console.log("Membuat koneksi async sementara untuk mengambil daftar simbol...")
        async_exchange = None
        try:
            # Gunakan ccxt.pro untuk koneksi async
            async_exchange = ccxtpro.binance({
                'apiKey': API_KEYS['live']['api_key'],
                'secret': API_KEYS['live']['api_secret'],
                'options': {'defaultType': 'future'},
                'enableRateLimit': True,
            })
            async_exchange.set_sandbox_mode(False)
            symbols = await get_all_futures_symbols(async_exchange)
            return symbols
        finally:
            if async_exchange:
                await async_exchange.close()
                console.log("Koneksi async sementara ditutup.")
    backtester = PortfolioBacktester(initial_balance=CONFIG["account_balance"], simulate_latency=False)

    # --- PERBAIKAN: Inisialisasi ulang exchange sinkron untuk backtester ---
    # Backtester utama membutuhkan instance exchange sinkron untuk mengambil data historis.
    exchange = ccxt.binance({
        'apiKey': API_KEYS['live']['api_key'],
        'secret': API_KEYS['live']['api_secret'],
        'options': {'defaultType': 'future'},
        'enableRateLimit': True,
    })
    backtester.exchange = exchange
    
    # --- FITUR BARU: Logika untuk memilih metode ranking simbol ---
    if args.historical_ranking and args.start_date:
        console.log(f"[bold yellow]Mode Ranking Historis Aktif.[/bold yellow] Merangking simbol berdasarkan volume dari periode {args.start_date}.")
        # Ambil semua simbol terlebih dahulu
        all_available_symbols = await fetch_symbols_async()
        
        # Panggil fungsi baru dari backtester engine untuk merangking secara historis
        symbols_to_scan = backtester.rank_symbols_by_historical_volume(
            all_available_symbols, 
            args.start_date, 
            args.max_symbols
        )
        if not symbols_to_scan:
            console.log("[bold red]Gagal merangking simbol secara historis. Menggunakan ranking saat ini sebagai fallback.[/bold red]")
            # Fallback ke metode lama jika gagal
            all_symbols = await fetch_symbols_async()
            symbols_to_scan = all_symbols[:args.max_symbols]
    else:
        if args.historical_ranking and not args.start_date:
            console.log("[yellow]Peringatan: --historical_ranking memerlukan --start_date. Menggunakan ranking saat ini.[/yellow]")
        
        console.log("[bold green]Mode Ranking Saat Ini Aktif.[/bold green] Merangking simbol berdasarkan volume 24 jam terakhir.")
        # Metode lama: ambil simbol berdasarkan volume saat ini
        all_symbols = await fetch_symbols_async()
        symbols_to_scan = all_symbols[:args.max_symbols]

    if not symbols_to_scan:
        console.log("[bold red]Tidak ada simbol yang bisa diproses. Bot berhenti.[/bold red]")
        return

    console.log(f"Top {len(symbols_to_scan)} simbol yang akan di-backtest: {', '.join(symbols_to_scan)}")
    # --------------------------------------------------------------------

    await run_scan(backtester, symbols=symbols_to_scan, limit=args.limit, start_date=args.start_date, end_date=args.end_date)
    backtester.get_results(args=args)
    backtester.get_results_with_realism_report(args=args)

if __name__ == "__main__":
    asyncio.run(main())