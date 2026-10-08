import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class MonitorConfig(BaseModel):
    watch_paths: List[str] = Field(default_factory=lambda: ["./data/sandbox"])
    quarantine_path: str = "./data/quarantine"
    entropy_threshold: float = 6.5
    window_seconds: int = 10
    max_events_per_window: int = 15
    cpu_spike_threshold: float = 75.0
    simulation_mode: bool = True

class WeightsConfig(BaseModel):
    rapid_encryption: float = 40.0
    mass_rename: float = 30.0
    high_entropy: float = 25.0
    cpu_spike: float = 15.0
    unknown_program: float = 10.0

class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    monitor: MonitorConfig = Field(default_factory=MonitorConfig)
    weights: WeightsConfig = Field(default_factory=WeightsConfig)

def load_config(config_path: str = "config.yaml") -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        return AppConfig()
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    return AppConfig(**data)