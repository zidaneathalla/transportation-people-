from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config.settings import settings
from services.analytics_service import AnalyticsService
from services.data_validator import DataValidator
from services.feature_engineering import FeatureEngineeringService
from services.ml_service import PassengerPredictionService
from services.preprocessing_service import PreprocessingService
from services.recommendation_service import FleetRecommendationService
from services.report_service import ReportService
from utils.helpers import rupiah
from utils.logger import get_logger


logger = get_logger(__name__)


st.set_page_config(
    page_title=settings.app_name,
    page_icon="T",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Airbnb Design System Colors
CHART_COLORS = ["#ff385c", "#0f766e", "#14b8a6", "#f59e0b", "#ef4444", "#7c3aed"]


def load_css() -> None:
    css_path = ROOT_DIR / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def create_sample_data(rows: int = 900) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2026-01-01", periods=45, freq="D")
    lines = ["BRT-01", "BRT-02", "MRT-01", "LRT-02", "BUS-07", "BUS-12"]
    stops = [f"STOP-{i:03d}" for i in range(1, 18)]

    records = []
    for _ in range(rows):
        day = pd.Timestamp(rng.choice(dates))
        hour = int(rng.choice(range(5, 23)))
        line = str(rng.choice(lines))
        seats = int(rng.choice([35, 45, 50, 60, 80]))
        peak_boost = 30 if hour in [7, 8, 17, 18] else 0
        route_boost = {"BRT-01": 25, "MRT-01": 35, "LRT-02": 18}.get(line, 5)
        passengers = max(0, int(rng.normal(22 + peak_boost + route_boost, 12)))
        arrival = pd.Timestamp(day) + pd.Timedelta(hours=hour, minutes=int(rng.integers(0, 55)))
        departure = arrival + pd.Timedelta(minutes=int(rng.integers(2, 12)))
        records.append(
            {
                "operating_day": day.date(),
                "line_id": line,
                "stop_id": str(rng.choice(stops)),
                "arrival": arrival,
                "departure": departure,
                "vehicle_seats": seats,
                "passengers": passengers,
            }
        )
    return pd.DataFrame(records)


def read_uploaded_dataset(uploaded_file) -> pd.DataFrame:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(uploaded_file)
    if suffix == ".parquet":
        return pd.read_parquet(uploaded_file)
    raise ValueError("Format file belum didukung. Gunakan CSV atau Parquet.")


def render_page_header(raw_rows: int | None = None, source: str = "Demo") -> None:
    row_text = f"{raw_rows:,} rows" if raw_rows is not None else "No data"
    st.markdown(
        f"""
        <div class="topbar">
            <div>
                <div class="eyebrow">Transport Operations Intelligence</div>
                <h1>Sistem Rekomendasi Peluncuran Armada Harian</h1>
                <p>Analisis demand, rute padat, jam puncak, prediksi penumpang, dan rekomendasi armada dalam satu cockpit BI.</p>
            </div>
            <div class="topbar-status">
                <span>{source}</span>
                <strong>{row_text}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def authenticate() -> bool:
    if st.session_state.get("authenticated"):
        return True

    # Initialize session state for showing login form
    if "show_login" not in st.session_state:
        st.session_state.show_login = False

    # Landing page - show before Get Started is clicked
    if not st.session_state.show_login:
        intro_col, action_col = st.columns([1.25, 0.75], gap="large")
        with intro_col:
            st.markdown(
                """
                <div class="landing-page landing-page-split">
                    <div class="eyebrow">Transport Operations Intelligence</div>
                    <h1 class="landing-title">Transport BI System</h1>
                    <p class="landing-subtitle">Masuk ke dashboard operasional armada dan demand penumpang.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with action_col:
            st.markdown(
                """
                <div class="auth-card">
                    <div class="auth-card-header"></div>
                    <div class="auth-card-content">
                        <h2>Mulai Analisis</h2>
                        <p>Buka cockpit BI untuk mengelola dataset, prediksi penumpang, dan rekomendasi armada.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Get Started", use_container_width=True, key="get_started"):
                st.session_state.show_login = True
                st.rerun()
        return False

    # Login form - show after Get Started is clicked
    intro_col, form_col = st.columns([1.25, 0.75], gap="large")
    with intro_col:
        st.markdown(
            """
            <div class="landing-page landing-page-split">
                <div class="eyebrow">Secure Access</div>
                <h1 class="landing-title">Transport BI System</h1>
                <p class="landing-subtitle">Login untuk masuk ke dashboard operasional, analytics, dan rekomendasi armada harian.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    login = False
    with form_col:
        st.markdown(
            """
            <div class="auth-card">
                <div class="auth-card-header"></div>
                <div class="auth-card-content">
                    <h2>Login Dashboard</h2>
                    <p>Masukkan kredensial admin untuk melanjutkan.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        col_a, col_b = st.columns(2)

        with col_a:
            login = st.button("Login", use_container_width=True, key="login_btn")

        with col_b:
            if st.button("Back", use_container_width=True, key="back_btn"):
                st.session_state.show_login = False
                st.rerun()

    if login:
        if username == settings.admin_username and password == settings.admin_password:
            st.session_state["authenticated"] = True
            st.rerun()
        st.error("Username atau password salah.")
    return False


@st.cache_data(show_spinner=False)
def build_dataset(raw_df: pd.DataFrame, use_spark: bool) -> pd.DataFrame:
    validator = DataValidator()
    preprocessing = PreprocessingService()
    features = FeatureEngineeringService()

    validation = validator.validate(raw_df)
    if not validation.is_valid:
        raise ValueError(
            "Kolom wajib belum lengkap: " + ", ".join(validation.missing_columns)
        )

    cleaned = (
        preprocessing.clean_with_spark(validation.dataframe)
        if use_spark
        else preprocessing.clean_with_pandas(validation.dataframe)
    )
    return features.transform(cleaned)


def render_kpi_cards(kpis: dict) -> None:
    metrics = [
        ("Total Penumpang", f"{kpis['total_passengers']:,}", "Demand historis"),
        ("Total Rute", f"{kpis['total_routes']:,}", "Rute unik"),
        ("Occupancy Avg", f"{kpis['avg_occupancy']:.1f}%", "Utilisasi kursi"),
        ("Jam Puncak", kpis["peak_hour"], "Peak hour"),
        ("Biaya Operasional", rupiah(kpis["operational_cost"]), "Estimasi total"),
    ]
    columns = st.columns(5)
    for column, (label, value, caption) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <span>{caption}</span>
                    <h3>{value}</h3>
                    <p>{label}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def style_figure(fig: go.Figure, height: int = 360) -> go.Figure:
    """Apply Airbnb design system styling to Plotly figures"""
    fig.update_layout(
        height=height,
        template="plotly_white",
        margin=dict(l=16, r=16, t=48, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(
            color="#222222",
            family="'Airbnb Cereal VF', Circular, -apple-system, system-ui, Roboto, 'Helvetica Neue', sans-serif",
            size=14,
        ),
        title=dict(
            font=dict(
                size=16,
                color="#222222",
                family="'Airbnb Cereal VF', Circular, -apple-system, system-ui, Roboto, 'Helvetica Neue', sans-serif",
            ),
            x=0.0,
            xanchor="left",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
        hovermode="x unified",
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#dddddd",
        showline=True,
        linewidth=1,
    )
    fig.update_yaxes(
        gridcolor="#ebebeb",
        linecolor="#dddddd",
        showline=True,
        linewidth=1,
    )
    return fig


def render_dashboard(df: pd.DataFrame, recommendation: pd.DataFrame, kpis: dict) -> None:
    analytics = AnalyticsService()
    route_df = analytics.busiest_routes(df)
    peak_df = analytics.peak_hours(df)
    trend_df = analytics.passenger_trend(df)
    cost_df = analytics.operational_cost(df)

    render_kpi_cards(kpis)

    left, right = st.columns((1.4, 1))
    with left:
        fig = px.line(
            trend_df,
            x="tanggal",
            y="total_penumpang",
            markers=True,
            title="Tren Penumpang Harian",
            color_discrete_sequence=[CHART_COLORS[0]],
        )
        fig.update_traces(
            line=dict(width=3, color=CHART_COLORS[0]),
            marker=dict(size=8, color=CHART_COLORS[0]),
        )
        fig = style_figure(fig, 380)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            peak_df.sort_values("jam"),
            x="jam",
            y="total_penumpang",
            title="Distribusi Jam Sibuk",
            color="rata_occupancy",
            color_continuous_scale=[CHART_COLORS[2], CHART_COLORS[0], CHART_COLORS[4]],
        )
        fig = style_figure(fig, 380)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            route_df.head(10),
            x="total_penumpang",
            y="line_id",
            orientation="h",
            title="Top 10 Rute Terpadat",
            color="rata_occupancy",
            color_continuous_scale=[CHART_COLORS[2], CHART_COLORS[3], CHART_COLORS[4]],
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig = style_figure(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(
            cost_df.head(10),
            x="line_id",
            y="total_biaya",
            title="Biaya Operasional per Rute",
            color="total_penumpang",
            color_continuous_scale=[CHART_COLORS[2], CHART_COLORS[0]],
        )
        fig = style_figure(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title"><h2>Tabel Rekomendasi Armada Harian</h2><span>Hasil kalkulasi: ceil(prediksi / kapasitas)</span></div>', unsafe_allow_html=True)
    st.dataframe(
        recommendation[
            [
                "tanggal",
                "line_id",
                "jam_kategori",
                "prediksi_penumpang",
                "kapasitas_armada",
                "jumlah_armada",
                "prioritas_rute",
                "estimasi_biaya",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown('<div class="section-title"><h2>Klasifikasi Prioritas Rute</h2><span>Berdasarkan occupancy rate dan demand</span></div>', unsafe_allow_html=True)
    priority_df = (
        recommendation.groupby("prioritas_rute", as_index=False)
        .agg(total_armada=("jumlah_armada", "sum"), total_prediksi=("prediksi_penumpang", "sum"))
        .sort_values("total_armada", ascending=False)
    )
    fig = px.pie(
        priority_df,
        values="total_armada",
        names="prioritas_rute",
        hole=0.4,
        title="Komposisi Armada Berdasarkan Prioritas",
        color_discrete_sequence=CHART_COLORS,
    )
    fig = style_figure(fig, 420)
    fig.update_traces(textposition="inside", textinfo="label+percent")
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    load_css()
    if not authenticate():
        return

    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <strong>Transport BI</strong>
            <span>Fleet Decision Platform</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    uploaded_file = st.sidebar.file_uploader(
        "Upload dataset Kaggle",
        type=["csv", "parquet"],
        help="Mendukung file .csv dan .parquet",
    )
    use_sample = st.sidebar.toggle("Gunakan sample data demo", value=uploaded_file is None)
    use_spark = st.sidebar.toggle(
        "Preprocessing dengan PySpark",
        value=False,
        help="Jika Spark/Java bermasalah di laptop atau deployment, matikan toggle ini. Aplikasi tetap berjalan dengan Pandas.",
    )
    algorithm = st.sidebar.selectbox(
        "Algoritma ML",
        ["random_forest", "linear_regression"],
        format_func=lambda value: "Random Forest Regression" if value == "random_forest" else "Linear Regression",
    )

    try:
        if uploaded_file is not None:
            raw_df = read_uploaded_dataset(uploaded_file)
            data_source = Path(uploaded_file.name).suffix.upper().replace(".", "") + " Upload"
        elif use_sample:
            raw_df = create_sample_data()
            data_source = "Demo Dataset"
        else:
            render_page_header(None, "Waiting")
            st.info("Upload CSV atau aktifkan sample data demo.")
            return

        render_page_header(len(raw_df), data_source)

        validator = DataValidator()
        validation = validator.validate(raw_df)
        validation_state = "Valid" if validation.is_valid else "Needs Fix"
        st.markdown(
            f"""
            <div class="validation-strip">
                <div><span>Status Dataset</span><strong>{validation_state}</strong></div>
                <div><span>Rows</span><strong>{len(validation.dataframe):,}</strong></div>
                <div><span>Columns</span><strong>{len(validation.dataframe.columns):,}</strong></div>
                <div><span>Missing Required</span><strong>{len(validation.missing_columns)}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Detail Validasi Dataset", expanded=not validation.is_valid):
            st.json(
                {
                    "valid": validation.is_valid,
                    "missing_columns": validation.missing_columns,
                    "warnings": validation.warnings,
                    "rows": len(validation.dataframe),
                    "columns": list(validation.dataframe.columns),
                }
            )
            st.dataframe(validation.dataframe.head(20), use_container_width=True)

        if not validation.is_valid:
            st.error("Dataset belum valid. Lengkapi kolom wajib sebelum analisis.")
            return

        df = build_dataset(raw_df, use_spark)
        settings.processed_data_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(settings.processed_data_dir / "transport_business_dataset.csv", index=False)

        predictor = PassengerPredictionService(algorithm=algorithm)
        model_result = None
        try:
            model_result = predictor.train(df)
            df["prediksi_penumpang"] = predictor.predict(df).round(0)
        except Exception as exc:
            logger.exception("Model training failed")
            st.warning(f"Model ML belum bisa dilatih: {exc}. Sistem memakai data aktual.")
            df["prediksi_penumpang"] = df["passengers"]

        recommendation_service = FleetRecommendationService()
        recommendation = recommendation_service.build_daily_recommendation(df)
        analytics = AnalyticsService()
        kpis = analytics.kpis(df)

        if model_result:
            st.markdown(
                f"""
                <div class="model-banner">
                    <strong>{model_result.model_name}</strong>
                    <span>MAE {model_result.mae:.2f}</span>
                    <span>R2 {model_result.r2:.2f}</span>
                    <span>{model_result.rows:,} training rows</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        tabs = st.tabs(["Dashboard BI", "Business Dataset", "Prediksi", "Laporan"])
        with tabs[0]:
            render_dashboard(df, recommendation, kpis)

        with tabs[1]:
            st.markdown('<div class="section-title"><h2>Business Dataset Hasil Transformasi</h2><span>Dataset setelah feature engineering dan preprocessing</span></div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                "📥 Download Business Dataset (CSV)",
                df.to_csv(index=False).encode("utf-8"),
                "transport_business_dataset.csv",
                "text/csv",
                use_container_width=True,
            )

        with tabs[2]:
            st.markdown('<div class="section-title"><h2>Prediksi Jumlah Penumpang</h2><span>Hasil prediksi model ML dengan occupancy rate</span></div>', unsafe_allow_html=True)
            prediction_view = df[
                [
                    "tanggal",
                    "line_id",
                    "stop_id",
                    "jam",
                    "jam_kategori",
                    "vehicle_seats",
                    "passengers",
                    "prediksi_penumpang",
                    "occupancy_rate",
                    "prioritas_rute",
                ]
            ].sort_values(["tanggal", "line_id", "jam"])
            st.dataframe(prediction_view, use_container_width=True, hide_index=True)

        with tabs[3]:
            st.markdown('<div class="section-title"><h2>Laporan Rekomendasi Harian</h2><span>Export dan ringkasan operasional</span></div>', unsafe_allow_html=True)
            report = ReportService()
            summary = report.daily_summary_text(recommendation)
            st.text_area("Ringkasan Rekomendasi Harian", summary, height=200, disabled=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Export ke Excel", use_container_width=True):
                    path = report.export_excel(
                        recommendation,
                        kpis,
                        {
                            "Rute Terpadat": analytics.busiest_routes(df),
                            "Jam Sibuk": analytics.peak_hours(df),
                            "Tren Harian": analytics.passenger_trend(df),
                            "Biaya Operasional": analytics.operational_cost(df),
                        },
                    )
                    st.success(f"Laporan berhasil dibuat: {path}")
            
            with col2:
                if st.button("Copy Summary", use_container_width=True):
                    st.info("Ringkasan tersalin ke clipboard (copy dari text area di atas)")

    except Exception as exc:
        logger.exception("Application error")
        st.error(f"❌ Terjadi kesalahan: {exc}")


if __name__ == "__main__":
    main()
