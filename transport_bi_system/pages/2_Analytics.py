"""
Analytics Page - Detailed transportation analytics and insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from services.analytics_service import AnalyticsService
from config.settings import settings

st.set_page_config(page_title="Analytics", layout="wide")

# Load CSS
css_path = ROOT_DIR / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="page-header">
        <div class="eyebrow">Advanced Analytics</div>
        <h1>Transportation Insights & Trends</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Analisis mendalam tentang pola penumpang, performa rute, dan efisiensi operasional.")

# Check if data exists
data_path = settings.processed_data_dir / "transport_business_dataset.csv"
if not data_path.exists():
    st.info("Belum ada data. Jalankan dashboard utama terlebih dahulu untuk memproses data.")
    st.stop()

# Load data
df = pd.read_csv(data_path)
analytics = AnalyticsService()

# Define chart colors (Airbnb design system)
COLORS = ["#ff385c", "#0f766e", "#14b8a6", "#f59e0b", "#ef4444", "#7c3aed"]

def style_figure(fig, height=360):
    """Apply Airbnb design system styling"""
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
        title=dict(font=dict(size=16, color="#222222")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor="#dddddd", showline=True, linewidth=1)
    fig.update_yaxes(gridcolor="#ebebeb", linecolor="#dddddd", showline=True, linewidth=1)
    return fig

# Main Analytics
tab1, tab2, tab3 = st.tabs(["Tren & Pola", "Performa Rute", "Operasional"])

with tab1:
    st.markdown("### Tren Penumpang & Demand")
    
    col1, col2 = st.columns(2)
    with col1:
        trend_df = analytics.passenger_trend(df)
        fig = px.area(
            trend_df,
            x="tanggal",
            y="total_penumpang",
            title="📅 Tren Penumpang Harian",
            color_discrete_sequence=[COLORS[0]],
        )
        fig.update_traces(fill="tozeroy", fillcolor="rgba(255, 56, 92, 0.1)")
        fig = style_figure(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        peak_df = analytics.peak_hours(df)
        fig = px.bar(
            peak_df.sort_values("jam"),
            x="jam",
            y="total_penumpang",
            title="Distribusi Penumpang per Jam",
            color="rata_occupancy",
            color_continuous_scale=[COLORS[2], COLORS[0], COLORS[4]],
        )
        fig = style_figure(fig, 380)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Performa & Kapasitas Rute")
    
    col1, col2 = st.columns(2)
    with col1:
        route_df = analytics.busiest_routes(df)
        fig = px.bar(
            route_df.head(12),
            x="total_penumpang",
            y="line_id",
            orientation="h",
            title="Top 12 Rute (Total Penumpang)",
            color="rata_occupancy",
            color_continuous_scale=[COLORS[2], COLORS[3], COLORS[4]],
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig = style_figure(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        route_stats = df.groupby("line_id").agg({
            "occupancy_rate": "mean",
            "passengers": "sum",
            "vehicle_seats": "mean",
        }).reset_index().sort_values("occupancy_rate", ascending=False)
        
        fig = px.bar(
            route_stats,
            x="line_id",
            y="occupancy_rate",
            title="Rata-rata Occupancy Rate per Rute",
            color="occupancy_rate",
            color_continuous_scale=[COLORS[2], COLORS[0]],
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig = style_figure(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Analisis Operasional")
    
    col1, col2 = st.columns(2)
    with col1:
        cost_df = analytics.operational_cost(df)
        fig = px.bar(
            cost_df.head(10),
            x="line_id",
            y="total_biaya",
            title="Biaya Operasional Top 10 Rute",
            color="total_penumpang",
            color_continuous_scale=[COLORS[2], COLORS[0]],
        )
        fig = style_figure(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost per passenger analysis
        cost_analysis = df.groupby("line_id").agg({
            "passengers": "sum",
        }).reset_index()
        cost_analysis["cost_per_passenger"] = 750000 / (cost_analysis["passengers"] / cost_analysis["passengers"].sum() * 100)
        
        fig = px.scatter(
            cost_analysis,
            x="passengers",
            y="cost_per_passenger",
            size="passengers",
            color="cost_per_passenger",
            hover_data={"line_id": True},
            title="Cost Efficiency Analysis",
            color_continuous_scale=[COLORS[2], COLORS[4]],
        )
        fig = style_figure(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

# Data Export
st.markdown("### Data Export")
col1, col2 = st.columns(2)

with col1:
    if st.button("Download Analytics Report", use_container_width=True):
        analytics_data = {
            "Busiest Routes": analytics.busiest_routes(df).to_csv(index=False),
            "Peak Hours": analytics.peak_hours(df).to_csv(index=False),
            "Passenger Trend": analytics.passenger_trend(df).to_csv(index=False),
        }
        st.success("✅ Data siap didownload")

with col2:
    if st.button("📋 Copy Summary Statistics", use_container_width=True):
        st.info("📌 Salin statistik dari charts di atas")
