import pandas as pd
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_trades(file_path: Path):
    """
    Membaca file hasil backtest (CSV) dan menganalisis hari-hari dengan kerugian terbesar
    untuk mengidentifikasi penyebabnya, terutama 'Circuit Breaker'.
    """
    if not file_path.exists():
        console.print(f"[bold red]Error: File tidak ditemukan di '{file_path}'[/bold red]")
        return

    try:
        df = pd.read_csv(file_path)
        console.print(f"✅ Berhasil memuat {len(df)} trade dari '{file_path.name}'.")
    except Exception as e:
        console.print(f"[bold red]Error saat membaca file CSV: {e}[/bold red]")
        return

    # --- Persiapan Data ---
    if 'Exit Time' not in df.columns or 'PnL (USD)' not in df.columns:
        console.print("[bold red]Error: File CSV harus memiliki kolom 'Exit Time' dan 'PnL (USD)'[/bold red]")
        return
        
    df['Exit Time'] = pd.to_datetime(df['Exit Time'])
    df['Exit Date'] = df['Exit Time'].dt.date

    # --- Analisis 1: Temukan Hari Trading Terburuk ---
    daily_pnl = df.groupby('Exit Date')['PnL (USD)'].sum().sort_values()
    worst_days = daily_pnl.head(5)

    console.print("\n[bold red]Top 5 Hari Trading Terburuk berdasarkan Net PnL:[/bold red]")
    worst_days_table = Table(show_header=True, header_style="bold red")
    worst_days_table.add_column("Tanggal")
    worst_days_table.add_column("Total PnL (USD)", justify="right")
    for date, pnl in worst_days.items():
        worst_days_table.add_row(str(date), f"${pnl:,.2f}")
    console.print(worst_days_table)

    # --- Analisis BARU: Temukan Hari Trading Terbaik ---
    best_days = daily_pnl.tail(5).sort_values(ascending=False)
    console.print("\n[bold green]Top 5 Hari Trading Terbaik berdasarkan Net PnL:[/bold green]")
    best_days_table = Table(show_header=True, header_style="bold green")
    best_days_table.add_column("Tanggal")
    best_days_table.add_column("Total PnL (USD)", justify="right")
    for date, pnl in best_days.items():
        best_days_table.add_row(str(date), f"${pnl:,.2f}")
    console.print(best_days_table)

    # --- Analisis 2: Selami Lebih Dalam Hari-Hari Terburuk ---
    console.print("\n[bold]Detail Trade pada Hari-Hari Terburuk:[/bold]")
    for date, total_pnl in worst_days.items():
        day_trades = df[df['Exit Date'] == date].sort_values(by='PnL (USD)')
        
        day_table = Table(title=f"Analisis untuk Tanggal: {date} (Total PnL: ${total_pnl:,.2f})", show_header=True, header_style="bold yellow")
        day_table.add_column("Simbol")
        day_table.add_column("Arah")
        day_table.add_column("PnL (USD)", justify="right")
        day_table.add_column("Alasan Keluar", style="yellow")

        for _, trade in day_trades.iterrows():
            pnl_color = "red" if trade['PnL (USD)'] < 0 else "green"
            day_table.add_row(
                trade['Symbol'],
                trade['Direction'],
                f"[{pnl_color}]${trade['PnL (USD)']:.2f}[/{pnl_color}]",
                trade['Exit Reason']
            )
        console.print(day_table)

    # --- Analisis BARU: Selami Lebih Dalam Hari-Hari Terbaik ---
    console.print("\n[bold]Detail Trade pada Hari-Hari Terbaik:[/bold]")
    for date, total_pnl in best_days.items():
        day_trades = df[df['Exit Date'] == date].sort_values(by='PnL (USD)', ascending=False)
        
        day_table = Table(title=f"Analisis untuk Tanggal: {date} (Total PnL: ${total_pnl:,.2f})", show_header=True, header_style="bold green")
        day_table.add_column("Simbol")
        day_table.add_column("Arah")
        day_table.add_column("PnL (USD)", justify="right")
        day_table.add_column("Alasan Keluar", style="green")

        for _, trade in day_trades.iterrows():
            pnl_color = "green" if trade['PnL (USD)'] > 0 else "red"
            day_table.add_row(
                trade['Symbol'],
                trade['Direction'],
                f"[{pnl_color}]${trade['PnL (USD)']:.2f}[/{pnl_color}]",
                trade['Exit Reason']
            )
        console.print(day_table)

    # --- Analisis 3: Konfirmasi Hipotesis ---
    circuit_breaker_trades = df[df['Exit Reason'] == 'Circuit Breaker']
    if not circuit_breaker_trades.empty:
        total_cb_loss = circuit_breaker_trades['PnL (USD)'].sum()
        console.print("\n[bold magenta]--- Analisis Penyebab Kerugian Besar ---[/bold magenta]")
        console.print(f"Ditemukan [bold]{len(circuit_breaker_trades)}[/bold] trade yang ditutup oleh '[bold yellow]Circuit Breaker[/bold yellow]'.")
        console.print(f"Total kerugian dari trade ini adalah [bold red]${total_cb_loss:,.2f}[/bold red].")
        console.print("Ini mengkonfirmasi bahwa kerugian besar pada hari-hari tertentu kemungkinan besar disebabkan oleh peristiwa pasar ekstrem yang memicu penutupan darurat di beberapa posisi secara bersamaan, mensimulasikan slippage yang signifikan.")
    else:
        console.print("\n[bold green]Tidak ada trade yang ditutup oleh 'Circuit Breaker'. Kerugian kemungkinan disebabkan oleh akumulasi stop loss normal (death by a thousand cuts).[/bold green]")


def main():
    parser = argparse.ArgumentParser(
        description="Menganalisis file hasil backtest untuk menemukan penyebab kerugian besar."
    )
    parser.add_argument(
        "filepath",
        type=Path,
        default=Path("output/market_scan_results.csv"),
        nargs='?',
        help="Path ke file market_scan_results.csv. Default: 'output/market_scan_results.csv'"
    )
    args = parser.parse_args()
    analyze_trades(args.filepath)

if __name__ == "__main__":
    main()