import argparse
import pandas as pd
import numpy as np
from datetime import datetime # Impor datetime untuk timestamp log
from concurrent.futures import ThreadPoolExecutor, as_completed # Tetap digunakan untuk paralelisasi
import time # Impor modul time
import math # Impor math untuk fungsi ceil
import ccxt
import ccxt.pro as ccxtpro # Impor ccxt.pro untuk koneksi async
from pathlib import Path
from dateutil.relativedelta import relativedelta
from rich.console import Console
from rich.table import Table

from utils.common_utils import get_dynamic_risk_params, get_all_futures_symbols
from config import CONFIG, FEES, SLIPPAGE, LEVERAGE_MAP, LIVE_TRADING_CONFIG, API_KEYS
from indicators import fetch_binance_data_sync # REVISI: Impor versi sinkron
from utils.data_preparer import prepare_data
from strategies import STRATEGY_CONFIG

console = Console()

class PortfolioBacktester:
    """
    A backtester that manages a single compounding portfolio across multiple assets and strategies.
    """
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.trades = []
        self.trade_id_counter = 0
        self.active_positions = {} # symbol -> trade_details

        self.pending_orders = {} # symbol -> pending_order_details
    def run_scan(self, symbols, limit):
        """Scans all symbols, finds signals, and simulates trades."""
        all_signals = []
        all_data = {}

        # --- REVISI: Fetching data secara sekuensial untuk menghindari IP Ban ---
        console.log(f"Starting sequential data fetching for {len(symbols)} symbols to avoid rate limits...")
        for i, symbol in enumerate(symbols):
            try:
                console.log(f"({i+1}/{len(symbols)}) Fetching data for [bold cyan]{symbol}[/bold cyan]...")
                result = self.fetch_and_prepare_symbol_data(symbol, limit)
                if result is not None:
                    all_data[symbol] = result
                    console.log(f"({i+1}/{len(symbols)}) Successfully processed [bold cyan]{symbol}[/bold cyan]")
                else:
                    console.log(f"({i+1}/{len(symbols)}) [yellow]Skipping {symbol} due to data issues.[/yellow]")
                
                # Tambahkan jeda 1 detik di antara setiap panggilan API untuk keamanan
                time.sleep(1) 
            except Exception as exc:
                console.log(f"({i+1}/{len(symbols)}) [bold red]Error processing {symbol}: {exc}[/bold red]")

        if not all_data:
            console.log("[bold red]Failed to prepare data for any symbol. Exiting.[/bold red]")
            return

        # --- REVISI BESAR: Implementasi Logika Konsensus Sinyal pada Backtester ---
        console.log("\nGenerating signals using consensus filter (min. 2 votes)...")
        for symbol, base_data in all_data.items():
            if base_data is None:
                continue

            # 1. Dapatkan sinyal dan bobot dari setiap strategi
            strategy_signals = {}
            for strategy_name, config in STRATEGY_CONFIG.items():
                signal_function = config["function"]
                weight = config["weight"]
                long_s, short_s, _ = signal_function(base_data.copy())
                strategy_signals[strategy_name] = {'long': long_s, 'short': short_s, 'weight': weight}

            # 2. Hitung skor berbobot untuk setiap candle
            long_score = pd.Series(0.0, index=base_data.index)
            short_score = pd.Series(0.0, index=base_data.index)
            for strat_name, signals in strategy_signals.items():
                long_score += signals['long'].astype(int) * signals['weight']
                short_score += signals['short'].astype(int) * signals['weight']

            # 3. Tentukan sinyal konsensus berdasarkan skor
            # --- REVISI FINAL: Logika ambang batas hybrid yang cerdas ---
            num_strategies = len(STRATEGY_CONFIG)
            if num_strategies == 1:
                required_score = next(iter(c['weight'] for c in STRATEGY_CONFIG.values())) * 0.99
            elif num_strategies == 2:
                required_score = min(c['weight'] for c in STRATEGY_CONFIG.values()) * 0.99
            else: # Untuk 3 atau lebih strategi
                total_possible_score = sum(c['weight'] for c in STRATEGY_CONFIG.values())
                consensus_ratio = LIVE_TRADING_CONFIG.get('consensus_ratio', 0.55)
                required_score = total_possible_score * consensus_ratio

            consensus_long = (long_score >= required_score)
            consensus_short = (short_score >= required_score)

            # 4. Buat DataFrame sinyal final dari konsensus, dan tentukan strategi utama
            df_consensus = base_data.copy()
            df_consensus['signal'] = pd.Series(np.nan, index=base_data.index, dtype='object')
            df_consensus['strategy'] = pd.Series(np.nan, index=base_data.index, dtype='object')

            # Tentukan strategi utama (yang pertama memberikan suara) untuk setiap sinyal konsensus
            # Ini penting untuk mengambil exit_params yang benar nanti.
            primary_strat_long = pd.Series(np.nan, index=base_data.index, dtype='object')
            primary_strat_short = pd.Series(np.nan, index=base_data.index, dtype='object')
            for strat_name, signals in strategy_signals.items():
                primary_strat_long.loc[signals['long']] = primary_strat_long.loc[signals['long']].fillna(strat_name)
                primary_strat_short.loc[signals['short']] = primary_strat_short.loc[signals['short']].fillna(strat_name)

            df_consensus.loc[consensus_long, 'signal'] = 'LONG'
            df_consensus.loc[consensus_long, 'strategy'] = primary_strat_long
            df_consensus.loc[consensus_short, 'signal'] = 'SHORT'
            df_consensus.loc[consensus_short, 'strategy'] = primary_strat_short

            df_consensus['symbol'] = symbol

            signals_df = df_consensus[df_consensus['signal'].isin(['LONG', 'SHORT'])].copy()
            if not signals_df.empty:
                all_signals.extend(signals_df.reset_index().to_dict('records'))

        if not all_signals:
            console.log("[bold red]No signals found across any symbols.[/bold red]")
            return

        # 3. Sort all signals chronologically
        sorted_signals = sorted(all_signals, key=lambda x: x['timestamp'])
        console.log(f"Found a total of {len(sorted_signals)} signals across all symbols. Starting chronological simulation...")

        # --- OPTIMISASI: Lacak waktu terakhir yang diproses ---
        last_processed_time = None
        if sorted_signals:
            # Mulai dari waktu sebelum sinyal pertama
            last_processed_time = sorted_signals[0]['timestamp'] - pd.Timedelta(minutes=1)

        # 4. Process signals one by one in time order
        for signal in sorted_signals:
            symbol = signal['symbol']
            strategy_name = signal['strategy']
            # --- REVISI: Pastikan timestamp adalah objek Timestamp yang tz-aware ---
            signal_time = pd.to_datetime(signal['timestamp'], utc=True)

            # --- OPTIMISASI: Hanya proses candle baru sejak pengecekan terakhir ---
            # 1. Periksa exit dan pending order untuk semua candle BARU
            self.check_trades_and_orders(last_processed_time, signal_time, all_data)

            # 3. Process the new signal
            # Check if we are already in a position OR have a pending order for this symbol
            # (Pengecekan ini dilakukan setelah check_trades_and_orders untuk memastikan state terbaru)
            if symbol in self.active_positions:
                continue

            # Find the signal row in the original dataframe to get all necessary data
            full_data = all_data[symbol]
            signal_row = full_data.loc[signal_time]
            
            signal_row_dict = signal_row.to_dict()
            signal_row_dict['signal'] = signal['signal']
            signal_row_dict['strategy'] = strategy_name
            
            # Re-fetch the correct exit_params for the specific strategy
            # --- REVISI: Ambil fungsi dari STRATEGY_CONFIG ---
            signal_function = STRATEGY_CONFIG[strategy_name]['function']
            _, _, exit_params = signal_function(full_data)

            # --- REVISI: Pindahkan pengambilan parameter dinamis ke sini ---
            # Ini memastikan parameter yang benar diteruskan ke create_pending_order
            risk_params = get_dynamic_risk_params(self.balance)
            current_risk_per_trade = risk_params['risk_per_trade']
            default_leverage = risk_params['default_leverage']

            self.create_pending_order(signal_row_dict, signal_time, full_data, exit_params, symbol, current_risk_per_trade, default_leverage)

            # --- OPTIMISASI: Perbarui waktu terakhir yang diproses ---
            last_processed_time = signal_time

        # Final check for any remaining open trades at the end of the data
        # --- REVISI: Gunakan timestamp terakhir dari data masing-masing simbol ---
        if self.active_positions:
            console.log("Closing any remaining open positions at the end of their respective data series...")
            # --- REVISI: Logika baru untuk menangani trade yang belum ditutup ---
            # Alih-alih memanggil check_active_trades, kita akan secara eksplisit
            # menutup setiap trade yang tersisa dan menambahkannya ke daftar self.trades.
            # Ini memastikan tidak ada trade yang terlewat.
            remaining_symbols = list(self.active_positions.keys())
            for symbol in remaining_symbols:
                trade_details = self.active_positions[symbol]
                full_data = all_data.get(symbol)

                if full_data is None or full_data.empty:
                    console.log(f"[bold red]Cannot close trade for {symbol}: No data available.[/bold red]")
                    continue

                last_candle = full_data.iloc[-1]
                exit_price = last_candle['close']
                exit_time = last_candle.name
                exit_reason = "End of Data"

                # Panggil close_trade untuk menghitung PnL dan menambahkan ke self.trades
                self.close_trade(symbol, exit_price, exit_time, exit_reason)

    def fetch_and_prepare_symbol_data(self, symbol, limit):
        """Helper function to fetch and prepare data for a single symbol. Designed for parallel execution."""
        # REVISI: Hapus semua logika asyncio.run().
        # Fungsi fetch_binance_data sekarang bisa menangani instance exchange sinkron.
        # We need a larger buffer for multi-timeframe indicators
        buffer = 200 
        limit_15m = (limit // 3) + buffer
        limit_1h = (limit // 12) + buffer
        
        # REVISI: Panggil fungsi sinkron yang baru
        df_5m = fetch_binance_data_sync(self.exchange, symbol, '5m', limit=limit, use_cache=True) if self.exchange else None
        df_15m = fetch_binance_data_sync(self.exchange, symbol, '15m', limit=limit_15m, use_cache=True) if self.exchange else None
        df_1h = fetch_binance_data_sync(self.exchange, symbol, '1h', limit=limit_1h, use_cache=True) if self.exchange else None

        if any(df is None for df in [df_5m, df_15m, df_1h]):
            return None

        base_data = prepare_data(df_5m, df_15m, df_1h)
        return base_data

    def check_trades_and_orders(self, start_time, end_time, all_data):
        """
        Optimized function to check for trade exits and pending order fills
        only within the new candle range (start_time to end_time).
        """
        # --- 1. Periksa Active Trades untuk Exit ---
        closed_symbols = []
        # Buat salinan karena dictionary bisa berubah selama iterasi
        for symbol, trade_details in list(self.active_positions.items()):
            full_data = all_data[symbol]

            # --- OPTIMISASI: Hanya ambil candle BARU sejak pengecekan terakhir ---
            # Pastikan start_time tidak sebelum trade dibuka
            check_start = max(start_time, trade_details['entry_time'])
            
            # Jika rentang waktu tidak valid, lewati
            if end_time <= check_start:
                continue

            # Slice hanya candle baru yang relevan
            candles_to_check = full_data.loc[check_start:end_time].iloc[1:]

            if candles_to_check.empty:
                continue

            exit_reason = None
            for idx, candle in candles_to_check.iterrows():
                if (trade_details['direction'] == 'LONG' and candle['low'] <= trade_details['sl_price']) or \
                   (trade_details['direction'] == 'SHORT' and candle['high'] >= trade_details['sl_price']):
                    exit_price = trade_details['sl_price']
                    exit_time = idx
                    exit_reason = "Stop Loss"
                    break
                if (trade_details['direction'] == 'LONG' and candle['high'] >= trade_details['tp_price']) or \
                   (trade_details['direction'] == 'SHORT' and candle['low'] <= trade_details['tp_price']):
                    exit_price = trade_details['tp_price']
                    exit_time = idx
                    exit_reason = "Take Profit"
                    break
            
            if exit_reason: # Jika trade ditutup karena SL/TP
                self.close_trade(symbol, exit_price, exit_time, exit_reason)
                closed_symbols.append(symbol)

        # Remove closed trades from active positions
        for symbol in closed_symbols:
            del self.active_positions[symbol]
        
        # --- 2. Periksa Pending Orders untuk Fill atau Expiry ---
        filled_symbols = []
        expired_symbols = []
        # Buat salinan karena dictionary bisa berubah selama iterasi
        for symbol, order_details in list(self.pending_orders.items()):
            full_data = all_data[symbol]
            
            # Check for expiration first
            if end_time > order_details['expiration_time']:
                expired_symbols.append(symbol)
                continue

            # --- OPTIMISASI: Hanya periksa candle BARU ---
            candles_to_check = full_data.loc[start_time:end_time].iloc[1:]
            for fill_time, candle in candles_to_check.iterrows():
                filled = False
                if order_details['direction'] == 'LONG' and candle['low'] <= order_details['limit_price']:
                    filled = True
                elif order_details['direction'] == 'SHORT' and candle['high'] >= order_details['limit_price']:
                    filled = True
                
                if filled:
                    # Order filled! Open the trade.
                    self.open_trade(symbol, order_details, fill_time=fill_time)
                    filled_symbols.append(symbol)
                    break # Stop checking candles for this symbol

        # Clean up filled and expired orders
        for symbol in filled_symbols + expired_symbols:
            if symbol in self.pending_orders:
                if symbol in expired_symbols:
                    console.log(f"[yellow]Pending order for {symbol} expired at {end_time}.[/yellow]")
                del self.pending_orders[symbol]

    def open_trade(self, symbol, order_details, fill_time):
        """Moves a filled pending order to active positions."""
        # Cannot open a new trade if one is already active for this symbol
        if symbol in self.active_positions:
            return

        # --- REVISI: Terapkan Slippage pada harga entry ---
        # Saat membeli (LONG), harga sedikit lebih tinggi. Saat menjual (SHORT), harga sedikit lebih rendah.
        if order_details['direction'] == 'LONG':
            entry_price = order_details['limit_price'] * (1 + SLIPPAGE['pct'])
        else: # SHORT
            entry_price = order_details['limit_price'] * (1 - SLIPPAGE['pct'])

        # --- REVISI: Hitung biaya entry (Maker Fee karena dari limit order) ---
        entry_fee = order_details['position_size_usd'] * FEES['maker']

        self.trade_id_counter += 1
        console.log(
            f"[green]Opening trade {self.trade_id_counter} on {symbol} ({order_details['strategy']}). "
            f"Limit: {order_details['limit_price']:.5f}, Entry (w/ slippage): {entry_price:.5f}[/green]"
        )

        self.active_positions[symbol] = {
            'id': self.trade_id_counter,
            'entry_time': fill_time,
            'entry_price': entry_price, # Gunakan harga entry yang sudah disesuaikan
            'direction': order_details['direction'],
            'sl_price': order_details['sl_price'],
            'tp_price': order_details['tp_price'],
            'position_size_usd': order_details['position_size_usd'],
            'margin_used': order_details['margin_used'],
            'strategy': order_details['strategy'],
            'entry_fee': entry_fee,
        }



    def close_trade(self, symbol, exit_price, exit_time, exit_reason):
        """Calculates PnL and finalizes a closed trade."""
        trade_details = self.active_positions[symbol]
        entry_price = trade_details['entry_price']
        direction = trade_details['direction']
        position_size_usd = trade_details['position_size_usd']

        # --- REVISI: Terapkan Slippage pada harga exit ---
        # Saat menjual (menutup LONG), harga sedikit lebih rendah. Saat membeli (menutup SHORT), harga sedikit lebih tinggi.
        if direction == 'LONG':
            actual_exit_price = exit_price * (1 - SLIPPAGE['pct'])
        else: # SHORT
            actual_exit_price = exit_price * (1 + SLIPPAGE['pct'])

        # --- REVISI: Hitung biaya exit (Taker atau Maker) ---
        # Take Profit adalah limit order (maker), Stop Loss dan End of Data adalah market order (taker)
        exit_fee_rate = FEES['maker'] if exit_reason == 'Take Profit' else FEES['taker']
        exit_fee = position_size_usd * exit_fee_rate
        total_fees = trade_details['entry_fee'] + exit_fee

        if direction == 'LONG':
            pnl_pct = (actual_exit_price - entry_price) / entry_price
        else: # SHORT
            pnl_pct = (entry_price - actual_exit_price) / entry_price
        
        # --- REVISI: Pastikan pnl_usd bukan NaN sebelum compounding ---
        pnl_usd = pnl_pct * position_size_usd if pd.notna(pnl_pct) and pd.notna(position_size_usd) else 0.0
        net_pnl_usd = pnl_usd - total_fees

        # Hanya tambahkan ke balance jika PnL valid, untuk mencegah balance menjadi NaN
        if pd.notna(pnl_usd):
            self.balance += pnl_usd

        self.trades.append({
            "ID": trade_details['id'],
            "Symbol": symbol,
            "Strategy": trade_details['strategy'],
            "Direction": direction,
            # --- REVISI: Gunakan entry_time dari detail trade yang disimpan ---
            "Entry Time": trade_details.get('entry_time'),
            "Exit Time": exit_time,
            "PnL (USD)": net_pnl_usd,
            "Balance": self.balance,
            "Exit Reason": exit_reason,
        })
        console.log(
            f"Closed trade {trade_details['id']} on {symbol}. Reason: {exit_reason}. "
            f"Net PnL: ${net_pnl_usd:,.2f} (Gross: ${pnl_usd:,.2f}, Fees: ${total_fees:,.2f}). New Balance: ${self.balance:,.2f}"
        )

    def create_pending_order(self, signal_row, signal_time, full_data, exit_params, symbol, current_risk_per_trade, default_leverage):
        """Creates a pending limit order instead of opening a trade directly."""
        # Don't create a new pending order if one already exists for this symbol
        if symbol in self.pending_orders:
            return

        # --- REVISI: Jangan buka trade di candle terakhir dari data ---
        if signal_time >= full_data.index[-1]:
            console.log(f"[yellow]Skipping signal on {symbol} at {signal_time} as it's the last available candle.[/yellow]")
            return

        # --- REVISI KRUSIAL: Pemeriksaan Batas Posisi Aktif Global ---
        # Dapatkan parameter dinamis dan periksa sebelum membuat pending order.
        # Periksa total eksposur: posisi aktif + order yang sedang pending.
        risk_params = get_dynamic_risk_params(self.balance)
        total_exposure = len(self.active_positions) + len(self.pending_orders)
        if total_exposure >= risk_params['max_active_positions']:
            # Lewati pembuatan order baru jika total eksposur sudah mencapai batas.
            return 

        signal_price = signal_row['close']
        direction = signal_row['signal']
        atr_val = signal_row[f"ATRr_{CONFIG['atr_period']}"]

        # --- REVISI: Limit Order Logic ---
        limit_offset_pct = 0.001 # 0.1% away from signal price
        limit_price = signal_price * (1 - limit_offset_pct) if direction == 'LONG' else signal_price * (1 + limit_offset_pct)
        expiration_candles = 10 # REVISI: Beri waktu lebih lama untuk order terisi

        sl_multiplier = exit_params.get('sl_multiplier', 1.5)
        rr_ratio = exit_params.get('rr_ratio', 1.5)

        # Handle dynamic params (Series/ndarray)
        if isinstance(sl_multiplier, (pd.Series, np.ndarray)):
            sl_multiplier = sl_multiplier[full_data.index.get_loc(signal_time)]
        if isinstance(rr_ratio, (pd.Series, np.ndarray)):
            rr_ratio = rr_ratio[full_data.index.get_loc(signal_time)]

        # --- Core Futures Logic ---
        risk_amount_usd = self.balance * current_risk_per_trade # Gunakan risk dinamis
        # SL is calculated from the intended limit price, not the signal price
        stop_loss_dist = atr_val * sl_multiplier
        stop_loss_pct = stop_loss_dist / limit_price
        
        # --- PERBAIKAN KEAMANAN: Validasi parameter risiko ---
        # Mencegah pembagian dengan nol atau logika terbalik jika parameter SL/TP tidak valid.
        if stop_loss_pct <= 0:
            console.log(f"[yellow]Skipping order for {symbol}: Invalid stop_loss_pct ({stop_loss_pct:.4f}). Check strategy exit_params.[/yellow]")
            return

        if stop_loss_pct == 0: return # Avoid division by zero

        # Gunakan leverage dinamis per simbol, dengan fallback ke leverage dinamis dari modal
        leverage_for_symbol = LEVERAGE_MAP.get(symbol, LEVERAGE_MAP.get("DEFAULT", default_leverage))

        position_size_usd = risk_amount_usd / stop_loss_pct
        margin_for_this_trade = position_size_usd / leverage_for_symbol

        # --- REVISI: Pindahkan pengecekan margin ke sini ---
        total_margin_used = sum(pos['margin_used'] for pos in self.active_positions.values())
        
        # Margin Call Protection
        if (total_margin_used + margin_for_this_trade) > self.balance:
            return # Not enough available balance for this trade.

        console.log(f"[blue]Creating pending {direction} order for {symbol} at limit price {limit_price:.5f} (Leverage: {leverage_for_symbol}x)[/blue]")

        stop_loss_price = limit_price - stop_loss_dist if direction == 'LONG' else limit_price + stop_loss_dist
        take_profit_price = limit_price + (stop_loss_dist * rr_ratio) if direction == 'LONG' else limit_price - (stop_loss_dist * rr_ratio)
        
        timeframe_duration = pd.to_timedelta(CONFIG['timeframe_signal'])
        expiration_time = signal_time + (timeframe_duration * expiration_candles)

        self.pending_orders[symbol] = {
            'creation_time': signal_time,
            'expiration_time': expiration_time,
            'limit_price': limit_price,
            'direction': direction,
            'sl_price': stop_loss_price,
            'tp_price': take_profit_price,
            'position_size_usd': position_size_usd,
            'margin_used': margin_for_this_trade,
            'strategy': signal_row['strategy'],
        }
    def get_results(self, args):
        if not self.trades:
            # --- REVISI: Tambahkan penanganan jika ada posisi aktif tapi tidak ada trade yang selesai ---
            console.log("[bold yellow]No trades were executed across the entire market scan.[/bold yellow]")
            return

        trades_df = pd.DataFrame(self.trades)
        net_profit = self.balance - self.initial_balance
        net_profit_pct = (net_profit / self.initial_balance) * 100
        total_trades = len(trades_df)
        wins = len(trades_df[trades_df['PnL (USD)'] > 0])
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

        # --- REVISI: Hitung Profit Factor dan Max Drawdown ---
        gross_profit = trades_df[trades_df['PnL (USD)'] > 0]['PnL (USD)'].sum()
        gross_loss = abs(trades_df[trades_df['PnL (USD)'] < 0]['PnL (USD)'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

        # Hitung equity curve untuk Max Drawdown
        equity_curve = self.initial_balance + trades_df['PnL (USD)'].cumsum()
        peak = equity_curve.cummax()
        drawdown = (peak - equity_curve) / peak
        max_drawdown = drawdown.max() * 100 if not drawdown.empty else 0

        # --- REVISI: Hitung perbandingan Long vs Short ---
        long_trades_df = trades_df[trades_df['Direction'] == 'LONG']
        short_trades_df = trades_df[trades_df['Direction'] == 'SHORT']
        
        total_long = len(long_trades_df)
        total_short = len(short_trades_df)
        
        long_wins = len(long_trades_df[long_trades_df['PnL (USD)'] > 0])
        short_wins = len(short_trades_df[short_trades_df['PnL (USD)'] > 0])

        long_win_rate = (long_wins / total_long) * 100 if total_long > 0 else 0
        short_win_rate = (short_wins / total_short) * 100 if total_short > 0 else 0


        # --- REVISI: Hitung dan tambahkan durasi backtest ---
        trades_df['Entry Time'] = pd.to_datetime(trades_df['Entry Time'])
        trades_df['Exit Time'] = pd.to_datetime(trades_df['Exit Time'])
        start_date = trades_df['Entry Time'].min()
        end_date = trades_df['Exit Time'].max()
        # --- REVISI: Buat format durasi yang adaptif (Tahun, Bulan, Hari) ---
        # Perhitungan ini diselaraskan dengan jumlah hari kalender yang terlibat.
        duration_str = "N/A"
        if pd.notna(start_date) and pd.notna(end_date):
            # Normalisasi ke awal hari untuk menghitung hari kalender
            start_day = start_date.normalize()
            end_day = end_date.normalize()
            
            # Hitung total hari kalender yang terlibat
            total_days = (end_day - start_day).days + 1

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
        summary_table.add_row("Strategies Tested", strategy_names)
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

        # --- REVISI: Tambahkan ringkasan PnL harian ---
        console.print("\n[bold]Daily PnL Summary:[/bold]")
        # Pastikan 'Exit Time' adalah datetime
        trades_df['Exit Time'] = pd.to_datetime(trades_df['Exit Time'])
        daily_summary = trades_df.set_index('Exit Time').resample('D').agg({
            'PnL (USD)': 'sum',
            'ID': 'count'
        }).rename(columns={'PnL (USD)': 'pnl', 'ID': 'trade_count'})
        daily_summary = daily_summary[daily_summary['trade_count'] > 0] # Hanya tampilkan hari dengan trade

        if not daily_summary.empty:
            daily_pnl_table = Table(show_header=True, header_style="bold yellow")
            daily_pnl_table.add_column("Date", style="cyan")
            daily_pnl_table.add_column("Trades", justify="right")
            daily_pnl_table.add_column("Daily PnL (USD)", justify="right")
            daily_pnl_table.add_column("Cumulative PnL (USD)", justify="right")

            cumulative_pnl = daily_summary['pnl'].cumsum()

            for date, row in daily_summary.iterrows():
                pnl = row['pnl']
                trade_count = row['trade_count']
                pnl_str = f"[green]${pnl:,.2f}[/green]" if pnl > 0 else f"[red]${pnl:,.2f}[/red]"
                cum_pnl_val = cumulative_pnl.loc[date]
                cum_pnl_str = f"[green]${cum_pnl_val:,.2f}[/green]" if cum_pnl_val > 0 else f"[red]${cum_pnl_val:,.2f}[/red]"
                daily_pnl_table.add_row(date.strftime('%Y-%m-%d'), str(trade_count), pnl_str, cum_pnl_str)
            
            console.print(daily_pnl_table)

        # --- REVISI: Tambahkan tabel performa per strategi jika > 1 strategi aktif ---
        if len(STRATEGY_CONFIG) > 1:
            console.print("\n[bold]Performance by Strategy:[/bold]")

            # Agregasi metrik untuk setiap strategi
            strategy_performance = trades_df.groupby('Strategy').agg(
                total_pnl=('PnL (USD)', 'sum'),
                total_trades=('ID', 'count'),
                wins=('PnL (USD)', lambda pnl: (pnl > 0).sum())
            ).reset_index()

            strategy_performance['win_rate'] = (strategy_performance['wins'] / strategy_performance['total_trades']) * 100
            strategy_performance = strategy_performance.sort_values(by="total_pnl", ascending=False)

            # Buat dan isi tabel
            strategy_table = Table(show_header=True, header_style="bold green")
            strategy_table.add_column("Strategy", style="green")
            strategy_table.add_column("Total Trades", justify="right")
            strategy_table.add_column("Win Rate", justify="right")
            strategy_table.add_column("Total PnL (USD)", justify="right")

            for _, row in strategy_performance.iterrows():
                pnl_str = f"[green]${row['total_pnl']:,.2f}[/green]" if row['total_pnl'] > 0 else f"[red]${row['total_pnl']:,.2f}[/red]"
                strategy_table.add_row(
                    row['Strategy'], str(row['total_trades']), f"{row['win_rate']:.2f}%", pnl_str
                )
            
            console.print(strategy_table)

        # --- REVISI: Tampilkan performa per koin dengan metrik yang lebih detail ---
        console.print("\n[bold]Performance by Symbol:[/bold]")

        def calculate_symbol_metrics(group):
            """Menghitung metrik performa untuk satu grup simbol."""
            gross_profit = group[group['PnL (USD)'] > 0]['PnL (USD)'].sum()
            gross_loss = abs(group[group['PnL (USD)'] < 0]['PnL (USD)'].sum())
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

            equity = group['PnL (USD)'].cumsum()
            peak = equity.cummax()
            drawdown = peak - equity
            max_drawdown = drawdown.max()

            long_trades = group[group['Direction'] == 'LONG']
            short_trades = group[group['Direction'] == 'SHORT']
            long_win_rate = (long_trades['PnL (USD)'] > 0).sum() / len(long_trades) * 100 if not long_trades.empty else 0
            short_win_rate = (short_trades['PnL (USD)'] > 0).sum() / len(short_trades) * 100 if not short_trades.empty else 0

            return pd.Series({
                'Total PnL (USD)': group['PnL (USD)'].sum(),
                'Total Trades': len(group),
                'Win Rate': (group['PnL (USD)'] > 0).sum() / len(group) * 100,
                'Profit Factor': profit_factor,
                'Max Drawdown (USD)': max_drawdown,
                'Longs (Win %)': f"{len(long_trades)} ({long_win_rate:.1f}%)",
                'Shorts (Win %)': f"{len(short_trades)} ({short_win_rate:.1f}%)"
            })

        perf_by_symbol = trades_df.groupby('Symbol').apply(calculate_symbol_metrics, include_groups=False)
        perf_by_symbol = perf_by_symbol.sort_values(by="Total PnL (USD)", ascending=False)

        symbol_table = Table(show_header=True, header_style="bold cyan")
        symbol_table.add_column("Symbol", style="cyan")
        symbol_table.add_column("Total Trades", justify="right")
        symbol_table.add_column("Win Rate", justify="right")
        symbol_table.add_column("Total PnL (USD)", justify="right")
        symbol_table.add_column("Profit Factor", justify="right")
        symbol_table.add_column("Max DD (USD)", justify="right")
        symbol_table.add_column("Longs (Win %)", justify="right")
        symbol_table.add_column("Shorts (Win %)", justify="right")

        for _, row in perf_by_symbol.iterrows():
            pnl_str = f"[green]${row['Total PnL (USD)']:,.2f}[/green]" if row['Total PnL (USD)'] > 0 else f"[red]${row['Total PnL (USD)']:,.2f}[/red]"
            dd_str = f"[red]${row['Max Drawdown (USD)']:,.2f}[/red]"
            symbol_table.add_row(row.name, f"{row['Total Trades']:.0f}", f"{row['Win Rate']:.2f}%", pnl_str, f"{row['Profit Factor']:.2f}", dd_str, row['Longs (Win %)'], row['Shorts (Win %)'])
        console.print(symbol_table)

        # --- Top Performing Trades ---
        console.print("\n[bold]Top 5 Most Profitable Trades:[/bold]")
        top_trades = trades_df.sort_values(by="PnL (USD)", ascending=False).head(5)
        top_trades_table = Table(show_header=True, header_style="bold green")
        for col in top_trades.columns:
            top_trades_table.add_column(col)
        for _, row in top_trades.iterrows():
            row_str = [str(item) for item in row]
            row_str[6] = f"[green]{row['PnL (USD)']:.2f}[/green]" # Colorize PnL
            top_trades_table.add_row(*row_str)
        console.print(top_trades_table)

        # Save results to CSV
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        filename = output_dir / "market_scan_results.csv"
        trades_df.to_csv(filename, index=False)
        console.log(f"\n[bold]Full trade log saved to '{filename}'[/bold]")
        
        # --- REVISI: Panggil fungsi untuk menulis ke BACKTEST_LOG.md ---
        self._log_results_to_markdown(
            args=args,
            net_profit=net_profit,
            net_profit_pct=net_profit_pct,
            total_trades=total_trades,
            win_rate=win_rate,
            profit_factor=profit_factor,
            max_drawdown=max_drawdown,
            duration_str=duration_str
        )

    def _log_results_to_markdown(self, args, **kwargs):
        """Secara otomatis menambahkan entri baru ke BACKTEST_LOG.md."""
        log_file_path = Path('BACKTEST_LOG.md')
        console.log(f"\n[bold]Appending results to {log_file_path}...[/bold]")

        # 1. Siapkan bagian Konfigurasi Strategi
        strategy_table_header = "| Nama Strategi                | Fungsi                 | Bobot (Weight) | Status   |\n"
        strategy_table_divider = "| ---------------------------- | ---------------------- | -------------- | -------- |\n"
        strategy_rows = ""
        for name, config in STRATEGY_CONFIG.items():
            # Asumsi: semua strategi di STRATEGY_CONFIG adalah yang aktif untuk run ini
            strategy_rows += f"| `{name}`      | `{config['function'].__name__}`    | {config['weight']}            | ✅ Aktif |\n"

        # 2. Siapkan bagian Hasil Ringkas
        results_table = (
            f"| Metrik            | Nilai                      |\n"
            f"| ----------------- | -------------------------- |\n"
            f"| Saldo Awal        | ${self.initial_balance:,.2f}                     |\n"
            f"| Saldo Akhir       | ${self.balance:,.2f}                     |\n"
            f"| **Net Profit**    | **+${kwargs['net_profit']:,.2f} (+{kwargs['net_profit_pct']:.2f}%)**       |\n"
            f"| Total Trades      | {kwargs['total_trades']}                         |\n"
            f"| Win Rate          | {kwargs['win_rate']:.2f}%                     |\n"
            f"| Profit Factor     | {kwargs['profit_factor']:.2f}                       |\n"
            f"| Max Drawdown      | {kwargs['max_drawdown']:.2f}%                      |\n"
        )

        # 3. Gabungkan semua menjadi satu entri log
        log_entry = (
            f"\n---\n\n"
            f"## Backtest: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Parameter:**\n"
            f"-   **Simbol:** Top {args.max_symbols} (berdasarkan volume)\n"
            f"-   **Candles:** {args.limit}\n"
            f"-   **Periode:** ~{kwargs['duration_str']}\n\n"
            f"**Konfigurasi Strategi (`STRATEGY_CONFIG` saat dijalankan):**\n\n"
            f"{strategy_table_header}"
            f"{strategy_table_divider}"
            f"{strategy_rows}\n"
            f"**Hasil Ringkas:**\n\n"
            f"{results_table}\n"
            f"**Catatan & Observasi:**\n"
            f"-   (Isi observasi Anda di sini)\n\n"
        )

        # 4. Tulis entri ke file (prepend/tambahkan di awal)
        original_content = log_file_path.read_text() if log_file_path.exists() else ""
        log_file_path.write_text(log_entry + original_content)
        console.log(f"[green]✅ Results successfully appended to {log_file_path}[/green]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Binance Futures Market Scanner Backtester")
    parser.add_argument("--limit", type=int, default=1500, help="Number of 5m candles to backtest per symbol")
    parser.add_argument("--max_symbols", type=int, default=50, help="Maximum number of symbols to scan (sorted by volume)")
    args = parser.parse_args()

    import asyncio # Impor asyncio di sini agar hanya digunakan saat skrip dijalankan
    # --- PERBAIKAN: Logika baru untuk mengambil simbol secara asinkron ---
    async def fetch_symbols_async():
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

    scanner = PortfolioBacktester(initial_balance=CONFIG["account_balance"])

    # --- PERBAIKAN: Inisialisasi ulang exchange sinkron untuk backtester ---
    # Backtester utama membutuhkan instance exchange sinkron untuk mengambil data historis.
    # Ini terpisah dari koneksi asinkron yang digunakan untuk mengambil daftar simbol.
    scanner.exchange = ccxt.binance({
        'apiKey': API_KEYS['live']['api_key'],
        'secret': API_KEYS['live']['api_secret'],
        'options': {'defaultType': 'future'},
        'enableRateLimit': True,
    })
    scanner.exchange.set_sandbox_mode(False)

    symbols_to_scan = all_symbols[:args.max_symbols]

    scanner.run_scan(symbols=symbols_to_scan, limit=args.limit)
    scanner.get_results(args=args)