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
            "risk_per_trade": 0.01,   # 1% (risiko lebih tinggi untuk akun sangat kecil)
            "max_active_positions": 1,
            "default_leverage": 15
        }

    elif total_balance < 50:  # Tier $25
        return {
            "risk_per_trade": 0.01,  # 1%
            "max_active_positions": 2,
            "default_leverage": 25
        }

    elif total_balance < 250:  # Tier $50–$249
        return {
            "risk_per_trade": 0.005,   # 0.5% (Sesuai permintaan)
            "max_active_positions": 2, # REVISI: Batasi maksimal 2 posisi
            "default_leverage": 20
        }

    elif total_balance < 1000:  # Tier $250–$999 (growth → preservation)
        return {
            "risk_per_trade": 0.004,   # 0.4%
            "max_active_positions": 2, # REVISI: Batasi maksimal 2 posisi
            "default_leverage": 15
        }

    else:  # Tier $1000+ (capital preservation phase)
        return {
            "risk_per_trade": 0.003,   # 0.3%
            "max_active_positions": 2, # REVISI: Batasi maksimal 2 posisi
            "default_leverage": 10
        }


async def get_all_futures_symbols(exchange: ccxt.Exchange):
    """Fetches all USDT perpetual futures symbols from Binance using the provided exchange instance."""
    try:
        markets = await exchange.load_markets()
        tickers = await exchange.fetch_tickers()

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
