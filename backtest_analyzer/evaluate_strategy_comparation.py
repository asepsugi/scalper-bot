import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Konfigurasi logging
LOG_DIR = Path(__file__).parent / 'output' / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'advanced_backtest.log'),
        logging.StreamHandler()
    ]
)

from utils.io_handler import load_backtest_results
from utils.plotting import plot_monte_carlo_distribution, plot_equity_curve_with_bands, plot_slippage_sensitivity
from utils.helpers import get_project_root
from risk_metrics import calculate_advanced_metrics
from montecarlo import run_monte_carlo_simulation
from sensitivity import run_sensitivity_analysis
from report_generator import generate_full_report
from slippage_model import estimate_slippage_impact
from rich.console import Console


def main():
    parser = argparse.ArgumentParser(description="Advanced Backtest Comparison and Analysis Tool")
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the JSON file with portfolio backtest results (e.g., 'strategy_comparison_results.json')."
    )
    parser.add_argument("--show_plots", action="store_true", help="Tampilkan grafik interaktif.")
    parser.add_argument("--export_pdf", action="store_true", help="Generate PDF report")
    parser.add_argument("--rank_only", action="store_true", help="Hanya tampilkan ranking strategi.")
    parser.add_argument("--slippage_max", type=float, default=0.01, help="Nilai max slippage untuk analisis (default 1%).")
    parser.add_argument("--weights", type=str, default="0.4,0.2,0.2,0.2", help="Comma-separated weights for effectiveness score (pf,win_rate,sharpe,dd).")
    parser.add_argument("--final-weights", type=str, default="0.5,0.3,0.2", help="Comma-separated weights for final score (effectiveness,SI,ES).")
    args = parser.parse_args()

    console = Console()

    # Setup direktori output
    output_dir = get_project_root() / 'output'
    plots_dir = output_dir / 'plots'

    # 1. Muat hasil backtest
    all_symbol_results = load_backtest_results(args.filepath)
    if not all_symbol_results:
        logging.error("Tidak ada data untuk dianalisis. Keluar.")
        return

    # --- PERBAIKAN: Langsung gunakan data karena sudah diagregasi oleh backtester ---
    console.log(f"Loaded {len(all_symbol_results)} aggregated strategy results.")
    df = pd.DataFrame(all_symbol_results)

    # Ganti nilai inf dengan NaN untuk perhitungan yang aman
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    aggregated_metrics_list = df.to_dict('records')

    all_processed_metrics = []

    for metrics in aggregated_metrics_list:
        version = metrics['version']
        logging.info(f"--- Menganalisis versi: {version} ---")

        # --- PERBAIKAN: Gunakan total_trades yang diagregasi untuk simulasi ---
        num_days = int(metrics.get('total_trades', 1) * 0.5) # Asumsi: 2 trade per hari
        if num_days == 0: continue
        
        # Simulasikan daily returns berdasarkan Sharpe Ratio
        daily_std = (metrics['net_profit_pct'] / 100) / (metrics.get('sharpe_ratio', 1) * np.sqrt(252))
        # --- PERBAIKAN: Pastikan standar deviasi (scale) selalu positif ---
        # Standar deviasi tidak boleh negatif. Ambil nilai absolutnya.
        # Arah return (positif/negatif) sudah diatur oleh parameter 'loc'.
        daily_std = abs(daily_std)
        if not np.isfinite(daily_std) or daily_std == 0: daily_std = 0.001 # Gunakan nilai kecil jika std nol
        daily_returns = pd.Series(np.random.normal(
            loc=(metrics['net_profit_pct'] / 100) / 252,
            scale=daily_std,
            size=num_days
        ))

        # 2. Hitung metrik risiko lanjutan pada data agregat
        metrics = calculate_advanced_metrics(metrics, daily_returns)

        # 3. Jalankan Monte Carlo
        final_equities, equity_paths = run_monte_carlo_simulation(daily_returns)
        metrics['mc_median_equity'] = np.median(final_equities)
        metrics['mc_p5_equity'] = np.percentile(final_equities, 5)
        metrics['mc_p95_equity'] = np.percentile(final_equities, 95)
        metrics['mc_prob_loss'] = (final_equities < 10000).mean()

        # 4. Jalankan Analisis Sensitivitas pada data agregat
        sensitivity_results = run_sensitivity_analysis(
            daily_returns, metrics['total_trades'], metrics['avg_rr'], metrics['win_rate'], args.slippage_max
        )
        metrics['sensitivity_summary'] = sensitivity_results['summary']
        
        # Estimasi dampak slippage 0.1%
        metrics['slippage_impact'] = metrics['net_profit_pct'] - estimate_slippage_impact(metrics['net_profit_pct'], metrics['total_trades'], 0.001)

        # 5. Generate plot (jika diminta)
        if not args.rank_only:
            plot_monte_carlo_distribution(final_equities, 10000, plots_dir / f'{version}_mc_dist.png', args.show_plots)
            plot_equity_curve_with_bands(equity_paths, plots_dir / f'{version}_equity_bands.png', args.show_plots)
            plot_slippage_sensitivity(sensitivity_results['slippage_analysis'], plots_dir / f'{version}_slippage.png', args.show_plots)

        all_processed_metrics.append(metrics)

    # 6. Generate Laporan Akhir
    if all_processed_metrics:
        # Parse effectiveness score weights
        try:
            weights_list = [float(w) for w in args.weights.split(',')]
            assert len(weights_list) == 4
        except (ValueError, AssertionError):
            logging.error("Invalid weights format. Using default '0.4,0.2,0.2,0.2'.")
            weights_list = [0.4, 0.2, 0.2, 0.2]
        # Parse final score weights
        try:
            final_weights_list = [float(w) for w in args.final_weights.split(',')]
            assert len(final_weights_list) == 3
        except (ValueError, AssertionError):
            logging.error("Invalid final-weights format. Using default '0.5,0.3,0.2'.")
            final_weights_list = [0.5, 0.3, 0.2]
        best_strategy = generate_full_report(all_processed_metrics, output_dir, plots_dir, args.rank_only, args.export_pdf, weights_list, final_weights_list)
        logging.info(f"Best overall strategy: {best_strategy} ✅")
    else:
        logging.warning("Tidak ada metrik yang berhasil diproses.")


if __name__ == "__main__":
    main()