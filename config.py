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

    # CRITICAL FIX: Your risk was too high for a scalper
    "risk_per_trade": 0.003,  # DOWN from 0.005 (0.3% instead of 0.5%)
    
    "fib_levels": [1.618, 1.88, 2.618],
    "buffer_pips": 0.0001,
    
    # Indicator periods (optimized for 5m/15m scalping)
    "ema_period": 50,
    "rsi_period": 14,
    "rsi_oversold": 35,  # Slightly less extreme
    "rsi_overbought": 65,
    
    # CRITICAL FIX: Tighter ATR for scalping
    "atr_period": 14,  # PERBAIKAN: Naikkan periode ATR untuk baseline volatilitas yang lebih stabil
    
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
            "enable_wick_filter": False,
            "debug_mode": True  # Log kenapa sinyal None (e.g., "Skipped: ADX=17 < 18")
        },
        "B1": {
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
            "enable_wick_filter": False,
            "debug_mode": True  # Log kenapa sinyal None
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
    "continuation_adx_threshold": 15,
    "continuation_volume_spike_ratio": 1.5, # Volume > 1.5x rata-rata
    "pullback_rsi_overbought": 70,
    "pullback_rsi_oversold": 30,
    "pullback_macd_hist_shrink_pct": 0.20, # Hist MACD mengecil 20% dari puncaknya
    "pullback_bb_retrace_pct": 0.005, # Harga harus retrace 0.5% dari band luar

    # --- Parameter Eksekusi ---
    "continuation_offset_pct": 0.001,   # +0.1% (mengejar harga)
    "pullback_offset_pct": -0.0015,     # -0.15% (menunggu pullback)
    "default_offset_pct": 0.0002,       # Offset standar jika tidak terdeteksi

    # --- Parameter Risiko Dinamis ---
    "continuation_risk_pct": 0.002, # Risiko 0.2% untuk entry agresif
    "pullback_risk_pct": 0.004,     # Risiko 0.4% untuk entry pullback

    "market_order_adx_threshold": 18 # Gunakan market order jika ADX > 30 (tren sangat kuat)
}

LIVE_TRADING_CONFIG = {
    "max_symbols_to_trade": 20,  # DOWN from 30 (Symbol & Data Focus)
    
    "max_margin_usage_pct": 0.60,  # DOWN from 0.80 (more conservative)
    
    # CRITICAL FIX: Require stronger consensus
    "consensus_ratio": 0.40,  # DOWN from 0.75 (Longgarkan untuk lebih banyak trade)
    
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
    "max_drawdown_pct": 0.20,  # Stop trading jika drawdown > 20% dari peak
    "drawdown_cooldown_hours": 2, # Pause selama 2 jam setelah drawdown tercapai

    # NEW: Position sizing adjustments
    "scale_down_on_loss_streak": True,  # Reduce size after 2 losses
    "scale_up_on_win_streak": True,     # Increase after 3 wins (max 1.5x)
    "max_position_scale": 1.5,

    # NEW: Daily trade limit
    "max_trades_per_day": 20 # Batasi jumlah trade per hari
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
    "limit_order_expiration_candles": 10, # Setelah berapa candle, order limit di backtest dibatalkan
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
