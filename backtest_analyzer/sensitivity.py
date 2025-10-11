import numpy as np
import pandas as pd
from typing import Dict, Any

from slippage_model import apply_slippage_to_returns
 
 
def run_sensitivity_analysis(
    daily_returns: pd.Series,
    total_trades: int,
    initial_rr: float,
    initial_win_rate: float,
    slippage_max: float,
) -> Dict[str, Any]:
    """
    Menjalankan analisis sensitivitas terhadap R:R, Win Rate, dan Slippage.
 
    Args:
        daily_returns (pd.Series): Series return harian asli.
        total_trades (int): Jumlah total trade.
        initial_rr (float): R:R rata-rata awal.
        initial_win_rate (float): Win rate awal (dalam persen).
        slippage_max (float): Slippage maksimum untuk diuji (misal: 0.01 untuk 1%).
 
    Returns:
        Dict[str, Any]: Hasil analisis sensitivitas.
    """
    results = {}
 
    # 1. Sensitivitas terhadap Slippage
    slippage_range = np.linspace(0, slippage_max, 11)
    slippage_impact = []
    for slip in slippage_range:
        # Terapkan slippage ke return harian
        adjusted_returns = apply_slippage_to_returns(daily_returns, total_trades, slip)
        # Hitung net profit dari equity curve
        final_equity = 10000 * (1 + adjusted_returns).cumprod().iloc[-1]
        net_profit_pct = (final_equity - 10000) / 10000 * 100
        slippage_impact.append(
            {"slippage_pct": slip * 100, "net_profit_pct": net_profit_pct}
        )
 
    results["slippage_analysis"] = pd.DataFrame(slippage_impact)
 
    # 2. Sensitivitas terhadap Win Rate & R:R (Estimasi)
    # Ini adalah model sederhana, analisis riil memerlukan re-backtest
    # Untuk saat ini, kita berikan kesimpulan kualitatif
    # Jika profit factor > 2, sensitivitas winrate cenderung moderate
    # Jika avg_rr > 1.5, sensitivitas R:R cenderung strong positive
 
    # Placeholder untuk kesimpulan kualitatif
    results["summary"] = {
        "winrate_sensitivity": "moderate" if initial_win_rate > 55 else "high",
        "rr_sensitivity": "strong positive" if initial_rr > 1.5 else "moderate positive",
        "slippage_sensitivity": "negative exponential",
    }
 
    return results