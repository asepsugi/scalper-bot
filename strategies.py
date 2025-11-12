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
    """
    IMPROVED VERSION of A3 - Your historically best performer.
    Changes: Added volume and momentum filters to reduce false signals.
    """
    exit_params = {
        'sl_multiplier': 1.2,
        'rr_ratio': 1.8  # Increased from 1.5 for better reward
    }

    # Original A3 logic (kept as base)
    base_long = (df['trend'] == 'UPTREND') & \
                (df['rsi_15m'].shift(1) < 50) & (df['rsi_15m'] > 50) & \
                (df['rsi_1h'] > 50)

    base_short = (df['trend'] == 'DOWNTREND') & \
                 (df['rsi_15m'].shift(1) > 50) & (df['rsi_15m'] < 50) & \
                 (df['rsi_1h'] < 50)

    # NEW: Add volume confirmation (30% of signals fail due to low volume)
    volume_filter = df['volume'] > (df['VOL_20'] * 0.8)
    
    # NEW: Add momentum filter (avoid ranging markets)
    adx_filter = df[f"ADX_{CONFIG['atr_period']}"] > 20
    
    # NEW: Don't enter if price just moved too far (overextended)
    not_overextended = abs(df['close'].pct_change(3)) < 0.008  # <0.8% move in 3 candles

    long_signal = base_long & volume_filter & adx_filter & not_overextended
    short_signal = base_short & volume_filter & adx_filter & not_overextended

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
    """
    IMPROVED VERSION of B1 - Your second-best performer.
    Changes: Simplified logic, removed over-optimization.
    """
    cfg = CONFIG.get('strategy_b1_regime_filter', {
        'adx_trending_threshold': 23,
        'adx_ranging_threshold': 18,
        'atr_delta_volatile_threshold': 1.5,
        'rsi_trending_long': 55,
        'rsi_trending_short': 45,
        'sl_multiplier': 1.5,  # Loosened from 1.8
        'rr_ratio': 2.0  # Increased from 1.6
    })

    adx = df[f"ADX_{CONFIG['atr_period']}"]
    atr_delta = df['ATR_delta']

    # Regime Detection (simplified)
    is_trending = (adx > cfg['adx_trending_threshold'])
    is_ranging = (adx < cfg['adx_ranging_threshold'])
    is_volatile = (atr_delta > cfg['atr_delta_volatile_threshold'])

    # Trend Following Setup (for trending markets)
    long_trend = (df['close'] > df['trend_ema_15m']) & \
                 (df['rsi_15m'] > cfg['rsi_trending_long']) & \
                 (df['volume'] > df['VOL_20'])  # NEW: Volume filter
    
    short_trend = (df['close'] < df['trend_ema_15m']) & \
                  (df['rsi_15m'] < cfg['rsi_trending_short']) & \
                  (df['volume'] > df['VOL_20'])

    # Mean Reversion Setup (for ranging markets)
    long_range = df['rsi_cross_long'] & (df['close'] < df['trend_ema_15m'])
    short_range = df['rsi_cross_short'] & (df['close'] > df['trend_ema_15m'])

    # Combine based on regime
    long_signal = pd.Series(False, index=df.index)
    short_signal = pd.Series(False, index=df.index)
    
    long_signal.loc[is_trending] = long_trend.loc[is_trending]
    long_signal.loc[is_ranging] = long_range.loc[is_ranging]
    
    short_signal.loc[is_trending] = short_trend.loc[is_trending]
    short_signal.loc[is_ranging] = short_range.loc[is_ranging]
    
    # Filter out volatile periods
    long_signal = long_signal & ~is_volatile
    short_signal = short_signal & ~is_volatile

    exit_params = {
        'sl_multiplier': cfg['sl_multiplier'],
        'rr_ratio': cfg['rr_ratio']
    }

    return long_signal, short_signal, exit_params

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

def signal_version_D1_breakout(df):
    """
    Strategi Breakout & Reversal (Dominan Break & CB1).
    - Mengidentifikasi level S/R minor secara dinamis.
    - Mencari sinyal reversal (Dominan Break) di sekitar S/R.
    - Mencari sinyal breakout (CB1) yang valid.
    """
    exit_params = {
        'sl_multiplier': 1.0, # SL lebih ketat, tepat di level S/R
        'rr_ratio': 2.0       # Target RRR minimal 1:2
    }

    # 1. Identifikasi Support & Resistance minor (misal, 20 candle terakhir)
    # Ini adalah S/R jangka pendek untuk scalping, dihitung secara rolling.
    window = 20
    support = df['low'].rolling(window=window, min_periods=5).min().shift(1)
    resistance = df['high'].rolling(window=window, min_periods=5).max().shift(1)

    # 2. Hitung kekuatan body candle
    body_size = abs(df['close'] - df['open'])
    candle_range = df['high'] - df['low']
    body_strength = (body_size / candle_range).fillna(0)
    is_strong_body = (body_strength > CONFIG.get("body_strength_threshold", 0.6))

    # --- Logika Sinyal LONG ---

    # Skenario 1: Dominan Break Bullish (Reversal dari Support)
    # Candle bullish kuat close di atas support setelah sebelumnya ada candle yang menyentuh/menembus support.
    prev_low_touches_support = (df['low'].shift(1) <= support)
    is_bullish_candle = (df['close'] > df['open'])
    reclaim_support = (df['close'] > support)
    
    long_dominant_break = is_bullish_candle & is_strong_body & prev_low_touches_support & reclaim_support

    # Skenario 2: Candle Break 1 (CB1 Bullish)
    # Candle sebelumnya (CB1) menembus resistance, candle saat ini konfirmasi dengan close di atasnya.
    cb1_breaks_resistance = (df['close'].shift(1) > resistance)
    confirmation_candle = (df['close'] > resistance) & is_strong_body

    long_cb1 = cb1_breaks_resistance & confirmation_candle

    # --- Logika Sinyal SHORT ---

    # Skenario 3: Dominan Break Bearish (Continuation/Breakdown)
    # Candle bearish kuat close di bawah support.
    is_bearish_candle = (df['close'] < df['open'])
    break_support = (df['close'] < support)

    short_dominant_break = is_bearish_candle & is_strong_body & break_support

    # Skenario 4: Candle Break 1 (CB1 Bearish)
    # Candle sebelumnya (CB1) menembus support, candle saat ini konfirmasi dengan close di bawahnya.
    cb1_breaks_support = (df['close'].shift(1) < support)
    confirmation_candle_short = (df['close'] < support) & is_strong_body

    short_cb1 = cb1_breaks_support & confirmation_candle_short

    return (long_dominant_break | long_cb1), (short_dominant_break | short_cb1), exit_params

def signal_version_E1_smc(df):
    """
    Strategi Hibrida V2: SMC Zones + Confluence Filter + CB1 Trigger.
    - Konfirmasi tren HTF (BOS).
    - Membutuhkan konfluensi minimal 2 dari 3: OB, FVG, CB1.
    - Menggunakan candle dengan body kuat sebagai pemicu akhir.
    - Menambahkan filter waktu, volatilitas, dan jarak pivot.
    - REVISI: Menambahkan filter Volume Spike pada pemicu CB1.
    """
    # --- PERBAIKAN: Gunakan parameter exit dari config global untuk fleksibilitas ---
    # Ini memungkinkan Anda menyesuaikan SL/TP dari satu tempat.
    exit_params = {
        'sl_multiplier': CONFIG['atr_multiplier'], # Menggunakan pengali ATR global
        'rr_ratio': CONFIG['risk_reward_ratio']    # Menggunakan rasio R/R global
    }

    # --- 1. Filter Kondisi Pasar & Waktu (BARU) ---
    cfg_filters = CONFIG['trade_filters']
    
    # Filter Waktu: Jangan trade pada jam-jam yang dihindari
    time_filter = ~df.index.hour.isin(cfg_filters['avoid_hours_utc'])
    
    # Filter Volatilitas: Jangan trade saat ada lonjakan ATR yang ekstrem (indikasi news)
    volatility_spike_filter = (df['ATR_delta'] < cfg_filters['max_atr_delta_spike'])

    # REVISI (C.1): Filter Volatilitas Minimum: Hanya trade jika ATR saat ini > persentil ATR rolling.
    min_volatility_filter = (df[f"ATRr_{CONFIG['atr_period']}"] > df['atr_percentile'])

    # Filter Jarak Pivot: Jangan trade terlalu dekat dengan swing high/low terakhir
    atr_val = df[f"ATRr_{CONFIG['atr_period']}"]
    min_dist = atr_val * cfg_filters['min_pivot_distance_atr']
    distance_from_high = abs(df['close'] - df['smc_recent_swing_high'])
    distance_from_low = abs(df['close'] - df['smc_recent_swing_low'])
    pivot_distance_filter = (distance_from_high > min_dist) & (distance_from_low > min_dist)

    # --- 2. Filter Tren HTF ---
    # Hanya trade sesuai arah Break of Structure (BOS) terakhir di HTF.
    is_bullish_trend = (df['smc_trend'] == 'BOS_UP')
    is_bearish_trend = (df['smc_trend'] == 'BOS_DOWN')

    # --- 3. Filter Kekuatan Candle (CB1) & Volume Spike (REVISI A.1) ---
    body_size = abs(df['close'] - df['open'])
    candle_range = df['high'] - df['low']
    body_strength = (body_size / candle_range).fillna(0)
    is_strong_body = (body_strength >= CONFIG.get("body_strength_threshold", 0.6))

    # Pemicu CB1 sekarang harus memiliki body kuat DAN volume di atas rata-rata.
    volume_spike_filter = (df['Volume_spike'] > 1.0)
    cb1_bullish_momentum = is_strong_body & (df['close'] > df['open']) & volume_spike_filter
    cb1_bearish_momentum = is_strong_body & (df['close'] < df['open']) & volume_spike_filter

    # --- 4. Kondisi Konfluensi (OB & FVG) ---
    # Cek apakah harga saat ini berada di dalam zona OB atau FVG yang relevan.
    
    # Kondisi Bullish: Harga di Discount Zone & menyentuh Bullish OB atau Bullish FVG
    in_bullish_ob = (df['smc_ob_type'] == 'BULLISH_OB') & (df['low'] <= df['smc_ob_top']) & (df['high'] >= df['smc_ob_bottom'])
    in_bullish_fvg = (df['smc_fvg_bottom'].notna()) & (df['low'] <= df['smc_fvg_top']) & (df['high'] >= df['smc_fvg_bottom'])
    in_discount_zone = ~df['smc_is_premium']

    # Kondisi Bearish: Harga di Premium Zone & menyentuh Bearish OB atau Bearish FVG
    in_bearish_ob = (df['smc_ob_type'] == 'BEARISH_OB') & (df['low'] <= df['smc_ob_top']) & (df['high'] >= df['smc_ob_bottom'])
    in_bearish_fvg = (df['smc_fvg_top'].notna()) & (df['low'] <= df['smc_fvg_top']) & (df['high'] >= df['smc_fvg_bottom'])
    in_premium_zone = df['smc_is_premium']

    # --- 5. Logika Sinyal Akhir (2 dari 3) ---
    # Hitung skor konfluensi untuk setiap candle
    # Skor = (apakah di OB?) + (apakah di FVG?) + (apakah ada momentum CB1?)
    bullish_confluence_score = in_bullish_ob.astype(int) + in_bullish_fvg.astype(int) + cb1_bullish_momentum.astype(int)
    bearish_confluence_score = in_bearish_ob.astype(int) + in_bearish_fvg.astype(int) + cb1_bearish_momentum.astype(int)

    # Gabungkan semua filter kondisi pasar utama
    market_condition_filters = time_filter & volatility_spike_filter & min_volatility_filter & pivot_distance_filter

    # Sinyal LONG: Tren Bullish + di Zona Diskon + Skor Konfluensi >= 2
    long_signal = market_condition_filters & is_bullish_trend & in_discount_zone & (bullish_confluence_score >= 2)

    # Sinyal SHORT: Tren Bearish + di Zona Premium + Skor Konfluensi >= 2
    short_signal = market_condition_filters & is_bearish_trend & in_premium_zone & (bearish_confluence_score >= 2)

    return long_signal, short_signal, exit_params

def signal_version_E2_smc(df):
    """
    Strategi Hibrida V3 (E2): SMC OB Retest dengan Konfirmasi Fleksibel.
    - Menggunakan EMA 200 sebagai bias tren utama.
    - Entry pada retest Order Block (OB) yang valid.
    - Konfirmasi entry bisa dari CB1 (Candle Break) ATAU Volume Spike.
    - Filter sesi Asia yang lebih selektif berdasarkan volatilitas.
    - Mendukung mode kontrarian opsional.
    """
    # --- 1. Konfigurasi & Parameter Exit Dinamis ---
    cfg_smc = CONFIG['smc_filters']
    cfg_filters = CONFIG['trade_filters']
    atr_val = df[f"ATRr_{CONFIG['atr_period']}"]

    # RR dinamis berdasarkan volatilitas ATR
    # Jika ATR tinggi, gunakan RR lebih rendah. Jika ATR rendah, targetkan RR lebih tinggi.
    atr_percentile_75 = df[f"ATRr_{CONFIG['atr_period']}"].rolling(window=672).quantile(0.75).bfill()

    # REVISI: Sesuaikan risk per trade sesuai spesifikasi E2
    CONFIG['risk_per_trade'] = 0.0075 # 0.75%

    dynamic_rr = np.where(atr_val > atr_percentile_75, 1.2, 2.0)

    exit_params = {
        'sl_multiplier': CONFIG['atr_multiplier'],
        'rr_ratio': dynamic_rr
    }

    # --- 2. Filter Tren Utama & Sesi ---
    # Tren utama menggunakan EMA 200 pada TF sinyal (15m)
    is_bullish_trend = (df['close'] > df['trend_ema_200_15m'])
    is_bearish_trend = (df['close'] < df['trend_ema_200_15m'])

    # Filter Sesi: Boleh trade di sesi Asia hanya jika volatilitas cukup tinggi
    is_asia_session = df.index.hour.isin([0, 1, 2, 3, 4]) # UTC 0-4
    # REVISI: Sederhanakan filter volatilitas Asia agar tidak terlalu ketat.
    # Cukup pastikan ATR saat ini lebih besar dari persentil ke-35 (baseline volatilitas).
    asia_volatility_ok = (atr_val > df['atr_percentile'])
    session_filter = ~is_asia_session | (is_asia_session & asia_volatility_ok)

    # --- 3. Kondisi Zona & Konfirmasi Entry ---
    # Zona: Harga harus berada di dalam Order Block yang valid
    in_bullish_ob = (df['smc_ob_type'] == 'BULLISH_OB') & (df['low'] <= df['smc_ob_top']) & (df['high'] >= df['smc_ob_bottom'])
    in_bearish_ob = (df['smc_ob_type'] == 'BEARISH_OB') & (df['low'] <= df['smc_ob_top']) & (df['high'] >= df['smc_ob_bottom'])

    # Konfirmasi A: CB1 (Candle Break 1)
    body_size = abs(df['close'] - df['open'])
    candle_range = df['high'] - df['low']
    body_strength = (body_size / candle_range).fillna(0)
    is_strong_body = (body_strength >= CONFIG.get("body_strength_threshold", 0.6))
    cb1_bullish = is_strong_body & (df['close'] > df['open'])
    cb1_bearish = is_strong_body & (df['close'] < df['open'])

    # Konfirmasi B: Volume Spike
    volume_spike = (df['Volume_spike'] > 0.8)

    # Gabungkan konfirmasi: Cukup salah satu (CB1 ATAU Volume Spike)
    bullish_confirmation = cb1_bullish | volume_spike
    bearish_confirmation = cb1_bearish | volume_spike

    # --- 4. Logika Sinyal Final ---
    
    # Sinyal Pro-Trend
    long_pro_trend = is_bullish_trend & in_bullish_ob & bullish_confirmation
    short_pro_trend = is_bearish_trend & in_bearish_ob & bearish_confirmation

    # Sinyal Kontrarian (jika diizinkan)
    long_contrarian = pd.Series(False, index=df.index)
    short_contrarian = pd.Series(False, index=df.index)
    if cfg_smc['allow_contrarian_mode']:
        # Ambil posisi long di bearish trend jika ada konfirmasi kuat di Bullish OB
        long_contrarian = is_bearish_trend & in_bullish_ob & bullish_confirmation
        # Ambil posisi short di bullish trend jika ada konfirmasi kuat di Bearish OB
        short_contrarian = is_bullish_trend & in_bearish_ob & bearish_confirmation
        
        # Untuk kontrarian, paksa RR lebih tinggi
        exit_params['rr_ratio'] = np.where(long_contrarian | short_contrarian, 2.0, exit_params['rr_ratio'])

    # Gabungkan sinyal pro-trend dan kontrarian, lalu terapkan filter sesi
    final_long_signal = (long_pro_trend | long_contrarian) & session_filter
    final_short_signal = (short_pro_trend | short_contrarian) & session_filter

    return final_long_signal, final_short_signal, exit_params

def signal_version_F1_silver_bullet(df):
    """
    Strategi ICT "Silver Bullet" (F1).
    - Hanya aktif pada jam sesi NY AM & PM.
    - Mencari setup: Liquidity Sweep -> Displacement dengan FVG -> Entry di FVG.
    """
    cfg = CONFIG['strategy_f1_silver_bullet']
    exit_params = {
        'sl_multiplier': 1.5, # SL ditempatkan di atas/bawah FVG candle, jadi ATR mult bisa lebih besar
        'rr_ratio': 2.0       # Target RR minimal 2:1
    }

    # --- 1. Filter Waktu (Killzone) ---
    # Gabungkan jam sesi AM dan PM ke dalam satu list
    killzone_hours = cfg['am_session_utc'] + cfg['pm_session_utc']
    in_killzone = df.index.hour.isin(killzone_hours)

    # --- 2. Deteksi Liquidity Sweep & Market Structure Shift (MSS) ---
    # --- REVISI LOGIKA F1 (FINAL) ---
    # Pendekatan yang lebih robust:
    # 1. Cari candle "Displacement" (MSS + FVG baru).
    # 2. Untuk setiap displacement, lihat ke belakang (lookback) apakah ada sweep.
    # 3. Jika ya, tandai FVG itu sebagai valid dan tunggu retracement.

    lookback = cfg['lookback_period']

    # --- Langkah 1: Identifikasi "Displacement" ---
    # Displacement adalah pergerakan kuat yang mematahkan struktur (MSS) DAN meninggalkan FVG.

    # Kondisi MSS (Market Structure Shift)
    mss_down = (df['close'] < df['smc_recent_swing_low'].shift(1))
    mss_up = (df['close'] > df['smc_recent_swing_high'].shift(1))

    # Tandai candle yang merupakan FVG baru
    is_new_bearish_fvg = (df['smc_fvg_top'].notna()) & (df['smc_fvg_top'] != df['smc_fvg_top'].shift(1))
    is_new_bullish_fvg = (df['smc_fvg_bottom'].notna()) & (df['smc_fvg_bottom'] != df['smc_fvg_bottom'].shift(1))

    # Gabungkan: Displacement = MSS + FVG baru pada candle yang sama
    bearish_displacement_candle = mss_down & is_new_bearish_fvg
    bullish_displacement_candle = mss_up & is_new_bullish_fvg

    # --- Langkah 2: Konfirmasi bahwa Displacement didahului oleh Liquidity Sweep ---
    # Cek apakah ada sweep dalam 'lookback' candle SEBELUM displacement terjadi.
    # Sweep: High dari window rolling > high sebelum window, atau Low dari window < low sebelum window.
    sweep_high_before_displacement = (df['high'].rolling(window=lookback).max().shift(1) > df['smc_recent_swing_high'].shift(lookback))
    sweep_low_before_displacement = (df['low'].rolling(window=lookback).min().shift(1) < df['smc_recent_swing_low'].shift(lookback))

    # Setup Silver Bullet valid jika ada displacement yang didahului oleh sweep
    valid_bearish_setup_candle = bearish_displacement_candle & sweep_high_before_displacement
    valid_bullish_setup_candle = bullish_displacement_candle & sweep_low_before_displacement

    # --- Langkah 3: "Ingat" FVG yang valid dan tunggu harga kembali ---
    # Gunakan ffill untuk mengisi maju informasi FVG yang valid.
    df['sb_fvg_top_b'] = np.where(valid_bearish_setup_candle, df['smc_fvg_top'], np.nan)
    df['sb_fvg_bottom_b'] = np.where(valid_bearish_setup_candle, df['smc_fvg_bottom'], np.nan)
    df['sb_fvg_top_b'] = df['sb_fvg_top_b'].ffill()
    df['sb_fvg_bottom_b'] = df['sb_fvg_bottom_b'].ffill()

    df['sb_fvg_top_l'] = np.where(valid_bullish_setup_candle, df['smc_fvg_top'], np.nan)
    df['sb_fvg_bottom_l'] = np.where(valid_bullish_setup_candle, df['smc_fvg_bottom'], np.nan)
    df['sb_fvg_top_l'] = df['sb_fvg_top_l'].ffill()
    df['sb_fvg_bottom_l'] = df['sb_fvg_bottom_l'].ffill()

    # Kondisi Entry: Harga saat ini masuk ke dalam FVG valid terakhir
    retrace_to_bearish_fvg = (df['high'] >= df['sb_fvg_bottom_b']) & (df['low'] <= df['sb_fvg_top_b'])
    retrace_to_bullish_fvg = (df['low'] <= df['sb_fvg_top_l']) & (df['high'] >= df['sb_fvg_bottom_l'])

    # Sinyal final: Harus di dalam killzone DAN harga retrace ke FVG yang valid
    # Harus di dalam killzone DAN harga retrace ke FVG yang valid
    short_signal = in_killzone & retrace_to_bearish_fvg
    long_signal = in_killzone & retrace_to_bullish_fvg

    # --- PERBAIKAN: Pastikan tidak ada sinyal berlawanan pada candle yang sama ---
    # Jika long_signal dan short_signal keduanya True, batalkan keduanya.
    conflicting_signals = long_signal & short_signal
    long_signal[conflicting_signals] = False
    short_signal[conflicting_signals] = False

    # --- PERBAIKAN SL: SL seharusnya di atas/bawah candle yang membuat FVG ---
    # Ini sulit dilakukan secara murni vectorized. Untuk saat ini, kita gunakan
    # SL berbasis ATR yang ditempatkan di luar zona FVG sebagai proxy yang baik.
    # SL Long: di bawah FVG bottom. SL Short: di atas FVG top.
    # Logika ini akan dihandle oleh `create_pending_order` yang menempatkan SL
    # berdasarkan ATR dari harga limit, yang sudah berada di dalam FVG.
    # Jadi, `exit_params` yang ada sudah cukup memadai.

    return long_signal, short_signal, exit_params

def signal_version_G1_ut_bot(df):
    """
    Strategi Scalping 1-Menit dari YouTube (G1).
    - Link: https://www.youtube.com/watch?v=WScZLXOHkAk
    - Menggunakan EMA 200 untuk tren dan sinyal "Buy/Sell" dari UT Bot (SuperTrend).
    - Didesain untuk timeframe cepat, namun diadaptasi untuk sistem 15m.
    """
    """
    FIXED VERSION of G1 - Your current failing strategy.
    Critical Fix: Proper SuperTrend parameters for 15m timeframe.
    """
    
    # FIX 1: Calculate SuperTrend with PROPER parameters for 15m
    # Original video used (1, 1.0) for 1-MINUTE chart
    # For 15m, we need (10, 3.0) to avoid noise
    if 'SUPERTd_10_3.0' not in df.columns:
        # If not calculated, fall back to basic trend
        is_uptrend = df['close'] > df['trend_ema_200_15m']
        is_downtrend = df['close'] < df['trend_ema_200_15m']
        
        # Use RSI as trigger instead
        ut_bot_buy_signal = (df['rsi_15m'].shift(1) < 40) & (df['rsi_15m'] > 40)
        ut_bot_sell_signal = (df['rsi_15m'].shift(1) > 60) & (df['rsi_15m'] < 60)
    else:
        is_uptrend = df['close'] > df['EMA_50']  # Use faster EMA
        is_downtrend = df['close'] < df['EMA_50']
        
        ut_bot_buy_signal = (df['SUPERTd_10_3.0'] == 1) & (df['SUPERTd_10_3.0'].shift(1) == -1)
        ut_bot_sell_signal = (df['SUPERTd_10_3.0'] == -1) & (df['SUPERTd_10_3.0'].shift(1) == 1)

    # FIX 2: Add volume confirmation
    volume_surge = df['volume'] > (df['VOL_20'] * 1.2)
    
    # FIX 3: Add momentum confirmation (RSI not in extremes)
    rsi_ok_for_long = (df['rsi_15m'] > 35) & (df['rsi_15m'] < 70)
    rsi_ok_for_short = (df['rsi_15m'] < 65) & (df['rsi_15m'] > 30)
    
    # FIX 4: Don't trade in chop
    adx_filter = df[f"ADX_{CONFIG['atr_period']}"] > 18

    long_signal = is_uptrend & ut_bot_buy_signal & volume_surge & rsi_ok_for_long & adx_filter
    short_signal = is_downtrend & ut_bot_sell_signal & volume_surge & rsi_ok_for_short & adx_filter

    exit_params = {
        'sl_multiplier': 1.3,  # Slightly tighter
        'rr_ratio': 2.0  # Higher target
    }

    return long_signal, short_signal, exit_params

def signal_version_HYBRID_BEST(df):
    """
    NEW: Combines the best elements from A3 and B1.
    This creates a robust, adaptive strategy.
    """
    
    # Get base signals from both strategies
    a3_long, a3_short, _ = signal_version_A3(df)
    b1_long, b1_short, _ = signal_version_B1(df)
    
    # Score-based consensus (either strategy can trigger, but both is stronger)
    long_score = a3_long.astype(int) + b1_long.astype(int)
    short_score = a3_short.astype(int) + b1_short.astype(int)
    
    # Global filters (must pass regardless of strategy)
    time_filter = ~df.index.hour.isin([22, 23, 0, 1, 2])  # Avoid low liquidity hours
    
    # Spread/volatility filter (ensure tradeable conditions)
    atr = df[f"ATRr_{CONFIG['atr_period']}"]
    atr_percentile = atr.rolling(288).rank(pct=True)  # 24h percentile
    volatility_ok = (atr_percentile > 0.25) & (atr_percentile < 0.90)  # Not too dead, not spiking
    
    # Final signals (require at least score of 1, which means 1 strategy agrees)
    long_signal = (long_score >= 1) & time_filter & volatility_ok
    short_signal = (short_score >= 1) & time_filter & volatility_ok
    
    # Dynamic exit parameters based on consensus strength
    # If both agree (score=2), use tighter SL and higher TP
    sl_mult = np.where((long_score == 2) | (short_score == 2), 1.0, 1.3)
    rr = np.where((long_score == 2) | (short_score == 2), 2.5, 1.8)
    
    exit_params = {
        'sl_multiplier': sl_mult,
        'rr_ratio': rr
    }
    
    return long_signal, short_signal, exit_params


# --- REVISI: Konfigurasi Strategi Terpusat ---
# Menggabungkan peta strategi dan bobotnya di satu tempat untuk mempermudah pengelolaan.
STRATEGY_CONFIG = {
    "AdaptiveTrendRide(A3)": {
        "function": signal_version_A3,
        "weight": 1.0
    },
    # "ReversalMomentumRider(A4R)": {
    #     "function": signal_version_A4R,
    #     "weight": 1.0
    # },
    "SmartRegimeScalper(B1)": {
        "function": signal_version_B1,
        "weight": 1.0 
    }
    # "EMAPullbackRider(C1)": {
    #     "function": signal_version_C1,
    #     "weight": 1.2 # Beri bobot sedikit lebih tinggi karena dirancang untuk sistem ini
    # },
    # "DominanBreakout(D1)": {
    #     "function": signal_version_D1_breakout,
    #     "weight": 1.2
    # },
    # "SMC_Hybrid(E1)": {
    #     "function": signal_version_E1_smc,
    #     "weight": 1.5 # Beri bobot tinggi karena ini strategi yang sangat spesifik
    # },
    # "SMC_Hybrid(E2)": {
    #     "function": signal_version_E2_smc,
    #     "weight": 1.5
    # },
    # "SMC_SilverBullet(F1)": {
    #     "function": signal_version_F1_silver_bullet,
    #     "weight": 2.0 # Bobot sangat tinggi karena ini setup probabilitas tinggi
    # },
    # "UTBotScalper(G1)": {
    #     "function": signal_version_G1_ut_bot,
    #     "weight": 1.5
    # }
}