import numpy as np
import pandas as pd
 
 
def apply_slippage_to_returns(
    daily_returns: pd.Series, total_trades: int, slippage_pct: float
) -> pd.Series:
    """
    Mengaplikasikan model slippage sederhana ke series return harian.
    Model ini mengasumsikan slippage mengurangi return harian secara merata.
 
    Args:
        daily_returns (pd.Series): Series return harian asli.
        total_trades (int): Jumlah total trade.
        slippage_pct (float): Persentase slippage per trade (misal: 0.001 untuk 0.1%).
 
    Returns:
        pd.Series: Series return harian yang telah disesuaikan dengan slippage.
    """
    if total_trades == 0 or len(daily_returns) == 0:
        return daily_returns
 
    # Asumsi 2 eksekusi per trade (entry & exit)
    trades_per_day = total_trades / len(daily_returns)
    slippage_cost_per_day = trades_per_day * slippage_pct * 2
    return daily_returns - slippage_cost_per_day
 
 
def estimate_slippage_impact(net_profit_pct: float, total_trades: int, slippage_pct: float) -> float:
    """
    Memperkirakan dampak total slippage terhadap net profit.
    """
    # Asumsi 2 eksekusi per trade (entry & exit)
    total_slippage_cost = total_trades * slippage_pct * 2 * 100  # dalam persen
    return net_profit_pct - total_slippage_cost