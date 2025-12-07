
---

## Backtest: 2025-12-07 08:45:44

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-25 (~1 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `XNYUSDT, SWARMSUSDT, HMSTRUSDT, NEARUSDT, BCHUSDT...`
- **Minggu 42:** `XNYUSDT, MONUSDT, SAPIENUSDT, HMSTRUSDT, LUNA2USDT...`
- **Minggu 43:** `SWARMSUSDT, HMSTRUSDT, LUNA2USDT, BCHUSDT, XPLUSDT...`
- **Minggu 44:** `XNYUSDT, SWARMSUSDT, SAPIENUSDT, HMSTRUSDT, LUNA2USDT...`
- **Minggu 45:** `XNYUSDT, SWARMSUSDT, HMSTRUSDT, NEARUSDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $7.84 | 17 | 58.82% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $82.84                     |
| **Net Profit**    | **$7.84 (+10.46%)** |
| Total Trades      | 17                         |
| Win Rate          | 58.82%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 17 trades (58.82%)             |
| Profit Factor     | 2.04                       |
| Max Drawdown      | 5.03%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-06 22:51:07

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-25 (~1 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`, `rsi_divergence_tolerance=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `1000SHIBUSDT, 1000PEPEUSDT, APTUSDT, DOTUSDT, TRXUSDT...`
- **Minggu 42:** `LTCUSDT, FARTCOINUSDT, APTUSDT, TRUMPUSDT, DOTUSDT...`
- **Minggu 43:** `LTCUSDT, FILUSDT, 1000SHIBUSDT, 1000PEPEUSDT, TRUMPUSDT...`
- **Minggu 44:** `TRADOORUSDT, PAXGUSDT, 1000PEPEUSDT, DOTUSDT, TRUMPUSDT...`
- **Minggu 45:** `LTCUSDT, 1000SHIBUSDT, PAXGUSDT, 1000PEPEUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $9.15 | 12 | 66.67% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $84.15                     |
| **Net Profit**    | **$9.15 (+12.20%)** |
| Total Trades      | 12                         |
| Win Rate          | 66.67%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 12 trades (66.67%)             |
| Profit Factor     | 2.99                       |
| Max Drawdown      | 2.75%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-06 22:29:41

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2024-05-30 s/d 2024-07-02 (~1 Bulan 4 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`, `rsi_divergence_tolerance=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 19:** `TAOUSDT, WLDUSDT, DASHUSDT, TRXUSDT, 1000SHIBUSDT...`
- **Minggu 20:** `LUNA2USDT, WLDUSDT, DASHUSDT, TRXUSDT, 1000SHIBUSDT...`
- **Minggu 21:** `LUNA2USDT, WLDUSDT, DASHUSDT, TRXUSDT, 1000SHIBUSDT...`
- **Minggu 22:** `TAOUSDT, WLDUSDT, DASHUSDT, TRXUSDT, APTUSDT...`
- **Minggu 23:** `TAOUSDT, LUNA2USDT, WLDUSDT, DASHUSDT, TRXUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $5.02 | 4 | 75.00% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $80.02                     |
| **Net Profit**    | **$5.02 (+6.69%)** |
| Total Trades      | 4                         |
| Win Rate          | 75.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 4 trades (75.00%)             |
| Profit Factor     | 7.45                       |
| Max Drawdown      | 0.99%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-06 22:14:21

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2022-05-09 s/d 2022-11-28 (~6 Bulan 24 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`, `rsi_divergence_tolerance=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 18:** `BCHUSDT, NEARUSDT, 1000SHIBUSDT, UNIUSDT, LTCUSDT...`
- **Minggu 19:** `BCHUSDT, NEARUSDT, 1000SHIBUSDT, UNIUSDT, LTCUSDT...`
- **Minggu 20:** `BCHUSDT, NEARUSDT, 1000SHIBUSDT, UNIUSDT, LTCUSDT...`
- **Minggu 21:** `BCHUSDT, NEARUSDT, 1000SHIBUSDT, UNIUSDT, DOTUSDT...`
- **Minggu 22:** `BCHUSDT, NEARUSDT, 1000SHIBUSDT, UNIUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $0.90 | 12 | 58.33% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $75.90                     |
| **Net Profit**    | **$0.90 (+1.21%)** |
| Total Trades      | 12                         |
| Win Rate          | 58.33%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 12 trades (58.33%)             |
| Profit Factor     | 1.09                       |
| Max Drawdown      | 6.12%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-06 21:39:48

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-08 s/d 2021-04-14 (~3 Bulan 7 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`, `rsi_divergence_tolerance=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `LTCUSDT, AAVEUSDT, DASHUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 2:** `LTCUSDT, AAVEUSDT, DASHUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 3:** `LTCUSDT, AAVEUSDT, DASHUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 4:** `LTCUSDT, AAVEUSDT, DASHUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 5:** `LTCUSDT, AAVEUSDT, DASHUSDT, BCHUSDT, CRVUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-11.26 | 28 | 35.71% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $63.74                     |
| **Net Profit**    | **$-11.26 (-15.01%)** |
| Total Trades      | 28                         |
| Win Rate          | 35.71%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 28 trades (35.71%)             |
| Profit Factor     | 0.55                       |
| Max Drawdown      | 16.26%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 4 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-06 20:02:35

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2024-05-06 s/d 2024-06-23 (~1 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`
- **`MemecoinMoonshotHunter`:** `risk_per_trade=0.015`, `risk_per_trade=0.015`, `volume_spike_multiplier=5`, `rsi_threshold=70`, `breakout_window=14`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 19:** `ICPUSDT, EGLDUSDT, ACEUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 20:** `ICPUSDT, ACEUSDT, BCHUSDT, CRVUSDT, TRXUSDT...`
- **Minggu 21:** `ENAUSDT, EGLDUSDT, ACEUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 22:** `ICPUSDT, OPUSDT, ENAUSDT, EGLDUSDT, CRVUSDT...`
- **Minggu 23:** `ICPUSDT, EGLDUSDT, BCHUSDT, CRVUSDT, TRXUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.4 | $-0.15 | 3 | 33.33% |
| `MemecoinMoonshotHunter`     | 0.3 | $0.00 | 0 | N/A |
| `LongOnlyCorrectionHunter`   | 0.3 | $-26.66 | 95 | 36.84% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $48.19                     |
| **Net Profit**    | **$-26.81 (-35.74%)** |
| Total Trades      | 98                         |
| Win Rate          | 36.73%                     |
|  - Long Win Rate  | 65 trades (32.31%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 0.51                       |
| Max Drawdown      | 33.30%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 11 Triggers                     |

**Catatan & Observasi:**
-   Memecoin Mania 2024


---

## Backtest: 2025-12-06 19:46:26

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2022-05-02 s/d 2022-12-01 (~7 Bulan 4 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`
- **`MemecoinMoonshotHunter`:** `risk_per_trade=0.015`, `risk_per_trade=0.015`, `volume_spike_multiplier=5`, `rsi_threshold=70`, `breakout_window=14`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 18:** `DOTUSDT, CRVUSDT, LTCUSDT, HBARUSDT, FILUSDT...`
- **Minggu 19:** `DOTUSDT, CRVUSDT, LTCUSDT, HBARUSDT, FILUSDT...`
- **Minggu 20:** `DOTUSDT, CRVUSDT, LTCUSDT, HBARUSDT, FILUSDT...`
- **Minggu 21:** `DOTUSDT, CRVUSDT, LTCUSDT, HBARUSDT, FILUSDT...`
- **Minggu 22:** `DOTUSDT, CRVUSDT, LTCUSDT, HBARUSDT, FILUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.4 | $6.28 | 7 | 71.43% |
| `MemecoinMoonshotHunter`     | 0.3 | $0.00 | 0 | N/A |
| `LongOnlyCorrectionHunter`   | 0.3 | $-9.41 | 292 | 45.21% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $71.87                     |
| **Net Profit**    | **$-3.13 (-4.18%)** |
| Total Trades      | 299                         |
| Win Rate          | 45.82%                     |
|  - Long Win Rate  | 160 trades (40.62%)              |
|  - Short Win Rate | 139 trades (51.80%)             |
| Profit Factor     | 0.98                       |
| Max Drawdown      | 36.82%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 19 Triggers                     |

**Catatan & Observasi:**
-   Bear Market 2022


---

## Backtest: 2025-12-06 18:53:02

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-05-01 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`
- **`MemecoinMoonshotHunter`:** `risk_per_trade=0.015`, `risk_per_trade=0.015`, `volume_spike_multiplier=5`, `rsi_threshold=70`, `breakout_window=14`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `CRVUSDT, DOTUSDT, LTCUSDT, DASHUSDT, BCHUSDT...`
- **Minggu 2:** `DOTUSDT, CRVUSDT, LTCUSDT, DASHUSDT, BCHUSDT...`
- **Minggu 3:** `DOTUSDT, CRVUSDT, LTCUSDT, DASHUSDT, BCHUSDT...`
- **Minggu 4:** `DOTUSDT, CRVUSDT, LTCUSDT, DASHUSDT, BCHUSDT...`
- **Minggu 5:** `CRVUSDT, DOTUSDT, LTCUSDT, DASHUSDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.4 | $5.93 | 24 | 50.00% |
| `MemecoinMoonshotHunter`     | 0.3 | $0.00 | 0 | N/A |
| `LongOnlyCorrectionHunter`   | 0.3 | $4.51 | 171 | 45.61% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $85.44                     |
| **Net Profit**    | **$10.44 (+13.91%)** |
| Total Trades      | 195                         |
| Win Rate          | 46.15%                     |
|  - Long Win Rate  | 133 trades (45.86%)              |
|  - Short Win Rate | 62 trades (46.77%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 29.53%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   Bull Market 2021


---

## Backtest: 2025-12-06 15:49:58

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-06 s/d 2025-12-06 (~2 Bulan 2 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`
- **`MemecoinMoonshotHunter`:** `risk_per_trade=0.015`, `risk_per_trade=0.015`, `volume_spike_multiplier=5`, `rsi_threshold=70`, `breakout_window=14`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `ENAUSDT, ASTERUSDT, TAOUSDT, APTUSDT, WLDUSDT...`
- **Minggu 42:** `TAOUSDT, APTUSDT, FARTCOINUSDT, WLDUSDT, TIAUSDT...`
- **Minggu 43:** `ENAUSDT, TIAUSDT, DASHUSDT, PUMPUSDT, ETCUSDT...`
- **Minggu 44:** `ASTERUSDT, HYPEUSDT, WLDUSDT, PIPPINUSDT, DASHUSDT...`
- **Minggu 45:** `ENAUSDT, HYPEUSDT, PUMPUSDT, 1000BONKUSDT, ETCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.4 | $5.91 | 16 | 43.75% |
| `MemecoinMoonshotHunter`     | 0.3 | $0.00 | 0 | N/A |
| `LongOnlyCorrectionHunter`   | 0.3 | $3.01 | 134 | 45.52% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $83.92                     |
| **Net Profit**    | **$8.92 (+11.90%)** |
| Total Trades      | 150                         |
| Win Rate          | 45.33%                     |
|  - Long Win Rate  | 103 trades (44.66%)              |
|  - Short Win Rate | 47 trades (46.81%)             |
| Profit Factor     | 1.08                       |
| Max Drawdown      | 24.21%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   Kondisi market saat ini setelah fine tuning liquidity sweep


---

## Backtest: 2025-12-06 14:51:36

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-24 (~1 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`
- **`MemecoinMoonshotHunter`:** `risk_per_trade=0.015`, `risk_per_trade=0.015`, `volume_spike_multiplier=5`, `rsi_threshold=75`, `breakout_window=14`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=3.0`, `sl_multiplier=2.2`, `rsi_divergence_window=5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `ZENUSDT, BCHUSDT, ETCUSDT, TAOUSDT, 1000BONKUSDT...`
- **Minggu 42:** `BCHUSDT, ETCUSDT, TAOUSDT, 1000BONKUSDT, TRXUSDT...`
- **Minggu 43:** `ETCUSDT, ARBUSDT, AAVEUSDT, ICPUSDT, DASHUSDT...`
- **Minggu 44:** `ZENUSDT, BCHUSDT, TRXUSDT, ARBUSDT, WLDUSDT...`
- **Minggu 45:** `BCHUSDT, ETCUSDT, 1000BONKUSDT, TRXUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.4 | $7.24 | 10 | 70.00% |
| `MemecoinMoonshotHunter`     | 0.3 | $0.00 | 0 | N/A |
| `LongOnlyCorrectionHunter`   | 0.3 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $82.24                     |
| **Net Profit**    | **$7.24 (+9.65%)** |
| Total Trades      | 10                         |
| Win Rate          | 70.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 10 trades (70.00%)             |
| Profit Factor     | 2.92                       |
| Max Drawdown      | 1.99%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   Kondisi market saat ini
