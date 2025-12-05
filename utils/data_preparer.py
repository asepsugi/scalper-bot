import pandas as pd
import numpy as np
import sys
from .smc_utils import analyze_smc_on_trend_tf # Impor fungsi analisis SMC
from indicators import calculate_indicators # REVISI: Impor fungsi kalkulator

def prepare_data(df_signal, df_trend_15m, df_trend_1h):
    """
    Prepares a single DataFrame with all necessary indicators and aligned multi-timeframe data.
    This revised version is more robust and ensures all required columns are created.
    """
    if any(df is None or df.empty for df in [df_signal, df_trend_15m, df_trend_1h]):
        print("   [Error] Salah satu DataFrame input kosong. Membatalkan preparasi data.", file=sys.stderr)
        return None

    # --- PERBAIKAN: Impor CONFIG di dalam fungsi untuk menghindari circular import ---
    from config import CONFIG
    from indicators import add_linear_regression_angle # Impor fungsi helper
    
    # --- REVISI ALUR LOGIKA UNTUK MENGHILANGKAN WARNING ---
    # 1. Hitung indikator pada setiap DataFrame secara terpisah TERLEBIH DAHULU.
    # Ini memastikan semua kolom sumber ('RSI_14', 'EMA_50', dll.) ada sebelum digabungkan.
    # PERBAIKAN: Hanya hitung indikator dasar di sini. Indikator kustom akan dihitung nanti.
    df_signal, df_trend_15m, df_trend_1h = [calculate_indicators(df.copy()) for df in [df_signal, df_trend_15m, df_trend_1h]]

    # 2. Jadikan df_signal yang sudah diproses sebagai basis utama.
    base_df = df_signal.copy()
    
    # 3. Gabungkan indikator dari timeframe yang lebih tinggi (sekarang kolomnya pasti ada).
    # Daftar indikator yang akan digabungkan dan nama kolom barunya
    mta_indicators = {
        '15m': {
            f"RSI_{CONFIG['rsi_period']}": 'rsi_15m',
            f"EMA_{CONFIG['ema_period']}": 'trend_ema_15m',
            'EMA_200': 'trend_ema_200_15m',
            'SUPERTd_10_3.0': 'supertrend_15m' # PERBAIKAN: Secara eksplisit bawa SuperTrend dari TF 15m
        },
        '1h': {
            f"RSI_{CONFIG['rsi_period']}": 'rsi_1h',
            # REVISI: Hapus MACD karena tidak lagi dihitung di indicators.py dan tidak digunakan oleh strategi.
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

    # --- LANGKAH 4 (PERBAIKAN): Hitung indikator turunan SETELAH semua data gabungan tersedia ---
    base_df['trend'] = np.where(base_df['close'] > base_df['trend_ema_15m'], 'UPTREND', 'DOWNTREND')
    body_range = base_df['high'] - base_df['low']
    base_df['body_strength'] = (abs(base_df['close'] - base_df['open']) / body_range.replace(0, np.nan)).clip(0, 1).fillna(0)

    vol_sma_col = f"VOL_{CONFIG['volume_lookback']}"
    if vol_sma_col in base_df.columns:
        base_df["Volume_spike"] = (base_df["volume"] / base_df[vol_sma_col].replace(0, np.nan)).fillna(0)
    else:
        # Jika setelah semua proses VOL_20 masih tidak ada, ini adalah error, bukan warning.
        print(f"   [ERROR] Kolom krusial '{vol_sma_col}' tidak ada setelah penggabungan data. Periksa 'indicators.py'.", file=sys.stderr)
        base_df["Volume_spike"] = 0.0

    rsi_col = f"RSI_{CONFIG['rsi_period']}"
    base_df['rsi_cross_long'] = (base_df[rsi_col].shift(1) < CONFIG["rsi_oversold"]) & (base_df[rsi_col] > CONFIG["rsi_oversold"])
    base_df['rsi_cross_short'] = (base_df[rsi_col].shift(1) > CONFIG["rsi_overbought"]) & (base_df[rsi_col] < CONFIG["rsi_overbought"])
    
    # --- PERBAIKAN KONSISTENSI: Gunakan f-string untuk nama kolom ATR ---
    atr_col = f"ATRr_{CONFIG['atr_period']}"
    if atr_col in base_df.columns:
        base_df["ATR_delta"] = (base_df[atr_col] / base_df[atr_col].rolling(5).mean().replace(0, 1e-9)).fillna(0)
    else:
        base_df["ATR_delta"] = 0.0

    # --- LANGKAH 5 (BARU): Jalankan Analisis SMC pada TF Trend dan gabungkan ---
    # Kita gunakan df_trend_15m sebagai basis analisis SMC
    smc_zones = analyze_smc_on_trend_tf(df_trend_15m)
    
    # Inisialisasi kolom SMC dengan nilai default
    base_df['smc_ob_top'] = np.nan
    base_df['smc_ob_bottom'] = np.nan
    base_df['smc_ob_type'] = None
    base_df['smc_fvg_top'] = np.nan
    base_df['smc_fvg_bottom'] = np.nan
    base_df['smc_is_premium'] = False
    base_df['smc_recent_swing_high'] = np.nan
    base_df['smc_recent_swing_low'] = np.nan
    base_df['smc_trend'] = smc_zones.get("last_structure", {}).get('type')

    if smc_zones.get("order_block") and smc_zones.get("equilibrium"):
        ob = smc_zones["order_block"]
        base_df['smc_ob_top'] = ob['top']
        base_df['smc_ob_bottom'] = ob['bottom']
        base_df['smc_ob_type'] = ob['type']
    
    if smc_zones.get("fvg"):
        fvg = smc_zones["fvg"]
        base_df['smc_fvg_top'] = fvg['top']
        base_df['smc_fvg_bottom'] = fvg['bottom']

    if smc_zones.get("equilibrium"):
        base_df['smc_recent_swing_high'] = smc_zones.get('recent_swing_high')
        base_df['smc_recent_swing_low'] = smc_zones.get('recent_swing_low')
        base_df['smc_is_premium'] = base_df['close'] > smc_zones["equilibrium"]

    # --- PERBAIKAN FINAL: Isi nilai NaN setelah semua kolom digabungkan ---
    # HAPUS bfill() karena menyebabkan lookahead bias dan merusak data historis.
    # Gunakan ffill() saja untuk mengisi gap setelah penggabungan timeframe.
    base_df.ffill(inplace=True)

    # --- PERBAIKAN DEFINITIF: Hapus semua jenis .dropna() dari sini ---
    # Tugas data_preparer adalah menyiapkan dan menggabungkan data.
    # Pembersihan data akan ditangani oleh pemanggil (strategi atau backtester)
    # dengan cara yang sesuai dengan konteksnya masing-masing.

    return base_df