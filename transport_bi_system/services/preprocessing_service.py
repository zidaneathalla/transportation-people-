from __future__ import annotations

import os

import pandas as pd

from config.settings import settings
from utils.logger import get_logger


logger = get_logger(__name__)


class PreprocessingService:
    def clean_with_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        clean_df = df.copy()
        clean_df = clean_df.drop_duplicates()

        clean_df["operating_day"] = pd.to_datetime(
            clean_df["operating_day"], errors="coerce"
        )
        clean_df["arrival"] = pd.to_datetime(clean_df["arrival"], errors="coerce")
        clean_df["departure"] = pd.to_datetime(clean_df["departure"], errors="coerce")

        numeric_columns = ["vehicle_seats", "passengers"]
        for column in numeric_columns:
            clean_df[column] = pd.to_numeric(clean_df[column], errors="coerce")

        clean_df["vehicle_seats"] = clean_df["vehicle_seats"].fillna(
            settings.default_vehicle_capacity
        )
        clean_df["passengers"] = clean_df["passengers"].fillna(0)

        clean_df = clean_df.dropna(subset=["operating_day", "line_id", "stop_id"])
        clean_df = clean_df[clean_df["vehicle_seats"] > 0]
        clean_df = clean_df[clean_df["passengers"] >= 0]

        clean_df["line_id"] = clean_df["line_id"].astype(str)
        clean_df["stop_id"] = clean_df["stop_id"].astype(str)
        logger.info("Pandas preprocessing completed. rows=%s", len(clean_df))
        return clean_df.reset_index(drop=True)

    def clean_with_spark(self, df: pd.DataFrame) -> pd.DataFrame:
        spark = None
        try:
            from pyspark.sql import SparkSession
            from pyspark.sql.functions import col, to_timestamp

            os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
            os.environ.setdefault("SPARK_LOCAL_HOSTNAME", "localhost")

            spark = (
                SparkSession.builder.appName("TransportBIPreprocessing")
                .master("local[*]")
                .config("spark.driver.host", "127.0.0.1")
                .config("spark.driver.bindAddress", "127.0.0.1")
                .config("spark.local.hostname", "localhost")
                .config("spark.ui.showConsoleProgress", "false")
                .getOrCreate()
            )

            spark_df = spark.createDataFrame(df.astype(str))
            spark_df = spark_df.dropDuplicates()
            spark_df = spark_df.withColumn(
                "operating_day", to_timestamp(col("operating_day"))
            )
            spark_df = spark_df.withColumn("arrival", to_timestamp(col("arrival")))
            spark_df = spark_df.withColumn("departure", to_timestamp(col("departure")))
            spark_df = spark_df.withColumn("vehicle_seats", col("vehicle_seats").cast("double"))
            spark_df = spark_df.withColumn("passengers", col("passengers").cast("double"))
            spark_df = spark_df.fillna(
                {"vehicle_seats": settings.default_vehicle_capacity, "passengers": 0}
            )
            spark_df = spark_df.filter(col("vehicle_seats") > 0).filter(col("passengers") >= 0)

            result = spark_df.toPandas()
            logger.info("Spark preprocessing completed. rows=%s", len(result))
            return result.reset_index(drop=True)
        except Exception as exc:
            logger.warning("Spark preprocessing failed, fallback to pandas. error=%s", exc)
            return self.clean_with_pandas(df)
        finally:
            if spark is not None:
                try:
                    spark.stop()
                except Exception as exc:
                    logger.warning("Spark stop failed. error=%s", exc)
