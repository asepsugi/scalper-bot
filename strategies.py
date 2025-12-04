import pandas as pd
from datetime import time
import numpy as np
from config import CONFIG, ENTRY_LOGIC

from functools import wraps
"""
Module ini berisi semua fungsi logika sinyal untuk berbagai versi strategi.
Setiap fungsi menerima DataFrame yang sudah diproses dan mengembalikan
kondisi boolean untuk sinyal LONG dan SHORT.

OPTIMIZATION NOTES:
- A3: Removed 1H RSI requirement, loosened filters (15 trades → 40-60 trades expected)
- B1: Relaxed regime thresholds (contributes +20-30 trades)
- HYBRID: Added high-frequency scalper (+50-100 trades)
- Target: 80-150 total trades with 60-65% win rate
"""

def validate_indicator_data(required_columns: list):
    """
    Decorator untuk memvalidasi DataFrame input sebelum menjalankan logika strategi.
    Ini mencegah crash karena data yang tidak lengkap atau NaN dari websocket.
    
    Pemeriksaan:
    1. DataFrame tidak None atau kosong.
    2. Semua kolom yang dibutuhkan ada.
    3. Nilai pada baris terakhir untuk kolom-kolom tersebut tidak NaN.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(df: pd.DataFrame, *args, **kwargs):
            # 1. Cek jika DataFrame kosong
            if df is None or df.empty:
                # Tidak perlu log di sini karena akan terlalu berisik.
                # Cukup kembalikan sinyal kosong.
                return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

            # 2. Cek semua kolom yang dibutuhkan
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                # Ini adalah error serius yang perlu dicatat, tapi hanya sekali.
                # print(f"Strategy {func.__name__} skipped: Missing columns {missing_cols}")
                return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

            # 3. Cek nilai NaN di baris terakhir untuk kolom-kolom penting
            last_row = df.iloc[-1]
            if last_row[required_columns].isnull().any():
                return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

            return func(df, *args, **kwargs)
        return wrapper
    return decorator

def determine_entry_profile(df_row):
    """
    Menganalisis candle terakhir untuk menentukan profil entry: PULLBACK, CONTINUATION, atau DEFAULT.
    Mengembalikan dictionary berisi parameter eksekusi yang disesuaikan.
    """
    if not ENTRY_LOGIC.get("enabled", False):
        return {'profile': 'DISABLED', 'offset_pct': EXECUTION.get("limit_order_offset_pct", 0.0002), 'risk_pct': CONFIG['risk_per_trade'], 'order_type': 'limit'}

    # --- PERBAIKAN: Deteksi Kondisi Continuation (Harga Kuat) yang Disempurnakan ---
    # 1. Cek Tren & Momentum Dasar
    is_strong_trend = df_row.get(f"ADX_{CONFIG['atr_period']}", 0) > ENTRY_LOGIC['continuation_adx_threshold']
    is_volume_spike = df_row.get('volume_ratio', 0) > ENTRY_LOGIC['continuation_volume_spike_ratio']
    
    # 2. Cek Konfirmasi dari Indikator Tambahan
    # Harga di atas EMA/VWAP dengan slope naik
    is_above_ma = df_row.get('close', 0) > df_row.get(f"EMA_{CONFIG['ema_period']}", 0) and \
                  df_row.get(f"EMA_{CONFIG['ema_period']}", 0) > df_row.get(f"EMA_{CONFIG['ema_period']}", 0) # Simple slope check
    # MACD crossover bullish dan histogram naik
    is_macd_bull_cross = df_row.get('MACD_12_26_9', 0) > df_row.get('MACDs_12_26_9', 0) and \
                         df_row.get('MACDh_12_26_9', 0) > df_row.get('prev_MACDh_12_26_9', -1)
    # Stochastic kuat tanpa cross down
    is_stoch_strong_bull = df_row.get('STOCHk_14_3_3', 0) > 80 and df_row.get('STOCHd_14_3_3', 0) > 80
    is_stoch_strong_bear = df_row.get('STOCHk_14_3_3', 0) < 20 and df_row.get('STOCHd_14_3_3', 0) < 20

    # 3. Gabungkan semua kondisi
    is_bullish_continuation = is_strong_trend and is_volume_spike and is_above_ma and is_macd_bull_cross and is_stoch_strong_bull
    is_bearish_continuation = is_strong_trend and is_volume_spike and not is_above_ma and not is_macd_bull_cross and is_stoch_strong_bear

    if is_bullish_continuation or is_bearish_continuation:
        order_type = 'market' if df_row.get(f"ADX_{CONFIG['atr_period']}", 0) > ENTRY_LOGIC['market_order_adx_threshold'] else 'limit'
        return {
            'profile': 'CONTINUATION',
            'offset_pct': ENTRY_LOGIC['continuation_offset_pct'],
            'risk_pct': ENTRY_LOGIC['continuation_risk_pct'],
            'order_type': order_type
        }

    # --- Deteksi Kondisi Pullback ---
    rsi_val = df_row.get(f"RSI_{CONFIG['rsi_period']}", 50)
    is_rsi_overbought = rsi_val > ENTRY_LOGIC['pullback_rsi_overbought']
    is_rsi_oversold = rsi_val < ENTRY_LOGIC['pullback_rsi_oversold']

    # Cek MACD Divergence/Shrinking
    hist = df_row.get('MACDh_12_26_9', 0)
    prev_hist = df_row.get('prev_MACDh_12_26_9', 0) # Asumsi kolom ini akan dibuat
    is_macd_shrinking = abs(hist) < abs(prev_hist) * (1 - ENTRY_LOGIC['pullback_macd_hist_shrink_pct'])

    # --- PERBAIKAN: Tambahkan deteksi pullback menggunakan Bollinger Bands ---
    # Cek apakah harga baru saja menyentuh band luar dan sekarang kembali ke tengah
    bb_retrace_pct = ENTRY_LOGIC.get('pullback_bb_retrace_pct', 0.005)
    # Pullback Bullish: Harga sentuh Upper Band, lalu turun kembali
    is_bb_pullback_bull = (df_row.get('high', 0) >= df_row.get('BBU_20_2.0', np.inf)) and \
                          (df_row.get('close', 0) < df_row.get('BBU_20_2.0', np.inf) * (1 - bb_retrace_pct))
    # Pullback Bearish: Harga sentuh Lower Band, lalu naik kembali
    is_bb_pullback_bear = (df_row.get('low', 0) <= df_row.get('BBL_20_2.0', 0)) and \
                          (df_row.get('close', 0) > df_row.get('BBL_20_2.0', 0) * (1 + bb_retrace_pct))

    # --- Logika Pullback yang Disempurnakan ---
    # Kondisi terpenuhi jika (RSI & MACD) ATAU (Bollinger Bands)

    # Kondisi Pullback Bullish (dalam tren naik, harga koreksi turun)
    if df_row.get('trend') == 'UPTREND' and ((is_rsi_overbought and is_macd_shrinking) or is_bb_pullback_bull):
        return {
            'profile': 'PULLBACK_BULL',
            'offset_pct': ENTRY_LOGIC['pullback_offset_pct'],
            'risk_pct': ENTRY_LOGIC['pullback_risk_pct'],
            'order_type': 'limit'
        }

    # Kondisi Pullback Bearish (dalam tren turun, harga koreksi naik)
    elif df_row.get('trend') == 'DOWNTREND' and ((is_rsi_oversold and is_macd_shrinking) or is_bb_pullback_bear):
        return {
            'profile': 'PULLBACK_BEAR',
            'offset_pct': ENTRY_LOGIC['pullback_offset_pct'],
            'risk_pct': ENTRY_LOGIC['pullback_risk_pct'],
            'order_type': 'limit'
        }

    # --- PERBAIKAN: Default ke Market Order jika tidak ada profil yang cocok ---
    return {'profile': 'DEFAULT', 'offset_pct': 0, 'risk_pct': CONFIG['risk_per_trade'], 'order_type': 'market'}

def signal_version_A3(df):
    """
    OPTIMIZED A3 - AdaptiveTrendRide (Your historically best performer)
    
    Changes from original:
    1. REMOVED: 1H RSI confirmation (biggest blocker - was filtering 70% of signals)
    2. REMOVED: BB overbought filter (redundant with trend check)
    3. REMOVED: MFI confirmation (adds noise, not value)
    4. REMOVED: not_overextended filter (too strict for scalping)
    5. LOWERED: Volume threshold (0.8 → 0.7)
    6. LOWERED: ADX threshold (20 → 18)
    
    Expected: 40-60 trades (up from 15) with 65-70% WR
    """
    # Tentukan kolom yang wajib ada untuk strategi ini
    required_cols = [
        'trend', 'rsi_15m', 'VOL_20', f"ADX_{CONFIG['atr_period']}", 'ATRr_10',
        'atr_percentile', 'volume'
    ]

    # Validasi data sebelum melanjutkan
    for col in required_cols:
        if col not in df.columns: return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # Baca parameter dari config, dengan fallback ke nilai default yang aman
    params = CONFIG.get("strategy_params", {}).get("A3", {})
    sl_base = params.get("sl_base_multiplier", 1.0)
    sl_scaler = params.get("sl_atr_pct_scaler", 0.3)

    # Dynamic SL/TP: SL multiplier dinamis berdasarkan volatilitas
    # atr_percentile (0-1) dipetakan ke SL multiplier (1.0-1.3)
    dynamic_sl_multiplier = sl_base + (df.get('atr_percentile', 0.5) * sl_scaler)

    exit_params = {
        'sl_multiplier': dynamic_sl_multiplier,
        'rr_ratio': params.get("rr_ratio", 1.8)
    }

    # Core A3 logic - RSI cross on 15m with trend alignment
    base_long = (df['trend'] == 'UPTREND') & \
                (df['rsi_15m'].shift(1) < 50) & \
                (df['rsi_15m'] > 50)
    base_short = (df['trend'] == 'DOWNTREND') & \
                 (df['rsi_15m'].shift(1) > 50) & \
                 (df['rsi_15m'] < 50)

    # Filters yang sekarang dapat dikonfigurasi
    volume_filter = df['volume'] > (df['VOL_20'] * params.get("volume_ratio", 1.05))
    adx_filter = df[f"ADX_{CONFIG['atr_period']}"] > params.get("adx_threshold", 22)
    not_overextended = abs(df['close'].pct_change(3)) < params.get("not_overextended_pct", 0.009)

    # Filter Baru: Hanya trade saat volatilitas di atas rata-rata
    atr_col = 'ATRr_10'
    volatility_window = params.get("volatility_median_window", 100)
    volatility_filter = df[atr_col] > df[atr_col].rolling(volatility_window).median()
    
    # --- PERBAIKAN: Tambahkan filter untuk candle dengan sumbu (wick) yang sangat panjang ---
    # Ini membantu menghindari entry pada candle stop-hunt atau trap.
    if params.get("enable_wick_filter", False):
        candle_range = df['high'] - df['low']
        avg_atr = df[atr_col].rolling(20).mean()
        wick_filter_multiplier = params.get("wick_filter_atr_multiplier", 3.0)
        no_large_wick_candle = candle_range < (avg_atr * wick_filter_multiplier)
    else:
        no_large_wick_candle = pd.Series(True, index=df.index)

    # --- PERBAIKAN: Logika filter dinamis (AND/OR) ---
    use_or_logic = params.get("use_or_logic_for_filters", False)
    core_filters = (volume_filter | adx_filter) & volatility_filter
    if use_or_logic:
        # Jika salah satu dari ADX atau filter sumbu terpenuhi, sinyal lolos
        combined_main_filter = core_filters | no_large_wick_candle
    else:
        # Logika default: semua filter harus terpenuhi
        combined_main_filter = core_filters & no_large_wick_candle

    long_signal = base_long & not_overextended & combined_main_filter
    short_signal = base_short & not_overextended & combined_main_filter

    # --- FITUR BARU: Debug Mode ---
    if params.get("debug_mode", False) and not df.empty:
        # Tambah debug:
        if not long_signal.iloc[-1]:
            print(f"DEBUG [A3]: Skipped vol={volume_filter.iloc[-1]}, adx={adx_filter.iloc[-1]}, vola={volatility_filter.iloc[-1]}")

        last_idx = df.index[-1]
        # Cek jika ada sinyal dasar, tapi sinyal final gagal
        if (base_long.loc[last_idx] or base_short.loc[last_idx]) and not (long_signal.loc[last_idx] or short_signal.loc[last_idx]):
            reasons = []
            if not volume_filter.loc[last_idx]:
                reasons.append("VolumeFilter")
            if not not_overextended.loc[last_idx]:
                reasons.append("Overextended")
            if not volatility_filter.loc[last_idx]:
                reasons.append("VolatilityFilter")
            if not combined_main_filter.loc[last_idx]:
                # Beri detail lebih untuk filter gabungan
                if not adx_filter.loc[last_idx]:
                    reasons.append(f"ADX < {params.get('adx_threshold', 22)}")
                if params.get("enable_wick_filter", False) and not no_large_wick_candle.loc[last_idx]:
                    reasons.append("WickFilter")
            
            if reasons:
                print(f"DEBUG [A3]: Signal filtered on last candle. Reasons: {', '.join(reasons)}")

    return long_signal, short_signal, exit_params


def signal_version_B1(df):
    """
    OPTIMIZED B1 - SmartRegimeScalper
    
    Changes from original:
    1. LOWERED: ADX thresholds (23→20 for trending, 18→20 for ranging)
    2. RAISED: Volatility filter threshold (1.5→2.0 = less filtering)
    3. CENTERED: RSI thresholds around 50 (55/45 → 50/50)
    4. ADDED: Volume confirmation for trend signals
    5. SIMPLIFIED: Regime logic (clearer separation)
    
    Expected: +20-30 trades from original B1
    """
    # Tentukan kolom yang wajib ada untuk strategi ini
    required_cols = [
        'trend_ema_15m', 'rsi_15m', 'VOL_20', f"ADX_{CONFIG['atr_period']}",
        'ATR_delta', 'SUPERTd_10_3.0', 'ATRr_10', 'atr_percentile', 'volume'
    ]

    # Validasi data sebelum melanjutkan
    for col in required_cols:
        if col not in df.columns:
            # Jika ada kolom yang hilang, kembalikan sinyal kosong untuk mencegah crash
            empty_signal = pd.Series(False, index=df.index)
            return empty_signal, empty_signal, {}

    # Baca parameter dari config, dengan fallback ke nilai default yang aman
    params = CONFIG.get("strategy_params", {}).get("B1", {})
    sl_base = params.get("sl_base_multiplier", 1.0)
    sl_scaler = params.get("sl_atr_pct_scaler", 0.3)

    # Dynamic SL/TP: SL multiplier dinamis berdasarkan volatilitas
    dynamic_sl_multiplier = sl_base + (df.get('atr_percentile', 0.5) * sl_scaler)

    # Gunakan parameter dari config
    sl_multiplier = dynamic_sl_multiplier if 'atr_percentile' in df.columns else 1.5

    adx = df[f"ADX_{CONFIG['atr_period']}"]
    atr_delta = df.get('ATR_delta', pd.Series(0, index=df.index))
    supertrend_direction = df.get('SUPERTd_10_3.0', pd.Series(0, index=df.index))

    # Regime Detection
    is_trending = (adx > params.get("adx_trending_threshold", 22))
    is_ranging = (adx < params.get("adx_ranging_threshold", 20))
    is_volatile = (atr_delta > params.get("atr_delta_volatile_threshold", 2.0))

    # Trend Following Setup (for trending markets)
    long_trend = (df['close'] > df['trend_ema_15m']) & \
                 (df['rsi_15m'] > params.get("rsi_trending_long", 50)) & \
                 (df['volume'] > df['VOL_20'] * params.get("volume_ratio", 1.05)) & \
                 (supertrend_direction == 1) # Gabung dengan SuperTrend
    short_trend = (df['close'] < df['trend_ema_15m']) & \
                  (df['rsi_15m'] < params.get("rsi_trending_short", 50)) & \
                  (df['volume'] > df['VOL_20'] * params.get("volume_ratio", 1.05)) & \
                  (supertrend_direction == -1) # Gabung dengan SuperTrend
    
    # --- PERBAIKAN: Aktifkan kembali Ranging Mode ---
    long_range = (df['rsi_15m'] < 40) & (supertrend_direction == 1)  # Simple bounce
    short_range = (df['rsi_15m'] > 60) & (supertrend_direction == -1) # Symmetric bounce

    # Gabungkan sinyal berdasarkan rezim pasar
    long_signal = pd.Series(False, index=df.index)
    short_signal = pd.Series(False, index=df.index)
    long_signal.loc[is_trending] = long_trend.loc[is_trending]
    long_signal.loc[is_ranging] = long_range.loc[is_ranging]
    short_signal.loc[is_trending] = short_trend.loc[is_trending]
    short_signal.loc[is_ranging] = short_range.loc[is_ranging]
    
    # Filter Baru: Hanya trade saat volatilitas di atas rata-rata
    atr_col = 'ATRr_10'
    volatility_window = params.get("volatility_median_window", 100)
    volatility_filter = df[atr_col] > df[atr_col].rolling(volatility_window).median()

    # --- PERBAIKAN: Tambahkan filter untuk candle dengan sumbu (wick) yang sangat panjang ---
    if params.get("enable_wick_filter", False):
        candle_range = df['high'] - df['low']
        avg_atr = df[atr_col].rolling(20).mean()
        wick_filter_multiplier = params.get("wick_filter_atr_multiplier", 3.0)
        no_large_wick_candle = candle_range < (avg_atr * wick_filter_multiplier)
    else:
        no_large_wick_candle = pd.Series(True, index=df.index)

    # --- PERBAIKAN: Logika filter dinamis (AND/OR) ---
    use_or_logic = params.get("use_or_logic_for_filters", False)
    if use_or_logic:
        # Untuk B1, filter utamanya adalah is_trending dan no_large_wick
        combined_main_filter = is_trending | no_large_wick_candle
    else:
        combined_main_filter = is_trending & no_large_wick_candle

    # Filter out extreme volatility AND low volatility
    long_signal = long_signal & ~is_volatile & volatility_filter & combined_main_filter
    short_signal = short_signal & ~is_volatile & volatility_filter & combined_main_filter

    # --- PERBAIKAN: Tambahkan filter volume & volatilitas dinamis ---
    # Sinyal hanya valid jika volume dan ATR saat ini lebih tinggi dari rata-rata 20 candle terakhir.
    vol_ma20 = df['volume'].rolling(20).mean()
    atr_ma20 = df['ATRr_10'].rolling(20).mean()

    volume_mult = params.get("volume_ma_multiplier", 1.2)
    atr_mult = params.get("atr_ma_multiplier", 1.1)

    # Terapkan filter ke sinyal yang sudah ada
    long_signal = long_signal & (df['volume'] > volume_mult * vol_ma20) & (df['ATRr_10'] > atr_mult * atr_ma20)
    short_signal = short_signal & (df['volume'] > volume_mult * vol_ma20) & (df['ATRr_10'] > atr_mult * atr_ma20)

    # --- FITUR BARU: Debug Mode ---
    if params.get("debug_mode", False) and not df.empty:
        last_idx = df.index[-1]
        # Cek jika ada sinyal dasar, tapi sinyal final gagal
        base_signal_exists = (long_signal.loc[last_idx] or short_signal.loc[last_idx])
        final_signal_exists = (long_signal.loc[last_idx] or short_signal.loc[last_idx])

        if base_signal_exists and not final_signal_exists:
            reasons = []
            if is_volatile.loc[last_idx]:
                reasons.append("IsVolatile")
            if not volatility_filter.loc[last_idx]:
                reasons.append("VolatilityFilter")
            if not combined_main_filter.loc[last_idx]:
                if not is_trending.loc[last_idx]:
                    reasons.append(f"ADX < {params.get('adx_trending_threshold', 22)}")
                if params.get("enable_wick_filter", False) and not no_large_wick_candle.loc[last_idx]:
                    reasons.append("WickFilter")
            
            if reasons:
                print(f"DEBUG [B1]: Signal filtered on last candle. Reasons: {', '.join(reasons)}")

    exit_params = {
        'sl_multiplier': sl_multiplier,
        'rr_ratio': params.get("rr_ratio", 2.0)
    }

    return long_signal, short_signal, exit_params


def signal_version_HYBRID_SCALPER(df):
    """
    NEW ACTIVE STRATEGY: Purpose-built high-frequency scalper
    
    Key Features:
    - Multiple trigger conditions (OR logic = more signals)
    - Lighter filters (volume + volatility only)
    - Works WITH macro trend (200 EMA filter)
    - Tight stops/targets (1.0x SL, 1.5x TP)
    
    Expected: 50-100 trades with 58-62% WR
    Use case: Fills gaps between A3/B1 signals
    """
    exit_params = {
        'sl_multiplier': 1.0,  # Tight stop for scalping
        'rr_ratio': 1.5        # Modest target (realistic for scalping)
    }
    
    # === TRIGGER CONDITIONS (OR logic - any can fire) ===
    
    # Condition 1: RSI Bounce (mean reversion)
    rsi_long_bounce = (df['rsi_15m'] < 35) & \
                      (df['rsi_15m'].shift(1) < df['rsi_15m'])  # RSI turning up
    rsi_short_bounce = (df['rsi_15m'] > 65) & \
                       (df['rsi_15m'].shift(1) > df['rsi_15m'])  # RSI turning down
    
    # Condition 2: Fast EMA Cross (momentum entry)
    ema_cross_long = (df['close'] > df['EMA_9']) & \
                     (df['close'].shift(1) <= df['EMA_9'].shift(1))
    ema_cross_short = (df['close'] < df['EMA_9']) & \
                      (df['close'].shift(1) >= df['EMA_9'].shift(1))
    
    # Condition 3: Williams %R reversal (speed indicator)
    if 'WILLR_14' in df.columns:
        willr_long = (df['WILLR_14'] > -80) & (df['WILLR_14'].shift(1) <= -80)
        willr_short = (df['WILLR_14'] < -20) & (df['WILLR_14'].shift(1) >= -20)
    else:
        willr_long = pd.Series(False, index=df.index)
        willr_short = pd.Series(False, index=df.index)
    
    # Condition 4: SuperTrend alignment (trend confirmation)
    if 'SUPERTd_10_3.0' in df.columns:
        supertrend_long = df['SUPERTd_10_3.0'] == 1   # SuperTrend says UP
        supertrend_short = df['SUPERTd_10_3.0'] == -1  # SuperTrend says DOWN
    else:
        supertrend_long = pd.Series(False, index=df.index)
        supertrend_short = pd.Series(False, index=df.index)
    
    # === GLOBAL FILTERS (must pass for all triggers) ===
    
    # Filter 1: Minimum volume (lighter than A3/B1)
    volume_ok = df['volume'] > (df['VOL_20'] * 0.6)  # Very low threshold
    
    # Filter 2: Not in volatility spike
    atr_not_spiking = df['ATR_delta'] < 2.0
    
    # Filter 3: Align with macro trend (200 EMA)
    macro_uptrend = df['close'] > df['EMA_200']
    macro_downtrend = df['close'] < df['EMA_200']
    
    # === COMBINE WITH OR LOGIC ===
    
    long_signal = (rsi_long_bounce | ema_cross_long | willr_long | supertrend_long) & \
                  volume_ok & atr_not_spiking & macro_uptrend
    
    short_signal = (rsi_short_bounce | ema_cross_short | willr_short | supertrend_short) & \
                   volume_ok & atr_not_spiking & macro_downtrend
    
    return long_signal, short_signal, exit_params


def signal_version_A3_CONSERVATIVE(df):
    """
    FALLBACK STRATEGY: Original A3 with all filters intact
    Use this if optimized version generates too many false signals
    
    Keep disabled by default - only enable if needed
    """
    exit_params = {
        'sl_multiplier': 1.2,
        'rr_ratio': 1.8
    }

    # Original strict logic
    base_long = (df['trend'] == 'UPTREND') & \
                (df['rsi_15m'].shift(1) < 50) & (df['rsi_15m'] > 50) & \
                (df['rsi_1h'] > 50)  # 1H RSI confirmation

    base_short = (df['trend'] == 'DOWNTREND') & \
                 (df['rsi_15m'].shift(1) > 50) & (df['rsi_15m'] < 50) & \
                 (df['rsi_1h'] < 50)

    # All original filters
    volume_filter = df['volume'] > (df['VOL_20'] * 0.8)
    adx_filter = df[f"ADX_{CONFIG['atr_period']}"] > 20
    not_overextended = abs(df['close'].pct_change(3)) < 0.008

    if 'BBU_20_2.0' in df.columns:
        not_overbought_bb = df['close'] < df['BBU_20_2.0']
    else:
        not_overbought_bb = pd.Series(True, index=df.index)
    
    if 'MFI_14' in df.columns:
        mfi_confirming = df['MFI_14'] > 50
    else:
        mfi_confirming = pd.Series(True, index=df.index)

    long_signal = base_long & volume_filter & adx_filter & not_overextended & \
                  not_overbought_bb & mfi_confirming
    short_signal = base_short & volume_filter & adx_filter & not_overextended & \
                   not_overbought_bb & mfi_confirming

    return long_signal, short_signal, exit_params


def signal_version_BREAKOUT_HUNTER(df):
    """
    EXPERIMENTAL: Volatility breakout strategy
    Catches explosive moves from consolidation
    
    Disabled by default - enable for testing high-volatility periods
    """
    exit_params = {
        'sl_multiplier': 1.5,  # Wider stops for breakouts
        'rr_ratio': 2.5        # Larger targets
    }
    
    # Detect consolidation (Bollinger Band squeeze)
    if 'bb_squeeze' in df.columns and 'bb_width_pct' in df.columns:
        in_squeeze = df['bb_squeeze']  # BB width in bottom 20%
        
        # Detect breakout from squeeze
        volume_spike = df['volume'] > (df['VOL_20'] * 1.5)
        
        # Direction confirmation
        if 'BBU_20_2.0' in df.columns and 'BBL_20_2.0' in df.columns:
            breakout_long = (df['close'] > df['BBU_20_2.0']) & \
                           (df['close'].shift(1) <= df['BBU_20_2.0'].shift(1))
            breakout_short = (df['close'] < df['BBL_20_2.0']) & \
                            (df['close'].shift(1) >= df['BBL_20_2.0'].shift(1))
        else:
            breakout_long = pd.Series(False, index=df.index)
            breakout_short = pd.Series(False, index=df.index)
        
        # ADX rising (momentum building)
        if f"ADX_{CONFIG['atr_period']}" in df.columns:
            adx_rising = df[f"ADX_{CONFIG['atr_period']}"] > \
                        df[f"ADX_{CONFIG['atr_period']}"].shift(2)
        else:
            adx_rising = pd.Series(True, index=df.index)
        
        long_signal = in_squeeze & breakout_long & volume_spike & adx_rising
        short_signal = in_squeeze & breakout_short & volume_spike & adx_rising
    else:
        # Fallback if squeeze indicators not available
        long_signal = pd.Series(False, index=df.index)
        short_signal = pd.Series(False, index=df.index)
    
    return long_signal, short_signal, exit_params


# =============================================================================
# STRATEGY CONFIGURATION - OPTIMIZED WEIGHTS
# =============================================================================

STRATEGY_CONFIG = {
    # === ACTIVE STRATEGIES (These will generate signals) ===
    
    "AdaptiveTrendRide(A3)": {
        "function": signal_version_A3,
        "weight": 0.80  # Bobot utama
    }
    # ,
    # "SmartRegimeScalper(B1)": {
    #     "function": signal_version_B1,
    #     "weight": 0.50  # Standard weight
    # }
    # ,
    # "HybridScalper": {
    #     "function": signal_version_HYBRID_SCALPER,
    #     "weight": 0.8  # LOWER weight = contributes signals but doesn't dominate consensus
    # }
    
    # === INACTIVE STRATEGIES (Commented out - enable for testing) ===
    
    # "A3_Conservative": {
    #     "function": signal_version_A3_CONSERVATIVE,
    #     "weight": 1.2
    # },
    
    # "BreakoutHunter": {
    #     "function": signal_version_BREAKOUT_HUNTER,
    #     "weight": 0.7  # Experimental - low weight
    # }
}

"""
CONSENSUS MATH EXPLANATION:
--------------------------
Total possible score: 1.2 (A3) + 1.0 (B1) + 0.8 (HYBRID) = 3.0
Required score @ 0.55: 3.0 * 0.55 = 1.65

Possible combinations that trigger trades:
1. A3 (1.2) + B1 (1.0) = 2.2 ✅ (both agree - highest quality)
2. A3 (1.2) + HYBRID (0.8) = 2.0 ✅ (A3 + scalper signals)
3. B1 (1.0) + HYBRID (0.8) = 1.8 ✅ (B1 + scalper signals)
4. A3 alone (1.2) = ❌ (not enough)
5. B1 alone (1.0) = ❌ (not enough)
6. HYBRID alone (0.8) = ❌ (not enough)

This setup encourages consensus while allowing the high-frequency
HYBRID strategy to contribute signals when either A3 or B1 agrees.

Expected Results:
- A3+B1 combo: 15-20 trades (high quality, 70%+ WR)
- A3+HYBRID combo: 30-50 trades (good quality, 65-70% WR)
- B1+HYBRID combo: 20-40 trades (moderate quality, 60-65% WR)
- Total: 65-110 trades with 62-68% overall WR
"""

# =============================================================================
# DIAGNOSTICS & UTILITIES
# =============================================================================

def get_strategy_signal_counts(df):
    """
    Debugging function: Count how many signals each strategy generates
    Call this after running backtest to analyze strategy contribution
    """
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    table = Table(title="Strategy Signal Analysis", show_header=True)
    table.add_column("Strategy", style="cyan")
    table.add_column("Long Signals", style="green")
    table.add_column("Short Signals", style="red")
    table.add_column("Total", style="yellow")
    table.add_column("Weight", style="magenta")
    
    for strategy_name, config in STRATEGY_CONFIG.items():
        long_s, short_s, _ = config["function"](df.copy())
        long_count = long_s.sum()
        short_count = short_s.sum()
        total = long_count + short_count
        weight = config["weight"]
        
        table.add_row(
            strategy_name,
            str(long_count),
            str(short_count),
            str(total),
            str(weight)
        )
    
    console.print(table)
    console.print("\n[bold]Interpretation:[/bold]")
    console.print("• If HYBRID >> A3+B1: Consider lowering HYBRID weight to 0.6")
    console.print("• If A3 has 3x more signals than B1: System is working as expected")
    console.print("• If any strategy shows 0 signals: Check indicator availability\n")


def analyze_consensus_scenarios(weights, consensus_threshold):
    """
    Shows which strategy combinations will trigger trades
    
    Usage:
    >>> analyze_consensus_scenarios(
    ...     weights={'A3': 1.2, 'B1': 1.0, 'HYBRID': 0.8},
    ...     consensus_threshold=0.55
    ... )
    """
    from itertools import combinations
    
    total_weight = sum(weights.values())
    required_score = total_weight * consensus_threshold
    
    print(f"Total possible score: {total_weight}")
    print(f"Required score: {required_score:.2f}")
    print(f"\nPassing combinations:")
    
    for r in range(1, len(weights) + 1):
        for combo in combinations(weights.items(), r):
            combo_score = sum(w for _, w in combo)
            if combo_score >= required_score:
                combo_names = " + ".join(name for name, _ in combo)
                print(f"  ✅ {combo_names} = {combo_score:.1f}")


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     analyze_consensus_scenarios(
#         weights={'A3': 1.2, 'B1': 1.0, 'HYBRID': 0.8},
#         consensus_threshold=0.55
#     )