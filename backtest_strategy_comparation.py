import argparse
import pandas as pd
import json
import numpy as np
from pathlib import Path
from rich.console import Console
from rich.table import Table
import asyncio
import time

from config import CONFIG, LIVE_TRADING_CONFIG, FEES, SLIPPAGE
from indicators import fetch_binance_data_sync, calculate_indicators
from utils.data_preparer import prepare_data
from utils.common_utils import get_all_futures_symbols
from strategies import STRATEGY_CONFIG
from utils.backtester_engine import PortfolioBacktester # REVISI: Impor engine backtesting


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Portfolio-based Comparative Backtester for Trading Strategies")
    parser.add_argument("--max_symbols", type=int, default=20, help="Number of top symbols to test against (sorted by volume)")
    parser.add_argument("--limit", type=int, default=1500, help="Number of 5m candles to backtest")
    args = parser.parse_args()

    console = Console()

    # --- REVISI BESAR: Ambil daftar simbol teratas ---
    async def fetch_symbols_async():
        """Fungsi helper async untuk mengambil daftar simbol."""
        from config import API_KEYS
        import ccxt.pro as ccxtpro
        async_exchange = None
        try:
            async_exchange = ccxtpro.binance({
                'apiKey': API_KEYS['live']['api_key'], 'secret': API_KEYS['live']['api_secret'],
                'options': {'defaultType': 'future'}, 'enableRateLimit': True,
            })
            async_exchange.set_sandbox_mode(False)
            return await get_all_futures_symbols(async_exchange)
        finally:
            if async_exchange: await async_exchange.close()

    console.log("Fetching top symbols by volume...")
    all_symbols = asyncio.run(fetch_symbols_async())
    symbols_to_test = all_symbols[:args.max_symbols]
    console.log(f"Will run comparison across these {len(symbols_to_test)} symbols: {', '.join(symbols_to_test)}")

    # --- Inisialisasi exchange sinkron untuk fetching data historis ---
    import ccxt # type: ignore
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'}, 'enableRateLimit': True,
    })

    # --- REVISI BESAR: Loop melalui setiap strategi, jalankan simulasi portofolio penuh untuk masing-masing ---
    strategy_versions = STRATEGY_CONFIG
    all_results = [] # Akan menyimpan hasil dari setiap (strategi, simbol)
    all_data = {} # PERBAIKAN: Inisialisasi dictionary all_data

    for symbol in symbols_to_test:
        console.log(f"\n[bold]===== Processing Symbol: {symbol} =====[/bold]")
        
        # 1. Fetch data untuk simbol saat ini
        # Logika dinamis untuk mengambil data multi-timeframe
        signal_tf = CONFIG['timeframe_signal']
        trend_tf = CONFIG['timeframe_trend']

        # --- PERBAIKAN: Logika dinamis untuk macro_tf ---
        # Pastikan macro_tf selalu lebih tinggi dari trend_tf untuk menghindari duplikasi.
        if pd.to_timedelta(trend_tf) >= pd.to_timedelta('1h'):
            macro_tf = '4h' # Jika trend sudah 1h atau lebih, gunakan 4h untuk makro
        else:
            macro_tf = '1h' # Default makro adalah 1h

        limit_signal = args.limit
        buffer = 200
        limit_trend = (limit_signal // max(1, (pd.to_timedelta(trend_tf).total_seconds() / pd.to_timedelta(signal_tf).total_seconds()))) + buffer
        limit_macro = (limit_signal // max(1, (pd.to_timedelta(macro_tf).total_seconds() / pd.to_timedelta(signal_tf).total_seconds()))) + buffer

        df_signal, _ = fetch_binance_data_sync(exchange, symbol, signal_tf, limit=int(limit_signal), use_cache=True)
        df_trend, _ = fetch_binance_data_sync(exchange, symbol, trend_tf, limit=int(limit_trend), use_cache=True)
        df_macro, _ = fetch_binance_data_sync(exchange, symbol, macro_tf, limit=int(limit_macro), use_cache=True)

        if any(df is None or df.empty for df in [df_signal, df_trend, df_macro]):
            console.log(f"[yellow]Skipping {symbol} due to data fetching issues.[/yellow]")
            continue

        # 2. Prepare data
        df_signal = calculate_indicators(df_signal)
        df_trend = calculate_indicators(df_trend) # type: ignore
        df_macro = calculate_indicators(df_macro) # type: ignore
        
        prepared_data = prepare_data(df_signal, df_trend, df_macro) # type: ignore
        if prepared_data is None:
            console.log(f"[yellow]Skipping {symbol} due to data preparation issues.[/yellow]")
            continue
        
        all_data[symbol] = prepared_data
        
        # Jeda singkat untuk menghormati rate limit
        time.sleep(0.1)

    # --- REVISI BESAR: Jalankan simulasi portofolio untuk setiap strategi ---
    for strat_name, strat_config in strategy_versions.items():
        console.log(f"\n[bold magenta]===== Running Full Portfolio Simulation for: {strat_name} =====[/bold magenta]")
        
        # Buat instance backtester baru untuk setiap strategi untuk memastikan isolasi
        backtester = PortfolioBacktester(initial_balance=CONFIG["account_balance"])
        all_signals = []

        # Hasilkan sinyal HANYA untuk strategi saat ini di semua simbol
        for symbol, base_data in all_data.items():
            long_s, short_s, _ = strat_config["function"](base_data.copy())
            
            df_signals = base_data.copy()
            # PERBAIKAN: Inisialisasi kolom dengan dtype 'object' untuk mencegah FutureWarning
            df_signals['signal'] = pd.Series(np.nan, index=df_signals.index, dtype='object')
            df_signals.loc[long_s, 'signal'] = 'LONG'
            df_signals.loc[short_s, 'signal'] = 'SHORT'
            df_signals['strategy'] = strat_name
            df_signals['symbol'] = symbol

            signals_found = df_signals.dropna(subset=['signal'])
            if not signals_found.empty:
                all_signals.extend(signals_found.reset_index().to_dict('records'))

        # Jalankan simulasi kronologis dengan sinyal yang sudah difilter
        if all_signals:
            sorted_signals = sorted(all_signals, key=lambda x: x['timestamp'])
            all_timestamps = sorted(list(set(s['timestamp'] for s in sorted_signals)))

            for i in range(len(all_timestamps) - 1):
                current_time = all_timestamps[i]
                next_time = all_timestamps[i+1]
                
                # Temukan sinyal yang terjadi pada timestamp ini
                current_signals = [s for s in sorted_signals if s['timestamp'] == current_time]
                
                backtester.check_trades_and_orders(current_time, next_time, all_data)
                for signal in current_signals:
                    backtester.process_new_signal(signal, all_data)

            backtester.close_remaining_trades(all_data)

        # Kumpulkan hasil dari simulasi portofolio ini
        summary = backtester.get_results_summary()
        summary['version'] = strat_name
        all_results.append(summary)

    # --- Agregasi dan Tampilkan Hasil Akhir ---
    if all_results:
        results_df = pd.DataFrame(all_results)
        agg_metrics = results_df.sort_values(by='net_profit_pct', ascending=False)

        # --- PERBAIKAN: Gunakan Rich Table untuk output yang lebih rapi ---
        summary_table = Table(
            title="Portfolio Backtest Strategy Comparison (Aggregated Results)",
            show_header=True,
            header_style="bold magenta",
            expand=True
        )

        # Tambahkan kolom ke tabel
        summary_table.add_column("Strategy", style="cyan", no_wrap=True, min_width=25)
        summary_table.add_column("Total Trades", justify="right")
        summary_table.add_column("Win Rate", justify="right")
        summary_table.add_column("Profit Factor", justify="right")
        summary_table.add_column("Max Drawdown", justify="right")
        summary_table.add_column("Net PnL %", justify="right")

        # Tambahkan baris dari DataFrame yang sudah diagregasi
        for _, row in agg_metrics.iterrows():
            pnl_style = "green" if row['net_profit_pct'] > 0 else "red"
            summary_table.add_row(
                row['version'],
                f"{row['total_trades']:.0f}",
                f"{row['win_rate']:.2f}%",
                f"{row['profit_factor']:.2f}",
                f"[red]{row['max_drawdown']:.2f}%[/red]",
                f"[{pnl_style}]{row['net_profit_pct']:+.2f}%[/{pnl_style}]"
            )
        
        console.print(summary_table)

        # Simpan hasil agregasi
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        filename = output_dir / f"strategy_comparison_results.json"
        with open(filename, 'w') as f:
            results_df.to_json(f, orient='records', indent=2)
        console.log(f"\nSaved detailed results for all symbols to {filename}")

    console.log(f"\n✅ Backtest strategy comparison complete.")
