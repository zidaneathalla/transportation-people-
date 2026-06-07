"""
Executive Summary - Ringkasan umum Transport BI System
"""
from pathlib import Path
import sys
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

st.set_page_config(page_title="Executive Summary", layout="wide")

# Load CSS
css_path = ROOT_DIR / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="topbar">
        <div>
            <div class="eyebrow">Executive Summary</div>
            <h1>Transport BI System Overview</h1>
            <p>Platform Business Intelligence untuk optimalisasi armada transportasi publik dan peningkatan efisiensi operasional.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
### Informasi Penting

Halaman ini adalah overview dari Transport BI System. Untuk menggunakan aplikasi, silakan:
""")

# Quick Links
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="quick-link-card">
        <h4>Main Dashboard</h4>
        <p>Akses dashboard utama dengan analytics lengkap dan recommendations.</p>
        <ul>
            <li>Pilih <strong>app.py</strong> atau jalankan:</li>
        </ul>
        <span class="command-pill">streamlit run transport_bi_system/app.py</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="quick-link-card">
        <h4>Advanced Analytics</h4>
        <p>Halaman analitik mendalam dengan visualisasi detail.</p>
        <ul>
            <li>Pilih tab <strong>Analytics</strong> di sidebar</li>
            <li>Lihat trend, performa rute, dan analisis operasional</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="quick-link-card">
        <h4>Settings & Docs</h4>
        <p>Konfigurasi sistem dan dokumentasi lengkap.</p>
        <ul>
            <li>Pilih tab <strong>Settings</strong> di sidebar</li>
            <li>Baca panduan penggunaan dan API documentation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# System Overview
st.markdown("""
### Tujuan Sistem

Transport BI System dirancang untuk:
1. **Analisis Data Real-time** - Monitoring demand penumpang dan performa rute
2. **Prediksi Penumpang** - Machine Learning untuk forecasting demand
3. **Optimalisasi Armada** - Rekomendasi fleet allocation berdasarkan demand
4. **Efisiensi Biaya** - Tracking cost per passenger dan optimalisasi rute
5. **Decision Support** - Dashboard interaktif untuk decision making

### Key Features

| Fitur | Deskripsi |
|-------|-----------|
| **Interactive Dashboard** | Real-time monitoring dengan visualisasi interaktif |
| **ML Predictions** | Prediksi penumpang menggunakan Random Forest / Linear Regression |
| **Smart Recommendations** | Rekomendasi armada optimal berdasarkan prediksi |
| **Cost Analysis** | Tracking biaya operasional dan efisiensi per rute |
| **Data Export** | Export laporan ke Excel untuk presentasi |
| **Multi-Algorithm Support** | Pilih algoritma ML yang sesuai kebutuhan |

### Workflow Aplikasi
""")

st.markdown("""
<div class="workflow-grid">
    <div class="workflow-step">
        <span>01</span>
        <strong>Upload Dataset</strong>
        <p>Masukkan file CSV atau Parquet sebagai sumber data operasional.</p>
    </div>
    <div class="workflow-step">
        <span>02</span>
        <strong>Validasi Data</strong>
        <p>Sistem memeriksa kelengkapan kolom dan kualitas dataset.</p>
    </div>
    <div class="workflow-step">
        <span>03</span>
        <strong>Preprocessing</strong>
        <p>Data dibersihkan, dinormalisasi, dan diperkaya dengan fitur analitik.</p>
    </div>
    <div class="workflow-step">
        <span>04</span>
        <strong>Train ML Model</strong>
        <p>Model dilatih untuk membaca pola demand dan performa rute.</p>
    </div>
    <div class="workflow-step">
        <span>05</span>
        <strong>Generate Predictions</strong>
        <p>Prediksi penumpang dibuat untuk mendukung keputusan operasional.</p>
    </div>
    <div class="workflow-step">
        <span>06</span>
        <strong>Fleet Recommendations</strong>
        <p>Sistem menghitung kebutuhan armada berdasarkan demand dan kapasitas.</p>
    </div>
    <div class="workflow-step">
        <span>07</span>
        <strong>Visualize & Analyze</strong>
        <p>Insight ditampilkan lewat KPI, grafik, tabel, dan prioritas rute.</p>
    </div>
    <div class="workflow-step">
        <span>08</span>
        <strong>Export Reports</strong>
        <p>Laporan dapat diekspor untuk evaluasi dan presentasi harian.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### Security & Access

- **Authentication** - Username & password admin (default: admin/admin123)
- **Data Privacy** - Semua data tersimpan lokal
- **Session Management** - Auto-logout untuk keamanan

### Tech Stack

- **Frontend**: Streamlit 1.35.0
- **Data Processing**: Pandas 2.2.2, PySpark 3.5.1
- **ML Framework**: Scikit-learn 1.5.0
- **Visualization**: Plotly 5.22.0
- **Language**: Python 3.10+

---

**Catatan:** Halaman `pages/` hanya untuk informasi. Main entry point adalah `transport_bi_system/app.py`
""")
