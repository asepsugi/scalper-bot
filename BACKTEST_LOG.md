
---

## Backtest: 2025-12-08 21:11:36

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-11-23 (~3 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `VIRTUALUSDT, NEARUSDT, OPUSDT, XLMUSDT, ICPUSDT...`
- **Minggu 33:** `VIRTUALUSDT, NEARUSDT, OPUSDT, DOTUSDT, TIAUSDT...`
- **Minggu 34:** `NEARUSDT, OPUSDT, XLMUSDT, APTUSDT, ICPUSDT...`
- **Minggu 35:** `VIRTUALUSDT, DOTUSDT, CRVUSDT, XLMUSDT, APTUSDT...`
- **Minggu 36:** `NEARUSDT, OPUSDT, XLMUSDT, APTUSDT, 1000PEPEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $11.76 | 17 | 47.06% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $86.76                     |
| **Net Profit**    | **$11.76 (+15.68%)** |
| Total Trades      | 17                         |
| Win Rate          | 47.06%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 17 trades (47.06%)             |
| Profit Factor     | 1.70                       |
| Max Drawdown      | 11.62%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 18:39:49

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-23 (~1 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `WLFIUSDT, NEARUSDT, VIRTUALUSDT, PENGUUSDT, ZENUSDT...`
- **Minggu 42:** `CRVUSDT, VIRTUALUSDT, ZENUSDT, TAOUSDT, BCHUSDT...`
- **Minggu 43:** `WLFIUSDT, ARBUSDT, VIRTUALUSDT, PENGUUSDT, PUMPUSDT...`
- **Minggu 44:** `PAXGUSDT, WLFIUSDT, ARBUSDT, VIRTUALUSDT, PUMPUSDT...`
- **Minggu 45:** `CRVUSDT, ARBUSDT, PENGUUSDT, PUMPUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $23.93 | 12 | 66.67% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $98.93                     |
| **Net Profit**    | **$23.93 (+31.91%)** |
| Total Trades      | 12                         |
| Win Rate          | 66.67%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 12 trades (66.67%)             |
| Profit Factor     | 3.83                       |
| Max Drawdown      | 4.65%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 18:12:06

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 15000
-   **Periode:** 2025-10-23 s/d 2025-12-07 (~1 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 43:** `DOTUSDT, TRUMPUSDT, XPLUSDT, HBARUSDT, 1000LUNCUSDT...`
- **Minggu 44:** `DOTUSDT, MOODENGUSDT, XNYUSDT, XPLUSDT, HBARUSDT...`
- **Minggu 45:** `TURBOUSDT, DOTUSDT, ENAUSDT, XPLUSDT, HBARUSDT...`
- **Minggu 46:** `TURBOUSDT, XNYUSDT, HBARUSDT, 1000LUNCUSDT, BCHUSDT...`
- **Minggu 47:** `TURBOUSDT, DOTUSDT, HBARUSDT, BCHUSDT, AAVEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-71.19 | 7 | 14.29% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $3.81                     |
| **Net Profit**    | **$-71.19 (-94.92%)** |
| Total Trades      | 7                         |
| Win Rate          | 14.29%                     |
|  - Long Win Rate  | 1 trades (0.00%)              |
|  - Short Win Rate | 6 trades (16.67%)             |
| Profit Factor     | 0.00                       |
| Max Drawdown      | 12.89%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 16:23:25

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 15000
-   **Periode:** 2025-10-30 s/d 2025-11-04 (~6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 43:** `FHEUSDT, PIPPINUSDT`
- **Minggu 44:** `FHEUSDT, PIPPINUSDT`
- **Minggu 45:** `FHEUSDT, PIPPINUSDT`
- **Minggu 46:** `FHEUSDT, PIPPINUSDT`
- **Minggu 47:** `BEATUSDT, PIPPINUSDT, PIEVERSEUSDT, FHEUSDT`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-1.54 | 1 | 0.00% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $73.46                     |
| **Net Profit**    | **$-1.54 (-2.06%)** |
| Total Trades      | 1                         |
| Win Rate          | 0.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 1 trades (0.00%)             |
| Profit Factor     | 0.00                       |
| Max Drawdown      | 0.00%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 16:14:19

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-23 (~1 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `ASTERUSDT, APTUSDT, PIPPINUSDT, HUSDT, 1000BONKUSDT...`
- **Minggu 42:** `CRVUSDT, TIAUSDT, APTUSDT, HUSDT, XPLUSDT...`
- **Minggu 43:** `ASTERUSDT, TIAUSDT, LTCUSDT, SUIUSDT, ARBUSDT...`
- **Minggu 44:** `ASTERUSDT, SUIUSDT, PIPPINUSDT, XPLUSDT, ARBUSDT...`
- **Minggu 45:** `CRVUSDT, LTCUSDT, SUIUSDT, PIPPINUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $23.93 | 12 | 66.67% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $98.93                     |
| **Net Profit**    | **$23.93 (+31.91%)** |
| Total Trades      | 12                         |
| Win Rate          | 66.67%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 12 trades (66.67%)             |
| Profit Factor     | 3.83                       |
| Max Drawdown      | 4.65%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 15:47:48

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-23 (~1 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `FETUSDT, HUSDT, 1000BONKUSDT, NEARUSDT, PIPPINUSDT...`
- **Minggu 42:** `HBARUSDT, FETUSDT, CRVUSDT, HUSDT, 1000BONKUSDT...`
- **Minggu 43:** `HBARUSDT, ICPUSDT, TIAUSDT, 1000PEPEUSDT, XPLUSDT...`
- **Minggu 44:** `FETUSDT, ICPUSDT, PIPPINUSDT, XPLUSDT, DASHUSDT...`
- **Minggu 45:** `HBARUSDT, CRVUSDT, 1000BONKUSDT, ICPUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $13.93 | 12 | 66.67% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $88.93                     |
| **Net Profit**    | **$13.93 (+18.57%)** |
| Total Trades      | 12                         |
| Win Rate          | 66.67%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 12 trades (66.67%)             |
| Profit Factor     | 4.02                       |
| Max Drawdown      | 2.79%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 15:27:08

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-23 (~1 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=12`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `PENGUUSDT, WLFIUSDT, 1000PEPEUSDT, ZENUSDT, ASTERUSDT...`
- **Minggu 42:** `GIGGLEUSDT, CRVUSDT, ZENUSDT, TIAUSDT, TRXUSDT...`
- **Minggu 43:** `LTCUSDT, PENGUUSDT, DASHUSDT, WLFIUSDT, 1000PEPEUSDT...`
- **Minggu 44:** `GIGGLEUSDT, DASHUSDT, WLFIUSDT, ZENUSDT, ASTERUSDT...`
- **Minggu 45:** `LTCUSDT, PENGUUSDT, CRVUSDT, 1000PEPEUSDT, TRXUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $12.59 | 10 | 70.00% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $87.59                     |
| **Net Profit**    | **$12.59 (+16.79%)** |
| Total Trades      | 10                         |
| Win Rate          | 70.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 10 trades (70.00%)             |
| Profit Factor     | 4.90                       |
| Max Drawdown      | 1.26%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-08 15:07:44

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-23 (~1 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `WIFUSDT, 1000PEPEUSDT, ZENUSDT, BCHUSDT, PIPPINUSDT...`
- **Minggu 42:** `WLDUSDT, WIFUSDT, BCHUSDT, ZENUSDT, TRUMPUSDT...`
- **Minggu 43:** `1000PEPEUSDT, TRUMPUSDT, XPLUSDT, DOTUSDT, AAVEUSDT...`
- **Minggu 44:** `WLDUSDT, ZENUSDT, BCHUSDT, HYPEUSDT, TRUMPUSDT...`
- **Minggu 45:** `WIFUSDT, 1000PEPEUSDT, BCHUSDT, HYPEUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $8.73 | 14 | 57.14% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $83.73                     |
| **Net Profit**    | **$8.73 (+11.65%)** |
| Total Trades      | 14                         |
| Win Rate          | 57.14%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 14 trades (57.14%)             |
| Profit Factor     | 2.25                       |
| Max Drawdown      | 4.46%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 13:17:58

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-12-02 (~1 Bulan 24 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `HEMIUSDT, PNUTUSDT, SWARMSUSDT, ENAUSDT, AAVEUSDT...`
- **Minggu 42:** `PNUTUSDT, PUMPUSDT, GIGGLEUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 43:** `HEMIUSDT, PNUTUSDT, PUMPUSDT, SWARMSUSDT, ENAUSDT...`
- **Minggu 44:** `HEMIUSDT, PUMPUSDT, SWARMSUSDT, HYPEUSDT, GIGGLEUSDT...`
- **Minggu 45:** `PNUTUSDT, PUMPUSDT, SWARMSUSDT, HYPEUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-6.71 | 22 | 36.36% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $68.29                     |
| **Net Profit**    | **$-6.71 (-8.95%)** |
| Total Trades      | 22                         |
| Win Rate          | 36.36%                     |
|  - Long Win Rate  | 1 trades (0.00%)              |
|  - Short Win Rate | 21 trades (38.10%)             |
| Profit Factor     | 0.67                       |
| Max Drawdown      | 15.56%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 12:55:52

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-12-05 (~1 Bulan 27 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=10`, `volume_spike_multiplier=3.4`, `candle_body_ratio=0.58`, `anti_chase_pct=0.09`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `NOTUSDT, TRXUSDT, SWARMSUSDT, NEARUSDT, APTUSDT...`
- **Minggu 42:** `NOTUSDT, PUFFERUSDT, TRXUSDT, LUNA2USDT, GIGGLEUSDT...`
- **Minggu 43:** `LUNA2USDT, SWARMSUSDT, PUMPUSDT, LTCUSDT, ACEUSDT...`
- **Minggu 44:** `NOTUSDT, PUFFERUSDT, HYPEUSDT, TRXUSDT, SWARMSUSDT...`
- **Minggu 45:** `HYPEUSDT, TRXUSDT, SWARMSUSDT, 1000PEPEUSDT, PUMPUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-6.46 | 31 | 35.48% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $68.54                     |
| **Net Profit**    | **$-6.46 (-8.62%)** |
| Total Trades      | 31                         |
| Win Rate          | 35.48%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 29 trades (37.93%)             |
| Profit Factor     | 0.83                       |
| Max Drawdown      | 18.41%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 12:18:39

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-23 (~1 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=10`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.09`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `ASTERUSDT, TAOUSDT, PIPPINUSDT, FARTCOINUSDT, ENAUSDT...`
- **Minggu 42:** `ASTERUSDT, TAOUSDT, FARTCOINUSDT, XPLUSDT, GIGGLEUSDT...`
- **Minggu 43:** `ASTERUSDT, TAOUSDT, PIPPINUSDT, FARTCOINUSDT, ENAUSDT...`
- **Minggu 44:** `ASTERUSDT, PIPPINUSDT, XPLUSDT, GIGGLEUSDT, GRIFFAINUSDT...`
- **Minggu 45:** `PIPPINUSDT, ENAUSDT, 1000SHIBUSDT, PENGUUSDT, TRXUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-0.77 | 21 | 33.33% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $74.23                     |
| **Net Profit**    | **$-0.77 (-1.03%)** |
| Total Trades      | 21                         |
| Win Rate          | 33.33%                     |
|  - Long Win Rate  | 1 trades (0.00%)              |
|  - Short Win Rate | 20 trades (35.00%)             |
| Profit Factor     | 0.97                       |
| Max Drawdown      | 15.96%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 11:46:14

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-25 (~1 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `PUMPUSDT, THEUSDT, PENGUUSDT, LTCUSDT, 1000SHIBUSDT...`
- **Minggu 42:** `SAPIENUSDT, PUMPUSDT, LTCUSDT, NEARUSDT, MONUSDT...`
- **Minggu 43:** `PUMPUSDT, THEUSDT, PENGUUSDT, LTCUSDT, 1000SHIBUSDT...`
- **Minggu 44:** `SAPIENUSDT, PUMPUSDT, USTCUSDT, TRADOORUSDT, MOODENGUSDT...`
- **Minggu 45:** `PUMPUSDT, THEUSDT, PENGUUSDT, LTCUSDT, USTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $6.77 | 19 | 47.37% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $81.77                     |
| **Net Profit**    | **$6.77 (+9.02%)** |
| Total Trades      | 19                         |
| Win Rate          | 47.37%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 19 trades (47.37%)             |
| Profit Factor     | 1.74                       |
| Max Drawdown      | 5.02%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 11:14:48

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-10-10 s/d 2025-11-25 (~1 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 41:** `ENAUSDT, PIPPINUSDT, SWARMSUSDT, WIFUSDT, NEARUSDT...`
- **Minggu 42:** `SAPIENUSDT, WIFUSDT, GIGGLEUSDT, FARTCOINUSDT, MOODENGUSDT...`
- **Minggu 43:** `ENAUSDT, HMSTRUSDT, PIPPINUSDT, SWARMSUSDT, FARTCOINUSDT...`
- **Minggu 44:** `SAPIENUSDT, HMSTRUSDT, PIPPINUSDT, SWARMSUSDT, GIGGLEUSDT...`
- **Minggu 45:** `ENAUSDT, PIPPINUSDT, SWARMSUSDT, WIFUSDT, MOODENGUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $5.39 | 18 | 44.44% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $80.39                     |
| **Net Profit**    | **$5.39 (+7.18%)** |
| Total Trades      | 18                         |
| Win Rate          | 44.44%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 18 trades (44.44%)             |
| Profit Factor     | 1.60                       |
| Max Drawdown      | 5.02%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 10:54:57

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2024-05-30 s/d 2024-07-02 (~1 Bulan 4 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 19:** `BCHUSDT, NEARUSDT, 1000LUNCUSDT, ACEUSDT, LTCUSDT...`
- **Minggu 20:** `BCHUSDT, NEARUSDT, 1000LUNCUSDT, ACEUSDT, LTCUSDT...`
- **Minggu 21:** `BCHUSDT, NEARUSDT, 1000LUNCUSDT, ACEUSDT, LTCUSDT...`
- **Minggu 22:** `BCHUSDT, NEARUSDT, 1000LUNCUSDT, ACEUSDT, LTCUSDT...`
- **Minggu 23:** `BCHUSDT, NEARUSDT, 1000LUNCUSDT, ACEUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-0.81 | 4 | 50.00% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $74.19                     |
| **Net Profit**    | **$-0.81 (-1.08%)** |
| Total Trades      | 4                         |
| Win Rate          | 50.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 4 trades (50.00%)             |
| Profit Factor     | 0.83                       |
| Max Drawdown      | 5.87%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 10:44:00

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2022-05-09 s/d 2022-12-02 (~6 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 18:** `TRXUSDT, AAVEUSDT, BCHUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 19:** `TRXUSDT, AAVEUSDT, BCHUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 20:** `TRXUSDT, AAVEUSDT, BCHUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 21:** `TRXUSDT, AAVEUSDT, BCHUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 22:** `TRXUSDT, AAVEUSDT, BCHUSDT, LTCUSDT, NEARUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.46 | 7 | 85.71% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.46                     |
| **Net Profit**    | **$4.46 (+5.95%)** |
| Total Trades      | 7                         |
| Win Rate          | 85.71%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 7 trades (85.71%)             |
| Profit Factor     | 2.05                       |
| Max Drawdown      | 5.07%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-07 10:15:25

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-08 s/d 2021-04-27 (~3 Bulan 20 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.012`, `breakout_window=15`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.8`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `BCHUSDT, DOTUSDT, TRXUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 2:** `BCHUSDT, DOTUSDT, TRXUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 3:** `BCHUSDT, DOTUSDT, TRXUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 4:** `BCHUSDT, DOTUSDT, TRXUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 5:** `BCHUSDT, DOTUSDT, TRXUSDT, AAVEUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-10.39 | 12 | 33.33% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $64.61                     |
| **Net Profit**    | **$-10.39 (-13.86%)** |
| Total Trades      | 12                         |
| Win Rate          | 33.33%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 12 trades (33.33%)             |
| Profit Factor     | 0.33                       |
| Max Drawdown      | 14.65%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 11 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


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
