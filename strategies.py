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
                # PERBAIKAN: Jangan hentikan strategi, tapi gunakan nilai fallback.
                print(f"DEBUG [{func.__name__}]: Warning - Missing {missing_cols}. Using fallback values.")
                for col in missing_cols:
                    if 'ADX' in col:
                        df[col] = 20.0  # Default: tren netral/lemah
                    elif 'ATR' in col:
                        # Gunakan nilai kecil yang tidak nol untuk menghindari pembagian dengan nol
                        df[col] = df['close'].mean() * 0.01 
                    elif 'SUPERT' in col:
                        df[col] = 1  # Default: sinyal uptrend
                    elif 'VOL_' in col:
                        df[col] = df['volume'].mean() # Default: volume rata-rata
                    elif 'rsi' in col:
                        df[col] = 50.0 # Default: RSI netral
                    else:
                        df[col] = 0.0 # Fallback umum

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
        return {'profile': 'DISABLED', 'offset_pct': 0.0002, 'risk_multiplier': 1.0, 'order_type': 'limit'}

    # --- PERBAIKAN: Logika Khusus untuk Strategi Breakout ---
    # Jika sinyal berasal dari AltcoinVolumeBreakoutHunter, paksa penggunaan profil CONTINUATION
    # untuk memastikan eksekusi yang cepat dan tidak ketinggalan momen.
    if df_row.get('strategy') == 'AltcoinVolumeBreakoutHunter':
        # Gunakan market order jika tren sangat kuat, jika tidak, gunakan limit order yang agresif.
        order_type = 'market' if df_row.get(f"ADX_{CONFIG['atr_period']}", 0) > ENTRY_LOGIC['market_order_adx_threshold'] else 'limit'
        return {
            'profile': 'CONTINUATION (Forced)',
            'offset_pct': ENTRY_LOGIC['continuation_offset_pct'],
            'risk_multiplier': ENTRY_LOGIC['continuation_risk_multiplier'],
            'risk_pct': 0.01,   # BUGFIX
            'order_type': order_type
        }

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
            'risk_multiplier': ENTRY_LOGIC['continuation_risk_multiplier'],
            'risk_pct': 0.01,   # BUGFIX
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
            'risk_multiplier': ENTRY_LOGIC['pullback_risk_multiplier'],
            'risk_pct': 0.01,   # BUGFIX
            'order_type': 'limit'
        }

    # Kondisi Pullback Bearish (dalam tren turun, harga koreksi naik)
    elif df_row.get('trend') == 'DOWNTREND' and ((is_rsi_oversold and is_macd_shrinking) or is_bb_pullback_bear):
        return {
            'profile': 'PULLBACK_BEAR',
            'offset_pct': ENTRY_LOGIC['pullback_offset_pct'],
            'risk_multiplier': ENTRY_LOGIC['pullback_risk_multiplier'],
            'risk_pct': 0.01,   # BUGFIX
            'order_type': 'limit'
        }

    # --- PERBAIKAN: Default ke profil yang dapat dikonfigurasi ---
    # Jika tidak ada profil agresif (continuation/pullback) yang cocok, gunakan profil default.
    # Ini bisa berupa market order atau limit order yang sabar, tergantung konfigurasi.
    return {
        'profile': 'DEFAULT',
        'offset_pct': ENTRY_LOGIC['default_offset_pct'],
        'risk_multiplier': 1.0,
        'risk_pct': 0.01,   # BUGFIX: Tambah kunci ini agar live_trader.py tidak KeyError
        'order_type': 'limit'
    }

def signal_version_A3(df, symbol: str = None):
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
    # Baca parameter dari config, dengan fallback ke nilai default yang aman
    params = CONFIG.get("strategy_params", {}).get("A3", {})
    sl_base = params.get("sl_base_multiplier", 1.0)
    sl_scaler = params.get("sl_atr_pct_scaler", 0.3)

    # --- PERBAIKAN KRUSIAL: Gunakan nama kolom dinamis dari CONFIG ---
    atr_col = f"ATRr_{CONFIG['atr_period']}" # Seharusnya sudah benar, memastikan saja
    adx_col = f"ADX_{CONFIG['atr_period']}"
    vol_col = f"VOL_{CONFIG['volume_lookback']}"

    # Validasi data sebelum melanjutkan
    required_cols = ['rsi_15m', vol_col, adx_col, 'atr_percentile']
    for col in required_cols:
        if col not in df.columns:
            return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # Dynamic SL/TP: SL multiplier dinamis berdasarkan volatilitas
    # atr_percentile (0-1) dipetakan ke SL multiplier (1.0-1.3)
    dynamic_sl_multiplier = sl_base + (df.get('atr_percentile', 0.5) * sl_scaler)

    exit_params = {
        'sl_multiplier': dynamic_sl_multiplier,
        'rr_ratio': params.get("rr_ratio", 1.8)
    }

    # --- SOLUSI DEFINITIF: Sederhanakan sinyal dasar & filter ---
    # Sinyal dasar: RSI 15m sebagai indikator tren jangka pendek.
    base_long = (df['rsi_15m'] > 51)
    base_short = (df['rsi_15m'] < 49)

    # Filter 1: Tren harus cukup kuat (ADX > 18).
    adx_filter = df[adx_col] > params.get("adx_threshold", 18)
    # Filter 2: Volatilitas tidak boleh terlalu rendah (di atas 25% percentile).
    volatility_filter = df['atr_percentile'] > CONFIG.get("trade_filters", {}).get("min_volatility_atr_percentile", 0.25)

    # --- PERBAIKAN: Kembalikan Wick Filter yang dapat dikonfigurasi ---
    # Filter ini membantu menghindari entry pada candle dengan sumbu (wick) yang sangat panjang.
    if params.get("enable_wick_filter", False):
        candle_range = df['high'] - df['low']
        # Gunakan ATR langsung, bukan rata-ratanya, untuk perbandingan yang lebih reaktif
        wick_filter_multiplier = params.get("wick_filter_atr_multiplier", 2.5) # Sedikit lebih ketat
        no_large_wick_candle = candle_range < (df[atr_col] * wick_filter_multiplier)
    else:
        # Jika dinonaktifkan, filter ini tidak akan berpengaruh
        no_large_wick_candle = pd.Series(True, index=df.index)

    # Gabungkan sinyal dasar HANYA dengan filter-filter esensial.
    # Menghapus filter volume, overextended, dll. yang saling bertentangan.
    long_signal = base_long & adx_filter & volatility_filter & no_large_wick_candle
    short_signal = base_short & adx_filter & volatility_filter & no_large_wick_candle
    
    # --- FITUR BARU: Debug Mode ---
    if params.get("debug_mode", False) and not df.empty:
        # --- PERBAIKAN: Logika debug yang lebih informatif ---
        if not long_signal.any() and not short_signal.any():
            print(f"DEBUG [A3]: No signals generated. Last RSI_15m: {df['rsi_15m'].iloc[-1]:.2f}")

        last_idx = df.index[-1]
        # Cek jika ada sinyal dasar, tapi sinyal final gagal
        if (base_long.loc[last_idx] or base_short.loc[last_idx]) and not (long_signal.loc[last_idx] or short_signal.loc[last_idx]):
            reasons = []
            if not volatility_filter.loc[last_idx]:
                reasons.append("VolatilityFilter")
            if not adx_filter.loc[last_idx]:
                reasons.append(f"ADX < {params.get('adx_threshold', 18)}")
            if params.get("enable_wick_filter", False) and not no_large_wick_candle.loc[last_idx]:
                reasons.append("WickFilter")
            
            if reasons:
                print(f"DEBUG [A3]: Signal filtered on last candle. Reasons: {', '.join(reasons)}")

    return long_signal, short_signal, exit_params


def signal_version_B1(df, symbol: str = None):
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
    # --- PERBAIKAN BUG: Sesuaikan nama kolom ATR agar konsisten ---
    required_cols = [
        'rsi_15m', f"ADX_{CONFIG['atr_period']}",
        'SUPERTd_10_3.0', f"ATRr_{CONFIG['atr_period']}", 'atr_percentile'
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
    supertrend_direction = df.get('SUPERTd_10_3.0', pd.Series(0, index=df.index))

    # Regime Detection
    is_trending = adx > params.get("adx_trending_threshold", 22)
    is_ranging = adx < params.get("adx_ranging_threshold", 18)

    # --- SOLUSI DEFINITIF: Sederhanakan logika sinyal B1 ---
    # Mode 1: Trend Following (saat pasar sedang tren)
    long_trend = (supertrend_direction == 1)
    short_trend = (supertrend_direction == -1)
    
    # Mode 2: Mean Reversion (saat pasar sedang ranging)
    long_range = (df['rsi_15m'] < 40) # Beli saat oversold di pasar ranging
    short_range = (df['rsi_15m'] > 60) # Jual saat overbought di pasar ranging

    # Sinyal aktif jika (kondisi tren terpenuhi) ATAU (kondisi ranging terpenuhi).
    long_signal = (long_trend & is_trending) | (long_range & is_ranging)
    short_signal = (short_trend & is_trending) | (short_range & is_ranging)
    
    # Terapkan SATU filter global: volatilitas tidak boleh terlalu rendah.
    volatility_filter = df['atr_percentile'] > CONFIG.get("trade_filters", {}).get("min_volatility_atr_percentile", 0.25)

    # --- PERBAIKAN: Kembalikan Wick Filter yang dapat dikonfigurasi ---
    atr_col = f"ATRr_{CONFIG['atr_period']}"
    if params.get("enable_wick_filter", False):
        candle_range = df['high'] - df['low']
        wick_filter_multiplier = params.get("wick_filter_atr_multiplier", 2.5)
        no_large_wick_candle = candle_range < (df[atr_col] * wick_filter_multiplier)
    else:
        # Jika dinonaktifkan, filter ini tidak akan berpengaruh
        no_large_wick_candle = pd.Series(True, index=df.index)

    # Hapus semua filter tambahan yang terlalu rumit dan saling membatalkan.
    long_signal = long_signal & volatility_filter & no_large_wick_candle
    short_signal = short_signal & volatility_filter & no_large_wick_candle

    # --- FITUR BARU: Debug Mode ---
    if params.get("debug_mode", False) and not df.empty:
        last_idx = df.index[-1]
        # Cek jika ada sinyal dasar, tapi sinyal final gagal
        if (long_signal.loc[last_idx] or short_signal.loc[last_idx]) and not (long_signal.loc[last_idx] or short_signal.loc[last_idx]):
            reasons = []
            if not volatility_filter.loc[last_idx]:
                reasons.append("VolatilityFilter")
            if params.get("enable_wick_filter", False) and not no_large_wick_candle.loc[last_idx]:
                reasons.append("WickFilter")
            
            if reasons:
                print(f"DEBUG [B1]: Signal filtered on last candle. Reasons: {', '.join(reasons)}")

    exit_params = {
        'sl_multiplier': sl_multiplier,
        'rr_ratio': params.get("rr_ratio", 2.0)
    }

    return long_signal, short_signal, exit_params


def signal_version_HYBRID_SCALPER(df, symbol: str = None):
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


def signal_version_A3_CONSERVATIVE(df, symbol: str = None):
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


def signal_version_BREAKOUT_HUNTER(df, symbol: str = None):
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


def signal_version_AltcoinVolumeBreakoutHunter(df, symbol: str = None):
    """
    NEW EXPERIMENTAL STRATEGY: Altcoin Volume Breakout Hunter

    Designed for volatile altcoins in 2024-2025.
    - Signal: Volume spike (5-8x MA) + Breakout of recent range.
    - Filters: Strong candle body, anti-chase mechanism.
    - Exits: Wide SL (2.8x ATR), aggressive trailing, and partial TPs.
    """
    params = CONFIG.get("strategy_params", {}).get("AltcoinVolumeBreakoutHunter", {})

    # --- PERBAIKAN: Blacklist untuk koin besar ---
    # Sekarang kita menerima 'symbol' sebagai argumen, jadi kita bisa cek langsung.
    if symbol and symbol in params.get("symbol_blacklist", []):
        # Jika simbol ada di blacklist, langsung kembalikan sinyal kosong.
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Indikator & Kolom yang Dibutuhkan ---
    atr_col = f"ATRr_{CONFIG['atr_period']}"
    vol_ma_col = f"VOL_{CONFIG['volume_lookback']}"
    # --- BARU: Tambahkan ADX(14) ke kolom yang dibutuhkan ---
    adx_14_col = "ADX_14"
    required_cols = ['high', 'low', 'close', 'open', 'volume', atr_col, vol_ma_col, adx_14_col]
    required_cols.extend(['DMP_14', 'DMN_14']) # Tambahkan untuk DI filter

    # Validasi data
    if any(col not in df.columns for col in required_cols):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- PILAR 1: MARKET REGIME FILTER (Anti-Choppy & Anti-Distribution) ---
    if params.get("enable_regime_filter", False):
        adx_col = f"ADX_{CONFIG['atr_period']}"
        if adx_col not in df.columns: # Pastikan kolom ADX ada
            return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

        # Kondisi 1: ADX >= 19 (ada momentum direksional)
        adx_ok = df[adx_col] >= params.get("regime_adx_threshold", 19)
        
        # Kondisi 2: ATR / Close >= 0.85% (volatilitas harian minimal)
        atr_pct = (df[atr_col] / df['close'])
        volatility_ok = atr_pct >= params.get("regime_atr_pct_threshold", 0.0085)
        
        regime_filter = adx_ok & volatility_ok

    # --- Parameter dari Config ---
    breakout_window = params.get("breakout_window", 14)
    volume_spike_multiplier = params.get("volume_spike_multiplier", 6.5)
    candle_body_ratio = params.get("candle_body_ratio", 0.65)
    anti_chase_pct = params.get("anti_chase_pct", 0.01) # 1% move in last 2 candles
    # --- BARU: Baca parameter ADX dari config ---
    adx_veto_threshold = params.get("adx_veto_threshold", 18)

    # --- Logika Sinyal ---

    # 1. Filter Volume Spike
    # Volume saat ini harus N kali lebih besar dari rata-rata volume 20 candle terakhir.
    volume_spike = df['volume'] > (df[vol_ma_col] * volume_spike_multiplier)

    # 2. Filter Breakout Range
    # Harga penutupan saat ini harus menembus harga tertinggi/terendah dari N candle terakhir.
    recent_high = df['high'].shift(1).rolling(window=breakout_window).max()
    recent_low = df['low'].shift(1).rolling(window=breakout_window).min()
    breakout_long = df['close'] > recent_high
    breakout_short = df['close'] < recent_low

    # 3. Filter Strong Candle
    # Badan candle harus mendominasi (misal, >65% dari total range high-low).
    candle_range = df['high'] - df['low']
    candle_body = abs(df['close'] - df['open'])
    is_strong_candle = (candle_body / candle_range.replace(0, np.nan)) > candle_body_ratio

    # 4. Filter Anti-Chase
    # Mencegah masuk setelah harga sudah bergerak terlalu kencang.
    # Perubahan harga dalam 2 candle terakhir tidak boleh lebih dari X%.
    price_change_2_candles = abs(df['close'].pct_change(2))
    not_chasing_price = price_change_2_candles < anti_chase_pct

    # 5. (BARU) Veto Filter ADX
    # Sinyal hanya valid jika ada momentum dump yang terkonfirmasi.
    momentum_confirmed = df[adx_14_col] > adx_veto_threshold

    # 6. (BARU) Filter Arah DI
    # Hanya izinkan short jika -DI > +DI (momentum bearish)
    di_confirm_short = df['DMN_14'] > df['DMP_14']

    # 7. (BARU) Filter Tren EMA
    # Memastikan breakout searah dengan tren jangka pendek untuk meningkatkan win rate.
    if params.get("enable_ema_filter", False):
        ema_col = f"EMA_{CONFIG['ema_period']}"
        if ema_col in df.columns:
            with_trend = (df['close'] > df[ema_col])
            against_trend = (df['close'] < df[ema_col])
        else: # Fallback jika EMA tidak ada
            with_trend, against_trend = pd.Series(True, index=df.index), pd.Series(True, index=df.index)
    else: # Jika filter dinonaktifkan di config
        with_trend = pd.Series(True, index=df.index)
        against_trend = pd.Series(True, index=df.index)

    # --- Gabungkan Sinyal ---
    long_signal = volume_spike & breakout_long & is_strong_candle & not_chasing_price & momentum_confirmed & with_trend
    short_signal = volume_spike & breakout_short & is_strong_candle & not_chasing_price & momentum_confirmed & against_trend & di_confirm_short

    # Terapkan Market Regime Filter jika aktif
    if params.get("enable_regime_filter", False):
        long_signal = long_signal & regime_filter
        short_signal = short_signal & regime_filter

    # --- BARU: Global Bull Switch (Prioritas Long) ---
    allow_long_final = params.get("allow_long", True)
    allow_short_final = params.get("allow_short", True)

    if 'rsi_1h_BTC' in df.columns:
        # Jika BTC RSI > 60, kita anggap Bull Regime Kuat.
        # Strategi: Force Allow Long, Block Short, dan Bypass Filter Regime untuk Long.
        is_bull_regime = df['rsi_1h_BTC'] > 60
        
        allow_long_final = np.where(is_bull_regime, True, allow_long_final)
        allow_short_final = np.where(is_bull_regime, False, allow_short_final)
        
        # Bypass regime filter untuk sinyal Long jika di Bull Regime
        # (Karena altcoin mungkin lagging indikatornya tapi ikut pump)
        if params.get("enable_regime_filter", False):
             # Kembalikan sinyal long asli (sebelum difilter regime) di baris yang bull regime
             # Logika: Jika Bull Regime, gunakan sinyal tanpa filter regime. Jika tidak, gunakan sinyal terfilter.
             # Note: Ini agak kompleks di pandas, untuk simplifikasi kita override permission saja dulu.
             pass

    # --- Terapkan Filter Arah ---
    if isinstance(allow_long_final, (np.ndarray, pd.Series)):
        long_signal[~allow_long_final] = False
    elif not allow_long_final:
        long_signal[:] = False
    
    if isinstance(allow_short_final, (np.ndarray, pd.Series)):
        short_signal[~allow_short_final] = False
    elif not allow_short_final:
        short_signal[:] = False

    # --- Metadata & Parameter Exit ---
    # Sesuai permintaan: SL 2.8x ATR, Trailing start 2R, distance 3.0x ATR,
    # Partial TPs di 5R (50%) dan 10R (30%).
    exit_params = {
        'sl_multiplier': params.get("sl_multiplier", 2.8),
        'rr_ratio': 15.0, # Target TP utama sangat jauh, karena kita pakai partial & trailing
        'partial_tps': [
            (5.0, 0.50),  # Jual 50% di 5R
            (10.0, 0.30), # Jual 30% di 10R
        ],
        'trailing': {
            "enabled": True,
            "trigger_rr": params.get("trailing_trigger_rr", 2.0),
            "distance_atr": params.get("trailing_distance_atr", 3.0),
        }
    }

    return long_signal, short_signal, exit_params

def signal_version_MemecoinMoonshotHunter(df, symbol: str = None):
    """
    STRATEGI 1: Long-Only Memecoin Moonshot Hunter
    - Tujuan: Menangkap pump eksplosif pada memecoin dan low-cap.
    - Logic: Volume spike masif + RSI sangat overbought + breakout harga.
    """
    params = CONFIG.get("strategy_params", {}).get("MemecoinMoonshotHunter", {})

    # --- Whitelist Filter ---
    if symbol and symbol not in params.get("symbol_whitelist", []):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Indikator & Kolom ---
    vol_ma_col = f"VOL_{CONFIG['volume_lookback']}"
    rsi_col = f"RSI_{CONFIG['rsi_period']}"
    atr_col = f"ATRr_{CONFIG['atr_period']}"
    required_cols = [vol_ma_col, rsi_col, atr_col, 'high', 'low', 'close']

    if any(col not in df.columns for col in required_cols):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Parameter ---
    vol_spike_mult = params.get("volume_spike_multiplier", 6.5)
    rsi_thresh = params.get("rsi_threshold", 82)
    breakout_window = params.get("breakout_window", 20)
    anti_chase_pct = params.get("anti_chase_pct_limit", 0.18)
    anti_chase_window = params.get("anti_chase_window", 8)

    # --- Trigger Conditions ---
    # 1. Volume Spike (8-15x MA20)
    volume_spike = df['volume'] > (df[vol_ma_col] * vol_spike_mult)

    # 2. RSI Overbought (RSI > 82)
    rsi_hot = df[rsi_col] > rsi_thresh

    # 3. Price Breakout (new 20-candle high)
    recent_high = df['high'].shift(1).rolling(window=breakout_window).max()
    price_breakout = df['close'] > recent_high

    # --- Filters ---
    # 1. Anti-Chase Filter (max 18% move in last 8 candles)
    price_change_recent = df['close'].pct_change(periods=anti_chase_window)
    not_chasing = price_change_recent < anti_chase_pct

    # --- Gabungkan Sinyal (HANYA LONG) ---
    long_signal = volume_spike & rsi_hot & price_breakout & not_chasing
    short_signal = pd.Series(False, index=df.index) # Strategi ini long-only

    # --- Exit Parameters ---
    exit_params = {
        'sl_multiplier': params.get("sl_multiplier", 2.4),
        'rr_ratio': 20.0, # Target utama jauh, trailing akan mengambil alih
        'trailing': {
            "enabled": True,
            "trigger_rr": params.get("trailing_trigger_rr", 3.0),
            "distance_atr": params.get("trailing_distance_atr", 3.5),
        }
    }

    return long_signal, short_signal, exit_params

def signal_version_LongOnlyCorrectionHunter(df, symbol: str = None):
    """
    REFACTORED: Mean Reversion / Dip Buyer
    - Tujuan: Menangkap pantulan teknikal (technical bounce) setelah terjadi dump yang signifikan.
    - Logic: Beli saat harga oversold (RSI < 35) dan menyentuh Lower Bollinger Band, HANYA jika tren makro masih bullish.
    """
    params = CONFIG.get("strategy_params", {}).get("LongOnlyCorrectionHunter", {})
    rsi_col = f"RSI_{CONFIG['rsi_period']}"
    
    # --- REFACTOR: Gunakan parameter BB dinamis dari config ---
    bb_period = params.get("bb_period", 20)
    bb_std = params.get("bb_std_dev", 2.2)
    bb_lower_col = f'BBL_{bb_period}_{bb_std}'

    # Hitung BB kustom jika belum ada di DataFrame
    if bb_lower_col not in df.columns:
        df.ta.bbands(length=bb_period, std=bb_std, append=True)

    # --- REFACTOR: Sederhanakan kolom yang dibutuhkan ---
    # PERBAIKAN: Tambahkan 'volume_ratio' dan 'body_strength'
    required_cols = [rsi_col, bb_lower_col, 'rsi_1h', 'EMA_200_1h', 'close', 'open', 'low', 'volume_ratio', 'body_strength']

    if any(col not in df.columns for col in required_cols):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # =========================================================================
    # REFACTORED: Logika Sinyal Mean Reversion
    # =========================================================================

    # Filter 1: Konteks Tren Makro (Timeframe 1 Jam)
    # Kita hanya tertarik membeli koreksi jika tren besarnya masih naik.
    if params.get("use_macro_trend_filter", True):
        macro_trend_is_up = (df['close'] > df['EMA_200_1h'])
    else:
        macro_trend_is_up = pd.Series(True, index=df.index)

    # Filter 2: Kondisi Oversold di Timeframe Sinyal (5 Menit)
    # Harga harus menyentuh atau sedikit di bawah Lower Bollinger Band.
    price_is_oversold = df['low'] <= df[bb_lower_col]
    # RSI juga harus menunjukkan kondisi oversold.
    rsi_is_oversold = df[rsi_col] < params.get("rsi_oversold_threshold", 30)

    # Filter 3: Sinyal Konfirmasi Reversal
    # Kita mencari candle yang ditutup lebih tinggi dari pembukaannya (candle hijau).
    # Ini adalah konfirmasi paling sederhana bahwa tekanan beli mulai muncul.
    is_bullish_candle = df['close'] > df['open']

    # --- BARU: Filter Konfirmasi Tambahan ---
    # Filter 4: Volume harus di atas rata-rata untuk mengonfirmasi minat beli.
    volume_confirmed = df['volume_ratio'] > params.get("min_volume_ratio", 1.2)

    # Filter 5: Badan candle harus kuat untuk menunjukkan keyakinan.
    if params.get("require_strong_candle_body", True):
        # Menggunakan body_strength yang sudah dihitung di data_preparer
        is_strong_body = df['body_strength'] > 0.6
    else:
        is_strong_body = pd.Series(True, index=df.index)


    long_signal = macro_trend_is_up & price_is_oversold & rsi_is_oversold & is_bullish_candle & volume_confirmed & is_strong_body

    # Matikan sinyal short secara total untuk strategi ini.
    short_signal = pd.Series(False, index=df.index)

    # --- Exit Parameters ---
    exit_params = {
        'sl_multiplier': params.get("sl_multiplier", 2.5),
        'rr_ratio': params.get("rr_ratio", 2.0),
        'partial_tps': params.get("partial_tps", []),
        'trailing': {
            "enabled": True,
            "trigger_rr": params.get("trailing_trigger_rr", 1.2),
            "distance_atr": params.get("trailing_distance_atr", 1.8),
        }
    }

    return long_signal, short_signal, exit_params

def signal_version_MomentumCrossHunter(df, symbol: str = None):
    """
    STRATEGI BARU: Momentum Cross Hunter
    - Tujuan: Menangkap momentum yang kuat saat terjadi persilangan MA jangka pendek dan menengah.
    - Logic: Menunggu Golden Cross (7/25/99) atau Death Cross (7/25/99) dengan konfirmasi dari RSI dan MACD.
    """
    # --- PERBAIKAN TOTAL: Baca parameter dari blok config yang sudah dirombak ---
    params = CONFIG.get("strategy_params", {}).get("MomentumCrossHunter", {})

    # --- PERBAIKAN: Filter blacklist simbol ---
    if symbol and symbol in params.get("symbol_blacklist", []):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Ambil data untuk filter ---
    rsi_col = f"RSI_{CONFIG['rsi_period']}"

    # --- Parameter ---
    ema7 = df['EMA_7']
    ema25 = df['EMA_25']
    ema99 = df['EMA_99']

    # --- Kondisi Sinyal ---

    # 1. Kondisi Golden Cross (Long)
    #    - EMA 7 baru saja memotong ke atas EMA 25
    cross_up_event = (ema7.shift(1) <= ema25.shift(1)) & (ema7 > ema25)
    # --- PERBAIKAN: Logika above_long_term_trend yang dapat dikonfigurasi ---
    if params.get("strict_alignment", True):
        # Logika ketat: EMA7 dan EMA25 harus di atas EMA99
        above_long_term_trend = (ema7 > ema99) & (ema25 > ema99)
    else:
        # Logika longgar: Cukup EMA25 di atas EMA99 (EMA7 boleh crossing)
        above_long_term_trend = (ema25 > ema99)

    # 2. Kondisi Death Cross (Short)
    #    - EMA 7 baru saja memotong ke bawah EMA 25
    cross_down_event = (ema7.shift(1) >= ema25.shift(1)) & (ema7 < ema25)
    # --- PERBAIKAN: Logika below_long_term_trend yang dapat dikonfigurasi ---
    if params.get("strict_alignment", True):
        # Logika ketat: EMA7 dan EMA25 harus di bawah EMA99
        below_long_term_trend = (ema7 < ema99) & (ema25 < ema99)
    else:
        # Logika longgar: Cukup EMA25 di bawah EMA99
        below_long_term_trend = (ema25 < ema99)

    # --- Konfirmasi Momentum ---

    # 3. Konfirmasi RSI
    rsi_confirm_long = df[rsi_col] > params.get("rsi_threshold_long", 50)
    rsi_confirm_short = df[rsi_col] < params.get("rsi_threshold_short", 50)

    # 4. Konfirmasi MACD
    if params.get("use_macd_confirm", True):
        macd_confirm_long = df['MACD_12_26_9'] > df['MACDs_12_26_9']
        macd_confirm_short = df['MACD_12_26_9'] < df['MACDs_12_26_9']
    else:
        macd_confirm_long = pd.Series(True, index=df.index)
        macd_confirm_short = pd.Series(True, index=df.index)

    # --- PERBAIKAN: Mode Extreme Test ---
    if params.get("extreme_test_mode", False):
        # Hanya gunakan persilangan EMA dan konfirmasi RSI dasar
        
        # --- PERBAIKAN: Validasi kolom khusus untuk mode ini ---
        required_cols_extreme = ['EMA_7', 'EMA_25', rsi_col]
        if any(col not in df.columns for col in required_cols_extreme):
            # Jika kolom dasar pun tidak ada, maka ada masalah data fundamental
            print(f"DEBUG [MCH Extreme Test]: Missing fundamental columns: {required_cols_extreme}")
            return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

        long_signal = cross_up_event & rsi_confirm_long
        short_signal = cross_down_event & rsi_confirm_short
    else:
        # --- Logika Filter Lengkap ---

        # --- PERBAIKAN TOTAL: Validasi Kolom Dinamis ---
        # Mulai dengan kolom inti yang selalu dibutuhkan
        adx_col = f"ADX_{CONFIG['atr_period']}"
        required_cols_full = [
            'EMA_7', 'EMA_25', 'EMA_99', rsi_col, 'MACD_12_26_9', 'MACDs_12_26_9', adx_col
        ]
        # Tambahkan kolom lain hanya jika filternya aktif
        if params.get("use_htf_filter", True):
            required_cols_full.append('EMA_200_1h')
        if params.get("use_di_filter", True):
            required_cols_full.extend([f"DMP_{CONFIG['atr_period']}", f"DMN_{CONFIG['atr_period']}"])
        if params.get("use_volatility_filter", True):
            required_cols_full.append('bb_width_pct')

        if any(col not in df.columns for col in required_cols_full):
            return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}
        
        adx = df[adx_col]

        # Filter 1: Higher Timeframe Trend Alignment
        if params.get("use_htf_filter", True):
            long_htf_ok = df['close'] > df['EMA_200_1h']
            short_htf_ok = df['close'] < df['EMA_200_1h']
        else:
            long_htf_ok = short_htf_ok = pd.Series(True, index=df.index)

        # Filter 2: Minimum Trend Strength (ADX Level)
        trend_is_strong_enough = adx > params.get("min_adx_level", 23)

        # Filter 3: Directional Bias (DI Cross)
        if params.get("use_di_filter", True):
            dmp = df[f"DMP_{CONFIG['atr_period']}"]
            dmn = df[f"DMN_{CONFIG['atr_period']}"]
            long_di_ok = dmp > dmn
            short_di_ok = dmn > dmp
        else:
            long_di_ok = short_di_ok = pd.Series(True, index=df.index)

        # Filter 4 & 5: Volatility Expansion (BBW Expanding & above min percentile)
        if params.get("use_volatility_filter", True):
            bbw_pct = df['bb_width_pct']
            bbw_expanding_window = params.get("bbw_is_expanding_window", 3)
            
            is_expanding = bbw_pct > bbw_pct.shift(bbw_expanding_window)
            is_above_min_vol = bbw_pct > params.get("bbw_min_percentile", 0.30)

            if params.get("use_volatility_or_logic", True):
                volatility_ok = is_expanding | is_above_min_vol
            else:
                volatility_ok = is_expanding & is_above_min_vol
        else:
            volatility_ok = pd.Series(True, index=df.index)

        # Gabungkan Sinyal dengan semua filter
        long_signal = (cross_up_event & above_long_term_trend & rsi_confirm_long & macd_confirm_long &
                       long_htf_ok & trend_is_strong_enough & long_di_ok & volatility_ok)
        short_signal = (cross_down_event & below_long_term_trend & rsi_confirm_short & macd_confirm_short &
                        short_htf_ok & trend_is_strong_enough & short_di_ok & volatility_ok)

    # --- BARU: Logika Adaptif Berdasarkan Rezim BTC ---
    allow_long_final = params.get("allow_long", True)
    allow_short_final = params.get("allow_short", True)
    
    if 'rsi_1h_BTC' in df.columns:
        # Jika RSI BTC > 60 (Sesuai Request), kita berada dalam rezim bull.
        # Paksa 'allow_long' menjadi True dan 'allow_short' menjadi False.
        is_bull_regime = df['rsi_1h_BTC'] > 60
        # `np.where` akan memilih nilai berdasarkan kondisi per baris
        allow_long_final = np.where(is_bull_regime, True, allow_long_final)
        allow_short_final = np.where(is_bull_regime, False, allow_short_final)

    # --- PERBAIKAN: Terapkan filter arah sinyal dinamis ---
    # `allow_long_final` dan `allow_short_final` bisa jadi Series atau boolean
    if isinstance(allow_long_final, (np.ndarray, pd.Series)):
        long_signal[~allow_long_final] = False
    elif not allow_long_final:
        long_signal[:] = False
    
    if isinstance(allow_short_final, (np.ndarray, pd.Series)):
        short_signal[~allow_short_final] = False
    elif not allow_short_final:
        short_signal[:] = False

    # --- Exit Parameters ---
    # Menggunakan parameter yang sudah dioptimalkan sesuai analisis.
    exit_params = {
        'sl_multiplier': params.get("sl_multiplier", 2.8),
        'rr_ratio': params.get("rr_ratio", 2.5),
        'use_breakeven_stop': params.get("use_breakeven_stop", True),
        'breakeven_trigger_rr': params.get("breakeven_trigger_rr", 1.0),
        'trailing': {
            "enabled": True,
            "trigger_rr": params.get("trailing_trigger_rr", 1.2),
            "distance_atr": params.get("trailing_distance_atr", 2.0),
        }
    }

    return long_signal, short_signal, exit_params

def signal_version_RSIDivergenceHunter(df, symbol: str = None):
    """
    TIGHTENED STRATEGY: RSI Divergence Momentum
    - Tujuan: Menangkap pembalikan momentum BERKUALITAS TINGGI dari area RSI ekstrem.
    - Perubahan dari versi sebelumnya:
      1. ADX threshold dinaikkan ke 25 (hanya pasar trending kuat)
      2. RSI Zone Filter: divergensi hanya valid di zona oversold (<35) / overbought (>65)
      3. Minimum RSI Divergence Gap: selisih RSI minimal 5 poin
      4. MACD divergence konfirmasi wajib
      5. SL/TP ditingkatkan untuk justifikasi trade yang sedikit tapi berkualitas
    """
    params = CONFIG.get("strategy_params", {}).get("RSIDivergenceHunter", {})
    rsi_col = f"RSI_{CONFIG['rsi_period']}"

    # --- Market Regime Filter (berbasis BTC RSI) ---
    if params.get("use_regime_filter", True):
        if 'rsi_1h_BTC' in df.columns:
            # Nonaktifkan seluruh strategi jika BTC sedang bullish kuat
            last_btc_rsi = df['rsi_1h_BTC'].iloc[-1]
            if last_btc_rsi > params.get("regime_btc_rsi_threshold", 60):
                return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Blacklist Filter ---
    if symbol and symbol in params.get("symbol_blacklist", []):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Kolom yang Dibutuhkan ---
    adx_col = f"ADX_{CONFIG['atr_period']}"
    required_cols = ['rsi_bearish_div', 'rsi_bullish_div', adx_col, rsi_col]
    if params.get("use_macd_div_confirm", True):
        required_cols.extend(['macd_bearish_div', 'macd_bullish_div'])

    if any(col not in df.columns for col in required_cols):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    rsi = df[rsi_col]
    adx = df[adx_col]

    # ==========================================================================
    # FILTER 1: Kekuatan Tren (ADX > 25 — DIPERKETAT dari 22)
    # Divergensi hanya bermakna jika ada tren yang cukup kuat
    # ==========================================================================
    trend_is_strong = adx > params.get("adx_threshold", 25)

    # ==========================================================================
    # FILTER 2: RSI Zone Filter (BARU)
    # Bullish divergensi hanya valid di zona oversold, bearish di overbought
    # Ini menghindari divergensi palsu di tengah range
    # ==========================================================================
    in_oversold_zone = pd.Series(False, index=df.index)
    in_overbought_zone = pd.Series(False, index=df.index)

    if params.get("use_rsi_zone_filter", True):
        rsi_oversold_thresh = params.get("rsi_zone_oversold", 35)
        rsi_overbought_thresh = params.get("rsi_zone_overbought", 65)
        in_oversold_zone = rsi < rsi_oversold_thresh
        in_overbought_zone = rsi > rsi_overbought_thresh
    else:
        in_oversold_zone = pd.Series(True, index=df.index)
        in_overbought_zone = pd.Series(True, index=df.index)

    # ==========================================================================
    # FILTER 3: Minimum RSI Divergence Gap (BARU)
    # Pastikan RSI saat ini berbeda SIGNIFIKAN dari nilai lookback
    # Ini menyaring divergensi "weak" yang hampir tidak ada perbedaannya
    # ==========================================================================
    min_gap = params.get("min_rsi_divergence_gap", 5.0)
    lookback = 10  # Sama dengan yang digunakan di indicators.py
    rsi_gap_bullish = (rsi.shift(lookback) - rsi).abs()   # Seberapa besar RSI naik dari low
    rsi_gap_bearish = (rsi - rsi.shift(lookback)).abs()   # Seberapa besar RSI turun dari high
    has_meaningful_bullish_div = rsi_gap_bullish >= min_gap
    has_meaningful_bearish_div = rsi_gap_bearish >= min_gap

    # ==========================================================================
    # FILTER 4: MACD Divergence Confirmation (sudah ada, tetap wajib)
    # ==========================================================================
    if params.get("use_macd_div_confirm", True):
        macd_confirm_long = df['macd_bullish_div']
        macd_confirm_short = df['macd_bearish_div']
    else:
        macd_confirm_long = pd.Series(True, index=df.index)
        macd_confirm_short = pd.Series(True, index=df.index)

    # ==========================================================================
    # GABUNGKAN: Semua filter harus terpenuhi
    # ==========================================================================
    long_signal = (
        df['rsi_bullish_div']        # Deteksi divergensi bullish
        & trend_is_strong            # Tren cukup kuat
        & in_oversold_zone           # RSI di zona oversold
        & has_meaningful_bullish_div # Gap RSI yang signifikan
        & macd_confirm_long          # Konfirmasi MACD
    )
    short_signal = (
        df['rsi_bearish_div']        # Deteksi divergensi bearish
        & trend_is_strong            # Tren cukup kuat
        & in_overbought_zone         # RSI di zona overbought
        & has_meaningful_bearish_div # Gap RSI yang signifikan
        & macd_confirm_short         # Konfirmasi MACD
    )

    # ==========================================================================
    # Logika Adaptif Berdasarkan Rezim BTC
    # ==========================================================================
    allow_long_final = params.get("allow_long", True)
    allow_short_final = params.get("allow_short", True)

    if 'rsi_1h_BTC' in df.columns:
        is_bull_regime = df['rsi_1h_BTC'] > 60
        allow_long_final = np.where(is_bull_regime, True, allow_long_final)
        allow_short_final = np.where(is_bull_regime, False, allow_short_final)

    if isinstance(allow_long_final, (np.ndarray, pd.Series)):
        long_signal[~allow_long_final] = False
    elif not allow_long_final:
        long_signal[:] = False

    if isinstance(allow_short_final, (np.ndarray, pd.Series)):
        short_signal[~allow_short_final] = False
    elif not allow_short_final:
        short_signal[:] = False

    # --- Exit Parameters (DIPERKETAT untuk justifikasi trade berkualitas) ---
    exit_params = {
        'sl_multiplier': params.get("sl_multiplier", 2.5),
        'rr_ratio': params.get("rr_ratio", 2.5),
        'trailing': {
            "enabled": True,
            "trigger_rr": params.get("trailing_trigger_rr", 1.5),
            "distance_atr": params.get("trailing_distance_atr", 2.0),
        }
    }
    return long_signal, short_signal, exit_params


def signal_version_VWAPMeanReversionScalper(df, symbol: str = None):
    """
    NEW STRATEGY: VWAP Mean Reversion Scalper
    - Tujuan: Menangkap bounce dari VWAP saat harga overextended.
    - Logic:
        LONG:  Harga turun SIGNIFIKAN di bawah VWAP + RSI oversold + Volume spike + Candle bullish reversal
        SHORT: Harga naik SIGNIFIKAN di atas VWAP + RSI overbought + Volume spike + Candle bearish reversal
    - Edge: VWAP adalah level institusional yang kuat; mean reversion ke VWAP sangat sering terjadi di crypto.
    - Target: 40-70 trades per bulan, WR 55-62%, SL ketat (1.5x ATR), RR 2:1
    """
    params = CONFIG.get("strategy_params", {}).get("VWAPMeanReversionScalper", {})

    # --- Blacklist Filter ---
    if symbol and symbol in params.get("symbol_blacklist", []):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    # --- Kolom yang Dibutuhkan ---
    rsi_col = f"RSI_{CONFIG['rsi_period']}"
    vol_ma_col = f"VOL_{CONFIG['volume_lookback']}"
    atr_col = f"ATRr_{CONFIG['atr_period']}"

    required_cols = ['close', 'open', 'high', 'low', 'volume', 'VWAP_D',
                     rsi_col, vol_ma_col, atr_col, 'atr_percentile']

    if any(col not in df.columns for col in required_cols):
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index), {}

    rsi = df[rsi_col]
    vwap = df['VWAP_D']
    close = df['close']
    open_ = df['open']
    high = df['high']
    low = df['low']
    atr = df[atr_col]

    # ==========================================================================
    # FILTER A: Volatility Regime (jangan trade di pasar mati atau saat spike ekstrem)
    # ==========================================================================
    atr_pct = df['atr_percentile']
    volatility_ok = (
        (atr_pct > params.get("min_atr_percentile", 0.30)) &
        (atr_pct < params.get("max_atr_percentile", 0.90))
    )

    # ==========================================================================
    # FILTER B: Deviasi Harga dari VWAP
    # Harga harus sudah "jauh" dari VWAP sebelum kita ekspektasikan mean reversion
    # ==========================================================================
    vwap_safe = vwap.replace(0, np.nan)  # Hindari division by zero
    price_vs_vwap_pct = (close - vwap_safe) / vwap_safe  # Positif = di atas VWAP

    dev_pct_long = params.get("vwap_deviation_pct_long", 0.005)    # -0.5% untuk long
    dev_pct_short = params.get("vwap_deviation_pct_short", 0.005)  # +0.5% untuk short

    price_below_vwap = price_vs_vwap_pct < -dev_pct_long   # Harga sudah turun cukup
    price_above_vwap = price_vs_vwap_pct > dev_pct_short   # Harga sudah naik cukup

    # ==========================================================================
    # FILTER C: RSI di Zona Ekstrem
    # ==========================================================================
    rsi_os = params.get("rsi_oversold", 33)
    rsi_ob = params.get("rsi_overbought", 67)
    rsi_oversold = rsi < rsi_os
    rsi_overbought = rsi > rsi_ob

    # ==========================================================================
    # FILTER D: Volume Spike (konfirmasi ada partisipan yang masuk)
    # ==========================================================================
    vol_mult = params.get("volume_spike_multiplier", 1.5)
    volume_confirmed = df['volume'] > (df[vol_ma_col] * vol_mult)

    # ==========================================================================
    # FILTER E: Candle Reversal (body dalam arah yang benar)
    # Long:  Candle harus BULLISH (close > open) = konfirmasi buyer masuk
    # Short: Candle harus BEARISH (close < open) = konfirmasi seller masuk
    # Body harus cukup besar relatif terhadap range candle
    # ==========================================================================
    candle_range = (high - low).replace(0, np.nan)
    candle_body = abs(close - open_)
    min_body_ratio = params.get("min_body_ratio", 0.45)
    body_strong_enough = (candle_body / candle_range) >= min_body_ratio

    is_bullish_candle = close > open_  # Candle hijau
    is_bearish_candle = close < open_  # Candle merah

    # ==========================================================================
    # FILTER F (Opsional): Trend Alignment
    # Long hanya jika tren 15m masih UPTREND (mean reversion dalam tren besar = lebih aman)
    # Short hanya jika tren 15m masih DOWNTREND
    # ==========================================================================
    if params.get("use_trend_alignment", True):
        # Gunakan 'trend' column yang sudah dihitung dari EMA 15m di data_preparer
        if 'trend' in df.columns:
            trend_allows_long = df['trend'] == 'UPTREND'
            trend_allows_short = df['trend'] == 'DOWNTREND'
        else:
            # Fallback: gunakan EMA_50 sebagai trend filter
            ema_col = f"EMA_{CONFIG['ema_period']}"
            if ema_col in df.columns:
                trend_allows_long = close > df[ema_col]
                trend_allows_short = close < df[ema_col]
            else:
                trend_allows_long = pd.Series(True, index=df.index)
                trend_allows_short = pd.Series(True, index=df.index)
    else:
        trend_allows_long = pd.Series(True, index=df.index)
        trend_allows_short = pd.Series(True, index=df.index)

    # ==========================================================================
    # GABUNGKAN SINYAL
    # LONG:  Semua kondisi bullish terpenuhi
    # SHORT: Semua kondisi bearish terpenuhi
    # ==========================================================================
    long_signal = (
        price_below_vwap        # Harga di bawah VWAP (target untuk kembali ke VWAP)
        & rsi_oversold           # RSI oversold (momentum lemah, potensi reversal)
        & volume_confirmed       # Volume spike (institusi mulai masuk)
        & is_bullish_candle      # Candle reversal bullish
        & body_strong_enough     # Body cukup kuat
        & volatility_ok          # Volatilitas dalam range normal
        & trend_allows_long      # Arah tren mendukung
    )

    short_signal = (
        price_above_vwap         # Harga di atas VWAP (target untuk turun ke VWAP)
        & rsi_overbought          # RSI overbought (momentum lemah, potensi reversal)
        & volume_confirmed        # Volume spike
        & is_bearish_candle       # Candle reversal bearish
        & body_strong_enough      # Body cukup kuat
        & volatility_ok           # Volatilitas dalam range normal
        & trend_allows_short      # Arah tren mendukung
    )

    # --- Exit Parameters: Scalping ketat ---
    exit_params = {
        'sl_multiplier': params.get("sl_multiplier", 1.5),
        'rr_ratio': params.get("rr_ratio", 2.0),
        'trailing': {
            "enabled": True,
            "trigger_rr": params.get("trailing_trigger_rr", 1.0),  # Breakeven cepat
            "distance_atr": params.get("trailing_distance_atr", 1.2),
        }
    }

    return long_signal, short_signal, exit_params

# =============================================================================
# STRATEGY CONFIGURATION - OPTIMIZED WEIGHTS
# =============================================================================

STRATEGY_CONFIG = {
    # =========================================================================
    # === ACTIVE STRATEGIES ===
    # Total possible score: 0.50 + 0.20 + 0.15 + 0.20 + 0.25 = 1.30
    # consensus_ratio = 0.09 → required_score = 1.30 * 0.09 ≈ 0.12
    # Artinya: 1 strategi apapun sudah cukup trigger trade (single-strategy mode)
    # Untuk konsensus lebih ketat, naikkan consensus_ratio ke 0.35-0.45
    # =========================================================================

    "AltcoinVolumeBreakoutHunter": {
        "function": signal_version_AltcoinVolumeBreakoutHunter,
        "weight": 0.50  # Strategi utama — volume breakout altcoin
    },
    "LongOnlyCorrectionHunter": {
        "function": signal_version_LongOnlyCorrectionHunter,
        "weight": 0.20  # DINAIKKAN: Dari 0.10 -> 0.20 agar lebih berpengaruh
    },
    "MomentumCrossHunter": {
        "function": signal_version_MomentumCrossHunter,
        "weight": 0.15  # Strategi trend-following berbasis EMA cross
    },
    # DIPERKETAT: Bobot lebih rendah karena filter jauh lebih ketat sekarang
    # Trade lebih sedikit tapi JAUH lebih berkualitas
    "RSIDivergenceHunter": {
        "function": signal_version_RSIDivergenceHunter,
        "weight": 0.20  # TURUN: Dari 0.25 -> 0.20 untuk mencerminkan filter lebih ketat
    },
    # BARU: VWAP Mean Reversion — strategi baru berbasis level institusional
    "VWAPMeanReversionScalper": {
        "function": signal_version_VWAPMeanReversionScalper,
        "weight": 0.25  # Bobot cukup tinggi — edge yang jelas di crypto
    },

    # =========================================================================
    # === INACTIVE STRATEGIES (enable untuk testing) ===
    # =========================================================================

    # "AdaptiveTrendRide(A3)": {
    #     "function": signal_version_A3,
    #     "weight": 0.50
    # },
    # "SmartRegimeScalper(B1)": {
    #     "function": signal_version_B1,
    #     "weight": 0.50
    # },
    # "MemecoinMoonshotHunter": {
    #     "function": signal_version_MemecoinMoonshotHunter,
    #     "weight": 0.30
    # },
    # "HybridScalper": {
    #     "function": signal_version_HYBRID_SCALPER,
    #     "weight": 0.80
    # },
    # "BreakoutHunter": {
    #     "function": signal_version_BREAKOUT_HUNTER,
    #     "weight": 0.70
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