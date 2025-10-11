import numpy as np
import pandas as pd
from typing import Tuple, List
 
 
def run_monte_carlo_simulation(
    daily_returns: pd.Series,
    initial_equity: float = 10000,
    simulations: int = 1000,
) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Menjalankan simulasi Monte Carlo pada return harian.
 
    Args:
        daily_returns (pd.Series): Series return harian.
        initial_equity (float): Modal awal.
        simulations (int): Jumlah simulasi yang akan dijalankan.
 
    Returns:
        Tuple[np.ndarray, List[np.ndarray]]:
        - Array dari final equity setiap simulasi.
        - Daftar dari setiap jalur equity yang disimulasikan.
    """
    if daily_returns.empty:
        return np.array([initial_equity] * simulations), [np.array([initial_equity])]
 
    final_equities = np.zeros(simulations)
    equity_paths = []
 
    for i in range(simulations):
        # Resample return harian dengan replacement (bootstrap)
        simulated_returns = np.random.choice(
            daily_returns, size=len(daily_returns), replace=True
        )
 
        # Buat equity curve dari return yang disimulasikan
        equity_curve = initial_equity * (1 + simulated_returns).cumprod()
 
        final_equities[i] = equity_curve[-1]
        equity_paths.append(equity_curve)
 
    return final_equities, equity_paths