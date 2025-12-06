
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
- **`LiquiditySweepReversal`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`

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
| `MemecoinMoonshotHunter` | 0.3 | $0.00 | 0 | N/A |
| `LiquiditySweepReversal` | 0.3 | $4.51 | 171 | 45.61% |

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
- **`LiquiditySweepReversal`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=2.5`, `sl_multiplier=2.2`, `rsi_divergence_window=8`

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
| `MemecoinMoonshotHunter` | 0.3 | $0.00 | 0 | N/A |
| `LiquiditySweepReversal` | 0.3 | $3.01 | 134 | 45.52% |

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
- **`LiquiditySweepReversal`:** `risk_per_trade=0.009`, `risk_per_trade=0.009`, `volume_spike_multiplier=3.0`, `sl_multiplier=2.2`, `rsi_divergence_window=5`

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
| `MemecoinMoonshotHunter` | 0.3 | $0.00 | 0 | N/A |
| `LiquiditySweepReversal` | 0.3 | $0.00 | 0 | N/A |

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
