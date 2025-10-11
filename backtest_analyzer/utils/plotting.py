import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List

from .helpers import ensure_dir_exists
 
 
def plot_monte_carlo_distribution(
    final_equities: np.ndarray,
    initial_equity: float,
    output_path: Path,
    show: bool = False,
) -> None:
    """Membuat plot distribusi hasil Monte Carlo."""
    ensure_dir_exists(output_path.parent)
    plt.figure(figsize=(12, 7))
    sns.histplot(final_equities, bins=50, kde=True, color="skyblue")
    plt.axvline(
        initial_equity,
        color="red",
        linestyle="--",
        label=f"Initial Equity (${initial_equity:,.0f})",
    )
    plt.axvline(
        np.mean(final_equities),
        color="orange",
        linestyle="-",
        label=f"Mean Equity (${np.mean(final_equities):,.0f})",
    )
    plt.title("Monte Carlo Simulation: Final Equity Distribution", fontsize=16)
    plt.xlabel("Final Equity (USDT)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(output_path)
    if show:
        plt.show()
    plt.close()
 
 
def plot_equity_curve_with_bands(
    equity_paths: List[np.ndarray],
    output_path: Path,
    show: bool = False,
) -> None:
    """Membuat plot equity curve dengan confidence bands (P5, Median, P95)."""
    ensure_dir_exists(output_path.parent)
    plt.figure(figsize=(14, 8))
 
    # Ubah list of arrays menjadi 2D array untuk perhitungan persentil
    max_len = max(len(p) for p in equity_paths)
    padded_paths = np.array(
        [np.pad(p, (0, max_len - len(p)), "edge") for p in equity_paths]
    )
 
    p5 = np.percentile(padded_paths, 5, axis=0)
    p50 = np.percentile(padded_paths, 50, axis=0)
    p95 = np.percentile(padded_paths, 95, axis=0)
 
    x_axis = np.arange(max_len)
    plt.plot(x_axis, p50, label="Median Equity Path", color="blue")
    plt.fill_between(
        x_axis, p5, p95, color="skyblue", alpha=0.4, label="90% Confidence Interval (P5-P95)"
    )
 
    plt.title("Simulated Equity Curve with Confidence Bands", fontsize=16)
    plt.xlabel("Days", fontsize=12)
    plt.ylabel("Equity (USDT)", fontsize=12)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(output_path)
    if show:
        plt.show()
    plt.close()
 
 
def plot_slippage_sensitivity(
    sensitivity_df: pd.DataFrame, output_path: Path, show: bool = False
) -> None:
    """Membuat plot heatmap sensitivitas profit terhadap slippage."""
    ensure_dir_exists(output_path.parent)
    plt.figure(figsize=(10, 6))
 
    # Pivot data untuk heatmap (jika diperlukan, untuk saat ini kita plot garis)
    sns.lineplot(data=sensitivity_df, x="slippage_pct", y="net_profit_pct", marker="o")
 
    plt.axhline(0, color="red", linestyle="--", label="Break-even Point")
    plt.title("Profit Sensitivity to Slippage", fontsize=16)
    plt.xlabel("Slippage per Trade (%)", fontsize=12)
    plt.ylabel("Net Profit (%)", fontsize=12)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(output_path)
    if show:
        plt.show()
    plt.close()