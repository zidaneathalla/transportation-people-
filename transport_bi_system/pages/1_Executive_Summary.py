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

css_path = ROOT_DIR / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="page-header">
        <div class="eyebrow">Executive Summary</div>
        <h1>Transport BI System Overview</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "Platform Business Intelligence untuk optimalisasi armada transportasi publik "
    "dan peningkatan efisiensi operasional."
)

st.markdown("### Navigasi")
st.markdown(
    """
- **Dashboard utama** — jalankan `streamlit run transport_bi_system/app.py`
- **Analytics** — analitik mendalam di tab sidebar
- **Settings** — konfigurasi dan dokumentasi
"""
)

st.divider()

st.markdown("### Tujuan Sistem")
st.markdown(
    """
1. **Analisis Data Real-time** — monitoring demand penumpang dan performa rute
2. **Prediksi Penumpang** — machine learning untuk forecasting demand
3. **Optimalisasi Armada** — rekomendasi fleet allocation berdasarkan demand
4. **Efisiensi Biaya** — tracking cost per passenger dan optimalisasi rute
5. **Decision Support** — dashboard interaktif untuk decision making
"""
)

st.markdown("### Workflow Aplikasi")
st.markdown(
    """
1. Upload dataset CSV atau Parquet
2. Validasi kelengkapan kolom
3. Preprocessing dan feature engineering
4. Training model ML
5. Generate prediksi penumpang
6. Rekomendasi armada harian
7. Visualisasi KPI, grafik, dan prioritas rute
8. Export laporan Excel
"""
)

st.markdown("### Tech Stack")
st.markdown(
    """
| Komponen | Teknologi |
|----------|-----------|
| Frontend | Streamlit 1.35.0 |
| Data Processing | Pandas 2.2.2, PySpark 3.5.1 |
| ML | Scikit-learn 1.5.0 |
| Visualisasi | Plotly 5.22.0 |
"""
)

st.caption(
    "Entry point utama: `transport_bi_system/app.py` · "
    "Login default: admin / admin123"
)
