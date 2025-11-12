import argparse
import pandas as pd
import numpy as np
import time # Impor modul time
import ccxt
from rich.console import Console

from config import CONFIG, LIVE_TRADING_CONFIG, API_KEYS
from strategies import STRATEGY_CONFIG
from utils.backtester_engine import PortfolioBacktester # REVISI: Impor engine backtesting
from utils.common_utils import get_all_futures_symbols

console = Console()

def run_scan(backtester, symbols, limit):
    """Scans all symbols, finds signals, and simulates trades."""
    all_signals = []
    all_data = {}

    console.log(f"Starting sequential data fetching for {len(symbols)} symbols to avoid rate limits...")
    for i, symbol in enumerate(symbols):
        try:
            console.log(f"({i+1}/{len(symbols)}) Fetching data for [bold cyan]{symbol}[/bold cyan]...")
            result_df, from_cache = backtester.fetch_and_prepare_symbol_data(symbol, limit)
            if result_df is not None and not result_df.empty:
                all_data[symbol] = result_df
                console.log(f"({i+1}/{len(symbols)}) Successfully processed [bold cyan]{symbol}[/bold cyan] (from cache: {not from_cache})")
            else:
                console.log(f"({i+1}/{len(symbols)}) [yellow]Skipping {symbol} due to data issues.[/yellow]")
            
            if not from_cache:
                console.log("   [dim]Data fetched from API, sleeping for 1s to respect rate limits...[/dim]")
                time.sleep(1)
            else:
                time.sleep(0.05)
        except Exception as exc:
            console.log(f"({i+1}/{len(symbols)}) [bold red]Error processing {symbol}: {exc}[/bold red]")

    if not all_data:
        console.log("[bold red]Failed to prepare data for any symbol. Exiting.[/bold red]")
        return

    console.log("\nGenerating signals using consensus filter...")
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

    for i in range(len(all_timestamps) - 1):
        current_time = all_timestamps[i]
        next_time = all_timestamps[i+1]
        # REVISI: Gunakan fungsi backtest yang lebih realistis
        # backtester.check_trades_and_orders(current_time, next_time, all_data)
        backtester.check_trades_and_orders_fixed(current_time, next_time, all_data)
        if current_time in signals_by_time:
            backtester.process_new_signal(signals_by_time[current_time], all_data)

    backtester.close_remaining_trades(all_data)

if __name__ == "__main__":
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
    all_symbols = asyncio.run(fetch_symbols_async())

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

    run_scan(backtester, symbols=symbols_to_scan, limit=args.limit)
    backtester.get_results(args=args)
    backtester.get_results_with_realism_report(args=args)