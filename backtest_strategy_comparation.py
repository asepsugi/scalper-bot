import argparse
import pandas as pd
import json
import numpy as np
from datetime import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
import asyncio

from config import CONFIG, LIVE_TRADING_CONFIG, FEES, SLIPPAGE
from indicators import fetch_binance_data_sync, calculate_indicators
from utils.data_preparer import prepare_data
from utils.common_utils import get_all_futures_symbols
from strategies import STRATEGY_CONFIG

def evaluate_statistical_validity(metrics):
    """Analyzes a single strategy's metrics for statistical validity and effectiveness."""
    trade_count = metrics.get("total_trades", 0)
    pf = metrics.get("profit_factor", 0)
    dd = metrics.get("max_drawdown", 100)
    rr = metrics.get("avg_rr", 0)
    win = metrics.get("win_rate", 0)

    # Step 1: Determine sample validity rating
    if trade_count < 30:
        metrics["sample_validity"] = "❌ Insufficient (<30)"
        metrics["validity_score"] = 0.2
    elif trade_count < 100:
        metrics["sample_validity"] = "⚠️ Moderate (30-100)"
        metrics["validity_score"] = 0.6
    elif trade_count < 300:
        metrics["sample_validity"] = "✅ Strong (100-300)"
        metrics["validity_score"] = 0.85
    else:
        metrics["sample_validity"] = "🔥 Excellent (>300)"
        metrics["validity_score"] = 1.0

    # Step 2: Determine strategy efficiency
    if pf >= 1.5 and win >= 55 and dd <= 5:
        metrics["strategy_efficiency"] = "✅ Efficient & Profitable"
    elif pf >= 1.2 and win >= 50:
        metrics["strategy_efficiency"] = "⚠️ Moderate Efficiency"
    else:
        metrics["strategy_efficiency"] = "❌ Inefficient / Overfiltered"

    # Step 3: Classify strategy type
    if trade_count < 30 and pf > 2:
        metrics["strategy_type"] = "Swing-like"
    elif 30 <= trade_count <= 120:
        metrics["strategy_type"] = "Balanced Scalper"
    else:
        metrics["strategy_type"] = "High-Frequency Scalper"

    # Step 4: Calculate final effectiveness score
    # Normalize metrics to avoid extreme values skewing the score
    pf_score = min(pf, 5) / 5
    rr_score = min(rr, 3) / 3
    dd_score = (100 - min(dd, 100)) / 100
    win_score = min(win, 100) / 100

    metrics["effectiveness_score"] = round(
        (metrics["validity_score"] * 0.4) +
        (pf_score * 0.25) +
        (rr_score * 0.15) +
        (dd_score * 0.1) +
        (win_score * 0.1),
        3
    )
    return metrics

def strategy_recommendation(metrics):
    """Provides an optimization recommendation based on performance metrics."""
    if metrics["total_trades"] < 30:
        return "Increase trade frequency by relaxing entry filters (e.g., adjust RSI thresholds or EMA gaps)."
    elif metrics["effectiveness_score"] >= 0.7:
        return "Strategy appears stable. Proceed with forward testing on different market periods."
    else:
        return "Requires re-optimization of signal filters or multi-timeframe alignment."

class Backtester:
    def __init__(self, symbol, initial_balance, risk_per_trade, rr_ratio):
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.rr_ratio = rr_ratio
        self.trades = []
        self.trade_id_counter = 0
        self.active_position = None # Hanya satu posisi aktif pada satu waktu untuk perbandingan
        self.pending_order = None # Hanya satu pending order pada satu waktu

    def run(self, version_name, signal_function, base_data):
        self.balance = self.initial_balance
        self.trades = []
        self.active_position = None
        self.pending_order = None
        self.trade_id_counter = 0
        
        df = base_data.copy()
        long_signals, short_signals, exit_params = signal_function(df)
        df.loc[long_signals, 'signal'] = 'LONG'
        df.loc[short_signals, 'signal'] = 'SHORT'

        all_signals = df[df['signal'].isin(['LONG', 'SHORT'])].copy()
        if all_signals.empty:
            return self.get_results(version_name)

        # --- REVISI: Implementasi simulasi kronologis seperti market_scanner ---
        sorted_timestamps = sorted(list(df.index))

        for i in range(len(sorted_timestamps) - 1):
            current_time = sorted_timestamps[i]
            next_time = sorted_timestamps[i+1]

            # A. Periksa exit, trailing stop, dan pending order
            self.check_trade_and_order(current_time, next_time, df)

            # B. Proses sinyal baru yang muncul pada timestamp ini
            if current_time in all_signals.index:
                signal_row = all_signals.loc[current_time]
                # Hanya proses jika tidak ada posisi aktif atau pending order
                if not self.active_position and not self.pending_order:
                    self.create_pending_order(signal_row, df, exit_params)

        # Tutup posisi yang masih terbuka di akhir data
        if self.active_position:
            last_candle = df.iloc[-1]
            self.close_trade(last_candle['close'], last_candle.name, "End of Data")

        return self.get_results(version_name)

    def create_pending_order(self, signal_row, full_data, exit_params):
        """Membuat pending order, meniru logika market_scanner."""
        signal_price = signal_row['close']
        direction = signal_row['signal']
        atr_val = signal_row[f"ATRr_{CONFIG['atr_period']}"]

        limit_offset_pct = 0.001
        limit_price = signal_price * (1 - limit_offset_pct) if direction == 'LONG' else signal_price * (1 + limit_offset_pct)
        expiration_candles = 10

        sl_multiplier = exit_params['sl_multiplier']
        rr_ratio = exit_params['rr_ratio']

        # --- PERBAIKAN: Tangani parameter dinamis (Series atau ndarray) ---
        # Beberapa strategi mengembalikan SL/TP sebagai array untuk setiap candle.
        # Kita perlu mengambil nilai yang sesuai dengan timestamp sinyal saat ini.
        if isinstance(sl_multiplier, (pd.Series, np.ndarray)):
            # Dapatkan posisi integer dari timestamp sinyal di dalam DataFrame
            idx_pos = full_data.index.get_loc(signal_row.name)
            sl_multiplier = sl_multiplier[idx_pos] if isinstance(sl_multiplier, np.ndarray) else sl_multiplier.iloc[idx_pos]
        if isinstance(rr_ratio, (pd.Series, np.ndarray)):
            idx_pos = full_data.index.get_loc(signal_row.name)
            rr_ratio = rr_ratio[idx_pos] if isinstance(rr_ratio, np.ndarray) else rr_ratio.iloc[idx_pos]

        stop_loss_dist = atr_val * sl_multiplier
        if stop_loss_dist <= 0: return

        risk_amount_usd = self.balance * self.risk_per_trade
        stop_loss_pct = stop_loss_dist / limit_price
        if stop_loss_pct <= 0: return

        position_size_usd = risk_amount_usd / stop_loss_pct

        stop_loss_price = limit_price - stop_loss_dist if direction == 'LONG' else limit_price + stop_loss_dist
        take_profit_price = limit_price + (stop_loss_dist * rr_ratio) if direction == 'LONG' else limit_price - (stop_loss_dist * rr_ratio)
        
        timeframe_duration = pd.to_timedelta(CONFIG['timeframe_signal'])
        expiration_time = signal_row.name + (timeframe_duration * expiration_candles)

        self.pending_order = {
            'limit_price': limit_price, 'direction': direction,
            'sl_price': stop_loss_price, 'initial_sl': stop_loss_price,
            'tp_price': take_profit_price, 'position_size_usd': position_size_usd,
            'expiration_time': expiration_time
        }

    def check_trade_and_order(self, start_time, end_time, full_data):
        """Memeriksa exit untuk posisi aktif dan fill untuk pending order."""
        # 1. Periksa Posisi Aktif untuk Exit
        if self.active_position:
            candles_to_check = full_data.loc[start_time:end_time].iloc[1:]
            if candles_to_check.empty: return

            exit_reason = None
            for idx, candle in candles_to_check.iterrows():
                # Logika Trailing Stop (jika diaktifkan)
                if LIVE_TRADING_CONFIG.get("trailing_sl_enabled", False):
                    is_trailing_active = self.active_position.get('trailing_sl_active', False)
                    risk_distance = abs(self.active_position['entry_price'] - self.active_position['initial_sl'])
                    if risk_distance > 0:
                        current_rr = abs(candle['close'] - self.active_position['entry_price']) / risk_distance
                        if not is_trailing_active and current_rr >= LIVE_TRADING_CONFIG.get("trailing_sl_trigger_rr", 1.0):
                            self.active_position['trailing_sl_active'] = True
                            is_trailing_active = True
                    
                    if is_trailing_active:
                        atr_val = candle[f"ATRr_{CONFIG['atr_period']}"]
                        trail_dist = atr_val * LIVE_TRADING_CONFIG.get("trailing_sl_distance_atr", 1.5)
                        if self.active_position['direction'] == 'LONG':
                            self.active_position['sl_price'] = max(self.active_position['sl_price'], candle['close'] - trail_dist)
                        else:
                            self.active_position['sl_price'] = min(self.active_position['sl_price'], candle['close'] + trail_dist)

                current_sl_price = self.active_position['sl_price']
                
                # Logika Exit berdasarkan penutupan candle
                if (self.active_position['direction'] == 'LONG' and candle['close'] <= current_sl_price) or \
                   (self.active_position['direction'] == 'SHORT' and candle['close'] >= current_sl_price):
                    exit_price, exit_time, exit_reason = candle['close'], idx, "Stop Loss (Close)"
                    break
                
                if not self.active_position.get('trailing_sl_active', False) and \
                   ((self.active_position['direction'] == 'LONG' and candle['close'] >= self.active_position['tp_price']) or \
                   (self.active_position['direction'] == 'SHORT' and candle['close'] <= self.active_position['tp_price'])):
                    exit_price, exit_time, exit_reason = candle['close'], idx, "Take Profit (Close)"
                    break
            
            if exit_reason:
                self.close_trade(exit_price, exit_time, exit_reason)

        # 2. Periksa Pending Order untuk Fill atau Expiry
        elif self.pending_order:
            if end_time > self.pending_order['expiration_time']:
                self.pending_order = None # Order kedaluwarsa
                return

            candles_to_check = full_data.loc[start_time:end_time].iloc[1:]
            for fill_time, candle in candles_to_check.iterrows():
                if (self.pending_order['direction'] == 'LONG' and candle['low'] <= self.pending_order['limit_price']) or \
                   (self.pending_order['direction'] == 'SHORT' and candle['high'] >= self.pending_order['limit_price']):
                    self.open_trade(self.pending_order, fill_time)
                    self.pending_order = None
                    break

    def open_trade(self, order_details, fill_time):
        """Membuka posisi dari pending order yang terisi."""
        self.trade_id_counter += 1
        entry_price = order_details['limit_price'] * (1 + SLIPPAGE['pct'] if order_details['direction'] == 'LONG' else 1 - SLIPPAGE['pct'])
        entry_fee = order_details['position_size_usd'] * FEES['maker']

        self.active_position = {
            'id': self.trade_id_counter, 'entry_time': fill_time,
            'entry_price': entry_price, 'entry_fee': entry_fee, **order_details
        }

    def close_trade(self, exit_price, exit_time, exit_reason):
        """Menutup posisi aktif dan mencatat hasilnya."""
        if not self.active_position: return

        trade = self.active_position
        direction = trade['direction']
        entry_price = trade['entry_price']
        position_size_usd = trade['position_size_usd']

        actual_exit_price = exit_price * (1 - SLIPPAGE['pct'] if direction == 'LONG' else 1 + SLIPPAGE['pct'])
        exit_fee_rate = FEES['maker'] if exit_reason == 'Take Profit (Close)' else FEES['taker']
        exit_fee = position_size_usd * exit_fee_rate
        total_fees = trade['entry_fee'] + exit_fee

        pnl_pct = (actual_exit_price - entry_price) / entry_price if direction == 'LONG' else (entry_price - actual_exit_price) / entry_price
        pnl_usd = pnl_pct * position_size_usd
        net_pnl_usd = pnl_usd - total_fees

        self.balance += net_pnl_usd
        outcome = "WIN" if net_pnl_usd > 0 else "LOSS"

        self.trades.append({
            "outcome": outcome, "pnl": net_pnl_usd, "entry_time": trade['entry_time'], 
            "exit_time": exit_time, "exit_reason": exit_reason,
            "sl_dist": abs(trade['entry_price'] - trade['initial_sl']), 
            "tp_dist": abs(trade['tp_price'] - trade['entry_price']),
        })
        self.active_position = None

    def get_results(self, version_name):
        total_trades = len(self.trades)
        if total_trades == 0:
            summary_results = {
                "Version": version_name,
                "Duration": "N/A",
                "Net Profit": "0.00%",
                "Win Rate": "0.00%",
                "Trades": 0,
                "Final Balance": f"{self.initial_balance:,.2f}",
            }
            # Return 3 values to match the expected unpacking, even if some are None
            return summary_results, None, None

        # --- Calculate Backtest Duration ---
        trades_df = pd.DataFrame(self.trades)
        trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])
        trades_df['exit_time'] = pd.to_datetime(trades_df['exit_time'])
        start_time = trades_df['entry_time'].min()
        end_time = trades_df['exit_time'].max()
        duration_days = (end_time - start_time).days

        # --- Performance Metrics Calculation ---
        trades_df = pd.DataFrame(self.trades)
        wins = len(trades_df[trades_df['outcome'] == 'WIN'])
        win_rate = (wins / total_trades) * 100
        net_profit_pct = ((self.balance - self.initial_balance) / self.initial_balance) * 100

        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = trades_df[trades_df['pnl'] < 0]['pnl'].sum()
        profit_factor = gross_profit / abs(gross_loss) if gross_loss != 0 else float('inf')

        trades_df['rr'] = trades_df['tp_dist'] / trades_df['sl_dist'].replace(0, np.nan)
        avg_rr = trades_df['rr'].mean()

        equity = (self.initial_balance + trades_df['pnl'].cumsum())
        peak = equity.cummax()
        drawdown = (peak - equity) / peak
        max_drawdown = drawdown.max() * 100

        trades_df['duration'] = (trades_df['exit_time'] - trades_df['entry_time']).dt.total_seconds() / 60
        avg_trade_duration = trades_df['duration'].mean()

        daily_returns = trades_df.set_index('exit_time')['pnl'].resample('D').sum() / self.initial_balance
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(365) if daily_returns.std() != 0 else 0

        # --- Format Results ---
        summary_results = {
            "Version": version_name,
            "Duration": f"{duration_days}d",
            "Net Profit": f"{net_profit_pct:.2f}%",
            "Win Rate": f"{win_rate:.2f}%",
            "Trades": total_trades,
            "Final Balance": f"{self.balance:,.2f}",
        }
        
        detailed_metrics = {
            "Version": version_name, "Avg RR": f"{avg_rr:.2f}", "Profit Factor": f"{profit_factor:.2f}",
            "Max DD": f"{max_drawdown:.2f}%", "Sharpe": f"{sharpe_ratio:.2f}", "Avg Duration": f"{avg_trade_duration:.0f}m"
        }

        # --- JSON Logging ---
        json_log = {
            "version": version_name, "symbol": self.symbol,
            "net_profit_pct": round(net_profit_pct, 2), "win_rate": round(win_rate, 2),
            "total_trades": total_trades, "avg_rr": round(avg_rr, 2),
            "profit_factor": round(profit_factor, 2), "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2), "avg_trade_duration": round(avg_trade_duration, 2),
            "final_balance": round(self.balance, 2)
        }
        
        return summary_results, detailed_metrics, json_log


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
    import ccxt
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'}, 'enableRateLimit': True,
    })

    # --- REVISI BESAR: Loop melalui setiap strategi dan setiap simbol ---
    strategy_versions = STRATEGY_CONFIG
    all_results = [] # Akan menyimpan hasil dari setiap (strategi, simbol)

    for symbol in symbols_to_test:
        console.log(f"\n[bold]===== Processing Symbol: {symbol} =====[/bold]")
        
        # 1. Fetch data untuk simbol saat ini
        limit_5m = args.limit
        buffer = 200
        limit_15m = (limit_5m // 3) + buffer
        limit_1h = (limit_5m // 12) + buffer

        df_5m, _ = fetch_binance_data_sync(exchange, symbol, '5m', limit=limit_5m, use_cache=True)
        df_15m, _ = fetch_binance_data_sync(exchange, symbol, '15m', limit=limit_15m, use_cache=True)
        df_1h, _ = fetch_binance_data_sync(exchange, symbol, '1h', limit=limit_1h, use_cache=True)

        if any(df is None or df.empty for df in [df_5m, df_15m, df_1h]):
            console.log(f"[yellow]Skipping {symbol} due to data fetching issues.[/yellow]")
            continue

        # 2. Prepare data
        df_5m = calculate_indicators(df_5m)
        df_15m = calculate_indicators(df_15m)
        df_1h = calculate_indicators(df_1h)
        base_data = prepare_data(df_5m, df_15m, df_1h)
        if base_data is None:
            console.log(f"[yellow]Skipping {symbol} due to data preparation issues.[/yellow]")
            continue

        # 3. Jalankan backtest untuk setiap strategi pada simbol ini
        for name, config in strategy_versions.items():
            console.log(f"--- Running backtest for [cyan]{name}[/cyan] on [yellow]{symbol}[/yellow] ---")
            backtester = Backtester(
                symbol=symbol,
                initial_balance=CONFIG["account_balance"],
                risk_per_trade=CONFIG["risk_per_trade"],
                rr_ratio=CONFIG["risk_reward_ratio"]
            )
            func = config['function']
            _, _, json_log = backtester.run(name, func, base_data)
            
            if json_log:
                all_results.append(json_log)

    # --- REVISI BESAR: Agregasi dan Tampilkan Hasil Akhir ---
    if all_results:
        results_df = pd.DataFrame(all_results)

        # Agregasi metrik per strategi di semua simbol
        agg_metrics = results_df.groupby('version').agg(
            total_pnl_pct=('net_profit_pct', 'sum'),
            avg_win_rate=('win_rate', 'mean'),
            avg_pf=('profit_factor', lambda x: x[np.isfinite(x)].mean()), # Rata-rata profit factor yang valid
            avg_dd=('max_drawdown', 'mean'),
            total_trades=('total_trades', 'sum'),
            num_symbols_tested=('symbol', 'nunique')
        ).reset_index()

        agg_metrics = agg_metrics.sort_values(by='total_pnl_pct', ascending=False)

        # --- PERBAIKAN: Gunakan Rich Table untuk output yang lebih rapi ---
        summary_table = Table(
            title="Portfolio Backtest Strategy Comparison (Aggregated Results)",
            show_header=True,
            header_style="bold magenta",
            expand=True
        )

        # Tambahkan kolom ke tabel
        summary_table.add_column("Strategy", style="cyan", no_wrap=True, min_width=25)
        summary_table.add_column("Symbols Tested", justify="right")
        summary_table.add_column("Total Trades", justify="right")
        summary_table.add_column("Avg Win Rate", justify="right")
        summary_table.add_column("Avg Profit Factor", justify="right")
        summary_table.add_column("Avg Max Drawdown", justify="right")
        summary_table.add_column("Total PnL %", justify="right")

        # Tambahkan baris dari DataFrame yang sudah diagregasi
        for _, row in agg_metrics.iterrows():
            pnl_style = "green" if row['total_pnl_pct'] > 0 else "red"
            summary_table.add_row(
                row['version'],
                f"{row['num_symbols_tested']:.0f}",
                f"{row['total_trades']:.0f}",
                f"{row['avg_win_rate']:.2f}%",
                f"{row['avg_pf']:.2f}",
                f"[red]{row['avg_dd']:.2f}%[/red]",
                f"[{pnl_style}]{row['total_pnl_pct']:+.2f}%[/{pnl_style}]"
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
