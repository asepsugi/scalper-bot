# =============================================================================
# CONFIGURATION
# =============================================================================
import os
from dotenv import load_dotenv

# Muat variabel dari file .env ke environment
load_dotenv()


# Semua parameter strategi dan bot disimpan di sini agar mudah diubah.

CONFIG = {
    "timeframe_trend": "15m", # Timeframe untuk konteks tren jangka menengah
    "timeframe_signal": "5m",  # Timeframe utama untuk eksekusi sinyal
    "risk_per_trade": 0.005,  # REVISI: Turunkan risiko per trade menjadi 0.5%
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

    # --- REVISI: Konfigurasi baru untuk SmartRegimeScalper(B1) ---
    # Blok "strategy_b1_indicators" yang lama sudah usang dan dihapus.
    "strategy_b1_regime_filter": {
        "adx_trending_threshold": 23,   # ADX di atas nilai ini dianggap 'Trending'
        "adx_ranging_threshold": 18,    # ADX di bawah nilai ini dianggap 'Ranging'
        "atr_delta_volatile_threshold": 1.5, # ATR_delta di atas ini dianggap 'Volatile' (jangan trade)
        "rsi_trending_long": 55,        # RSI 15m harus > ini saat trending long
        "rsi_trending_short": 45,       # RSI 15m harus < ini saat trending short
        "sl_multiplier": 1.8,           # Pengali ATR untuk Stop Loss
        "rr_ratio": 1.6                 # Rasio Risk/Reward
    }
    ,
    # --- FITUR BARU: Filter Waktu & Volatilitas Global ---
    "trade_filters": {
        "avoid_hours_utc": [22, 23, 0, 1], # Hindari jam-jam ini (misal, sesi NY close & Sydney open)
        "max_atr_delta_spike": 2.5, # Hindari trade jika ATR delta > 2.5 (indikasi news/spike)
        "min_pivot_distance_atr": 0.5, # Jarak minimal dari swing high/low terakhir (dalam kelipatan ATR)
        "min_volatility_atr_percentile": 0.35 # REVISI: Entry hanya jika ATR > persentil ke-35 dari periode rolling
    }
    ,
    # --- FITUR BARU: Filter Lanjutan untuk SMC ---
    "smc_filters": {
        "ob_volume_multiplier": 1.2, # Volume OB atau candle setelahnya harus > 1.2x rata-rata
        "ob_impulse_atr_multiplier": 2.0, # Gerakan impulsif setelah OB harus > 2.0x ATR
        "ob_consecutive_candles": 2, # Butuh 2 candle konsekutif setelah OB untuk konfirmasi impuls
        "allow_contrarian_mode": False # Izinkan entry counter-trend dengan RR lebih tinggi
    },
    # --- FITUR BARU: Konfigurasi untuk Strategi ICT Silver Bullet (F1) ---
    "strategy_f1_silver_bullet": {
        "am_session_utc": [14, 15], # Sesi AM: 10:00-11:00 EST (UTC-4)
        "pm_session_utc": [18, 19], # Sesi PM: 14:00-15:00 EST (UTC-4)
        "lookback_period": 30 # Periode candle untuk mencari swing high/low likuiditas
    }

}

# --- Konfigurasi Live Trading ---
LIVE_TRADING_CONFIG = {
    "max_symbols_to_trade": 50, # Jumlah maksimum simbol yang akan dipantau dan ditradingkan secara live
    "risk_per_trade": 0.005, # Risiko per trade untuk live trading (0.5% dari balance)
    "max_margin_usage_pct": 0.80, # Batas maksimum total margin yang digunakan dari total balance (misal: 0.80 = 80%),
    # --- REVISI: Gunakan rasio untuk ambang batas yang sepenuhnya dinamis ---
    "consensus_ratio": 0.55, # Dibutuhkan 55% dari total bobot skor untuk mencapai konsensus.
    # --- FITUR BARU: Pengaturan Circuit Breaker ---
    "circuit_breaker_multiplier": 1.5, # Keluar jika harga menembus SL sejauh 1.5x jarak SL awal (artinya 50% lebih jauh dari SL).
    # --- FITUR BARU: Pengaturan Trailing Stop Loss ---
    "trailing_sl_enabled": True, # Aktifkan/nonaktifkan Trailing SL
    "trailing_sl_trigger_rr": 1.0, # Mulai trailing saat trade mencapai 1.0x Risk/Reward
    "trailing_sl_distance_atr": 1.5, # Jarak trailing stop dari harga saat ini (dalam kelipatan ATR)
    "trailing_sl_check_interval": 3, # Seberapa sering (dalam detik) untuk memeriksa & memperbarui trailing SL
    # --- FITUR BARU: Pilihan Strategi Exit & Cooldown ---
    "use_advanced_exit_logic": True, # True: Gunakan SL/TP manual, circuit breaker, trailing. False: Gunakan SL/TP statis dari bursa.
    "trade_cooldown_minutes": 60 # Waktu tunggu (dalam menit) sebelum membuka trade baru pada simbol yang sama.
}

# Biaya dan Slippage
FEES = {
  "maker": 0.0003,      # Biaya untuk limit order (fraksi)
  "taker": 0.0007,      # REVISI: Biaya taker standar Binance Futures (0.05%)
}

SLIPPAGE = {
  "fixed": 0.0,         # Slippage absolut dalam unit harga (misal: $0.5)
  "pct": 0.0008         # Slippage sebagai fraksi dari harga (misal: 0.0003 = 0.03%)
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
    # "DEFAULT": 20
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
