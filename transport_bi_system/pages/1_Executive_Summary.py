import streamlit as st


st.set_page_config(page_title="Executive Summary", layout="wide")
st.title("Executive Summary")
st.warning("Halaman ini bukan entry point deployment.")
st.info(
    "Untuk menjalankan atau deploy aplikasi, gunakan `transport_bi_system/app.py` "
    "sebagai main file. Folder `pages/` hanya untuk halaman tambahan Streamlit."
)
st.code("streamlit run transport_bi_system/app.py", language="bash")
