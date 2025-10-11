import argparse
import pandas as pd
import json
import numpy as np
from datetime import time
from pathlib import Path

from config import CONFIG
from indicators import fetch_binance_data, calculate_indicators
from utils.data_preparer import prepare_data
from strategies import STRATEGY_MAP

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
        self.risk_per_trade = risk_per_trade
        self.rr_ratio = rr_ratio

    def run(self, version_name, signal_function, base_data):
        self.balance = self.initial_balance
        self.trades = []
        self.in_position = False
        
        df = base_data.copy()
        long_signals, short_signals, exit_params = signal_function(df)
        df.loc[long_signals, 'signal'] = 'LONG'
        df.loc[short_signals, 'signal'] = 'SHORT'

        signals_df = df[df['signal'].isin(['LONG', 'SHORT'])].copy()

        if signals_df.empty:
            return self.get_results(version_name)

        for _, row in signals_df.iterrows():
            if not self.in_position:
                self.simulate_trade(row, base_data, exit_params)

        return self.get_results(version_name)

    def simulate_trade(self, signal_row, full_data, exit_params):
        self.in_position = True
        entry_price = signal_row['close']
        direction = signal_row['signal']
        atr_val = signal_row[f"ATRr_{CONFIG['atr_period']}"]
        
        # Ambil parameter SL/TP dari dictionary exit_params
        sl_multiplier = exit_params['sl_multiplier']
        rr_ratio = exit_params['rr_ratio']

        # --- REVISI: Handle numpy array dari strategi dinamis ---
        # Jika multiplier adalah array/series, ambil nilai yang sesuai dengan indeks sinyal
        if isinstance(sl_multiplier, pd.Series):
            sl_multiplier = sl_multiplier.loc[signal_row.name]
        elif isinstance(sl_multiplier, np.ndarray):
            # Untuk numpy array, kita butuh indeks integer, bukan timestamp
            idx = full_data.index.get_loc(signal_row.name)
            sl_multiplier = sl_multiplier[idx]
        if isinstance(rr_ratio, pd.Series):
            rr_ratio = rr_ratio.loc[signal_row.name]
        elif isinstance(rr_ratio, np.ndarray):
            # Also handle numpy array for rr_ratio
            idx = full_data.index.get_loc(signal_row.name)
            rr_ratio = rr_ratio[idx]

        stop_loss_dist = atr_val * sl_multiplier
        take_profit_dist = stop_loss_dist * rr_ratio

        if direction == 'LONG':
            stop_loss_price = entry_price - stop_loss_dist
            take_profit_price = entry_price + take_profit_dist
        else: # SHORT
            stop_loss_price = entry_price + stop_loss_dist
            take_profit_price = entry_price - take_profit_dist

        future_candles = full_data.loc[signal_row.name:].iloc[1:]
        
        # --- REVISI: Handle sinyal pada candle terakhir ---
        # Jika tidak ada candle masa depan, lewati trade ini.
        if future_candles.empty:
            self.in_position = False
            return

        # --- REVISI: Logika exit yang lebih canggih ---
        exit_reason = "End of Data"
        exit_price = future_candles.iloc[-1]['close']
        exit_time = future_candles.index[-1]

        for idx, candle in future_candles.iterrows():
            # Trailing Stop Logic
            if exit_params.get('trailing_atr', False):
                trail_dist = candle[f"ATRr_{CONFIG['atr_period']}"] * exit_params.get('atr_trail_mult', 1.2)
                if direction == 'LONG':
                    new_sl = candle['high'] - trail_dist
                    stop_loss_price = max(stop_loss_price, new_sl)
                else: # SHORT
                    new_sl = candle['low'] + trail_dist
                    stop_loss_price = min(stop_loss_price, new_sl)

            # Check SL Hit
            if (direction == 'LONG' and candle['low'] <= stop_loss_price) or \
               (direction == 'SHORT' and candle['high'] >= stop_loss_price):
                exit_price = stop_loss_price
                exit_time = idx
                exit_reason = "Stop Loss"
                break

            # Check TP Hit
            if (direction == 'LONG' and candle['high'] >= take_profit_price) or \
               (direction == 'SHORT' and candle['low'] <= take_profit_price):
                exit_price = take_profit_price
                exit_time = idx
                exit_reason = "Take Profit"
                break

            # Volume Fade Exit Logic
            if exit_params.get('exit_on_vol_drop', False):
                if candle['volume'] < (candle[f"VOL_{CONFIG['volume_lookback']}"] * 0.8):
                    exit_price = candle['close']
                    exit_time = idx
                    exit_reason = "Volume Fade"
                    break
        
        # --- REVISI: Kalkulasi PnL berdasarkan exit price ---
        # Apply slippage
        slippage = exit_params.get('slippage_sensitivity', 0.0)
        if direction == 'LONG': # Selling to close
            exit_price *= (1 - slippage)
        else: # Buying to close
            exit_price *= (1 + slippage)

        if direction == 'LONG':
            pnl = (exit_price - entry_price) / entry_price * self.initial_balance
        else: # SHORT
            pnl = (entry_price - exit_price) / entry_price * self.initial_balance

        # Simplified PnL for now, not using full contract size logic
        outcome = "WIN" if pnl > 0 else "LOSS"

        self.balance += pnl
        self.trades.append({
            "outcome": outcome, "pnl": pnl, "entry_time": signal_row.name, 
            "exit_time": exit_time, "exit_reason": exit_reason,
            "sl_dist": stop_loss_dist, "tp_dist": take_profit_dist,
        })
        self.in_position = False

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
        start_time = self.trades[0]['entry_time']
        end_time = self.trades[-1]['exit_time']
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
    parser = argparse.ArgumentParser(description="Comparative Backtester for Trading Strategies")
    parser.add_argument("--symbol", type=str, default="BTC/USDT", help="Trading symbol (e.g., BTC/USDT)")
    parser.add_argument("--limit", type=int, default=1500, help="Number of 5m candles to backtest")
    args = parser.parse_args()

    # 1. Fetch all required data once
    # Correctly scale the limit for different timeframes to cover the same time duration
    limit_5m = args.limit
    # For 15m data, we need 1/3rd the number of candles to cover the same period (5m * 3 = 15m)
    limit_15m = (limit_5m // 3) + 5 # Add a small buffer
    # For 1h data, we need 1/12th the number of candles (5m * 12 = 1h)
    limit_1h = (limit_5m // 12) + 5 # Add a small buffer

    # --- PERBAIKAN KONSISTENSI ---
    import ccxt
    from config import API_KEYS
    exchange = ccxt.binance({
        'apiKey': API_KEYS['live']['api_key'],
        'secret': API_KEYS['live']['api_secret'],
        'options': {'defaultType': 'future'},
        'enableRateLimit': True,
        'test': False,
    })
    exchange.set_sandbox_mode(False)

    import asyncio
    print(f"Fetching {limit_5m} candles for 5m, {limit_15m} for 15m, and {limit_1h} for 1h...")

    df_5m = asyncio.run(fetch_binance_data(exchange, args.symbol, '5m', limit=limit_5m, use_cache=True)) if exchange else None
    df_15m = asyncio.run(fetch_binance_data(exchange, args.symbol, '15m', limit=limit_15m, use_cache=True)) if exchange else None
    df_1h = asyncio.run(fetch_binance_data(exchange, args.symbol, '1h', limit=limit_1h, use_cache=True)) if exchange else None

    if any(df is None for df in [df_5m, df_15m, df_1h]):
        print("Failed to fetch all required data. Exiting.")
        exit()

    # 2. Prepare a single, rich DataFrame
    base_data = prepare_data(df_5m, df_15m, df_1h)

    # 3. Define strategy versions to test
    strategy_versions = STRATEGY_MAP

    # 4. Run backtest for each version
    all_summary_results = []
    all_detailed_metrics = []
    all_json_logs = []

    backtester = Backtester(
        symbol=args.symbol,
        initial_balance=CONFIG["account_balance"],
        risk_per_trade=CONFIG["risk_per_trade"],
        rr_ratio=CONFIG["risk_reward_ratio"]
    )

    for name, func in strategy_versions.items():
        print(f"\n--- Running Backtest for Version: {name} ---")
        summary, detailed, json_log = backtester.run(name, func, base_data)
        if summary:
            all_summary_results.append(summary)
        if detailed:
            all_detailed_metrics.append(detailed)
        if json_log:
            all_json_logs.append(json_log)

    # 5. Display final comparison tables
    if all_summary_results:
        summary_df = pd.DataFrame(all_summary_results)
        header = " BACKTEST RESULTS (SUMMARY) "
        print("\n\n" + "="*80)
        print(f"{header:=^80}")
        print("="*80)
        print(summary_df.to_string(index=False))
        print("="*80)

    if all_detailed_metrics:
        detailed_df = pd.DataFrame(all_detailed_metrics)
        header = " PERFORMANCE METRICS (DETAILED) "
        print("\n" + "="*80)
        print(f"{header:=^80}")
        print("="*80)
        print(detailed_df.to_string(index=False))
        print("="*80)

    # 6. Save all metrics to a single JSON file
    if all_json_logs:
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        filename = output_dir / f"metrics_{args.symbol.replace('/', '')}.json"
        with open(filename, 'w') as f:
            json.dump(all_json_logs, f, indent=2)
        print(f"\nSaved all detailed metrics to {filename}")

    print(f"\n✅ Backtest strategy comparison complete. Run 'python backtest_analyzer/evaluate_strategy_comparation.py {filename}' for advanced risk analysis.")
