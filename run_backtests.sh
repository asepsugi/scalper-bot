#!/bin/bash

# ==============================================================================
# SCRIPT UNTUK MENJALANKAN BACKTEST PADA BERBAGAI PERIODE PASAR
# ==============================================================================
#
# Script ini akan menjalankan backtest_market_scanner.py secara berurutan
# untuk beberapa periode pasar yang krusial. Setiap backtest akan berjalan
# hingga selesai sebelum yang berikutnya dimulai, memastikan tidak ada tumpang tindih.
#
# Cara Menjalankan:
# 1. Beri izin eksekusi: chmod +x run_backtests.sh
# 2. Jalankan script: ./run_backtests.sh
#
# Hasil dari setiap backtest akan ditambahkan ke bagian atas file BACKTEST_LOG.md.
#

# Header untuk menandai dimulainya proses
echo "======================================================"
echo "Memulai Rangkaian Backtest Multi-Periode..."
echo "======================================================"
date

# --- Periode 1: Bull Market 2021 ---
echo ""
echo "--> Menjalankan Backtest untuk Bull Market (Jan 2021 - Apr 2021)..."
python3 backtest_market_scanner.py --start_date 2021-01-01 --end_date 2021-04-30 --max_symbols 50 --historical_ranking

# --- Periode 2: Bear Market 2022 ---
echo ""
echo "--> Menjalankan Backtest untuk Bear Market (Mei 2022 - Nov 2022)..."
python3 backtest_market_scanner.py --start_date 2022-05-01 --end_date 2022-11-30 --max_symbols 50 --historical_ranking

# --- Periode 3: Memecoin Mania 2024 ---
echo ""
echo "--> Menjalankan Backtest untuk Memecoin Mania (Mei 2024 - Jun 2024)..."
python3 backtest_market_scanner.py --start_date 2024-05-01 --end_date 2024-06-30 --max_symbols 50 --historical_ranking

# --- Periode 4: Proyeksi Altseason 2025 ---
echo ""
echo "--> Menjalankan Backtest untuk Proyeksi Altseason (Okt 2025 - Des 2025)..."
python3 backtest_market_scanner.py --start_date 2025-10-01 --end_date 2025-12-31 --max_symbols 50 --historical_ranking

echo ""
echo "======================================================"
echo "Semua backtest telah selesai."
echo "======================================================"
date