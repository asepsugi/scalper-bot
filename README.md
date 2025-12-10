# Binance Futures Multi-Strategy Scalping Bot

Proyek ini adalah bot scalping algoritmik canggih untuk Binance Futures, dirancang dengan arsitektur tiga pilar untuk profitabilitas jangka panjang: **(1) Sinyal Konsensus Multi-Strategi**, **(2) Seleksi Aset Dinamis**, dan **(3) Manajemen Risiko Berlapis**. Dibangun dengan `asyncio` dan `ccxt.pro`, bot ini mampu memantau dan mengeksekusi perdagangan di puluhan simbol secara bersamaan dengan performa tinggi.

## ✨ Key Features

### Pilar 1: Mesin Sinyal & Eksekusi

-   **Konsensus Multi-Strategi**: Menggabungkan sinyal dari berbagai strategi (`strategies.py`) dengan sistem skor berbobot untuk menghasilkan sinyal berkualitas tinggi.
-   **Profil Entri Dinamis**: Secara otomatis memilih mode eksekusi (`CONTINUATION` atau `PULLBACK`) berdasarkan kondisi pasar, menyesuaikan jenis order (limit/market) dan risiko.
-   **Logika Exit Canggih**:
    -   **Partial Take Profits**: Mengamankan keuntungan di beberapa level Risk/Reward (RR).
    -   **Trailing Stop Loss**: Mengunci keuntungan secara dinamis saat harga bergerak sesuai arah.
    -   **Exit Berbasis Candle**: Menggunakan penutupan candle untuk eksekusi SL/TP, mengurangi dampak *stop-loss hunting*.

### Pilar 2: Seleksi Aset Dinamis

-   **Rotasi Whitelist Mingguan**: Secara otomatis memindai ratusan koin setiap minggu untuk memilih 20 koin "paling panas" berdasarkan skor momentum (volume & kenaikan harga), memastikan bot selalu berdagang di aset yang relevan.
-   **Filter Market Regime**: Strategi dapat dilengkapi dengan filter untuk hanya aktif dalam kondisi pasar tertentu (misalnya, tren kuat vs. *ranging*), menghindari *choppy market*.

### Pilar 3: Manajemen Risiko Berlapis

-   **Drawdown Circuit Breaker**: Secara otomatis menghentikan semua aktivitas trading jika drawdown akun melebihi ambang batas (misal, 10%), dengan periode *cooldown* yang meningkat pada pemicu berikutnya.
-   **Killswitch Kinerja Mingguan**: Menghentikan bot selama 72 jam jika kerugian dalam seminggu mencapai batas yang ditentukan (misal, -8%), mencegah kerugian besar.
-   **Skala Posisi Otomatis**: Mengurangi ukuran posisi setelah 2 kekalahan beruntun dan meningkatkannya (hingga 1.5x) setelah 3 kemenangan beruntun.
-   **Manajemen Risiko Per Trade**: Ukuran posisi dihitung secara presisi berdasarkan persentase risiko yang ditetapkan per trade, jarak stop-loss, dan total ekuitas akun.

### Alat Pendukung & Lainnya

-   **Backtester Portofolio Realistis**: `backtest_market_scanner.py` mensimulasikan perdagangan di banyak simbol secara kronologis, lengkap dengan simulasi rotasi *whitelist* dan ranking volume historis untuk hasil yang akurat.
-   **Skrip Diagnostik**: `diagnostic.py` membantu menganalisis mengapa sinyal tidak muncul, memeriksa kualitas data, dan mengevaluasi ambang batas konsensus.
-   **Arsitektur Asinkron**: Dibangun dengan `asyncio` untuk performa tinggi, memantau puluhan simbol secara bersamaan tanpa *blocking*.
-   **Notifikasi Telegram**: Peringatan instan untuk status bot, order, eksekusi, dan error kritis.

## 💡 Menambahkan Strategi Baru

Bot ini dirancang secara modular, memudahkan penambahan strategi trading kustom Anda.

1.  **Buka `strategies.py`**: File ini berisi semua logika trading.

2.  **Buat Fungsi Strategi Anda**: Buat fungsi Python baru yang menerima DataFrame (`df`) dan `symbol` (opsional). Fungsi ini harus mengembalikan tiga item: `long_signals`, `short_signals`, dan `exit_params`.

    ```python
    # Contoh strategi baru yang dapat dikonfigurasi di strategies.py
    def signal_version_MyNewStrategy(df, symbol: str = None):
        # Baca parameter dari config.py
        params = CONFIG.get("strategy_params", {}).get("MyNewStrategy", {})
        
        # Ambil nilai dari config atau gunakan default
        rsi_oversold = params.get("rsi_oversold", 30)
        ema_period = params.get("ema_period", 200)
        
        # Logika sinyal
        long_condition = (df[f"RSI_{CONFIG['rsi_period']}"] < rsi_oversold) & (df['close'] > df[f"EMA_{ema_period}"])
        short_condition = pd.Series(False, index=df.index) # Strategi ini long-only
        
        # Parameter exit
        exit_params = {
            'sl_multiplier': params.get("sl_multiplier", 2.0),
            'rr_ratio': params.get("rr_ratio", 1.5),
            'partial_tps': [(2.0, 0.50)], # Jual 50% di 2R
            'trailing': {"enabled": True, "trigger_rr": 1.5, "distance_atr": 2.5}
        }
        return long_condition, short_condition, exit_params
    ```

3.  **Daftarkan Strategi Anda**: Di bagian bawah `strategies.py`, tambahkan strategi baru Anda ke kamus `STRATEGY_CONFIG`. Beri nama unik, arahkan ke fungsi yang baru dibuat, dan berikan `weight` (bobot).

    ```python
    # Tambahkan strategi Anda ke kamus di strategies.py
    "MyNewStrategy": {
        "function": signal_version_MyNewStrategy,
        "weight": 0.5 # Beri bobot sesuai kepercayaan Anda pada strategi ini
    }
    ```

4.  **(Opsional) Tambah Parameter & Indikator**:
    -   Tambahkan blok konfigurasi untuk strategi baru Anda di `config.py` di bawah `strategy_params`.
    -   Jika strategi Anda memerlukan indikator baru, tambahkan perhitungannya di `indicators.py`.

## 📂 Project Structure

```
.
├── cache/                # Menyimpan cache data pasar historis
├── output/               # Menyimpan log, state posisi, dan hasil backtest
├── utils/                # Fungsi utilitas (manajemen risiko, persiapan data)
├── .env                  # (Anda buat) Menyimpan API key dan token secara aman
├── .env.example          # Template untuk file .env
├── .gitignore            # File yang diabaikan oleh Git
├── backtest_market_scanner.py # Backtester portofolio multi-simbol
├── backtest_strategy_comparation.py # Backtester untuk membandingkan strategi
├── config.py             # Konfigurasi utama untuk parameter bot dan strategi
├── diagnostic.py         # Skrip untuk mendiagnosis masalah sinyal dan data
├── demo_trader.py        # Skrip utama untuk menjalankan bot di Testnet
├── indicators.py         # Fungsi untuk menghitung indikator teknis
├── live_trader.py        # Skrip utama untuk menjalankan bot di lingkungan LIVE
├── live_trader_monitor.py # Dashboard terminal real-time
├── requirements.txt      # Daftar library Python yang dibutuhkan
└── strategies.py         # Semua logika strategi trading didefinisikan di sini
```

## 🚀 Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a Virtual Environment**
    Sangat disarankan untuk menggunakan virtual environment.
    ```bash
    python -m venv venv
    ```
    Aktifkan:
    -   **Windows**: `.\venv\Scripts\activate`
    -   **macOS/Linux**: `source venv/bin/activate`

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Credentials**
    Salin file contoh `.env` dan isi detail Anda.
    ```bash
    cp .env.example .env
    ```
    Edit file `.env` dengan API key Binance (live & testnet) dan token/chat ID Telegram Anda.

## ⚙️ Usage

Pastikan virtual environment Anda aktif sebelum menjalankan skrip apa pun.

### Menjalankan Trading Bots

-   **Run the LIVE Trader:**
    ```bash
    python live_trader.py
    ```

-   **Run the DEMO Trader:**
    ```bash
    python demo_trader.py
    ```

### Menjalankan Monitor

Jalankan monitor di terminal terpisah untuk memantau aktivitas bot.

-   **Monitor the LIVE Environment:**
    ```bash
    python live_trader_monitor.py --env live
    ```

-   **Monitor the DEMO Environment:**
    ```bash
    python live_trader_monitor.py --env demo
    ```

### Menjalankan Backtesters & Diagnostics

-   **Market Scanner (`backtest_market_scanner.py`)**:
    Jalankan simulasi portofolio di banyak simbol untuk mengevaluasi performa gabungan strategi.
    ```bash
    # Jalankan backtest pada 50 simbol teratas untuk periode Q4 2025
    # Gunakan --historical-ranking untuk hasil yang lebih realistis
    python backtest_market_scanner.py --start_date 2025-10-01 --end_date 2025-12-31 --max_symbols 50 --historical-ranking
    ```

-   **Diagnostic Tool (`diagnostic.py`)**:
    Gunakan skrip ini jika backtester Anda tidak menghasilkan sinyal.
    ```bash
    python diagnostic.py --symbols 5 --start_date 2025-10-01
    ```

-   **Strategy Comparer (`backtest_strategy_comparation.py`)**:
    Uji setiap strategi secara individual pada portofolio simbol.
    ```bash
    python backtest_strategy_comparation.py --max_symbols 20 --limit 2500
    ```

## 🔧 Configuration

Sebagian besar perilaku bot dapat diatur di `config.py`.

-   `strategy_params`: Atur parameter untuk setiap strategi secara individual.
-   `LIVE_TRADING_CONFIG`: Konfigurasi parameter global untuk bot live, seperti batas rugi harian, *circuit breaker*, dan rasio konsensus.
-   `WHITELIST_ROTATION_CONFIG`: Atur interval dan kriteria untuk rotasi *whitelist* mingguan.
-   `EXECUTION`: Konfigurasi logika eksekusi, termasuk TP parsial dan *trailing stop*.
-   `LEVERAGE_MAP`: Tentukan leverage kustom untuk simbol tertentu.

