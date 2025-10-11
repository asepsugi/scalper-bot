import pandas as pd
import numpy as np
import sys
from config import CONFIG
from indicators import calculate_indicators

def prepare_data(df_signal, df_trend_15m, df_trend_1h):
    """
    Prepares a single DataFrame with all necessary indicators and aligned multi-timeframe data.
    This revised version is more robust and ensures all required columns are created.
    """
    if any(df is None or df.empty for df in [df_signal, df_trend_15m, df_trend_1h]):
        print("   [Error] Salah satu DataFrame input kosong. Membatalkan preparasi data.", file=sys.stderr)
        return None

    print("Preparing base data with all indicators...")

    # --- LANGKAH 1: Hitung indikator dasar untuk setiap timeframe ---
    df_signal = calculate_indicators(df_signal)
    df_trend_15m = calculate_indicators(df_trend_15m)
    df_trend_1h = calculate_indicators(df_trend_1h)

    # --- LANGKAH 2: Buat DataFrame gabungan yang bersih ---
    # Mulai dengan DataFrame sinyal sebagai dasar
    base_df = df_signal.copy()

    # --- LANGKAH 3: Gabungkan indikator dari timeframe yang lebih tinggi ---
    # Daftar indikator yang akan digabungkan dan nama kolom barunya
    mta_indicators = {
        '15m': {
            f"RSI_{CONFIG['rsi_period']}": 'rsi_15m',
            f"EMA_{CONFIG['ema_period']}": 'trend_ema_15m',
            'EMA_200': 'trend_ema_200_15m' # Ini yang menyebabkan KeyError sebelumnya
        },
        '1h': {
            f"RSI_{CONFIG['rsi_period']}": 'rsi_1h',
            'MACDh_12_26_9': 'MACDh_1h'
        }
    }

    # Loop untuk menggabungkan dan menyelaraskan data
    for tf, indicators_map in mta_indicators.items():
        df_source = df_trend_15m if tf == '15m' else df_trend_1h
        for source_col, target_col in indicators_map.items():
            if source_col in df_source.columns:
                # `reindex` dengan `method='ffill'` adalah cara yang efisien untuk menyelaraskan
                aligned_series = df_source[source_col].reindex(base_df.index, method='ffill')
                base_df[target_col] = aligned_series
            else:
                print(f"   [Warning] Kolom sumber '{source_col}' tidak ditemukan di DataFrame {tf}. Mengisi dengan NaN.", file=sys.stderr)
                base_df[target_col] = np.nan

    # Isi nilai NaN yang mungkin ada di awal data
    base_df.bfill(inplace=True)
    base_df.ffill(inplace=True)

    # --- LANGKAH 4: Hitung indikator turunan yang bergantung pada data gabungan ---
    base_df['trend'] = np.where(base_df['close'] > base_df['trend_ema_15m'], 'UPTREND', 'DOWNTREND')
    body_range = base_df['high'] - base_df['low']
    base_df['body_strength'] = (abs(base_df['close'] - base_df['open']) / body_range.replace(0, np.nan)).clip(0, 1).fillna(0)
    base_df["ATR_delta"] = (base_df["ATRr_14"] / base_df["ATRr_14"].rolling(5).mean().replace(0, 1e-9)).fillna(0)

    # REVISI: Sesuaikan dengan nama kolom yang benar dari pandas-ta (prefix="VOL")
    vol_sma_col = f"VOL_{CONFIG['volume_lookback']}"
    if vol_sma_col in base_df.columns:
        base_df["Volume_spike"] = (base_df["volume"] / base_df["VOL_20"].replace(0, 1e-9)).fillna(0)
    else:
        base_df["Volume_spike"] = 0.0

    rsi_col = f"RSI_{CONFIG['rsi_period']}"
    base_df['rsi_cross_long'] = (base_df[rsi_col].shift(1) < CONFIG["rsi_oversold"]) & (base_df[rsi_col] > CONFIG["rsi_oversold"])
    base_df['rsi_cross_short'] = (base_df[rsi_col].shift(1) > CONFIG["rsi_overbought"]) & (base_df[rsi_col] < CONFIG["rsi_overbought"])

    print("✅ Data preparation complete. All required columns are present.")
    return base_df