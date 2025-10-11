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
    """Strategy based on the new configurable indicator checklist."""
    exit_params = {
        'sl_multiplier': 1.5 if CONFIG.get('strategy_b1_indicators', {}).get('atr_exit', False) else 1.2,
        'rr_ratio': 2.5 / 1.5 if CONFIG.get('strategy_b1_indicators', {}).get('atr_exit', False) else CONFIG['risk_reward_ratio']
    }

    cfg = CONFIG["strategy_b1_indicators"]
    
    # --- Build filter conditions based on config ---
    # 1. EMA Trend Filter
    long_ema_filter = (df['close'] > df['trend_ema_200_15m']) & (df['trend_ema_15m'] > df['trend_ema_200_15m']) if cfg['ema_trend'] else pd.Series(True, index=df.index)
    short_ema_filter = (df['close'] < df['trend_ema_200_15m']) & (df['trend_ema_15m'] < df['trend_ema_200_15m']) if cfg['ema_trend'] else pd.Series(True, index=df.index)

    # 2. RSI Confirmation
    long_rsi_filter = ((df['rsi_15m'].shift(1) < 45) & (df['rsi_15m'] > 45) & (df['rsi_1h'] > 50)) if cfg['rsi_confirm'] else pd.Series(True, index=df.index)
    short_rsi_filter = ((df['rsi_15m'].shift(1) > 55) & (df['rsi_15m'] < 55) & (df['rsi_1h'] < 50)) if cfg['rsi_confirm'] else pd.Series(True, index=df.index)

    # 3. ADX Filter
    adx_filter = (df[f"ADX_{CONFIG['atr_period']}"] > 15) if cfg['adx_filter'] else pd.Series(True, index=df.index)

    # 5. EMA9 Trigger
    long_ema9_trigger = (df['close'] > df['EMA_9']) if cfg['ema9_trigger'] else pd.Series(True, index=df.index)
    short_ema9_trigger = (df['close'] < df['EMA_9']) if cfg['ema9_trigger'] else pd.Series(True, index=df.index)

    # 6. Volume Filter
    if cfg['volume_filter']:
        vol_col = f"VOL_{CONFIG['volume_lookback']}"
        if vol_col in df.columns:
            volume_filter = (df['volume'] > df[vol_col])
        else:
            volume_filter = pd.Series(False, index=df.index) # Jika kolom tidak ada, jangan beri sinyal
    else:
        volume_filter = pd.Series(True, index=df.index)

    # 7. ATR Percentile Filter (Regime Filter)
    if cfg.get('atr_percentile_filter', False): # Gunakan .get() agar aman jika key tidak ada
        atr_col = f"ATRr_{CONFIG['atr_period']}"
        if atr_col in df.columns:
            # Hitung persentil ke-40 dari ATR dalam ~7 hari terakhir (288 candle 5m/hari * 7 hari = 2016)
            atr_percentile_40 = df[atr_col].rolling(window=2016, min_periods=200).quantile(0.40).bfill()
            atr_percentile_filter = (df[atr_col] > atr_percentile_40)
        else:
            atr_percentile_filter = pd.Series(False, index=df.index)
    else:
        atr_percentile_filter = pd.Series(True, index=df.index)

    # --- Combine all active filters ---
    long_signal = long_ema_filter & long_rsi_filter & adx_filter & long_ema9_trigger & volume_filter & atr_percentile_filter
    short_signal = short_ema_filter & short_rsi_filter & adx_filter & short_ema9_trigger & volume_filter & atr_percentile_filter

    return long_signal, short_signal, exit_params

# --- REVISI: Konfigurasi Strategi Terpusat ---
# Menggabungkan peta strategi dan bobotnya di satu tempat untuk mempermudah pengelolaan.
STRATEGY_CONFIG = {
    "AdaptiveTrendRide(A3)": {
        "function": signal_version_A3,
        "weight": 1.0
    # },
    # "ReversalMomentumRider(A4R)": {
    #     "function": signal_version_A4R,
    #     "weight": 1.0
    },
    "VolatilityScalper(B1)": {
        "function": signal_version_B1,
        "weight": 0.8 # Contoh: B1 sedikit kurang dipercaya, jadi bobotnya lebih rendah
    }
}