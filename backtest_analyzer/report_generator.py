import pandas as pd
from pathlib import Path
import numpy as np
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from fpdf import FPDF

from utils.io_handler import save_output
 

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Advanced Backtest Strategy Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, df: pd.DataFrame):
        self.set_font('Arial', '', 10)
        # --- REVISI: Dynamic column width calculation ---
        # Get effective page width
        effective_page_width = self.w - 2 * self.l_margin
        # Calculate equal width for each column
        col_width = effective_page_width / len(df.columns)
        col_widths = [col_width] * len(df.columns)
        header = df.columns
        self.set_font('Arial', 'B', 9)
        for i, h in enumerate(header):
            self.cell(col_widths[i], 7, h, 1, 0, 'C')
        self.ln()
        self.set_font('Arial', '', 9)
        for _, row in df.iterrows():
            for i, item in enumerate(row):
                self.cell(col_widths[i], 6, str(item), 1)
            self.ln()
        self.ln(10)

def export_to_pdf(df: pd.DataFrame, output_path: Path, plots_dir: Path):
    """Exports the summary DataFrame and plots to a PDF report."""
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Strategy Performance Ranking (by Final Score)')

    # --- REVISI: Gunakan DataFrame yang sudah diformat dan difilter ---
    # Pilih dan ganti nama kolom seperti di generate_summary_table
    report_df = df[[
        'version', 'total_trades', 'profit_factor', 'win_rate', 'max_drawdown', 
        'avg_rr', 'final_score', 'sharpe_ratio', 'calmar_ratio', 'SI', 'ES'
    ]].copy().head(10) # Ambil top 10

    report_df.rename(columns={'version': 'Version', 'total_trades': 'Trades', 'profit_factor': 'PF', 'win_rate': 'Win %', 'max_drawdown': 'DD %', 'avg_rr': 'Avg RR', 'final_score': 'Score', 'sharpe_ratio': 'Sharpe', 'calmar_ratio': 'Calmar', 'SI': 'Sustain.', 'ES': 'Stability'}, inplace=True)

    # Format angka
    for col in report_df.columns:
        if report_df[col].dtype == 'float64':
            report_df[col] = report_df[col].apply(lambda x: f"{x:.2f}")

    pdf.chapter_body(report_df)
    pdf.output(output_path)
    print(f"📄 Laporan PDF disimpan ke '{output_path}'")
 
def calculate_final_score(df: pd.DataFrame, weights_list: List[float], final_weights_list: List[float]) -> pd.DataFrame:
    """
    Menghitung skor komprehensif (effectiveness, robustness, dan final)
    berdasarkan logika dari evaluate_results.py.
    """
    # 1. Hitung Effectiveness Score
    def calc_effectiveness_score(row, weights_list):
        pf = row.get('profit_factor', 0)
        win_rate = row.get('win_rate', 0)
        max_dd = row.get('max_drawdown', 100)
        sharpe = row.get('sharpe_ratio', 0)

        pf_score = min(pf, 5) / 5
        win_rate_score = win_rate / 100
        sharpe_score = min(sharpe, 20) / 20
        drawdown_score = 1 - (min(max_dd, 50) / 50)

        weights = {'pf': weights_list[0], 'win_rate': weights_list[1], 'sharpe': weights_list[2], 'dd': weights_list[3]}
        score = (
            pf_score * weights['pf'] +
            win_rate_score * weights['win_rate'] +
            sharpe_score * weights['sharpe'] +
            drawdown_score * weights['dd']
        )

        if row.get('total_trades', 0) < 100:
            score *= 0.85
        if row.get('net_profit_pct', 0) > 100:
            score *= 1.1
        if sharpe > 5:
            score *= 1.2
        return score

    df['effectiveness_score'] = df.apply(lambda row: calc_effectiveness_score(row, weights_list), axis=1)

    # 2. Hitung Robustness Metrics (ES, CI, SI)
    df['ES'] = (1 / df['max_drawdown'].replace(0, 1e-6)) * (df['profit_factor'] / 2)
    
    overall_avg_duration = df['avg_trade_duration'].mean()
    # PERBAIKAN: Hindari pembagian dengan nol jika hanya ada satu data atau durasi nol
    if overall_avg_duration > 0:
        df['TDV'] = abs(df['avg_trade_duration'] - overall_avg_duration) / overall_avg_duration
    else:
        df['TDV'] = 0
    df['CI'] = (df['profit_factor'] * (df['win_rate'] / 100)) / (1 + (df['TDV'] / 10))

    # PERBAIKAN: Tangani kasus jika hanya ada satu strategi (df.max() akan error pada scalar)
    if len(df) > 1:
        es_norm = df['ES'] / df['ES'].max() if df['ES'].max() > 0 else 0
        ci_norm = df['CI'] / df['CI'].max() if df['CI'].max() > 0 else 0
        sharpe_norm = df['sharpe_ratio'] / df['sharpe_ratio'].max() if df['sharpe_ratio'].max() > 0 else 0
    else: # Jika hanya satu strategi, skor normalisasi adalah 1 (karena itu yang terbaik dan terburuk)
        es_norm, ci_norm, sharpe_norm = 1.0, 1.0, 1.0
    df['SI'] = (es_norm + ci_norm + sharpe_norm) / 3

    # 3. Hitung Final Score
    df['final_score'] = (
        df['effectiveness_score'] * final_weights_list[0] + 
        df['SI'] * final_weights_list[1] + 
        df['ES'] * final_weights_list[2]
    )
    return df
 
 
def generate_terminal_ranking(df: pd.DataFrame, rank_by: str = 'sharpe_ratio') -> None:
    """
    Menampilkan ranking strategi di terminal menggunakan Rich.
    """
    console = Console()
    console.print("\n--- [bold cyan]Advanced Backtest Compare[/bold cyan] ---")
 
    df_sorted = df.sort_values(by=rank_by, ascending=False)
 
    console.print(f"Loaded {len(df)} strategy versions.")
    console.print(f"\n[bold]Top 3 by {rank_by.replace('_', ' ').title()}:[/bold]")
 
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="dim", width=6)
    table.add_column("Version", style="bold")
    table.add_column("Sharpe", justify="right")
    table.add_column("Sustain.", justify="right")
    table.add_column("Stability", justify="right")
    table.add_column("Drawdown", justify="right")
    table.add_column("Profit %", justify="right")
    table.add_column("Slippage Impact @0.1%", justify="right")
 
    for i, row in enumerate(df_sorted.head(3).itertuples(), 1):
        # --- PERBAIKAN: Logika pewarnaan dinamis berdasarkan legenda ---
        sharpe_val = row.sharpe_ratio
        sharpe_style = "green" if sharpe_val > 1.0 else ("red" if sharpe_val < 0.5 else "yellow")

        si_val = row.SI
        si_style = "green" if si_val > 0.7 else ("red" if si_val < 0.5 else "yellow")

        es_val = row.ES
        es_style = "green" if es_val > 0.8 else ("red" if es_val < 0.4 else "yellow")

        dd_val = row.max_drawdown
        dd_style = "green" if dd_val < 10 else ("red" if dd_val > 25 else "yellow")

        profit_val = row.net_profit_pct
        profit_style = "green" if profit_val > 0 else "red"

        slippage_val = row.slippage_impact
        slippage_style = "green" if slippage_val < 15 else ("red" if slippage_val > 30 else "yellow")

        table.add_row(
            f"{i}.",
            row.version,
            f"[{sharpe_style}]{sharpe_val:.2f}[/{sharpe_style}]",
            f"[{si_style}]{si_val:.2f}[/{si_style}]",
            f"[{es_style}]{es_val:.2f}[/{es_style}]",
            f"[{dd_style}]{dd_val:.2f}%[/{dd_style}]",
            f"[{profit_style}]{profit_val:+.2f}%[/{profit_style}]",
            f"[{slippage_style}]{slippage_val:.2f}%[/{slippage_style}]",
        )
 
    console.print(table)
 
def print_legend(console: Console):
    """Prints a legend for interpreting the robustness metrics."""
    console.print("\n--- [bold]Metrics Legend[/bold] ---")
    legend_table = Table(show_header=True, header_style="bold blue", box=None)
    legend_table.add_column("Metric", style="bold")
    legend_table.add_column("Description")
    legend_table.add_column("Good", style="green")
    legend_table.add_column("Bad", style="red")

    legend_table.add_row(
        "Sharpe", "Risk-adjusted return. Higher is better.", "> 1.0", "< 0.5"
    )
    legend_table.add_row(
        "Sustain. (SI)", "Sustainability Index. Overall long-term viability.", "> 0.70", "< 0.50"
    )
    legend_table.add_row(
        "Stability (ES)", "Equity Stability. Measures how smooth the profit curve is.", "> 0.80", "< 0.40"
    )
    legend_table.add_row(
        "Slippage Impact", "Profit drop with 0.1% slippage. Measures real-world resilience.", "< 15%", "> 30%"
    )
    legend_table.add_row(
        "Drawdown", "Maximum loss from a peak. Measures risk.", "< 10%", "> 25%"
    )

    console.print(legend_table)

 
def generate_full_report(
    all_metrics: List[Dict[str, Any]], output_dir: Path, plots_dir: Path, rank_only: bool = False, export_pdf_flag: bool = False, weights_list: List[float] = [0.4, 0.2, 0.2, 0.2], final_weights_list: List[float] = [0.5, 0.3, 0.2]
) -> str:
    """
    Menggabungkan semua metrik, membuat laporan, dan menyimpannya.
    """
    df = pd.DataFrame(all_metrics)
    
    # --- LANGKAH PRE-FILTERING ---
    # Ganti nilai 'inf' dengan NaN agar mudah difilter
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Tentukan kolom kritis untuk validasi
    critical_metrics = ['sharpe_ratio', 'profit_factor', 'max_drawdown']
    
    # Pisahkan strategi yang valid dan tidak valid
    invalid_mask = df[critical_metrics].isna().any(axis=1)
    invalid_strategies_df = df[invalid_mask]
    valid_df = df[~invalid_mask].copy()

    if valid_df.empty:
        print("\n❌ Tidak ada strategi dengan data yang valid untuk dianalisis.")
        if not invalid_strategies_df.empty:
            print("Strategi berikut didiskualifikasi karena data tidak lengkap (NaN/inf):")
            print(invalid_strategies_df['version'].tolist())
        return "No valid strategies found"
 
    # Hitung skor komprehensif
    valid_df = calculate_final_score(valid_df, weights_list, final_weights_list)
 
    # Ranking berdasarkan final_score
    rank_by = "final_score"
    df_sorted = valid_df.sort_values(by=rank_by, ascending=False).copy()
    best_strategy = df_sorted.iloc[0]
 
    if not rank_only:
        # Simpan laporan lengkap
        save_output(df_sorted, "summary", output_dir)
 
    if export_pdf_flag:
        pdf_path = output_dir / "summary_report.pdf"
        export_to_pdf(df_sorted, pdf_path, plots_dir)

    generate_terminal_ranking(df_sorted, 'sharpe_ratio') # Tetap tampilkan ranking Sharpe di terminal untuk perbandingan

    # --- REVISI: Tampilkan legend di console ---
    print_legend(Console())

    # Laporkan strategi yang didiskualifikasi di akhir
    if not invalid_strategies_df.empty:
        console = Console()
        console.print("\n[yellow]Info: Strategi berikut didiskualifikasi karena data tidak lengkap (NaN/inf):[/yellow]")
        console.print(f"[dim]{invalid_strategies_df['version'].tolist()}[/dim]")

    return best_strategy["version"]