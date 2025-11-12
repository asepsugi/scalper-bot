import pandas as pd
import numpy as np
from rich.console import Console
from datetime import datetime
from pathlib import Path

from config import CONFIG, FEES, SLIPPAGE, LEVERAGE_MAP, LIVE_TRADING_CONFIG
from utils.common_utils import get_dynamic_risk_params
from indicators import fetch_binance_data_sync, calculate_indicators
from utils.data_preparer import prepare_data
from strategies import STRATEGY_CONFIG
from rich.table import Table

console = Console()

class PortfolioBacktester:
    """
    A backtester that manages a single compounding portfolio across multiple assets and strategies.
    This class is the core engine for both market_scanner and strategy_comparation.
    """
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.trades = []
        self.trade_id_counter = 0
        self.active_positions = {} # symbol -> trade_details
        self.pending_orders = {} # symbol -> pending_order_details
        # --- FITUR BARU: Lacak waktu trade terakhir untuk cooldown ---
        self.last_trade_time = {} # symbol -> timestamp
        self.exchange = None # Akan diinisialisasi oleh skrip pemanggil

    def fetch_and_prepare_symbol_data(self, symbol, limit):
        """Helper function to fetch and prepare data for a single symbol."""
        buffer = 200 
        signal_tf = CONFIG['timeframe_signal']
        trend_tf = CONFIG['timeframe_trend']
        
        if pd.to_timedelta(trend_tf) >= pd.to_timedelta('1h'):
            macro_tf = '4h'
        else:
            macro_tf = '1h'

        limit_signal = limit
        limit_trend = (limit_signal // max(1, (pd.to_timedelta(trend_tf).total_seconds() / pd.to_timedelta(signal_tf).total_seconds()))) + buffer
        limit_macro = (limit_signal // max(1, (pd.to_timedelta(macro_tf).total_seconds() / pd.to_timedelta(signal_tf).total_seconds()))) + buffer

        df_signal, from_cache_signal = fetch_binance_data_sync(self.exchange, symbol, signal_tf, limit=int(limit_signal), use_cache=True)
        df_trend, from_cache_trend = fetch_binance_data_sync(self.exchange, symbol, trend_tf, limit=int(limit_trend), use_cache=True)
        df_macro, from_cache_macro = fetch_binance_data_sync(self.exchange, symbol, macro_tf, limit=int(limit_macro), use_cache=True)

        if any(df is None for df in [df_signal, df_trend, df_macro]):
            return None, False

        df_signal = calculate_indicators(df_signal)
        df_trend = calculate_indicators(df_trend)
        df_macro = calculate_indicators(df_macro)
        base_data = prepare_data(df_signal, df_trend, df_macro)
        was_api_call = not (from_cache_signal and from_cache_trend and from_cache_macro)
        return base_data, not was_api_call

    def process_new_signal(self, signal, all_data):
        """Memproses satu sinyal baru: validasi dan buat pending order."""
        symbol = signal['symbol']
        strategy_name = signal['strategy']
        signal_time = pd.to_datetime(signal['timestamp'], utc=True)

        # --- FITUR BARU: Filter Cooldown ---
        cooldown_minutes = LIVE_TRADING_CONFIG.get('trade_cooldown_minutes', 60)
        last_trade_t = self.last_trade_time.get(symbol)
        if last_trade_t and (signal_time - last_trade_t) < pd.Timedelta(minutes=cooldown_minutes):
            # console.log(f"[grey50]Skipping signal for {symbol}: Cooldown period active.[/grey50]")
            return
        # --- Akhir Filter Cooldown ---

        if symbol in self.active_positions or symbol in self.pending_orders:
            return

        full_data = all_data[symbol]
        try:
            signal_row = full_data.loc[signal_time]
        except KeyError:
            return
        
        signal_row_dict = signal_row.to_dict()
        signal_row_dict['signal'] = signal['signal']
        signal_row_dict['strategy'] = strategy_name
        
        # Dapatkan exit_params dari strategi yang relevan
        signal_function = STRATEGY_CONFIG[strategy_name]['function']
        _, _, exit_params = signal_function(full_data)

        risk_params = get_dynamic_risk_params(self.balance)
        current_risk_per_trade = risk_params['risk_per_trade']
        default_leverage = risk_params['default_leverage']

        self.create_pending_order(signal_row_dict, signal_time, full_data, exit_params, symbol, current_risk_per_trade, default_leverage)

    def check_trades_and_orders(self, start_time, end_time, all_data):
        """
        Optimized function to check for trade exits and pending order fills
        only within the new candle range (start_time to end_time).
        """
        closed_symbols = []
        for symbol, trade_details in list(self.active_positions.items()):
            full_data = all_data.get(symbol)
            if full_data is None: continue

            check_start = max(start_time, trade_details['entry_time'])
            if end_time <= check_start: continue

            candles_to_check = full_data.loc[check_start:end_time].iloc[1:]
            if candles_to_check.empty: continue

            exit_reason = None
            exit_price = None
            exit_time = None
            for idx, candle in candles_to_check.iterrows():
                if LIVE_TRADING_CONFIG.get("trailing_sl_enabled", False):
                    is_trailing_active = trade_details.get('trailing_sl_active', False)
                    risk_distance = abs(trade_details['entry_price'] - trade_details['initial_sl'])
                    if risk_distance > 0:
                        current_rr = abs(candle['close'] - trade_details['entry_price']) / risk_distance
                        if not is_trailing_active and current_rr >= LIVE_TRADING_CONFIG.get("trailing_sl_trigger_rr", 1.0):
                            trade_details['trailing_sl_active'] = True
                            is_trailing_active = True
                    
                    if is_trailing_active:
                        atr_val = candle[f"ATRr_{CONFIG['atr_period']}"]
                        trail_dist = atr_val * LIVE_TRADING_CONFIG.get("trailing_sl_distance_atr", 1.5)
                        if trade_details['direction'] == 'LONG':
                            trade_details['sl_price'] = max(trade_details['sl_price'], candle['close'] - trail_dist)
                        else:
                            trade_details['sl_price'] = min(trade_details['sl_price'], candle['close'] + trail_dist)

                cb_multiplier = LIVE_TRADING_CONFIG.get("circuit_breaker_multiplier", 1.5)
                sl_breach_threshold = abs(trade_details['entry_price'] - trade_details['initial_sl']) * (cb_multiplier - 1.0)
                
                price_breached = False
                if trade_details['direction'] == 'LONG' and candle['low'] < (trade_details['sl_price'] - sl_breach_threshold):
                    price_breached = True
                    exit_price = trade_details['sl_price'] - sl_breach_threshold
                elif trade_details['direction'] == 'SHORT' and candle['high'] > (trade_details['sl_price'] + sl_breach_threshold):
                    price_breached = True
                    exit_price = trade_details['sl_price'] + sl_breach_threshold

                if price_breached:
                    avg_volume = full_data.loc[idx, f"VOL_{CONFIG['volume_lookback']}"]
                    if candle['volume'] > (avg_volume * 2.0):
                        exit_time = idx
                        exit_reason = "Circuit Breaker"
                        break

                current_sl_price = trade_details['sl_price']
                
                if (trade_details['direction'] == 'LONG' and candle['close'] <= current_sl_price) or \
                   (trade_details['direction'] == 'SHORT' and candle['close'] >= current_sl_price):
                    exit_price, exit_time, exit_reason = candle['close'], idx, "Stop Loss (Close)"
                    break
                
                if not trade_details.get('trailing_sl_active', False) and \
                   ((trade_details['direction'] == 'LONG' and candle['close'] >= trade_details['tp_price']) or \
                   (trade_details['direction'] == 'SHORT' and candle['close'] <= trade_details['tp_price'])):
                    exit_price, exit_time, exit_reason = candle['close'], idx, "Take Profit (Close)"
                    break
            
            if exit_reason:
                self.close_trade(symbol, exit_price, exit_time, exit_reason)
                closed_symbols.append(symbol)

        for symbol in closed_symbols:
            if symbol in self.active_positions:
                del self.active_positions[symbol]
        
        filled_symbols = []
        expired_symbols = []
        for symbol, order_details in list(self.pending_orders.items()):
            full_data = all_data.get(symbol)
            if full_data is None: continue
            
            if end_time > order_details['expiration_time']:
                expired_symbols.append(symbol)
                continue

            candles_to_check = full_data.loc[start_time:end_time].iloc[1:]
            for fill_time, candle in candles_to_check.iterrows():
                if (order_details['direction'] == 'LONG' and candle['low'] <= order_details['limit_price']) or \
                   (order_details['direction'] == 'SHORT' and candle['high'] >= order_details['limit_price']):
                    self.open_trade(symbol, order_details, fill_time=fill_time)
                    filled_symbols.append(symbol)
                    break

        for symbol in filled_symbols + expired_symbols:
            if symbol in self.pending_orders:
                if symbol in expired_symbols:
                    console.log(f"[yellow]Pending order for {symbol} expired at {end_time}.[/yellow]")
                del self.pending_orders[symbol]

    def open_trade(self, symbol, order_details, fill_time):
        if symbol in self.active_positions: return

        entry_price = order_details['limit_price'] * (1 + SLIPPAGE['pct'] if order_details['direction'] == 'LONG' else 1 - SLIPPAGE['pct'])
        entry_fee = order_details['position_size_usd'] * FEES['maker']

        self.trade_id_counter += 1
        console.log(
            f"[green]Opening trade {self.trade_id_counter} on {symbol} ({order_details['strategy']}). "
            f"Limit: {order_details['limit_price']:.5f}, Entry (w/ slippage): {entry_price:.5f}[/green]"
        )

        self.active_positions[symbol] = {
            'id': self.trade_id_counter, 'entry_time': fill_time, 'entry_price': entry_price,
            'direction': order_details['direction'], 'sl_price': order_details['sl_price'],
            'initial_sl': order_details['initial_sl'], 'tp_price': order_details['tp_price'],
            'position_size_usd': order_details['position_size_usd'], 'margin_used': order_details['margin_used'],
            'strategy': order_details['strategy'], 'entry_fee': entry_fee,
        }

    def close_trade(self, symbol, exit_price, exit_time, exit_reason):
        if symbol not in self.active_positions: return
        trade_details = self.active_positions[symbol]
        
        direction = trade_details['direction']
        entry_price = trade_details['entry_price']
        position_size_usd = trade_details['position_size_usd']

        actual_exit_price = exit_price * (1 - SLIPPAGE['pct'] if direction == 'LONG' else 1 + SLIPPAGE['pct'])
        exit_fee_rate = FEES['maker'] if exit_reason == 'Take Profit' else FEES['taker']
        exit_fee = position_size_usd * exit_fee_rate
        total_fees = trade_details['entry_fee'] + exit_fee

        pnl_pct = (actual_exit_price - entry_price) / entry_price if direction == 'LONG' else (entry_price - actual_exit_price) / entry_price
        pnl_usd = pnl_pct * position_size_usd if pd.notna(pnl_pct) and pd.notna(position_size_usd) else 0.0
        net_pnl_usd = pnl_usd - total_fees

        if pd.notna(net_pnl_usd):
            self.balance += net_pnl_usd

        # --- FITUR BARU: Catat waktu penutupan trade untuk cooldown ---
        self.last_trade_time[symbol] = exit_time

        self.trades.append({
            "ID": trade_details['id'], "Symbol": symbol, "Strategy": trade_details['strategy'],
            "Direction": direction, "Entry Time": trade_details.get('entry_time'), "Exit Time": exit_time,
            "PnL (USD)": net_pnl_usd, "Balance": self.balance, "Exit Reason": exit_reason,
        })
        console.log(
            f"Closed trade {trade_details['id']} on {symbol}. Reason: {exit_reason}. "
            f"Net PnL: ${net_pnl_usd:,.2f} (Gross: ${pnl_usd:,.2f}, Fees: ${total_fees:,.2f}). New Balance: ${self.balance:,.2f}"
        )
        # Hapus dari posisi aktif setelah ditutup
        if symbol in self.active_positions:
            del self.active_positions[symbol]

    def create_pending_order(self, signal_row, signal_time, full_data, exit_params, symbol, current_risk_per_trade, default_leverage):
        if symbol in self.pending_orders: return

        if signal_time >= full_data.index[-1]:
            console.log(f"[yellow]Skipping signal on {symbol} at {signal_time} as it's the last available candle.[/yellow]")
            return

        risk_params = get_dynamic_risk_params(self.balance)
        total_exposure = len(self.active_positions) + len(self.pending_orders)
        if total_exposure >= risk_params['max_active_positions']:
            return 

        signal_price = signal_row['close']
        direction = signal_row['signal']
        atr_val = signal_row[f"ATRr_{CONFIG['atr_period']}"]

        limit_offset_pct = 0.001
        limit_price = signal_price * (1 - limit_offset_pct) if direction == 'LONG' else signal_price * (1 + limit_offset_pct)
        expiration_candles = 10

        sl_multiplier = exit_params.get('sl_multiplier', 1.5)
        rr_ratio = exit_params.get('rr_ratio', 1.5)

        if isinstance(sl_multiplier, (pd.Series, np.ndarray)):
            sl_multiplier = sl_multiplier[full_data.index.get_loc(signal_time)]
        if isinstance(rr_ratio, (pd.Series, np.ndarray)):
            rr_ratio = rr_ratio[full_data.index.get_loc(signal_time)]

        risk_amount_usd = self.balance * current_risk_per_trade
        stop_loss_dist = atr_val * sl_multiplier
        
        if limit_price <= 0: return
        stop_loss_pct = stop_loss_dist / limit_price
        
        if stop_loss_pct <= 0:
            console.log(f"[yellow]Skipping order for {symbol}: Invalid stop_loss_pct ({stop_loss_pct:.4f}).[/yellow]")
            return

        leverage_for_symbol = LEVERAGE_MAP.get(symbol, LEVERAGE_MAP.get("DEFAULT", default_leverage))
        position_size_usd = risk_amount_usd / stop_loss_pct
        margin_for_this_trade = position_size_usd / leverage_for_symbol

        total_margin_used = sum(pos.get('margin_used', 0) for pos in self.active_positions.values())
        
        if (total_margin_used + margin_for_this_trade) > self.balance:
            return

        console.log(f"[blue]Creating pending {direction} order for {symbol} at limit price {limit_price:.5f} (Leverage: {leverage_for_symbol}x)[/blue]")

        stop_loss_price = limit_price - stop_loss_dist if direction == 'LONG' else limit_price + stop_loss_dist
        take_profit_price = limit_price + (stop_loss_dist * rr_ratio) if direction == 'LONG' else limit_price - (stop_loss_dist * rr_ratio)
        
        timeframe_duration = pd.to_timedelta(CONFIG['timeframe_signal'])
        expiration_time = signal_time + (timeframe_duration * expiration_candles)

        self.pending_orders[symbol] = {
            'creation_time': signal_time, 'expiration_time': expiration_time,
            'limit_price': limit_price, 'direction': direction,
            'sl_price': stop_loss_price, 'initial_sl': stop_loss_price,
            'tp_price': take_profit_price, 'position_size_usd': position_size_usd,
            'margin_used': margin_for_this_trade, 'strategy': signal_row['strategy'],
        }

    def close_remaining_trades(self, all_data):
        """Closes any open positions at the end of the backtest."""
        if not self.active_positions:
            return

        console.log("Closing any remaining open positions at the end of their respective data series...")
        remaining_symbols = list(self.active_positions.keys())
        for symbol in remaining_symbols:
            full_data = all_data.get(symbol)
            if full_data is None or full_data.empty:
                console.log(f"[bold red]Cannot close trade for {symbol}: No data available.[/bold red]")
                continue

            last_candle = full_data.iloc[-1]
            self.close_trade(symbol, last_candle['close'], last_candle.name, "End of Data")

    def get_results_summary(self):
        """Calculates and returns a dictionary of aggregated performance metrics."""
        if not self.trades:
            return {
                "net_profit_pct": 0, "win_rate": 0, "total_trades": 0,
                "avg_rr": 0, "profit_factor": 0, "max_drawdown": 0,
                "sharpe_ratio": 0, "avg_trade_duration": 0,
                "final_balance": self.initial_balance
            }

        trades_df = pd.DataFrame(self.trades)
        net_profit_pct = ((self.balance - self.initial_balance) / self.initial_balance) * 100
        total_trades = len(trades_df)
        wins = len(trades_df[trades_df['PnL (USD)'] > 0])
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

        gross_profit = trades_df[trades_df['PnL (USD)'] > 0]['PnL (USD)'].sum()
        gross_loss = abs(trades_df[trades_df['PnL (USD)'] < 0]['PnL (USD)'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')

        # Simplified RR calculation for summary
        avg_rr = CONFIG.get('risk_reward_ratio', 1.5)

        equity = (self.initial_balance + trades_df['PnL (USD)'].cumsum())
        peak = equity.cummax()
        drawdown = (peak - equity) / peak
        max_drawdown = drawdown.max() * 100 if not drawdown.empty else 0

        trades_df['Entry Time'] = pd.to_datetime(trades_df['Entry Time'])
        trades_df['Exit Time'] = pd.to_datetime(trades_df['Exit Time'])
        trades_df['duration'] = (trades_df['Exit Time'] - trades_df['Entry Time']).dt.total_seconds() / 60
        avg_trade_duration = trades_df['duration'].mean()

        daily_returns = trades_df.set_index('Exit Time')['PnL (USD)'].resample('D').sum() / self.initial_balance
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(365) if daily_returns.std() != 0 else 0

        return {
            "net_profit_pct": round(net_profit_pct, 2),
            "win_rate": round(win_rate, 2),
            "total_trades": total_trades,
            "avg_rr": round(avg_rr, 2),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "avg_trade_duration": round(avg_trade_duration, 2),
            "final_balance": round(self.balance, 2)
        }

    def get_results(self, args):
        """Generates and displays a detailed summary of the backtest results."""
        if not self.trades:
            console.log("[bold yellow]No trades were executed across the entire market scan.[/bold yellow]")
            return

        trades_df = pd.DataFrame(self.trades)
        net_profit = self.balance - self.initial_balance
        net_profit_pct = (net_profit / self.initial_balance) * 100
        total_trades = len(trades_df)
        wins = len(trades_df[trades_df['PnL (USD)'] > 0])
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

        gross_profit = trades_df[trades_df['PnL (USD)'] > 0]['PnL (USD)'].sum()
        gross_loss = abs(trades_df[trades_df['PnL (USD)'] < 0]['PnL (USD)'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

        equity_curve = self.initial_balance + trades_df['PnL (USD)'].cumsum()
        peak = equity_curve.cummax()
        drawdown = (peak - equity_curve) / peak
        max_drawdown = drawdown.max() * 100 if not drawdown.empty else 0

        long_trades_df = trades_df[trades_df['Direction'] == 'LONG']
        short_trades_df = trades_df[trades_df['Direction'] == 'SHORT']
        total_long = len(long_trades_df)
        total_short = len(short_trades_df)
        long_wins = len(long_trades_df[long_trades_df['PnL (USD)'] > 0])
        short_wins = len(short_trades_df[short_trades_df['PnL (USD)'] > 0])
        long_win_rate = (long_wins / total_long) * 100 if total_long > 0 else 0
        short_win_rate = (short_wins / total_short) * 100 if total_short > 0 else 0

        trades_df['Entry Time'] = pd.to_datetime(trades_df['Entry Time'])
        trades_df['Exit Time'] = pd.to_datetime(trades_df['Exit Time'])
        start_date = trades_df['Entry Time'].min()
        end_date = trades_df['Exit Time'].max()
        duration_str = "N/A"
        if pd.notna(start_date) and pd.notna(end_date):
            total_days = (end_date.normalize() - start_date.normalize()).days + 1
            if total_days >= 365:
                years = total_days // 365
                months = (total_days % 365) // 30
                duration_str = f"{years} Tahun {months} Bulan"
            elif total_days >= 30:
                months = total_days // 30
                days = total_days % 30
                duration_str = f"{months} Bulan {days} Hari"
            else:
                duration_str = f"{total_days} Hari"

        strategy_names = ", ".join(STRATEGY_CONFIG.keys())
        console.print("\n" + "="*80, style="bold blue")
        console.print(f"{'MARKET SCAN BACKTEST SUMMARY':^80}", style="bold blue")
        console.print("="*80, style="bold blue")
        
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric")
        summary_table.add_column("Value", justify="right")

        exit_logic_mode = "Dinamis (Advanced)" if LIVE_TRADING_CONFIG.get("use_advanced_exit_logic", True) else "Statis (SL/TP Bursa)"
        
        summary_table.add_row("Strategies Tested", strategy_names)
        summary_table.add_row("Exit Logic Mode", exit_logic_mode)
        summary_table.add_row("Initial Balance", f"${self.initial_balance:,.2f}")
        summary_table.add_row("Final Balance", f"${self.balance:,.2f}")
        summary_table.add_row("Net Profit", f"[green]${net_profit:,.2f} ({net_profit_pct:+.2f}%)" if net_profit > 0 else f"[red]${net_profit:,.2f} ({net_profit_pct:.2f}%)")
        summary_table.add_row("Backtest Duration", duration_str)
        summary_table.add_row("Total Trades", str(total_trades))
        summary_table.add_row(" Long Trades (Win %)", f"{total_long} ({long_win_rate:.2f}%)")
        summary_table.add_row(" Short Trades (Win %)", f"{total_short} ({short_win_rate:.2f}%)")
        summary_table.add_row("Overall Win Rate", f"{win_rate:.2f}%")
        summary_table.add_row("Profit Factor", f"{profit_factor:.2f}")
        summary_table.add_row("Max Drawdown", f"[red]{max_drawdown:.2f}%[/red]")
        console.print(summary_table)

        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        filename = output_dir / "market_scan_results.csv"
        trades_df.to_csv(filename, index=False)
        console.log(f"\n[bold]Full trade log saved to '{filename}'[/bold]")
        
        self._log_results_to_markdown(args=args, net_profit=net_profit, net_profit_pct=net_profit_pct, total_trades=total_trades, win_rate=win_rate, profit_factor=profit_factor, max_drawdown=max_drawdown, duration_str=duration_str)

    def _log_results_to_markdown(self, args, **kwargs):
        """Secara otomatis menambahkan entri baru ke BACKTEST_LOG.md."""
        log_file_path = Path('BACKTEST_LOG.md')
        console.log(f"\n[bold]Appending results to {log_file_path}...[/bold]")
        trades_df = pd.DataFrame(self.trades)

        strategy_performance = pd.DataFrame()
        if not trades_df.empty and 'Strategy' in trades_df.columns:
            strategy_performance = trades_df.groupby('Strategy').agg(
                total_pnl=('PnL (USD)', 'sum'),
                total_trades=('ID', 'count'),
                wins=('PnL (USD)', lambda pnl: (pnl > 0).sum())
            ).reset_index()
            strategy_performance['win_rate'] = (strategy_performance['wins'] / strategy_performance['total_trades']) * 100

        strategy_table_header = "| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |\n"
        strategy_table_divider = "| ---------------------------- | ----- | --------------- | ------ | -------- |\n"
        strategy_rows = ""
        for name, config in STRATEGY_CONFIG.items():
            perf = strategy_performance[strategy_performance['Strategy'] == name]
            if not perf.empty:
                perf_row = perf.iloc[0]
                pnl_str = f"${perf_row['total_pnl']:,.2f}"
                trades_str = str(perf_row['total_trades'])
                win_rate_str = f"{perf_row['win_rate']:.2f}%"
            else:
                pnl_str = "$0.00"
                trades_str = "0"
                win_rate_str = "N/A"
            
            strategy_rows += f"| `{name}` | {config['weight']} | {pnl_str} | {trades_str} | {win_rate_str} |\n"

        results_table = (
            f"| Metrik            | Nilai                      |\n"
            f"| ----------------- | -------------------------- |\n"
            f"| Saldo Awal        | ${self.initial_balance:,.2f}                     |\n"
            f"| Saldo Akhir       | ${self.balance:,.2f}                     |\n"
            f"| **Net Profit**    | **${kwargs['net_profit']:,.2f} ({kwargs['net_profit_pct']:+.2f}%)**       |\n"
            f"| Total Trades      | {kwargs['total_trades']}                         |\n"
            f"| Win Rate          | {kwargs['win_rate']:.2f}%                     |\n"
            f"| Profit Factor     | {kwargs['profit_factor']:.2f}                       |\n"
            f"| Max Drawdown      | {kwargs['max_drawdown']:.2f}%                      |\n"
        )

        # Perbaikan format Net Profit untuk nilai negatif
        if kwargs['net_profit'] < 0:
             results_table = results_table.replace(
                f"**+${kwargs['net_profit']:,.2f} (+{kwargs['net_profit_pct']:.2f}%)**",
                f"**${kwargs['net_profit']:,.2f} ({kwargs['net_profit_pct']:.2f}%)**"
            )

        log_entry = (
            f"\n---\n\n"
            f"## Backtest: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Parameter:**\n"
            f"-   **Simbol:** Top {args.max_symbols} (berdasarkan volume)\n"
            f"-   **Candles:** {args.limit}\n"
            f"-   **Periode:** ~{kwargs['duration_str']}\n"
            f"-   **Mode Exit:** {'Dinamis (Advanced)' if LIVE_TRADING_CONFIG.get('use_advanced_exit_logic', True) else 'Statis (SL/TP Bursa)'}\n\n"
            f"**Konfigurasi & Performa Strategi:**\n\n"
            f"{strategy_table_header}"
            f"{strategy_table_divider}"
            f"{strategy_rows}\n"
            f"**Hasil Ringkas:**\n\n"
            f"{results_table}\n"
            f"**Catatan & Observasi:**\n"
            f"-   (Isi observasi Anda di sini)\n\n"
        )

        original_content = log_file_path.read_text() if log_file_path.exists() else ""
        log_file_path.write_text(log_entry + original_content)
        console.log(f"[green]✅ Results successfully appended to {log_file_path}[/green]")