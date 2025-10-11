from config import CONFIG
from indicators import (
    fetch_binance_data,
    calculate_indicators,
    get_trend,
    find_support_resistance,
    rsi_signal,
    stochastic_signal,
    macd_slope,
    breakout_check,
    is_bullish,
    is_bearish,
    body_strength,
    atr_stoploss,
    calculate_fibonacci_extension
)

# =============================================================================
# EXECUTION & LOGGING (PLACEHOLDERS)
# =============================================================================

def execute_order(order_type, entry, stop_loss, take_profits, position_size):
    """Placeholder for order execution. Replace with your exchange's API call."""
    print("\n" + "="*20 + "\n🚀 EXECUTING ORDER 🚀")
    print(f"  - Type: {order_type}\n  - Entry Price: {entry:.5f}")
    print(f"  - Position Size: {position_size:.4f}\n  - Stop Loss: {stop_loss:.5f}")
    print(f"  - Take Profits: {[f'{tp:.5f}' for tp in take_profits]}")
    print("="*20 + "\n")

def log_trade(details):
    """Placeholder for logging. Replace with logging to a file or database."""
    print(f"📝 LOGGING TRADE: {details}")

def update_position_status():
    """Placeholder for monitoring active positions."""
    pass

# =============================================================================
# MAIN TRADING LOOP
# =============================================================================

def run_strategy(df_signal, df_trend):
    """
    Fungsi utama yang menjalankan strategi untuk setiap candle baru.
    """
    # Buat salinan agar tidak mengubah data asli
    try:
        df_signal_processed = df_signal.copy()
        df_trend_processed = df_trend.copy()

        # Step 0: Hitung semua indikator yang dibutuhkan
        df_signal_processed = calculate_indicators(df_signal_processed)
        df_trend_processed.ta.ema(length=CONFIG["ema_period"], append=True) # Hanya butuh EMA untuk tren

        # Validasi bahwa kolom EMA berhasil dibuat
        if f"EMA_{CONFIG['ema_period']}" not in df_trend_processed.columns:
            # print(f"Warning: Gagal menghitung EMA_{CONFIG['ema_period']} untuk timeframe tren. Melewati candle ini.")
            return

        print(f"\n--- Analyzing new candle at {df_signal_processed.index[-1]} ---")
        
        # Step 1: Market Context
        trend = get_trend(df_trend_processed, CONFIG["ema_period"])
        resistance, support = find_support_resistance(df_signal_processed, lookback=CONFIG["sr_lookback"])
        print(f"Market Context: Trend is {trend}, Support: {support:.5f}, Resistance: {resistance:.5f}")

        # Ambil candle terakhir dari data sinyal
        latest_candle = df_signal_processed.iloc[-1]

        # Step 2: Generate Signals
        rsi_trigger = rsi_signal(df_signal_processed, CONFIG["rsi_period"], CONFIG["rsi_oversold"], CONFIG["rsi_overbought"])
        stoch_trigger = stochastic_signal(df_signal_processed)
        macd_trigger = macd_slope(df_signal_processed)
        breakout_trigger = breakout_check(latest_candle, resistance, support, df_signal_processed, volume_lookback=CONFIG["volume_lookback"])
        
        print(f"Triggers: RSI={rsi_trigger}, Stoch={stoch_trigger}, MACD={macd_trigger}, Breakout={breakout_trigger}")

        # ===========================
        # LONG SETUPS
        # ===========================
        if trend == "UPTREND":
            # (A) Strong Long (Momentum)
            if rsi_trigger == "LONG" or stoch_trigger == "LONG" or macd_trigger == "LONG":
                signal = "STRONG LONG"
                entry = latest_candle['close']
                stop_loss = atr_stoploss(entry, "LONG", df_signal_processed, CONFIG["atr_period"], CONFIG["atr_multiplier"])
                _, last_swing_high = find_support_resistance(df_signal_processed, CONFIG["swing_lookback"])
                fib_targets = calculate_fibonacci_extension(last_swing_high, support, "UPTREND")
                position_size = (CONFIG["account_balance"] * CONFIG["risk_per_trade"]) / abs(entry - stop_loss)
                
                execute_order("BUY", entry, stop_loss, fib_targets, position_size)
                log_trade({"signal": signal, "entry": entry, "sl": stop_loss, "tp": fib_targets})
                return

            # (B) Breakout Long
            if breakout_trigger == "BREAKOUT_LONG":
                signal = "BREAKOUT LONG"
                entry = latest_candle['close']
                stop_loss = atr_stoploss(entry, "LONG", df_signal_processed, CONFIG["atr_period"], CONFIG["atr_multiplier_breakout"])
                tp = entry + (entry - stop_loss) * CONFIG["risk_reward_ratio"]
                position_size = (CONFIG["account_balance"] * CONFIG["risk_per_trade"]) / abs(entry - stop_loss)
                
                execute_order("BUY", entry, stop_loss, [tp], position_size)
                log_trade({"signal": signal, "entry": entry, "sl": stop_loss, "tp": [tp]})
                return

            # (C) Dominan Break Bullish
            if is_bullish(latest_candle) and latest_candle['close'] > support and body_strength(latest_candle) > CONFIG["body_strength_threshold"]:
                signal = "Dominan Break Bullish"
                entry = latest_candle['close']
                stop_loss = latest_candle['low'] - CONFIG["buffer_pips"]
                tp = entry + (entry - stop_loss) * CONFIG["risk_reward_ratio"]
                position_size = (CONFIG["account_balance"] * CONFIG["risk_per_trade"]) / abs(entry - stop_loss)
                
                execute_order("BUY", entry, stop_loss, [tp], position_size)
                log_trade({"signal": signal, "entry": entry, "sl": stop_loss, "tp": [tp]})
                return

        # ===========================
        # SHORT SETUPS
        # ===========================
        if trend == "DOWNTREND":
            # (D) Strong Short
            if rsi_trigger == "SHORT" or stoch_trigger == "SHORT" or macd_trigger == "SHORT":
                signal = "STRONG SHORT"
                entry = latest_candle['close']
                stop_loss = atr_stoploss(entry, "SHORT", df_signal_processed, CONFIG["atr_period"], CONFIG["atr_multiplier"])
                last_swing_low, _ = find_support_resistance(df_signal_processed, CONFIG["swing_lookback"])
                fib_targets = calculate_fibonacci_extension(resistance, last_swing_low, "DOWNTREND")
                position_size = (CONFIG["account_balance"] * CONFIG["risk_per_trade"]) / abs(entry - stop_loss)
                
                execute_order("SELL", entry, stop_loss, fib_targets, position_size)
                log_trade({"signal": signal, "entry": entry, "sl": stop_loss, "tp": fib_targets})
                return

            # (E) Breakout Short
            if breakout_trigger == "BREAKOUT_SHORT":
                signal = "BREAKOUT SHORT"
                entry = latest_candle['close']
                stop_loss = atr_stoploss(entry, "SHORT", df_signal_processed, CONFIG["atr_period"], CONFIG["atr_multiplier_breakout"])
                tp = entry - (stop_loss - entry) * CONFIG["risk_reward_ratio"]
                position_size = (CONFIG["account_balance"] * CONFIG["risk_per_trade"]) / abs(entry - stop_loss)
                
                execute_order("SELL", entry, stop_loss, [tp], position_size)
                log_trade({"signal": signal, "entry": entry, "sl": stop_loss, "tp": [tp]})
                return
                
            # (F) Dominan Break Bearish
            if is_bearish(latest_candle) and latest_candle['close'] < resistance and body_strength(latest_candle) > CONFIG["body_strength_threshold"]:
                signal = "Dominan Break Bearish"
                entry = latest_candle['close']
                stop_loss = latest_candle['high'] + CONFIG["buffer_pips"]
                last_swing_low, _ = find_support_resistance(df_signal_processed, CONFIG["swing_lookback"])
                fib_targets = calculate_fibonacci_extension(resistance, last_swing_low, "DOWNTREND")
                position_size = (CONFIG["account_balance"] * CONFIG["risk_per_trade"]) / abs(entry - stop_loss)
                
                execute_order("SELL", entry, stop_loss, fib_targets, position_size)
                log_trade({"signal": signal, "entry": entry, "sl": stop_loss, "tp": fib_targets})
                return

        # ===========================
        # Position Monitoring
        # ===========================
        update_position_status()
    except Exception as e:
        print(f"ERROR dalam run_strategy: {e}")
        # Optionally, you can add more detailed error logging here
        # import traceback
        # traceback.print_exc()

# =============================================================================
# MAIN EXECUTION (FOR LIVE/SINGLE ANALYSIS)
# =============================================================================
if __name__ == "__main__":
    # This block demonstrates how you would run the strategy for a single, live analysis.
    # In a real bot, this would be inside a loop that runs every 5 minutes.
    import asyncio
    SYMBOL = 'BTC/USDT'
    print(f"--- Performing single analysis for {SYMBOL} ---")

    # --- PERBAIKAN KONSISTENSI ---
    import ccxt
    from config import API_KEYS
    exchange = ccxt.binance({
        'apiKey': API_KEYS['live']['api_key'],
        'secret': API_KEYS['live']['api_secret'],
        'options': {'defaultType': 'future'},
        'enableRateLimit': True,
        'test': False,
    })
    exchange.set_sandbox_mode(False)

    # Fetch the latest historical data needed for indicators
    df_signal_full = asyncio.run(fetch_binance_data(exchange, SYMBOL, CONFIG["timeframe_signal"], limit=200, use_cache=False)) if exchange else None
    df_trend_full = asyncio.run(fetch_binance_data(exchange, SYMBOL, CONFIG["timeframe_trend"], limit=100, use_cache=False)) if exchange else None

    if df_signal_full is None or df_trend_full is None:
        print("Gagal mengambil data, skrip berhenti.")
    else:
        # In a real bot, you would pass the full dataframes.
        # The run_strategy function is designed to work with the latest candle.
        run_strategy(df_signal_full, df_trend_full)
