from __future__ import annotations

import pandas as pd


class AnalyticsService:
    def kpis(self, df: pd.DataFrame) -> dict:
        total_passengers = int(df["passengers"].sum())
        total_routes = int(df["line_id"].nunique())
        avg_occupancy = float(df["occupancy_rate"].mean()) if not df.empty else 0.0
        peak_hour = self.peak_hours(df).head(1)
        busiest_route = self.busiest_routes(df).head(1)

        return {
            "total_passengers": total_passengers,
            "total_routes": total_routes,
            "avg_occupancy": avg_occupancy,
            "peak_hour": "-" if peak_hour.empty else str(peak_hour.iloc[0]["jam"]),
            "busiest_route": "-" if busiest_route.empty else str(busiest_route.iloc[0]["line_id"]),
            "operational_cost": float(df["biaya_operasional"].sum()),
        }

    def busiest_routes(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("line_id", as_index=False)
            .agg(
                total_penumpang=("passengers", "sum"),
                rata_occupancy=("occupancy_rate", "mean"),
                total_trip=("line_id", "size"),
            )
            .sort_values("total_penumpang", ascending=False)
        )

    def peak_hours(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("jam", as_index=False)
            .agg(total_penumpang=("passengers", "sum"), rata_occupancy=("occupancy_rate", "mean"))
            .sort_values("total_penumpang", ascending=False)
        )

    def passenger_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("tanggal", as_index=False)
            .agg(total_penumpang=("passengers", "sum"), rata_occupancy=("occupancy_rate", "mean"))
            .sort_values("tanggal")
        )

    def operational_cost(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("line_id", as_index=False)
            .agg(total_biaya=("biaya_operasional", "sum"), total_penumpang=("passengers", "sum"))
            .sort_values("total_biaya", ascending=False)
        )
