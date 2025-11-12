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
    
    # CRITICAL FIX: Your RR was too ambitious for scalping
    "risk_reward_ratio": 1.8,  # DOWN from 2.4 (more realistic)
    
    "fib_levels": [1.618, 1.88, 2.618],
    "buffer_pips": 0.0001,
    
    # Indicator periods (optimized for 5m/15m scalping)
    "ema_period": 50,
    "rsi_period": 14,
    "rsi_oversold": 35,  # Slightly less extreme
    "rsi_overbought": 65,
    
    # CRITICAL FIX: Tighter ATR for scalping
    "atr_period": 10,  # DOWN from 14 (faster response)
    "atr_multiplier": 1.0,  # DOWN from 1.2 (tighter stops)
    "atr_multiplier_breakout": 0.8,  # Even tighter for breakouts
    
    "body_strength_threshold": 0.6,
    "atr_volatility_threshold": 0.0005,
    "account_balance": 50.0,
    "leverage": 10,
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

    # Strategy B1 - Simplified parameters
    "strategy_b1_regime_filter": {
        "adx_trending_threshold": 22,  # Slightly lower
        "adx_ranging_threshold": 18,
        "atr_delta_volatile_threshold": 1.5,
        "rsi_trending_long": 52,  # Closer to 50 (less extreme)
        "rsi_trending_short": 48,
        "sl_multiplier": 1.5,  # Loosened
        "rr_ratio": 2.0        # Increased
    },
    
    # NEW: Essential filters for scalping profitability
    "trade_filters": {
        "avoid_hours_utc": [22, 23, 0, 1, 2],  # Extended (Asian session start)
        "max_atr_delta_spike": 2.5,
        "min_pivot_distance_atr": 0.3,  # Closer to levels
        "min_volatility_atr_percentile": 0.25,  # Lower threshold
        "max_spread_bps": 2.5  # NEW: Critical for scalping
    },
    
    # Disabled complex filters (keep it simple)
    "smc_filters": {
        "ob_volume_multiplier": 1.2,
        "ob_impulse_atr_multiplier": 2.0,
        "ob_consecutive_candles": 2,
        "allow_contrarian_mode": False
    },
    
    "strategy_f1_silver_bullet": {
        "am_session_utc": [14, 15],
        "pm_session_utc": [18, 19],
        "lookback_period": 30
    }
}

LIVE_TRADING_CONFIG = {
    "max_symbols_to_trade": 30,  # DOWN from 50 (less is more focused)
    
    # CRITICAL FIX: Match the per-trade risk
    "risk_per_trade": 0.003,  # DOWN from 0.005
    
    "max_margin_usage_pct": 0.60,  # DOWN from 0.80 (more conservative)
    
    # CRITICAL FIX: Require stronger consensus
    "consensus_ratio": 0.70,  # UP from 0.55 (fewer but better signals)
    
    # Circuit breaker - Tightened
    "circuit_breaker_multiplier": 1.3,  # DOWN from 1.5 (exit sooner)
    
    # Trailing stop - More aggressive
    "trailing_sl_enabled": True,
    "trailing_sl_trigger_rr": 0.8,  # DOWN from 1.0 (start earlier)
    "trailing_sl_distance_atr": 1.0,  # DOWN from 1.5 (tighter trail)
    "trailing_sl_check_interval": 2,  # More frequent checks
    
    # CRITICAL: Keep advanced exit logic ON
    "use_advanced_exit_logic": True,
    
    # NEW: Prevent revenge trading
    "trade_cooldown_minutes": 30,  # NEW: Wait 30min after loss on same symbol
    
    # NEW: Daily loss limit (stop trading for the day)
    "max_daily_loss_pct": 0.05,  # Stop at -5% daily loss
    
    # NEW: Position sizing adjustments
    "scale_down_on_loss_streak": True,  # Reduce size after 2 losses
    "scale_up_on_win_streak": True,     # Increase after 3 wins (max 1.5x)
    "max_position_scale": 1.5
}

# Biaya dan Slippage
FEES = {
  "maker": 0.0002,      # Biaya untuk limit order (fraksi)
  "taker": 0.0005,      # REVISI: Biaya taker standar Binance Futures (0.05%)
}

SLIPPAGE = {
  "fixed": 0.0,         # Slippage absolut dalam unit harga (misal: $0.5)
  "pct": 0.0005         # Slippage sebagai fraksi dari harga (misal: 0.0003 = 0.03%)
}

# Metadata Kontrak Futures
CONTRACT = {
  "symbol": "BTCUSDT",
  "contract_size": 0.001,  # Setiap kontrak merepresentasikan 0.001 BTC
  "point_value": 1.0,      # Nilai per 1 poin pergerakan harga per 1 kontrak (dalam quote currency)
}

# Konfigurasi Eksekusi (Partial TP & Trailing Stop)
EXECUTION = {
  "partial_tps": [
      # (fraksi_posisi, rr_multiplier)
      (0.5, 1.0), # Tutup 50% posisi pada 1:1 RR
      (0.5, 2.0)  # Tutup 50% sisa posisi pada 1:2 RR
  ],
  "trailing": {
     "enabled": True,
     "trigger_rr": 1.5,    # Mulai trailing saat harga mencapai 1.5x RR
     "trail_dist_rr": 0.5, # Jarak trailing stop adalah 0.5x RR dari harga saat ini
  }
}

# --- REVISI: Leverage Dinamis per Simbol ---
# Tentukan leverage spesifik untuk simbol tertentu.
# Gunakan 'DEFAULT' untuk semua simbol lain yang tidak terdaftar.
LEVERAGE_MAP = {
    # High volatility coins - Lower leverage
    "1000PEPE/USDT": 5,
    "1000SHIB/USDT": 5,
    "DOGE/USDT": 8,
    
    # Stable coins - Moderate leverage
    "BTC/USDT": 10,  # DOWN from 20
    "ETH/USDT": 10,  # DOWN from 20
    
    # DEFAULT - Conservative
    "DEFAULT": 8  # DOWN from 20 (much safer)
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
