from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from utils.helpers import normalize_columns


REQUIRED_COLUMNS = {
    "operating_day",
    "line_id",
    "stop_id",
    "arrival",
    "departure",
    "vehicle_seats",
    "passengers",
}

COLUMN_ALIASES = {
    "date": "operating_day",
    "day": "operating_day",
    "route_id": "line_id",
    "route": "line_id",
    "line": "line_id",
    "station_id": "stop_id",
    "halte_id": "stop_id",
    "seats": "vehicle_seats",
    "capacity": "vehicle_seats",
    "vehicle_capacity": "vehicle_seats",
    "passenger_count": "passengers",
    "jumlah_penumpang": "passengers",
}


@dataclass
class ValidationResult:
    is_valid: bool
    missing_columns: list[str]
    warnings: list[str]
    dataframe: pd.DataFrame


class DataValidator:
    def standardize(self, df: pd.DataFrame) -> pd.DataFrame:
        clean_df = normalize_columns(df)
        rename_map = {
            column: COLUMN_ALIASES[column]
            for column in clean_df.columns
            if column in COLUMN_ALIASES
        }
        return clean_df.rename(columns=rename_map)

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        standardized = self.standardize(df)
        missing = sorted(REQUIRED_COLUMNS.difference(standardized.columns))
        warnings: list[str] = []

        if standardized.empty:
            warnings.append("Dataset kosong.")
        if "passengers" in standardized.columns and standardized["passengers"].isna().all():
            warnings.append("Kolom passengers seluruhnya kosong.")
        if "vehicle_seats" in standardized.columns and (standardized["vehicle_seats"] <= 0).any():
            warnings.append("Ada kapasitas armada bernilai nol atau negatif.")

        return ValidationResult(
            is_valid=len(missing) == 0 and not standardized.empty,
            missing_columns=missing,
            warnings=warnings,
            dataframe=standardized,
        )
