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

from config import CONFIG, LEVERAGE_MAP, API_KEYS, TELEGRAM, LIVE_TRADING_CONFIG, EXECUTION, WHITELIST_ROTATION_CONFIG
from indicators import fetch_binance_data, calculate_indicators
from utils.common_utils import get_all_futures_symbols, get_dynamic_risk_params
from utils.data_preparer import prepare_data
from utils.telegram_notifier import TelegramNotifier
from strategies import STRATEGY_CONFIG, determine_entry_profile

console = Console(log_path=False) # Nonaktifkan logging duplikat dari Rich
notifier = TelegramNotifier(TELEGRAM['bot_token'], TELEGRAM['chat_id'])

# --- REVISI: Gunakan path absolut untuk file output agar tidak bergantung pada direktori kerja ---
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
STATE_FILE = OUTPUT_DIR / "live_positions.json"
EVENT_LOG_FILE = OUTPUT_DIR / "events.log"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def log_restart_event():
    """Menulis event restart secara sinkron saat bot dimulai."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(EVENT_LOG_FILE, 'a') as f:
        f.write(f"[{now}] --- BOT RESTARTED ---\n")

class LiveTrader:
    def __init__(self, symbols, max_symbols_to_trade):
        self.symbols = symbols
        self.max_symbols_to_trade = max_symbols_to_trade
        self.exchange = None
        self.historical_data = {symbol: pd.DataFrame() for symbol in symbols}
        self.is_fetching = {symbol: False for symbol in symbols} # Lock untuk mencegah fetching ganda
        # --- REVISI: Tambahkan manajemen state posisi aktif ---
        self.active_positions = {} # {symbol: {details}}
        # --- PERBAIKAN: Ubah open_limit_orders menjadi dict untuk menyimpan state ---
        self.open_limit_orders = {} # {symbol: {sl_price, tp_price, initial_sl}}
        self.load_positions_state()
        # --- REVISI: Gunakan antrian untuk memproses sinyal ---
        self.signal_queue = asyncio.Queue()
        # --- REVISI: Tambahkan state untuk rate limit saldo tidak cukup ---
        self.insufficient_balance_attempts = 0
        self.cooldown_until = None
        self.cooldown_duration_hours = 6
        # --- FITUR BARU: Lacak volume real-time untuk Circuit Breaker ---
        # --- FITUR BARU: State untuk Drawdown Circuit Breaker ---
        self.peak_balance = 0.0
        self.drawdown_cooldown_until = None
        self.drawdown_trigger_level = 0 # 0: first trigger, 1: second, etc.
        # ---------------------------------------------------------
        self.trade_volume_tracker = {} # {symbol: {'volume': float, 'last_update': datetime}}
        self.avg_5m_volume = {} # {symbol: float}
        # --- PILAR 2: State untuk Whitelist Dinamis ---
        self.dynamic_whitelist = set(self.symbols)
        # --- PILAR 3: State untuk Weekly Killswitch ---
        self.weekly_pnl_start_balance = None
        self.weekly_killswitch_pause_until = None
        self.last_weekly_check_day = None


    async def log_event(self, message):
        """Menulis event ke file log secara asinkron untuk menghindari pemblokiran."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{now}] {message}\n"
        async with aiofiles.open(EVENT_LOG_FILE, mode='a') as f:
            await f.write(log_message)

    async def initialize_exchange(self):
        """Inisialisasi koneksi exchange ke Binance Futures LIVE."""
        self.exchange = ccxtpro.binance({
            'apiKey': API_KEYS['live']['api_key'],
            'secret': API_KEYS['live']['api_secret'],
            # Konfigurasi untuk environment LIVE
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
            },
            # REVISI: Paksa ccxt untuk tidak menggunakan mode sandbox/testnet.
            'test': False,
            'enableRateLimit': True,
        })
        # --- PERBAIKAN DEFINITIF ---
        # Perintah eksplisit untuk menonaktifkan mode sandbox. Ini menimpa deteksi otomatis
        # dari ccxt dan memastikan koneksi selalu ke server LIVE.
        self.exchange.set_sandbox_mode(False)
        console.log("[bold green]Berhasil terhubung ke Binance Futures (LIVE).[/bold green]")
        await notifier.send_message("🚀 *Bot Trading LIVE Dimulai!*\nTerhubung ke Binance Futures.")

    # --- REVISI: Fungsi untuk menyimpan dan memuat state posisi ---
    def save_positions_state(self):
        """Menyimpan posisi aktif ke file JSON."""
        with open(STATE_FILE, 'w') as f:
            state_to_save = {
                'active_positions': {s: {'entryPrice': p['entryPrice'], 'positionAmt': p['positionAmt']} for s, p in self.active_positions.items()},
                'peak_balance': self.peak_balance,
                'drawdown_trigger_level': self.drawdown_trigger_level
            }
            json.dump(state_to_save, f, indent=4)

    def load_positions_state(self):
        """Memuat posisi aktif dari file JSON saat bot dimulai."""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                state_data = json.load(f)
                self.active_positions = state_data.get('active_positions', {})
                self.peak_balance = state_data.get('peak_balance', 0.0)
                self.drawdown_trigger_level = state_data.get('drawdown_trigger_level', 0)
            console.log(f"[yellow]State dimuat dari {STATE_FILE}. Posisi: {len(self.active_positions)}, Peak Balance: ${self.peak_balance:.2f}[/yellow]")

    async def prefetch_data(self):
        """Mengambil data historis awal untuk setiap simbol."""
        console.log("Mengambil data historis awal...")
        tasks = [self.fetch_initial_data(symbol) for symbol in self.symbols]
        results = await asyncio.gather(*tasks)

        # --- REVISI: Filter simbol yang tidak memiliki cukup data historis ---
        successful_symbols = [symbol for symbol, success in zip(self.symbols, results) if success]
        failed_symbols = [symbol for symbol, success in zip(self.symbols, results) if not success]

        if failed_symbols:
            console.log(f"[yellow]Menghapus simbol berikut karena riwayat data tidak mencukupi: {', '.join(failed_symbols)}[/yellow]")

        self.symbols = successful_symbols
        console.log(f"[green]Data historis awal berhasil dimuat untuk {len(self.symbols)} simbol yang valid.[/green]")

    async def fetch_initial_data(self, symbol):
        """Mengambil data awal untuk satu simbol dan memvalidasi jumlahnya."""
        try:
            # REVISI: Pindahkan log fetching ke sini untuk kejelasan
            console.log(f"Fetching initial data for [cyan]{symbol}[/cyan]...")
            required_candles = 650
            df_5m = await fetch_binance_data(self.exchange, symbol, '5m', limit=required_candles, use_cache=False)
            if df_5m is not None and not df_5m.empty:
                if len(df_5m) >= required_candles - 50: # Beri sedikit toleransi
                    self.historical_data[symbol] = df_5m.copy()
                    console.log(f"Data awal untuk [cyan]{symbol}[/cyan] dimuat ({len(df_5m)} candles).")
                    return True # Sukses
            console.log(f"[yellow]Gagal memuat data yang cukup untuk {symbol} (hanya dapat {len(df_5m) if df_5m is not None else 0} dari {required_candles}).[/yellow]")
            return False # Gagal
        except Exception as e:
            console.log(f"[red]Error saat prefetch data {symbol}: {e}[/red]")
            # REVISI: Tambahkan logging ke file untuk kegagalan prefetch.
            await self.log_event(f"PREFETCH_FAIL: {symbol} - {e}")
            return False # Gagal

    async def handle_kline(self, symbol, kline):
        """Callback yang dieksekusi saat ada data kline baru dari websocket."""
        timestamp, o, h, l, c, v = kline
        is_closed = True # Dari ccxt.pro, watch_ohlcv mengembalikan candle yang sudah ditutup

        if is_closed and not self.is_fetching[symbol]:
            self.is_fetching[symbol] = True
            try:
                console.log(f"Candle [cyan]{symbol}[/cyan] 5m ditutup pada [yellow]{pd.to_datetime(timestamp, unit='ms', utc=True)}[/yellow]. Harga: {c}")
                
                # 1. Update data historis
                new_candle_df = pd.DataFrame([{
                    'timestamp': pd.to_datetime(timestamp, unit='ms', utc=True),
                    'open': float(o), 'high': float(h), 'low': float(l), 'close': float(c), 'volume': float(v)
                }]).set_index('timestamp')
                
                # Gabungkan dan pastikan tidak ada duplikat
                self.historical_data[symbol] = pd.concat([self.historical_data[symbol], new_candle_df])
                self.historical_data[symbol] = self.historical_data[symbol][~self.historical_data[symbol].index.duplicated(keep='last')]
                # Jaga ukuran DataFrame agar tidak terlalu besar
                self.historical_data[symbol] = self.historical_data[symbol].tail(650)

                # --- FITUR BARU: Update rata-rata volume 5 menit ---
                # Digunakan oleh circuit breaker untuk mendeteksi anomali volume.
                # Ambil rata-rata volume dari 12 candle terakhir (1 jam).
                self.avg_5m_volume[symbol] = self.historical_data[symbol]['volume'].tail(12).mean()

                # 2. Masukkan data ke antrian untuk dianalisis
                await self.signal_queue.put({'symbol': symbol, 'data': self.historical_data[symbol].copy()})

            except Exception as e:
                console.log(f"[bold red]Error di handle_kline untuk {symbol}: {e}[/bold red]")
                # REVISI: Tambahkan logging ke file untuk kegagalan pemrosesan candle.
                await self.log_event(f"KLINE_HANDLE_FAIL: {symbol} - {e}")
            finally:
                self.is_fetching[symbol] = False

    # --- REVISI: Fungsi baru untuk memproses sinyal dari antrian ---
    async def signal_processor(self):
        """Loop untuk mengambil sinyal dari antrian dan menganalisisnya."""
        while True:
            try:
                task = await self.signal_queue.get()
                symbol, df_5m = task['symbol'], task['data']

                # --- Filter Batas Trade ---
                # Hitung total eksposur: posisi aktif + order limit yang sedang dibuka
                total_exposure = len(self.active_positions) + len(self.open_limit_orders)

                # Filter Baru: Batas trade harian
                today_str = datetime.now().strftime('%Y-%m-%d')
                trades_today = len([t for t in self.trades if t['Exit Time'].strftime('%Y-%m-%d') == today_str])
                if trades_today >= LIVE_TRADING_CONFIG.get('max_trades_per_day', 999):
                    console.log(f"[yellow]SKIP SIGNAL for {symbol}: Batas trade harian ({trades_today}) telah tercapai.[/yellow]")
                    continue

                if total_exposure >= LIVE_TRADING_CONFIG.get('max_active_positions_limit', 10): # Gunakan batas statis sementara
                    console.log(f"[yellow]SKIP SIGNAL for {symbol}: Batas total eksposur ({total_exposure}) telah tercapai.[/yellow]")
                    continue
                
                # --- PILAR 3: Cek Killswitch Pause ---
                if self.weekly_killswitch_pause_until and datetime.now() < self.weekly_killswitch_pause_until:
                    # Jika dalam masa pause, jangan proses sinyal
                    # console.log(f"[grey50]SKIP SIGNAL for {symbol}: Weekly Killswitch active.[/grey50]")
                    continue
                elif self.weekly_killswitch_pause_until and datetime.now() >= self.weekly_killswitch_pause_until:
                    self.weekly_killswitch_pause_until = None # Reset pause jika sudah selesai
                
                # --- PILAR 2: Filter berdasarkan Whitelist Dinamis ---
                if WHITELIST_ROTATION_CONFIG.get("enabled", False) and symbol not in self.dynamic_whitelist:
                    # console.log(f"[grey50]SKIP SIGNAL for {symbol}: Not in dynamic whitelist.[/grey50]")
                    continue

                # Pemeriksaan keamanan sekunder: jangan proses jika sudah ada posisi/order untuk simbol ini.
                # Meskipun sebagian besar sudah ditangani oleh cek total_exposure, ini mencegah race condition.
                if symbol in self.active_positions or symbol in self.open_limit_orders.keys():
                    continue

                # --- REVISI: Buat data MTA dari data 5m ---
                def resample_df(df, timeframe):
                    return df.resample(timeframe).agg({
                        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
                    }).dropna()

                df_15m = resample_df(df_5m, '15min')
                df_1h = resample_df(df_5m, 'h') # REVISI: Ganti '1H' menjadi 'h' untuk mengatasi FutureWarning

                if any(df.empty for df in [df_15m, df_1h]):
                    console.log(f"[yellow]Data resample untuk {symbol} tidak cukup, analisis dilewati.[/yellow]")
                    continue

                # --- PERBAIKAN KRUSIAL: Hitung indikator untuk setiap timeframe SEBELUM digabungkan ---
                # Ini memastikan data_preparer menerima semua kolom yang dibutuhkan.
                df_5m = calculate_indicators(df_5m)
                df_15m = calculate_indicators(df_15m)
                df_1h = calculate_indicators(df_1h)

                # Siapkan data gabungan
                base_data = prepare_data(df_5m, df_15m, df_1h)
                if base_data is None or base_data.empty:
                    console.log(f"[yellow]Gagal mempersiapkan data untuk {symbol}, analisis dilewati.[/yellow]")
                    continue

                # --- PERBAIKAN KONSISTENSI: Hapus baris dengan NaN sebelum analisis ---
                # Ini menyelaraskan logika dengan backtester dan mencegah error dari data warmup.
                base_data_cleaned = base_data.dropna()
                if base_data_cleaned.empty: continue
                latest_candle = base_data_cleaned.iloc[-1]

                # --- REVISI: Implementasi Weighted Consensus Filter ---
                long_score = 0.0
                short_score = 0.0
                consensus_contributors = [] # Menyimpan {'strategy': str, 'direction': str, 'params': dict}

                # 1. Kumpulkan suara dari setiap strategi
                for strategy_name, config in STRATEGY_CONFIG.items():
                    signal_function = config["function"]
                    weight = config["weight"]
                    # Gunakan .copy() untuk memastikan setiap strategi mendapat data bersih
                    long_signals, short_signals, exit_params = signal_function(base_data_cleaned.copy(), symbol=symbol)
                    
                    if not long_signals.empty and long_signals.iloc[-1]:
                        long_score += weight
                        consensus_contributors.append({'strategy': strategy_name, 'direction': 'LONG', 'params': exit_params})
                    elif not short_signals.empty and short_signals.iloc[-1]:
                        short_score += weight
                        consensus_contributors.append({'strategy': strategy_name, 'direction': 'SHORT', 'params': exit_params})

                # 2. Tentukan sinyal final berdasarkan skor konsensus
                # --- REVISI FINAL: Logika ambang batas hybrid yang cerdas ---
                num_strategies = len(STRATEGY_CONFIG)
                if num_strategies == 1:
                    # Jika hanya 1 strategi, cukup sinyal itu sendiri. Ambil bobotnya sebagai ambang batas.
                    required_score = next(iter(c['weight'] for c in STRATEGY_CONFIG.values())) * 0.99
                elif num_strategies == 2:
                    # Jika 2 strategi, cukup salah satu yang setuju. Ambil bobot TERENDAH sebagai ambang batas.
                    required_score = min(c['weight'] for c in STRATEGY_CONFIG.values()) * 0.99
                else: # Untuk 3 atau lebih strategi
                    # Gunakan rasio dinamis untuk skalabilitas.
                    total_possible_score = sum(c['weight'] for c in STRATEGY_CONFIG.values())
                    consensus_ratio = LIVE_TRADING_CONFIG.get('consensus_ratio', 0.55)
                    required_score = total_possible_score * consensus_ratio

                final_signal = None
                if long_score >= required_score:
                    final_signal = 'LONG'
                elif short_score >= required_score:
                    final_signal = 'SHORT'

                # 3. Jika ada konsensus, lanjutkan eksekusi
                if final_signal:
                    # Ambil parameter dari strategi PERTAMA yang berkontribusi pada konsensus
                    primary_contributor = next(c for c in consensus_contributors if c['direction'] == final_signal)
                    strategy_name = primary_contributor['strategy']
                    exit_params = primary_contributor['params']
                    
                    # Dapatkan nama semua strategi yang berkontribusi
                    contributing_strats = [c['strategy'] for c in consensus_contributors if c['direction'] == final_signal]
                    consensus_details = f"({len(contributing_strats)}/{len(STRATEGY_CONFIG)}: {', '.join(contributing_strats)})"

                    # --- Hitung parameter trade di sini untuk logging & notifikasi terpusat ---
                    signal_price = latest_candle['close']
                    atr_val = latest_candle[f"ATRr_{CONFIG['atr_period']}"]
                    
                    # --- PERBAIKAN: Tentukan profil entry dinamis ---
                    # Gunakan data yang sudah bersih untuk analisis profil entry
                    base_data_cleaned['prev_MACDh_12_26_9'] = base_data_cleaned['MACDh_12_26_9'].shift(1)
                    latest_candle_with_prev = base_data_cleaned.iloc[-1]
                    entry_profile = determine_entry_profile(latest_candle_with_prev)

                    # Ambil parameter dari profil yang terdeteksi
                    limit_offset_pct = entry_profile['offset_pct']
                    risk_for_this_trade = entry_profile['risk_pct']
                    entry_order_type = entry_profile['order_type']
                    
                    limit_price_float = signal_price * (1 - limit_offset_pct) if final_signal == 'LONG' else signal_price * (1 + limit_offset_pct)

                    sl_multiplier = exit_params.get('sl_multiplier', 1.5)
                    rr_ratio = exit_params.get('rr_ratio', 1.5)

                    # PERBAIKAN: Gunakan .iloc untuk konsistensi dan praktik terbaik
                    if isinstance(sl_multiplier, (pd.Series, np.ndarray)): sl_multiplier = sl_multiplier.iloc[-1]
                    if isinstance(rr_ratio, (pd.Series, np.ndarray)): rr_ratio = rr_ratio.iloc[-1]

                    stop_loss_dist = atr_val * sl_multiplier

                    # --- PERBAIKAN: Jangan hitung harga absolut SL/TP di sini ---
                    # Kita hanya akan log harga entry yang ditargetkan. SL/TP akan dihitung setelah fill.
                    limit_price_str = self.exchange.price_to_precision(symbol, limit_price_float)
                    leverage = LEVERAGE_MAP.get(symbol, LEVERAGE_MAP.get("DEFAULT", 10))

                    log_msg = f"SIGNAL_CONSENSUS ({entry_profile['profile']}): {final_signal} {symbol} {consensus_details} | Target Entry:{limit_price_str}"
                    console.log(f"[bold green]KONSENSUS SINYAL DITEMUKAN![/bold green] {log_msg}")
                    await self.log_event(log_msg)
                    
                    notif_msg = (f"🔔 *Sinyal Konsensus ({entry_profile['profile']}): {final_signal} {symbol}*\n{consensus_details}\n\n"
                                 f"Target Entry: `{limit_price_str}`\nLeverage: `{leverage}x`")
                    await notifier.send_message(notif_msg)
                    await self.execute_trade_logic(symbol, final_signal, latest_candle, exit_params, strategy_name, limit_price_float, stop_loss_dist, rr_ratio, risk_for_this_trade, entry_order_type)

            except KeyError as e:
                console.log(f"[bold red]Error KeyError di signal_processor untuk {symbol}: Kolom {e} tidak ditemukan. Periksa 'prepare_data' dan 'strategies'.[/bold red]")
            except Exception as e:
                console.log(f"[bold red]Error di signal_processor: {e}[/bold red]")
                # REVISI: Tambahkan logging ke file untuk kegagalan pemrosesan sinyal.
                # --- PERBAIKAN: Tambahkan notifikasi jika IP diblokir ---
                if "418" in str(e) and "banned" in str(e):
                    await notifier.send_message(f"🚨 *IP DIBLOKIR (LIVE)!* 🚨\nBot tidak dapat melanjutkan. Harap ganti IP atau tunggu hingga blokir dicabut.\nError: `{str(e)}`")
                await self.log_event(f"SIGNAL_PROCESSOR_FAIL: {e}")
            finally:
                self.signal_queue.task_done()

    async def execute_trade_logic(self, symbol, direction, candle, exit_params, strategy_name, limit_price_float, stop_loss_dist, rr_ratio, risk_for_this_trade, entry_order_type):
        """Menghitung parameter dan menempatkan order di bursa."""
        # --- FITUR BARU: Cek Drawdown Circuit Breaker ---
        if self.drawdown_cooldown_until and datetime.now() < self.drawdown_cooldown_until:
            # Jika dalam masa cooldown drawdown, jangan lakukan apa-apa.
            return

        # --- REVISI: Cek status cooldown sebelum eksekusi ---
        if self.cooldown_until and datetime.now() < self.cooldown_until:
            # Jika dalam masa cooldown, jangan lakukan apa-apa. Logging sudah dilakukan di signal_processor.
            return
        elif self.cooldown_until and datetime.now() >= self.cooldown_until:
            # Jika masa cooldown sudah berakhir, reset state.
            log_msg = "COOLDOWN_ENDED: Mode cooldown saldo tidak cukup telah berakhir. Percobaan eksekusi diaktifkan kembali."
            console.log(f"[green]{log_msg}[/green]")
            await self.log_event(log_msg)
            await notifier.send_message("✅ *Cooldown Berakhir*\nPercobaan eksekusi trade diaktifkan kembali.")
            self.cooldown_until = None
            self.insufficient_balance_attempts = 0

        try:
            # 1. Ambil Balance Akun menggunakan metode standar ccxt yang terbukti stabil.
            # Ini menyelaraskan logika dengan live_trader_monitor.py yang berfungsi.
            balance_info = await self.exchange.fetch_balance()
            if 'USDT' not in balance_info:
                raise ValueError(f"Respons saldo tidak valid atau tidak mengandung USDT. Diterima: {str(balance_info)[:200]}")
            free_balance = balance_info['USDT']['free']
            total_balance = balance_info['USDT']['total']
            used_margin = balance_info['USDT']['used']

            # 2. Hitung Parameter Trade
            # Harga sudah dihitung di signal_processor, kita tinggal gunakan
            signal_price = candle['close'] # Harga saat sinyal terdeteksi
            
            # Gunakan risiko yang sudah disesuaikan dari profil entry
            current_risk_per_trade = risk_for_this_trade

            if free_balance < 5: # REVISI: Turunkan minimal balance ke $5
                # REVISI: Tambahkan logging dan notifikasi untuk kegagalan ini.
                log_msg = f"EXECUTION_SKIPPED: {direction} {symbol} - Saldo tidak cukup (Free: ${free_balance:.2f})."
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                await notifier.send_message(f"⚠️ *Trade Dilewati* untuk {symbol}\nAlasan: Saldo tidak cukup.")

                # --- REVISI: Logika Rate Limit ---
                self.insufficient_balance_attempts += 1
                if self.insufficient_balance_attempts >= 2:
                    self.cooldown_until = datetime.now() + pd.Timedelta(hours=self.cooldown_duration_hours)
                    cooldown_end_str = self.cooldown_until.strftime('%Y-%m-%d %H:%M:%S')
                    log_msg = (f"COOLDOWN_STARTED: Saldo tidak cukup terdeteksi {self.insufficient_balance_attempts} kali. "
                               f"Memasuki mode cooldown selama {self.cooldown_duration_hours} jam, berakhir pada {cooldown_end_str}.")
                    console.log(f"[bold red]{log_msg}[/bold red]")
                    await self.log_event(log_msg)
                    await notifier.send_message(f"🥶 *Mode Cooldown Aktif*\nBot tidak akan mencoba eksekusi trade selama {self.cooldown_duration_hours} jam karena saldo tidak cukup.")
                # ---------------------------------
                return

            stop_loss_pct = stop_loss_dist / limit_price_float
            risk_amount_usd = total_balance * current_risk_per_trade

            if stop_loss_pct == 0:
                # REVISI: Tambahkan logging untuk kegagalan ini.
                log_msg = f"EXECUTION_SKIPPED: {direction} {symbol} - Kalkulasi stop_loss_pct menghasilkan nol (kemungkinan harga SL = harga entry)."
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                # Tidak perlu notifikasi Telegram untuk error teknis ini.
                return

            risk_params = get_dynamic_risk_params(total_balance) # Tetap panggil untuk default leverage
            leverage = LEVERAGE_MAP.get(symbol, risk_params.get('default_leverage', 10))
            position_size_usd = risk_amount_usd / stop_loss_pct
            margin_for_this_trade = position_size_usd / leverage
            amount = position_size_usd / signal_price # Jumlah koin

            # --- REVISI: Validasi Minimum Notional ---
            # Dapatkan nilai minNotional dari market data yang sudah dimuat ccxt.
            market_info = self.exchange.markets.get(symbol, {})
            min_notional = market_info.get('limits', {}).get('cost', {}).get('min')

            if min_notional and position_size_usd < min_notional:
                log_msg = (f"EXECUTION_SKIPPED: {direction} {symbol} - Ukuran posisi terhitung (${position_size_usd:.2f}) "
                           f"di bawah minimum notional yang disyaratkan (${min_notional}).")
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                await notifier.send_message(f"⚠️ *Trade Dilewati* untuk {symbol}\nAlasan: Ukuran posisi terlalu kecil.")
                return # Hentikan eksekusi
            # --- Akhir Validasi Minimum Notional ---

            # --- REVISI: Pengecekan Margin Maksimum ---
            # Pastikan total margin yang akan digunakan tidak melebihi 80% dari total balance.
            max_margin_pct = LIVE_TRADING_CONFIG['max_margin_usage_pct']
            margin_limit_usd = total_balance * max_margin_pct
            projected_used_margin = used_margin + margin_for_this_trade

            if projected_used_margin > margin_limit_usd:
                log_msg = f"EXECUTION_SKIPPED: {direction} {symbol} - Proyeksi margin ({projected_used_margin:.2f} USD) akan melebihi batas ({margin_limit_usd:.2f} USD)."
                console.log(f"[yellow]{log_msg}[/yellow]")
                await self.log_event(log_msg)
                await notifier.send_message(f"⚠️ *Trade Dilewati* untuk {symbol}\nAlasan: Batas penggunaan margin akan terlampaui.")
                return # Hentikan eksekusi trade
            # --- Akhir Pengecekan Margin ---

            # Pembulatan sesuai aturan market
            amount = self.exchange.amount_to_precision(symbol, amount)
            limit_price_str = self.exchange.price_to_precision(symbol, limit_price_float)

            # 3. Eksekusi Order
            console.log(f"Mencoba menempatkan order untuk {symbol}...")
            
            # Set leverage
            # REVISI DEFINITIF: Gunakan set_leverage standar dengan header mock.
            await self.exchange.set_leverage(leverage, symbol)

            console.log(f"Leverage untuk {symbol} diatur ke {leverage}x.")

            # Buat parameter untuk order gabungan (entry, sl, tp)
            side = 'buy' if direction == 'LONG' else 'sell'
            
            # --- PERBAIKAN: Gunakan saklar untuk memilih strategi exit ---
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

            # --- PERBAIKAN: Gunakan tipe order yang dapat dikonfigurasi ---
            if entry_order_type == "market":
                # Untuk market order, kita tidak perlu harga limit
                order = await self.exchange.create_order(symbol, 'market', side, amount, None, params)
            else: # Default ke limit order
                order = await self.exchange.create_order(symbol, 'limit', side, amount, limit_price_str, params)

            # --- PERBAIKAN: Simpan state order (termasuk initial_sl) di open_limit_orders ---
            self.open_limit_orders[symbol] = {
                # --- PERBAIKAN: Simpan jarak SL & RR, bukan harga absolut ---
                'stop_loss_dist': stop_loss_dist,
                'rr_ratio': rr_ratio,
                'positionAmt': amount if side == 'buy' else -amount,
                'strategy': strategy_name,
            }

            console.log(f"[bold green]Order berhasil dibuat untuk {symbol}. ID: {order['id']}[/bold green]")
            await notifier.send_message(f"✅ *Order Ditempatkan* untuk {symbol}!\nID: `{order['id']}`")
            # REVISI: Tambahkan log untuk eksekusi yang sukses.
            await self.log_event(f"EXECUTION_SUCCESS: {direction} {symbol} - Order ID: {order['id']}")

        except Exception as e:
            console.log(f"[bold red]Error saat eksekusi trade {symbol}: {e}[/bold red]")
            # REVISI: Pastikan notifikasi dan log kegagalan selalu dikirim.
            # --- PERBAIKAN: Tambahkan notifikasi jika IP diblokir ---
            if "418" in str(e) and "banned" in str(e):
                await notifier.send_message(f"🚨 *IP DIBLOKIR (LIVE)!* 🚨\nBot tidak dapat melanjutkan. Harap ganti IP atau tunggu hingga blokir dicabut.\nError: `{str(e)}`")
            await notifier.send_message(f"❌ *Error Eksekusi* pada {symbol}:\n`{e}`")
            # REVISI: Gunakan format log yang konsisten.
            await self.log_event(f"EXECUTION_FAIL: {direction} {symbol} - Error: {e}")

    async def dry_run_check(self):
        """
        Melakukan pemeriksaan 'kering' saat startup untuk memvalidasi koneksi API
        dan izin sebelum memulai loop utama.
        """
        console.log("[yellow]Memulai pemeriksaan Dry Run untuk validasi API...[/yellow]")
        try:
            # 1. Cek koneksi dan kemampuan mengambil saldo mock
            console.log("  - Memeriksa koneksi ke endpoint saldo (fetch_balance)...")
            # REVISI FINAL: Gunakan fetch_balance() yang terbukti stabil, sama seperti di monitor.
            balance_info = await self.exchange.fetch_balance()
            if 'USDT' not in balance_info:
                raise ValueError(f"Dry Run Gagal: Respons saldo tidak valid atau tidak mengandung USDT. Diterima: {str(balance_info)[:200]}")
            console.log("    [green]✅ Endpoint saldo OK.[/green]")

            # 2. Cek kemampuan mengatur leverage pada simbol sampel
            # REVISI FINAL: Hapus panggilan set_leverage() yang bermasalah.
            # Sebagai gantinya, kita akan mencoba membuat dan membatalkan order dummy
            # untuk memvalidasi izin 'Enable Futures' secara definitif.
            # REVISI: Hardcode simbol untuk Dry Run ke ETH/USDT untuk konsistensi.
            # Ini menghindari masalah minNotional yang berbeda-beda (misal: BTC butuh 100 USDT).
            sample_symbol = 'ETH/USDT'
            console.log(f"  - Memvalidasi izin 'Enable Futures' dengan order dummy pada {sample_symbol}...")

            # Dapatkan harga terakhir untuk membuat order yang realistis
            ticker = await self.exchange.fetch_ticker(sample_symbol)
            price = ticker['last']

            # Buat order limit POST_ONLY yang sangat kecil dan jauh dari harga pasar
            # agar tidak terisi, lalu langsung batalkan.
            # --- PERBAIKAN: Gunakan format simbol yang benar untuk mengakses market ---
            # self.symbols berisi format 'ETH/USDT:USDT' atau 'ETH/USDT'. Kita perlu menormalkannya
            # ke format ccxt standar ('ETH/USDT') untuk semua operasi.
            try:
                # Metode market() adalah cara paling andal untuk mendapatkan struktur market standar
                market_info = self.exchange.market(sample_symbol)
                sample_symbol_ccxt = market_info['symbol']
            except ccxtpro.BadSymbol: # Jika formatnya sudah 'ETH/USDT:USDT'
                sample_symbol_ccxt = sample_symbol.split(':')[0]
            market = self.exchange.markets[sample_symbol_ccxt]
            amount_precision = market['precision']['amount'] # Contoh: 0.001 untuk ETH

            # 2. Hitung nilai harga dan jumlah sebagai float.
            # Kita tempatkan order jauh dari harga pasar agar tidak terisi.
            dummy_price_float = price * 0.5 
            
            # --- PERBAIKAN FINAL: Hitung amount berdasarkan DUMMY PRICE, bukan market price ---
            # Binance memvalidasi nosional limit order menggunakan: limit_price * amount.
            # Jadi, kita harus menghitung 'required_amount' menggunakan 'dummy_price_float'
            # untuk memastikan nosional order dummy kita > 20 USDT.
            if dummy_price_float > 0 and amount_precision > 0:
                # Targetkan nosional $21 menggunakan harga dummy
                required_amount = 21.0 / dummy_price_float 
                dummy_amount_float = np.ceil(required_amount / amount_precision) * amount_precision
            else:
                dummy_amount_float = 0.0

            # 3. Setelah semua perhitungan selesai, format hasilnya ke string presisi yang benar.
            dummy_price_str = self.exchange.price_to_precision(sample_symbol_ccxt, dummy_price_float)
            dummy_amount_str = self.exchange.amount_to_precision(sample_symbol_ccxt, dummy_amount_float)

            # --- DEBUGGING PRINTOUT ---
            # Cetak semua parameter yang digunakan untuk membuat order dummy.
            debug_table = Table(title="[bold yellow]Dry Run Dummy Order Debug[/bold yellow]")
            debug_table.add_column("Parameter", style="cyan")
            debug_table.add_column("Value", style="white")
            debug_table.add_row("Sample Symbol", str(sample_symbol_ccxt))
            debug_table.add_row("Market Price (`price`)", f"{price:.8f}")
            debug_table.add_row("Dummy Limit Price (float)", f"{dummy_price_float:.8f}")
            debug_table.add_row("Calculated Amount (float)", f"{dummy_amount_float:.8f}")
            debug_table.add_row("--- Sent to API ---", "---")
            debug_table.add_row("Formatted Amount (str)", f"'{dummy_amount_str}'")
            debug_table.add_row("Formatted Price (str)", f"'{dummy_price_str}'")
            debug_table.add_row("--- Validation ---", "---")
            # REVISI: Gunakan harga limit untuk proyeksi nosional karena itu yang akan digunakan Binance untuk limit order
            # Namun, untuk validasi error -4164, Binance menggunakan Mark Price. Market Price adalah proxy yang cukup baik.
            projected_notional = float(dummy_price_str) * float(dummy_amount_str) if dummy_amount_str and dummy_price_str else 0.0
            debug_table.add_row("Projected Notional (Limit Price * Formatted Amount)", f"${projected_notional:.4f}")
            console.print(debug_table)

            # REVISI: Perbaiki parameter untuk Post-Only order.
            # 'POST' bukan nilai yang valid untuk 'timeInForce'. Parameter yang benar adalah 'postOnly': True.
            dummy_order = await self.exchange.create_order(sample_symbol_ccxt, 'limit', 'buy', dummy_amount_str, dummy_price_str, {'postOnly': True})
            await self.exchange.cancel_order(dummy_order['id'], sample_symbol_ccxt)

            console.log("    [green]✅ Izin 'Enable Futures' OK.[/green]")

            console.log("[bold green]✅ Dry Run berhasil. Semua pemeriksaan API lolos.[/bold green]")
            return True
        except Exception as e:
            console.log("[bold red]❌ Dry Run GAGAL.[/bold red]")
            # REVISI: Tampilkan error dengan format yang lebih baik untuk dibaca
            console.print(f"  Error: {e}")
            console.log("[bold yellow]Hint: Pastikan API Key Anda memiliki izin 'Enable Futures', 'Read Info', dan IP Anda sudah di-whitelist untuk akun live.[/bold yellow]")
            # REVISI: Tambahkan logging ke events.log saat dry run gagal.
            await self.log_event(f"DRY_RUN_FAIL: {e}")
            return False

    # --- REVISI: Ganti nama dan fungsionalitas menjadi position_manager ---
    async def position_manager(self):
        """Secara periodik memeriksa dan mengelola posisi/order aktif."""
        while True:
            try:
                # 1. Dapatkan update order real-time
                orders = await self.exchange.watch_orders()
                for order in orders:
                    status = order.get('status')
                    symbol = order.get('symbol')
                    symbol_ccxt = symbol.replace('USDT', '/USDT')

                    if status == 'closed': # 'closed' berarti terisi (filled)
                        # Cek apakah ini order entry atau SL/TP
                        if order['type'] in ['limit', 'market'] and symbol_ccxt not in self.active_positions:
                            # Ini adalah order entry yang terisi
                            # Ambil state kustom yang kita simpan
                            custom_state = self.open_limit_orders.pop(symbol_ccxt, {})
                            if not custom_state:
                                # Jika tidak ada state, mungkin ini posisi manual, abaikan.
                                continue

                            # REVISI DEFINITIF: Gunakan metode standar 'fetch_position'.
                            position_info = await self.exchange.fetch_position(symbol)

                            # --- PERBAIKAN: Gabungkan info dari bursa dengan state kustom kita ---
                            final_position_details = position_info['info']
                            final_position_details.update(custom_state) # Tambahkan sl_price, tp_price, initial_sl, dll.

                            # --- PERBAIKAN KRUSIAL: Hitung SL/TP dari harga entry riil ---
                            entry_price = float(final_position_details['entryPrice'])
                            stop_loss_dist = final_position_details['stop_loss_dist']
                            rr_ratio = final_position_details['rr_ratio']
                            direction = "LONG" if float(final_position_details['positionAmt']) > 0 else "SHORT"
                            final_position_details['sl_price'] = entry_price - stop_loss_dist if direction == "LONG" else entry_price + stop_loss_dist
                            final_position_details['initial_sl'] = final_position_details['sl_price']
                            final_position_details['tp_price'] = entry_price + (stop_loss_dist * rr_ratio) if direction == "LONG" else entry_price - (stop_loss_dist * rr_ratio)

                            self.active_positions[symbol_ccxt] = final_position_details
                            # --- FITUR BARU: Inisialisasi Multi-Level TP untuk Live ---
                            # Panggil fungsi baru untuk menghitung dan menyimpan target TP parsial
                            self.initialize_partial_tp_targets(symbol_ccxt)

                            self.save_positions_state()
                            filled_price = order.get('average', order.get('price'))
                            msg = f"✅ *Posisi Dibuka* untuk {symbol} @ `{filled_price}`"
                            console.log(f"[green]{msg}[/green]")
                            await notifier.send_message(msg)
                            await self.log_event(f"ENTRY_FILLED: Posisi {symbol} dibuka @ {filled_price}")
                        else:
                            # Ini adalah order SL/TP yang terisi, posisi ditutup
                            # Hapus dari open_limit_orders jika ada (kasus langka)
                            if symbol_ccxt in self.open_limit_orders.keys():
                                self.open_limit_orders.remove(symbol_ccxt)

                            if symbol_ccxt in self.active_positions:
                                del self.active_positions[symbol_ccxt]
                                self.save_positions_state()
                            filled_price = order.get('average', order.get('price'))
                            msg = f"🔴 *Posisi Ditutup* untuk {symbol} @ `{filled_price}`"
                            console.log(f"[magenta]{msg}[/magenta]")
                            await notifier.send_message(msg)
                            await self.log_event(f"EXIT_FILLED: Posisi {symbol} ditutup @ {filled_price}")

                    elif status in ['canceled', 'expired']:
                        # Hapus dari open_limit_orders jika dibatalkan/kedaluwarsa
                        if symbol_ccxt in self.open_limit_orders.keys():
                            self.open_limit_orders.remove(symbol_ccxt)

                        msg = f"ℹ️ *Order Dibatalkan/Kedaluwarsa* untuk {symbol}"
                        console.log(f"[yellow]{msg}[/yellow]")
                        await notifier.send_message(msg)
                        await self.log_event(f"ORDER_CANCEL: Order untuk {symbol} dibatalkan/kedaluwarsa.")

            except asyncio.CancelledError:
                raise # Pastikan pembatalan bisa menghentikan loop
            except Exception as e:
                console.log(f"[red]Error pada position_manager: {e}[/red]")
                # REVISI: Tambahkan logging ke file untuk kegagalan position manager.
                await self.log_event(f"POSITION_MANAGER_FAIL: {e}")
                if isinstance(e, ccxtpro.AuthenticationError) and "-2015" in str(e):
                    console.log("[bold yellow]Hint: Error -2015 biasanya berarti API Key tidak memiliki izin 'Enable Futures' atau IP Anda tidak di-whitelist. Silakan periksa pengaturan API Key di Binance.[/bold yellow]")
                if "418" in str(e) and "banned" in str(e):
                    await notifier.send_message(f"🚨 *IP DIBLOKIR (LIVE)!* 🚨\nBot tidak dapat melanjutkan. Harap ganti IP atau tunggu hingga blokir dicabut.\nError: `{str(e)}`")
                if isinstance(e, ccxtpro.NotSupported):
                    break
                await asyncio.sleep(10) # Tunggu sebelum mencoba lagi

    # --- FITUR BARU: Drawdown Circuit Breaker ---
    async def drawdown_circuit_breaker_check(self):
        """Memeriksa drawdown akun secara periodik dan mengaktifkan cooldown jika perlu."""
        while True:
            await asyncio.sleep(60) # Periksa setiap menit
            cb_config = LIVE_TRADING_CONFIG.get("drawdown_circuit_breaker", {})
            if not cb_config.get("enabled", False):
                continue

            # If in cooldown, do nothing
            if self.drawdown_cooldown_until and datetime.now() < self.drawdown_cooldown_until:
                continue

            try:
                balance_info = await self.exchange.fetch_balance()
                current_balance = balance_info.get('USDT', {}).get('total', 0)

                # PERBAIKAN: Update peak balance setiap kali balance saat ini lebih tinggi.
                # Ini akan "mengunci" profit dan membuat drawdown lebih sensitif.
                if current_balance > self.peak_balance:
                    self.peak_balance = current_balance
                
                # Cek drawdown
                drawdown_pct = (self.peak_balance - current_balance) / self.peak_balance if self.peak_balance > 0 else 0
                if drawdown_pct > cb_config.get("trigger_pct", 0.10):
                    cooldown_levels = cb_config.get("cooldown_hours", [2, 6, 24])
                    cooldown_hours = cooldown_levels[min(self.drawdown_trigger_level, len(cooldown_levels) - 1)]
                    self.drawdown_cooldown_until = datetime.now() + pd.Timedelta(hours=cooldown_hours)
                    msg = f"🚨 *DRAWDOWN CIRCUIT BREAKER (Level {self.drawdown_trigger_level + 1}) TERPICU!* 🚨\nDrawdown mencapai *{drawdown_pct:.2%}*. Semua trading dihentikan selama *{cooldown_hours} jam*."
                    await self.log_event(msg.replace("*", ""))
                    await notifier.send_message(msg)
                    # PERBAIKAN KRUSIAL: Reset peak balance ke balance saat ini untuk siklus berikutnya.
                    self.drawdown_trigger_level += 1
                    self.save_positions_state() # Save the new state
            except Exception as e:
                console.log(f"[red]Error di drawdown_circuit_breaker_check: {e}[/red]")
    
    # --- PILAR 3: WEEKLY PERFORMANCE KILLSWITCH ---
    async def weekly_performance_killswitch(self):
        """
        Memeriksa PnL mingguan. Jika kerugian melebihi ambang batas, hentikan trading sementara.
        """
        ks_config = LIVE_TRADING_CONFIG.get("weekly_killswitch", {})
        if not ks_config.get("enabled", False):
            console.log("[yellow]Weekly Performance Killswitch dinonaktifkan.[/yellow]")
            return

        while True:
            await asyncio.sleep(3600) # Periksa setiap jam
            now = datetime.now()
            current_day_of_week = now.weekday() # Senin = 0, Minggu = 6

            # Reset pada hari Senin
            if current_day_of_week == 0 and self.last_weekly_check_day != 0:
                try:
                    balance_info = await self.exchange.fetch_balance()
                    self.weekly_pnl_start_balance = balance_info.get('USDT', {}).get('total', 0)
                    self.weekly_killswitch_pause_until = None # Hapus pause saat minggu baru dimulai
                    msg = f"KILLSWITCH: Minggu baru dimulai. Balance awal PnL mingguan diatur ke ${self.weekly_pnl_start_balance:.2f}."
                    console.log(f"[cyan]{msg}[/cyan]")
                    await self.log_event(msg)
                    await notifier.send_message(f"🗓️ *Reset PnL Mingguan*\nBalance awal untuk minggu ini: `${self.weekly_pnl_start_balance:,.2f}` USDT. Killswitch direset.")
                except Exception as e:
                    console.log(f"[red]KILLSWITCH: Gagal mereset PnL mingguan: {e}[/red]")
            
            self.last_weekly_check_day = current_day_of_week

            # Jangan periksa jika belum ada balance awal atau sedang dalam masa pause
            if not self.weekly_pnl_start_balance or (self.weekly_killswitch_pause_until and now < self.weekly_killswitch_pause_until):
                continue

            try:
                balance_info = await self.exchange.fetch_balance()
                current_balance = balance_info.get('USDT', {}).get('total', 0)
                
                pnl_pct = (current_balance - self.weekly_pnl_start_balance) / self.weekly_pnl_start_balance

                if pnl_pct <= ks_config.get("max_weekly_loss_pct", -0.08):
                    pause_hours = ks_config.get("pause_duration_hours", 72)
                    self.weekly_killswitch_pause_until = now + pd.Timedelta(hours=pause_hours)
                    
                    # Tutup semua posisi aktif
                    active_symbols_to_close = list(self.active_positions.keys())
                    for symbol in active_symbols_to_close:
                        await self.close_position_manually(symbol, "Weekly Killswitch Triggered")

                    msg = (f"🚨 *WEEKLY KILLSWITCH TERPICU!* 🚨\n"
                           f"Kerugian mingguan mencapai {pnl_pct:.2%}. "
                           f"Semua trading dihentikan selama {pause_hours} jam.")
                    
                    console.log(f"[bold red]{msg.replace('*', '')}[/bold red]")
                    await self.log_event(msg.replace('*', ''))
                    await notifier.send_message(msg)

            except Exception as e:
                console.log(f"[red]Error di weekly_performance_killswitch: {e}[/red]")

    # --- FITUR BARU: Logika untuk inisialisasi target TP parsial ---
    def initialize_partial_tp_targets(self, symbol):
        """Menghitung dan menyimpan target TP parsial untuk posisi yang baru dibuka."""
        pos_info = self.active_positions.get(symbol)
        if not pos_info or 'initial_sl' not in pos_info:
            return

        entry_price = float(pos_info['entryPrice'])
        initial_sl = float(pos_info['initial_sl'])
        direction = "LONG" if float(pos_info['positionAmt']) > 0 else "SHORT"
        risk_distance = abs(entry_price - initial_sl)

        pos_info['partial_tp_targets'] = []
        if risk_distance > 0:
            for rr_multiplier, fraction in EXECUTION.get('partial_tps', []):
                tp_price_target = entry_price + (risk_distance * rr_multiplier) if direction == 'LONG' else entry_price - (risk_distance * rr_multiplier)
                pos_info['partial_tp_targets'].append({
                    'rr': rr_multiplier,
                    'fraction': fraction,
                    'price': tp_price_target,
                    'hit': False
                })

    # --- FITUR BARU: Logika SL/TP berbasis penutupan candle ---
    async def check_manual_sl_tp(self):
        """Memeriksa posisi aktif terhadap data candle terbaru untuk SL/TP manual."""
        while True:
            await asyncio.sleep(5) # Periksa setiap 5 detik
            active_symbols = list(self.active_positions.keys())
            if not active_symbols:
                continue

            for symbol in active_symbols:
                try:
                    pos_info = self.active_positions.get(symbol)
                    if not pos_info or 'sl_price' not in pos_info or 'positionAmt' not in pos_info: continue

                    # Ambil candle terbaru yang sudah ditutup
                    latest_candle = self.historical_data.get(symbol, pd.DataFrame()).iloc[-1]
                    if latest_candle.empty: continue

                    high_price = latest_candle['high']
                    low_price = latest_candle['low']
                    sl_price = pos_info['sl_price']
                    direction = "LONG" if float(pos_info['positionAmt']) > 0 else "SHORT"

                    # 1. Cek Stop Loss
                    if direction == "LONG":
                        if low_price <= sl_price:
                            await self.close_position_manually(symbol, "Manual SL (Low)")
                            continue # Lanjut ke simbol berikutnya
                    elif direction == "SHORT":
                        if high_price >= sl_price:
                            await self.close_position_manually(symbol, "Manual SL (High)")
                            continue # Lanjut ke simbol berikutnya

                    # 2. Cek Take Profit Parsial
                    for tp_target in pos_info.get('partial_tp_targets', []):
                        if tp_target['hit']: continue

                        is_hit = (direction == 'LONG' and high_price >= tp_target['price']) or \
                                 (direction == 'SHORT' and low_price <= tp_target['price'])

                        if is_hit:
                            initial_amount = abs(float(pos_info.get('initialAmt', pos_info['positionAmt']))) # Gunakan initialAmt jika ada
                            amount_to_close = initial_amount * tp_target['fraction']
                            
                            # Pastikan amount_to_close valid
                            amount_to_close = float(self.exchange.amount_to_precision(symbol, amount_to_close))
                            current_pos_amount = abs(float(pos_info['positionAmt']))
                            
                            # Jangan tutup lebih dari yang tersisa
                            amount_to_close = min(amount_to_close, current_pos_amount)

                            if amount_to_close > 0:
                                await self.close_position_manually(symbol, f"Partial TP {tp_target['rr']}R", partial_amount=amount_to_close)
                            tp_target['hit'] = True

                except Exception as e:
                    console.log(f"[red]Error di check_manual_sl_tp untuk {symbol}: {e}[/red]")

    async def close_position_manually(self, symbol, exit_reason, partial_amount=None):
        """Helper untuk menutup posisi (penuh atau parsial) dengan market order."""
        pos_info = self.active_positions.get(symbol)
        if not pos_info: return
        
        try:
            direction = "LONG" if float(pos_info['positionAmt']) > 0 else "SHORT"
            amount_to_close = partial_amount if partial_amount is not None else abs(float(pos_info['positionAmt']))
            
            if amount_to_close <= 0: return

            log_msg = f"MANUAL_EXIT_TRIGGER: {exit_reason} untuk {symbol}."
            console.log(f"[bold magenta]{log_msg}[/bold magenta]")
            await self.log_event(log_msg)
            
            if direction == "LONG":
                await self.exchange.create_market_sell_order(symbol, amount_to_close)
            else: # SHORT
                await self.exchange.create_market_buy_order(symbol, amount_to_close)
        except Exception as e:
            console.log(f"[red]Error saat menutup posisi manual untuk {symbol}: {e}[/red]")
            await self.log_event(f"MANUAL_EXIT_FAIL: {symbol} - {e}")

    # --- FITUR BARU: Circuit Breaker untuk Volatilitas Ekstrem ---
    async def volatility_circuit_breaker(self):
        """
        Memantau harga mark secara real-time. Jika harga bergerak melewati SL 
        dengan persentase tertentu, segera tutup posisi untuk mencegah likuidasi.
        Ini adalah jaring pengaman terakhir.
        """
        while True:
            await asyncio.sleep(1) # Periksa setiap detik
            active_symbols = list(self.active_positions.keys())
            if not active_symbols:
                continue

            try:
                # Ambil semua ticker sekaligus untuk efisiensi
                tickers = await self.exchange.fetch_tickers(active_symbols)
                for symbol in active_symbols:
                    pos_info = self.active_positions.get(symbol)
                    ticker = tickers.get(symbol)
                    if not pos_info or not ticker or 'sl_price' not in pos_info: continue

                    mark_price = ticker['mark']
                    sl_price = pos_info['sl_price']
                    direction = "LONG" if float(pos_info['positionAmt']) > 0 else "SHORT"

                    # Tentukan ambang batas "darurat" (misal: 1.5x jarak SL awal)
                    # Ini berarti jika harga menembus SL lebih dari 50% jarak SL-nya, kita keluar.
                    cb_multiplier = LIVE_TRADING_CONFIG.get("circuit_breaker_multiplier", 1.5)
                    # PERBAIKAN: Gunakan initial_sl untuk ambang batas yang konsisten
                    sl_breach_threshold = abs(pos_info['entryPrice'] - pos_info['initial_sl']) * (cb_multiplier - 1.0)

                    price_breached = (direction == "LONG" and mark_price < (sl_price - sl_breach_threshold)) or \
                                     (direction == "SHORT" and mark_price > (sl_price + sl_breach_threshold))

                    if price_breached:
                        # --- PERBAIKAN: Tambahkan konfirmasi volume ---
                        current_realtime_volume = self.trade_volume_tracker.get(symbol, {}).get('volume', 0)
                        avg_volume = self.avg_5m_volume.get(symbol, 0)
                        # Picu hanya jika volume real-time saat ini sudah > 50% dari volume rata-rata 1 candle penuh
                        volume_confirmed = avg_volume > 0 and current_realtime_volume > (avg_volume * 0.5)

                        if volume_confirmed:
                            log_msg = f"CIRCUIT_BREAKER_TRIGGERED: Volatilitas ekstrem & volume tinggi pada {symbol}. Menutup posisi di {mark_price}."
                            console.log(f"[bold red]{log_msg}[/bold red]")
                            await self.log_event(log_msg)
                            await self.close_position_manually(symbol, "Circuit Breaker")
                        else:
                            # Harga menembus tapi volume rendah, kemungkinan glitch. Jangan panik.
                            pass

            except Exception as e:
                console.log(f"[red]Error di volatility_circuit_breaker: {e}[/red]")

    # --- FITUR BARU: Trailing Stop Loss Manager ---
    async def trailing_stop_manager(self):
        """
        Mengelola Trailing Stop Loss untuk posisi yang profit.
        Memperbarui level SL secara dinamis untuk mengunci profit.
        """
        trailing_config = EXECUTION.get("trailing", {})
        if not trailing_config.get("enabled", False):
            return # Jangan jalankan jika fitur dinonaktifkan

        while True:
            check_interval = trailing_config.get("check_interval_seconds", 3)
            await asyncio.sleep(check_interval) # Periksa sesuai interval di config
            active_symbols = list(self.active_positions.keys())
            if not active_symbols:
                continue

            try:
                tickers = await self.exchange.fetch_tickers(active_symbols)
                for symbol in active_symbols:
                    pos_info = self.active_positions.get(symbol)
                    ticker = tickers.get(symbol)
                    if not pos_info or not ticker or 'sl_price' not in pos_info: continue

                    mark_price = ticker['mark']
                    entry_price = pos_info['entryPrice']
                    initial_sl = pos_info['initial_sl'] # Kita butuh SL awal untuk kalkulasi RR
                    direction = "LONG" if float(pos_info['positionAmt']) > 0 else "SHORT"
                    
                    # Hitung RR saat ini
                    risk_distance = abs(entry_price - initial_sl)
                    if risk_distance == 0: continue
                    current_profit_distance = abs(mark_price - entry_price)
                    current_rr = current_profit_distance / risk_distance

                    trigger_rr = trailing_config.get("trigger_rr", 1.0)

                    # Jika trade sudah mencapai target untuk memulai trailing
                    if current_rr >= trigger_rr:
                        if not pos_info.get('trailing_sl_active', False):
                            pos_info['trailing_sl_active'] = True
                            log_msg = f"TRAILING_SL_ACTIVATED: {symbol} mencapai {current_rr:.2f}R. Trailing Stop Loss aktif."
                            console.log(f"[bold cyan]{log_msg}[/bold cyan]")
                            await self.log_event(log_msg)

                        # Hitung level Trailing SL yang baru
                        atr_val = self.historical_data[symbol].iloc[-1][f"ATRr_{CONFIG['atr_period']}"]
                        trail_dist = atr_val * trailing_config.get("distance_atr", 1.5)
                        
                        new_sl = mark_price - trail_dist if direction == "LONG" else mark_price + trail_dist
                        
                        # Hanya update jika SL baru lebih baik (mengunci lebih banyak profit)
                        if (direction == "LONG" and new_sl > pos_info['sl_price']) or \
                           (direction == "SHORT" and new_sl < pos_info['sl_price']):
                            pos_info['sl_price'] = new_sl
                            # Tidak perlu log setiap kali SL bergerak untuk menghindari spam

            except Exception as e:
                console.log(f"[red]Error di trailing_stop_manager: {e}[/red]")

    async def main_loop(self):
        """Loop utama untuk mendengarkan data kline dari semua simbol."""
        await self.initialize_exchange()

        # --- REVISI: Dapatkan balance awal dan posisi aktif saat startup ---
        initial_balance_info = await self.exchange.fetch_balance()
        initial_total_balance = initial_balance_info.get('USDT', {}).get('total', 0)

        # --- REVISI BARU: Cetak status awal ke log ---
        startup_log_msg = f"STARTUP_STATE: Balance: ${initial_total_balance:.2f}, Loaded Active Positions: {len(self.active_positions)}"
        console.log(f"[bold blue]{startup_log_msg}[/bold blue]")
        await self.log_event(startup_log_msg)

        # Tentukan parameter dinamis berdasarkan modal
        dynamic_params = get_dynamic_risk_params(initial_total_balance)
        self.max_symbols_to_trade = dynamic_params['max_active_positions'] * 10 # Pantau 10x dari maks posisi

        # --- REVISI: Dapatkan simbol secara dinamis ---
        all_symbols = await get_all_futures_symbols(self.exchange)
        self.symbols = all_symbols[:self.max_symbols_to_trade] # Gunakan batas dinamis
        console.log(f"Modal awal: ${initial_total_balance:.2f}. Menggunakan parameter risiko dinamis: {dynamic_params}")
        console.log(f"Memindai [bold]{len(self.symbols)}[/bold] simbol teratas (dari {len(all_symbols)} yang ditemukan) berdasarkan modal.")

        # --- REVISI: Inisialisasi ulang dictionary setelah simbol didapatkan ---
        # Ini untuk mencegah KeyError karena dictionary dibuat saat self.symbols masih kosong.
        self.historical_data = {} # Akan diisi oleh prefetch_data
        self.is_fetching = {symbol: False for symbol in self.symbols}
        # --------------------------------------------------------------------

        # --- REVISI: Hentikan bot jika tidak ada simbol yang bisa diproses ---
        if not self.symbols:
            console.log("[bold red]Tidak ada simbol yang ditemukan sesuai kriteria. Bot berhenti.[/bold red]")
            await notifier.send_message("❌ Bot Berhenti: Tidak ada simbol yang bisa diproses.")
            # REVISI: Tambahkan logging ke file saat tidak ada simbol yang valid.
            await self.log_event("NO_VALID_SYMBOLS: Bot berhenti karena tidak ada simbol yang memenuhi kriteria.")
            return # Keluar dari main_loop

        await self.prefetch_data() # Prefetch data untuk simbol yang sudah dipilih

        # --- REVISI: Jalankan Dry Run Check setelah prefetch ---
        if not await self.dry_run_check():
            console.log("[bold red]Pemeriksaan Dry Run gagal. Bot berhenti untuk mencegah error lebih lanjut.[/bold red]")
            # REVISI: Hapus notifikasi Telegram untuk kegagalan Dry Run sesuai permintaan.
            # await notifier.send_message("❌ *Bot LIVE Berhenti:* Gagal validasi API (Dry Run).")
            return # Hentikan eksekusi

        # --- REVISI: Setelah prefetch, perbarui dictionary is_fetching dengan simbol yang valid ---
        self.is_fetching = {symbol: False for symbol in self.symbols}

        # Buat tasks untuk setiap websocket kline
        kline_tasks = [self.watch_ohlcv_loop(symbol) for symbol in self.symbols]
        # Buat task untuk memproses sinyal dari antrian
        processor_task = self.signal_processor()
        # Buat task untuk memantau posisi dan order
        manager_task = self.position_manager()
        # --- FITUR BARU: Jalankan task untuk memantau volume trade real-time ---
        trade_watcher_tasks = [self.watch_trades_loop(symbol) for symbol in self.symbols]

        # Kumpulkan semua task yang akan dijalankan
        all_tasks = [*kline_tasks, *trade_watcher_tasks, processor_task, manager_task]
        
        # --- PERBAIKAN: Jalankan task exit canggih hanya jika diaktifkan ---
        if LIVE_TRADING_CONFIG.get("use_advanced_exit_logic", True):
            console.log("[bold cyan]Mode Exit Canggih Aktif:[/bold cyan] Menggunakan SL/TP manual, Circuit Breaker, dan Trailing Stop.")
            # Jalankan semua task untuk strategi exit canggih
            all_tasks.append(self.check_manual_sl_tp())
            all_tasks.append(self.volatility_circuit_breaker())
            all_tasks.append(self.trailing_stop_manager())
            # --- FITUR BARU: Jalankan Drawdown Circuit Breaker ---
            all_tasks.append(self.drawdown_circuit_breaker_check())
        
        # --- PILAR 2: Jalankan task untuk rotasi whitelist ---
        all_tasks.append(self.dynamic_whitelist_rotator())

        # Jalankan semua task yang sudah dikumpulkan
        await asyncio.gather(*all_tasks)

    async def watch_ohlcv_loop(self, symbol):
        """Loop tak terbatas untuk satu simbol, menangani koneksi ulang."""
        timeframe = '5m'
        while True:
            try:
                console.log(f"Memulai websocket untuk [cyan]{symbol}[/cyan] timeframe {timeframe}...")
                while True:
                    klines = await self.exchange.watch_ohlcv(symbol, timeframe, params={'type': 'future'})
                    for kline in klines:
                        # REVISI: Tambahkan penanganan CancelledError di level ini
                        # untuk memastikan loop internal bisa berhenti dengan bersih.
                        try:
                            await self.handle_kline(symbol, kline)
                        except asyncio.CancelledError:
                            raise # Propagate cancellation to stop the loop
            except (ccxtpro.NetworkError, ccxtpro.ExchangeError) as e:
                # REVISI: Tambahkan logging ke file untuk error koneksi websocket.
                log_msg = f"WEBSOCKET_ERROR: {symbol} - {e}. Reconnecting..."
                await self.log_event(log_msg)
                console.log(f"[bold red]Websocket error untuk {symbol}: {e}. Mencoba menghubungkan ulang dalam 30 detik...[/bold red]")
                await asyncio.sleep(30)

    # --- FITUR BARU: Pemantau Volume Trade Real-time ---
    async def watch_trades_loop(self, symbol):
        """Memantau stream trade publik untuk mengakumulasi volume secara real-time."""
        while True:
            try:
                console.log(f"Memulai websocket trade volume untuk [cyan]{symbol}[/cyan]...")
                while True:
                    trades = await self.exchange.watch_trades(symbol)
                    if not trades: continue

                    now = datetime.now()
                    current_minute = now.minute

                    # Inisialisasi atau reset tracker setiap 5 menit
                    if symbol not in self.trade_volume_tracker or (current_minute % 5 == 0 and (now - self.trade_volume_tracker[symbol]['last_update']).total_seconds() > 60):
                        self.trade_volume_tracker[symbol] = {'volume': 0.0, 'last_update': now}

                    # Akumulasi volume dari trade baru
                    for trade in trades:
                        self.trade_volume_tracker[symbol]['volume'] += trade['amount']
                    
                    self.trade_volume_tracker[symbol]['last_update'] = now

            except (ccxtpro.NetworkError, ccxtpro.ExchangeError) as e:
                log_msg = f"TRADE_WATCHER_ERROR: {symbol} - {e}. Reconnecting..."
                await self.log_event(log_msg)
                console.log(f"[bold red]Trade watcher error untuk {symbol}: {e}. Mencoba menghubungkan ulang dalam 30 detik...[/bold red]")
                await asyncio.sleep(30)
    
    # --- PILAR 2: DYNAMIC WEEKLY WHITELIST ROTATION ---
    async def dynamic_whitelist_rotator(self):
        """
        Secara periodik memperbarui daftar pantau simbol berdasarkan momentum volume dan harga.
        """
        if not WHITELIST_ROTATION_CONFIG.get("enabled", False):
            console.log("[yellow]Dynamic Whitelist Rotator dinonaktifkan.[/yellow]")
            return

        while True:
            try:
                console.log("[bold cyan]ROTATION ENGINE: Memulai pembaruan whitelist dinamis...[/bold cyan]")
                
                # 1. Dapatkan semua ticker futures
                tickers = await self.exchange.fetch_tickers()
                futures_tickers = {s: t for s, t in tickers.items() if '/USDT' in s and ':USDT' in s}

                # 2. Filter Top N Market Cap
                sorted_by_mc = sorted(futures_tickers.values(), key=lambda t: t.get('quoteVolume', 0) * t.get('last', 1), reverse=True)
                top_mc_symbols = {t['symbol'] for t in sorted_by_mc[:WHITELIST_ROTATION_CONFIG.get("exclude_top_market_cap", 10)]}

                scores = []
                # Ambil 200 simbol teratas berdasarkan volume untuk dianalisis
                top_volume_symbols = [t['symbol'] for t in sorted_by_mc[:200]]

                for symbol in top_volume_symbols:
                    if symbol in top_mc_symbols:
                        continue

                    # 3. Ambil data historis untuk kalkulasi skor
                    # Kita butuh data 30 hari + 7 hari = 37 hari
                    df_daily, _ = await asyncio.get_event_loop().run_in_executor(None, self.exchange.fetch_ohlcv, symbol, '1d', limit=37)
                    if df_daily is None or len(df_daily) < 37:
                        continue
                    
                    df = pd.DataFrame(df_daily, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    
                    # 4. Hitung Skor & Filter
                    volume_7d = df['volume'].tail(7).mean()
                    volume_30d_ma = df['volume'].rolling(30).mean().iloc[-1]
                    close_7d_gain = (df['close'].iloc[-1] / df['close'].iloc[-8] - 1) if len(df) > 7 else 0
                    
                    # Filter ATH Drawdown
                    ath_30_days = df['high'].tail(30).max()
                    drawdown_from_ath = (ath_30_days - df['close'].iloc[-1]) / ath_30_days
                    if drawdown_from_ath > WHITELIST_ROTATION_CONFIG.get("max_drawdown_from_ath_pct", 0.35):
                        continue

                    if volume_30d_ma > 0:
                        score = (volume_7d / volume_30d_ma) * (close_7d_gain + 1)
                        scores.append({'symbol': symbol, 'score': score})

                # 5. Rank dan pilih Top N
                sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
                new_whitelist = {item['symbol'] for item in sorted_scores[:WHITELIST_ROTATION_CONFIG.get("top_n_coins", 20)]}
                
                self.dynamic_whitelist = new_whitelist
                msg = f"ROTATION ENGINE: Whitelist diperbarui. {len(self.dynamic_whitelist)} koin aktif: {', '.join(list(self.dynamic_whitelist)[:5])}..."
                console.log(f"[bold green]{msg}[/bold green]")
                await self.log_event(msg)
                await notifier.send_message(f"🔄 *Whitelist Diperbarui*\n{len(self.dynamic_whitelist)} koin 'panas' baru telah dipilih untuk minggu ini.")

            except Exception as e:
                console.log(f"[red]Error di dynamic_whitelist_rotator: {e}[/red]")
            
            await asyncio.sleep(WHITELIST_ROTATION_CONFIG.get("update_interval_hours", 24*7) * 3600)

async def main():
    """Fungsi utama async untuk menjalankan bot dan menangani cleanup."""
    trader = None
    try:
        console.log("[bold blue]Memulai bot trading live...[/bold blue]")
        # --- REVISI: Inisialisasi dengan parameter ---
        # Batasi jumlah simbol yang dipantau. Nilai awal ini akan ditimpa oleh
        # logika dinamis berdasarkan modal saat main_loop() berjalan.
        trader = LiveTrader(symbols=[], max_symbols_to_trade=LIVE_TRADING_CONFIG["max_symbols_to_trade"])
        await trader.main_loop()
    except Exception as e:
        # Menangkap semua error tak terduga lainnya (crash)
        console.log(f"\n[bold red]Bot CRASHED dengan error tak terduga: {e}[/bold red]")
        if trader:
            await trader.log_event(f"--- BOT CRASHED: {e} ---")
            await notifier.send_message(f"💥 *Bot LIVE CRASHED!*\nError: `{e}`")
    finally:
        # Blok ini akan selalu dieksekusi untuk memastikan koneksi ditutup dengan aman
        if trader and trader.exchange:
            console.log("Menutup koneksi exchange...")
            await trader.exchange.close()
            console.log("[green]Koneksi berhasil ditutup.[/green]")

if __name__ == "__main__":
    log_restart_event()
    # REVISI: Tangani KeyboardInterrupt di level tertinggi untuk mencegah traceback error
    # saat pengguna menekan Ctrl+C.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Menangani penghentian manual (Ctrl+C) dengan bersih
        console.log("\n[yellow]Bot dihentikan oleh pengguna (Ctrl+C).[/yellow]")
        asyncio.run(notifier.send_message("🛑 *Bot LIVE Dihentikan Manual*"))
        # Menulis ke log secara sinkron saat keluar.
        with open(EVENT_LOG_FILE, 'a') as f:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{now}] --- BOT STOPPED MANUALLY (Ctrl+C) ---\n")