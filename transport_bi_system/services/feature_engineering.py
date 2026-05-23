from __future__ import annotations

import numpy as np
import pandas as pd

from config.settings import settings


class FeatureEngineeringService:
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()

        data["operating_day"] = pd.to_datetime(data["operating_day"], errors="coerce")
        data["arrival"] = pd.to_datetime(data["arrival"], errors="coerce")
        data["departure"] = pd.to_datetime(data["departure"], errors="coerce")

        data["hari"] = data["operating_day"].dt.day_name()
        data["day_of_week"] = data["operating_day"].dt.dayofweek
        data["jenis_hari"] = np.where(data["day_of_week"] >= 5, "Weekend", "Weekday")
        data["jam"] = data["arrival"].dt.hour.fillna(data["departure"].dt.hour).fillna(0).astype(int)
        data["jam_kategori"] = data["jam"].apply(self._hour_category)
        data["tanggal"] = data["operating_day"].dt.date

        data["occupancy_rate"] = (
            data["passengers"] / data["vehicle_seats"] * 100
        ).replace([np.inf, -np.inf], 0).fillna(0)

        data["cuaca"] = data.apply(self._dummy_weather, axis=1)
        data["biaya_operasional"] = data["vehicle_seats"].apply(
            lambda seats: max(1, round(float(seats) / settings.default_vehicle_capacity))
            * settings.default_cost_per_fleet
        )
        data["prioritas_rute"] = data["occupancy_rate"].apply(self._route_priority)
        data["is_peak_hour"] = data["jam_kategori"].isin(["Pagi Sibuk", "Sore Sibuk"]).astype(int)
        return data

    @staticmethod
    def _hour_category(hour: int) -> str:
        if 6 <= hour <= 9:
            return "Pagi Sibuk"
        if 10 <= hour <= 15:
            return "Siang"
        if 16 <= hour <= 19:
            return "Sore Sibuk"
        if 20 <= hour <= 23:
            return "Malam"
        return "Dini Hari"

    @staticmethod
    def _route_priority(occupancy_rate: float) -> str:
        if occupancy_rate >= 85:
            return "Tinggi"
        if occupancy_rate >= 60:
            return "Sedang"
        return "Rendah"

    @staticmethod
    def _dummy_weather(row: pd.Series) -> str:
        code = (int(row.get("day_of_week", 0)) + int(row.get("jam", 0))) % 4
        return ["Cerah", "Berawan", "Hujan Ringan", "Hujan"][code]
