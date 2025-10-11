# Binance Futures Multi-Strategy Scalping Bot

This project is a sophisticated, asynchronous scalping bot designed for Binance Futures. It employs a multi-strategy consensus system to generate trading signals across multiple cryptocurrency pairs simultaneously. The bot is built with modularity, security, and performance in mind, utilizing `ccxt.pro` for real-time data via websockets.

## ✨ Key Features

-   **Live & Demo Trading**: Separate, robust scripts for both `live_trader.py` and `demo_trader.py` environments.
-   **Real-time Dashboard**: A terminal-based monitor (`live_trader_monitor.py`) to view account balance, active positions, and event logs for both live and demo environments.
-   **Multi-Strategy Consensus**: Combines signals from multiple trading strategies (`strategies.py`) using a weighted scoring system to improve signal quality.
-   **Dynamic Risk Management**: Automatically adjusts risk per trade, max active positions, and leverage based on account balance tiers (`utils/common_utils.py`).
-   **Asynchronous Architecture**: Built with `asyncio` for high performance, capable of monitoring dozens of symbols concurrently without blocking.
-   **Secure Configuration**: Sensitive API keys and tokens are managed securely using a `.env` file, keeping them out of the source code.
-   **Telegram Notifications**: Instant alerts for bot status (start/stop/crash), new orders, filled positions, and critical errors like IP bans.
-   **Resilience & Error Handling**: Includes robust reconnection logic for websockets and graceful handling of API errors and rate limits.
-   **Backtesting Suite**:
    -   `backtest_market_scanner.py`: Simulates portfolio performance across multiple symbols over a historical period.
    -   `backtest_strategy_comparation.py`: Compares the performance of different strategies on a single symbol.

### 💡 Adding Your Own Strategy

The bot is designed to be modular, making it easy to add your own custom trading strategies. Here’s how:

1.  **Open `strategies.py`**: This file contains all the trading logic.

2.  **Define Your Strategy Function**: Create a new Python function that accepts a pandas DataFrame (`df`) as input. This DataFrame will contain the OHLCV data and all pre-calculated indicators. Your function must return three items:
    -   `long_signals`: A pandas Series of booleans indicating a buy signal.
    -   `short_signals`: A pandas Series of booleans indicating a sell signal.
    -   `exit_params`: A dictionary specifying the Stop Loss (`sl_multiplier`) and Risk-Reward Ratio (`rr_ratio`) for your strategy.

    ```python
    # Example of a new strategy function in strategies.py
    def signal_my_awesome_strategy(df):
        exit_params = {'sl_multiplier': 2.0, 'rr_ratio': 1.5}
        long_condition = (df['rsi_15m'] < 30) & (df['close'] > df['EMA_200'])
        short_condition = (df['rsi_15m'] > 70) & (df['close'] < df['EMA_200'])
        return long_condition, short_condition, exit_params
    ```

3.  **Register Your Strategy**: Scroll to the bottom of `strategies.py` and add your new strategy to the `STRATEGY_CONFIG` dictionary. Give it a unique name, point to the function you just created, and assign it a `weight`. The weight determines its influence in the consensus signal.

    ```python
    # Add your strategy to the dictionary in strategies.py
    "MyAwesomeStrategy": {
        "function": signal_my_awesome_strategy,
        "weight": 1.5 # Give it a higher weight if you trust it more
    }
    ```

4.  **(Optional) Add New Indicators**: If your strategy requires an indicator that isn't already calculated (e.g., Bollinger Bands), you'll need to add its calculation to the `calculate_indicators` function in `indicators.py`.

## 📂 Project Structure

```
.
├── cache/                # Caches historical market data to speed up restarts
├── output/               # Stores logs and position state files
├── utils/                # Utility functions (risk management, data preparation)
├── .env                  # (You create this) Securely stores your API keys and tokens
├── .env.example          # Template for the .env file
├── .gitignore            # Specifies files for Git to ignore
├── backtest_market_scanner.py # Backtester for multi-symbol portfolio simulation
├── BACKTEST_LOG.md       # (You update this) Log for your backtest results
├── backtest_strategy_comparation.py # Backtester to compare strategies
├── config.py             # Main configuration for strategies and bot parameters
├── demo_trader.py        # Main script for running the bot on Binance Testnet
├── indicators.py         # Functions for calculating technical indicators (RSI, EMA, etc.)
├── live_trader.py        # Main script for running the bot in the LIVE environment
├── live_trader_monitor.py# Real-time terminal dashboard
├── main.py               # (Legacy) Single-symbol analysis script
├── requirements.txt      # List of Python dependencies
└── strategies.py         # All trading strategy logic is defined here
```

## 🚀 Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a Virtual Environment**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```
    Activate it:
    -   **Windows**: `.\venv\Scripts\activate`
    -   **macOS/Linux**: `source venv/bin/activate`

3.  **Install Dependencies**
    Install all the required Python libraries from `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Credentials**
    Copy the example environment file and fill in your details.
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your actual Binance API keys (for both live and testnet) and your Telegram bot token/chat ID.

    ```
    # Binance Testnet API Credentials
    TESTNET_API_KEY="YOUR_TESTNET_API_KEY"
    TESTNET_API_SECRET="YOUR_TESTNET_API_SECRET"

    # Binance Live API Credentials
    LIVE_API_KEY="YOUR_LIVE_API_KEY"
    LIVE_API_SECRET="YOUR_LIVE_API_SECRET"

    # Telegram Bot Credentials
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
    ```
    **Security Note**: The `.gitignore` file is already configured to prevent your `.env` file from being committed to Git.

## ⚙️ Usage

Make sure your virtual environment is activated before running any scripts.

### Running the Trading Bots

-   **Run the LIVE Trader:**
    ```bash
    python live_trader.py
    ```

-   **Run the DEMO Trader:**
    ```bash
    python demo_trader.py
    ```

### Running the Monitor

The monitor can be run in a separate terminal window to watch the bot's activity.

-   **Monitor the LIVE Environment:**
    ```bash
    python live_trader_monitor.py --env live
    ```

-   **Monitor the DEMO Environment:**
    ```bash
    python live_trader_monitor.py --env demo
    ```

## 🔧 Configuration

Most of the bot's behavior can be tweaked in `config.py` and `strategies.py`.

-   **`config.py`**:
    -   `CONFIG`: Adjust core indicator parameters like RSI period, EMA lengths, etc.
    -   `LIVE_TRADING_CONFIG`: Set global parameters for the live/demo bots, such as max symbols to trade, risk per trade, and the consensus ratio.
    -   `LEVERAGE_MAP`: Define custom leverage for specific symbols or set a default.

-   **`strategies.py`**:
    -   `STRATEGY_CONFIG`: This dictionary is the control center for your strategies. You can enable/disable strategies by commenting them out, and adjust their `weight` in the consensus scoring.

## ⚠️ Disclaimer

This trading bot is provided for educational and experimental purposes only. Trading cryptocurrencies, especially with leverage, involves substantial risk and may not be suitable for every investor. You are solely responsible for any financial losses. The creators of this software are not liable for any losses incurred. **Do not use this bot with real money unless you fully understand the code and the risks involved.** Always start with `demo_trader.py` to test your strategies.