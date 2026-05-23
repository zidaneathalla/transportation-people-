from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Transport BI System")
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")
    default_vehicle_capacity: int = int(os.getenv("DEFAULT_VEHICLE_CAPACITY", "50"))
    default_cost_per_fleet: float = float(os.getenv("DEFAULT_COST_PER_FLEET", "750000"))
    model_path: Path = BASE_DIR / os.getenv("MODEL_PATH", "models/passenger_model.joblib")
    raw_data_dir: Path = BASE_DIR / "data" / "raw"
    processed_data_dir: Path = BASE_DIR / "data" / "processed"
    reports_dir: Path = BASE_DIR / "reports"
    logs_dir: Path = BASE_DIR / "logs"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
