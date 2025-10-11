import ccxt
from rich.console import Console

# --- PERBAIKAN: Impor API_KEYS dari config ---
from config import API_KEYS

console = Console()

def get_dynamic_risk_params(total_balance: float) -> dict:
    """
    Menentukan parameter risiko dinamis berdasarkan total balance akun.
    Mengembalikan dictionary berisi risk_per_trade, max_active_positions, dan default_leverage.
    """
    if total_balance < 25:  # Tier $10
        return {
            "risk_per_trade": 0.005,   # 0.5%
            "max_active_positions": 1,
            "default_leverage": 15
        }

    elif total_balance < 50:  # Tier $25
        return {
            "risk_per_trade": 0.0075,  # 0.75%
            "max_active_positions": 2,
            "default_leverage": 25
        }

    elif total_balance < 250:  # Tier $50–$249
        return {
            "risk_per_trade": 0.005,   # 0.5%
            "max_active_positions": 3,
            "default_leverage": 20
        }

    elif total_balance < 1000:  # Tier $250–$999 (growth → preservation)
        return {
            "risk_per_trade": 0.004,   # 0.4%
            "max_active_positions": 5,
            "default_leverage": 15
        }

    else:  # Tier $1000+ (capital preservation phase)
        return {
            "risk_per_trade": 0.003,   # 0.3%
            "max_active_positions": 4,
            "default_leverage": 10
        }


def get_all_futures_symbols():
    """Fetches all USDT perpetual futures symbols from Binance."""
    try:
        binance_sync = ccxt.binance({
            'apiKey': API_KEYS['live']['api_key'],
            'secret': API_KEYS['live']['api_secret'],
            'options': {'defaultType': 'future'},
            'test': False,
            'enableRateLimit': True,
        })
        binance_sync.set_sandbox_mode(False)
        markets = binance_sync.load_markets()
        tickers = binance_sync.fetch_tickers()

        min_volume_usd = 50_000_000

        symbols_with_volume = [
            (m['id'].replace(':USDT', ''), tickers.get(m['symbol'], {}).get('quoteVolume', 0))
            for s, m in markets.items()
            if m.get('type') == 'swap'
            and m.get('settle') == 'USDT'
            and m.get('active', True)
            and (tickers.get(m['symbol'], {}).get('quoteVolume', 0) > min_volume_usd if tickers.get(m['symbol']) else False)
        ]

        sorted_symbols_by_volume = sorted(symbols_with_volume, key=lambda item: item[1], reverse=True)
        final_symbols = [symbol for symbol, volume in sorted_symbols_by_volume]

        console.log(f"Found {len(final_symbols)} active USDT perpetual symbols with volume > ${min_volume_usd/1_000_000:.0f}M. Disortir berdasarkan volume.")
        return final_symbols
    except (ccxt.NetworkError, ccxt.ExchangeError, ccxt.BadSymbol) as e:
        console.log(f"[bold red]Error fetching symbols from Binance:[/bold red] {e}")
        return []
