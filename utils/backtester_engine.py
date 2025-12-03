import pandas as pd
import numpy as np
from rich.console import Console
from datetime import datetime
from pathlib import Path

from config import CONFIG, FEES, SLIPPAGE, LEVERAGE_MAP, LIVE_TRADING_CONFIG, BACKTEST_REALISM_CONFIG, EXECUTION
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
        # --- FITUR BARU: State untuk Drawdown Circuit Breaker ---
        self.peak_balance = initial_balance
        self.drawdown_cooldown_until = None
        # ---------------------------------------------------------
        self.exchange = None # Akan diinisialisasi oleh skrip pemanggil
        # NEW: Track fill statistics
        self.limit_order_stats = {
            'attempted': 0,
            'filled': 0,
            'expired': 0,
            'fill_rate': 0.0
        }

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

        # REVISI: Pindahkan kalkulasi indikator ke dalam prepare_data untuk memastikan semua dihitung pada DataFrame akhir.
        base_data = prepare_data(df_signal, df_trend, df_macro) # type: ignore
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
        # --- FITUR BARU: Inisialisasi untuk Multi-Level TP ---
        self.active_positions[symbol]['initial_position_size_usd'] = order_details['position_size_usd']
        self.active_positions[symbol]['remaining_position_usd'] = order_details['position_size_usd']
        self.active_positions[symbol]['partial_tp_targets'] = []

        risk_distance = abs(entry_price - order_details['initial_sl'])
        for rr_multiplier, fraction in EXECUTION['partial_tps']:
            if risk_distance > 0:
                tp_price_target = entry_price + (risk_distance * rr_multiplier) if order_details['direction'] == 'LONG' else entry_price - (risk_distance * rr_multiplier)
                self.active_positions[symbol]['partial_tp_targets'].append({
                    'rr': rr_multiplier,
                    'fraction': fraction,
                    'price': tp_price_target,
                    'hit': False
                })
        # Urutkan target dari yang paling dekat ke paling jauh
        sort_reverse = order_details['direction'] == 'SHORT'
        self.active_positions[symbol]['partial_tp_targets'].sort(key=lambda x: x['price'], reverse=sort_reverse)

    def close_trade(self, symbol, exit_price, exit_time, exit_reason, size_to_close_usd=None):
        if symbol not in self.active_positions: return
        trade_details = self.active_positions[symbol]
        
        direction = trade_details['direction']
        entry_price = trade_details['entry_price']
        position_size_to_close = size_to_close_usd if size_to_close_usd is not None else trade_details['remaining_position_usd']

        actual_exit_price = exit_price * (1 - SLIPPAGE['pct'] if direction == 'LONG' else 1 + SLIPPAGE['pct'])
        exit_fee_rate = FEES['maker'] if 'Take Profit' in exit_reason else FEES['taker']
        exit_fee = position_size_to_close * exit_fee_rate
        total_fees = trade_details['entry_fee'] + exit_fee

        pnl_pct = (actual_exit_price - entry_price) / entry_price if direction == 'LONG' else (entry_price - actual_exit_price) / entry_price
        pnl_usd = pnl_pct * position_size_to_close if pd.notna(pnl_pct) else 0.0
        net_pnl_usd = pnl_usd - total_fees

        if pd.notna(net_pnl_usd):
            self.balance += net_pnl_usd
        
        # --- FITUR BARU: Update Peak Balance setelah setiap trade ---
        if self.balance > self.peak_balance:
            self.peak_balance = self.balance
        # ---------------------------------------------------------

        # --- FITUR BARU: Catat waktu penutupan trade untuk cooldown ---
        self.last_trade_time[symbol] = exit_time

        self.trades.append({
            "ID": trade_details['id'], "Symbol": symbol, "Strategy": trade_details['strategy'],
            "Direction": direction, "Entry Time": trade_details.get('entry_time'), "Exit Time": exit_time,
            "PnL (USD)": net_pnl_usd, "Balance": self.balance, "Exit Reason": exit_reason,
        })

        trade_details['remaining_position_usd'] -= position_size_to_close

        if trade_details['remaining_position_usd'] < 1: # Jika posisi sudah habis
            console.log(
                f"Closed trade {trade_details['id']} on {symbol}. Reason: {exit_reason}. "
                f"Net PnL: ${net_pnl_usd:,.2f}. New Balance: ${self.balance:,.2f}"
            )
            del self.active_positions[symbol]
        else: # Jika ini penutupan parsial
            console.log(
                f"Partially closed trade {trade_details['id']} on {symbol} ({exit_reason}). "
                f"Closed ${position_size_to_close:,.2f} USD. Remaining: ${trade_details['remaining_position_usd']:,.2f} USD. "
                f"PnL: ${net_pnl_usd:,.2f}."
            )

    def check_drawdown_and_cooldown(self, current_time):
        """Memeriksa drawdown dan mengelola status cooldown."""
        if self.drawdown_cooldown_until and current_time < self.drawdown_cooldown_until:
            return False # Masih dalam masa cooldown
        return True # Boleh trading
        
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

    def check_and_trigger_drawdown(self, current_time):
        """Memeriksa apakah drawdown terpicu dan memulai cooldown jika perlu."""
        drawdown_pct = (self.peak_balance - self.balance) / self.peak_balance if self.peak_balance > 0 else 0
        if drawdown_pct > LIVE_TRADING_CONFIG['max_drawdown_pct']:
            if self.drawdown_cooldown_until is None or current_time > self.drawdown_cooldown_until:
                cooldown_hours = LIVE_TRADING_CONFIG['drawdown_cooldown_hours']
                self.drawdown_cooldown_until = current_time + pd.Timedelta(hours=cooldown_hours)
                console.log(f"🚨 [bold red]DRAWDOWN CIRCUIT BREAKER TERPICU![/bold red] Drawdown: {drawdown_pct:.2%}. Trading dihentikan selama {cooldown_hours} jam.")
                return True
        return False

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
        
        # Perbaikan format Net Profit untuk nilai negatif
        profit_color = "green" if kwargs['net_profit'] >= 0 else "red"
        profit_sign = "+" if kwargs['net_profit'] >= 0 else ""
        results_table = (
            f"| Metrik            | Nilai                      |\n"
            f"| ----------------- | -------------------------- |\n"
            f"| Saldo Awal        | ${self.initial_balance:,.2f}                     |\n"
            f"| Saldo Akhir       | ${self.balance:,.2f}                     |\n"
            f"| **Net Profit**    | **[{profit_color}]${kwargs['net_profit']:,.2f} ({profit_sign}{kwargs['net_profit_pct']:.2f}%)[/{profit_color}]**       |\n"
            f"| Total Trades      | {kwargs['total_trades']}                         |\n"
            f"| Win Rate          | {kwargs['win_rate']:.2f}%                     |\n"
            f"| Profit Factor     | {kwargs['profit_factor']:.2f}                       |\n"
            f"| Max Drawdown      | {kwargs['max_drawdown']:.2f}%                      |\n"
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
    
    def check_limit_order_fill_realistic(self, symbol, order_details, candle, avg_volume):
        """
        FIXED: Probabilistic limit order fill model
        More realistic than assuming 100% fill when price touches
        """
        limit_price = order_details['limit_price']
        direction = order_details['direction']
        
        # Step 1: Did price reach our limit?
        if direction == 'LONG':
            price_touched = candle['low'] <= limit_price
            if not price_touched:
                return False, None
            
            # Step 2: How far did price move past our limit?
            distance_past_limit = candle['close'] - limit_price
            range_size = candle['high'] - candle['low']
            
        else:  # SHORT
            price_touched = candle['high'] >= limit_price
            if not price_touched:
                return False, None
            
            distance_past_limit = limit_price - candle['close']
            range_size = candle['high'] - candle['low']
        
        # Step 3: Calculate fill probability
        # If close is far from limit, more likely we filled
        if range_size > 0:
            penetration_ratio = distance_past_limit / range_size
            # Clamp between 0.4 and 1.0
            min_prob = BACKTEST_REALISM_CONFIG.get("min_fill_probability", 0.4)
            base_probability = min(1.0, max(min_prob, penetration_ratio))
        else:
            base_probability = 0.5
        
        # Step 4: Volume factor
        # More volume = higher chance of fill
        vol_multiplier = BACKTEST_REALISM_CONFIG.get("volume_factor_multiplier", 0.5)
        volume_factor = min(1.0, candle['volume'] / (avg_volume * vol_multiplier)) if avg_volume > 0 else 1.0
        fill_probability = base_probability * volume_factor
        
        # Step 5: Simulate the fill
        filled = np.random.random() < fill_probability
        
        if filled:
            # Calculate actual fill price (might be slightly better or worse than limit)
            if direction == 'LONG':
                # Sometimes get filled slightly above limit
                actual_fill_price = limit_price * (1 + np.random.uniform(0, 0.0002))
            else:
                actual_fill_price = limit_price * (1 - np.random.uniform(0, 0.0002))
            
            return True, actual_fill_price
        
        return False, None
    
    def check_stop_loss_realistic(self, trade_details, candle, previous_candle):
        """
        FIXED: Use worst-case price within candle, not close
        Also handles gaps and adds realistic slippage
        """
        direction = trade_details['direction']
        sl_price = trade_details['sl_price']
        
        # Step 1: Check for gap (price jump between candles)
        gap_occurred = False
        if previous_candle is not None:
            if direction == 'LONG':
                # Gap down through SL
                if candle['open'] < sl_price < previous_candle['close']:
                    gap_occurred = True
                    # Exit at open price (worst case)
                    exit_price = candle['open']
                    exit_reason = "Gap Stop Loss"
                    return exit_price, exit_reason, True
            else:  # SHORT
                # Gap up through SL
                if candle['open'] > sl_price > previous_candle['close']:
                    gap_occurred = True
                    exit_price = candle['open']
                    exit_reason = "Gap Stop Loss"
                    return exit_price, exit_reason, True
        
        # Step 2: Check if SL was hit during the candle
        if direction == 'LONG':
            if candle['low'] <= sl_price:
                # Assume we got stopped at SL price + realistic slippage
                # Slippage is worse during fast moves
                atr = candle.get(f"ATRr_14", candle['high'] - candle['low'])
                candle_range = candle['high'] - candle['low']
                
                # If candle is large (volatile), assume more slippage
                volatility_factor = min(candle_range / atr, 2.0) if atr > 0 else 1.0
                slippage_pct = SLIPPAGE['pct'] * volatility_factor
                
                exit_price = sl_price * (1 - slippage_pct)
                exit_reason = "Stop Loss"
                return exit_price, exit_reason, True
                
        else:  # SHORT
            if candle['high'] >= sl_price:
                atr = candle.get(f"ATRr_14", candle['high'] - candle['low'])
                candle_range = candle['high'] - candle['low']
                volatility_factor = min(candle_range / atr, 2.0) if atr > 0 else 1.0
                slippage_pct = SLIPPAGE['pct'] * volatility_factor
                
                exit_price = sl_price * (1 + slippage_pct)
                exit_reason = "Stop Loss"
                return exit_price, exit_reason, True
        
        return None, None, False
    
    def update_trailing_stop(self, trade_details, candle):
        """
        MISSING FUNCTION - Now implemented!
        Updates trailing stop loss based on price movement
        """
        if not LIVE_TRADING_CONFIG.get("trailing_sl_enabled", False):
            return
        
        is_trailing_active = trade_details.get('trailing_sl_active', False)
        direction = trade_details['direction']
        
        # Calculate current R-multiple
        risk_distance = abs(trade_details['entry_price'] - trade_details['initial_sl'])
        if risk_distance > 0:
            current_profit_distance = abs(candle['close'] - trade_details['entry_price'])
            current_rr = current_profit_distance / risk_distance
            trigger_rr = LIVE_TRADING_CONFIG.get("trailing_sl_trigger_rr", 1.0)
            
            # Activate trailing if we've reached trigger RR
            if not is_trailing_active and current_rr >= trigger_rr:
                trade_details['trailing_sl_active'] = True
                is_trailing_active = True
        
        # If trailing is active, update SL
        if is_trailing_active:
            atr_val = candle.get(f"ATRr_{CONFIG['atr_period']}", (candle['high'] - candle['low']))
            trail_dist = atr_val * LIVE_TRADING_CONFIG.get("trailing_sl_distance_atr", 1.5)
            
            if direction == 'LONG':
                # Use close price for trailing (your original logic)
                new_sl = candle['close'] - trail_dist
                # Only update if new SL is better (higher)
                if new_sl > trade_details['sl_price']:
                    trade_details['sl_price'] = new_sl
            else:  # SHORT
                new_sl = candle['close'] + trail_dist
                # Only update if new SL is better (lower)
                if new_sl < trade_details['sl_price']:
                    trade_details['sl_price'] = new_sl
    
    def check_take_profit_realistic(self, trade_details, candle):
        """
        FIXED: Check if TP was hit using high/low, not just close
        """
        direction = trade_details['direction']
        tp_price = trade_details['tp_price']
        
        if direction == 'LONG':
            if candle['high'] >= tp_price:
                # Assume we got filled at TP (limit order)
                # But add small negative slippage for realism
                exit_price = tp_price * (1 - SLIPPAGE['pct'] * 0.5)
                return exit_price, "Take Profit", True
        else:  # SHORT
            if candle['low'] <= tp_price:
                exit_price = tp_price * (1 + SLIPPAGE['pct'] * 0.5)
                return exit_price, "Take Profit", True
        
        return None, None, False
    
    def check_circuit_breaker_realistic(self, trade_details, candle):
        """
        FIXED: Circuit breaker with realistic emergency exit slippage
        """
        from config import LIVE_TRADING_CONFIG
        
        if not LIVE_TRADING_CONFIG.get("circuit_breaker_enabled", True):
            return None, None, False
        
        cb_multiplier = LIVE_TRADING_CONFIG.get("circuit_breaker_multiplier", 1.5)
        sl_breach_threshold = abs(trade_details['entry_price'] - trade_details['initial_sl']) * (cb_multiplier - 1.0)
        
        direction = trade_details['direction']
        sl_price = trade_details['sl_price']
        
        # Check if price breached the circuit breaker level
        price_breached = False
        
        if direction == 'LONG' and candle['low'] < (sl_price - sl_breach_threshold):
            price_breached = True
            # Emergency exit - assume TERRIBLE fill due to panic
            emergency_slippage = sl_breach_threshold * 0.3  # 30% of the breach distance
            exit_price = sl_price - sl_breach_threshold - emergency_slippage
            
        elif direction == 'SHORT' and candle['high'] > (sl_price + sl_breach_threshold):
            price_breached = True
            emergency_slippage = sl_breach_threshold * 0.3
            exit_price = sl_price + sl_breach_threshold + emergency_slippage
        
        if price_breached:
            # Additional check: Volume confirmation (from your original code)
            avg_volume = trade_details.get('avg_volume', candle['volume'])
            volume_spike_multiplier = 2.0
            
            if candle['volume'] > (avg_volume * volume_spike_multiplier):
                return exit_price, "Circuit Breaker", True
        
        return None, None, False
    
    def check_trades_and_orders_fixed(self, start_time, end_time, all_data):
        """
        FIXED VERSION: Check for exits and fills with realistic execution
        """
        # 1. Check Active Trades for Exit
        closed_symbols = []
        for symbol, trade_details in list(self.active_positions.items()):
            full_data = all_data[symbol]
            
            check_start = max(start_time, trade_details['entry_time'])
            if end_time <= check_start:
                continue
            
            # PERBAIKAN: Jangan gunakan .iloc[1:]. Slicing loc sudah inklusif untuk start dan end.
            # Kita ingin memeriksa SEMUA candle di antara dua timestamp sinyal, dimulai dari
            # candle SETELAH sinyal dibuat. `check_start` sudah menangani ini.
            candles_to_check = full_data.loc[check_start:end_time]
            if candles_to_check.empty:
                continue
            
            previous_candle = full_data.loc[:check_start].iloc[-1] if len(full_data.loc[:check_start]) > 0 else None
            exit_reason = None
            
            for idx, candle in candles_to_check.iterrows():
                # Priority 1: Check Circuit Breaker (most urgent)
                exit_price, reason, triggered = self.check_circuit_breaker_realistic(trade_details, candle)
                if triggered:
                    exit_reason = reason
                    break
                
                # Priority 2: Check Stop Loss
                exit_price, reason, triggered = self.check_stop_loss_realistic(trade_details, candle, previous_candle)
                if triggered:
                    exit_reason = reason
                    break
                
                # --- FITUR BARU: Logika Multi-Level TP ---
                # Priority 3: Check Partial Take Profits
                for tp_target in trade_details['partial_tp_targets']:
                    if tp_target['hit']: continue # Lewati jika sudah tercapai

                    is_hit = (trade_details['direction'] == 'LONG' and candle['high'] >= tp_target['price']) or \
                             (trade_details['direction'] == 'SHORT' and candle['low'] <= tp_target['price'])

                    if is_hit:
                        size_to_close = trade_details['initial_position_size_usd'] * tp_target['fraction']
                        # Pastikan tidak menutup lebih dari sisa posisi
                        size_to_close = min(size_to_close, trade_details['remaining_position_usd'])
                        
                        if size_to_close > 1:
                            self.close_trade(symbol, tp_target['price'], candle.name, f"Partial TP {tp_target['rr']}R", size_to_close_usd=size_to_close)
                        tp_target['hit'] = True
                        
                        # Jika posisi sudah tidak ada lagi setelah TP parsial, keluar dari loop candle
                        if symbol not in self.active_positions:
                            exit_reason = "Position fully closed by partial TPs"
                            break
                
                if exit_reason: break # Keluar dari loop candle jika posisi sudah ditutup
                
                # Priority 4: Update Trailing Stop (if enabled)
                self.update_trailing_stop(trade_details, candle)
                
                previous_candle = candle
            
            if exit_reason and symbol not in closed_symbols and symbol in self.active_positions:
                self.close_trade(symbol, exit_price, end_time, exit_reason)
                closed_symbols.append(symbol)

        # 2. Check Pending Orders for Fill or Expiry
        filled_symbols = []
        expired_symbols = []
        
        for symbol, order_details in list(self.pending_orders.items()):
            full_data = all_data[symbol]
            
            # Check expiration
            if end_time > order_details['expiration_time']:
                expired_symbols.append(symbol)
                self.limit_order_stats['expired'] += 1
                continue
            
            # PERBAIKAN: Gunakan slicing yang sama dengan di atas.
            # Kita periksa semua candle dari waktu sinyal dibuat hingga sinyal berikutnya.
            check_start_order = max(start_time, order_details['creation_time'])
            candles_to_check = full_data.loc[check_start_order:end_time]
            avg_volume = full_data['volume'].rolling(20).mean().loc[start_time:end_time].mean()
            
            for fill_time, candle in candles_to_check.iterrows():
                self.limit_order_stats['attempted'] += 1
                
                # Use realistic fill model
                filled, actual_fill_price = self.check_limit_order_fill_realistic(
                    symbol, order_details, candle, avg_volume
                )
                
                if filled:
                    # Update order details with actual fill price
                    order_details['actual_fill_price'] = actual_fill_price
                    self.open_trade(symbol, order_details, fill_time)
                    filled_symbols.append(symbol)
                    self.limit_order_stats['filled'] += 1
                    break
        
        # Clean up
        for symbol in filled_symbols + expired_symbols:
            if symbol in self.pending_orders:
                del self.pending_orders[symbol]
        
        # Update fill rate statistics
        if self.limit_order_stats['attempted'] > 0:
            self.limit_order_stats['fill_rate'] = (
                self.limit_order_stats['filled'] / self.limit_order_stats['attempted']
            )
        
        # 3. Check for Drawdown Trigger
        self.check_and_trigger_drawdown(end_time)
    
    def get_results_with_realism_report(self, args):
        """
        ENHANCED: Add statistics about backtest realism
        """
        # ... (your existing get_results code) ...
        
        # NEW: Add realism metrics to report
        console.print("\n[bold cyan]Backtest Realism Metrics:[/bold cyan]")
        realism_table = Table(show_header=True, header_style="bold yellow")
        realism_table.add_column("Metric")
        realism_table.add_column("Value", justify="right")
        realism_table.add_column("Note")
        
        realism_table.add_row(
            "Limit Order Fill Rate",
            f"{self.limit_order_stats['fill_rate']*100:.1f}%",
            "70-85% is realistic"
        )
        
        # Calculate gap events
        gap_stops = len([t for t in self.trades if t['Exit Reason'] == 'Gap Stop Loss'])
        realism_table.add_row(
            "Gap Stop Events",
            str(gap_stops),
            "Should see 1-5% of trades"
        )
        
        # Calculate circuit breaker events
        cb_stops = len([t for t in self.trades if t['Exit Reason'] == 'Circuit Breaker'])
        realism_table.add_row(
            "Circuit Breaker Events",
            str(cb_stops),
            "Should be rare (<2%)"
        )
        
        console.print(realism_table)
        
        # Warning if backtest seems too optimistic
        if self.limit_order_stats['fill_rate'] > 0.90:
            console.print("\n[bold yellow]⚠️  WARNING: Fill rate >90% suggests backtest may be optimistic[/bold yellow]")
        
        if gap_stops == 0:
            console.print("[bold yellow]⚠️  WARNING: No gap events detected. Consider longer backtest period.[/bold yellow]")
