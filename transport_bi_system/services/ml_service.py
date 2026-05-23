from __future__ import annotations

from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from config.settings import settings
from utils.helpers import ensure_parent


FEATURES = [
    "line_id",
    "stop_id",
    "day_of_week",
    "jenis_hari",
    "jam",
    "jam_kategori",
    "vehicle_seats",
    "cuaca",
    "is_peak_hour",
]
TARGET = "passengers"


@dataclass
class ModelResult:
    model_name: str
    mae: float
    r2: float
    rows: int


class PassengerPredictionService:
    def __init__(self, algorithm: str = "random_forest") -> None:
        self.algorithm = algorithm
        self.pipeline: Pipeline | None = None

    def train(self, df: pd.DataFrame) -> ModelResult:
        train_df = df.dropna(subset=FEATURES + [TARGET]).copy()
        if len(train_df) < 10:
            raise ValueError("Minimal 10 baris data valid diperlukan untuk training model.")

        x = train_df[FEATURES]
        y = train_df[TARGET]
        test_size = 0.25 if len(train_df) >= 40 else 0.2
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=42
        )

        categorical = ["line_id", "stop_id", "jenis_hari", "jam_kategori", "cuaca"]
        numeric = ["day_of_week", "jam", "vehicle_seats", "is_peak_hour"]
        estimator = (
            LinearRegression()
            if self.algorithm == "linear_regression"
            else RandomForestRegressor(n_estimators=120, random_state=42, n_jobs=-1)
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
                ("numeric", "passthrough", numeric),
            ]
        )
        self.pipeline = Pipeline(
            steps=[("preprocessor", preprocessor), ("model", estimator)]
        )
        self.pipeline.fit(x_train, y_train)

        predictions = self.pipeline.predict(x_test)
        result = ModelResult(
            model_name=estimator.__class__.__name__,
            mae=float(mean_absolute_error(y_test, predictions)),
            r2=float(r2_score(y_test, predictions)) if len(y_test) > 1 else 0.0,
            rows=len(train_df),
        )
        ensure_parent(settings.model_path)
        joblib.dump(self.pipeline, settings.model_path)
        return result

    def load(self) -> Pipeline | None:
        if settings.model_path.exists():
            self.pipeline = joblib.load(settings.model_path)
        return self.pipeline

    def predict(self, df: pd.DataFrame) -> pd.Series:
        if self.pipeline is None:
            self.load()
        if self.pipeline is None:
            raise ValueError("Model belum dilatih.")
        return pd.Series(self.pipeline.predict(df[FEATURES]).clip(min=0), index=df.index)
