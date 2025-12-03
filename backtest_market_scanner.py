import argparse
import asyncio
import pandas as pd
import numpy as np
import time
import ccxt
from rich.console import Console

from utils.backtester_engine import PortfolioBacktester
from config import CONFIG, LIVE_TRADING_CONFIG, API_KEYS
from strategies import STRATEGY_CONFIG
from utils.backtester_engine import PortfolioBacktester # REVISI: Impor engine backtesting
from utils.common_utils import get_all_futures_symbols

console = Console()

async def run_scan(backtester, symbols, limit):
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
    tasks = [loop.run_in_executor(None, backtester.fetch_and_prepare_symbol_data, symbol, limit) for symbol in symbols]
    
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

    console.log("\nGenerating signals from prepared data...")
    for symbol, base_data in all_data.items():
        if base_data is None: continue

        strategy_signals = {}
        for strategy_name, config in STRATEGY_CONFIG.items():
            long_s, short_s, _ = config["function"](base_data.copy())
            strategy_signals[strategy_name] = {'long': long_s, 'short': short_s, 'weight': config["weight"]}

        long_score = pd.Series(0.0, index=base_data.index)
        short_score = pd.Series(0.0, index=base_data.index)
        for signals in strategy_signals.values():
            long_score += signals['long'].astype(int) * signals['weight']
            short_score += signals['short'].astype(int) * signals['weight']

        total_possible_score = sum(c['weight'] for c in STRATEGY_CONFIG.values())
        required_score = total_possible_score * LIVE_TRADING_CONFIG.get('consensus_ratio', 0.55)

        df_consensus = base_data.copy()
        # PERBAIKAN: Inisialisasi kolom dengan dtype 'object' untuk mencegah FutureWarning
        df_consensus['signal'] = pd.Series(np.nan, index=df_consensus.index, dtype='object')
        df_consensus.loc[long_score >= required_score, 'signal'] = 'LONG'
        df_consensus.loc[short_score >= required_score, 'signal'] = 'SHORT'
        
        primary_strat = pd.Series(np.nan, index=base_data.index, dtype='object')
        for strat_name, signals in strategy_signals.items():
            primary_strat.loc[signals['long']] = primary_strat.loc[signals['long']].fillna(strat_name)
            primary_strat.loc[signals['short']] = primary_strat.loc[signals['short']].fillna(strat_name)
        df_consensus['strategy'] = primary_strat
        df_consensus['symbol'] = symbol

        signals_df = df_consensus.dropna(subset=['signal'])
        if not signals_df.empty:
            all_signals.extend(signals_df.reset_index().to_dict('records'))

    if not all_signals:
        console.log("[bold red]No signals found across any symbols.[/bold red]")
        return
    
    sorted_signals = sorted(all_signals, key=lambda x: x['timestamp'])
    signals_by_time = {s['timestamp']: s for s in sorted_signals}
    
    all_timestamps = sorted(list(set(s['timestamp'] for s in sorted_signals)))
    console.log(f"Starting chronological simulation across {len(all_timestamps)} unique signal timestamps...")

    # --- PERBAIKAN KRUSIAL: Ubah urutan logika loop ---
    # Kita harus memproses sinyal PADA current_time, LALU memeriksa apa yang terjadi
    # di antara current_time dan next_time.
    for i in range(len(all_timestamps)):
        current_time = all_timestamps[i]

        # --- FITUR BARU: Cek Drawdown Circuit Breaker di Backtester ---
        # Asumsikan kita menambahkan metode ini ke PortfolioBacktester
        if not backtester.check_drawdown_and_cooldown(current_time):
            # Jika circuit breaker aktif dan masih dalam masa cooldown, lewati iterasi ini
            continue

        # Proses semua sinyal yang terjadi pada timestamp ini TERLEBIH DAHULU
        signals_at_this_time = [s for s in sorted_signals if s['timestamp'] == current_time]
        for signal in signals_at_this_time:
            backtester.process_new_signal(signal, all_data)

        # SEKARANG, jalankan simulasi dari current_time ke next_time
        # Fungsi ini harus dimodifikasi di dalam backtester_engine.py untuk
        # menangani Multi-Level TP dan Trailing Stop.
        # Ini akan memeriksa order yang BARU SAJA dibuat.
        next_time = all_timestamps[i+1] if i + 1 < len(all_timestamps) else None
        if not next_time: continue # Jangan proses iterasi terakhir
        backtester.check_trades_and_orders_fixed(current_time, next_time, all_data)

    backtester.close_remaining_trades(all_data)

async def main():
    parser = argparse.ArgumentParser(description="Binance Futures Market Scanner Backtester")
    parser.add_argument("--limit", type=int, default=1500, help="Number of 5m candles to backtest per symbol")
    parser.add_argument("--max_symbols", type=int, default=50, help="Maximum number of symbols to scan (sorted by volume)")
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

    # Jalankan fungsi async menggunakan asyncio.run() yang modern dan aman
    all_symbols = await fetch_symbols_async()

    backtester = PortfolioBacktester(initial_balance=CONFIG["account_balance"])

    # --- PERBAIKAN: Inisialisasi ulang exchange sinkron untuk backtester ---
    # Backtester utama membutuhkan instance exchange sinkron untuk mengambil data historis.
    exchange = ccxt.binance({
        'apiKey': API_KEYS['live']['api_key'],
        'secret': API_KEYS['live']['api_secret'],
        'options': {'defaultType': 'future'},
        'enableRateLimit': True,
    })
    backtester.exchange = exchange

    symbols_to_scan = all_symbols[:args.max_symbols]

    await run_scan(backtester, symbols=symbols_to_scan, limit=args.limit)
    backtester.get_results(args=args)
    backtester.get_results_with_realism_report(args=args)

if __name__ == "__main__":
    asyncio.run(main())