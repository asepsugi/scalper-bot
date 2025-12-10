# =============================================================================
# CONFIGURATION
# =============================================================================
import os
from dotenv import load_dotenv

# Muat variabel dari file .env ke environment
load_dotenv()


# Semua parameter strategi dan bot disimpan di sini agar mudah diubah.

# CORE STRATEGY PARAMETERS - OPTIMIZED
CONFIG = {
    "timeframe_trend": "15m",
    "timeframe_signal": "5m",

    "fib_levels": [1.618, 1.88, 2.618],
    "buffer_pips": 0.0001,
    
    # Indicator periods (optimized for 5m/15m scalping)
    "ema_period": 50,
    "rsi_period": 14,
    "rsi_oversold": 35,  # Slightly less extreme
    "rsi_overbought": 65,
    
    # CRITICAL FIX: Tighter ATR for scalping
    "atr_period": 20,  # PERBAIKAN: Naikkan periode ATR untuk baseline volatilitas yang lebih stabil
    
    "body_strength_threshold": 0.6,
    "atr_volatility_threshold": 0.0005,
    "account_balance": 75.0,
    "sr_lookback": 30,
    "swing_lookback": 60,
    "volume_lookback": 20,
    "min_confluence_filters": 2,

    "signal_filters": {
        "rsi_momentum": True,  # Re-enabled
        "volatility": True,    # Re-enabled
        "volume": True,        # Re-enabled (CRITICAL)
        "adx": True,
        "vwap": False,
        "mta_rsi": True
    },

    # =========================================================================
    # NEW: TWEAKABLE STRATEGY PARAMETERS
    # =========================================================================
    "strategy_params": {
        "A3": {
            "risk_per_trade": 0.01, # Risiko 1% untuk strategi ini
            # PERBAIKAN: Beri ruang lebih untuk SL agar tidak kena noise
            "sl_base_multiplier": 2.2,
            "sl_atr_pct_scaler": 0.3,
            "rr_ratio": 1.8,
            "volume_ratio": 0.9,
            "adx_threshold": 14, # PERBAIKAN: Longgarkan sedikit lagi
            "not_overextended_pct": 0.015, # PERBAIKAN: Longgarkan filter, 0.05% terlalu ketat. Sekarang 1.5%
            "volatility_median_window": 50,
            "wick_filter_atr_multiplier": 2.0, # Filter candle sumbu panjang
            "use_or_logic_for_filters": True, # ADX OR wick OK → sinyal lewat
            "enable_wick_filter": True, 
            "debug_mode": False  # Log kenapa sinyal None (e.g., "Skipped: ADX=17 < 18")
        },
        "B1": {
            "risk_per_trade": 0.008, # Risiko 0.8% untuk strategi ini
            "adx_trending_threshold": 15, # PERBAIKAN: Longgarkan dan selaraskan
            "adx_ranging_threshold": 22, # Aktifkan kembali untuk ranging mode
            "atr_delta_volatile_threshold": 1.5,
            "rsi_trending_long": 50, 
            "rsi_trending_short": 50,
            # PERBAIKAN: Beri ruang lebih untuk SL agar tidak kena noise
            "sl_base_multiplier": 2.2,
            "sl_atr_pct_scaler": 0.3,
            "rr_ratio": 2.0,
            "volume_ratio": 1.05,
            "volatility_median_window": 100,
            "wick_filter_atr_multiplier": 2.0, # Filter candle sumbu panjang
            "volume_ma_multiplier": 1.0, # Trade kalau vol > 1.0x MA20
            "atr_ma_multiplier": 1.1, # Trade kalau ATR > 1.1x MA20
            "use_or_logic_for_filters": True, # ADX OR wick OK → sinyal lewat
            "enable_wick_filter": True, 
            "debug_mode": False  # Log kenapa sinyal None
        },
        "AltcoinVolumeBreakoutHunter": {
            "risk_per_trade": 0.025, # Risiko 2.5% untuk strategi breakout yang lebih agresif
            # --- REKOMENDASI OPTIMASI ---
            "breakout_window": 12,
            "volume_spike_multiplier": 4.0, # 3.5-4.0x, kita ambil tengah
            "candle_body_ratio": 0.58,
            "anti_chase_pct": 0.08, # Maksimal naik 8%
            # --- BARU: Filter ADX yang dapat dikonfigurasi ---
            "adx_veto_threshold": 18, # Filter momentum dump, hindari sideways chop
            "sl_multiplier": 2.9,
            "trailing_trigger_rr": 2.2,
            "trailing_distance_atr": 3.2,
            "enable_ema_filter": True,
            "symbol_blacklist": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT", "ZECUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT"],
            # --- PILAR 1: MARKET REGIME FILTER ---
            "enable_regime_filter": True,
            "regime_adx_threshold": 19,
            "regime_atr_pct_threshold": 0.0085 # 0.85%
        },
        "MemecoinMoonshotHunter": {
            "risk_per_trade": 0.015, # Risiko lebih tinggi untuk potensi moonshot
            "volume_spike_multiplier": 5, # 4.5-5.5x, kita ambil tengah-atas
            "rsi_threshold": 70,
            "breakout_window": 14,
            "anti_chase_pct_limit": 0.25, # Maksimal naik 18%
            "anti_chase_window": 10,
            "sl_multiplier": 2.4,
            "trailing_trigger_rr": 3.0,
            "trailing_distance_atr": 3.5, # type: ignore
            "symbol_whitelist": ["PEPEUSDT", "WIFUSDT", "BONKUSDT", "FLOKIUSDT", "MEMEUSDT", "ORDIUSDT", "SATSUSDT"] # Fokus pada memecoin
        },
        "LongOnlyCorrectionHunter": {
            "risk_per_trade": 0.009, # Risiko standar
            # --- PERBAIKAN BERDASARKAN ANALISIS ---
            "volume_spike_multiplier": 2.5, # Untuk konfirmasi entry (vs MA20)
            "sl_multiplier": 2.2,
            "bb_period": 20, # Periode Bollinger Bands
            "bb_std_dev": 1.8, # Dibuat lebih sensitif (dari 2.0 ke 1.8)
            
            # --- BARU: Parameter Auto-Deteksi Dump Keras (Pre-Filter) ---
            "dump_ath30d_threshold": 0.65,   # close < 65% dari ATH 30 hari (dump >35%)
            "dump_ath7d_threshold": 0.78,    # close < 78% dari ATH 7 hari (dump >22%)
            "dump_vol_ma_multiplier": 2.8,   # Volume > 2.8x MA volume 30 hari
            "dump_rsi_threshold": 45,        # RSI < 45 (konfirmasi momentum bearish)
            "dump_adx_threshold": 22,        # ADX > 22 (konfirmasi tren bearish kuat)
            # -------------------------------------------------------------
            
            # --- Exit Strategy ---
            "partial_tps": [
                (4.0, 0.50), # Jual 50% di 4R
                (8.0, 0.30)  # Jual 30% di 8R
            ],
            "trailing_trigger_rr": 3.0 # Mulai trailing setelah 3R
        }
    },

    # NEW: Essential filters for scalping profitability
    "trade_filters": {
        # Hanya parameter ini yang masih digunakan di data_preparer.py
        "min_volatility_atr_percentile": 0.25
    },
    
    # Disabled complex filters (keep it simple)
    "smc_filters": {
        "ob_volume_multiplier": 1.2,
        "ob_impulse_atr_multiplier": 2.0,
        "ob_consecutive_candles": 2,
        "allow_contrarian_mode": False
    }
}

# ============================================================================
# NEW: DYNAMIC ENTRY LOGIC CONFIGURATION
# ============================================================================
ENTRY_LOGIC = {
    "enabled": True, # Aktifkan/nonaktifkan seluruh logika ini

    # --- Kondisi Deteksi ---
    "continuation_adx_threshold": 20, # PERBAIKAN: Turunkan ambang batas agar profil continuation lebih sering aktif.
    "continuation_volume_spike_ratio": 1.5, # Volume > 1.5x rata-rata
    "pullback_rsi_overbought": 70,
    "pullback_rsi_oversold": 30,
    "pullback_macd_hist_shrink_pct": 0.20, # Hist MACD mengecil 20% dari puncaknya
    "pullback_bb_retrace_pct": 0.002, # PERBAIKAN: Harga cukup retrace 0.2% dari band luar, membuatnya lebih sensitif

    # --- Parameter Eksekusi ---
    "continuation_offset_pct": 0.0001, # Offset positif kecil untuk mengejar harga
    "pullback_offset_pct": -0.0015,    # Offset negatif untuk menunggu pullback
    "default_offset_pct": 0.0,         # Tempatkan limit order tepat di harga sinyal

    # --- Parameter Risiko Dinamis ---
    "continuation_risk_multiplier": 0.75, # Gunakan 75% dari risiko dasar strategi
    "pullback_risk_multiplier": 1.25,     # Gunakan 125% dari risiko dasar strategi

    "market_order_adx_threshold": 28 # PERBAIKAN: Hanya gunakan market order jika tren SANGAT kuat (ADX > 28)
}

LIVE_TRADING_CONFIG = {
    "max_symbols_to_trade": 20,  # DOWN from 30 (Symbol & Data Focus)
    
    "max_margin_usage_pct": 0.60,  # DOWN from 0.80 (more conservative)
    
    # CRITICAL FIX: Require stronger consensus
    "consensus_ratio": 0.01,  # DOWN from 0.75 (Longgarkan untuk lebih banyak trade)
    
    # Circuit breaker - Tightened
    "circuit_breaker_multiplier": 1.3,  # DOWN from 1.5 (exit sooner)
    
    # CRITICAL: Keep advanced exit logic ON
    # Logika exit canggih (termasuk trailing stop) sekarang dikontrol oleh blok EXECUTION
    "use_advanced_exit_logic": True,
    
    # NEW: Prevent revenge trading (dipercepat)
    "trade_cooldown_seconds": 120, # DOWN from 45min (2700s)
    
    # NEW: Daily loss limit (stop trading for the day)
    "max_daily_loss_pct": 0.05,  # Stop at -5% daily loss
    
    # NEW: Drawdown circuit breaker
    "drawdown_circuit_breaker": {
        "enabled": True,
        "trigger_pct": 0.10,  # Trigger at 10% drawdown from the last peak
        "cooldown_hours": [2, 6, 24] # Cooldown hours for 1st, 2nd, and subsequent triggers
    },
    # --- PILAR 3: WEEKLY PERFORMANCE KILLSWITCH ---
    "weekly_killswitch": {
        "enabled": True,
        "max_weekly_loss_pct": -0.08, # -8.0%
        "pause_duration_hours": 72, # 3 hari
        "reactivate_adx_threshold": 20,
        "reactivate_atr_pct_threshold": 0.0090 # 0.9%
    },

    # NEW: Position sizing adjustments
    "scale_down_on_loss_streak": True,  # Reduce size after 2 losses
    "scale_up_on_win_streak": True,     # Increase after 3 wins (max 1.5x)
    "max_position_scale": 1.5,

    # NEW: Daily trade limit
    "max_trades_per_day": 20 # Batasi jumlah trade per hari
}

# ============================================================================
# NEW: DYNAMIC WHITELIST ROTATION CONFIG (PILAR 2)
# ============================================================================
WHITELIST_ROTATION_CONFIG = {
    "enabled": True,
    "update_interval_hours": 24 * 7, # Perbarui setiap 7 hari (168 jam)
    "top_n_coins": 20, # Ambil Top 18-22 koin
    "exclude_top_market_cap": 10, # Exclude Top 10
    "max_drawdown_from_ath_pct": 0.35 # Exclude koin yang turun >35% dari ATH 30 hari
}

# ============================================================================
# NEW: BACKTEST REALISM CONFIG
# ============================================================================
BACKTEST_REALISM_CONFIG = {
    "min_fill_probability": 0.75,  # Peluang terisi minimal jika harga hanya menyentuh limit
    "volume_factor_multiplier": 0.2 # Seberapa besar pengaruh volume (lebih kecil = pengaruh lebih besar)
}

# ============================================================================
# NEW: CACHE CONFIGURATION
# ============================================================================
CACHE_CONFIG = {
    "enabled": True,
    "expiration_hours": 24  # Invalidate cache files older than 24 hours
}

# Biaya dan Slippage
FEES = {
  "maker": 0.0002,      # Biaya untuk limit order (fraksi)
  "taker": 0.0005,      # REVISI: Biaya taker standar Binance Futures (0.05%)
}

SLIPPAGE = {
  "fixed": 0.0,         # Slippage absolut dalam unit harga (misal: $0.5)
  "pct": 0.001         # Slippage sebagai fraksi dari harga (misal: 0.0003 = 0.03%)
}

# Konfigurasi Eksekusi (Partial TP & Trailing Stop)
EXECUTION = {
    "entry_order_type": "limit", # "limit" atau "market"
    "limit_order_offset_pct": 0.0005, # Offset untuk limit order (positif = sedikit mengejar harga)
    "limit_order_expiration_candles": 15, # PERBAIKAN: Beri waktu 75 menit (15 candle * 5m) agar order lebih mungkin terisi
    "partial_tps": [
        (5.0, 0.5),   # 50% baru keluar di 5 RR
        (10.0, 0.3),  # 30% di 10 RR
    ],
    "trailing": {
        "enabled": True,
        "trigger_rr": 1.8,
        "distance_atr": 1.5,        # Sangat longgar, biar rider beneran ride
        "check_interval_seconds": 5
    }
}

# --- REVISI: Leverage Dinamis per Simbol ---
# Tentukan leverage spesifik untuk simbol tertentu.
# Gunakan 'DEFAULT' untuk semua simbol lain yang tidak terdaftar.
LEVERAGE_MAP = {
    # Stable coins - Moderate leverage
    "BTC/USDT": 10,
    "ETH/USDT": 10,
    
    # DEFAULT - Conservative
    "DEFAULT": 10  # Capped at 10x (Risk & Cooldown Enhance)
}

# ============================================================================
# NEW: PERFORMANCE TRACKING CONFIG
# ============================================================================
PERFORMANCE_TRACKING = {
    # Enable daily performance reporting
    "daily_report_enabled": True,
    "daily_report_time_utc": "00:00",  # Midnight UTC
    
    # Strategy performance monitoring
    "track_strategy_performance": True,
    "disable_underperforming": True,  # Auto-disable if PF < 0.9 over 50 trades
    "min_trades_for_evaluation": 50,
    
    # Correlation tracking
    "track_position_correlation": True,
    "max_correlated_pairs": 2,  # Don't hold more than 2 highly correlated positions
    "correlation_threshold": 0.7
}

# ============================================================================
# INDICATORS CONFIG UPDATE - Add SuperTrend with proper parameters
# ============================================================================
INDICATOR_PARAMS = {
    # For strategies that use SuperTrend
    "supertrend_periods": [
        {"length": 10, "multiplier": 3.0},  # For 15m timeframe
        {"length": 7, "multiplier": 2.5},   # Alternative
    ],
    
    # Volume analysis
    "volume_sma_periods": [20, 50],  # Multiple lookbacks
    
    # ATR percentiles for volatility regime
    "atr_lookback_for_percentile": 288,  # 24 hours of 5m candles
}

# --- Kredensial API ---
# JANGAN PERNAH MEMASUKKAN KREDENSIAL ASLI LANGSUNG DI SINI UNTUK PRODUKSI
# Gunakan environment variables atau secret manager
API_KEYS = {
    "testnet": {
        "api_key": os.getenv("TESTNET_API_KEY"),
        "api_secret": os.getenv("TESTNET_API_SECRET")
    },
    "live": {
        "api_key": os.getenv("LIVE_API_KEY"),
        "api_secret": os.getenv("LIVE_API_SECRET")
    }
}

# --- Konfigurasi Notifikasi Telegram ---
TELEGRAM = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID") # Bisa berupa ID user atau grup
}
