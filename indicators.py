import pandas as pd
import pandas_ta as ta
import ccxt
from pathlib import Path
import ccxt.pro as ccxtpro_base # Import ccxt.pro base class for type checking
import pickle

from config import CONFIG

# =============================================================================
# DATA FETCHING & INDICATOR FUNCTIONS
# =============================================================================

# --- REVISI: Tambahkan direktori cache ---
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

async def fetch_binance_data(exchange, symbol, timeframe, limit, use_cache=True):
    """Mengambil data OHLCV dari Binance Futures menggunakan ccxt."""
    # --- REVISI: Implementasi Caching Kondisional ---
    # Buat nama file cache yang unik berdasarkan parameter
    safe_symbol = symbol.replace('/', '_')
    cache_file = CACHE_DIR / f"{safe_symbol}_{timeframe}_{limit}.pkl"

    # Jika cache diaktifkan dan file ada, muat dari disk
    if use_cache and cache_file.exists():
        print(f"Loading {symbol} data from cache (use_cache=True): {cache_file}")
        with open(cache_file, 'rb') as f:
            return pickle.load(f)

    if not exchange:
        print("Exchange is not initialized. Cannot fetch data.")
        return None
    try:
        # REVISI: Hapus log dari sini, akan ditangani oleh pemanggil (live_trader.py)
        # print(f"Fetching {limit} candles for {symbol} on {timeframe} timeframe...")
        
        # Get exchange rate limits, default to 1000 if not available
        limit_per_call = exchange.limits.get('ohlcv', {}).get('max', 1000)
        
        # Convert timeframe string to milliseconds for duration calculation
        timeframe_duration_in_ms = exchange.parse_timeframe(timeframe) * 1000

        # --- REVISI: Gunakan loop while untuk memastikan jumlah data yang diminta terpenuhi ---
        all_ohlcv = []
        
        # Start fetching from the past, moving towards the present
        # Calculate the starting timestamp
        since = exchange.milliseconds() - limit * timeframe_duration_in_ms

        while len(all_ohlcv) < limit:
            # Fetch a chunk of data
            # --- REVISI: Deteksi otomatis apakah exchange sinkron atau asinkron ---
            if isinstance(exchange, ccxtpro_base.Exchange):
                # Jika asinkron (dari live_trader), gunakan await
                ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit_per_call)
            else:
                # Jika sinkron (dari backtester), panggil langsung
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit_per_call)
            
            if not ohlcv:
                break # No more data available

            all_ohlcv.extend(ohlcv)
            # Update the 'since' timestamp to the timestamp of the last candle received + 1ms
            since = ohlcv[-1][0] + 1

        # Ensure we only have the number of candles requested
        all_ohlcv = all_ohlcv[-limit:]
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # --- REVISI: Jadikan timestamp tz-aware (UTC) untuk konsistensi ---
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
        df.set_index('timestamp', inplace=True)

        # --- REVISI: Simpan DataFrame ke cache hanya jika diaktifkan ---
        if use_cache:
            with open(cache_file, 'wb') as f:
                pickle.dump(df, f)
            print(f"Saved {symbol} data to cache: {cache_file}")
        return df
    except (ccxt.NetworkError, ccxt.ExchangeError, ccxt.BadSymbol) as e:
        print(f"Error fetching data from Binance for {symbol}: {e}")
        return None

def fetch_binance_data_sync(exchange, symbol, timeframe, limit, use_cache=True):
    """
    Versi SINKRON dari fetch_binance_data, khusus untuk backtester.
    Menghilangkan semua kebutuhan asyncio.run() di dalam backtester.
    """
    safe_symbol = symbol.replace('/', '_')
    cache_file = CACHE_DIR / f"{safe_symbol}_{timeframe}_{limit}.pkl"

    if use_cache and cache_file.exists():
        print(f"Loading {symbol} data from cache (use_cache=True): {cache_file}")
        with open(cache_file, 'rb') as f:
            return pickle.load(f), True # Kembalikan data dan flag 'from_cache'

    if not exchange:
        print("Exchange is not initialized. Cannot fetch data.")
        return None
    try:
        limit_per_call = exchange.limits.get('ohlcv', {}).get('max', 1000)
        timeframe_duration_in_ms = exchange.parse_timeframe(timeframe) * 1000
        all_ohlcv = []
        since = exchange.milliseconds() - limit * timeframe_duration_in_ms

        while len(all_ohlcv) < limit:
            # Panggil langsung karena ini adalah fungsi sinkron
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit_per_call)
            
            if not ohlcv:
                break

            all_ohlcv.extend(ohlcv)
            since = ohlcv[-1][0] + 1

        all_ohlcv = all_ohlcv[-limit:]
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
        df.set_index('timestamp', inplace=True)

        if use_cache:
            with open(cache_file, 'wb') as f:
                pickle.dump(df, f)
            print(f"Saved {symbol} data to cache: {cache_file}")
        return df, False # Kembalikan data dan flag 'from_cache'
    except (ccxt.NetworkError, ccxt.ExchangeError, ccxt.BadSymbol) as e:
        print(f"Error fetching data from Binance for {symbol}: {e}")
        return None, False

def get_trend(df, ema_period):
    """Menentukan tren berdasarkan harga penutupan terhadap EMA."""
    ema_col = f"EMA_{ema_period}"
    latest_price = df['close'].iloc[-1]
    latest_ema = df[ema_col].iloc[-1]
    return "UPTREND" if latest_price > latest_ema else "DOWNTREND"

def find_support_resistance(df, lookback):
    """Mencari swing high dan low terdekat sebagai support/resistance."""
    recent_data = df.iloc[-lookback:]
    return recent_data['high'].max(), recent_data['low'].min()

def calculate_fibonacci_extension(swing_high, swing_low, trend):
    """Menghitung level Fibonacci Extension."""
    diff = abs(swing_high - swing_low)
    levels = {}
    base = swing_high if trend == "UPTREND" else swing_low
    multiplier = 1 if trend == "UPTREND" else -1

    for level in CONFIG["fib_levels"]:
        levels[level] = base + (diff * level * multiplier)
    return list(levels.values())

def is_bullish(candle):
    """Memeriksa apakah candle bullish."""
    return candle['close'] > candle['open']

def is_bearish(candle):
    """Memeriksa apakah candle bearish."""
    return candle['close'] < candle['open']

def body_strength(candle):
    """Menghitung rasio body candle terhadap total range-nya."""
    total_range = candle['high'] - candle['low']
    if total_range == 0:
        return 0
    return abs(candle['close'] - candle['open']) / total_range

def rsi_signal(df, rsi_period, oversold, overbought):
    """Memberikan sinyal berdasarkan RSI crossover."""
    rsi_col = f"RSI_{rsi_period}"
    rsi_prev = df[rsi_col].iloc[-2]
    rsi_curr = df[rsi_col].iloc[-1]
    
    if rsi_prev < oversold and rsi_curr > oversold:
        return "LONG"
    if rsi_prev > overbought and rsi_curr < overbought:
        return "SHORT"
    return "NONE"

def stochastic_signal(df):
    """Memberikan sinyal berdasarkan Stochastic crossover."""
    k_prev = df['STOCHk_14_3_3'].iloc[-2]
    d_prev = df['STOCHd_14_3_3'].iloc[-2]
    k_curr = df['STOCHk_14_3_3'].iloc[-1]
    d_curr = df['STOCHd_14_3_3'].iloc[-1]
    
    if k_prev < d_prev and k_curr > d_curr:
        return "LONG"
    if k_prev > d_prev and k_curr < d_curr:
        return "SHORT"
    return "NONE"

def macd_slope(df):
    """Memberikan sinyal berdasarkan slope dari MACD histogram."""
    hist_prev = df['MACDh_12_26_9'].iloc[-2]
    hist_curr = df['MACDh_12_26_9'].iloc[-1]
    
    if hist_curr > hist_prev:
        return "LONG"
    if hist_curr < hist_prev:
        return "SHORT"
    return "NONE"

def atr_stoploss(entry, direction, df, atr_period, atr_mult):
    """Menghitung Stop Loss menggunakan ATR."""
    atr_col = f"ATRr_{atr_period}"
    atr_val = df[atr_col].iloc[-1]
    
    if direction == "LONG":
        return entry - (atr_val * atr_mult)
    return entry + (atr_val * atr_mult)

def breakout_check(candle, resistance, support, df, volume_lookback):
    """Memeriksa sinyal breakout dengan konfirmasi volume."""
    avg_volume = df['volume'].iloc[-volume_lookback-1:-1].mean()
    
    if candle['close'] > resistance and candle['volume'] > avg_volume:
        return "BREAKOUT_LONG"
    if candle['close'] < support and candle['volume'] > avg_volume:
        return "BREAKOUT_SHORT"
    return "NONE"

def calculate_indicators(df):
    """Menghitung semua indikator teknikal yang dibutuhkan dan menambahkannya ke DataFrame."""
    # Pastikan DataFrame tidak kosong untuk mencegah error pada pandas_ta
    if df is None or df.empty:
        return pd.DataFrame()

    # --- REVISI: Sentralisasi semua perhitungan indikator dasar ---
    df.ta.ema(length=CONFIG["ema_period"], append=True)
    df.ta.ema(length=9, append=True) # Untuk strategi lain
    df.ta.ema(length=200, append=True) # Untuk filter tren
    df.ta.rsi(length=CONFIG["rsi_period"], append=True)
    df.ta.stoch(append=True) # Menggunakan default pandas-ta (14, 3, 3)
    df.ta.macd(append=True) # Menggunakan default pandas-ta (12, 26, 9)
    df.ta.atr(length=CONFIG["atr_period"], append=True)
    # REVISI: Gunakan periode dari config untuk ADX agar konsisten dengan strategi
    df.ta.adx(length=CONFIG["atr_period"], append=True)
    df.ta.vwap(append=True)

    # --- FITUR BARU: Indikator untuk Strategi G1 (UT Bot / SuperTrend) ---
    # Menggunakan parameter dari video: ATR Period=1, Multiplier=1.0
    df.ta.supertrend(length=10, multiplier=3.0, append=True)

    # --- PERBAIKAN FINAL: Kembalikan perhitungan Volume SMA ke sini ---
    # Ini memastikan VOL_20 dihitung pada semua timeframe sejak awal.
    df.ta.sma(close=df['volume'], length=CONFIG["volume_lookback"], prefix="VOL", append=True)
    
    # --- PERBAIKAN KRUSIAL: Ganti nama kolom default pandas_ta ---
    # pandas_ta membuat kolom 'VOL_SMA_20', kita butuh 'VOL_20' agar konsisten.
    default_vol_col = f"VOL_SMA_{CONFIG['volume_lookback']}"
    target_vol_col = f"VOL_{CONFIG['volume_lookback']}"
    if default_vol_col in df.columns:
        df.rename(columns={default_vol_col: target_vol_col}, inplace=True)

    return df