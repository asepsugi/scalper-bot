import pandas as pd
from datetime import time
import numpy as np
from config import CONFIG

"""
Module ini berisi semua fungsi logika sinyal untuk berbagai versi strategi.
Setiap fungsi menerima DataFrame yang sudah diproses dan mengembalikan
kondisi boolean untuk sinyal LONG dan SHORT.
"""

def signal_version_A3(df):
    """Simplified MTA RSI: 15m RSI cross is the trigger, 1H RSI is a bias."""
    exit_params = {
        'sl_multiplier': 1.2,
        'rr_ratio': CONFIG['risk_reward_ratio']
    }

    long_signal = (df['trend'] == 'UPTREND') & \
                  (df['rsi_15m'].shift(1) < 50) & (df['rsi_15m'] > 50) & \
                  (df['rsi_1h'] > 50)

    short_signal = (df['trend'] == 'DOWNTREND') & \
                   (df['rsi_15m'].shift(1) > 50) & (df['rsi_15m'] < 50) & \
                   (df['rsi_1h'] < 50)

    return long_signal, short_signal, exit_params

def signal_version_A4R(df):
    """Refined Dynamic SL/TP: Uses A3 entry logic, but with fixed ATR bug."""
    long_signal, short_signal, _ = signal_version_A3(df)
    
    # --- REVISI: Gunakan ROLLING MEDIAN untuk ATR agar lebih adaptif ---
    # Menghitung median ATR dari 100 candle terakhir untuk setiap titik waktu.
    # Ini membuat strategi lebih responsif terhadap perubahan volatilitas pasar.
    # .bfill() digunakan untuk mengisi nilai NaN di awal data.
    rolling_median_atr = df[f"ATRr_{CONFIG['atr_period']}"].rolling(window=100, min_periods=20).median().bfill()
    current_atr = df[f"ATRr_{CONFIG['atr_period']}"]
    
    # Gunakan np.where untuk logika dinamis berbasis kondisi
    # Kondisi: Jika ATR saat ini > 1.5x dari rolling median ATR, anggap volatilitas tinggi dan ketatkan SL/TP.
    sl_multiplier = np.where(current_atr > (1.5 * rolling_median_atr), 1.2 * 0.8, 1.2)
    rr_ratio = np.where(current_atr > (1.5 * rolling_median_atr), 2.4 * 0.8, 2.4)

    exit_params = {
        'sl_multiplier': sl_multiplier, # Ini sekarang menjadi Series, bukan satu nilai
        'rr_ratio': rr_ratio # Ini juga menjadi Series
    }
    return long_signal, short_signal, exit_params

def signal_version_B1(df):
    """
    REVISED Strategy B1: Smart Regime Filter.
    Adapts its entry logic based on market conditions (Trending, Ranging, or Volatile).
    """
    # --- LANGKAH 1: Tentukan Rezim Pasar ---
    adx = df[f"ADX_{CONFIG['atr_period']}"]
    atr_delta = df['ATR_delta'] # Indikator baru dari data_preparer

    # Kondisi Rezim
    is_trending = (adx > 23)
    is_ranging = (adx < 18)
    is_volatile = (atr_delta > 1.5) # Lonjakan volatilitas mendadak

    # --- LANGKAH 2: Definisikan Logika Sinyal untuk Setiap Rezim ---
    # Sinyal untuk Pasar Trending (mengikuti tren)
    long_trending_signal = (df['close'] > df['trend_ema_15m']) & (df['rsi_15m'] > 55)
    short_trending_signal = (df['close'] < df['trend_ema_15m']) & (df['rsi_15m'] < 45)

    # Sinyal untuk Pasar Ranging (kontrarian/reversal)
    long_ranging_signal = df['rsi_cross_long'] # Menggunakan RSI cross dari data_preparer
    short_ranging_signal = df['rsi_cross_short']

    # --- LANGKAH 3: Gabungkan Sinyal Berdasarkan Rezim Aktif ---
    # Logika:
    # - Jika pasar trending, gunakan sinyal trending.
    # - Jika pasar ranging, gunakan sinyal ranging.
    # - Jika pasar volatile, JANGAN trade (filter keamanan).
    # - Jika tidak ada kondisi di atas (pasar "normal"), gabungkan keduanya.
    
    long_signal = np.where(
        is_volatile, False, np.where(
            is_trending, long_trending_signal, np.where(
                is_ranging, long_ranging_signal, long_trending_signal | long_ranging_signal
            )
        )
    )
    
    short_signal = np.where(
        is_volatile, False, np.where(
            is_trending, short_trending_signal, np.where(
                is_ranging, short_ranging_signal, short_trending_signal | short_ranging_signal
            )
        )
    )

    # --- LANGKAH 4: Tentukan Parameter Exit ---
    # Parameter exit bisa tetap sederhana atau dibuat dinamis juga
    exit_params = {
        'sl_multiplier': 1.8,
        'rr_ratio': 1.6
    }

    # Konversi hasil np.where (array) kembali ke pandas Series
    return pd.Series(long_signal, index=df.index), pd.Series(short_signal, index=df.index), exit_params

def signal_version_C1(df):
    """
    EMA Pullback Rider: Identifies a strong trend and enters on a pullback to a short-term EMA.
    Designed to work well with limit order entries.
    """
    exit_params = {
        'sl_multiplier': 1.5,
        'rr_ratio': 1.8
    }

    # 1. Filter Tren Makro (Timeframe 1 Jam)
    # Tren dianggap kuat jika harga berada di atas EMA 200 pada timeframe 1 jam.
    long_macro_trend = (df['close'] > df['trend_ema_200_15m']) # Menggunakan 15m sebagai proxy yang lebih cepat
    short_macro_trend = (df['close'] < df['trend_ema_200_15m'])

    # 2. Filter Momentum (Timeframe 15 Menit)
    # Momentum dianggap kuat jika RSI 15m berada di zona bullish/bearish.
    long_momentum = (df['rsi_15m'] > 55)
    short_momentum = (df['rsi_15m'] < 45)

    # 3. Pemicu Entry (Pullback pada Timeframe 5 Menit)
    # Sinyal muncul ketika harga menyentuh EMA 9 dari atas (untuk long) atau dari bawah (untuk short).
    # Ini adalah sinyal pullback klasik.
    long_pullback = (df['low'] <= df['EMA_9']) & (df['close'] > df['EMA_9'])
    short_pullback = (df['high'] >= df['EMA_9']) & (df['close'] < df['EMA_9'])

    # 4. Filter Volatilitas (ATR)
    # Hanya trade jika pasar memiliki volatilitas yang cukup (ATR di atas persentil ke-30).
    # Ini menghindari pasar yang terlalu datar.
    atr_col = f"ATRr_{CONFIG['atr_period']}"
    atr_percentile_30 = df[atr_col].rolling(window=1440, min_periods=200).quantile(0.30).bfill()
    volatility_filter = (df[atr_col] > atr_percentile_30)

    # Gabungkan semua kondisi
    long_signal = long_macro_trend & long_momentum & long_pullback & volatility_filter
    short_signal = short_macro_trend & short_momentum & short_pullback & volatility_filter

    return long_signal, short_signal, exit_params

# --- REVISI: Konfigurasi Strategi Terpusat ---
# Menggabungkan peta strategi dan bobotnya di satu tempat untuk mempermudah pengelolaan.
STRATEGY_CONFIG = {
    "AdaptiveTrendRide(A3)": {
        "function": signal_version_A3,
        "weight": 1.0
    },
    "ReversalMomentumRider(A4R)": {
        "function": signal_version_A4R,
        "weight": 1.0
    },
    "SmartRegimeScalper(B1)": {
        "function": signal_version_B1,
        "weight": 1.0 
    },
    "EMAPullbackRider(C1)": {
        "function": signal_version_C1,
        "weight": 1.2 # Beri bobot sedikit lebih tinggi karena dirancang untuk sistem ini
    }
}