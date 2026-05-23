# Sistem Rekomendasi Peluncuran Armada Transportasi Harian

Project Business Intelligence dan Big Data berbasis Python untuk menganalisis data historis transportasi umum, memprediksi jumlah penumpang, dan memberikan rekomendasi jumlah armada harian.

Dataset utama:
https://www.kaggle.com/datasets/ifuurh/public-transportation-passenger-counts

## Tech Stack

- Python 3
- Streamlit
- Pandas
- PySpark
- Scikit-learn
- Plotly
- Matplotlib

## Struktur Project

```text
transport_bi_system/
├── app.py
├── requirements.txt
├── README.md
├── .env
├── config/
│   └── settings.py
├── data/
│   ├── raw/
│   └── processed/
├── database/
│   └── schema.sql
├── models/
├── services/
│   ├── analytics_service.py
│   ├── data_validator.py
│   ├── feature_engineering.py
│   ├── ml_service.py
│   ├── preprocessing_service.py
│   ├── recommendation_service.py
│   └── report_service.py
├── utils/
│   ├── helpers.py
│   └── logger.py
├── pages/
├── assets/
│   └── styles.css
├── notebooks/
├── logs/
└── reports/
```

## Business Objective

Sistem ini membantu operator transportasi untuk:

- Mengetahui pola jumlah penumpang.
- Menganalisis rute terpadat.
- Mendeteksi jam sibuk.
- Memprediksi jumlah penumpang.
- Merekomendasikan jumlah armada yang perlu diluncurkan setiap hari.

## Kolom Dataset

Dataset CSV atau Parquet divalidasi agar memiliki kolom berikut:

```text
operating_day, line_id, stop_id, arrival, departure, vehicle_seats, passengers
```

Validator juga menerima beberapa alias umum seperti `route_id`, `capacity`, `passenger_count`, dan `date`.

## Business Dataset

Setelah preprocessing dan feature engineering, data diperkaya menjadi:

- `hari`
- `jenis_hari`
- `jam`
- `jam_kategori`
- `occupancy_rate`
- `prioritas_rute`
- `cuaca`
- `biaya_operasional`
- `is_peak_hour`
- `prediksi_penumpang`

Rumus:

```text
Occupancy Rate = jumlah_penumpang / kapasitas_armada * 100
Jumlah Armada = ceil(prediksi_penumpang / kapasitas_armada)
```

## Pipeline

1. Upload CSV atau Parquet dari dashboard.
2. Standardisasi nama kolom.
3. Validasi kolom wajib.
4. Data cleaning dengan Pandas atau PySpark.
5. Feature engineering.
6. Training model Random Forest Regression atau Linear Regression.
7. Prediksi jumlah penumpang.
8. Rekomendasi jumlah armada.
9. Dashboard BI dan export laporan Excel.

## Setup Guide

1. Masuk ke folder project:

```bash
cd transport_bi_system
```

2. Buat virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependency:

```bash
pip install -r requirements.txt
```

4. Jalankan dashboard:

```bash
streamlit run app.py
```

5. Login admin default:

```text
username: admin
password: admin123
```

Ubah kredensial di file `.env` sebelum demo produksi.

## Cara Menggunakan Dataset Kaggle

1. Download dataset dari halaman Kaggle.
2. Ekstrak file CSV atau siapkan file Parquet.
3. Jalankan aplikasi Streamlit.
4. Upload CSV atau Parquet melalui sidebar.
5. Pastikan panel validasi menyatakan dataset valid.
6. Buka tab Dashboard BI, Prediksi, dan Export Laporan.

Jika belum memiliki dataset, aktifkan toggle `Gunakan sample data demo` untuk simulasi presentasi.

## Fitur Dashboard

- Login admin.
- Upload dataset CSV atau Parquet.
- Validasi dataset.
- KPI cards.
- Total penumpang.
- Total rute.
- Occupancy rate.
- Top rute terpadat.
- Analisis jam sibuk.
- Tren penumpang harian.
- Prediksi jumlah penumpang.
- Tabel rekomendasi armada.
- Klasifikasi prioritas rute.
- Grafik biaya operasional.
- Export laporan Excel.
- Ringkasan rekomendasi harian.

## Contoh Visualisasi Dashboard

Dashboard menampilkan:

- Line chart tren penumpang harian.
- Bar chart distribusi jam sibuk.
- Horizontal bar chart top rute terpadat.
- Bar chart biaya operasional per rute.
- Donut chart komposisi armada berdasarkan prioritas.
- Tabel rekomendasi armada harian.

## Contoh Laporan Rekomendasi Harian

```text
Ringkasan rekomendasi harian:
- Total armada direkomendasikan: 128
- Estimasi biaya operasional: Rp 96.000.000
- Rute prioritas utama:
  MRT-01 | Pagi Sibuk | 8 armada | Tinggi
  BRT-01 | Sore Sibuk | 7 armada | Tinggi
  LRT-02 | Pagi Sibuk | 5 armada | Sedang
```

## SQL Schema

Skema database tersedia di:

```text
database/schema.sql
```

Tabel utama:

- `routes`
- `stops`
- `passenger_counts`
- `bi_transport_daily`
- `fleet_recommendations`

## Catatan Production Ready

- Konfigurasi environment berada di `.env`.
- Logging tersimpan di folder `logs/`.
- Model tersimpan di folder `models/`.
- Dataset hasil transformasi tersimpan di `data/processed/`.
- Laporan Excel tersimpan di `reports/`.
- Logika bisnis dipisahkan ke folder `services/` agar mudah diuji dan dikembangkan.
