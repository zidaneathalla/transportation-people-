"""
📋 Executive Summary - Ringkasan umum Transport BI System
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
            <div class="eyebrow">📋 Executive Summary</div>
            <h1>Transport BI System Overview</h1>
            <p>Platform Business Intelligence untuk optimalisasi armada transportasi publik dan peningkatan efisiensi operasional.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
### ℹ️ Informasi Penting

Halaman ini adalah overview dari Transport BI System. Untuk menggunakan aplikasi, silakan:
""")

# Quick Links
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🚀 Main Dashboard
    Akses dashboard utama dengan analytics lengkap dan recommendations.
    
    - Pilih **"app.py"** atau jalankan:
    ```bash
    streamlit run transport_bi_system/app.py
    ```
    """)

with col2:
    st.markdown("""
    #### 📊 Advanced Analytics
    Halaman analitik mendalam dengan visualisasi detail.
    
    - Pilih tab **"Analytics"** di sidebar
    - Lihat trend, performa rute, dan analisis operasional
    """)

with col3:
    st.markdown("""
    #### ⚙️ Settings & Docs
    Konfigurasi sistem dan dokumentasi lengkap.
    
    - Pilih tab **"Settings"** di sidebar
    - Baca panduan penggunaan dan API documentation
    """)

st.divider()

# System Overview
st.markdown("""
### 🎯 Tujuan Sistem

Transport BI System dirancang untuk:
1. **Analisis Data Real-time** - Monitoring demand penumpang dan performa rute
2. **Prediksi Penumpang** - Machine Learning untuk forecasting demand
3. **Optimalisasi Armada** - Rekomendasi fleet allocation berdasarkan demand
4. **Efisiensi Biaya** - Tracking cost per passenger dan optimalisasi rute
5. **Decision Support** - Dashboard interaktif untuk decision making

### 💡 Key Features

| Fitur | Deskripsi |
|-------|-----------|
| **Interactive Dashboard** | Real-time monitoring dengan visualisasi interaktif |
| **ML Predictions** | Prediksi penumpang menggunakan Random Forest / Linear Regression |
| **Smart Recommendations** | Rekomendasi armada optimal berdasarkan prediksi |
| **Cost Analysis** | Tracking biaya operasional dan efisiensi per rute |
| **Data Export** | Export laporan ke Excel untuk presentasi |
| **Multi-Algorithm Support** | Pilih algoritma ML yang sesuai kebutuhan |

### 📈 Workflow Aplikasi

```
1. Upload Dataset (CSV/Parquet)
   ↓
2. Validasi Data
   ↓
3. Preprocessing & Feature Engineering
   ↓
4. Train ML Model
   ↓
5. Generate Predictions
   ↓
6. Build Fleet Recommendations
   ↓
7. Visualize & Analyze
   ↓
8. Export Reports
```

### 🔒 Security & Access

- **Authentication** - Username & password admin (default: admin/admin123)
- **Data Privacy** - Semua data tersimpan lokal
- **Session Management** - Auto-logout untuk keamanan

### 🛠️ Tech Stack

- **Frontend**: Streamlit 1.35.0
- **Data Processing**: Pandas 2.2.2, PySpark 3.5.1
- **ML Framework**: Scikit-learn 1.5.0
- **Visualization**: Plotly 5.22.0
- **Language**: Python 3.10+

---

**📌 Catatan:** Halaman `pages/` hanya untuk informasi. Main entry point adalah `transport_bi_system/app.py`
""")
