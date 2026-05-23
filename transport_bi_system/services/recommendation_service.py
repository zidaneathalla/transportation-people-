from __future__ import annotations

import pandas as pd

from config.settings import settings
from utils.helpers import ceil_division


class FleetRecommendationService:
    def build_daily_recommendation(
        self,
        df: pd.DataFrame,
        prediction_column: str = "prediksi_penumpang",
    ) -> pd.DataFrame:
        data = df.copy()
        if prediction_column not in data.columns:
            prediction_column = "passengers"

        recommendation = (
            data.groupby(["tanggal", "line_id", "jam_kategori"], as_index=False)
            .agg(
                prediksi_penumpang=(prediction_column, "sum"),
                kapasitas_armada=("vehicle_seats", "median"),
                occupancy_rate=("occupancy_rate", "mean"),
                biaya_operasional=("biaya_operasional", "sum"),
            )
            .sort_values(["tanggal", "prediksi_penumpang"], ascending=[True, False])
        )

        recommendation["kapasitas_armada"] = recommendation["kapasitas_armada"].fillna(
            settings.default_vehicle_capacity
        )
        recommendation["jumlah_armada"] = recommendation.apply(
            lambda row: ceil_division(row["prediksi_penumpang"], row["kapasitas_armada"]),
            axis=1,
        )
        recommendation["prioritas_rute"] = recommendation["occupancy_rate"].apply(
            self._priority_from_occupancy
        )
        recommendation["estimasi_biaya"] = (
            recommendation["jumlah_armada"] * settings.default_cost_per_fleet
        )
        return recommendation

    @staticmethod
    def _priority_from_occupancy(occupancy_rate: float) -> str:
        if occupancy_rate >= 85:
            return "Tinggi"
        if occupancy_rate >= 60:
            return "Sedang"
        return "Rendah"
