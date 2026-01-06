
---

## Backtest: 2026-01-06 23:56:53

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2022-01-03 (~1 Tahun 0 Bulan)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `DASHUSDT, LTCUSDT, 1000SHIBUSDT, XLMUSDT, UNIUSDT...`
- **Minggu 2:** `DASHUSDT, LTCUSDT, FILUSDT, UNIUSDT, XLMUSDT...`
- **Minggu 3:** `DASHUSDT, LTCUSDT, FILUSDT, UNIUSDT, XLMUSDT...`
- **Minggu 4:** `DASHUSDT, LTCUSDT, FILUSDT, UNIUSDT, XLMUSDT...`
- **Minggu 5:** `DASHUSDT, LTCUSDT, XLMUSDT, UNIUSDT, FILUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-7.48 | 72 | 37.50% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $2.93 | 11 | 63.64% |
| `RSIDivergenceHunter` | 0.25 | $-26.89 | 400 | 41.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $43.55                     |
| **Net Profit**    | **$-31.45 (-41.93%)** |
| Total Trades      | 483                         |
| Win Rate          | 40.99%                     |
|  - Long Win Rate  | 285 trades (40.00%)              |
|  - Short Win Rate | 198 trades (42.42%)             |
| Profit Factor     | 0.87                       |
| Max Drawdown      | 60.84%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 23:41:16

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-03-31 (~2 Bulan 27 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `UNIUSDT, XLMUSDT, DASHUSDT, DOTUSDT, NEARUSDT...`
- **Minggu 2:** `UNIUSDT, XLMUSDT, DASHUSDT, NEARUSDT, DOTUSDT...`
- **Minggu 3:** `UNIUSDT, XLMUSDT, DASHUSDT, NEARUSDT, DOTUSDT...`
- **Minggu 4:** `UNIUSDT, XLMUSDT, DASHUSDT, DOTUSDT, NEARUSDT...`
- **Minggu 5:** `UNIUSDT, XLMUSDT, DASHUSDT, DOTUSDT, NEARUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-2.72 | 33 | 39.39% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.25 | $-9.96 | 66 | 37.88% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $62.31                     |
| **Net Profit**    | **$-12.69 (-16.91%)** |
| Total Trades      | 99                         |
| Win Rate          | 38.38%                     |
|  - Long Win Rate  | 35 trades (34.29%)              |
|  - Short Win Rate | 64 trades (40.62%)             |
| Profit Factor     | 0.79                       |
| Max Drawdown      | 22.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 23:36:05

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-03-31 (~2 Bulan 27 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `DOTUSDT, UNIUSDT, AAVEUSDT, FILUSDT, LTCUSDT...`
- **Minggu 2:** `DOTUSDT, UNIUSDT, AAVEUSDT, FILUSDT, LTCUSDT...`
- **Minggu 3:** `DOTUSDT, UNIUSDT, AAVEUSDT, FILUSDT, LTCUSDT...`
- **Minggu 4:** `DOTUSDT, UNIUSDT, AAVEUSDT, FILUSDT, LTCUSDT...`
- **Minggu 5:** `DOTUSDT, UNIUSDT, AAVEUSDT, FILUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-3.03 | 31 | 35.48% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.35 | 2 | 50.00% |
| `RSIDivergenceHunter` | 0.25 | $-1.84 | 54 | 40.74% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $70.48                     |
| **Net Profit**    | **$-4.52 (-6.02%)** |
| Total Trades      | 87                         |
| Win Rate          | 39.08%                     |
|  - Long Win Rate  | 30 trades (30.00%)              |
|  - Short Win Rate | 57 trades (43.86%)             |
| Profit Factor     | 0.91                       |
| Max Drawdown      | 17.25%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 23:28:28

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-15 (~12 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `FILUSDT, NEARUSDT, UNIUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 2:** `FILUSDT, NEARUSDT, UNIUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 3:** `FILUSDT, NEARUSDT, UNIUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 4:** `FILUSDT, NEARUSDT, UNIUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 5:** `FILUSDT, NEARUSDT, UNIUSDT, XLMUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-1.29 | 8 | 25.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $1.42 | 1 | 100.00% |
| `RSIDivergenceHunter` | 0.25 | $-3.18 | 11 | 27.27% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $71.95                     |
| **Net Profit**    | **$-3.05 (-4.06%)** |
| Total Trades      | 20                         |
| Win Rate          | 30.00%                     |
|  - Long Win Rate  | 8 trades (25.00%)              |
|  - Short Win Rate | 12 trades (33.33%)             |
| Profit Factor     | 0.74                       |
| Max Drawdown      | 7.49%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 23:25:35

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-17 (~14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `UNIUSDT, NEARUSDT, BCHUSDT, LTCUSDT, XLMUSDT...`
- **Minggu 2:** `UNIUSDT, NEARUSDT, BCHUSDT, LTCUSDT, XLMUSDT...`
- **Minggu 3:** `UNIUSDT, NEARUSDT, BCHUSDT, LTCUSDT, XLMUSDT...`
- **Minggu 4:** `UNIUSDT, NEARUSDT, BCHUSDT, LTCUSDT, XLMUSDT...`
- **Minggu 5:** `UNIUSDT, NEARUSDT, BCHUSDT, LTCUSDT, XLMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-1.88 | 9 | 22.22% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $1.42 | 1 | 100.00% |
| `RSIDivergenceHunter` | 0.25 | $-4.56 | 10 | 20.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $69.98                     |
| **Net Profit**    | **$-5.02 (-6.69%)** |
| Total Trades      | 20                         |
| Win Rate          | 25.00%                     |
|  - Long Win Rate  | 8 trades (25.00%)              |
|  - Short Win Rate | 12 trades (25.00%)             |
| Profit Factor     | 0.58                       |
| Max Drawdown      | 7.49%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 23:22:26

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-15 (~12 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `LTCUSDT, XLMUSDT, NEARUSDT, UNIUSDT, BCHUSDT...`
- **Minggu 2:** `LTCUSDT, XLMUSDT, NEARUSDT, UNIUSDT, BCHUSDT...`
- **Minggu 3:** `LTCUSDT, XLMUSDT, NEARUSDT, UNIUSDT, BCHUSDT...`
- **Minggu 4:** `LTCUSDT, XLMUSDT, NEARUSDT, UNIUSDT, BCHUSDT...`
- **Minggu 5:** `LTCUSDT, XLMUSDT, NEARUSDT, UNIUSDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $0.60 | 10 | 40.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.25 | $-2.29 | 10 | 30.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $73.31                     |
| **Net Profit**    | **$-1.69 (-2.26%)** |
| Total Trades      | 20                         |
| Win Rate          | 35.00%                     |
|  - Long Win Rate  | 7 trades (28.57%)              |
|  - Short Win Rate | 13 trades (38.46%)             |
| Profit Factor     | 0.84                       |
| Max Drawdown      | 8.26%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 23:10:08

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-15 (~12 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `LTCUSDT, NEARUSDT, BCHUSDT, UNIUSDT, AAVEUSDT...`
- **Minggu 2:** `LTCUSDT, NEARUSDT, BCHUSDT, UNIUSDT, AAVEUSDT...`
- **Minggu 3:** `LTCUSDT, NEARUSDT, BCHUSDT, UNIUSDT, AAVEUSDT...`
- **Minggu 4:** `LTCUSDT, NEARUSDT, BCHUSDT, UNIUSDT, AAVEUSDT...`
- **Minggu 5:** `LTCUSDT, NEARUSDT, BCHUSDT, UNIUSDT, AAVEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-1.91 | 9 | 22.22% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $1.45 | 1 | 100.00% |
| `RSIDivergenceHunter` | 0.25 | $-1.71 | 10 | 30.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $72.83                     |
| **Net Profit**    | **$-2.17 (-2.89%)** |
| Total Trades      | 20                         |
| Win Rate          | 30.00%                     |
|  - Long Win Rate  | 8 trades (25.00%)              |
|  - Short Win Rate | 12 trades (33.33%)             |
| Profit Factor     | 0.80                       |
| Max Drawdown      | 5.58%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 22:57:24

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-15 (~12 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `AAVEUSDT, DOTUSDT, UNIUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 2:** `AAVEUSDT, DOTUSDT, UNIUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 3:** `AAVEUSDT, DOTUSDT, UNIUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 4:** `AAVEUSDT, DOTUSDT, UNIUSDT, LTCUSDT, NEARUSDT...`
- **Minggu 5:** `AAVEUSDT, DOTUSDT, UNIUSDT, LTCUSDT, NEARUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-0.03 | 11 | 36.36% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.25 | $-0.83 | 9 | 33.33% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $74.14                     |
| **Net Profit**    | **$-0.86 (-1.15%)** |
| Total Trades      | 20                         |
| Win Rate          | 35.00%                     |
|  - Long Win Rate  | 6 trades (33.33%)              |
|  - Short Win Rate | 14 trades (35.71%)             |
| Profit Factor     | 0.91                       |
| Max Drawdown      | 8.26%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 22:37:17

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-15 (~12 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `XLMUSDT, UNIUSDT, LTCUSDT, BCHUSDT, DOTUSDT...`
- **Minggu 2:** `XLMUSDT, BCHUSDT, LTCUSDT, DOTUSDT, UNIUSDT...`
- **Minggu 3:** `XLMUSDT, UNIUSDT, BCHUSDT, LTCUSDT, DOTUSDT...`
- **Minggu 4:** `XLMUSDT, BCHUSDT, LTCUSDT, DOTUSDT, UNIUSDT...`
- **Minggu 5:** `XLMUSDT, UNIUSDT, BCHUSDT, LTCUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-1.92 | 9 | 22.22% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $1.43 | 1 | 100.00% |
| `RSIDivergenceHunter` | 0.25 | $-3.01 | 11 | 27.27% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $71.50                     |
| **Net Profit**    | **$-3.50 (-4.67%)** |
| Total Trades      | 21                         |
| Win Rate          | 28.57%                     |
|  - Long Win Rate  | 8 trades (25.00%)              |
|  - Short Win Rate | 13 trades (30.77%)             |
| Profit Factor     | 0.70                       |
| Max Drawdown      | 6.98%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 22:21:33

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-11 (~8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `DOTUSDT, FILUSDT, 1000SHIBUSDT, XLMUSDT, NEARUSDT...`
- **Minggu 2:** `DOTUSDT, FILUSDT, XLMUSDT, NEARUSDT, LTCUSDT...`
- **Minggu 3:** `DOTUSDT, FILUSDT, XLMUSDT, NEARUSDT, LTCUSDT...`
- **Minggu 4:** `DOTUSDT, FILUSDT, XLMUSDT, NEARUSDT, LTCUSDT...`
- **Minggu 5:** `DOTUSDT, FILUSDT, XLMUSDT, NEARUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $2.88 | 9 | 55.56% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.50 | 2 | 50.00% |
| `RSIDivergenceHunter` | 0.25 | $-6.44 | 9 | 11.11% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $71.94                     |
| **Net Profit**    | **$-3.06 (-4.08%)** |
| Total Trades      | 20                         |
| Win Rate          | 35.00%                     |
|  - Long Win Rate  | 4 trades (0.00%)              |
|  - Short Win Rate | 16 trades (43.75%)             |
| Profit Factor     | 0.73                       |
| Max Drawdown      | 8.94%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 22:02:23

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-10 (~7 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=False`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `BCHUSDT, XLMUSDT, NEARUSDT, LTCUSDT, 1000SHIBUSDT...`
- **Minggu 2:** `BCHUSDT, NEARUSDT, XLMUSDT, LTCUSDT, DOTUSDT...`
- **Minggu 3:** `BCHUSDT, NEARUSDT, XLMUSDT, LTCUSDT, DOTUSDT...`
- **Minggu 4:** `BCHUSDT, NEARUSDT, XLMUSDT, LTCUSDT, DOTUSDT...`
- **Minggu 5:** `BCHUSDT, XLMUSDT, NEARUSDT, LTCUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-2.13 | 3 | 0.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $-0.89 | 1 | 0.00% |
| `RSIDivergenceHunter` | 0.25 | $-2.03 | 4 | 25.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $69.94                     |
| **Net Profit**    | **$-5.06 (-6.74%)** |
| Total Trades      | 8                         |
| Win Rate          | 12.50%                     |
|  - Long Win Rate  | 1 trades (0.00%)              |
|  - Short Win Rate | 7 trades (14.29%)             |
| Profit Factor     | 0.13                       |
| Max Drawdown      | 5.99%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 21:56:39

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-09 (~6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `XLMUSDT, NEARUSDT, BCHUSDT, AAVEUSDT, HBARUSDT...`
- **Minggu 2:** `BCHUSDT, NEARUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 3:** `BCHUSDT, NEARUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 4:** `BCHUSDT, NEARUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 5:** `XLMUSDT, BCHUSDT, NEARUSDT, AAVEUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-2.13 | 3 | 0.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $-0.89 | 1 | 0.00% |
| `RSIDivergenceHunter` | 0.25 | $-2.48 | 4 | 25.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $69.50                     |
| **Net Profit**    | **$-5.50 (-7.34%)** |
| Total Trades      | 8                         |
| Win Rate          | 12.50%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 8 trades (12.50%)             |
| Profit Factor     | 0.12                       |
| Max Drawdown      | 6.59%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 21:24:09

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-06-07 s/d 2021-06-10 (~4 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `HBARUSDT, 1000SHIBUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 24:** `HBARUSDT, 1000SHIBUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 25:** `HBARUSDT, 1000SHIBUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 26:** `HBARUSDT, 1000SHIBUSDT, XLMUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 27:** `HBARUSDT, XLMUSDT, AAVEUSDT, LTCUSDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-0.13 | 1 | 0.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.25 | $8.18 | 8 | 75.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $83.06                     |
| **Net Profit**    | **$8.06 (+10.74%)** |
| Total Trades      | 9                         |
| Win Rate          | 66.67%                     |
|  - Long Win Rate  | 2 trades (50.00%)              |
|  - Short Win Rate | 7 trades (71.43%)             |
| Profit Factor     | 2.60                       |
| Max Drawdown      | 4.53%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-06 20:12:57

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-06-07 s/d 2021-06-09 (~3 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=27`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `NEARUSDT, BCHUSDT, DOTUSDT, HBARUSDT, LTCUSDT...`
- **Minggu 24:** `NEARUSDT, DOTUSDT, HBARUSDT, LTCUSDT, FILUSDT...`
- **Minggu 25:** `NEARUSDT, DOTUSDT, HBARUSDT, LTCUSDT, FILUSDT...`
- **Minggu 26:** `NEARUSDT, BCHUSDT, DOTUSDT, HBARUSDT, LTCUSDT...`
- **Minggu 27:** `NEARUSDT, DOTUSDT, HBARUSDT, LTCUSDT, FILUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-0.13 | 1 | 0.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.25 | $10.56 | 8 | 75.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $85.43                     |
| **Net Profit**    | **$10.43 (+13.91%)** |
| Total Trades      | 9                         |
| Win Rate          | 66.67%                     |
|  - Long Win Rate  | 2 trades (50.00%)              |
|  - Short Win Rate | 7 trades (71.43%)             |
| Profit Factor     | 4.91                       |
| Max Drawdown      | 1.80%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 22:45:45

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2021-01-09 (~6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=27`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `TRXUSDT, DOTUSDT, AAVEUSDT, NEARUSDT, HBARUSDT...`
- **Minggu 2:** `DOTUSDT, TRXUSDT, AAVEUSDT, NEARUSDT, FILUSDT...`
- **Minggu 3:** `TRXUSDT, AAVEUSDT, DOTUSDT, NEARUSDT, FILUSDT...`
- **Minggu 4:** `DOTUSDT, TRXUSDT, AAVEUSDT, NEARUSDT, FILUSDT...`
- **Minggu 5:** `TRXUSDT, DOTUSDT, AAVEUSDT, NEARUSDT, FILUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-1.76 | 3 | 0.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $-1.03 | 1 | 0.00% |
| `RSIDivergenceHunter` | 0.25 | $-2.21 | 4 | 25.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $70.00                     |
| **Net Profit**    | **$-5.00 (-6.67%)** |
| Total Trades      | 8                         |
| Win Rate          | 12.50%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 8 trades (12.50%)             |
| Profit Factor     | 0.31                       |
| Max Drawdown      | 8.11%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 22:19:03

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2022-01-04 (~1 Tahun 0 Bulan)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.01`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=27`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.01`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `DOTUSDT, TRXUSDT, NEARUSDT, BCHUSDT, HBARUSDT...`
- **Minggu 2:** `TRXUSDT, NEARUSDT, BCHUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 3:** `TRXUSDT, NEARUSDT, BCHUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 4:** `TRXUSDT, NEARUSDT, BCHUSDT, XLMUSDT, LTCUSDT...`
- **Minggu 5:** `TRXUSDT, NEARUSDT, BCHUSDT, XLMUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-3.84 | 51 | 33.33% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $6.02 | 20 | 55.00% |
| `RSIDivergenceHunter` | 0.25 | $-58.30 | 352 | 35.23% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $18.88                     |
| **Net Profit**    | **$-56.12 (-74.82%)** |
| Total Trades      | 423                         |
| Win Rate          | 35.93%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 423 trades (35.93%)             |
| Profit Factor     | 0.65                       |
| Max Drawdown      | 78.89%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 21:06:34

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2021-01-04 s/d 2022-01-01 (~12 Bulan 3 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.02`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `1000SHIBUSDT, TRXUSDT, AAVEUSDT, UNIUSDT, XLMUSDT...`
- **Minggu 2:** `TRXUSDT, AAVEUSDT, UNIUSDT, XLMUSDT, NEARUSDT`
- **Minggu 3:** `TRXUSDT, AAVEUSDT, UNIUSDT, XLMUSDT, NEARUSDT`
- **Minggu 4:** `TRXUSDT, AAVEUSDT, UNIUSDT, XLMUSDT, NEARUSDT`
- **Minggu 5:** `TRXUSDT, AAVEUSDT, UNIUSDT, XLMUSDT, NEARUSDT`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-14.56 | 38 | 23.68% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $14.02 | 16 | 62.50% |
| `RSIDivergenceHunter` | 0.25 | $-55.73 | 256 | 39.06% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $18.72                     |
| **Net Profit**    | **$-56.28 (-75.04%)** |
| Total Trades      | 310                         |
| Win Rate          | 38.39%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 310 trades (38.39%)             |
| Profit Factor     | 0.76                       |
| Max Drawdown      | 78.52%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 9 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 19:23:22

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2022-01-01 s/d 2023-01-04 (~1 Tahun 0 Bulan)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.02`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 1:** `LTCUSDT, NEARUSDT, XLMUSDT, BCHUSDT, TRXUSDT...`
- **Minggu 2:** `LTCUSDT, NEARUSDT, XLMUSDT, TRXUSDT, BCHUSDT...`
- **Minggu 3:** `LTCUSDT, NEARUSDT, XLMUSDT, TRXUSDT, BCHUSDT...`
- **Minggu 4:** `LTCUSDT, NEARUSDT, XLMUSDT, TRXUSDT, BCHUSDT...`
- **Minggu 5:** `LTCUSDT, NEARUSDT, XLMUSDT, BCHUSDT, TRXUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-7.01 | 18 | 27.78% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $-6.44 | 20 | 30.00% |
| `RSIDivergenceHunter` | 0.25 | $-26.48 | 411 | 45.01% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $35.07                     |
| **Net Profit**    | **$-39.93 (-53.24%)** |
| Total Trades      | 449                         |
| Win Rate          | 43.65%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 449 trades (43.65%)             |
| Profit Factor     | 0.90                       |
| Max Drawdown      | 73.82%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 18 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 17:02:34

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.02`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `FILUSDT, WIFUSDT, FETUSDT, PENGUUSDT, TIAUSDT...`
- **Minggu 24:** `WIFUSDT, FETUSDT, PENGUUSDT, TIAUSDT, ENAUSDT...`
- **Minggu 25:** `FETUSDT, PENGUUSDT, TIAUSDT, UNIUSDT, ENAUSDT...`
- **Minggu 26:** `FILUSDT, WIFUSDT, FETUSDT, PENGUUSDT, PAXGUSDT...`
- **Minggu 27:** `FETUSDT, PENGUUSDT, PAXGUSDT, UNIUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $25.08 | 36 | 50.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $-1.29 | 9 | 33.33% |
| `RSIDivergenceHunter` | 0.25 | $31.15 | 130 | 51.54% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $129.94                     |
| **Net Profit**    | **$54.94 (+73.25%)** |
| Total Trades      | 175                         |
| Win Rate          | 50.29%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 175 trades (50.29%)             |
| Profit Factor     | 1.33                       |
| Max Drawdown      | 56.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 16:59:40

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-11-07 (~5 Bulan 9 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.02`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=25`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `AAVEUSDT, ARBUSDT, XLMUSDT, NEARUSDT, UNIUSDT...`
- **Minggu 24:** `AAVEUSDT, ARBUSDT, XLMUSDT, MOODENGUSDT, NEARUSDT...`
- **Minggu 25:** `AAVEUSDT, ARBUSDT, XLMUSDT, NEARUSDT, UNIUSDT...`
- **Minggu 26:** `ARBUSDT, MOODENGUSDT, NEARUSDT, UNIUSDT, 1000SHIBUSDT...`
- **Minggu 27:** `ARBUSDT, XLMUSDT, MOODENGUSDT, NEARUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.5 | $-5.25 | 32 | 43.75% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.15 | $-1.57 | 3 | 0.00% |
| `RSIDivergenceHunter` | 0.25 | $-19.47 | 106 | 43.40% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $48.71                     |
| **Net Profit**    | **$-26.29 (-35.06%)** |
| Total Trades      | 141                         |
| Win Rate          | 42.55%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 141 trades (42.55%)             |
| Profit Factor     | 0.81                       |
| Max Drawdown      | 55.68%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 20 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 16:42:06

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `ARBUSDT, LTCUSDT, TAOUSDT, TRXUSDT, DOTUSDT...`
- **Minggu 24:** `ARBUSDT, TAOUSDT, TRXUSDT, DOTUSDT, FETUSDT...`
- **Minggu 25:** `LTCUSDT, ARBUSDT, TAOUSDT, TRXUSDT, DOTUSDT...`
- **Minggu 26:** `ARBUSDT, TAOUSDT, TRXUSDT, DOTUSDT, FETUSDT...`
- **Minggu 27:** `ARBUSDT, LTCUSDT, TAOUSDT, TRXUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $30.89 | 36 | 50.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $0.27 | 8 | 37.50% |
| `RSIDivergenceHunter` | 0.2 | $27.06 | 114 | 51.75% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $133.22                     |
| **Net Profit**    | **$58.22 (+77.62%)** |
| Total Trades      | 158                         |
| Win Rate          | 50.63%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 158 trades (50.63%)             |
| Profit Factor     | 1.40                       |
| Max Drawdown      | 55.38%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 16:38:59

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.01`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `ARBUSDT, UNIUSDT, BCHUSDT, WLDUSDT, TAOUSDT...`
- **Minggu 24:** `ARBUSDT, IPUSDT, BCHUSDT, TAOUSDT, FETUSDT...`
- **Minggu 25:** `ARBUSDT, IPUSDT, UNIUSDT, BCHUSDT, WLDUSDT...`
- **Minggu 26:** `ARBUSDT, IPUSDT, UNIUSDT, TAOUSDT, FETUSDT...`
- **Minggu 27:** `ARBUSDT, IPUSDT, UNIUSDT, WLDUSDT, TAOUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $17.96 | 36 | 50.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-2.81 | 12 | 25.00% |
| `RSIDivergenceHunter` | 0.2 | $14.87 | 130 | 52.31% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $105.02                     |
| **Net Profit**    | **$30.02 (+40.02%)** |
| Total Trades      | 178                         |
| Win Rate          | 50.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 178 trades (50.00%)             |
| Profit Factor     | 1.19                       |
| Max Drawdown      | 56.21%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 16:36:31

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `BCHUSDT, TIAUSDT, NEARUSDT, 1000SHIBUSDT, SUIUSDT...`
- **Minggu 24:** `BCHUSDT, TIAUSDT, NEARUSDT, HBARUSDT, SUIUSDT...`
- **Minggu 25:** `BCHUSDT, TIAUSDT, NEARUSDT, HBARUSDT, 1000SHIBUSDT...`
- **Minggu 26:** `TIAUSDT, NEARUSDT, 1000SHIBUSDT, MYXUSDT, MOODENGUSDT...`
- **Minggu 27:** `NEARUSDT, 1000SHIBUSDT, MYXUSDT, MOODENGUSDT, PENGUUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $46.05 | 37 | 48.65% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $0.04 | 12 | 41.67% |
| `RSIDivergenceHunter` | 0.2 | $62.54 | 115 | 54.78% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $183.63                     |
| **Net Profit**    | **$108.63 (+144.84%)** |
| Total Trades      | 164                         |
| Win Rate          | 52.44%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 164 trades (52.44%)             |
| Profit Factor     | 1.55                       |
| Max Drawdown      | 48.42%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 16:30:30

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-15 (~6 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `WIFUSDT, 1000PEPEUSDT, TRXUSDT, BCHUSDT, AAVEUSDT...`
- **Minggu 24:** `WIFUSDT, 1000PEPEUSDT, TRXUSDT, VIRTUALUSDT, BCHUSDT...`
- **Minggu 25:** `TRXUSDT, VIRTUALUSDT, BCHUSDT, HBARUSDT, AAVEUSDT...`
- **Minggu 26:** `WIFUSDT, TRXUSDT, VIRTUALUSDT, PAXGUSDT, DOTUSDT...`
- **Minggu 27:** `1000PEPEUSDT, TRXUSDT, VIRTUALUSDT, PAXGUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $34.76 | 38 | 50.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-0.97 | 13 | 38.46% |
| `RSIDivergenceHunter` | 0.2 | $15.96 | 120 | 50.83% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $124.75                     |
| **Net Profit**    | **$49.75 (+66.33%)** |
| Total Trades      | 171                         |
| Win Rate          | 49.71%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 171 trades (49.71%)             |
| Profit Factor     | 1.30                       |
| Max Drawdown      | 56.56%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 16:04:20

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `WLDUSDT, 1000PEPEUSDT, WIFUSDT, LTCUSDT, 1000SHIBUSDT...`
- **Minggu 24:** `WLDUSDT, 1000PEPEUSDT, WIFUSDT, SUIUSDT, ARBUSDT...`
- **Minggu 25:** `WLDUSDT, LTCUSDT, 1000SHIBUSDT, ARBUSDT, HBARUSDT...`
- **Minggu 26:** `WIFUSDT, MYXUSDT, PAXGUSDT, 1000SHIBUSDT, ARBUSDT...`
- **Minggu 27:** `WLDUSDT, 1000PEPEUSDT, MYXUSDT, PAXGUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-21.98 | 36 | 41.67% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.2 | $29.94 | 89 | 56.18% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $82.96                     |
| **Net Profit**    | **$7.96 (+10.61%)** |
| Total Trades      | 125                         |
| Win Rate          | 52.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 125 trades (52.00%)             |
| Profit Factor     | 1.05                       |
| Max Drawdown      | 46.62%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 15:52:05

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-15 (~6 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `WIFUSDT, DOTUSDT, TIAUSDT, BCHUSDT, 1000FLOKIUSDT...`
- **Minggu 24:** `MOODENGUSDT, WIFUSDT, DOTUSDT, TIAUSDT, BCHUSDT...`
- **Minggu 25:** `DOTUSDT, TIAUSDT, BCHUSDT, HBARUSDT, XLMUSDT...`
- **Minggu 26:** `MOODENGUSDT, WIFUSDT, PNUTUSDT, DOTUSDT, TIAUSDT...`
- **Minggu 27:** `MOODENGUSDT, PNUTUSDT, MYXUSDT, DOTUSDT, XLMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $52.13 | 38 | 47.37% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-6.52 | 12 | 41.67% |
| `RSIDivergenceHunter` | 0.2 | $80.21 | 107 | 57.94% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $200.82                     |
| **Net Profit**    | **$125.82 (+167.76%)** |
| Total Trades      | 157                         |
| Win Rate          | 54.14%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 157 trades (54.14%)             |
| Profit Factor     | 1.65                       |
| Max Drawdown      | 34.16%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 15:49:28

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `NEARUSDT, AAVEUSDT, UNIUSDT, DOTUSDT, 1000SHIBUSDT...`
- **Minggu 24:** `NEARUSDT, AAVEUSDT, IPUSDT, DOTUSDT, 1000BONKUSDT...`
- **Minggu 25:** `NEARUSDT, AAVEUSDT, IPUSDT, 1000SHIBUSDT, UNIUSDT...`
- **Minggu 26:** `PAXGUSDT, NEARUSDT, IPUSDT, 1000SHIBUSDT, UNIUSDT...`
- **Minggu 27:** `NEARUSDT, PAXGUSDT, IPUSDT, DOTUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-26.06 | 36 | 44.44% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `RSIDivergenceHunter` | 0.2 | $40.62 | 104 | 57.69% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $89.56                     |
| **Net Profit**    | **$14.56 (+19.42%)** |
| Total Trades      | 140                         |
| Win Rate          | 54.29%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 140 trades (54.29%)             |
| Profit Factor     | 1.07                       |
| Max Drawdown      | 47.48%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 15:40:39

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-17 (~6 Bulan 19 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `UNIUSDT, TIAUSDT, 1000SHIBUSDT, NEARUSDT, DOTUSDT...`
- **Minggu 24:** `TIAUSDT, IPUSDT, NEARUSDT, DOTUSDT, XLMUSDT...`
- **Minggu 25:** `UNIUSDT, TIAUSDT, IPUSDT, 1000SHIBUSDT, NEARUSDT...`
- **Minggu 26:** `UNIUSDT, TIAUSDT, IPUSDT, 1000SHIBUSDT, NEARUSDT...`
- **Minggu 27:** `UNIUSDT, IPUSDT, 1000SHIBUSDT, NEARUSDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $63.26 | 40 | 47.50% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-10.57 | 7 | 28.57% |
| `RSIDivergenceHunter` | 0.2 | $132.36 | 106 | 63.21% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $260.05                     |
| **Net Profit**    | **$185.05 (+246.74%)** |
| Total Trades      | 153                         |
| Win Rate          | 57.52%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 153 trades (57.52%)             |
| Profit Factor     | 1.92                       |
| Max Drawdown      | 31.80%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2026-01-05 15:34:02

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2026-01-02 (~7 Bulan 5 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `ARBUSDT, LTCUSDT, XLMUSDT, 1000PEPEUSDT, PENGUUSDT...`
- **Minggu 24:** `ARBUSDT, IPUSDT, XLMUSDT, MOODENGUSDT, 1000PEPEUSDT...`
- **Minggu 25:** `ARBUSDT, IPUSDT, LTCUSDT, XLMUSDT, VIRTUALUSDT...`
- **Minggu 26:** `ARBUSDT, IPUSDT, MOODENGUSDT, VIRTUALUSDT, PENGUUSDT...`
- **Minggu 27:** `ARBUSDT, IPUSDT, LTCUSDT, XLMUSDT, MOODENGUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $20.95 | 25 | 44.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-0.82 | 9 | 44.44% |
| `RSIDivergenceHunter` | 0.2 | $14.90 | 134 | 53.73% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $110.03                     |
| **Net Profit**    | **$35.03 (+46.71%)** |
| Total Trades      | 168                         |
| Win Rate          | 51.79%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 168 trades (51.79%)             |
| Profit Factor     | 1.16                       |
| Max Drawdown      | 38.30%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 19 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-18 06:04:29

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-04-07 s/d 2025-10-02 (~5 Bulan 29 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `use_regime_filter=True`, `regime_btc_rsi_threshold=52`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 15:** `SUIUSDT, FETUSDT, PENGUUSDT, SEIUSDT, 1000SHIBUSDT...`
- **Minggu 16:** `ENAUSDT, UNIUSDT, SUIUSDT, NEARUSDT, FETUSDT...`
- **Minggu 17:** `NEARUSDT, PENGUUSDT, SEIUSDT, 1000SHIBUSDT, VIRTUALUSDT...`
- **Minggu 18:** `UNIUSDT, NEARUSDT, SUIUSDT, FETUSDT, SEIUSDT...`
- **Minggu 19:** `UNIUSDT, SUIUSDT, PENGUUSDT, 1000SHIBUSDT, VIRTUALUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-3.15 | 12 | 33.33% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-1.73 | 9 | 22.22% |
| `RSIDivergenceHunter` | 0.2 | $-58.36 | 264 | 31.82% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $11.77                     |
| **Net Profit**    | **$-63.23 (-84.31%)** |
| Total Trades      | 285                         |
| Win Rate          | 31.58%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 285 trades (31.58%)             |
| Profit Factor     | 0.60                       |
| Max Drawdown      | 85.54%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 6 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-18 05:55:25

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-02 s/d 2025-12-15 (~6 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `TRXUSDT, WIFUSDT, FILUSDT, TIAUSDT, ETCUSDT...`
- **Minggu 24:** `TRXUSDT, WIFUSDT, TIAUSDT, ETCUSDT, NEARUSDT...`
- **Minggu 25:** `TRXUSDT, TIAUSDT, NEARUSDT, TAOUSDT, ARBUSDT...`
- **Minggu 26:** `TRXUSDT, SEIUSDT, WIFUSDT, FILUSDT, TIAUSDT...`
- **Minggu 27:** `TRXUSDT, SEIUSDT, HUSDT, NEARUSDT, INJUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $13.02 | 24 | 54.17% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $4.11 | 12 | 50.00% |
| `RSIDivergenceHunter` | 0.2 | $-1.95 | 86 | 45.35% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $90.18                     |
| **Net Profit**    | **$15.18 (+20.24%)** |
| Total Trades      | 122                         |
| Win Rate          | 47.54%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 122 trades (47.54%)             |
| Profit Factor     | 1.12                       |
| Max Drawdown      | 39.42%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-18 00:27:09

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-04-07 s/d 2025-10-02 (~5 Bulan 29 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 15:** `SUIUSDT, LTCUSDT, ARBUSDT, SEIUSDT, ETCUSDT...`
- **Minggu 16:** `SUIUSDT, FILUSDT, WLDUSDT, LTCUSDT, VIRTUALUSDT...`
- **Minggu 17:** `FILUSDT, WLDUSDT, LTCUSDT, VIRTUALUSDT, ARBUSDT...`
- **Minggu 18:** `SUIUSDT, FILUSDT, WLDUSDT, LTCUSDT, VIRTUALUSDT...`
- **Minggu 19:** `SUIUSDT, FILUSDT, LTCUSDT, VIRTUALUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $1.61 | 13 | 38.46% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-0.46 | 8 | 37.50% |
| `RSIDivergenceHunter` | 0.2 | $-62.53 | 205 | 30.24% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $13.62                     |
| **Net Profit**    | **$-61.38 (-81.84%)** |
| Total Trades      | 226                         |
| Win Rate          | 30.97%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 226 trades (30.97%)             |
| Profit Factor     | 0.53                       |
| Max Drawdown      | 82.85%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 12 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:42:06

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-03 s/d 2025-12-16 (~6 Bulan 17 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=30`, `bb_period=20`, `bb_std_dev=2.2`, `use_macro_trend_filter=False`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `FILUSDT, ENAUSDT, WLDUSDT, XLMUSDT, TAOUSDT...`
- **Minggu 24:** `SUIUSDT, ENAUSDT, WLDUSDT, XLMUSDT, VIRTUALUSDT...`
- **Minggu 25:** `ENAUSDT, JELLYJELLYUSDT, WLDUSDT, XLMUSDT, VIRTUALUSDT...`
- **Minggu 26:** `PAXGUSDT, ENAUSDT, FILUSDT, JELLYJELLYUSDT, VIRTUALUSDT...`
- **Minggu 27:** `PAXGUSDT, ENAUSDT, JELLYJELLYUSDT, WLDUSDT, XLMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $42.25 | 32 | 59.38% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $9.82 | 13 | 76.92% |
| `RSIDivergenceHunter` | 0.2 | $5.90 | 13 | 61.54% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $132.97                     |
| **Net Profit**    | **$57.97 (+77.29%)** |
| Total Trades      | 58                         |
| Win Rate          | 63.79%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 58 trades (63.79%)             |
| Profit Factor     | 1.81                       |
| Max Drawdown      | 26.49%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:35:35

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-09 s/d 2025-12-16 (~6 Bulan 11 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.0`, `use_macro_trend_filter=True`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `NEARUSDT, DOTUSDT, TAOUSDT, AAVEUSDT, OMUSDT...`
- **Minggu 24:** `NEARUSDT, DOTUSDT, TAOUSDT, AAVEUSDT, OMUSDT...`
- **Minggu 25:** `NEARUSDT, DOTUSDT, TAOUSDT, AAVEUSDT, OMUSDT...`
- **Minggu 26:** `NEARUSDT, PAXGUSDT, DOTUSDT, TAOUSDT, OMUSDT...`
- **Minggu 27:** `NEARUSDT, PAXGUSDT, DOTUSDT, TAOUSDT, HUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $47.51 | 31 | 64.52% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $5.50 | 11 | 63.64% |
| `RSIDivergenceHunter` | 0.2 | $7.87 | 14 | 57.14% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $135.88                     |
| **Net Profit**    | **$60.88 (+81.18%)** |
| Total Trades      | 56                         |
| Win Rate          | 62.50%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 56 trades (62.50%)             |
| Profit Factor     | 1.91                       |
| Max Drawdown      | 24.95%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:32:27

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-06 s/d 2025-12-16 (~4 Bulan 13 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.0`, `use_macro_trend_filter=True`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `HUSDT, NEARUSDT, XLMUSDT, FILUSDT, TRUMPUSDT...`
- **Minggu 33:** `AAVEUSDT, HUSDT, 1000PEPEUSDT, NEARUSDT, LTCUSDT...`
- **Minggu 34:** `AAVEUSDT, HUSDT, 1000PEPEUSDT, NEARUSDT, XLMUSDT...`
- **Minggu 35:** `HUSDT, LTCUSDT, PUMPUSDT, XLMUSDT, TRUMPUSDT...`
- **Minggu 36:** `HUSDT, 1000PEPEUSDT, NEARUSDT, LTCUSDT, XLMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $56.98 | 22 | 68.18% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $0.12 | 9 | 55.56% |
| `RSIDivergenceHunter` | 0.2 | $9.11 | 6 | 83.33% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $141.20                     |
| **Net Profit**    | **$66.20 (+88.27%)** |
| Total Trades      | 37                         |
| Win Rate          | 67.57%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 37 trades (67.57%)             |
| Profit Factor     | 3.21                       |
| Max Drawdown      | 16.71%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:27:41

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-06 s/d 2025-12-13 (~4 Bulan 10 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.0`, `use_macro_trend_filter=True`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `HUSDT, ETCUSDT, UNIUSDT, 1000SHIBUSDT, 1000BONKUSDT...`
- **Minggu 33:** `HUSDT, ETCUSDT, UNIUSDT, PAXGUSDT, 1000SHIBUSDT...`
- **Minggu 34:** `HUSDT, ETCUSDT, UNIUSDT, PAXGUSDT, 1000SHIBUSDT...`
- **Minggu 35:** `HUSDT, UNIUSDT, PAXGUSDT, 1000SHIBUSDT, 1000BONKUSDT...`
- **Minggu 36:** `HUSDT, ETCUSDT, UNIUSDT, 1000SHIBUSDT, 1000BONKUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $38.84 | 21 | 66.67% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-0.64 | 12 | 50.00% |
| `RSIDivergenceHunter` | 0.2 | $7.31 | 23 | 56.52% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $120.50                     |
| **Net Profit**    | **$45.50 (+60.67%)** |
| Total Trades      | 56                         |
| Win Rate          | 58.93%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 56 trades (58.93%)             |
| Profit Factor     | 1.84                       |
| Max Drawdown      | 30.63%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:21:55

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-04 s/d 2025-12-13 (~6 Bulan 13 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.0`, `use_macro_trend_filter=True`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`
- **`RSIDivergenceHunter`:** `risk_per_trade=0.015`, `adx_threshold=20`, `use_macd_div_confirm=True`, `allow_long=False`, `allow_short=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `PENGUUSDT, ARBUSDT, NEARUSDT, 1000LUNCUSDT, TAOUSDT...`
- **Minggu 24:** `PENGUUSDT, ARBUSDT, NEARUSDT, 1000LUNCUSDT, TAOUSDT...`
- **Minggu 25:** `ARBUSDT, NEARUSDT, 1000LUNCUSDT, TAOUSDT, ENAUSDT...`
- **Minggu 26:** `PENGUUSDT, ARBUSDT, NEARUSDT, 1000LUNCUSDT, TAOUSDT...`
- **Minggu 27:** `PENGUUSDT, ARBUSDT, NEARUSDT, 1000LUNCUSDT, TAOUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $45.83 | 30 | 66.67% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-7.86 | 15 | 40.00% |
| `RSIDivergenceHunter` | 0.2 | $-6.54 | 33 | 57.58% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $106.43                     |
| **Net Profit**    | **$31.43 (+41.91%)** |
| Total Trades      | 78                         |
| Win Rate          | 57.69%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 78 trades (57.69%)             |
| Profit Factor     | 1.22                       |
| Max Drawdown      | 51.20%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:17:52

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-13 s/d 2025-12-17 (~6 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.0`, `use_macro_trend_filter=True`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `BCHUSDT, WLDUSDT, SUIUSDT, DOTUSDT, ENAUSDT...`
- **Minggu 24:** `VIRTUALUSDT, BCHUSDT, WLDUSDT, SUIUSDT, DOTUSDT...`
- **Minggu 25:** `VIRTUALUSDT, BCHUSDT, JELLYJELLYUSDT, WLDUSDT, DOTUSDT...`
- **Minggu 26:** `VIRTUALUSDT, BCHUSDT, JELLYJELLYUSDT, DOTUSDT, ENAUSDT...`
- **Minggu 27:** `VIRTUALUSDT, JELLYJELLYUSDT, WLDUSDT, DOTUSDT, OPUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $80.94 | 43 | 67.44% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-4.74 | 13 | 53.85% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $151.19                     |
| **Net Profit**    | **$76.19 (+101.59%)** |
| Total Trades      | 56                         |
| Win Rate          | 64.29%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 56 trades (64.29%)             |
| Profit Factor     | 2.10                       |
| Max Drawdown      | 21.03%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:06:38

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-14 (~4 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.01`, `rsi_oversold_threshold=35`, `bb_period=20`, `bb_std_dev=2.0`, `use_macro_trend_filter=True`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `UNIUSDT, AAVEUSDT, OPUSDT, 1000SHIBUSDT, HUSDT...`
- **Minggu 33:** `UNIUSDT, AAVEUSDT, OPUSDT, 1000SHIBUSDT, HUSDT...`
- **Minggu 34:** `UNIUSDT, AAVEUSDT, OPUSDT, 1000SHIBUSDT, HUSDT...`
- **Minggu 35:** `UNIUSDT, 1000SHIBUSDT, BCHUSDT, HUSDT, PUMPUSDT...`
- **Minggu 36:** `UNIUSDT, OPUSDT, 1000SHIBUSDT, BCHUSDT, HUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $72.69 | 35 | 60.00% |
| `LongOnlyCorrectionHunter` | 0.1 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.1 | $-15.63 | 4 | 50.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $132.07                     |
| **Net Profit**    | **$57.07 (+76.09%)** |
| Total Trades      | 39                         |
| Win Rate          | 58.97%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 39 trades (58.97%)             |
| Profit Factor     | 2.08                       |
| Max Drawdown      | 15.61%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 23:00:11

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-14 (~4 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, OPUSDT, APTUSDT, HUSDT, ETCUSDT...`
- **Minggu 33:** `SUIUSDT, BCHUSDT, OPUSDT, APTUSDT, LTCUSDT...`
- **Minggu 34:** `SUIUSDT, BCHUSDT, OPUSDT, HUSDT, APTUSDT...`
- **Minggu 35:** `1000LUNCUSDT, BCHUSDT, APTUSDT, LTCUSDT, HUSDT...`
- **Minggu 36:** `BCHUSDT, OPUSDT, LTCUSDT, HUSDT, APTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.9 | $65.21 | 33 | 60.61% |
| `MomentumCrossHunter` | 0.1 | $-9.00 | 10 | 40.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $131.21                     |
| **Net Profit**    | **$56.21 (+74.94%)** |
| Total Trades      | 43                         |
| Win Rate          | 55.81%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 43 trades (55.81%)             |
| Profit Factor     | 2.22                       |
| Max Drawdown      | 23.65%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:57:28

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-14 (~4 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.028`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `HUSDT, VIRTUALUSDT, JELLYJELLYUSDT, OMUSDT, 1000BONKUSDT...`
- **Minggu 33:** `HUSDT, VIRTUALUSDT, OMUSDT, DOTUSDT, 1000BONKUSDT...`
- **Minggu 34:** `HUSDT, VIRTUALUSDT, JELLYJELLYUSDT, 1000BONKUSDT, PAXGUSDT...`
- **Minggu 35:** `HUSDT, VIRTUALUSDT, XPLUSDT, JELLYJELLYUSDT, OMUSDT...`
- **Minggu 36:** `HUSDT, VIRTUALUSDT, XPLUSDT, JELLYJELLYUSDT, OMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.9 | $78.40 | 34 | 61.76% |
| `MomentumCrossHunter` | 0.1 | $-15.02 | 9 | 44.44% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $138.37                     |
| **Net Profit**    | **$63.37 (+84.50%)** |
| Total Trades      | 43                         |
| Win Rate          | 58.14%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 43 trades (58.14%)             |
| Profit Factor     | 2.04                       |
| Max Drawdown      | 17.95%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:49:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-14 (~4 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, 1000PEPEUSDT, UNIUSDT, FILUSDT, ETCUSDT...`
- **Minggu 33:** `OMUSDT, 1000PEPEUSDT, BCHUSDT, UNIUSDT, PENGUUSDT...`
- **Minggu 34:** `1000PEPEUSDT, UNIUSDT, BCHUSDT, FILUSDT, ETCUSDT...`
- **Minggu 35:** `XPLUSDT, OMUSDT, BCHUSDT, UNIUSDT, PENGUUSDT...`
- **Minggu 36:** `XPLUSDT, OMUSDT, 1000PEPEUSDT, BCHUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $55.86 | 32 | 59.38% |
| `MomentumCrossHunter` | 0.2 | $-1.71 | 9 | 44.44% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $129.15                     |
| **Net Profit**    | **$54.15 (+72.20%)** |
| Total Trades      | 41                         |
| Win Rate          | 56.10%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 41 trades (56.10%)             |
| Profit Factor     | 2.35                       |
| Max Drawdown      | 18.36%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:47:10

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-11 (~4 Bulan 3 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, WIFUSDT, UNIUSDT, 1000PEPEUSDT, WLDUSDT...`
- **Minggu 33:** `SUIUSDT, WIFUSDT, UNIUSDT, 1000PEPEUSDT, WLDUSDT...`
- **Minggu 34:** `SUIUSDT, UNIUSDT, 1000PEPEUSDT, WLDUSDT, ARBUSDT...`
- **Minggu 35:** `WIFUSDT, UNIUSDT, WLDUSDT, OMUSDT, ARBUSDT...`
- **Minggu 36:** `WIFUSDT, UNIUSDT, 1000PEPEUSDT, WLDUSDT, OMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $51.78 | 30 | 63.33% |
| `MomentumCrossHunter` | 0.2 | $-13.47 | 20 | 45.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $113.30                     |
| **Net Profit**    | **$38.30 (+51.07%)** |
| Total Trades      | 50                         |
| Win Rate          | 56.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 50 trades (56.00%)             |
| Profit Factor     | 1.66                       |
| Max Drawdown      | 19.83%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:45:31

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-11 (~4 Bulan 3 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, PENGUUSDT, 1000PEPEUSDT, FILUSDT, WIFUSDT...`
- **Minggu 33:** `OMUSDT, PENGUUSDT, 1000PEPEUSDT, BCHUSDT, DOTUSDT...`
- **Minggu 34:** `1000PEPEUSDT, BCHUSDT, PUMPUSDT, LTCUSDT, FILUSDT...`
- **Minggu 35:** `OMUSDT, PENGUUSDT, BCHUSDT, DOTUSDT, PUMPUSDT...`
- **Minggu 36:** `OMUSDT, 1000PEPEUSDT, PENGUUSDT, BCHUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $38.76 | 30 | 63.33% |
| `MomentumCrossHunter` | 0.2 | $-30.58 | 22 | 27.27% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $83.18                     |
| **Net Profit**    | **$8.18 (+10.90%)** |
| Total Trades      | 52                         |
| Win Rate          | 48.08%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 52 trades (48.08%)             |
| Profit Factor     | 1.13                       |
| Max Drawdown      | 28.29%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:35:17

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-11 (~4 Bulan 3 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WLDUSDT, 1000SHIBUSDT, AAVEUSDT, FILUSDT, LUNA2USDT...`
- **Minggu 33:** `1000SHIBUSDT, AAVEUSDT, WLDUSDT, FILUSDT, NEARUSDT...`
- **Minggu 34:** `WLDUSDT, AAVEUSDT, 1000SHIBUSDT, FILUSDT, NEARUSDT...`
- **Minggu 35:** `1000SHIBUSDT, WLDUSDT, LUNA2USDT, ENAUSDT, JELLYJELLYUSDT...`
- **Minggu 36:** `1000SHIBUSDT, WLDUSDT, FILUSDT, LUNA2USDT, NEARUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $50.89 | 36 | 61.11% |
| `MomentumCrossHunter` | 0.2 | $-22.88 | 37 | 27.03% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $103.01                     |
| **Net Profit**    | **$28.01 (+37.34%)** |
| Total Trades      | 73                         |
| Win Rate          | 43.84%                     |
|  - Long Win Rate  | 19 trades (26.32%)              |
|  - Short Win Rate | 54 trades (50.00%)             |
| Profit Factor     | 1.37                       |
| Max Drawdown      | 26.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   use_htf_filter: False


---

## Backtest: 2025-12-17 22:31:35

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-15 (~4 Bulan 7 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=20`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, DOTUSDT, WLDUSDT, 1000PEPEUSDT, 1000BONKUSDT...`
- **Minggu 33:** `OMUSDT, DOTUSDT, WLDUSDT, 1000PEPEUSDT, 1000BONKUSDT...`
- **Minggu 34:** `WLDUSDT, 1000PEPEUSDT, 1000BONKUSDT, ARBUSDT, ENAUSDT...`
- **Minggu 35:** `OMUSDT, DOTUSDT, WLDUSDT, 1000BONKUSDT, XPLUSDT...`
- **Minggu 36:** `OMUSDT, WLDUSDT, 1000PEPEUSDT, 1000BONKUSDT, XPLUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $84.48 | 41 | 73.17% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $159.48                     |
| **Net Profit**    | **$84.48 (+112.64%)** |
| Total Trades      | 41                         |
| Win Rate          | 73.17%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 41 trades (73.17%)             |
| Profit Factor     | 2.44                       |
| Max Drawdown      | 20.13%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   use_htf_filter: True


---

## Backtest: 2025-12-17 22:29:13

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-11 (~4 Bulan 3 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ENAUSDT, 1000BONKUSDT, UNIUSDT, ARBUSDT, 1000PEPEUSDT...`
- **Minggu 33:** `LTCUSDT, ENAUSDT, 1000BONKUSDT, UNIUSDT, ARBUSDT...`
- **Minggu 34:** `LTCUSDT, TAOUSDT, ENAUSDT, 1000BONKUSDT, UNIUSDT...`
- **Minggu 35:** `LTCUSDT, 1000LUNCUSDT, TAOUSDT, ENAUSDT, 1000BONKUSDT...`
- **Minggu 36:** `LTCUSDT, 1000LUNCUSDT, ENAUSDT, 1000BONKUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.8 | $65.22 | 36 | 63.89% |
| `MomentumCrossHunter` | 0.2 | $-2.71 | 18 | 50.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $137.51                     |
| **Net Profit**    | **$62.51 (+83.35%)** |
| Total Trades      | 54                         |
| Win Rate          | 59.26%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 54 trades (59.26%)             |
| Profit Factor     | 2.05                       |
| Max Drawdown      | 21.39%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:22:46

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-14 (~4 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PENGUUSDT, FILUSDT, AAVEUSDT, HUSDT, ARBUSDT...`
- **Minggu 33:** `PENGUUSDT, FILUSDT, AAVEUSDT, HUSDT, PAXGUSDT...`
- **Minggu 34:** `PENGUUSDT, FILUSDT, AAVEUSDT, HUSDT, PAXGUSDT...`
- **Minggu 35:** `PENGUUSDT, HUSDT, PAXGUSDT, ARBUSDT, BCHUSDT...`
- **Minggu 36:** `PENGUUSDT, FILUSDT, HUSDT, ARBUSDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $64.54 | 37 | 59.46% |
| `MomentumCrossHunter` | 0.4 | $-3.39 | 6 | 33.33% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $136.14                     |
| **Net Profit**    | **$61.14 (+81.53%)** |
| Total Trades      | 43                         |
| Win Rate          | 55.81%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 43 trades (55.81%)             |
| Profit Factor     | 2.49                       |
| Max Drawdown      | 18.36%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:12:54

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-16 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, BCHUSDT, FILUSDT, OMUSDT, AAVEUSDT...`
- **Minggu 33:** `ETCUSDT, BCHUSDT, FILUSDT, OMUSDT, AAVEUSDT...`
- **Minggu 34:** `ETCUSDT, BCHUSDT, FILUSDT, AAVEUSDT, WLDUSDT...`
- **Minggu 35:** `1000LUNCUSDT, BCHUSDT, OMUSDT, XPLUSDT, DOTUSDT...`
- **Minggu 36:** `1000LUNCUSDT, ETCUSDT, BCHUSDT, FILUSDT, OMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $14.80 | 30 | 46.67% |
| `MomentumCrossHunter` | 0.4 | $-27.92 | 142 | 46.48% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $61.88                     |
| **Net Profit**    | **$-13.12 (-17.49%)** |
| Total Trades      | 172                         |
| Win Rate          | 46.51%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 172 trades (46.51%)             |
| Profit Factor     | 0.92                       |
| Max Drawdown      | 25.87%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:11:38

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-16 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `BCHUSDT, DOTUSDT, OMUSDT, SUIUSDT, UNIUSDT...`
- **Minggu 33:** `BCHUSDT, DOTUSDT, LTCUSDT, OMUSDT, SUIUSDT...`
- **Minggu 34:** `BCHUSDT, TAOUSDT, LTCUSDT, SUIUSDT, UNIUSDT...`
- **Minggu 35:** `BCHUSDT, TAOUSDT, DOTUSDT, LTCUSDT, OMUSDT...`
- **Minggu 36:** `BCHUSDT, LTCUSDT, OMUSDT, XPLUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $3.41 | 24 | 41.67% |
| `MomentumCrossHunter` | 0.4 | $-30.36 | 111 | 42.34% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $48.04                     |
| **Net Profit**    | **$-26.96 (-35.94%)** |
| Total Trades      | 135                         |
| Win Rate          | 42.22%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 135 trades (42.22%)             |
| Profit Factor     | 0.73                       |
| Max Drawdown      | 41.84%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 12 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:09:05

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-16 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, FILUSDT, PUMPUSDT, AAVEUSDT, PENGUUSDT...`
- **Minggu 33:** `ARBUSDT, FILUSDT, PAXGUSDT, AAVEUSDT, LTCUSDT...`
- **Minggu 34:** `ARBUSDT, FILUSDT, PAXGUSDT, PUMPUSDT, AAVEUSDT...`
- **Minggu 35:** `ARBUSDT, PAXGUSDT, PUMPUSDT, LTCUSDT, PENGUUSDT...`
- **Minggu 36:** `ARBUSDT, FILUSDT, LTCUSDT, PENGUUSDT, HUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $15.24 | 25 | 48.00% |
| `MomentumCrossHunter` | 0.4 | $-20.90 | 136 | 46.32% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $69.34                     |
| **Net Profit**    | **$-5.66 (-7.54%)** |
| Total Trades      | 161                         |
| Win Rate          | 46.58%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 161 trades (46.58%)             |
| Profit Factor     | 0.95                       |
| Max Drawdown      | 36.93%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:07:46

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-16 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PUMPUSDT, JELLYJELLYUSDT, WIFUSDT, ARBUSDT, ENAUSDT...`
- **Minggu 33:** `WIFUSDT, ARBUSDT, LTCUSDT, ENAUSDT, SUIUSDT...`
- **Minggu 34:** `PUMPUSDT, JELLYJELLYUSDT, ARBUSDT, LTCUSDT, ENAUSDT...`
- **Minggu 35:** `PUMPUSDT, JELLYJELLYUSDT, WIFUSDT, ARBUSDT, LTCUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, WIFUSDT, ARBUSDT, LTCUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $13.24 | 24 | 45.83% |
| `MomentumCrossHunter` | 0.4 | $-25.64 | 139 | 46.76% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $62.59                     |
| **Net Profit**    | **$-12.41 (-16.54%)** |
| Total Trades      | 163                         |
| Win Rate          | 46.63%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 163 trades (46.63%)             |
| Profit Factor     | 0.90                       |
| Max Drawdown      | 45.48%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:06:30

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-16 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, ETCUSDT, DOTUSDT, OMUSDT, HUSDT...`
- **Minggu 33:** `ETCUSDT, DOTUSDT, 1000LUNCUSDT, OMUSDT, HUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, ETCUSDT, OMUSDT, HUSDT, 1000PEPEUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, DOTUSDT, 1000LUNCUSDT, OMUSDT, HUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, ETCUSDT, 1000LUNCUSDT, OMUSDT, HUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $17.09 | 18 | 61.11% |
| `MomentumCrossHunter` | 0.4 | $-24.31 | 119 | 45.38% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $67.77                     |
| **Net Profit**    | **$-7.23 (-9.63%)** |
| Total Trades      | 137                         |
| Win Rate          | 47.45%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 137 trades (47.45%)             |
| Profit Factor     | 0.93                       |
| Max Drawdown      | 42.70%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 33 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:03:13

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-17 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, HUSDT, PENGUUSDT, DOTUSDT, 1000PEPEUSDT...`
- **Minggu 33:** `WIFUSDT, HUSDT, DOTUSDT, PENGUUSDT, 1000PEPEUSDT...`
- **Minggu 34:** `HUSDT, PENGUUSDT, DOTUSDT, 1000PEPEUSDT, UNIUSDT...`
- **Minggu 35:** `WIFUSDT, PENGUUSDT, HUSDT, DOTUSDT, UNIUSDT...`
- **Minggu 36:** `WIFUSDT, HUSDT, PENGUUSDT, 1000PEPEUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $33.65 | 34 | 58.82% |
| `MomentumCrossHunter` | 0.4 | $-18.36 | 143 | 46.85% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $90.29                     |
| **Net Profit**    | **$15.29 (+20.38%)** |
| Total Trades      | 177                         |
| Win Rate          | 49.15%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 177 trades (49.15%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 38.60%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 22:01:54

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-17 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, LUNA2USDT, ENAUSDT, SUIUSDT, WLDUSDT...`
- **Minggu 33:** `WIFUSDT, LTCUSDT, ENAUSDT, SUIUSDT, WLDUSDT...`
- **Minggu 34:** `LTCUSDT, ENAUSDT, SUIUSDT, WLDUSDT, PENGUUSDT...`
- **Minggu 35:** `WIFUSDT, LUNA2USDT, LTCUSDT, ENAUSDT, SUIUSDT...`
- **Minggu 36:** `WIFUSDT, LUNA2USDT, LTCUSDT, ENAUSDT, SUIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $14.08 | 18 | 50.00% |
| `MomentumCrossHunter` | 0.4 | $-18.81 | 73 | 46.58% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $70.27                     |
| **Net Profit**    | **$-4.73 (-6.30%)** |
| Total Trades      | 91                         |
| Win Rate          | 47.25%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 91 trades (47.25%)             |
| Profit Factor     | 0.94                       |
| Max Drawdown      | 26.92%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 22 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 21:48:53

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-17 (~4 Bulan 9 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, LUNA2USDT, SUIUSDT, JELLYJELLYUSDT, HUSDT...`
- **Minggu 33:** `OMUSDT, SUIUSDT, JELLYJELLYUSDT, HUSDT, ARBUSDT...`
- **Minggu 34:** `OMUSDT, SUIUSDT, JELLYJELLYUSDT, HUSDT, ARBUSDT...`
- **Minggu 35:** `OMUSDT, LUNA2USDT, SUIUSDT, JELLYJELLYUSDT, HUSDT...`
- **Minggu 36:** `OMUSDT, LUNA2USDT, SUIUSDT, JELLYJELLYUSDT, HUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $18.84 | 32 | 53.12% |
| `MomentumCrossHunter` | 0.4 | $-21.60 | 23 | 43.48% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $72.24                     |
| **Net Profit**    | **$-2.76 (-3.68%)** |
| Total Trades      | 55                         |
| Win Rate          | 49.09%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 55 trades (49.09%)             |
| Profit Factor     | 0.96                       |
| Max Drawdown      | 23.71%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 8 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 21:44:19

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-13 s/d 2025-12-16 (~6 Bulan 7 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `WLDUSDT, ENAUSDT, EPICUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 24:** `WLDUSDT, ENAUSDT, EPICUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 25:** `WLDUSDT, ENAUSDT, EPICUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 26:** `WLDUSDT, ENAUSDT, EPICUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 27:** `WLDUSDT, ENAUSDT, EPICUSDT, ARBUSDT, PAXGUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-9.74 | 34 | 38.24% |
| `MomentumCrossHunter` | 0.4 | $-17.82 | 23 | 39.13% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $47.44                     |
| **Net Profit**    | **$-27.56 (-36.75%)** |
| Total Trades      | 57                         |
| Win Rate          | 38.60%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 57 trades (38.60%)             |
| Profit Factor     | 0.56                       |
| Max Drawdown      | 41.51%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 21:38:07

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-13 s/d 2025-12-15 (~6 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `TAOUSDT, NEARUSDT, SUIUSDT, WIFUSDT, 1000PEPEUSDT...`
- **Minggu 24:** `TAOUSDT, NEARUSDT, SUIUSDT, WIFUSDT, 1000PEPEUSDT...`
- **Minggu 25:** `TAOUSDT, NEARUSDT, SUIUSDT, WIFUSDT, 1000PEPEUSDT...`
- **Minggu 26:** `TAOUSDT, NEARUSDT, SUIUSDT, WIFUSDT, 1000PEPEUSDT...`
- **Minggu 27:** `TAOUSDT, NEARUSDT, HUSDT, SUIUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $75.88 | 50 | 70.00% |
| `MomentumCrossHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $150.88                     |
| **Net Profit**    | **$75.88 (+101.18%)** |
| Total Trades      | 50                         |
| Win Rate          | 70.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 50 trades (70.00%)             |
| Profit Factor     | 2.00                       |
| Max Drawdown      | 20.23%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 21:12:59

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-06-13 s/d 2025-12-15 (~6 Bulan 6 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 23:** `ENAUSDT, UNIUSDT, 1000PEPEUSDT, LUNA2USDT, DOTUSDT...`
- **Minggu 24:** `ENAUSDT, UNIUSDT, 1000PEPEUSDT, LUNA2USDT, DOTUSDT...`
- **Minggu 25:** `ENAUSDT, UNIUSDT, 1000PEPEUSDT, LUNA2USDT, DOTUSDT...`
- **Minggu 26:** `ENAUSDT, UNIUSDT, 1000PEPEUSDT, LUNA2USDT, DOTUSDT...`
- **Minggu 27:** `ENAUSDT, UNIUSDT, 1000PEPEUSDT, LUNA2USDT, DOTUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $76.85 | 42 | 71.43% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $151.85                     |
| **Net Profit**    | **$76.85 (+102.47%)** |
| Total Trades      | 42                         |
| Win Rate          | 71.43%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 42 trades (71.43%)             |
| Profit Factor     | 2.76                       |
| Max Drawdown      | 19.94%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 20:18:49

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-15 (~4 Bulan 0 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, AAVEUSDT, PUMPUSDT, NEARUSDT, ETCUSDT...`
- **Minggu 33:** `WIFUSDT, AAVEUSDT, PUMPUSDT, NEARUSDT, ETCUSDT...`
- **Minggu 34:** `WIFUSDT, AAVEUSDT, PUMPUSDT, NEARUSDT, ETCUSDT...`
- **Minggu 35:** `WIFUSDT, PUMPUSDT, AAVEUSDT, NEARUSDT, LTCUSDT...`
- **Minggu 36:** `WIFUSDT, AAVEUSDT, NEARUSDT, ETCUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $89.62 | 37 | 72.97% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $164.62                     |
| **Net Profit**    | **$89.62 (+119.50%)** |
| Total Trades      | 37                         |
| Win Rate          | 72.97%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 37 trades (72.97%)             |
| Profit Factor     | 3.73                       |
| Max Drawdown      | 8.46%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 20:16:10

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-15 (~4 Bulan 0 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=17`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000PEPEUSDT, WLDUSDT, LUNA2USDT, AAVEUSDT, PENGUUSDT...`
- **Minggu 33:** `1000PEPEUSDT, WLDUSDT, AAVEUSDT, PENGUUSDT, JELLYJELLYUSDT...`
- **Minggu 34:** `1000PEPEUSDT, WLDUSDT, AAVEUSDT, PENGUUSDT, JELLYJELLYUSDT...`
- **Minggu 35:** `1000PEPEUSDT, WLDUSDT, LUNA2USDT, AAVEUSDT, PENGUUSDT...`
- **Minggu 36:** `1000PEPEUSDT, WLDUSDT, LUNA2USDT, AAVEUSDT, PENGUUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $89.62 | 37 | 72.97% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $164.62                     |
| **Net Profit**    | **$89.62 (+119.50%)** |
| Total Trades      | 37                         |
| Win Rate          | 72.97%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 37 trades (72.97%)             |
| Profit Factor     | 3.73                       |
| Max Drawdown      | 8.46%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 20:14:43

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-15 (~4 Bulan 0 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, LUNA2USDT, NEARUSDT, AAVEUSDT, FILUSDT...`
- **Minggu 33:** `ARBUSDT, NEARUSDT, AAVEUSDT, FILUSDT, BCHUSDT...`
- **Minggu 34:** `ARBUSDT, NEARUSDT, AAVEUSDT, FILUSDT, BCHUSDT...`
- **Minggu 35:** `ARBUSDT, LUNA2USDT, NEARUSDT, AAVEUSDT, BCHUSDT...`
- **Minggu 36:** `ARBUSDT, LUNA2USDT, NEARUSDT, AAVEUSDT, FILUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $89.62 | 37 | 72.97% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $164.62                     |
| **Net Profit**    | **$89.62 (+119.50%)** |
| Total Trades      | 37                         |
| Win Rate          | 72.97%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 37 trades (72.97%)             |
| Profit Factor     | 3.73                       |
| Max Drawdown      | 8.46%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 20:11:27

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `DOTUSDT, WIFUSDT, OMUSDT, JELLYJELLYUSDT, PUMPUSDT...`
- **Minggu 33:** `DOTUSDT, WIFUSDT, OMUSDT, JELLYJELLYUSDT, PUMPUSDT...`
- **Minggu 34:** `DOTUSDT, WIFUSDT, OMUSDT, JELLYJELLYUSDT, PUMPUSDT...`
- **Minggu 35:** `DOTUSDT, WIFUSDT, OMUSDT, JELLYJELLYUSDT, PUMPUSDT...`
- **Minggu 36:** `DOTUSDT, WIFUSDT, OMUSDT, BASUSDT, JELLYJELLYUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $78.09 | 28 | 78.57% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $153.09                     |
| **Net Profit**    | **$78.09 (+104.12%)** |
| Total Trades      | 28                         |
| Win Rate          | 78.57%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 28 trades (78.57%)             |
| Profit Factor     | 3.65                       |
| Max Drawdown      | 13.74%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:54:56

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, WLDUSDT, FILUSDT, LTCUSDT, ARBUSDT...`
- **Minggu 33:** `ETCUSDT, WLDUSDT, PAXGUSDT, FILUSDT, LTCUSDT...`
- **Minggu 34:** `ETCUSDT, WLDUSDT, PAXGUSDT, FILUSDT, LTCUSDT...`
- **Minggu 35:** `WLDUSDT, PAXGUSDT, FILUSDT, LTCUSDT, ARBUSDT...`
- **Minggu 36:** `ETCUSDT, WLDUSDT, FILUSDT, LTCUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $78.09 | 28 | 78.57% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $153.09                     |
| **Net Profit**    | **$78.09 (+104.12%)** |
| Total Trades      | 28                         |
| Win Rate          | 78.57%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 28 trades (78.57%)             |
| Profit Factor     | 3.65                       |
| Max Drawdown      | 13.74%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:53:00

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-14 s/d 2025-12-13 (~4 Bulan 2 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, WIFUSDT, 1000PEPEUSDT, SUIUSDT, AAVEUSDT...`
- **Minggu 33:** `JELLYJELLYUSDT, WIFUSDT, 1000PEPEUSDT, SUIUSDT, AAVEUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, WIFUSDT, 1000PEPEUSDT, SUIUSDT, AAVEUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, WIFUSDT, 1000PEPEUSDT, SUIUSDT, AAVEUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, WIFUSDT, 1000PEPEUSDT, SUIUSDT, AAVEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $45.57 | 25 | 60.00% |
| `MomentumCrossHunter` | 0.2 | $8.38 | 25 | 56.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $128.95                     |
| **Net Profit**    | **$53.95 (+71.93%)** |
| Total Trades      | 50                         |
| Win Rate          | 58.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 50 trades (58.00%)             |
| Profit Factor     | 2.39                       |
| Max Drawdown      | 22.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:50:27

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-14 s/d 2025-12-13 (~4 Bulan 2 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, DOTUSDT, FILUSDT, WLDUSDT, ENAUSDT...`
- **Minggu 33:** `ETCUSDT, DOTUSDT, FILUSDT, WLDUSDT, ENAUSDT...`
- **Minggu 34:** `ETCUSDT, DOTUSDT, FILUSDT, WLDUSDT, ENAUSDT...`
- **Minggu 35:** `DOTUSDT, FILUSDT, WLDUSDT, ENAUSDT, LTCUSDT...`
- **Minggu 36:** `ETCUSDT, DOTUSDT, FILUSDT, WLDUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $55.27 | 24 | 66.67% |
| `MomentumCrossHunter` | 0.2 | $14.79 | 23 | 56.52% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $145.06                     |
| **Net Profit**    | **$70.06 (+93.41%)** |
| Total Trades      | 47                         |
| Win Rate          | 61.70%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 47 trades (61.70%)             |
| Profit Factor     | 2.98                       |
| Max Drawdown      | 14.35%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:49:04

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-14 s/d 2025-12-13 (~4 Bulan 2 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, PUMPUSDT, TAOUSDT, AAVEUSDT, WIFUSDT...`
- **Minggu 33:** `OMUSDT, PUMPUSDT, TAOUSDT, AAVEUSDT, WIFUSDT...`
- **Minggu 34:** `OMUSDT, PUMPUSDT, TAOUSDT, AAVEUSDT, WIFUSDT...`
- **Minggu 35:** `OMUSDT, PUMPUSDT, TAOUSDT, AAVEUSDT, WIFUSDT...`
- **Minggu 36:** `OMUSDT, TAOUSDT, BASUSDT, AAVEUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $42.16 | 24 | 62.50% |
| `MomentumCrossHunter` | 0.2 | $12.68 | 28 | 64.29% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $129.84                     |
| **Net Profit**    | **$54.84 (+73.11%)** |
| Total Trades      | 52                         |
| Win Rate          | 63.46%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 52 trades (63.46%)             |
| Profit Factor     | 2.33                       |
| Max Drawdown      | 23.73%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:47:58

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-14 s/d 2025-12-13 (~4 Bulan 2 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `BCHUSDT, LTCUSDT, 1000PEPEUSDT, WLDUSDT, TAOUSDT...`
- **Minggu 33:** `BCHUSDT, LTCUSDT, 1000PEPEUSDT, WLDUSDT, PAXGUSDT...`
- **Minggu 34:** `BCHUSDT, LTCUSDT, 1000PEPEUSDT, WLDUSDT, PAXGUSDT...`
- **Minggu 35:** `BCHUSDT, LTCUSDT, 1000PEPEUSDT, WLDUSDT, PAXGUSDT...`
- **Minggu 36:** `BCHUSDT, LTCUSDT, 1000PEPEUSDT, WLDUSDT, TAOUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $45.10 | 23 | 60.87% |
| `MomentumCrossHunter` | 0.2 | $15.46 | 30 | 60.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $135.56                     |
| **Net Profit**    | **$60.56 (+80.74%)** |
| Total Trades      | 53                         |
| Win Rate          | 60.38%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 53 trades (60.38%)             |
| Profit Factor     | 2.47                       |
| Max Drawdown      | 18.88%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:45:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-14 s/d 2025-12-13 (~4 Bulan 2 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, PENGUUSDT, SUIUSDT, ETCUSDT, LUNA2USDT...`
- **Minggu 33:** `ARBUSDT, PENGUUSDT, SUIUSDT, PAXGUSDT, ETCUSDT...`
- **Minggu 34:** `ARBUSDT, PENGUUSDT, SUIUSDT, PAXGUSDT, ETCUSDT...`
- **Minggu 35:** `ARBUSDT, PENGUUSDT, SUIUSDT, PAXGUSDT, LUNA2USDT...`
- **Minggu 36:** `ARBUSDT, PENGUUSDT, SUIUSDT, ETCUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $42.36 | 23 | 60.87% |
| `MomentumCrossHunter` | 0.2 | $6.12 | 33 | 57.58% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $123.48                     |
| **Net Profit**    | **$48.48 (+64.64%)** |
| Total Trades      | 56                         |
| Win Rate          | 58.93%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 56 trades (58.93%)             |
| Profit Factor     | 2.16                       |
| Max Drawdown      | 23.25%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:40:16

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-17 s/d 2025-12-13 (~3 Bulan 29 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `UNIUSDT, DOTUSDT, 1000PEPEUSDT, ENAUSDT, PENGUUSDT...`
- **Minggu 33:** `UNIUSDT, DOTUSDT, 1000PEPEUSDT, ENAUSDT, PENGUUSDT...`
- **Minggu 34:** `UNIUSDT, DOTUSDT, 1000PEPEUSDT, ENAUSDT, WLDUSDT...`
- **Minggu 35:** `UNIUSDT, DOTUSDT, 1000PEPEUSDT, ENAUSDT, WLDUSDT...`
- **Minggu 36:** `UNIUSDT, DOTUSDT, 1000PEPEUSDT, ENAUSDT, BASUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $53.98 | 25 | 60.00% |
| `MomentumCrossHunter` | 0.2 | $15.01 | 31 | 61.29% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $143.99                     |
| **Net Profit**    | **$68.99 (+91.98%)** |
| Total Trades      | 56                         |
| Win Rate          | 60.71%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 56 trades (60.71%)             |
| Profit Factor     | 2.62                       |
| Max Drawdown      | 18.07%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:37:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-17 s/d 2025-12-15 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, FILUSDT, BCHUSDT, SUIUSDT, LUNA2USDT...`
- **Minggu 33:** `WIFUSDT, BCHUSDT, FILUSDT, SUIUSDT, UNIUSDT...`
- **Minggu 34:** `WIFUSDT, BCHUSDT, FILUSDT, SUIUSDT, UNIUSDT...`
- **Minggu 35:** `WIFUSDT, BCHUSDT, FILUSDT, SUIUSDT, LUNA2USDT...`
- **Minggu 36:** `WIFUSDT, BCHUSDT, FILUSDT, SUIUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $35.85 | 24 | 54.17% |
| `MomentumCrossHunter` | 0.2 | $1.59 | 43 | 44.19% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $112.44                     |
| **Net Profit**    | **$37.44 (+49.92%)** |
| Total Trades      | 67                         |
| Win Rate          | 47.76%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 67 trades (47.76%)             |
| Profit Factor     | 1.70                       |
| Max Drawdown      | 26.23%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:31:16

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, SUIUSDT, UNIUSDT, ETCUSDT, FILUSDT...`
- **Minggu 33:** `OMUSDT, ARCUSDT, SUIUSDT, LTCUSDT, UNIUSDT...`
- **Minggu 34:** `OMUSDT, ARCUSDT, SUIUSDT, LTCUSDT, UNIUSDT...`
- **Minggu 35:** `OMUSDT, ARCUSDT, SUIUSDT, LTCUSDT, UNIUSDT...`
- **Minggu 36:** `OMUSDT, ARCUSDT, SUIUSDT, LTCUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $49.54 | 27 | 59.26% |
| `MomentumCrossHunter` | 0.2 | $11.17 | 32 | 53.12% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $135.70                     |
| **Net Profit**    | **$60.70 (+80.94%)** |
| Total Trades      | 59                         |
| Win Rate          | 55.93%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 59 trades (55.93%)             |
| Profit Factor     | 2.17                       |
| Max Drawdown      | 16.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 19:29:00

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `UNIUSDT, AAVEUSDT, ENAUSDT, NEARUSDT, SUIUSDT...`
- **Minggu 33:** `UNIUSDT, AAVEUSDT, ENAUSDT, NEARUSDT, SUIUSDT...`
- **Minggu 34:** `UNIUSDT, AAVEUSDT, ENAUSDT, NEARUSDT, SUIUSDT...`
- **Minggu 35:** `UNIUSDT, ENAUSDT, SUIUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 36:** `UNIUSDT, ENAUSDT, NEARUSDT, SUIUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $37.09 | 34 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $38.58 | 44 | 61.36% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $150.68                     |
| **Net Profit**    | **$75.68 (+100.90%)** |
| Total Trades      | 78                         |
| Win Rate          | 56.41%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 78 trades (56.41%)             |
| Profit Factor     | 1.86                       |
| Max Drawdown      | 17.59%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:52:44

**Parameter:**
-   **Simbol:** Top 60 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-13 (~4 Bulan 5 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, BCHUSDT, UNIUSDT, 1000PEPEUSDT, WIFUSDT...`
- **Minggu 33:** `LTCUSDT, EPICUSDT, OMUSDT, BCHUSDT, 1000PEPEUSDT...`
- **Minggu 34:** `LTCUSDT, TAOUSDT, BCHUSDT, UNIUSDT, 1000PEPEUSDT...`
- **Minggu 35:** `LTCUSDT, EPICUSDT, OMUSDT, TAOUSDT, BCHUSDT...`
- **Minggu 36:** `LTCUSDT, EPICUSDT, OMUSDT, BCHUSDT, 1000PEPEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $25.44 | 18 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $20.92 | 29 | 65.52% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $121.36                     |
| **Net Profit**    | **$46.36 (+61.82%)** |
| Total Trades      | 47                         |
| Win Rate          | 59.57%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 47 trades (59.57%)             |
| Profit Factor     | 1.88                       |
| Max Drawdown      | 14.24%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 12 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:50:25

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-13 (~4 Bulan 5 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FORMUSDT, SUIUSDT, PENGUUSDT, OMUSDT, PUMPUSDT...`
- **Minggu 33:** `ARCUSDT, FORMUSDT, SUIUSDT, PENGUUSDT, OMUSDT...`
- **Minggu 34:** `ARCUSDT, FORMUSDT, SUIUSDT, PENGUUSDT, OMUSDT...`
- **Minggu 35:** `ARCUSDT, FORMUSDT, SUIUSDT, PENGUUSDT, OMUSDT...`
- **Minggu 36:** `ARCUSDT, FORMUSDT, SUIUSDT, PENGUUSDT, OMUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $55.13 | 36 | 55.56% |
| `MomentumCrossHunter` | 0.2 | $16.94 | 36 | 52.78% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $147.07                     |
| **Net Profit**    | **$72.07 (+96.10%)** |
| Total Trades      | 72                         |
| Win Rate          | 54.17%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 72 trades (54.17%)             |
| Profit Factor     | 1.84                       |
| Max Drawdown      | 9.74%                      |
| CB Triggers       | 0                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:47:04

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WLDUSDT, LUNA2USDT, BCHUSDT, PUMPUSDT, ENAUSDT...`
- **Minggu 33:** `WLDUSDT, BCHUSDT, ARCUSDT, ENAUSDT, CRVUSDT...`
- **Minggu 34:** `WLDUSDT, BCHUSDT, PUMPUSDT, ARCUSDT, ENAUSDT...`
- **Minggu 35:** `WLDUSDT, LUNA2USDT, BCHUSDT, PUMPUSDT, CRVUSDT...`
- **Minggu 36:** `WLDUSDT, LUNA2USDT, BCHUSDT, ARCUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $57.56 | 35 | 54.29% |
| `MomentumCrossHunter` | 0.2 | $17.16 | 44 | 54.55% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $149.72                     |
| **Net Profit**    | **$74.72 (+99.63%)** |
| Total Trades      | 79                         |
| Win Rate          | 54.43%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 79 trades (54.43%)             |
| Profit Factor     | 1.97                       |
| Max Drawdown      | 12.76%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:39:42

**Parameter:**
-   **Simbol:** Top 70 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, ETCUSDT, ENAUSDT, SUIUSDT, WIFUSDT...`
- **Minggu 33:** `ETCUSDT, NEARUSDT, ENAUSDT, SUIUSDT, AVAAIUSDT...`
- **Minggu 34:** `NEARUSDT, ETCUSDT, ENAUSDT, SUIUSDT, AAVEUSDT...`
- **Minggu 35:** `ENAUSDT, WIFUSDT, UNIUSDT, WLDUSDT, PENGUUSDT...`
- **Minggu 36:** `ETCUSDT, NEARUSDT, ENAUSDT, AVAAIUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $31.66 | 33 | 48.48% |
| `MomentumCrossHunter` | 0.2 | $4.43 | 44 | 50.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $111.09                     |
| **Net Profit**    | **$36.09 (+48.11%)** |
| Total Trades      | 77                         |
| Win Rate          | 49.35%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 77 trades (49.35%)             |
| Profit Factor     | 1.38                       |
| Max Drawdown      | 21.83%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:35:37

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, PUMPUSDT, FILUSDT, ETCUSDT, ENAUSDT...`
- **Minggu 33:** `ETCUSDT, ENAUSDT, 1000PEPEUSDT, NEARUSDT, PAXGUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, PUMPUSDT, FILUSDT, ETCUSDT, ENAUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, PUMPUSDT, ENAUSDT, PAXGUSDT, ARBUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, FILUSDT, ETCUSDT, ENAUSDT, 1000PEPEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $46.00 | 36 | 47.22% |
| `MomentumCrossHunter` | 0.2 | $31.55 | 47 | 55.32% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $152.55                     |
| **Net Profit**    | **$77.55 (+103.39%)** |
| Total Trades      | 83                         |
| Win Rate          | 51.81%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 83 trades (51.81%)             |
| Profit Factor     | 1.85                       |
| Max Drawdown      | 12.37%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:33:07

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `AAVEUSDT, BCHUSDT, FORMUSDT, PIPPINUSDT, NEARUSDT...`
- **Minggu 33:** `AAVEUSDT, BCHUSDT, LTCUSDT, FORMUSDT, PIPPINUSDT...`
- **Minggu 34:** `AAVEUSDT, BCHUSDT, LTCUSDT, FORMUSDT, PIPPINUSDT...`
- **Minggu 35:** `XPLUSDT, BCHUSDT, LTCUSDT, FORMUSDT, PIPPINUSDT...`
- **Minggu 36:** `XPLUSDT, BCHUSDT, LTCUSDT, FORMUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $50.39 | 38 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $9.69 | 37 | 51.35% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $135.08                     |
| **Net Profit**    | **$60.08 (+80.10%)** |
| Total Trades      | 75                         |
| Win Rate          | 50.67%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 75 trades (50.67%)             |
| Profit Factor     | 1.71                       |
| Max Drawdown      | 16.45%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:31:20

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `AAVEUSDT, OMUSDT, ARBUSDT, DOTUSDT, 1000PEPEUSDT...`
- **Minggu 33:** `AAVEUSDT, OMUSDT, ARCUSDT, DOTUSDT, 1000PEPEUSDT...`
- **Minggu 34:** `TAOUSDT, AAVEUSDT, ARCUSDT, ARBUSDT, 1000PEPEUSDT...`
- **Minggu 35:** `TAOUSDT, OMUSDT, ARBUSDT, DOTUSDT, XPLUSDT...`
- **Minggu 36:** `OMUSDT, ARCUSDT, ARBUSDT, 1000PEPEUSDT, XPLUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $22.07 | 39 | 43.59% |
| `MomentumCrossHunter` | 0.2 | $27.54 | 44 | 54.55% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $124.61                     |
| **Net Profit**    | **$49.61 (+66.15%)** |
| Total Trades      | 83                         |
| Win Rate          | 49.40%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 83 trades (49.40%)             |
| Profit Factor     | 1.61                       |
| Max Drawdown      | 23.94%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:29:46

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-05 s/d 2025-12-16 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `UNIUSDT, ARBUSDT, FARTCOINUSDT, PENGUUSDT, JELLYJELLYUSDT...`
- **Minggu 33:** `UNIUSDT, PAXGUSDT, FARTCOINUSDT, PENGUUSDT, CRVUSDT...`
- **Minggu 34:** `UNIUSDT, ARBUSDT, PAXGUSDT, PENGUUSDT, JELLYJELLYUSDT...`
- **Minggu 35:** `UNIUSDT, ARBUSDT, PAXGUSDT, PENGUUSDT, CRVUSDT...`
- **Minggu 36:** `UNIUSDT, ARBUSDT, FARTCOINUSDT, PENGUUSDT, JELLYJELLYUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $31.13 | 28 | 53.57% |
| `MomentumCrossHunter` | 0.2 | $12.93 | 26 | 69.23% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $119.06                     |
| **Net Profit**    | **$44.06 (+58.74%)** |
| Total Trades      | 54                         |
| Win Rate          | 61.11%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 54 trades (61.11%)             |
| Profit Factor     | 1.92                       |
| Max Drawdown      | 15.93%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 17 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:26:30

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-15 (~4 Bulan 14 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, ARBUSDT, AAVEUSDT, OMUSDT, FILUSDT...`
- **Minggu 33:** `ETCUSDT, ARBUSDT, AAVEUSDT, OMUSDT, ENAUSDT...`
- **Minggu 34:** `ETCUSDT, ARBUSDT, AAVEUSDT, FILUSDT, TAOUSDT...`
- **Minggu 35:** `ARBUSDT, OMUSDT, ORDIUSDT, ENAUSDT, PENGUUSDT...`
- **Minggu 36:** `ETCUSDT, ARBUSDT, OMUSDT, FILUSDT, ORDIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $51.25 | 30 | 63.33% |
| `MomentumCrossHunter` | 0.2 | $-9.11 | 56 | 46.43% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $117.15                     |
| **Net Profit**    | **$42.15 (+56.19%)** |
| Total Trades      | 86                         |
| Win Rate          | 52.33%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 86 trades (52.33%)             |
| Profit Factor     | 1.51                       |
| Max Drawdown      | 14.79%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:23:26

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, FARTCOINUSDT, AAVEUSDT, ORDIUSDT, WLDUSDT...`
- **Minggu 33:** `ARBUSDT, FARTCOINUSDT, AAVEUSDT, NEARUSDT, WLDUSDT...`
- **Minggu 34:** `ARBUSDT, AAVEUSDT, ORDIUSDT, NEARUSDT, WLDUSDT...`
- **Minggu 35:** `ARBUSDT, ORDIUSDT, WLDUSDT, UNIUSDT, XPLUSDT...`
- **Minggu 36:** `ARBUSDT, FARTCOINUSDT, ORDIUSDT, WLDUSDT, NEARUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $52.08 | 34 | 58.82% |
| `MomentumCrossHunter` | 0.2 | $5.45 | 67 | 53.73% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $132.53                     |
| **Net Profit**    | **$57.53 (+76.71%)** |
| Total Trades      | 101                         |
| Win Rate          | 55.45%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 101 trades (55.45%)             |
| Profit Factor     | 1.63                       |
| Max Drawdown      | 12.16%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 4 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:21:09

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FARTCOINUSDT, WLDUSDT, ENAUSDT, FORMUSDT, ARBUSDT...`
- **Minggu 33:** `FARTCOINUSDT, WLDUSDT, ENAUSDT, FORMUSDT, ARBUSDT...`
- **Minggu 34:** `WLDUSDT, ENAUSDT, FORMUSDT, ARBUSDT, PIPPINUSDT...`
- **Minggu 35:** `WLDUSDT, ENAUSDT, FORMUSDT, ARBUSDT, XPLUSDT...`
- **Minggu 36:** `FARTCOINUSDT, WLDUSDT, ENAUSDT, ARBUSDT, XPLUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $51.09 | 33 | 60.61% |
| `MomentumCrossHunter` | 0.2 | $10.76 | 81 | 51.85% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $136.86                     |
| **Net Profit**    | **$61.86 (+82.47%)** |
| Total Trades      | 114                         |
| Win Rate          | 54.39%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 114 trades (54.39%)             |
| Profit Factor     | 1.60                       |
| Max Drawdown      | 15.43%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 4 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:18:29

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, ORDIUSDT, JELLYJELLYUSDT, PENGUUSDT, ETCUSDT...`
- **Minggu 33:** `LTCUSDT, DOTUSDT, HYPEUSDT, CRVUSDT, ETCUSDT...`
- **Minggu 34:** `LTCUSDT, ORDIUSDT, ARBUSDT, HYPEUSDT, JELLYJELLYUSDT...`
- **Minggu 35:** `LTCUSDT, ORDIUSDT, ARBUSDT, DOTUSDT, HYPEUSDT...`
- **Minggu 36:** `LTCUSDT, ARBUSDT, ORDIUSDT, HYPEUSDT, JELLYJELLYUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $25.09 | 38 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $3.46 | 66 | 54.55% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $103.55                     |
| **Net Profit**    | **$28.55 (+38.07%)** |
| Total Trades      | 104                         |
| Win Rate          | 52.88%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 104 trades (52.88%)             |
| Profit Factor     | 1.27                       |
| Max Drawdown      | 15.35%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:10:36

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-17 (~4 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WLDUSDT, FORMUSDT, WIFUSDT, FILUSDT, FHEUSDT...`
- **Minggu 33:** `WLDUSDT, FORMUSDT, WIFUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 34:** `WLDUSDT, FORMUSDT, FILUSDT, BCHUSDT, ETCUSDT...`
- **Minggu 35:** `WLDUSDT, FORMUSDT, FHEUSDT, BCHUSDT, CRVUSDT...`
- **Minggu 36:** `WLDUSDT, WIFUSDT, FHEUSDT, BCHUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $36.24 | 39 | 51.28% |
| `MomentumCrossHunter` | 0.2 | $-0.26 | 69 | 50.72% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $110.98                     |
| **Net Profit**    | **$35.98 (+47.97%)** |
| Total Trades      | 108                         |
| Win Rate          | 50.93%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 108 trades (50.93%)             |
| Profit Factor     | 1.35                       |
| Max Drawdown      | 16.45%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:06:59

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-17 (~4 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, ARBUSDT, JELLYJELLYUSDT, ORDIUSDT, FHEUSDT...`
- **Minggu 33:** `BCHUSDT, WIFUSDT, FORMUSDT, ETCUSDT, CRVUSDT...`
- **Minggu 34:** `BCHUSDT, ARBUSDT, ORDIUSDT, JELLYJELLYUSDT, FORMUSDT...`
- **Minggu 35:** `BCHUSDT, ARBUSDT, JELLYJELLYUSDT, ORDIUSDT, FHEUSDT...`
- **Minggu 36:** `BCHUSDT, WIFUSDT, ARBUSDT, JELLYJELLYUSDT, ORDIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $44.74 | 38 | 52.63% |
| `MomentumCrossHunter` | 0.2 | $3.20 | 68 | 54.41% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $122.93                     |
| **Net Profit**    | **$47.93 (+63.91%)** |
| Total Trades      | 106                         |
| Win Rate          | 53.77%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 106 trades (53.77%)             |
| Profit Factor     | 1.49                       |
| Max Drawdown      | 20.40%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:05:55

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, 1000PEPEUSDT, FARTCOINUSDT, ORDIUSDT, LUNA2USDT...`
- **Minggu 33:** `PAXGUSDT, SUIUSDT, 1000PEPEUSDT, FARTCOINUSDT, CRVUSDT...`
- **Minggu 34:** `PAXGUSDT, SUIUSDT, 1000PEPEUSDT, ORDIUSDT, BCHUSDT...`
- **Minggu 35:** `PAXGUSDT, ORDIUSDT, CRVUSDT, LUNA2USDT, BCHUSDT...`
- **Minggu 36:** `1000PEPEUSDT, FARTCOINUSDT, ORDIUSDT, LUNA2USDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $17.68 | 30 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $-1.08 | 60 | 56.67% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $91.60                     |
| **Net Profit**    | **$16.60 (+22.13%)** |
| Total Trades      | 90                         |
| Win Rate          | 54.44%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 90 trades (54.44%)             |
| Profit Factor     | 1.19                       |
| Max Drawdown      | 21.24%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 8 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:03:56

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-17 (~4 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000PEPEUSDT, ARBUSDT, FORMUSDT, NEARUSDT, PIPPINUSDT...`
- **Minggu 33:** `1000PEPEUSDT, FORMUSDT, NEARUSDT, LTCUSDT, PAXGUSDT...`
- **Minggu 34:** `1000PEPEUSDT, ARBUSDT, FORMUSDT, NEARUSDT, LTCUSDT...`
- **Minggu 35:** `ARBUSDT, FORMUSDT, LTCUSDT, PAXGUSDT, PIPPINUSDT...`
- **Minggu 36:** `1000PEPEUSDT, ARBUSDT, NEARUSDT, LTCUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $31.05 | 29 | 51.72% |
| `MomentumCrossHunter` | 0.2 | $-4.81 | 63 | 47.62% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $101.25                     |
| **Net Profit**    | **$26.25 (+35.00%)** |
| Total Trades      | 92                         |
| Win Rate          | 48.91%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 92 trades (48.91%)             |
| Profit Factor     | 1.31                       |
| Max Drawdown      | 12.74%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 9 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 18:01:07

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, PENGUUSDT, ARBUSDT, ORDIUSDT, PIPPINUSDT...`
- **Minggu 33:** `BCHUSDT, LTCUSDT, ETCUSDT, PENGUUSDT, PAXGUSDT...`
- **Minggu 34:** `BCHUSDT, LTCUSDT, ETCUSDT, PENGUUSDT, ARBUSDT...`
- **Minggu 35:** `BCHUSDT, LTCUSDT, PENGUUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 36:** `BCHUSDT, LTCUSDT, ETCUSDT, PENGUUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $18.88 | 31 | 51.61% |
| `MomentumCrossHunter` | 0.2 | $-4.83 | 55 | 56.36% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $89.05                     |
| **Net Profit**    | **$14.05 (+18.74%)** |
| Total Trades      | 86                         |
| Win Rate          | 54.65%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 86 trades (54.65%)             |
| Profit Factor     | 1.16                       |
| Max Drawdown      | 24.54%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 8 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:59:12

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000PEPEUSDT, OMUSDT, PIPPINUSDT, SUIUSDT, ORDIUSDT...`
- **Minggu 33:** `1000PEPEUSDT, PIPPINUSDT, OMUSDT, SUIUSDT, CRVUSDT...`
- **Minggu 34:** `1000PEPEUSDT, PIPPINUSDT, SUIUSDT, ORDIUSDT, HYPEUSDT...`
- **Minggu 35:** `XPLUSDT, PIPPINUSDT, OMUSDT, ORDIUSDT, CRVUSDT...`
- **Minggu 36:** `1000PEPEUSDT, XPLUSDT, PIPPINUSDT, OMUSDT, ORDIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $29.02 | 39 | 51.28% |
| `MomentumCrossHunter` | 0.2 | $16.63 | 87 | 55.17% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $120.65                     |
| **Net Profit**    | **$45.65 (+60.86%)** |
| Total Trades      | 126                         |
| Win Rate          | 53.97%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 126 trades (53.97%)             |
| Profit Factor     | 1.35                       |
| Max Drawdown      | 15.56%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:57:39

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-17 (~4 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, WIFUSDT, FHEUSDT, PENGUUSDT, FARTCOINUSDT...`
- **Minggu 33:** `NEARUSDT, WIFUSDT, DOTUSDT, PENGUUSDT, FARTCOINUSDT...`
- **Minggu 34:** `NEARUSDT, PENGUUSDT, WLDUSDT, HYPEUSDT, UNIUSDT...`
- **Minggu 35:** `FHEUSDT, PENGUUSDT, DOTUSDT, WLDUSDT, XPLUSDT...`
- **Minggu 36:** `NEARUSDT, WIFUSDT, FHEUSDT, PENGUUSDT, FARTCOINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $43.29 | 35 | 54.29% |
| `MomentumCrossHunter` | 0.2 | $7.10 | 80 | 52.50% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $125.39                     |
| **Net Profit**    | **$50.39 (+67.18%)** |
| Total Trades      | 115                         |
| Win Rate          | 53.04%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 115 trades (53.04%)             |
| Profit Factor     | 1.44                       |
| Max Drawdown      | 15.07%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 4 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:54:06

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-17 (~4 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, ENAUSDT, FILUSDT, SUIUSDT, LUNA2USDT...`
- **Minggu 33:** `ETCUSDT, ENAUSDT, BCHUSDT, HYPEUSDT, SUIUSDT...`
- **Minggu 34:** `ETCUSDT, ENAUSDT, BCHUSDT, FILUSDT, HYPEUSDT...`
- **Minggu 35:** `ENAUSDT, BCHUSDT, HYPEUSDT, LUNA2USDT, PUMPUSDT...`
- **Minggu 36:** `ENAUSDT, ETCUSDT, BCHUSDT, HYPEUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $29.87 | 34 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $5.62 | 59 | 50.85% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $110.49                     |
| **Net Profit**    | **$35.49 (+47.32%)** |
| Total Trades      | 93                         |
| Win Rate          | 50.54%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 93 trades (50.54%)             |
| Profit Factor     | 1.41                       |
| Max Drawdown      | 23.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 8 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:51:42

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-17 (~4 Bulan 16 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, NEARUSDT, PENGUUSDT, WLDUSDT, ETCUSDT...`
- **Minggu 33:** `LTCUSDT, OMUSDT, NEARUSDT, DOTUSDT, PENGUUSDT...`
- **Minggu 34:** `LTCUSDT, NEARUSDT, PENGUUSDT, WLDUSDT, ETCUSDT...`
- **Minggu 35:** `LTCUSDT, OMUSDT, DOTUSDT, PENGUUSDT, WLDUSDT...`
- **Minggu 36:** `LTCUSDT, OMUSDT, NEARUSDT, PENGUUSDT, WLDUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $20.04 | 33 | 48.48% |
| `MomentumCrossHunter` | 0.2 | $-6.45 | 55 | 49.09% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $88.59                     |
| **Net Profit**    | **$13.59 (+18.12%)** |
| Total Trades      | 88                         |
| Win Rate          | 48.86%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 88 trades (48.86%)             |
| Profit Factor     | 1.18                       |
| Max Drawdown      | 20.15%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 11 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:47:19

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, WIFUSDT, ENAUSDT, PENGUUSDT, FHEUSDT...`
- **Minggu 33:** `DOTUSDT, WIFUSDT, BCHUSDT, ENAUSDT, PENGUUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, BCHUSDT, ENAUSDT, PENGUUSDT, HYPEUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, DOTUSDT, BCHUSDT, ENAUSDT, PENGUUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, WIFUSDT, BCHUSDT, ENAUSDT, PENGUUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $19.95 | 26 | 53.85% |
| `MomentumCrossHunter` | 0.2 | $9.64 | 53 | 52.83% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $104.58                     |
| **Net Profit**    | **$29.58 (+39.44%)** |
| Total Trades      | 79                         |
| Win Rate          | 53.16%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 79 trades (53.16%)             |
| Profit Factor     | 1.42                       |
| Max Drawdown      | 11.11%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 15 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:45:26

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ENAUSDT, FHEUSDT, SUIUSDT, FORMUSDT, FILUSDT...`
- **Minggu 33:** `ENAUSDT, HYPEUSDT, LTCUSDT, SUIUSDT, FORMUSDT...`
- **Minggu 34:** `HYPEUSDT, ENAUSDT, LTCUSDT, SUIUSDT, FORMUSDT...`
- **Minggu 35:** `HYPEUSDT, ENAUSDT, LTCUSDT, FHEUSDT, FORMUSDT...`
- **Minggu 36:** `ENAUSDT, HYPEUSDT, LTCUSDT, FHEUSDT, FARTCOINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $69.59 | 41 | 60.98% |
| `MomentumCrossHunter` | 0.2 | $16.54 | 25 | 64.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $161.13                     |
| **Net Profit**    | **$86.13 (+114.84%)** |
| Total Trades      | 66                         |
| Win Rate          | 62.12%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 66 trades (62.12%)             |
| Profit Factor     | 2.22                       |
| Max Drawdown      | 16.55%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:42:45

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000SHIBUSDT, ETCUSDT, ORDIUSDT, ARBUSDT, JELLYJELLYUSDT...`
- **Minggu 33:** `ETCUSDT, 1000SHIBUSDT, BCHUSDT, OMUSDT, LTCUSDT...`
- **Minggu 34:** `ETCUSDT, 1000SHIBUSDT, BCHUSDT, ORDIUSDT, PUMPUSDT...`
- **Minggu 35:** `1000SHIBUSDT, BCHUSDT, ORDIUSDT, PUMPUSDT, ARBUSDT...`
- **Minggu 36:** `1000SHIBUSDT, ETCUSDT, BCHUSDT, ORDIUSDT, ARBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $62.18 | 39 | 58.97% |
| `MomentumCrossHunter` | 0.2 | $20.06 | 25 | 68.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $157.24                     |
| **Net Profit**    | **$82.24 (+109.65%)** |
| Total Trades      | 64                         |
| Win Rate          | 62.50%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 64 trades (62.50%)             |
| Profit Factor     | 2.16                       |
| Max Drawdown      | 22.84%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:40:35

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WLDUSDT, LUNA2USDT, ARBUSDT, ETCUSDT, OMUSDT...`
- **Minggu 33:** `WLDUSDT, FARTCOINUSDT, ETCUSDT, PAXGUSDT, HYPEUSDT...`
- **Minggu 34:** `WLDUSDT, ARBUSDT, ETCUSDT, PAXGUSDT, HYPEUSDT...`
- **Minggu 35:** `WLDUSDT, LUNA2USDT, ARBUSDT, CRVUSDT, PAXGUSDT...`
- **Minggu 36:** `WLDUSDT, LUNA2USDT, ARBUSDT, FARTCOINUSDT, ETCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $56.37 | 40 | 57.50% |
| `MomentumCrossHunter` | 0.2 | $11.53 | 23 | 65.22% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $142.90                     |
| **Net Profit**    | **$67.90 (+90.54%)** |
| Total Trades      | 63                         |
| Win Rate          | 60.32%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 63 trades (60.32%)             |
| Profit Factor     | 2.00                       |
| Max Drawdown      | 21.06%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:38:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FHEUSDT, FORMUSDT, ENAUSDT, WLDUSDT, 1000SHIBUSDT...`
- **Minggu 33:** `FORMUSDT, ENAUSDT, WLDUSDT, 1000SHIBUSDT, PAXGUSDT...`
- **Minggu 34:** `PUMPUSDT, FORMUSDT, ENAUSDT, WLDUSDT, 1000SHIBUSDT...`
- **Minggu 35:** `FHEUSDT, PUMPUSDT, FORMUSDT, ENAUSDT, WLDUSDT...`
- **Minggu 36:** `FHEUSDT, ENAUSDT, WLDUSDT, 1000SHIBUSDT, JELLYJELLYUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $50.44 | 36 | 58.33% |
| `MomentumCrossHunter` | 0.2 | $20.41 | 23 | 69.57% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $145.85                     |
| **Net Profit**    | **$70.85 (+94.47%)** |
| Total Trades      | 59                         |
| Win Rate          | 62.71%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 59 trades (62.71%)             |
| Profit Factor     | 2.10                       |
| Max Drawdown      | 24.44%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:36:23

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, AAVEUSDT, SUIUSDT, PENGUUSDT, NEARUSDT...`
- **Minggu 33:** `AAVEUSDT, SUIUSDT, PENGUUSDT, NEARUSDT, BCHUSDT...`
- **Minggu 34:** `ARBUSDT, AAVEUSDT, SUIUSDT, NEARUSDT, BCHUSDT...`
- **Minggu 35:** `ARBUSDT, PENGUUSDT, LUNA2USDT, BCHUSDT, CRVUSDT...`
- **Minggu 36:** `ARBUSDT, PENGUUSDT, NEARUSDT, LUNA2USDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $38.68 | 34 | 55.88% |
| `MomentumCrossHunter` | 0.2 | $17.96 | 18 | 77.78% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $131.64                     |
| **Net Profit**    | **$56.64 (+75.52%)** |
| Total Trades      | 52                         |
| Win Rate          | 63.46%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 52 trades (63.46%)             |
| Profit Factor     | 1.98                       |
| Max Drawdown      | 21.94%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:35:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, 1000SHIBUSDT, LUNA2USDT, PIPPINUSDT, 1000PEPEUSDT...`
- **Minggu 33:** `SUIUSDT, 1000SHIBUSDT, BCHUSDT, HYPEUSDT, FARTCOINUSDT...`
- **Minggu 34:** `SUIUSDT, 1000SHIBUSDT, BCHUSDT, HYPEUSDT, PIPPINUSDT...`
- **Minggu 35:** `CRVUSDT, 1000SHIBUSDT, BCHUSDT, HYPEUSDT, LUNA2USDT...`
- **Minggu 36:** `1000SHIBUSDT, BCHUSDT, HYPEUSDT, FARTCOINUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $49.76 | 34 | 58.82% |
| `MomentumCrossHunter` | 0.2 | $20.12 | 23 | 69.57% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $144.88                     |
| **Net Profit**    | **$69.88 (+93.18%)** |
| Total Trades      | 57                         |
| Win Rate          | 63.16%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 57 trades (63.16%)             |
| Profit Factor     | 2.08                       |
| Max Drawdown      | 23.46%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:33:27

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, PENGUUSDT, FHEUSDT, JELLYJELLYUSDT, SUIUSDT...`
- **Minggu 33:** `PENGUUSDT, SUIUSDT, FARTCOINUSDT, HYPEUSDT, LTCUSDT...`
- **Minggu 34:** `ARBUSDT, JELLYJELLYUSDT, SUIUSDT, HYPEUSDT, LTCUSDT...`
- **Minggu 35:** `ARBUSDT, PENGUUSDT, FHEUSDT, JELLYJELLYUSDT, HYPEUSDT...`
- **Minggu 36:** `ARBUSDT, PENGUUSDT, FHEUSDT, JELLYJELLYUSDT, FARTCOINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $5.60 | 19 | 47.37% |
| `MomentumCrossHunter` | 0.2 | $-6.76 | 10 | 60.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $73.84                     |
| **Net Profit**    | **$-1.16 (-1.54%)** |
| Total Trades      | 29                         |
| Win Rate          | 51.72%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 29 trades (51.72%)             |
| Profit Factor     | 0.96                       |
| Max Drawdown      | 28.86%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 21 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:32:10

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ORDIUSDT, 1000PEPEUSDT, PIPPINUSDT, ENAUSDT, ETCUSDT...`
- **Minggu 33:** `LTCUSDT, 1000PEPEUSDT, PIPPINUSDT, ENAUSDT, ETCUSDT...`
- **Minggu 34:** `LTCUSDT, PUMPUSDT, ORDIUSDT, 1000PEPEUSDT, PIPPINUSDT...`
- **Minggu 35:** `LTCUSDT, PUMPUSDT, CRVUSDT, ORDIUSDT, PIPPINUSDT...`
- **Minggu 36:** `LTCUSDT, ORDIUSDT, 1000PEPEUSDT, PIPPINUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $18.01 | 37 | 48.65% |
| `MomentumCrossHunter` | 0.2 | $5.19 | 12 | 83.33% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $98.20                     |
| **Net Profit**    | **$23.20 (+30.94%)** |
| Total Trades      | 49                         |
| Win Rate          | 57.14%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 49 trades (57.14%)             |
| Profit Factor     | 1.49                       |
| Max Drawdown      | 28.27%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 6 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:31:20

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `UNIUSDT, ETCUSDT, FILUSDT, WIFUSDT, ENAUSDT...`
- **Minggu 33:** `UNIUSDT, FARTCOINUSDT, BCHUSDT, ETCUSDT, DOTUSDT...`
- **Minggu 34:** `UNIUSDT, BCHUSDT, ETCUSDT, PUMPUSDT, FILUSDT...`
- **Minggu 35:** `UNIUSDT, BCHUSDT, DOTUSDT, PUMPUSDT, ENAUSDT...`
- **Minggu 36:** `UNIUSDT, FARTCOINUSDT, BCHUSDT, XPLUSDT, ETCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $11.17 | 35 | 45.71% |
| `MomentumCrossHunter` | 0.2 | $-0.95 | 12 | 75.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $85.21                     |
| **Net Profit**    | **$10.21 (+13.62%)** |
| Total Trades      | 47                         |
| Win Rate          | 53.19%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 47 trades (53.19%)             |
| Profit Factor     | 1.22                       |
| Max Drawdown      | 30.51%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 6 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:29:54

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, PIPPINUSDT, 1000SHIBUSDT, FORMUSDT, LUNA2USDT...`
- **Minggu 33:** `1000SHIBUSDT, PIPPINUSDT, FORMUSDT, NEARUSDT, WIFUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, 1000SHIBUSDT, PIPPINUSDT, FORMUSDT, NEARUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, PIPPINUSDT, 1000SHIBUSDT, FORMUSDT, LUNA2USDT...`
- **Minggu 36:** `JELLYJELLYUSDT, PIPPINUSDT, 1000SHIBUSDT, LUNA2USDT, NEARUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $54.67 | 37 | 59.46% |
| `MomentumCrossHunter` | 0.2 | $6.88 | 20 | 65.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $136.56                     |
| **Net Profit**    | **$61.56 (+82.08%)** |
| Total Trades      | 57                         |
| Win Rate          | 61.40%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 57 trades (61.40%)             |
| Profit Factor     | 1.93                       |
| Max Drawdown      | 22.94%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:26:36

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, 1000SHIBUSDT, FILUSDT, PIPPINUSDT, AAVEUSDT...`
- **Minggu 33:** `PAXGUSDT, 1000SHIBUSDT, HYPEUSDT, LTCUSDT, PIPPINUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, PAXGUSDT, 1000SHIBUSDT, HYPEUSDT, LTCUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, PAXGUSDT, 1000SHIBUSDT, HYPEUSDT, LTCUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, 1000SHIBUSDT, HYPEUSDT, LTCUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $49.11 | 36 | 58.33% |
| `MomentumCrossHunter` | 0.2 | $16.69 | 25 | 64.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $140.80                     |
| **Net Profit**    | **$65.80 (+87.74%)** |
| Total Trades      | 61                         |
| Win Rate          | 60.66%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 61 trades (60.66%)             |
| Profit Factor     | 1.95                       |
| Max Drawdown      | 26.40%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:17:31

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=19`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, JELLYJELLYUSDT, ETCUSDT, ENAUSDT, UNIUSDT...`
- **Minggu 33:** `SUIUSDT, LTCUSDT, HYPEUSDT, ETCUSDT, ENAUSDT...`
- **Minggu 34:** `SUIUSDT, JELLYJELLYUSDT, LTCUSDT, HYPEUSDT, ETCUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, LTCUSDT, HYPEUSDT, ENAUSDT, UNIUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, LTCUSDT, HYPEUSDT, ETCUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $27.45 | 34 | 55.88% |
| `MomentumCrossHunter` | 0.2 | $-3.45 | 13 | 53.85% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $99.00                     |
| **Net Profit**    | **$24.00 (+32.00%)** |
| Total Trades      | 47                         |
| Win Rate          | 55.32%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 47 trades (55.32%)             |
| Profit Factor     | 1.49                       |
| Max Drawdown      | 32.64%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:04:54

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, ARBUSDT, FHEUSDT, FORMUSDT, PIPPINUSDT...`
- **Minggu 33:** `OMUSDT, FORMUSDT, PIPPINUSDT, NEARUSDT, 1000SHIBUSDT...`
- **Minggu 34:** `ARBUSDT, FORMUSDT, PIPPINUSDT, NEARUSDT, 1000SHIBUSDT...`
- **Minggu 35:** `OMUSDT, ARBUSDT, FHEUSDT, FORMUSDT, PIPPINUSDT...`
- **Minggu 36:** `ARBUSDT, FHEUSDT, PIPPINUSDT, NEARUSDT, 1000SHIBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.07 | 36 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $23.72 | 17 | 82.35% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $102.79                     |
| **Net Profit**    | **$27.79 (+37.05%)** |
| Total Trades      | 53                         |
| Win Rate          | 60.38%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 53 trades (60.38%)             |
| Profit Factor     | 1.33                       |
| Max Drawdown      | 21.66%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 17:03:47

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PENGUUSDT, WLDUSDT, UNIUSDT, WIFUSDT, ETCUSDT...`
- **Minggu 33:** `PENGUUSDT, WLDUSDT, UNIUSDT, WIFUSDT, ETCUSDT...`
- **Minggu 34:** `WLDUSDT, UNIUSDT, ETCUSDT, FILUSDT, ENAUSDT...`
- **Minggu 35:** `PENGUUSDT, WLDUSDT, UNIUSDT, CRVUSDT, ENAUSDT...`
- **Minggu 36:** `PENGUUSDT, WLDUSDT, UNIUSDT, WIFUSDT, ETCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-2.62 | 34 | 47.06% |
| `MomentumCrossHunter` | 0.2 | $6.08 | 12 | 75.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $78.46                     |
| **Net Profit**    | **$3.46 (+4.61%)** |
| Total Trades      | 46                         |
| Win Rate          | 54.35%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 46 trades (54.35%)             |
| Profit Factor     | 1.05                       |
| Max Drawdown      | 21.66%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:59:54

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FORMUSDT, LUNA2USDT, WLDUSDT, FHEUSDT, FILUSDT...`
- **Minggu 33:** `FORMUSDT, LTCUSDT, BCHUSDT, WLDUSDT, ETCUSDT...`
- **Minggu 34:** `FORMUSDT, LTCUSDT, BCHUSDT, WLDUSDT, PUMPUSDT...`
- **Minggu 35:** `CRVUSDT, FORMUSDT, LTCUSDT, BCHUSDT, LUNA2USDT...`
- **Minggu 36:** `LTCUSDT, BCHUSDT, LUNA2USDT, WLDUSDT, FHEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $7.61 | 40 | 45.00% |
| `MomentumCrossHunter` | 0.2 | $5.15 | 15 | 66.67% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $87.75                     |
| **Net Profit**    | **$12.75 (+17.01%)** |
| Total Trades      | 55                         |
| Win Rate          | 50.91%                     |
|  - Long Win Rate  | 5 trades (20.00%)              |
|  - Short Win Rate | 50 trades (54.00%)             |
| Profit Factor     | 1.23                       |
| Max Drawdown      | 16.32%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 8 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:58:17

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=True`, `min_adx_level=20`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FHEUSDT, NEARUSDT, 1000SHIBUSDT, LUNA2USDT, OMUSDT...`
- **Minggu 33:** `NEARUSDT, 1000SHIBUSDT, DOTUSDT, UNIUSDT, OMUSDT...`
- **Minggu 34:** `NEARUSDT, 1000SHIBUSDT, UNIUSDT, BCHUSDT, PAXGUSDT...`
- **Minggu 35:** `FHEUSDT, LUNA2USDT, 1000SHIBUSDT, DOTUSDT, UNIUSDT...`
- **Minggu 36:** `FHEUSDT, NEARUSDT, LUNA2USDT, 1000SHIBUSDT, UNIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $1.37 | 43 | 44.19% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $76.37                     |
| **Net Profit**    | **$1.37 (+1.83%)** |
| Total Trades      | 43                         |
| Win Rate          | 44.19%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 40 trades (47.50%)             |
| Profit Factor     | 1.02                       |
| Max Drawdown      | 20.22%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 1 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:54:08

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, JELLYJELLYUSDT, LUNA2USDT, OMUSDT, UNIUSDT...`
- **Minggu 33:** `WIFUSDT, OMUSDT, UNIUSDT, WLDUSDT, SUIUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, UNIUSDT, SUIUSDT, WLDUSDT, PAXGUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, LUNA2USDT, OMUSDT, UNIUSDT, WLDUSDT...`
- **Minggu 36:** `WIFUSDT, JELLYJELLYUSDT, LUNA2USDT, UNIUSDT, WLDUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $19.34 | 43 | 48.84% |
| `MomentumCrossHunter` | 0.2 | $4.25 | 16 | 62.50% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $98.59                     |
| **Net Profit**    | **$23.59 (+31.46%)** |
| Total Trades      | 59                         |
| Win Rate          | 52.54%                     |
|  - Long Win Rate  | 6 trades (16.67%)              |
|  - Short Win Rate | 53 trades (56.60%)             |
| Profit Factor     | 1.35                       |
| Max Drawdown      | 19.43%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 3 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:52:11

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PENGUUSDT, AAVEUSDT, FORMUSDT, WLDUSDT, ENAUSDT...`
- **Minggu 33:** `PENGUUSDT, BCHUSDT, AAVEUSDT, LTCUSDT, FORMUSDT...`
- **Minggu 34:** `BCHUSDT, PUMPUSDT, AAVEUSDT, LTCUSDT, FORMUSDT...`
- **Minggu 35:** `PENGUUSDT, BCHUSDT, PUMPUSDT, LTCUSDT, FORMUSDT...`
- **Minggu 36:** `PENGUUSDT, BCHUSDT, LTCUSDT, WLDUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $10.10 | 36 | 50.00% |
| `MomentumCrossHunter` | 0.2 | $2.82 | 14 | 50.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $87.92                     |
| **Net Profit**    | **$12.92 (+17.22%)** |
| Total Trades      | 50                         |
| Win Rate          | 50.00%                     |
|  - Long Win Rate  | 4 trades (0.00%)              |
|  - Short Win Rate | 46 trades (54.35%)             |
| Profit Factor     | 1.25                       |
| Max Drawdown      | 16.08%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 17 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:50:20

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=20`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ORDIUSDT, ENAUSDT, FORMUSDT, WIFUSDT, UNIUSDT...`
- **Minggu 33:** `BCHUSDT, ENAUSDT, LTCUSDT, FORMUSDT, PAXGUSDT...`
- **Minggu 34:** `BCHUSDT, PUMPUSDT, ORDIUSDT, ENAUSDT, LTCUSDT...`
- **Minggu 35:** `BCHUSDT, PUMPUSDT, ORDIUSDT, ENAUSDT, LTCUSDT...`
- **Minggu 36:** `BCHUSDT, ORDIUSDT, ENAUSDT, LTCUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.03 | 38 | 44.74% |
| `MomentumCrossHunter` | 0.2 | $3.03 | 12 | 50.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $82.06                     |
| **Net Profit**    | **$7.06 (+9.41%)** |
| Total Trades      | 50                         |
| Win Rate          | 46.00%                     |
|  - Long Win Rate  | 5 trades (0.00%)              |
|  - Short Win Rate | 45 trades (51.11%)             |
| Profit Factor     | 1.13                       |
| Max Drawdown      | 14.32%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 17 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:41:28

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, FILUSDT, OMUSDT, ARBUSDT, UNIUSDT...`
- **Minggu 33:** `NEARUSDT, OMUSDT, BCHUSDT, UNIUSDT, WIFUSDT...`
- **Minggu 34:** `NEARUSDT, PUMPUSDT, FILUSDT, BCHUSDT, ARBUSDT...`
- **Minggu 35:** `PUMPUSDT, OMUSDT, BCHUSDT, ARBUSDT, UNIUSDT...`
- **Minggu 36:** `NEARUSDT, BCHUSDT, ARBUSDT, UNIUSDT, JELLYJELLYUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $14.32 | 38 | 47.37% |
| `MomentumCrossHunter` | 0.2 | $1.23 | 9 | 55.56% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $90.56                     |
| **Net Profit**    | **$15.56 (+20.74%)** |
| Total Trades      | 47                         |
| Win Rate          | 48.94%                     |
|  - Long Win Rate  | 4 trades (25.00%)              |
|  - Short Win Rate | 43 trades (51.16%)             |
| Profit Factor     | 1.29                       |
| Max Drawdown      | 16.09%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:39:42

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-14 (~4 Bulan 13 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `AAVEUSDT, 1000SHIBUSDT, ARBUSDT, JELLYJELLYUSDT, WLDUSDT...`
- **Minggu 33:** `AAVEUSDT, 1000SHIBUSDT, PAXGUSDT, WLDUSDT, LTCUSDT...`
- **Minggu 34:** `AAVEUSDT, 1000SHIBUSDT, ARBUSDT, PAXGUSDT, PUMPUSDT...`
- **Minggu 35:** `1000SHIBUSDT, ARBUSDT, PAXGUSDT, PUMPUSDT, JELLYJELLYUSDT...`
- **Minggu 36:** `ARBUSDT, 1000SHIBUSDT, JELLYJELLYUSDT, WLDUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-3.57 | 26 | 42.31% |
| `MomentumCrossHunter` | 0.2 | $-7.96 | 33 | 54.55% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $63.48                     |
| **Net Profit**    | **$-11.52 (-15.36%)** |
| Total Trades      | 59                         |
| Win Rate          | 49.15%                     |
|  - Long Win Rate  | 5 trades (0.00%)              |
|  - Short Win Rate | 54 trades (53.70%)             |
| Profit Factor     | 0.81                       |
| Max Drawdown      | 35.81%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 20 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:33:21

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, 1000SHIBUSDT, WLDUSDT, ETCUSDT, PENGUUSDT...`
- **Minggu 33:** `LTCUSDT, NEARUSDT, 1000SHIBUSDT, ETCUSDT, WLDUSDT...`
- **Minggu 34:** `LTCUSDT, NEARUSDT, 1000SHIBUSDT, ETCUSDT, WLDUSDT...`
- **Minggu 35:** `LTCUSDT, 1000SHIBUSDT, WLDUSDT, PENGUUSDT, UNIUSDT...`
- **Minggu 36:** `LTCUSDT, 1000SHIBUSDT, NEARUSDT, ETCUSDT, WLDUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $14.93 | 36 | 47.22% |
| `MomentumCrossHunter` | 0.2 | $2.86 | 8 | 62.50% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $92.79                     |
| **Net Profit**    | **$17.79 (+23.72%)** |
| Total Trades      | 44                         |
| Win Rate          | 50.00%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 41 trades (53.66%)             |
| Profit Factor     | 1.35                       |
| Max Drawdown      | 14.24%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:31:53

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, LUNA2USDT, FORMUSDT, WIFUSDT, PENGUUSDT...`
- **Minggu 33:** `HYPEUSDT, FORMUSDT, WIFUSDT, PENGUUSDT, UNIUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, HYPEUSDT, FORMUSDT, PUMPUSDT, FILUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, HYPEUSDT, FORMUSDT, LUNA2USDT, PUMPUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, HYPEUSDT, LUNA2USDT, WIFUSDT, PENGUUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $19.13 | 35 | 51.43% |
| `MomentumCrossHunter` | 0.2 | $0.94 | 9 | 55.56% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $95.07                     |
| **Net Profit**    | **$20.07 (+26.76%)** |
| Total Trades      | 44                         |
| Win Rate          | 52.27%                     |
|  - Long Win Rate  | 5 trades (20.00%)              |
|  - Short Win Rate | 39 trades (56.41%)             |
| Profit Factor     | 1.38                       |
| Max Drawdown      | 14.40%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 6 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:29:19

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, 1000SHIBUSDT, WLDUSDT, OMUSDT, JELLYJELLYUSDT...`
- **Minggu 33:** `ETCUSDT, 1000SHIBUSDT, WLDUSDT, HYPEUSDT, OMUSDT...`
- **Minggu 34:** `ETCUSDT, 1000SHIBUSDT, WLDUSDT, HYPEUSDT, JELLYJELLYUSDT...`
- **Minggu 35:** `1000SHIBUSDT, WLDUSDT, HYPEUSDT, OMUSDT, CRVUSDT...`
- **Minggu 36:** `ETCUSDT, 1000SHIBUSDT, WLDUSDT, HYPEUSDT, FARTCOINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $15.29 | 38 | 47.37% |
| `MomentumCrossHunter` | 0.2 | $-1.09 | 8 | 50.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $89.20                     |
| **Net Profit**    | **$14.20 (+18.93%)** |
| Total Trades      | 46                         |
| Win Rate          | 47.83%                     |
|  - Long Win Rate  | 5 trades (20.00%)              |
|  - Short Win Rate | 41 trades (51.22%)             |
| Profit Factor     | 1.27                       |
| Max Drawdown      | 15.42%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 16:26:29

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `OMUSDT, FHEUSDT, ENAUSDT, 1000SHIBUSDT, ORDIUSDT...`
- **Minggu 33:** `OMUSDT, BCHUSDT, ENAUSDT, 1000SHIBUSDT, HYPEUSDT...`
- **Minggu 34:** `BCHUSDT, ENAUSDT, 1000SHIBUSDT, HYPEUSDT, ORDIUSDT...`
- **Minggu 35:** `OMUSDT, FHEUSDT, CRVUSDT, BCHUSDT, ENAUSDT...`
- **Minggu 36:** `FHEUSDT, XPLUSDT, BCHUSDT, ENAUSDT, 1000SHIBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $18.64 | 37 | 48.65% |
| `MomentumCrossHunter` | 0.2 | $-0.59 | 9 | 55.56% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $93.05                     |
| **Net Profit**    | **$18.05 (+24.07%)** |
| Total Trades      | 46                         |
| Win Rate          | 50.00%                     |
|  - Long Win Rate  | 4 trades (25.00%)              |
|  - Short Win Rate | 42 trades (52.38%)             |
| Profit Factor     | 1.35                       |
| Max Drawdown      | 15.56%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 5 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 15:11:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-13 (~4 Bulan 5 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=22`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000SHIBUSDT, ARBUSDT, ORDIUSDT, ENAUSDT, WIFUSDT...`
- **Minggu 33:** `1000SHIBUSDT, ENAUSDT, WIFUSDT, DOTUSDT, WLDUSDT...`
- **Minggu 34:** `1000SHIBUSDT, ARBUSDT, ORDIUSDT, ENAUSDT, WLDUSDT...`
- **Minggu 35:** `1000SHIBUSDT, ARBUSDT, ORDIUSDT, ENAUSDT, XPLUSDT...`
- **Minggu 36:** `1000SHIBUSDT, ARBUSDT, ORDIUSDT, SOMIUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $55.99 | 40 | 57.50% |
| `MomentumCrossHunter` | 0.2 | $-14.75 | 26 | 34.62% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $116.24                     |
| **Net Profit**    | **$41.24 (+54.99%)** |
| Total Trades      | 66                         |
| Win Rate          | 48.48%                     |
|  - Long Win Rate  | 15 trades (26.67%)              |
|  - Short Win Rate | 51 trades (54.90%)             |
| Profit Factor     | 1.55                       |
| Max Drawdown      | 17.13%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 15:09:49

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-07 s/d 2025-12-15 (~4 Bulan 11 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FARTCOINUSDT, NEARUSDT, PENGUUSDT, PIPPINUSDT, 1000PEPEUSDT...`
- **Minggu 33:** `FARTCOINUSDT, NEARUSDT, PENGUUSDT, PIPPINUSDT, 1000PEPEUSDT...`
- **Minggu 34:** `NEARUSDT, PIPPINUSDT, 1000PEPEUSDT, PUMPUSDT, ORDIUSDT...`
- **Minggu 35:** `CRVUSDT, PENGUUSDT, PIPPINUSDT, PUMPUSDT, ORDIUSDT...`
- **Minggu 36:** `FARTCOINUSDT, NEARUSDT, PENGUUSDT, 1000PEPEUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $21.27 | 30 | 53.33% |
| `MomentumCrossHunter` | 0.2 | $-22.63 | 84 | 44.05% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $73.65                     |
| **Net Profit**    | **$-1.35 (-1.81%)** |
| Total Trades      | 114                         |
| Win Rate          | 46.49%                     |
|  - Long Win Rate  | 46 trades (36.96%)              |
|  - Short Win Rate | 68 trades (52.94%)             |
| Profit Factor     | 0.99                       |
| Max Drawdown      | 31.36%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 15:03:12

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-07 s/d 2025-12-16 (~4 Bulan 12 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FORMUSDT, OMUSDT, 1000SHIBUSDT, ORDIUSDT, WLDUSDT...`
- **Minggu 33:** `DOTUSDT, FORMUSDT, OMUSDT, 1000SHIBUSDT, WLDUSDT...`
- **Minggu 34:** `FORMUSDT, 1000SHIBUSDT, ORDIUSDT, WLDUSDT, BCHUSDT...`
- **Minggu 35:** `DOTUSDT, FORMUSDT, OMUSDT, 1000SHIBUSDT, ORDIUSDT...`
- **Minggu 36:** `SOMIUSDT, 1000SHIBUSDT, ORDIUSDT, WLDUSDT, XPLUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $22.72 | 32 | 53.12% |
| `MomentumCrossHunter` | 0.2 | $-36.54 | 113 | 38.94% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $61.18                     |
| **Net Profit**    | **$-13.82 (-18.43%)** |
| Total Trades      | 145                         |
| Win Rate          | 42.07%                     |
|  - Long Win Rate  | 57 trades (31.58%)              |
|  - Short Win Rate | 88 trades (48.86%)             |
| Profit Factor     | 0.89                       |
| Max Drawdown      | 30.89%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 8 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:58:39

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-13 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=False`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PENGUUSDT, 1000SHIBUSDT, FARTCOINUSDT, LUNA2USDT, WIFUSDT...`
- **Minggu 33:** `PENGUUSDT, 1000SHIBUSDT, HYPEUSDT, FARTCOINUSDT, BCHUSDT...`
- **Minggu 34:** `1000SHIBUSDT, HYPEUSDT, BCHUSDT, PUMPUSDT, PIPPINUSDT...`
- **Minggu 35:** `PENGUUSDT, 1000SHIBUSDT, HYPEUSDT, LUNA2USDT, BCHUSDT...`
- **Minggu 36:** `PENGUUSDT, 1000SHIBUSDT, HYPEUSDT, FARTCOINUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $46.12 | 38 | 55.26% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $121.12                     |
| **Net Profit**    | **$46.12 (+61.49%)** |
| Total Trades      | 38                         |
| Win Rate          | 55.26%                     |
|  - Long Win Rate  | 1 trades (0.00%)              |
|  - Short Win Rate | 37 trades (56.76%)             |
| Profit Factor     | 2.10                       |
| Max Drawdown      | 15.26%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:57:18

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=True`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ORDIUSDT, FILUSDT, AAVEUSDT, PENGUUSDT, ARBUSDT...`
- **Minggu 33:** `HYPEUSDT, AAVEUSDT, PENGUUSDT, PIPPINUSDT, 1000SHIBUSDT...`
- **Minggu 34:** `HYPEUSDT, ORDIUSDT, FILUSDT, AAVEUSDT, ARBUSDT...`
- **Minggu 35:** `HYPEUSDT, ORDIUSDT, PENGUUSDT, ARBUSDT, PIPPINUSDT...`
- **Minggu 36:** `HYPEUSDT, ORDIUSDT, PENGUUSDT, ARBUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-8.24 | 6 | 0.00% |
| `MomentumCrossHunter` | 0.2 | $-40.05 | 329 | 33.74% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $26.71                     |
| **Net Profit**    | **$-48.29 (-64.38%)** |
| Total Trades      | 335                         |
| Win Rate          | 33.13%                     |
|  - Long Win Rate  | 163 trades (34.97%)              |
|  - Short Win Rate | 172 trades (31.40%)             |
| Profit Factor     | 0.72                       |
| Max Drawdown      | 70.30%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 33 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:49:27

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-13 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `extreme_test_mode=True`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WLDUSDT, ETCUSDT, FARTCOINUSDT, LUNA2USDT, FORMUSDT...`
- **Minggu 33:** `WLDUSDT, ETCUSDT, FARTCOINUSDT, PAXGUSDT, FORMUSDT...`
- **Minggu 34:** `WLDUSDT, ETCUSDT, PAXGUSDT, FORMUSDT, BCHUSDT...`
- **Minggu 35:** `WLDUSDT, CRVUSDT, PAXGUSDT, LUNA2USDT, FORMUSDT...`
- **Minggu 36:** `WLDUSDT, FARTCOINUSDT, ETCUSDT, LUNA2USDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $41.15 | 39 | 53.85% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $116.15                     |
| **Net Profit**    | **$41.15 (+54.86%)** |
| Total Trades      | 39                         |
| Win Rate          | 53.85%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 37 trades (56.76%)             |
| Profit Factor     | 1.93                       |
| Max Drawdown      | 15.26%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:43:20

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-13 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, 1000PEPEUSDT, UNIUSDT, ORDIUSDT, SUIUSDT...`
- **Minggu 33:** `NEARUSDT, 1000PEPEUSDT, UNIUSDT, BCHUSDT, HYPEUSDT...`
- **Minggu 34:** `NEARUSDT, 1000PEPEUSDT, UNIUSDT, BCHUSDT, HYPEUSDT...`
- **Minggu 35:** `UNIUSDT, BCHUSDT, HYPEUSDT, LTCUSDT, ORDIUSDT...`
- **Minggu 36:** `NEARUSDT, 1000PEPEUSDT, UNIUSDT, BCHUSDT, HYPEUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $18.27 | 33 | 51.52% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $93.27                     |
| **Net Profit**    | **$18.27 (+24.36%)** |
| Total Trades      | 33                         |
| Win Rate          | 51.52%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 31 trades (54.84%)             |
| Profit Factor     | 1.46                       |
| Max Drawdown      | 15.58%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:36:40

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-13 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000SHIBUSDT, ENAUSDT, 1000PEPEUSDT, ARBUSDT, JELLYJELLYUSDT...`
- **Minggu 33:** `1000SHIBUSDT, ENAUSDT, 1000PEPEUSDT, BCHUSDT, PAXGUSDT...`
- **Minggu 34:** `1000SHIBUSDT, ENAUSDT, 1000PEPEUSDT, PUMPUSDT, BCHUSDT...`
- **Minggu 35:** `1000SHIBUSDT, ENAUSDT, PUMPUSDT, BCHUSDT, PAXGUSDT...`
- **Minggu 36:** `1000SHIBUSDT, ENAUSDT, 1000PEPEUSDT, BCHUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $21.00 | 32 | 53.12% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $96.00                     |
| **Net Profit**    | **$21.00 (+28.00%)** |
| Total Trades      | 32                         |
| Win Rate          | 53.12%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 30 trades (56.67%)             |
| Profit Factor     | 1.55                       |
| Max Drawdown      | 15.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:34:52

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-13 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, ETCUSDT, ORDIUSDT, LUNA2USDT, ENAUSDT...`
- **Minggu 33:** `WIFUSDT, ETCUSDT, ENAUSDT, LTCUSDT, FORMUSDT...`
- **Minggu 34:** `ETCUSDT, ORDIUSDT, ENAUSDT, LTCUSDT, FORMUSDT...`
- **Minggu 35:** `ORDIUSDT, LUNA2USDT, ENAUSDT, LTCUSDT, FORMUSDT...`
- **Minggu 36:** `WIFUSDT, ETCUSDT, ORDIUSDT, ENAUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $18.27 | 33 | 51.52% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $93.27                     |
| **Net Profit**    | **$18.27 (+24.36%)** |
| Total Trades      | 33                         |
| Win Rate          | 51.52%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 31 trades (54.84%)             |
| Profit Factor     | 1.46                       |
| Max Drawdown      | 15.58%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:33:22

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-13 (~3 Bulan 28 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.8`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FILUSDT, AAVEUSDT, PIPPINUSDT, ETCUSDT, UNIUSDT...`
- **Minggu 33:** `AAVEUSDT, PIPPINUSDT, HYPEUSDT, ETCUSDT, PAXGUSDT...`
- **Minggu 34:** `FILUSDT, AAVEUSDT, PIPPINUSDT, HYPEUSDT, ETCUSDT...`
- **Minggu 35:** `PIPPINUSDT, HYPEUSDT, PAXGUSDT, UNIUSDT, LUNA2USDT...`
- **Minggu 36:** `PIPPINUSDT, HYPEUSDT, ETCUSDT, UNIUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $31.17 | 30 | 56.67% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $106.17                     |
| **Net Profit**    | **$31.17 (+41.56%)** |
| Total Trades      | 30                         |
| Win Rate          | 56.67%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 30 trades (56.67%)             |
| Profit Factor     | 2.02                       |
| Max Drawdown      | 15.00%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:32:18

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.2`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PIPPINUSDT, PENGUUSDT, WLDUSDT, ARBUSDT, ETCUSDT...`
- **Minggu 33:** `PIPPINUSDT, PENGUUSDT, WLDUSDT, DOTUSDT, ETCUSDT...`
- **Minggu 34:** `PIPPINUSDT, WLDUSDT, ARBUSDT, ETCUSDT, BCHUSDT...`
- **Minggu 35:** `PIPPINUSDT, PENGUUSDT, WLDUSDT, DOTUSDT, ARBUSDT...`
- **Minggu 36:** `PIPPINUSDT, PENGUUSDT, WLDUSDT, ARBUSDT, ETCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $5.74 | 22 | 40.91% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $80.74                     |
| **Net Profit**    | **$5.74 (+7.65%)** |
| Total Trades      | 22                         |
| Win Rate          | 40.91%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 22 trades (40.91%)             |
| Profit Factor     | 1.24                       |
| Max Drawdown      | 11.97%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:30:41

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ENAUSDT, ORDIUSDT, PENGUUSDT, AAVEUSDT, TRUMPUSDT...`
- **Minggu 33:** `ENAUSDT, PENGUUSDT, AAVEUSDT, PAXGUSDT, ETCUSDT...`
- **Minggu 34:** `ENAUSDT, ORDIUSDT, PUMPUSDT, AAVEUSDT, PAXGUSDT...`
- **Minggu 35:** `ORDIUSDT, ENAUSDT, PENGUUSDT, PUMPUSDT, CRVUSDT...`
- **Minggu 36:** `ENAUSDT, ORDIUSDT, PENGUUSDT, SOMIUSDT, TRUMPUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $3.66 | 26 | 46.15% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $78.66                     |
| **Net Profit**    | **$3.66 (+4.88%)** |
| Total Trades      | 26                         |
| Win Rate          | 46.15%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 26 trades (46.15%)             |
| Profit Factor     | 1.11                       |
| Max Drawdown      | 13.31%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:26:42

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, WLDUSDT, PIPPINUSDT, TRUMPUSDT, LUNA2USDT...`
- **Minggu 33:** `HYPEUSDT, SUIUSDT, WLDUSDT, FARTCOINUSDT, PIPPINUSDT...`
- **Minggu 34:** `PUMPUSDT, HYPEUSDT, SUIUSDT, WLDUSDT, PIPPINUSDT...`
- **Minggu 35:** `PUMPUSDT, HYPEUSDT, WLDUSDT, CRVUSDT, PIPPINUSDT...`
- **Minggu 36:** `HYPEUSDT, WLDUSDT, FARTCOINUSDT, PIPPINUSDT, TRUMPUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $3.66 | 26 | 46.15% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $78.66                     |
| **Net Profit**    | **$3.66 (+4.88%)** |
| Total Trades      | 26                         |
| Win Rate          | 46.15%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 26 trades (46.15%)             |
| Profit Factor     | 1.11                       |
| Max Drawdown      | 13.31%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:11:53

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=4.0`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, TIAUSDT, LUNA2USDT, ENAUSDT, JELLYJELLYUSDT...`
- **Minggu 33:** `PAXGUSDT, TIAUSDT, BCHUSDT, FARTCOINUSDT, ENAUSDT...`
- **Minggu 34:** `PAXGUSDT, TIAUSDT, BCHUSDT, PUMPUSDT, ENAUSDT...`
- **Minggu 35:** `PAXGUSDT, BCHUSDT, LUNA2USDT, PUMPUSDT, ENAUSDT...`
- **Minggu 36:** `WIFUSDT, BCHUSDT, LUNA2USDT, FARTCOINUSDT, ENAUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $8.12 | 25 | 48.00% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $83.12                     |
| **Net Profit**    | **$8.12 (+10.83%)** |
| Total Trades      | 25                         |
| Win Rate          | 48.00%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 25 trades (48.00%)             |
| Profit Factor     | 1.26                       |
| Max Drawdown      | 13.31%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:09:38

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.015`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, TIAUSDT, OMUSDT, ETCUSDT, UNIUSDT...`
- **Minggu 33:** `NEARUSDT, TIAUSDT, OMUSDT, ETCUSDT, UNIUSDT...`
- **Minggu 34:** `NEARUSDT, TIAUSDT, ETCUSDT, UNIUSDT, SUIUSDT...`
- **Minggu 35:** `CRVUSDT, OMUSDT, UNIUSDT, WLDUSDT, ENAUSDT...`
- **Minggu 36:** `NEARUSDT, ETCUSDT, UNIUSDT, SOMIUSDT, WLDUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-8.65 | 44 | 43.18% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $66.35                     |
| **Net Profit**    | **$-8.65 (-11.54%)** |
| Total Trades      | 44                         |
| Win Rate          | 43.18%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 41 trades (46.34%)             |
| Profit Factor     | 0.82                       |
| Max Drawdown      | 24.48%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:06:41

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `LUNA2USDT, ARBUSDT, ENAUSDT, ETCUSDT, PIPPINUSDT...`
- **Minggu 33:** `PAXGUSDT, ENAUSDT, ETCUSDT, PIPPINUSDT, AAVEUSDT...`
- **Minggu 34:** `PAXGUSDT, ARBUSDT, ENAUSDT, ETCUSDT, PIPPINUSDT...`
- **Minggu 35:** `PAXGUSDT, LUNA2USDT, ARBUSDT, XPLUSDT, ENAUSDT...`
- **Minggu 36:** `ARBUSDT, LUNA2USDT, XPLUSDT, ENAUSDT, FARTCOINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-23.67 | 38 | 39.47% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $51.33                     |
| **Net Profit**    | **$-23.67 (-31.56%)** |
| Total Trades      | 38                         |
| Win Rate          | 39.47%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 35 trades (42.86%)             |
| Profit Factor     | 0.70                       |
| Max Drawdown      | 45.07%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 9 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:05:17

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `FILUSDT, PENGUUSDT, OMUSDT, FORMUSDT, TIAUSDT...`
- **Minggu 33:** `PENGUUSDT, OMUSDT, FORMUSDT, TIAUSDT, AAVEUSDT...`
- **Minggu 34:** `FILUSDT, FORMUSDT, TIAUSDT, AAVEUSDT, HYPEUSDT...`
- **Minggu 35:** `XPLUSDT, PENGUUSDT, OMUSDT, FORMUSDT, HYPEUSDT...`
- **Minggu 36:** `XPLUSDT, PENGUUSDT, HYPEUSDT, ENAUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-23.67 | 38 | 39.47% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $51.33                     |
| **Net Profit**    | **$-23.67 (-31.56%)** |
| Total Trades      | 38                         |
| Win Rate          | 39.47%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 35 trades (42.86%)             |
| Profit Factor     | 0.70                       |
| Max Drawdown      | 45.07%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 9 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:03:38

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ARBUSDT, WIFUSDT, PENGUUSDT, 1000SHIBUSDT, 1000PEPEUSDT...`
- **Minggu 33:** `BCHUSDT, PENGUUSDT, 1000SHIBUSDT, 1000PEPEUSDT, ETCUSDT...`
- **Minggu 34:** `BCHUSDT, ARBUSDT, 1000SHIBUSDT, 1000PEPEUSDT, ETCUSDT...`
- **Minggu 35:** `BCHUSDT, ARBUSDT, PENGUUSDT, 1000SHIBUSDT, UNIUSDT...`
- **Minggu 36:** `SOMIUSDT, BCHUSDT, ARBUSDT, WIFUSDT, PENGUUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-23.67 | 38 | 39.47% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $51.33                     |
| **Net Profit**    | **$-23.67 (-31.56%)** |
| Total Trades      | 38                         |
| Win Rate          | 39.47%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 35 trades (42.86%)             |
| Profit Factor     | 0.70                       |
| Max Drawdown      | 45.07%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 9 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 14:00:37

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `TIAUSDT, AAVEUSDT, PENGUUSDT, FILUSDT, 1000SHIBUSDT...`
- **Minggu 33:** `TIAUSDT, AAVEUSDT, PENGUUSDT, PIPPINUSDT, 1000SHIBUSDT...`
- **Minggu 34:** `TIAUSDT, AAVEUSDT, PIPPINUSDT, FILUSDT, 1000SHIBUSDT...`
- **Minggu 35:** `XPLUSDT, PENGUUSDT, PIPPINUSDT, 1000SHIBUSDT, LUNA2USDT...`
- **Minggu 36:** `XPLUSDT, PENGUUSDT, PIPPINUSDT, 1000SHIBUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-14.85 | 43 | 44.19% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $60.15                     |
| **Net Profit**    | **$-14.85 (-19.80%)** |
| Total Trades      | 43                         |
| Win Rate          | 44.19%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 41 trades (46.34%)             |
| Profit Factor     | 0.83                       |
| Max Drawdown      | 40.09%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 13:57:10

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-10 (~3 Bulan 25 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_filter=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, ETCUSDT, OMUSDT, 1000PEPEUSDT, LUNA2USDT...`
- **Minggu 33:** `ETCUSDT, OMUSDT, 1000PEPEUSDT, FARTCOINUSDT, AAVEUSDT...`
- **Minggu 34:** `ETCUSDT, PUMPUSDT, 1000PEPEUSDT, AAVEUSDT, ARBUSDT...`
- **Minggu 35:** `XPLUSDT, PUMPUSDT, OMUSDT, LUNA2USDT, ARBUSDT...`
- **Minggu 36:** `XPLUSDT, WIFUSDT, ETCUSDT, FARTCOINUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-13.09 | 42 | 45.24% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $61.91                     |
| **Net Profit**    | **$-13.09 (-17.46%)** |
| Total Trades      | 42                         |
| Win Rate          | 45.24%                     |
|  - Long Win Rate  | 2 trades (0.00%)              |
|  - Short Win Rate | 40 trades (47.50%)             |
| Profit Factor     | 0.85                       |
| Max Drawdown      | 40.09%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 2 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 13:03:44

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_or_logic=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `PIPPINUSDT, PENGUUSDT, SUIUSDT, WLDUSDT, LUNA2USDT...`
- **Minggu 33:** `PIPPINUSDT, PENGUUSDT, SUIUSDT, WLDUSDT, HYPEUSDT...`
- **Minggu 34:** `PIPPINUSDT, SUIUSDT, WLDUSDT, JELLYJELLYUSDT, HYPEUSDT...`
- **Minggu 35:** `XPLUSDT, PIPPINUSDT, PENGUUSDT, WLDUSDT, LUNA2USDT...`
- **Minggu 36:** `XPLUSDT, PIPPINUSDT, PENGUUSDT, WLDUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 12:47:06

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_or_logic=False`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, PENGUUSDT, 1000PEPEUSDT, PIPPINUSDT, OMUSDT...`
- **Minggu 33:** `LTCUSDT, PENGUUSDT, 1000PEPEUSDT, PIPPINUSDT, HYPEUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, LTCUSDT, 1000PEPEUSDT, PIPPINUSDT, HYPEUSDT...`
- **Minggu 35:** `JELLYJELLYUSDT, PENGUUSDT, LTCUSDT, PIPPINUSDT, HYPEUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, PENGUUSDT, LTCUSDT, 1000PEPEUSDT, PIPPINUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 12:37:23

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=False`, `use_volatility_or_logic=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000SHIBUSDT, WIFUSDT, AAVEUSDT, PIPPINUSDT, JELLYJELLYUSDT...`
- **Minggu 33:** `1000SHIBUSDT, AAVEUSDT, PIPPINUSDT, PENGUUSDT, HYPEUSDT...`
- **Minggu 34:** `1000SHIBUSDT, AAVEUSDT, PIPPINUSDT, JELLYJELLYUSDT, HYPEUSDT...`
- **Minggu 35:** `1000SHIBUSDT, XPLUSDT, PIPPINUSDT, JELLYJELLYUSDT, PENGUUSDT...`
- **Minggu 36:** `1000SHIBUSDT, XPLUSDT, WIFUSDT, PIPPINUSDT, JELLYJELLYUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 12:35:56

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=False`, `min_adx_level=18`, `use_di_filter=True`, `use_volatility_or_logic=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `ETCUSDT, NEARUSDT, ARBUSDT, 1000SHIBUSDT, FILUSDT...`
- **Minggu 33:** `ETCUSDT, NEARUSDT, 1000SHIBUSDT, DOTUSDT, PENGUUSDT...`
- **Minggu 34:** `ETCUSDT, NEARUSDT, ARBUSDT, 1000SHIBUSDT, FILUSDT...`
- **Minggu 35:** `XPLUSDT, CRVUSDT, ARBUSDT, 1000SHIBUSDT, PUMPUSDT...`
- **Minggu 36:** `ETCUSDT, XPLUSDT, NEARUSDT, ARBUSDT, 1000SHIBUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 12:30:17

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=True`, `min_adx_level=20`, `use_di_filter=True`, `use_volatility_or_logic=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `NEARUSDT, ETCUSDT, LUNA2USDT, UNIUSDT, ARBUSDT...`
- **Minggu 33:** `NEARUSDT, FARTCOINUSDT, ETCUSDT, UNIUSDT, PAXGUSDT...`
- **Minggu 34:** `NEARUSDT, ETCUSDT, UNIUSDT, PUMPUSDT, ARBUSDT...`
- **Minggu 35:** `UNIUSDT, LUNA2USDT, PUMPUSDT, ARBUSDT, PAXGUSDT...`
- **Minggu 36:** `NEARUSDT, FARTCOINUSDT, ETCUSDT, UNIUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 12:20:14

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=True`, `min_adx_level=20`, `use_di_filter=True`, `use_volatility_or_logic=True`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, PIPPINUSDT, LUNA2USDT, AAVEUSDT, TRUMPUSDT...`
- **Minggu 33:** `PIPPINUSDT, HYPEUSDT, AAVEUSDT, SUIUSDT, OMUSDT...`
- **Minggu 34:** `PIPPINUSDT, HYPEUSDT, AAVEUSDT, SUIUSDT, WLDUSDT...`
- **Minggu 35:** `PIPPINUSDT, LUNA2USDT, HYPEUSDT, TRUMPUSDT, OMUSDT...`
- **Minggu 36:** `WIFUSDT, PIPPINUSDT, LUNA2USDT, HYPEUSDT, TRUMPUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 12:13:11

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `use_htf_filter=True`, `min_adx_level=23`, `use_di_filter=True`, `bbw_is_expanding_window=5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `JELLYJELLYUSDT, AAVEUSDT, ETCUSDT, SUIUSDT, WIFUSDT...`
- **Minggu 33:** `DOTUSDT, AAVEUSDT, BCHUSDT, ETCUSDT, SUIUSDT...`
- **Minggu 34:** `JELLYJELLYUSDT, AAVEUSDT, BCHUSDT, ETCUSDT, SUIUSDT...`
- **Minggu 35:** `CRVUSDT, JELLYJELLYUSDT, DOTUSDT, BCHUSDT, PUMPUSDT...`
- **Minggu 36:** `JELLYJELLYUSDT, BCHUSDT, SOMIUSDT, ETCUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |
| `MomentumCrossHunter` | 0.2 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 11:52:26

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `adx_is_rising=True`, `bbw_percentile_min=0.1`, `bbw_percentile_max=0.6`, `sl_multiplier=1.9`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `UNIUSDT, TIAUSDT, SUIUSDT, AAVEUSDT, ARBUSDT...`
- **Minggu 33:** `UNIUSDT, TIAUSDT, BCHUSDT, SUIUSDT, HYPEUSDT...`
- **Minggu 34:** `PUMPUSDT, UNIUSDT, BCHUSDT, TIAUSDT, SUIUSDT...`
- **Minggu 35:** `PUMPUSDT, UNIUSDT, BCHUSDT, HYPEUSDT, CRVUSDT...`
- **Minggu 36:** `UNIUSDT, BCHUSDT, HYPEUSDT, ARBUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $1.37 | 25 | 40.00% |
| `MomentumCrossHunter` | 0.4 | $-44.62 | 75 | 33.33% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $31.75                     |
| **Net Profit**    | **$-43.25 (-57.67%)** |
| Total Trades      | 100                         |
| Win Rate          | 35.00%                     |
|  - Long Win Rate  | 53 trades (32.08%)              |
|  - Short Win Rate | 47 trades (38.30%)             |
| Profit Factor     | 0.54                       |
| Max Drawdown      | 63.10%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 21 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 11:50:58

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `TIAUSDT, WLDUSDT, FILUSDT, JELLYJELLYUSDT, LUNA2USDT...`
- **Minggu 33:** `TIAUSDT, WLDUSDT, HYPEUSDT, FARTCOINUSDT, PENGUUSDT...`
- **Minggu 34:** `TIAUSDT, WLDUSDT, FILUSDT, HYPEUSDT, JELLYJELLYUSDT...`
- **Minggu 35:** `WLDUSDT, HYPEUSDT, JELLYJELLYUSDT, LUNA2USDT, PENGUUSDT...`
- **Minggu 36:** `WLDUSDT, HYPEUSDT, FARTCOINUSDT, JELLYJELLYUSDT, LUNA2USDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $4.33 | 36 | 41.67% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $79.33                     |
| **Net Profit**    | **$4.33 (+5.78%)** |
| Total Trades      | 36                         |
| Win Rate          | 41.67%                     |
|  - Long Win Rate  | 3 trades (0.00%)              |
|  - Short Win Rate | 33 trades (45.45%)             |
| Profit Factor     | 1.10                       |
| Max Drawdown      | 16.57%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 10 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 11:49:09

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `adx_is_rising=True`, `bbw_percentile_min=0.1`, `bbw_percentile_max=0.6`, `sl_multiplier=1.9`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `SUIUSDT, TRUMPUSDT, UNIUSDT, NEARUSDT, ETCUSDT...`
- **Minggu 33:** `SUIUSDT, BCHUSDT, UNIUSDT, NEARUSDT, DOTUSDT...`
- **Minggu 34:** `SUIUSDT, BCHUSDT, UNIUSDT, NEARUSDT, ETCUSDT...`
- **Minggu 35:** `BCHUSDT, TRUMPUSDT, UNIUSDT, DOTUSDT, HYPEUSDT...`
- **Minggu 36:** `BCHUSDT, TRUMPUSDT, UNIUSDT, NEARUSDT, ETCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-10.31 | 9 | 22.22% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.5 | $-24.85 | 57 | 36.84% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $39.84                     |
| **Net Profit**    | **$-35.16 (-46.88%)** |
| Total Trades      | 66                         |
| Win Rate          | 34.85%                     |
|  - Long Win Rate  | 34 trades (20.59%)              |
|  - Short Win Rate | 32 trades (50.00%)             |
| Profit Factor     | 0.52                       |
| Max Drawdown      | 53.70%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 31 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 11:43:06

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-14 (~4 Bulan 13 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`
- **`MomentumCrossHunter`:** `risk_per_trade=0.012`, `adx_is_rising=True`, `bbw_percentile_min=0.1`, `bbw_percentile_max=0.6`, `sl_multiplier=1.9`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000PEPEUSDT, JELLYJELLYUSDT, FORMUSDT, SUIUSDT, NEARUSDT...`
- **Minggu 33:** `1000PEPEUSDT, LTCUSDT, NEARUSDT, UNIUSDT, DOTUSDT...`
- **Minggu 34:** `1000PEPEUSDT, LTCUSDT, JELLYJELLYUSDT, NEARUSDT, SUIUSDT...`
- **Minggu 35:** `LTCUSDT, CRVUSDT, JELLYJELLYUSDT, UNIUSDT, FORMUSDT...`
- **Minggu 36:** `1000PEPEUSDT, LTCUSDT, JELLYJELLYUSDT, NEARUSDT, SOMIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-10.15 | 11 | 9.09% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.5 | $-36.61 | 48 | 27.08% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $28.24                     |
| **Net Profit**    | **$-46.76 (-62.34%)** |
| Total Trades      | 59                         |
| Win Rate          | 23.73%                     |
|  - Long Win Rate  | 31 trades (16.13%)              |
|  - Short Win Rate | 28 trades (32.14%)             |
| Profit Factor     | 0.30                       |
| Max Drawdown      | 66.70%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 32 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 11:13:38

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-11-16 (~3 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `TIAUSDT, FILUSDT, 1000PEPEUSDT, ARBUSDT, PENGUUSDT...`
- **Minggu 33:** `TIAUSDT, FARTCOINUSDT, LTCUSDT, 1000PEPEUSDT, PENGUUSDT...`
- **Minggu 34:** `TIAUSDT, FILUSDT, PUMPUSDT, 1000PEPEUSDT, LTCUSDT...`
- **Minggu 35:** `PUMPUSDT, LTCUSDT, ARBUSDT, PENGUUSDT, CRVUSDT...`
- **Minggu 36:** `FARTCOINUSDT, 1000PEPEUSDT, LTCUSDT, ARBUSDT, PENGUUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $0.41 | 23 | 39.13% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.5 | $-13.75 | 16 | 31.25% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $61.66                     |
| **Net Profit**    | **$-13.34 (-17.79%)** |
| Total Trades      | 39                         |
| Win Rate          | 35.90%                     |
|  - Long Win Rate  | 6 trades (33.33%)              |
|  - Short Win Rate | 33 trades (36.36%)             |
| Profit Factor     | 0.74                       |
| Max Drawdown      | 36.01%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 16 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 11:06:24

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-04 s/d 2025-12-16 (~4 Bulan 15 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `WIFUSDT, TIAUSDT, SUIUSDT, WLDUSDT, ETCUSDT...`
- **Minggu 33:** `FARTCOINUSDT, PAXGUSDT, HYPEUSDT, TIAUSDT, DOTUSDT...`
- **Minggu 34:** `PAXGUSDT, HYPEUSDT, TIAUSDT, SUIUSDT, WLDUSDT...`
- **Minggu 35:** `PAXGUSDT, HYPEUSDT, DOTUSDT, WLDUSDT, LTCUSDT...`
- **Minggu 36:** `FARTCOINUSDT, HYPEUSDT, WIFUSDT, WLDUSDT, LTCUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $1.36 | 12 | 41.67% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.5 | $-25.02 | 388 | 42.78% |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $51.33                     |
| **Net Profit**    | **$-23.67 (-31.55%)** |
| Total Trades      | 400                         |
| Win Rate          | 42.75%                     |
|  - Long Win Rate  | 200 trades (40.00%)              |
|  - Short Win Rate | 200 trades (45.50%)             |
| Profit Factor     | 0.90                       |
| Max Drawdown      | 52.60%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 30 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-17 10:16:29

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-18 s/d 2025-12-16 (~4 Bulan 1 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=3.5`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000SHIBUSDT, UNIUSDT, 1000PEPEUSDT, OMUSDT, WIFUSDT...`
- **Minggu 33:** `DOTUSDT, 1000SHIBUSDT, 1000PEPEUSDT, BCHUSDT, OMUSDT...`
- **Minggu 34:** `1000SHIBUSDT, UNIUSDT, PUMPUSDT, 1000PEPEUSDT, BCHUSDT...`
- **Minggu 35:** `DOTUSDT, 1000SHIBUSDT, PUMPUSDT, XPLUSDT, BCHUSDT...`
- **Minggu 36:** `1000SHIBUSDT, XPLUSDT, 1000PEPEUSDT, BCHUSDT, WIFUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $32.01 | 45 | 48.89% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.5 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $107.01                     |
| **Net Profit**    | **$32.01 (+42.68%)** |
| Total Trades      | 45                         |
| Win Rate          | 48.89%                     |
|  - Long Win Rate  | 4 trades (50.00%)              |
|  - Short Win Rate | 41 trades (48.78%)             |
| Profit Factor     | 1.63                       |
| Max Drawdown      | 13.63%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 0 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-16 17:14:10

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=2.7`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `APTUSDT, TRUMPUSDT, 1000SHIBUSDT, FILUSDT, TRXUSDT...`
- **Minggu 33:** `LTCUSDT, 1000SHIBUSDT, PAXGUSDT, AAVEUSDT, ENAUSDT...`
- **Minggu 34:** `APTUSDT, 1000SHIBUSDT, PAXGUSDT, FILUSDT, AAVEUSDT...`
- **Minggu 35:** `LTCUSDT, PUMPUSDT, CRVUSDT, APTUSDT, TRUMPUSDT...`
- **Minggu 36:** `APTUSDT, TRUMPUSDT, 1000SHIBUSDT, ENAUSDT, BCHUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-11.94 | 31 | 32.26% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |
| `MomentumCrossHunter` | 0.5 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $63.06                     |
| **Net Profit**    | **$-11.94 (-15.92%)** |
| Total Trades      | 31                         |
| Win Rate          | 32.26%                     |
|  - Long Win Rate  | 4 trades (25.00%)              |
|  - Short Win Rate | 27 trades (33.33%)             |
| Profit Factor     | 0.71                       |
| Max Drawdown      | 26.21%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 14 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-16 16:24:18

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-12-16 (~4 Bulan 8 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=2.7`, `candle_body_ratio=0.58`, `anti_chase_pct=0.08`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `TRUMPUSDT, 1000SHIBUSDT, JELLYJELLYUSDT, HBARUSDT, PIPPINUSDT...`
- **Minggu 33:** `1000SHIBUSDT, PIPPINUSDT, LTCUSDT, OPUSDT, PAXGUSDT...`
- **Minggu 34:** `1000SHIBUSDT, HBARUSDT, PIPPINUSDT, OPUSDT, PAXGUSDT...`
- **Minggu 35:** `TRUMPUSDT, 1000SHIBUSDT, JELLYJELLYUSDT, CRVUSDT, PIPPINUSDT...`
- **Minggu 36:** `TRUMPUSDT, 1000SHIBUSDT, JELLYJELLYUSDT, HBARUSDT, SOMIUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-13.04 | 32 | 31.25% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $61.96                     |
| **Net Profit**    | **$-13.04 (-17.39%)** |
| Total Trades      | 32                         |
| Win Rate          | 31.25%                     |
|  - Long Win Rate  | 5 trades (20.00%)              |
|  - Short Win Rate | 27 trades (33.33%)             |
| Profit Factor     | 0.69                       |
| Max Drawdown      | 26.26%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 14 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-16 15:02:15

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-09-28 s/d 2025-12-16 (~2 Bulan 20 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=2.7`, `candle_body_ratio=0.4`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `1000PEPEUSDT, SUIUSDT`
- **Minggu 33:** `1000PEPEUSDT, SUIUSDT`
- **Minggu 34:** `1000PEPEUSDT, SUIUSDT`
- **Minggu 35:** `1000PEPEUSDT, SUIUSDT`
- **Minggu 36:** `1000PEPEUSDT, SUIUSDT`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $3.24 | 8 | 62.50% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $78.24                     |
| **Net Profit**    | **$3.24 (+4.32%)** |
| Total Trades      | 8                         |
| Win Rate          | 62.50%                     |
|  - Long Win Rate  | 0 trades (0.00%)              |
|  - Short Win Rate | 8 trades (62.50%)             |
| Profit Factor     | 1.25                       |
| Max Drawdown      | 13.52%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 7 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


---

## Backtest: 2025-12-10 13:00:04

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** 2025-08-11 s/d 2025-11-18 (~3 Bulan 10 Hari)
-   **Mode Exit:** Dinamis (Advanced)

**Parameter Filter Aktif:**
- **`AltcoinVolumeBreakoutHunter`:** `risk_per_trade=0.025`, `breakout_window=12`, `volume_spike_multiplier=2.7`, `candle_body_ratio=0.4`, `anti_chase_pct=0.05`
- **`LongOnlyCorrectionHunter`:** `risk_per_trade=0.009`, `volume_spike_multiplier=1.8`, `sl_multiplier=2.2`, `bb_period=20`, `bb_std_dev=1.5`

**Contoh Rotasi Whitelist Mingguan:**

- **Minggu 32:** `XLMUSDT, WLDUSDT, NEARUSDT, 1000BONKUSDT, UNIUSDT...`
- **Minggu 33:** `PIPPINUSDT, NEARUSDT, 1000BONKUSDT, AAVEUSDT, HYPEUSDT...`
- **Minggu 34:** `XLMUSDT, PIPPINUSDT, WLDUSDT, 1000BONKUSDT, NEARUSDT...`
- **Minggu 35:** `XLMUSDT, WLDUSDT, 1000BONKUSDT, UNIUSDT, APTUSDT...`
- **Minggu 36:** `XLMUSDT, PIPPINUSDT, WLDUSDT, NEARUSDT, 1000BONKUSDT...`
- ... (dan seterusnya)

**Konfigurasi & Performa Strategi:**

| Nama Strategi                | Bobot | Total PnL (USD) | Trades | Win Rate |
| ---------------------------- | ----- | --------------- | ------ | -------- |
| `AltcoinVolumeBreakoutHunter` | 0.6 | $-21.93 | 26 | 34.62% |
| `LongOnlyCorrectionHunter` | 0.4 | $0.00 | 0 | N/A |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $75.00                     |
| Saldo Akhir       | $53.07                     |
| **Net Profit**    | **$-21.93 (-29.24%)** |
| Total Trades      | 26                         |
| Win Rate          | 34.62%                     |
|  - Long Win Rate  | 1 trades (0.00%)              |
|  - Short Win Rate | 25 trades (36.00%)             |
| Profit Factor     | 0.47                       |
| Max Drawdown      | 35.22%                      |
| CB Triggers       | 1                         |
| Weekly Killswitch | 15 Triggers                     |

**Catatan & Observasi:**
-   (Isi observasi Anda di sini)


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
