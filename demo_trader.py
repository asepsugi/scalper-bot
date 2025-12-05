import ccxt.pro as ccxtpro  # Gunakan ccxt.pro untuk websocket
import asyncio
import pandas as pd
import aiofiles
import numpy as np
import math # Impor math untuk fungsi ceil
import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table

from config import CONFIG, LEVERAGE_MAP, API_KEYS, TELEGRAM, LIVE_TRADING_CONFIG
from indicators import fetch_binance_data, calculate_indicators
from utils.common_utils import get_all_futures_symbols, get_dynamic_risk_params
from utils.data_preparer import prepare_data
from utils.telegram_notifier import TelegramNotifier
from strategies import STRATEGY_CONFIG

console = Console()
notifier = TelegramNotifier(TELEGRAM['bot_token'], TELEGRAM['chat_id'])

# --- Konfigurasi Spesifik Demo ---
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
DEMO_STATE_FILE = OUTPUT_DIR / "demo_positions.json"
DEMO_EVENT_LOG_FILE = OUTPUT_DIR / "demo_events.log"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def log_restart_event():
    """Menulis event restart secara sinkron saat bot demo dimulai."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(DEMO_EVENT_LOG_FILE, 'a') as f:
        f.write(f"[{now}] --- DEMO BOT RESTARTED ---\n")

class DemoTrader:
    def __init__(self, symbols, max_symbols_to_trade):
        self.symbols = symbols
        self.max_symbols_to_trade = max_symbols_to_trade
        self.exchange = None
        self.historical_data = {symbol: pd.DataFrame() for symbol in symbols}
        self.is_fetching = {symbol: False for symbol in symbols}
        self.active_positions = {}
        self.open_limit_orders = set()
        self.load_positions_state()
        self.signal_queue = asyncio.Queue()
        self.insufficient_balance_attempts = 0
        self.cooldown_until = None
        self.cooldown_duration_hours = 6

    async def log_event(self, message):
        """Menulis event ke file log demo secara asinkron."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{now}] {message}\n"
        async with aiofiles.open(DEMO_EVENT_LOG_FILE, mode='a') as f:
            await f.write(log_message)

    async def initialize_exchange(self):
        """Inisialisasi koneksi exchange ke Binance Futures TESTNET."""
        self.exchange = ccxtpro.binance({
            'apiKey': API_KEYS['testnet']['api_key'],
            'secret': API_KEYS['testnet']['api_secret'],
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
            },
            # --- PERBAIKAN: Gunakan 'test': True untuk mengakses Demo Trading Environment ---
            # Ini adalah cara baru yang didukung ccxt untuk mengakses demo futures.
            'test': True,
            'enableRateLimit': True,
        })
        # Hapus panggilan set_sandbox_mode(True) yang sudah usang.
        console.log("[bold yellow]Berhasil terhubung ke Binance Futures (DEMO TRADING).[/bold yellow]")
        await notifier.send_message("🧪 *Bot Demo Dimulai!*\nTerhubung ke Binance Futures Demo Trading.")

    def save_positions_state(self):
        """Menyimpan posisi aktif demo ke file JSON."""
        with open(DEMO_STATE_FILE, 'w') as f:
            serializable_positions = {s: {'entryPrice': p['entryPrice'], 'positionAmt': p['positionAmt']} for s, p in self.active_positions.items()}
            json.dump(serializable_positions, f, indent=4)

    def load_positions_state(self):
        """Memuat posisi aktif demo dari file JSON saat bot dimulai."""
        if DEMO_STATE_FILE.exists():
            with open(DEMO_STATE_FILE, 'r') as f:
                self.active_positions = json.load(f)
            console.log(f"[yellow]State posisi demo dimuat dari {DEMO_STATE_FILE}. Posisi aktif: {list(self.active_positions.keys())}[/yellow]")

    async def prefetch_data(self):
        """Mengambil data historis awal untuk setiap simbol."""
        console.log("Mengambil data historis awal untuk demo...")
        tasks = [self.fetch_initial_data(symbol) for symbol in self.symbols]
        results = await asyncio.gather(*tasks)

        successful_symbols = [symbol for symbol, success in zip(self.symbols, results) if success]
        failed_symbols = [symbol for symbol, success in zip(self.symbols, results) if not success]

        if failed_symbols:
            console.log(f"[yellow]Menghapus simbol berikut dari demo karena riwayat data tidak mencukupi: {', '.join(failed_symbols)}[/yellow]")

        self.symbols = successful_symbols
        console.log(f"[green]Data historis awal berhasil dimuat untuk {len(self.symbols)} simbol yang valid di demo.[/green]")

    async def fetch_initial_data(self, symbol):
        """Mengambil data awal untuk satu simbol dan memvalidasi jumlahnya."""
        try:
            console.log(f"Fetching initial data for [cyan]{symbol}[/cyan] (Demo)...")
            required_candles = 650
            df_5m = await fetch_binance_data(self.exchange, symbol, '5m', limit=required_candles, use_cache=False)
            if df_5m is not None and not df_5m.empty:
                if len(df_5m) >= required_candles - 50:
                    self.historical_data[symbol] = df_5m.copy()
                    console.log(f"Data awal untuk [cyan]{symbol}[/cyan] dimuat ({len(df_5m)} candles).")
                    return True
            console.log(f"[yellow]Gagal memuat data yang cukup untuk {symbol} di demo (hanya dapat {len(df_5m) if df_5m is not None else 0} dari {required_candles}).[/yellow]")
            return False
        except Exception as e:
            console.log(f"[red]Error saat prefetch data {symbol} di demo: {e}[/red]")
            await self.log_event(f"DEMO_PREFETCH_FAIL: {symbol} - {e}")
            return False

    async def handle_kline(self, symbol, kline):
        """Callback yang dieksekusi saat ada data kline baru dari websocket."""
        timestamp, o, h, l, c, v = kline
        is_closed = True

        if is_closed and not self.is_fetching.get(symbol, False):
            self.is_fetching[symbol] = True
            try:
                console.log(f"Candle [cyan]{symbol}[/cyan] 5m (Demo) ditutup pada [yellow]{pd.to_datetime(timestamp, unit='ms', utc=True)}[/yellow]. Harga: {c}")
                
                new_candle_df = pd.DataFrame([{
                    'timestamp': pd.to_datetime(timestamp, unit='ms', utc=True),
                    'open': float(o), 'high': float(h), 'low': float(l), 'close': float(c), 'volume': float(v)
                }]).set_index('timestamp')
                
                self.historical_data[symbol] = pd.concat([self.historical_data[symbol], new_candle_df])
                self.historical_data[symbol] = self.historical_data[symbol][~self.historical_data[symbol].index.duplicated(keep='last')]
                self.historical_data[symbol] = self.historical_data[symbol].tail(650)

                await self.signal_queue.put({'symbol': symbol, 'data': self.historical_data[symbol].copy()})

            except Exception as e:
                console.log(f"[bold red]Error di handle_kline (Demo) untuk {symbol}: {e}[/bold red]")
                await self.log_event(f"DEMO_KLINE_HANDLE_FAIL: {symbol} - {e}")
            finally:
                self.is_fetching[symbol] = False

    async def signal_processor(self):
        """Loop untuk mengambil sinyal dari antrian dan menganalisisnya."""
        while True:
            try:
                task = await self.signal_queue.get()
                symbol, df_5m = task['symbol'], task['data']

                # --- OPTIMISASI: Pindahkan pemeriksaan balance ke execute_trade_logic ---
                # Cek batas posisi hanya berdasarkan state internal untuk mengurangi panggilan API.
                total_exposure = len(self.active_positions) + len(self.open_limit_orders)
                if total_exposure >= LIVE_TRADING_CONFIG.get('max_active_positions_limit', 10): # Gunakan batas statis sementara
                    console.log(f"[yellow]SKIP DEMO SIGNAL for {symbol}: Batas total eksposur ({total_exposure}) telah tercapai.[/yellow]")
                    continue

                if symbol in self.active_positions or symbol in self.open_limit_orders:
                    continue

                def resample_df(df, timeframe):
                    return df.resample(timeframe).agg({
                        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
                    }).dropna()

                df_15m = resample_df(df_5m, '15min')
                df_1h = resample_df(df_5m, 'h')

                if any(df.empty for df in [df_15m, df_1h]):
                    console.log(f"[yellow]Data resample untuk {symbol} (Demo) tidak cukup, analisis dilewati.[/yellow]")
                    continue

                # --- PERBAIKAN: Selaraskan dengan live_trader, hitung indikator SEBELUM prepare_data ---
                df_5m = calculate_indicators(df_5m)
                df_15m = calculate_indicators(df_15m)
                df_1h = calculate_indicators(df_1h)

                # Siapkan data gabungan
                base_data = prepare_data(df_5m, df_15m, df_1h) # type: ignore
                if base_data is None or base_data.empty:
                    console.log(f"[yellow]Gagal mempersiapkan data untuk {symbol} (Demo), analisis dilewati.[/yellow]")
                    continue

                # --- PERBAIKAN KONSISTENSI: Hapus baris dengan NaN sebelum analisis ---
                base_data_cleaned = base_data.dropna()
                if base_data_cleaned.empty: continue
                latest_candle = base_data_cleaned.iloc[-1]

                long_score = 0.0
                short_score = 0.0
                consensus_contributors = []

                for strategy_name, config in STRATEGY_CONFIG.items():
                    signal_function = config["function"]
                    weight = config["weight"]
                    long_signals, short_signals, exit_params = signal_function(base_data_cleaned.copy())
                    
                    if not long_signals.empty and long_signals.iloc[-1]:
                        long_score += weight
                        consensus_contributors.append({'strategy': strategy_name, 'direction': 'LONG', 'params': exit_params})
                    elif not short_signals.empty and short_signals.iloc[-1]:
                        short_score += weight
                        consensus_contributors.append({'strategy': strategy_name, 'direction': 'SHORT', 'params': exit_params})

                num_strategies = len(STRATEGY_CONFIG)
                if num_strategies == 1:
                    required_score = next(iter(c['weight'] for c in STRATEGY_CONFIG.values())) * 0.99
                elif num_strategies == 2:
                    required_score = min(c['weight'] for c in STRATEGY_CONFIG.values()) * 0.99
                else:
                    total_possible_score = sum(c['weight'] for c in STRATEGY_CONFIG.values())
                    consensus_ratio = LIVE_TRADING_CONFIG.get('consensus_ratio', 0.55)
                    required_score = total_possible_score * consensus_ratio

                final_signal = None
                if long_score >= required_score:
                    final_signal = 'LONG'
                elif short_score >= required_score:
                    final_signal = 'SHORT'

                # --- PERBAIKAN: Tambahkan logging diagnostik untuk skor ---
                # Cetak skor jika ada setidaknya satu sinyal, untuk mempermudah debug.
                if long_score > 0 or short_score > 0:
                    console.log(f"[grey50]Debug Score for {symbol}: Long={long_score:.2f}, Short={short_score:.2f}, Required={required_score:.2f}[/grey50]")

                if final_signal:
                    primary_contributor = next(c for c in consensus_contributors if c['direction'] == final_signal)
                    strategy_name = primary_contributor['strategy']
                    exit_params = primary_contributor['params']
                    
                    contributing_strats = [c['strategy'] for c in consensus_contributors if c['direction'] == final_signal]
                    consensus_details = f"({len(contributing_strats)}/{len(STRATEGY_CONFIG)}: {', '.join(contributing_strats)})"

                    signal_price = latest_candle['close']
                    atr_val = latest_candle[f"ATRr_{CONFIG['atr_period']}"]
                    
                    # --- PERBAIKAN: Gunakan offset yang dapat dikonfigurasi ---
                    limit_offset_pct = EXECUTION.get("limit_order_offset_pct", 0.0002)
                    limit_price_float = signal_price * (1 - limit_offset_pct) if final_signal == 'LONG' else signal_price * (1 + limit_offset_pct)

                    sl_multiplier = exit_params.get('sl_multiplier', 1.5)
                    rr_ratio = exit_params.get('rr_ratio', 1.5)

                    # PERBAIKAN: Gunakan .iloc untuk konsistensi dan praktik terbaik
                    if isinstance(sl_multiplier, (pd.Series, np.ndarray)): sl_multiplier = sl_multiplier.iloc[-1]
                    if isinstance(rr_ratio, (pd.Series, np.ndarray)): rr_ratio = rr_ratio.iloc[-1]

                    stop_loss_dist = atr_val * sl_multiplier

                    # --- PERBAIKAN: Selaraskan dengan live_trader, jangan hitung harga absolut di sini ---
                    limit_price_str = self.exchange.price_to_precision(symbol, limit_price_float)
                    leverage = LEVERAGE_MAP.get(symbol, LEVERAGE_MAP.get("DEFAULT", 10))

                    log_msg = f"DEMO_SIGNAL_CONSENSUS: {final_signal} {symbol} {consensus_details} | Target Entry:{limit_price_str}"
                    console.log(f"[bold yellow]KONSENSUS SINYAL DEMO DITEMUKAN![/bold yellow] {log_msg}")
                    await self.log_event(log_msg)
                    
                    notif_msg = (f"🧪 *Sinyal Demo: {final_signal} {symbol}*\n{consensus_details}\n\n"
                                 f"Target Entry: `{limit_price_str}`\nLeverage: `{leverage}x`")
                    await notifier.send_message(notif_msg)
                    # --- PERBAIKAN: Kirim stop_loss_dist dan rr_ratio, bukan harga absolut ---
                    await self.execute_trade_logic(symbol, final_signal, latest_candle, exit_params, strategy_name, limit_price_float, stop_loss_dist, rr_ratio)

            except KeyError as e:
                console.log(f"[bold red]Error KeyError di signal_processor (Demo) untuk {symbol}: Kolom {e} tidak ditemukan.[/bold red]")
            except Exception as e:
                console.log(f"[bold red]Error di signal_processor (Demo): {e}[/bold red]")
                # --- PERBAIKAN: Tambahkan notifikasi jika IP diblokir ---
                if "418" in str(e) and "banned" in str(e):
                    await notifier.send_message(f"🚨 *IP DIBLOKIR (DEMO)!* 🚨\nBot demo tidak dapat melanjutkan. Harap ganti IP atau tunggu hingga blokir dicabut.\nError: `{str(e)}`")
                await self.log_event(f"DEMO_SIGNAL_PROCESSOR_FAIL: {e}")
            finally:
                self.signal_queue.task_done()

    async def execute_trade_logic(self, symbol, direction, candle, exit_params, strategy_name, limit_price_float, stop_loss_dist, rr_ratio):
        """Menghitung parameter dan menempatkan order di bursa demo."""
        if self.cooldown_until and datetime.now() < self.cooldown_until:
            return
        elif self.cooldown_until and datetime.now() >= self.cooldown_until:
            log_msg = "DEMO_COOLDOWN_ENDED: Mode cooldown saldo tidak cukup telah berakhir."
            console.log(f"[green]{log_msg}[/green]")
            await self.log_event(log_msg)
            await notifier.send_message("✅ *Cooldown Demo Berakhir*\nPercobaan eksekusi trade diaktifkan kembali.")
            self.cooldown_until = None
            self.insufficient_balance_attempts = 0

        try:
            balance_info = await self.exchange.fetch_balance()
            if 'USDT' not in balance_info:
                raise ValueError(f"Respons saldo demo tidak valid. Diterima: {str(balance_info)[:200]}")
            free_balance = balance_info['USDT']['free']
            total_balance = balance_info['USDT']['total']
            used_margin = balance_info['USDT']['used']

            signal_price = candle['close']
            risk_params = get_dynamic_risk_params(total_balance)
            current_risk_per_trade = risk_params['risk_per_trade']

            if free_balance < 5:
                log_msg = f"DEMO_EXECUTION_SKIPPED: {direction} {symbol} - Saldo demo tidak cukup (Free: ${free_balance:.2f})."
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                await notifier.send_message(f"⚠️ *Trade Demo Dilewati* untuk {symbol}\nAlasan: Saldo demo tidak cukup.")

                self.insufficient_balance_attempts += 1
                if self.insufficient_balance_attempts >= 2:
                    self.cooldown_until = datetime.now() + pd.Timedelta(hours=self.cooldown_duration_hours)
                    cooldown_end_str = self.cooldown_until.strftime('%Y-%m-%d %H:%M:%S')
                    log_msg = (f"DEMO_COOLDOWN_STARTED: Saldo demo tidak cukup terdeteksi {self.insufficient_balance_attempts} kali. "
                               f"Memasuki mode cooldown selama {self.cooldown_duration_hours} jam, berakhir pada {cooldown_end_str}.")
                    console.log(f"[bold red]{log_msg}[/bold red]")
                    await self.log_event(log_msg)
                    await notifier.send_message(f"🥶 *Mode Cooldown Demo Aktif*\nBot demo tidak akan mencoba eksekusi trade selama {self.cooldown_duration_hours} jam.")
                return

            stop_loss_pct = stop_loss_dist / limit_price_float
            risk_amount_usd = total_balance * current_risk_per_trade

            if stop_loss_pct == 0:
                log_msg = f"DEMO_EXECUTION_SKIPPED: {direction} {symbol} - Kalkulasi stop_loss_pct menghasilkan nol."
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                return

            leverage = LEVERAGE_MAP.get(symbol, risk_params['default_leverage'])
            position_size_usd = risk_amount_usd / stop_loss_pct
            margin_for_this_trade = position_size_usd / leverage
            amount = position_size_usd / signal_price

            market_info = self.exchange.markets.get(symbol, {})
            min_notional = market_info.get('limits', {}).get('cost', {}).get('min')

            if min_notional and position_size_usd < min_notional:
                log_msg = (f"DEMO_EXECUTION_SKIPPED: {direction} {symbol} - Ukuran posisi (${position_size_usd:.2f}) "
                           f"di bawah minimum notional (${min_notional}).")
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                await notifier.send_message(f"⚠️ *Trade Demo Dilewati* untuk {symbol}\nAlasan: Ukuran posisi terlalu kecil.")
                return

            max_margin_pct = LIVE_TRADING_CONFIG['max_margin_usage_pct']
            margin_limit_usd = total_balance * max_margin_pct
            projected_used_margin = used_margin + margin_for_this_trade

            if projected_used_margin > margin_limit_usd:
                log_msg = f"DEMO_EXECUTION_SKIPPED: {direction} {symbol} - Proyeksi margin ({projected_used_margin:.2f}) akan melebihi batas ({margin_limit_usd:.2f})."
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                await notifier.send_message(f"⚠️ *Trade Demo Dilewati* untuk {symbol}\nAlasan: Batas margin akan terlampaui.")
                return

            amount = self.exchange.amount_to_precision(symbol, amount)
            limit_price_str = self.exchange.price_to_precision(symbol, limit_price_float)

            console.log(f"Mencoba menempatkan order demo untuk {symbol}...")
            
            await self.exchange.set_leverage(leverage, symbol)
            console.log(f"Leverage demo untuk {symbol} diatur ke {leverage}x.")

            side = 'buy' if direction == 'LONG' else 'sell'
            params = {}
            if not LIVE_TRADING_CONFIG.get("use_advanced_exit_logic", True):
                # Mode Statis: Tempatkan SL/TP langsung di bursa
                # PERBAIKAN: Hitung SL/TP absolut di sini, tepat sebelum mengirim order
                sl_price_float = limit_price_float - stop_loss_dist if direction == 'LONG' else limit_price_float + stop_loss_dist
                tp_price_float = limit_price_float + (stop_loss_dist * rr_ratio) if direction == 'LONG' else limit_price_float - (stop_loss_dist * rr_ratio)
                sl_price_str = self.exchange.price_to_precision(symbol, sl_price_float)
                tp_price_str = self.exchange.price_to_precision(symbol, tp_price_float)
                params = {
                    'stopLoss': {'type': 'STOP_MARKET', 'triggerPrice': sl_price_str},
                    'takeProfit': {'type': 'TAKE_PROFIT_MARKET', 'triggerPrice': tp_price_str}
                }
            
            # --- PERBAIKAN: Selaraskan dengan live_trader, gunakan tipe order yang dapat dikonfigurasi ---
            entry_order_type = EXECUTION.get("entry_order_type", "limit")
            if entry_order_type == "market":
                order = await self.exchange.create_order(symbol, 'market', side, amount, None, params)
            else: # Default ke limit order
                order = await self.exchange.create_order(symbol, 'limit', side, amount, limit_price_str, params)
            
            # --- PERBAIKAN: Selaraskan dengan live_trader, simpan state di dict ---
            self.open_limit_orders[symbol] = {
                'stop_loss_dist': stop_loss_dist,
                'rr_ratio': rr_ratio,
                'positionAmt': amount if side == 'buy' else -amount,
                'strategy': strategy_name,
            }

            console.log(f"[bold yellow]Order demo berhasil dibuat untuk {symbol}. ID: {order['id']}[/bold yellow]")
            await notifier.send_message(f"🧪 *Order Demo Ditempatkan* untuk {symbol}!\nID: `{order['id']}`")
            await self.log_event(f"DEMO_EXECUTION_SUCCESS: {direction} {symbol} - Order ID: {order['id']}")

        except Exception as e:
            console.log(f"[bold red]Error saat eksekusi trade demo {symbol}: {e}[/bold red]")
            # --- PERBAIKAN: Tambahkan notifikasi jika IP diblokir ---
            if "418" in str(e) and "banned" in str(e):
                await notifier.send_message(f"🚨 *IP DIBLOKIR (DEMO)!* 🚨\nBot demo tidak dapat melanjutkan. Harap ganti IP atau tunggu hingga blokir dicabut.\nError: `{str(e)}`")
            await notifier.send_message(f"❌ *Error Eksekusi Demo* pada {symbol}:\n`{e}`")
            await self.log_event(f"DEMO_EXECUTION_FAIL: {direction} {symbol} - Error: {e}")

    async def dry_run_check(self):
        """
        Melakukan pemeriksaan 'kering' pada environment testnet.
        REVISI: Menyelaraskan logika dengan live_trader.py untuk mengatasi error -4164.
        """
        console.log("[yellow]Memulai pemeriksaan Dry Run untuk validasi API Demo...[/yellow]")
        try:
            console.log("  - Memeriksa koneksi ke endpoint saldo (fetch_balance)...")
            balance_info = await self.exchange.fetch_balance()
            if 'USDT' not in balance_info:
                raise ValueError(f"Dry Run Demo Gagal: Respons saldo tidak valid. Diterima: {str(balance_info)[:200]}")
            console.log("    [green]✅ Endpoint saldo Demo OK.[/green]")

            # --- PERBAIKAN: Gunakan ETH/USDT yang memiliki minNotional lebih rendah ---
            sample_symbol = 'ETH/USDT'
            console.log(f"  - Memvalidasi izin trading dengan order dummy pada {sample_symbol}...")

            ticker = await self.exchange.fetch_ticker(sample_symbol)
            price = ticker['last']

            # Logika normalisasi simbol dari live_trader
            try:
                market_info = self.exchange.market(sample_symbol)
                sample_symbol_ccxt = market_info['symbol']
            except ccxtpro.BadSymbol:
                sample_symbol_ccxt = sample_symbol.split(':')[0]
            market = self.exchange.markets[sample_symbol_ccxt]
            amount_precision = market['precision']['amount']

            # Perhitungan dummy order dari live_trader
            dummy_price_float = price * 0.5 
            
            if dummy_price_float > 0 and amount_precision > 0:
                # Targetkan nosional $21, cukup untuk melewati minNotional ETH
                required_amount = 21.0 / dummy_price_float 
                dummy_amount_float = np.ceil(required_amount / amount_precision) * amount_precision
            else:
                dummy_amount_float = 0.0

            dummy_price_str = self.exchange.price_to_precision(sample_symbol_ccxt, dummy_price_float)
            dummy_amount_str = self.exchange.amount_to_precision(sample_symbol_ccxt, dummy_amount_float)

            # Debugging table dari live_trader
            debug_table = Table(title="[bold yellow]Dry Run Demo Dummy Order Debug[/bold yellow]")
            debug_table.add_column("Parameter", style="cyan")
            debug_table.add_column("Value", style="white")
            debug_table.add_row("Sample Symbol", str(sample_symbol_ccxt))
            debug_table.add_row("Formatted Amount (str)", f"'{dummy_amount_str}'")
            debug_table.add_row("Formatted Price (str)", f"'{dummy_price_str}'")
            projected_notional = float(dummy_price_str) * float(dummy_amount_str) if dummy_amount_str and dummy_price_str else 0.0
            debug_table.add_row("Projected Notional", f"${projected_notional:.4f}")
            console.print(debug_table)

            dummy_order = await self.exchange.create_order(sample_symbol_ccxt, 'limit', 'buy', dummy_amount_str, dummy_price_str, {'postOnly': True})
            await self.exchange.cancel_order(dummy_order['id'], sample_symbol_ccxt)

            console.log("    [green]✅ Izin trading Demo OK.[/green]")
            console.log("[bold green]✅ Dry Run Demo berhasil. Semua pemeriksaan API lolos.[/bold green]")
            return True
        except Exception as e:
            console.log("[bold red]❌ Dry Run Demo GAGAL.[/bold red]")
            console.print(f"  Error: {e}")
            console.log("[bold yellow]Hint: Pastikan API Key Testnet Anda benar, memiliki saldo (bisa di-claim dari Faucet), dan izin 'Futures' aktif.[/bold yellow]")
            await self.log_event(f"DEMO_DRY_RUN_FAIL: {e}")
            return False

    async def position_manager(self):
        """Secara periodik memeriksa dan mengelola posisi/order aktif di demo."""
        while True:
            try:
                orders = await self.exchange.watch_orders()
                for order in orders:
                    status = order.get('status')
                    symbol = order.get('symbol')
                    symbol_ccxt = symbol.replace('USDT', '/USDT')

                    if status == 'closed':
                        if order['type'] in ['limit', 'market'] and symbol_ccxt not in self.active_positions:
                            # --- PERBAIKAN: Selaraskan dengan live_trader ---
                            custom_state = self.open_limit_orders.pop(symbol_ccxt, {})
                            if not custom_state:
                                continue

                            position_info = await self.exchange.fetch_position(symbol)
                            final_position_details = position_info['info']
                            final_position_details.update(custom_state)

                            # --- PERBAIKAN KRUSIAL: Hitung SL/TP dari harga entry riil ---
                            entry_price = float(final_position_details['entryPrice'])
                            stop_loss_dist = final_position_details['stop_loss_dist']
                            rr_ratio = final_position_details['rr_ratio']
                            direction = "LONG" if float(final_position_details['positionAmt']) > 0 else "SHORT"
                            final_position_details['sl_price'] = entry_price - stop_loss_dist if direction == "LONG" else entry_price + stop_loss_dist
                            final_position_details['initial_sl'] = final_position_details['sl_price']
                            final_position_details['tp_price'] = entry_price + (stop_loss_dist * rr_ratio) if direction == "LONG" else entry_price - (stop_loss_dist * rr_ratio)

                            self.active_positions[symbol_ccxt] = final_position_details
                            self.save_positions_state()
                            filled_price = order.get('average', order.get('price'))
                            msg = f"✅ *Posisi Demo Dibuka* untuk {symbol} @ `{filled_price}`"
                            console.log(f"[yellow]{msg}[/yellow]")
                            await notifier.send_message(msg)
                            await self.log_event(f"DEMO_ENTRY_FILLED: Posisi {symbol} dibuka @ {filled_price}")
                        else:
                            if symbol_ccxt in self.open_limit_orders.keys():
                                self.open_limit_orders.pop(symbol_ccxt, None)

                            if symbol_ccxt in self.active_positions:
                                del self.active_positions[symbol_ccxt]
                                self.save_positions_state()
                            filled_price = order.get('average', order.get('price'))
                            msg = f"🔴 *Posisi Demo Ditutup* untuk {symbol} @ `{filled_price}`"
                            console.log(f"[magenta]{msg}[/magenta]")
                            await notifier.send_message(msg)
                            await self.log_event(f"DEMO_EXIT_FILLED: Posisi {symbol} ditutup @ {filled_price}")

                    elif status in ['canceled', 'expired']:
                        if symbol_ccxt in self.open_limit_orders.keys():
                            self.open_limit_orders.pop(symbol_ccxt, None)

                        msg = f"ℹ️ *Order Demo Dibatalkan/Kedaluwarsa* untuk {symbol}"
                        console.log(f"[yellow]{msg}[/yellow]")
                        await notifier.send_message(msg)
                        await self.log_event(f"DEMO_ORDER_CANCEL: Order untuk {symbol} dibatalkan/kedaluwarsa.")

            except asyncio.CancelledError:
                raise
            except Exception as e:
                console.log(f"[red]Error pada position_manager (Demo): {e}[/red]")
                await self.log_event(f"DEMO_POSITION_MANAGER_FAIL: {e}")
                if isinstance(e, ccxtpro.NotSupported):
                    break
                await asyncio.sleep(10)

    async def main_loop(self):
        """Loop utama untuk mendengarkan data kline dari semua simbol di demo."""
        await self.initialize_exchange()

        # --- REVISI: Dapatkan balance awal dan posisi aktif saat startup ---
        initial_balance_info = await self.exchange.fetch_balance()
        initial_total_balance = initial_balance_info.get('USDT', {}).get('total', 0)

        # --- REVISI BARU: Cetak status awal ke log ---
        startup_log_msg = f"DEMO_STARTUP_STATE: Balance: ${initial_total_balance:.2f}, Loaded Active Positions: {len(self.active_positions)}"
        console.log(f"[bold yellow]{startup_log_msg}[/bold yellow]")
        await self.log_event(startup_log_msg)

        # Tentukan parameter dinamis berdasarkan modal
        dynamic_params = get_dynamic_risk_params(initial_total_balance)
        self.max_symbols_to_trade = dynamic_params['max_active_positions'] * 10

        # --- PERBAIKAN: Panggil fungsi tanpa argumen agar selaras dengan live_trader ---
        all_symbols = await get_all_futures_symbols(self.exchange)
        self.symbols = all_symbols[:self.max_symbols_to_trade]
        console.log(f"Modal demo awal: ${initial_total_balance:.2f}. Menggunakan parameter risiko dinamis: {dynamic_params}")
        console.log(f"Memindai [bold]{len(self.symbols)}[/bold] simbol teratas di Testnet.")

        self.historical_data = {}
        self.is_fetching = {symbol: False for symbol in self.symbols}

        if not self.symbols:
            console.log("[bold red]Tidak ada simbol yang ditemukan di Testnet. Bot berhenti.[/bold red]")
            await notifier.send_message("❌ Bot Demo Berhenti: Tidak ada simbol yang bisa diproses di Testnet.")
            await self.log_event("NO_VALID_SYMBOLS_DEMO: Bot berhenti.")
            return

        await self.prefetch_data()

        if not await self.dry_run_check():
            console.log("[bold red]Pemeriksaan Dry Run Demo gagal. Bot berhenti.[/bold red]")
            return

        self.is_fetching = {symbol: False for symbol in self.symbols}

        kline_tasks = [self.watch_ohlcv_loop(symbol) for symbol in self.symbols]
        processor_task = self.signal_processor()
        manager_task = self.position_manager()
        await asyncio.gather(*kline_tasks, processor_task, manager_task)

    async def watch_ohlcv_loop(self, symbol):
        """Loop tak terbatas untuk satu simbol, menangani koneksi ulang."""
        timeframe = '5m'
        while True:
            try:
                console.log(f"Memulai websocket demo untuk [cyan]{symbol}[/cyan] timeframe {timeframe}...")
                while True:
                    klines = await self.exchange.watch_ohlcv(symbol, timeframe, params={'type': 'future'})
                    for kline in klines:
                        try:
                            await self.handle_kline(symbol, kline)
                        except asyncio.CancelledError:
                            raise
            except (ccxtpro.NetworkError, ccxtpro.ExchangeError) as e:
                log_msg = f"DEMO_WEBSOCKET_ERROR: {symbol} - {e}. Reconnecting..."
                await self.log_event(log_msg)
                console.log(f"[bold red]Websocket error demo untuk {symbol}: {e}. Mencoba menghubungkan ulang dalam 30 detik...[/bold red]")
                await asyncio.sleep(30)

async def main():
    """Fungsi utama async untuk menjalankan bot demo dan menangani cleanup."""
    trader = None
    try:
        console.log("[bold yellow]Memulai bot trading DEMO...[/bold yellow]")
        trader = DemoTrader(symbols=[], max_symbols_to_trade=LIVE_TRADING_CONFIG["max_symbols_to_trade"])
        await trader.main_loop()
    except Exception as e:
        console.log(f"\n[bold red]Bot Demo CRASHED dengan error tak terduga: {e}[/bold red]")
        if trader:
            await trader.log_event(f"--- DEMO BOT CRASHED: {e} ---")
            await notifier.send_message(f"💥 *Bot Demo CRASHED!*\nError: `{e}`")
    finally:
        if trader and trader.exchange:
            console.log("Menutup koneksi exchange demo...")
            await trader.exchange.close()
            console.log("[green]Koneksi demo berhasil ditutup.[/green]")

if __name__ == "__main__":
    log_restart_event()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.log("\n[yellow]Bot Demo dihentikan oleh pengguna (Ctrl+C).[/yellow]")
        asyncio.run(notifier.send_message("🛑 *Bot Demo Dihentikan Manual*"))
        with open(DEMO_EVENT_LOG_FILE, 'a') as f:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{now}] --- DEMO BOT STOPPED MANUALLY (Ctrl+C) ---\n")