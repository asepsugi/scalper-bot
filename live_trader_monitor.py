import ccxt.pro as ccxtpro
import os
import asyncio
import collections
import json
import argparse
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.console import Group
from rich.table import Table
from datetime import datetime

from config import API_KEYS

# --- KONFIGURASI ---
REFRESH_RATE_SECONDS = 5  # Seberapa sering dashboard diperbarui (dalam detik)

console = Console()

async def initialize_exchange(env='live'):
    """Inisialisasi koneksi exchange (asinkron) untuk monitoring."""
    try:
        # --- PERBAIKAN: Konfigurasi dinamis berdasarkan lingkungan ---
        if env == 'live':
            api_key_config = API_KEYS['live']
            test_mode = False
            env_name = "LIVE"
        else:  # demo
            api_key_config = API_KEYS['testnet']
            test_mode = True
            env_name = "DEMO TRADING"

        exchange = ccxtpro.binance({
            'apiKey': api_key_config['api_key'],
            'secret': api_key_config['api_secret'],
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
            },
            'test': test_mode,
            'enableRateLimit': True,
        })
        # --- PERBAIKAN DEFINITIF: Selaraskan dengan live_trader.py ---
        # Untuk 'live', kita perlu secara eksplisit menonaktifkan sandbox mode untuk
        # menimpa deteksi otomatis ccxt, terutama jika API key sama dengan testnet.
        # Untuk 'demo', parameter 'test': True sudah cukup dan tidak perlu tindakan lebih lanjut.
        if env == 'live':
            exchange.set_sandbox_mode(False)
        console.log(f"[bold yellow]Berhasil terhubung ke Binance Futures ({env_name}).[/bold yellow]")
        return exchange
    except Exception as e:
        console.print(f"[bold red]Gagal terhubung ke exchange: {e}[/bold red]")
        return None

async def generate_dashboard(exchange, env='live') -> Group:
    """Membuat dan mengembalikan grup renderable untuk dashboard Rich."""
    
    # --- PERBAIKAN: Tentukan file log dan state berdasarkan lingkungan ---
    # Menyesuaikan path agar sama persis dengan yang ditulis oleh live_trader.py dan demo_trader.py
    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "output"
    if env == 'live':
        state_file = output_dir / "live_positions.json"
        event_log_file = output_dir / "events.log"
    else: # demo
        state_file = output_dir / "demo_positions.json"
        event_log_file = output_dir / "demo_events.log"

    # 1. Ambil data real-time dari exchange
    try:
        balance_info = await exchange.fetch_balance()
        positions = await exchange.fetch_positions()

        # Ekstrak informasi saldo dari respons fetch_balance
        total_balance = balance_info['USDT']['total'] if 'USDT' in balance_info and 'total' in balance_info['USDT'] else 0
        free_balance = balance_info['USDT']['free'] if 'USDT' in balance_info and 'free' in balance_info['USDT'] else 0

    except Exception as e:
        return Group(Table(title=f"Error: Gagal mengambil data - {e}"))

    # --- PENINGKATAN: Baca beberapa baris terakhir dari file event log ---
    event_logs = []
    if event_log_file.exists():
        try:
            with open(event_log_file, 'r', buffering=1) as f:
                event_logs = list(collections.deque(f, 5))
        except IOError:
            event_logs = ["Gagal membaca file event log."]

    # Filter posisi yang benar-benar aktif (memiliki size)
    active_positions = [p for p in positions if p.get('info') and float(p['info']['positionAmt']) != 0]

    # --- PENINGKATAN: Baca state file untuk menandai posisi yang dikelola bot ---
    managed_symbols = set()
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                managed_data = json.load(f)
                # Kunci dalam JSON adalah simbol dalam format 'BTC/USDT', kita butuh 'BTCUSDT'
                managed_symbols = {symbol.replace('/', '') for symbol in managed_data.keys()}
        except (json.JSONDecodeError, IOError):
            console.log(f"[yellow]Peringatan: Gagal membaca {state_file}.[/yellow]")

    # 2. Buat Tabel Dashboard
    env_title = "LIVE" if env == 'live' else "DEMO"
    status_table = Table(
        title=f"🤖 Trader Dashboard ({env_title}) - (Diperbarui setiap {REFRESH_RATE_SECONDS} detik)",
        caption=f"Terakhir diperbarui pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        header_style="bold magenta",
        show_header=True
    )
    status_table.add_column("Metric", style="cyan", no_wrap=True)
    status_table.add_column("Value", style="white")
    
    # 3. Isi Informasi Umum
    status_table.add_row("Total Balance (USDT)", f"${total_balance:,.4f}")
    status_table.add_row("Available Balance (USDT)", f"${free_balance:,.4f}")
    status_table.add_row("Total Posisi Aktif", str(len(active_positions)))

    # 4. Isi Detail Posisi Aktif
    if active_positions:
        status_table.add_section()
        for pos in sorted(active_positions, key=lambda p: p['symbol']): # Urutkan berdasarkan abjad
            info = pos['info']
            symbol = info['symbol']
            side = "LONG" if float(info['positionAmt']) > 0 else "SHORT"
            entry_price = float(info['entryPrice'])
            mark_price = float(info['markPrice'])
            pnl = float(info['unrealizedProfit'])

            # Cek apakah posisi ini dikelola oleh bot
            is_managed_by_bot = symbol in managed_symbols
            managed_indicator = "🤖 " if is_managed_by_bot else ""

            pnl_color = "green" if pnl >= 0 else "red"
            side_color = "green" if side == "LONG" else "red"

            pos_title = f"Posisi: {managed_indicator}[bold {side_color}]{symbol} ({side})[/bold {side_color}]"
            pos_details = (
                f"  Entry: ${entry_price:,.4f}\n"
                f"  Mark: ${mark_price:,.4f}\n"
                f"  PnL: [{pnl_color}]${pnl:,.4f}[/{pnl_color}]"
            )
            status_table.add_row(pos_title, pos_details)
    else:
        status_table.add_row("Posisi Aktif", "[yellow]Tidak ada[/yellow]")

    # 5. Tambahkan Event Log ke Dashboard
    log_table = Table(title="[bold]Event Log Terbaru[/bold]", show_header=False, box=None, expand=True)
    log_table.add_column("Marker", width=2)
    log_table.add_column("Log")
    
    if event_logs:
        for log_line in event_logs:
            log_table.add_row(">", log_line.strip())
    else:
        log_table.add_row(">", "[grey50]Menunggu event dari bot...[/grey50]")

    # Gabungkan kedua tabel ke dalam satu grup untuk dirender
    return Group(status_table, log_table)

async def main(env):
    """Fungsi utama asinkron untuk menjalankan monitor."""
    # --- REVISI: Loop koneksi yang lebih tangguh ---
    # Alih-alih langsung keluar, kita akan terus mencoba terhubung.
    exchange = None
    while exchange is None:
        try:
            env_name = "LIVE" if env == 'live' else "DEMO"
            console.print(f"Mencoba terhubung & memvalidasi koneksi ke Binance ({env_name})...", style="yellow")
            
            # --- PERBAIKAN: Kirim argumen env ke fungsi inisialisasi ---
            temp_exchange = await initialize_exchange(env)
            
            if temp_exchange:
                # --- REVISI: Lakukan panggilan API pertama untuk validasi ---
                # Ini akan langsung memicu error jika API Key/IP salah.
                validation_response = await temp_exchange.fetch_balance()

                # --- PENINGKATAN: Validasi respons saat inisialisasi ---
                if 'USDT' not in validation_response:
                    raise TypeError(f"Validasi koneksi gagal. Respons saldo tidak mengandung 'USDT'. Diterima: {str(validation_response)[:200]}")

                exchange = temp_exchange # Jika berhasil, tetapkan ke variabel utama
                console.print("✅ Berhasil terhubung & tervalidasi. Memulai dashboard monitor...", style="green")
            else:
                # Kasus jika initialize_exchange sendiri gagal
                raise Exception("Inisialisasi exchange gagal.")
        except Exception as e:
            console.print(f"[bold red]Koneksi gagal: {e}[/bold red]")
            console.print("[bold yellow]Hint: Ini kemungkinan besar karena masalah IP Whitelist atau izin API Key. Mencoba lagi dalam 30 detik...[/bold yellow]")
            await asyncio.sleep(30) # Tunggu sebelum mencoba lagi

    # --- REVISI: Gunakan try...finally untuk memastikan koneksi ditutup ---
    try:
        # REVISI: Pindahkan penanganan KeyboardInterrupt ke luar blok 'with Live'
        # Ini memastikan bahwa blok 'finally' utama akan selalu dieksekusi
        # bahkan jika Ctrl+C ditekan, mencegah 'Unclosed client session'.
        try:
            # REVISI: Dikembalikan ke screen=False untuk menghindari masalah rendering terminal.
            # Ini akan menyebabkan output menumpuk, tetapi lebih stabil.
            with Live(console=console, screen=False, auto_refresh=False) as live:
                # Lakukan pembaruan pertama kali saat startup
                initial_dashboard = await generate_dashboard(exchange, env)
                live.update(initial_dashboard, refresh=True)

                while True:
                    dashboard = await generate_dashboard(exchange, env)
                    live.update(dashboard, refresh=True)
                    await asyncio.sleep(REFRESH_RATE_SECONDS)
        except KeyboardInterrupt:
            # Cukup tangkap interupsi untuk keluar dari loop dengan anggun.
            # Pesan akan dicetak di blok finally.
            pass
    finally:
        # Blok ini akan selalu dijalankan, bahkan jika terjadi error atau KeyboardInterrupt.
        if exchange:
            console.print("\n[yellow]Monitor dihentikan. Menutup koneksi exchange...[/yellow]")
            await exchange.close()
            console.print("[green]Koneksi monitor berhasil ditutup.[/green]")

if __name__ == "__main__":
    # REVISI: Tangani KeyboardInterrupt di level tertinggi untuk mencegah traceback error
    # saat pengguna menekan Ctrl+C.
    parser = argparse.ArgumentParser(description="Live/Demo Trading Monitor")
    parser.add_argument("--env", type=str, choices=['live', 'demo'], default='live', 
                        help="Pilih lingkungan yang akan dipantau: 'live' atau 'demo'. Default: 'live'.")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.env))
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitor dihentikan oleh pengguna.[/yellow]")