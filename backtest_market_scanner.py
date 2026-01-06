import argparse
import asyncio
import pandas as pd
import pickle
import numpy as np
import time
import ccxt
from rich.console import Console
from pathlib import Path

from config import CONFIG, LIVE_TRADING_CONFIG, API_KEYS, WHITELIST_ROTATION_CONFIG, EXECUTION
from strategies import STRATEGY_CONFIG
from utils.backtester_engine import PortfolioBacktester # REVISI: Impor engine backtesting
from utils.common_utils import get_all_futures_symbols

console = Console()
# --- PERBAIKAN: Definisikan direktori cache di sini ---
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

async def run_scan(backtester, symbols, limit, start_date, end_date):
    """
    PERBAIKAN: Mengubah menjadi fungsi async.
    Memindai semua simbol, menemukan sinyal, dan mensimulasikan perdagangan secara konkuren.
    """
    all_signals = []
    all_data = {}

    # --- PERBAIKAN: Pengambilan data konkuren ---
    console.log(f"Starting concurrent data fetching for {len(symbols)} symbols...")
    
    loop = asyncio.get_event_loop()

    # --- BARU: Ambil Konteks Global BTC untuk Deteksi Rezim ---
    console.log("[bold yellow]Fetching Global BTC Context (Regime Detection)...[/bold yellow]")
    btc_result = await loop.run_in_executor(None, backtester.fetch_and_prepare_symbol_data, 'BTC/USDT', limit, start_date, end_date)
    btc_context = None
    if btc_result and btc_result[0] is not None and not btc_result[0].empty:
        btc_df = btc_result[0]
        # Ambil kolom penting saja untuk menghemat memori
        cols_to_keep = ['rsi_1h', 'close']
        # Pastikan kolom ada sebelum mengambil
        cols_to_keep = [c for c in cols_to_keep if c in btc_df.columns]
        btc_context = btc_df[cols_to_keep].copy()
        btc_context.rename(columns={c: c + '_BTC' for c in btc_context.columns}, inplace=True)
        console.log(f"Global BTC Context Loaded. Rows: {len(btc_context)}")

    # --- PERBAIKAN KRUSIAL: Proses data dalam batch untuk menghindari API ban ---
    batch_size = 5  # Proses 5 simbol sekaligus, ini jauh lebih aman dari 50.
    all_results = []
    for i in range(0, len(symbols), batch_size):
        batch_symbols = symbols[i:i + batch_size]
        console.log(f"\n[bold]Processing batch {i//batch_size + 1}/{(len(symbols) + batch_size - 1)//batch_size} (Symbols: {', '.join(batch_symbols)})[/bold]")

        # --- PERBAIKAN: Logika caching yang dipercepat ---
        async def process_symbol_with_smart_cache(symbol):
            """Wrapper untuk memproses data dengan cache yang sudah diolah."""
            # Buat nama file cache untuk data yang sudah diproses
            safe_symbol = symbol.replace('/', '_')
            date_part = f"_{start_date}_to_{end_date}" if start_date else f"_limit_{limit}"
            processed_cache_file = CACHE_DIR / f"PROCESSED_{safe_symbol}{date_part}.pkl"

            # 1. Coba muat dari cache yang sudah diproses
            if processed_cache_file.exists():
                try:
                    with open(processed_cache_file, 'rb') as f:
                        console.log(f"Loading [bold green]PROCESSED[/bold green] data for {symbol} from cache...")
                        return symbol, (pickle.load(f), True)
                except Exception as e:
                    console.log(f"[yellow]Corrupted processed cache for {symbol}, reprocessing... Error: {e}[/yellow]")

            # 2. Jika tidak ada, proses seperti biasa
            result_tuple = await loop.run_in_executor(None, backtester.fetch_and_prepare_symbol_data, symbol, limit, start_date, end_date)
            
            # 3. Simpan hasil olahan ke cache baru
            if result_tuple and result_tuple[0] is not None:
                with open(processed_cache_file, 'wb') as f:
                    pickle.dump(result_tuple[0], f)
            return symbol, result_tuple

        tasks = [process_symbol_with_smart_cache(symbol) for symbol in batch_symbols]
        batch_results = await asyncio.gather(*tasks)
        all_results.extend(batch_results)
        
        # Jeda singkat antar batch untuk lebih menghormati rate limit
        console.log("[grey50]Pausing for 2 seconds between batches...[/grey50]")
        await asyncio.sleep(2)

    # Proses hasil yang sudah dikumpulkan
    for symbol, (result_df, from_cache) in all_results:
        if result_df is not None and not result_df.empty:
            # --- BARU: Suntikkan Data BTC ke Simbol Altcoin ---
            if btc_context is not None and symbol != 'BTC/USDT':
                # Left join untuk mempertahankan index altcoin, ffill untuk mengisi gap
                result_df = result_df.join(btc_context, how='left')
                result_df.ffill(inplace=True)
            
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
        backtester.set_weekly_whitelists(weekly_whitelists) # Kirim data whitelist ke backtester untuk logging

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
        # --- BARU: Ambil batas posisi dari config ---
        max_pos = LIVE_TRADING_CONFIG.get('max_active_positions_limit', 8)

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

        # --- REFACTOR: Logika "Available Slots" untuk mencegah over-exposure ---
        # PERBAIKAN: Gunakan atribut yang benar dari engine: `active_positions` dan `pending_orders`
        active_positions = backtester.active_positions
        pending_orders = backtester.pending_orders
        current_exposure = len(active_positions) + len(pending_orders)
        available_slots = max_pos - current_exposure

        if available_slots > 0 and current_signals:
            # Hanya proses sinyal sebanyak slot yang tersedia
            for signal in current_signals[:available_slots]:
                backtester.process_new_signal(signal, all_data)
        elif current_signals:
            # Jika ada sinyal tapi tidak ada slot, log pesan skip sekali saja untuk efisiensi
            console.log(f"[grey50]Backtest Skip: Exposure limit ({max_pos}) reached. Active Trades: {len(active_positions)}, Pending Orders: {len(pending_orders)}. Skipping {len(current_signals)} signal(s).[/grey50]")
            
            # --- DEBUG: Tampilkan sampel trade yang membuat macet ---
            # Ini akan menjawab "Kenapa penuh?" dengan menunjukkan trade lama yang belum close.
            if len(active_positions) > 0 and i % 50 == 0: # Tampilkan setiap 50 candle (sekitar 4 jam sekali) agar tidak spam
                 console.log(f"[yellow]  ⚠️  STUCK TRADES SAMPLE ({len(active_positions)} total):[/yellow]")
                 # PERBAIKAN: Iterasi melalui `items()` untuk mendapatkan simbol dan detail trade aktif
                 for symbol, trade_details in list(active_positions.items())[:3]:
                     entry_time = trade_details.get('entry_time')
                     if entry_time:
                         duration_mins = (current_time - entry_time).total_seconds() / 60
                         console.log(f"     - {symbol} | Entry: {entry_time.strftime('%Y-%m-%d %H:%M')} | Dur: {duration_mins:.1f}m | SL: {trade_details.get('sl_price', 0):.4f}")

    backtester.close_remaining_trades(all_data)

def save_detailed_csv(backtester, filename="market_scan_results.csv"):
    """
    Menyimpan hasil backtest ke CSV dengan format kolom spesifik yang diminta user.
    File akan disimpan di dalam folder 'output'.
    """
    if not hasattr(backtester, 'closed_trades') or not backtester.closed_trades:
        console.log("[yellow]Tidak ada trade yang ditutup, file CSV tidak dibuat.[/yellow]")
        return

    filepath = OUTPUT_DIR / filename
    df = pd.DataFrame(backtester.closed_trades)

    # 1. Hitung Risk Per Trade Pct (dari config)
    try:
        def get_risk_pct(strategy_name):
            return CONFIG.get("strategy_params", {}).get(strategy_name, {}).get("risk_per_trade", np.nan)
        
        if 'strategy' in df.columns:
            df['risk_per_trade_pct'] = df['strategy'].apply(get_risk_pct)
        else:
            df['risk_per_trade_pct'] = np.nan
    except Exception as e:
        console.log(f"[yellow]Peringatan: Gagal menghitung 'risk_per_trade_pct'. Error: {e}[/yellow]")
        df['risk_per_trade_pct'] = np.nan

    # 2. Hitung Trade Size (Notional Value in USDT)
    try:
        if 'size' in df.columns and 'entry_price' in df.columns:
            df['trade_size_quote'] = df['size'] * df['entry_price']
        else:
            df['trade_size_quote'] = 0.0
    except Exception as e:
        console.log(f"[yellow]Peringatan: Gagal menghitung 'trade_size_quote'. Error: {e}[/yellow]")
        df['trade_size_quote'] = 0.0

    # 3. Buat ID
    df.insert(0, 'ID', range(1, len(df) + 1))

    # 4. Mapping nama kolom sesuai request
    # ID,Symbol,Strategy,Direction,Trade Size,Risk Per Trade Pct,Entry Time,Exit Time,PnL (USD),Balance,Exit Reason
    
    # Pastikan kolom Balance menggunakan balance_at_exit
    if 'balance_at_exit' in df.columns:
        df['Balance'] = df['balance_at_exit']
    else:
        df['Balance'] = np.nan

    rename_map = {
        'symbol': 'Symbol',
        'strategy': 'Strategy',
        'side': 'Direction',
        'trade_size_quote': 'Trade Size',
        'risk_per_trade_pct': 'Risk Per Trade Pct',
        'entry_time': 'Entry Time',
        'exit_time': 'Exit Time',
        'pnl': 'PnL (USD)',
        'exit_reason': 'Exit Reason'
    }
    
    df = df.rename(columns=rename_map)

    # 5. Pilih dan urutkan kolom
    target_columns = [
        'ID', 'Symbol', 'Strategy', 'Direction', 'Trade Size', 
        'Risk Per Trade Pct', 'Entry Time', 'Exit Time', 
        'PnL (USD)', 'Balance', 'Exit Reason'
    ]
    
    # Filter hanya kolom yang ada (untuk safety, meski kita sudah buat)
    final_columns = [col for col in target_columns if col in df.columns]
    
    df_final = df[final_columns]

    df_final.to_csv(filepath, index=False, float_format='%.4f')
    console.log(f"[bold green]Detailed trade log saved to {filepath}[/bold green]")


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
    
    # --- PERBAIKAN: Pastikan parameter eksekusi masuk ke CONFIG backtester ---
    if 'limit_order_expiration_candles' not in CONFIG:
        CONFIG['limit_order_expiration_candles'] = EXECUTION.get('limit_order_expiration_candles', 3)

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
    save_detailed_csv(backtester)

if __name__ == "__main__":
    asyncio.run(main())