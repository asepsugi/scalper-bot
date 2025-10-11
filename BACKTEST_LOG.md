# Log Hasil Backtest Konfigurasi Strategi

Dokumen ini digunakan untuk mencatat hasil dari berbagai backtest yang dijalankan menggunakan `backtest_market_scanner.py`, terutama saat menguji kombinasi strategi yang berbeda dari `strategies.py`.

---

## Backtest: 2024-05-21

**Parameter:**
-   **Simbol:** Top 50 (berdasarkan volume)
-   **Candles:** 2500
-   **Periode:** ~8.5 hari (2500 * 5 menit)

**Konfigurasi Strategi (`STRATEGY_CONFIG`):**

| Nama Strategi                | Fungsi                 | Bobot (Weight) | Status   |
| ---------------------------- | ---------------------- | -------------- | -------- |
| `AdaptiveTrendRide(A3)`      | `signal_version_A3`    | 1.0            | ✅ Aktif |
| `ReversalMomentumRider(A4R)` | `signal_version_A4R`   | 1.0            | ✅ Aktif |
| `VolatilityScalper(B1)`      | `signal_version_B1`    | 0.8            | ❌ Nonaktif |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $50.00                     |
| Saldo Akhir       | $55.78                     |
| **Net Profit**    | **+$5.78 (+11.56%)**       |
| Total Trades      | 45                         |
| Win Rate          | 55.56%                     |
| Profit Factor     | 1.89                       |
| Max Drawdown      | 4.21%                      |

**Catatan & Observasi:**
-   Kombinasi A3 dan A4R menunjukkan performa yang cukup stabil.
-   Profit Factor di atas 1.5, pertanda baik.
-   Perlu diuji pada periode pasar yang berbeda (misal, saat sideways).

---

## Backtest: 2024-05-20

**Parameter:**
-   **Simbol:** Top 20 (berdasarkan volume)
-   **Candles:** 1500
-   **Periode:** ~5.2 hari (1500 * 5 menit)

**Konfigurasi Strategi (`STRATEGY_CONFIG`):**

| Nama Strategi                | Fungsi                 | Bobot (Weight) | Status   |
| ---------------------------- | ---------------------- | -------------- | -------- |
| `AdaptiveTrendRide(A3)`      | `signal_version_A3`    | 1.0            | ✅ Aktif |
| `ReversalMomentumRider(A4R)` | `signal_version_A4R`   | 1.0            | ❌ Nonaktif |
| `VolatilityScalper(B1)`      | `signal_version_B1`    | 1.2            | ✅ Aktif |

**Hasil Ringkas:**

| Metrik            | Nilai                      |
| ----------------- | -------------------------- |
| Saldo Awal        | $50.00                     |
| Saldo Akhir       | $48.12                     |
| **Net Profit**    | **-$1.88 (-3.76%)**        |
| Total Trades      | 32                         |
| Win Rate          | 41.18%                     |
| Profit Factor     | 0.85                       |
| Max Drawdown      | 9.80%                      |

**Catatan & Observasi:**
-   Kombinasi A3 dan B1 tampaknya kurang cocok. Profit Factor di bawah 1 menunjukkan strategi ini merugi secara keseluruhan dalam kondisi pasar saat ini.
-   Drawdown cukup tinggi. Mungkin bobot untuk B1 terlalu agresif.

---