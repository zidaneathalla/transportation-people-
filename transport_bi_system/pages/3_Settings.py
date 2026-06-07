"""
⚙️ Settings & Documentation Page
"""
import streamlit as st
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config.settings import settings

st.set_page_config(page_title="Settings", layout="wide")

# Load CSS
css_path = ROOT_DIR / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("""
    <div class="topbar">
        <div>
            <div class="eyebrow">⚙️ System Settings</div>
            <h1>Configuration & Documentation</h1>
            <p>Pengaturan aplikasi, dokumentasi teknis, dan panduan penggunaan Transport BI System.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔧 Configuration", "📖 Documentation", "ℹ️ About"])

with tab1:
    st.markdown('<div class="section-title"><h2>Konfigurasi Aplikasi</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card"><span>App Name</span><h3>Transport BI</h3><p>Sistem operasional armada</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><span>Version</span><h3>1.0.0</h3><p>Alpha Release</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><span>Database</span><h3>CSV</h3><p>Local file storage</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><span>ML Engine</span><h3>Scikit-learn</h3><p>Random Forest & Linear Regression</p></div>', unsafe_allow_html=True)
    
    with st.expander("🔐 API Configuration", expanded=False):
        st.write("""
        ### API Endpoints
        - **Analytics**: `/api/analytics/*`
        - **Recommendations**: `/api/recommendations/*`
        - **Predictions**: `/api/predictions/*`
        """)
    
    with st.expander("📊 Data Pipeline", expanded=False):
        st.markdown("""
        ### Processing Steps
        1. **Data Validation** - Memastikan kolom wajib lengkap
        2. **Preprocessing** - Cleaning & normalisasi data
        3. **Feature Engineering** - Transformasi fitur tambahan
        4. **Model Training** - Latih ML model
        5. **Prediction** - Generate prediksi penumpang
        6. **Recommendation** - Kalkulasi rekomendasi armada
        """)

with tab2:
    st.markdown('<div class="section-title"><h2>Panduan Penggunaan</h2></div>', unsafe_allow_html=True)
    
    with st.expander("🚀 Getting Started", expanded=True):
        st.markdown("""
        ### Langkah Awal
        1. **Login** - Masukkan username & password admin
        2. **Upload Data** - Upload file CSV atau Parquet dari sidebar
        3. **Validasi** - Sistem otomatis validasi dataset
        4. **Proses** - Klik tombol untuk memproses data
        5. **Analisis** - Lihat hasil di dashboard
        
        ### Format Data Wajib
        - `operating_day`: Tanggal operasional (YYYY-MM-DD)
        - `line_id`: ID rute transportasi
        - `stop_id`: ID halte
        - `arrival`: Waktu kedatangan
        - `departure`: Waktu keberangkatan
        - `vehicle_seats`: Kapasitas kendaraan
        - `passengers`: Jumlah penumpang aktual
        """)
    
    with st.expander("📈 Dashboard BI", expanded=False):
        st.markdown("""
        ### Fitur Dashboard
        - **KPI Cards** - Ringkasan metrik utama
        - **Tren Charts** - Visualisasi trend penumpang
        - **Route Analysis** - Analisis performa rute
        - **Recommendations** - Saran armada optimal
        - **Priority Classification** - Klasifikasi prioritas rute
        
        ### Interpretasi Metrik
        - **Occupancy Rate** - Persentase kursi terisi
        - **Peak Hour** - Jam dengan demand tertinggi
        - **Cost per Passenger** - Efisiensi biaya operasional
        """)
    
    with st.expander("🤖 Machine Learning", expanded=False):
        st.markdown("""
        ### Algoritma Tersedia
        1. **Random Forest Regression** (Default)
           - Akurat untuk data non-linear
           - Tahan terhadap outlier
        
        2. **Linear Regression**
           - Model simple & interpretable
           - Cocok untuk baseline
        
        ### Performance Metrics
        - **MAE** - Mean Absolute Error
        - **R²** - Coefficient of Determination
        - **RMSE** - Root Mean Squared Error
        """)

with tab3:
    st.markdown('<div class="section-title"><h2>Tentang Transport BI System</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Misi
    Menyediakan platform Business Intelligence terintegrasi untuk optimalisasi armada transportasi publik dan 
    efisiensi operasional rute berbasis data dan machine learning.
    
    ### 🏗️ Arsitektur
    - **Frontend**: Streamlit (Interactive Web UI)
    - **Backend**: Python services (Analytics, ML, Recommendations)
    - **Data Processing**: Pandas & PySpark
    - **ML Framework**: Scikit-learn & Joblib
    - **Visualization**: Plotly & Matplotlib
    
    ### 📋 Key Features
    - ✅ Real-time analytics dashboard
    - ✅ ML-powered passenger predictions
    - ✅ Automated fleet recommendations
    - ✅ Route optimization analysis
    - ✅ Cost efficiency tracking
    - ✅ Interactive data exploration
    
    ### 👥 Support
    - 📧 Email: support@transportbi.local
    - 📞 Hotline: +62-XXX-XXXX-XXXX
    - 📚 Docs: [Link to documentation]
    
    ### 📄 License
    Proprietary - Transport Operations Platform
    Copyright © 2026 All Rights Reserved
    """)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Platform Version", "1.0.0")
    with col2:
        st.metric("Python Version", "3.10+")
    with col3:
        st.metric("Last Updated", "June 2026")
