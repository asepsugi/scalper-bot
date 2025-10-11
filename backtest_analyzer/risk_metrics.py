import numpy as np
import pandas as pd
from typing import Dict, Any

 
def calculate_advanced_metrics(
    metrics: Dict[str, Any], daily_returns: pd.Series
) -> Dict[str, Any]:
    """
    Menghitung metrik risiko lanjutan dan menambahkannya ke dictionary metrik.
 
    Args:
        metrics (Dict[str, Any]): Dictionary metrik yang ada.
        daily_returns (pd.Series): Series return harian.
 
    Returns:
        Dict[str, Any]: Dictionary metrik yang diperbarui.
    """
    # Pastikan daily_returns tidak kosong untuk menghindari error
    if daily_returns.empty or daily_returns.std() == 0:
        metrics["sortino_ratio"] = 0.0
        metrics["calmar_ratio"] = 0.0
        metrics["skewness"] = 0.0
        metrics["kurtosis"] = 0.0
        return metrics
 
    # 1. Sortino Ratio
    negative_returns = daily_returns[daily_returns < 0]
    downside_deviation = negative_returns.std()
    if downside_deviation > 0:
        sortino_ratio = (daily_returns.mean() * 252) / (downside_deviation * np.sqrt(252))
    else:
        sortino_ratio = np.inf
    metrics["sortino_ratio"] = sortino_ratio
 
    # 2. Calmar Ratio
    # Menggunakan max_drawdown yang sudah dihitung sebelumnya (dalam persen)
    max_dd_fraction = metrics.get("max_drawdown", 100.0) / 100.0
    annualized_return = daily_returns.mean() * 252
    if max_dd_fraction > 0:
        calmar_ratio = annualized_return / max_dd_fraction
    else:
        calmar_ratio = np.inf
    metrics["calmar_ratio"] = calmar_ratio
 
    # 3. Skewness
    metrics["skewness"] = daily_returns.skew()
 
    # 4. Kurtosis
    metrics["kurtosis"] = daily_returns.kurtosis()  # Excess kurtosis
 
    # Ganti nilai NaN atau inf dengan 0 untuk konsistensi
    for key in ["sortino_ratio", "calmar_ratio", "skewness", "kurtosis"]:
        if not np.isfinite(metrics[key]):
            metrics[key] = 0.0
 
    return metrics