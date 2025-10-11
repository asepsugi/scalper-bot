# =============================================================================
# CONFIGURATION
# =============================================================================
import os
from dotenv import load_dotenv

# Muat variabel dari file .env ke environment
load_dotenv()


# Semua parameter strategi dan bot disimpan di sini agar mudah diubah.

CONFIG = {
    "timeframe_trend": "15m",
    "timeframe_signal": "5m",
    "risk_per_trade": 0.01,  # 1% dari balance
    "risk_reward_ratio": 1.5, # RR 1:1.2, lebih realistis untuk scalping
    "fib_levels": [1.618, 1.88, 2.618],
    "buffer_pips": 0.0001,
    "ema_period": 50,
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "atr_period": 14,
    "atr_multiplier": 1.2,
    "atr_multiplier_breakout": 1.0,
    "body_strength_threshold": 0.6,
    "atr_volatility_threshold": 0.0005, # Min volatility: ATR harus > 0.05% dari harga
    "account_balance": 50.0,
    "leverage": 10,
    "sr_lookback": 30,
    "swing_lookback": 60,
    "volume_lookback": 20,
    "min_confluence_filters": 2, # Minimum number of filters that must be true

    # Indicator checklist for the main backtester (generate_vectorized_signals)
    "signal_filters": {
        "rsi_momentum": False,
        "volatility": False,
        "volume": False,
        "adx": True,
        "vwap": False,
        "mta_rsi": True
    },

    # Indicator checklist for strategy B1
    "strategy_b1_indicators": {
        "ema_trend": True,      # EMA 50/200 cross
        "rsi_confirm": True,    # RSI 15m/1h confirmation
        "adx_filter": True,     # ADX > 15
        "atr_exit": True,       # ATR for SL/TP
        "ema9_trigger": True,   # EMA 9 for entry trigger
        "volume_filter": False, # Volume > SMA(20)
        "atr_percentile_filter": True # Hanya trade jika ATR > 40th percentile (7-day lookback)
    }
}

# --- Konfigurasi Live Trading ---
LIVE_TRADING_CONFIG = {
    "max_symbols_to_trade": 50, # Jumlah maksimum simbol yang akan dipantau dan ditradingkan secara live
    "risk_per_trade": 0.005, # Risiko per trade untuk live trading (0.5% dari balance)
    "max_margin_usage_pct": 0.80, # Batas maksimum total margin yang digunakan dari total balance (misal: 0.80 = 80%),
    # --- REVISI: Gunakan rasio untuk ambang batas yang sepenuhnya dinamis ---
    "consensus_ratio": 0.55 # Dibutuhkan 55% dari total bobot skor untuk mencapai konsensus.
}

# Biaya dan Slippage
FEES = {
  "maker": 0.0002,      # Biaya untuk limit order (fraksi)
  "taker": 0.0005,      # REVISI: Biaya taker standar Binance Futures (0.05%)
}

SLIPPAGE = {
  "fixed": 0.0,         # Slippage absolut dalam unit harga (misal: $0.5)
  "pct": 0.0003         # Slippage sebagai fraksi dari harga (misal: 0.0003 = 0.03%)
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
    # Koin Volatilitas Tinggi -> Leverage Rendah
    # "1000PEPE/USDT": 8,
    # "1000SHIB/USDT": 10,
    # "DOGE/USDT": 10,
    # Koin Stabil -> Leverage Lebih Tinggi
    # "BTC/USDT": 20,
    # "ETH/USDT": 20,
    # Default untuk semua koin lain
    "DEFAULT": 20
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
