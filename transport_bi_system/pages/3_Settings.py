"""
Settings & Documentation Page
"""
import streamlit as st
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config.settings import settings

st.set_page_config(page_title="Settings", layout="wide")

css_path = ROOT_DIR / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="page-header">
        <div class="eyebrow">System Settings</div>
        <h1>Configuration & Documentation</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Pengaturan aplikasi, dokumentasi teknis, dan panduan penggunaan.")

tab1, tab2, tab3 = st.tabs(["Configuration", "Documentation", "About"])

with tab1:
    st.markdown("### Konfigurasi Aplikasi")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("App", settings.app_name)
    with col2:
        st.metric("Version", "1.0.0")
    with col3:
        st.metric("Storage", "CSV")
    with col4:
        st.metric("ML Engine", "Scikit-learn")

    with st.expander("Data Pipeline", expanded=False):
        st.markdown(
            """
            1. **Data Validation** — memastikan kolom wajib lengkap
            2. **Preprocessing** — cleaning & normalisasi data
            3. **Feature Engineering** — transformasi fitur tambahan
            4. **Model Training** — latih ML model
            5. **Prediction** — generate prediksi penumpang
            6. **Recommendation** — kalkulasi rekomendasi armada
            """
        )

with tab2:
    st.markdown("### Panduan Penggunaan")

    with st.expander("Getting Started", expanded=True):
        st.markdown(
            """
            ### Langkah Awal
            1. **Login** — masukkan username & password admin
            2. **Upload Data** — upload file CSV atau Parquet dari sidebar
            3. **Validasi** — sistem otomatis validasi dataset
            4. **Analisis** — lihat hasil di dashboard

            ### Format Data Wajib
            - `operating_day`: Tanggal operasional (YYYY-MM-DD)
            - `line_id`: ID rute transportasi
            - `stop_id`: ID halte
            - `arrival`: Waktu kedatangan
            - `departure`: Waktu keberangkatan
            - `vehicle_seats`: Kapasitas kendaraan
            - `passengers`: Jumlah penumpang aktual
            """
        )

    with st.expander("Dashboard BI", expanded=False):
        st.markdown(
            """
            ### Fitur Dashboard
            - KPI ringkasan metrik utama
            - Tren dan analisis jam sibuk
            - Analisis performa rute
            - Rekomendasi armada optimal
            - Klasifikasi prioritas rute
            """
        )

    with st.expander("Machine Learning", expanded=False):
        st.markdown(
            """
            ### Algoritma Tersedia
            1. **Random Forest Regression** (default) — akurat untuk data non-linear
            2. **Linear Regression** — model simple & interpretable

            ### Performance Metrics
            - **MAE** — Mean Absolute Error
            - **R²** — Coefficient of Determination
            """
        )

with tab3:
    st.markdown("### Tentang Transport BI System")
    st.markdown(
        """
        Platform Business Intelligence terintegrasi untuk optimalisasi armada transportasi
        publik berbasis data dan machine learning.

        **Arsitektur:** Streamlit · Python services · Pandas/PySpark · Scikit-learn · Plotly

        **Fitur utama:** analytics dashboard, prediksi penumpang, rekomendasi armada,
        analisis rute, tracking biaya operasional.

        Copyright © 2026 · Proprietary
        """
    )
