from pathlib import Path
from tomllib import load


class Config:
    db_path: str

    def __init__(self, path: Path):
        with open(path, "rb") as f:
            config_raw = load(f)
            self.db_path = config_raw["db_path"]
