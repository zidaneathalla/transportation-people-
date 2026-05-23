from __future__ import annotations

from pathlib import Path

import pandas as pd

from config.settings import settings
from utils.helpers import ensure_parent, timestamp_name


class ReportService:
    def export_excel(
        self,
        recommendation: pd.DataFrame,
        kpis: dict,
        analytics: dict[str, pd.DataFrame],
    ) -> Path:
        path = ensure_parent(settings.reports_dir / timestamp_name("daily_recommendation", "xlsx"))
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            pd.DataFrame([kpis]).to_excel(writer, sheet_name="KPI", index=False)
            recommendation.to_excel(writer, sheet_name="Rekomendasi Armada", index=False)
            for sheet, frame in analytics.items():
                frame.to_excel(writer, sheet_name=sheet[:31], index=False)
        return path

    def daily_summary_text(self, recommendation: pd.DataFrame) -> str:
        if recommendation.empty:
            return "Belum ada rekomendasi karena data kosong."

        top = recommendation.sort_values("prediksi_penumpang", ascending=False).head(5)
        total_fleet = int(recommendation["jumlah_armada"].sum())
        total_cost = float(recommendation["estimasi_biaya"].sum())
        lines = [
            "Ringkasan rekomendasi harian:",
            f"- Total armada direkomendasikan: {total_fleet}",
            f"- Estimasi biaya operasional: Rp {total_cost:,.0f}".replace(",", "."),
            "- Rute prioritas utama:",
        ]
        for _, row in top.iterrows():
            lines.append(
                f"  {row['line_id']} | {row['jam_kategori']} | "
                f"{row['jumlah_armada']} armada | {row['prioritas_rute']}"
            )
        return "\n".join(lines)
