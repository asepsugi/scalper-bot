import pandas as pd
import pandas_ta as ta
import ccxt
from pathlib import Path
import ccxt.pro as ccxtpro_base # Import ccxt.pro base class for type checking
import pickle
import sys  # <-- Tambahkan import ini
import os   # <-- Tambahkan import ini
import numpy as np # <-- Tambahkan import ini
from datetime import datetime, timedelta # <-- Tambahkan import ini
import threading # <-- PERBAIKAN: Impor modul threading untuk lock
from scipy import stats # PERBAIKAN: Tambahkan import yang hilang untuk linear regression

from config import CONFIG, CACHE_CONFIG

# =============================================================================
# DATA FETCHING & INDICATOR FUNCTIONS
# =============================================================================

# --- PERBAIKAN: Buat lock global untuk melindungi akses ke sys.stdout ---
stdout_lock = threading.Lock()

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
                # Symbol & Data Focus: Tambah noise ke OHLC
                if 'ATRr_10' in df.columns:
                    atr = df['ATRr_10']
                    noise_magnitude = 0.0005 * atr
                    for col in ['open', 'high', 'low', 'close']:
                        noise = np.random.normal(0, noise_magnitude)
                        df[col] += noise
                    # Pastikan high > low
                    df['high'] = df[['high', 'low', 'open', 'close']].max(axis=1)
                    df['low'] = df[['high', 'low', 'open', 'close']].min(axis=1)
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

    # --- PERBAIKAN: Logika Cache dengan Kedaluwarsa dan Penanganan Error ---
    if use_cache and CACHE_CONFIG.get("enabled", True) and cache_file.exists():
        try:
            # Cek masa berlaku cache
            file_mod_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            expiration_hours = CACHE_CONFIG.get("expiration_hours", 24)
            if datetime.now() - file_mod_time > timedelta(hours=expiration_hours):
                print(f"Cache for {symbol} has expired. Fetching new data.")
            else:
                # Jika cache valid, coba muat
                print(f"Loading {symbol} data from cache: {cache_file}")
                with open(cache_file, 'rb') as f:
                    return pickle.load(f), True # Kembalikan data dan flag 'from_cache'
        except (pickle.UnpicklingError, EOFError) as e:
            # Jika file cache rusak, hapus dan lanjutkan untuk mengambil data baru
            print(f"Cache file for {symbol} is corrupted ({e}). Deleting and fetching new data.")
            try:
                os.remove(cache_file)
            except OSError as ose:
                print(f"Error deleting corrupted cache file {cache_file}: {ose}")
        except Exception as e:
            print(f"An unexpected error occurred with cache handling for {symbol}: {e}")

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
                # Symbol & Data Focus: Tambah noise ke OHLC
                if 'ATRr_10' in df.columns:
                    atr = df['ATRr_10']
                    noise_magnitude = 0.0005 * atr
                    for col in ['open', 'high', 'low', 'close']:
                        noise = np.random.normal(0, noise_magnitude)
                        df[col] += noise
                    df['high'] = df[['high', 'low', 'open', 'close']].max(axis=1)
                    df['low'] = df[['high', 'low', 'open', 'close']].min(axis=1)
                pickle.dump(df, f)
            print(f"Saved {symbol} data to cache: {cache_file}")
        return df, False # Kembalikan data dan flag 'from_cache'
    except (ccxt.NetworkError, ccxt.ExchangeError, ccxt.BadSymbol) as e:
        print(f"Error fetching data from Binance for {symbol}: {e}")
        return None, False

# =============================================================================
# ENHANCED INDICATOR CALCULATION
# =============================================================================

def calculate_indicators(df):
    """
    OPTIMIZED VERSION: Calculates all indicators needed for scalping.
    
    Changes from original:
    1. Fixed SuperTrend parameters (1,1) → (10,3.0) for 15m timeframe
    2. Faster ATR (14 → 10) for more responsive stops
    3. Added Bollinger Bands (critical for scalping)
    4. Added Keltner Channels (better than BB in trends)
    5. Added MFI (volume-weighted RSI)
    6. Added Williams %R (faster momentum)
    7. Added OBV (volume flow)
    8. Added Donchian Channels (true high/low)
    9. Removed Stochastic and MACD (unused)
    10. Added custom indicators (ATR percentile, LR angle)
    """
    
    if df is None or df.empty:
        print("DEBUG: calculate_indicators received empty or None DataFrame.")
        return pd.DataFrame()
    
    # --- PERBAIKAN: Gunakan lock untuk membuat pengalihan stdout menjadi thread-safe ---
    with stdout_lock:
        original_stdout = sys.stdout
        f = open(os.devnull, 'w')
        sys.stdout = f
        try:
            # =========================================================================
            # TREND INDICATORS
            # =========================================================================
            df.ta.ema(length=9, append=True)
            df.ta.ema(length=CONFIG["ema_period"], append=True)
            df.ta.ema(length=200, append=True)
            
            # =========================================================================
            # MOMENTUM INDICATORS
            # =========================================================================
            df.ta.rsi(length=CONFIG["rsi_period"], append=True)
            df.ta.willr(length=14, append=True)
            # --- PERBAIKAN: Tambahkan Stochastic dan MACD sesuai permintaan ---
            df.ta.stoch(k=14, d=3, smooth_k=3, append=True)
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            # ----------------------------------------------------------------
            df.ta.mfi(length=14, append=True)
            
            # =========================================================================
            # VOLATILITY INDICATORS
            # =========================================================================
            df.ta.atr(length=CONFIG["atr_period"], append=True)
            
            bbands = df.ta.bbands(length=20, std=2, append=True)
            if bbands is not None and not bbands.empty:
                rename_map = {f'{col}_2.0': col for col in ['BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'BBB_20_2.0', 'BBP_20_2.0'] if f'{col}_2.0' in df.columns}
                if rename_map:
                    df.rename(columns=rename_map, inplace=True)

            if 'BBU_20_2.0' not in df.columns:
                for col in ['BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'BBB_20_2.0', 'BBP_20_2.0']:
                    if col not in df.columns: df[col] = np.nan
            
            df.ta.kc(length=20, scalar=2.0, append=True)
            
            # =========================================================================
            # TREND STRENGTH
            # =========================================================================
            df.ta.adx(length=CONFIG["atr_period"], append=True)
            df.ta.supertrend(length=10, multiplier=3.0, append=True)
            
            # =========================================================================
            # VOLUME INDICATORS
            # =========================================================================
            df.ta.sma(close=df['volume'], length=CONFIG["volume_lookback"], prefix="VOL", append=True)
            df.ta.obv(append=True)
            
            default_vol_col = f"VOL_SMA_{CONFIG['volume_lookback']}"
            target_vol_col = f"VOL_{CONFIG['volume_lookback']}"
            if default_vol_col in df.columns:
                df.rename(columns={default_vol_col: target_vol_col}, inplace=True)
            
            # =========================================================================
            # CHANNELS & VWAP
            # =========================================================================
            df.ta.donchian(length=20, append=True)
            df.ta.vwap(append=True)

        finally:
            sys.stdout = original_stdout
            f.close()

    # --- Kalkulasi indikator kustom dilakukan di luar blok yang dibungkam ---
    # 1. ATR Percentile (for volatility regime detection)
    atr_col = 'ATRr_10'
    if atr_col in df.columns:
        df['atr_percentile'] = df[atr_col].rolling(288).rank(pct=True)
        df['atr_percentile'] = df['atr_percentile'].fillna(0.5)
    
    # 2. Linear Regression Angle (trend acceleration)
    df = add_linear_regression_angle(df, period=14)
    
    # 3. Volume Ratio (for better volume analysis)
    target_vol_col = f"VOL_{CONFIG['volume_lookback']}"
    if target_vol_col in df.columns:
        df['volume_ratio'] = df['volume'] / df[target_vol_col]
        df['volume_ratio'] = df['volume_ratio'].fillna(1.0)
    
    # 4. Bollinger Band Width Percentile (squeeze detector)
    if 'BBB_20_2.0' in df.columns:
        df['bb_width_pct'] = df['BBB_20_2.0'].rolling(100).rank(pct=True)
        df['bb_width_pct'] = df['bb_width_pct'].fillna(0.5)
        df['bb_squeeze'] = df['bb_width_pct'] < 0.2
    
    # 5. Price position in Bollinger Bands (0-1 scale)
    if all(col in df.columns for col in ['BBL_20_2.0', 'BBU_20_2.0']):
        bb_range = df['BBU_20_2.0'] - df['BBL_20_2.0']
        df['bb_position'] = (df['close'] - df['BBL_20_2.0']) / bb_range
        df['bb_position'] = df['bb_position'].clip(0, 1).fillna(0.5)
    
    # 6. RSI Divergence Detection (simple version)
    rsi_col_name = f"RSI_{CONFIG['rsi_period']}"
    if rsi_col_name in df.columns:
        price_hh = (df['close'] > df['close'].shift(10)) & (df['close'] > df['close'].rolling(10).max().shift(1))
        rsi_lh = (df[rsi_col_name] < df[rsi_col_name].shift(10)) & (df[rsi_col_name] < df[rsi_col_name].rolling(10).max().shift(1))
        df['rsi_bearish_div'] = price_hh & rsi_lh
        
        price_ll = (df['close'] < df['close'].shift(10)) & (df['close'] < df['close'].rolling(10).min().shift(1))
        rsi_hl = (df[rsi_col_name] > df[rsi_col_name].shift(10)) & (df[rsi_col_name] > df[rsi_col_name].rolling(10).min().shift(1))
        df['rsi_bullish_div'] = price_ll & rsi_hl
    
    # 7. MFI Divergence (similar to RSI)
    if 'MFI_14' in df.columns:
        price_hh = (df['close'] > df['close'].shift(10)) & (df['close'] > df['close'].rolling(10).max().shift(1))
        mfi_lh = (df['MFI_14'] < df['MFI_14'].shift(10)) & (df['MFI_14'] < df['MFI_14'].rolling(10).max().shift(1))
        df['mfi_bearish_div'] = price_hh & mfi_lh
        
        price_ll = (df['close'] < df['close'].shift(10)) & (df['close'] < df['close'].rolling(10).min().shift(1))
        mfi_hl = (df['MFI_14'] > df['MFI_14'].shift(10)) & (df['MFI_14'] > df['MFI_14'].rolling(10).min().shift(1))
        df['mfi_bullish_div'] = price_ll & mfi_hl
    
    return df


def add_linear_regression_angle(df, period=14):
    """
    Add linear regression angle as trend strength indicator.
    
    Angle interpretation:
    - Positive angle: Uptrend (higher = stronger)
    - Negative angle: Downtrend (lower = stronger)
    - Near zero: Sideways/ranging
    - Multiply by R² to weight by trend quality
    """
    def lr_angle(series):
        if len(series) < 2:
            return 0
        
        try:
            x = np.arange(len(series))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, series)
            
            # Convert slope to angle in degrees
            angle_deg = np.degrees(np.arctan(slope))
            
            # Weight by R-squared (trend quality)
            # R² close to 1 = strong linear trend
            # R² close to 0 = noisy, not linear
            weighted_angle = angle_deg * (r_value ** 2)
            
            return weighted_angle
        except:
            return 0
    
    df['LR_ANGLE'] = df['close'].rolling(period).apply(lr_angle, raw=False)
    df['LR_ANGLE'] = df['LR_ANGLE'].fillna(0)
    
    # Add trend classification based on angle
    df['lr_trend'] = 'NEUTRAL'
    df.loc[df['LR_ANGLE'] > 15, 'lr_trend'] = 'STRONG_UP'
    df.loc[df['LR_ANGLE'] > 5, 'lr_trend'] = 'UP'
    df.loc[df['LR_ANGLE'] < -15, 'lr_trend'] = 'STRONG_DOWN'
    df.loc[df['LR_ANGLE'] < -5, 'lr_trend'] = 'DOWN'
    
    return df

# =============================================================================
# INDICATOR SUMMARY FUNCTION (For Debugging)
# =============================================================================

def print_indicator_summary(df):
    """Prints summary of available indicators in DataFrame."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    
    table = Table(title="Available Indicators", show_header=True)
    table.add_column("Category", style="cyan")
    table.add_column("Indicators", style="white")
    
    indicators = {
        "Trend": [col for col in df.columns if any(x in col for x in ['EMA', 'SUPER', 'LR'])],
        "Momentum": [col for col in df.columns if any(x in col for x in ['RSI', 'MFI', 'WILLR', 'div'])],
        "Volatility": [col for col in df.columns if any(x in col for x in ['ATR', 'BB', 'KC'])],
        "Volume": [col for col in df.columns if any(x in col for x in ['VOL', 'OBV'])],
        "Channels": [col for col in df.columns if any(x in col for x in ['DC'])],
        "Custom": [col for col in df.columns if any(x in col for x in ['percentile', 'ratio', 'position', 'squeeze'])]
    }
    
    for category, cols in indicators.items():
        if cols:
            table.add_row(category, ", ".join(cols[:5]) + ("..." if len(cols) > 5 else ""))
    
    console.print(table)
    console.print(f"\nTotal indicators: {len(df.columns) - 6}")  # Exclude OHLCV + timestamp