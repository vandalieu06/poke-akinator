import json
import os
from pathlib import Path


class DataHandler:
    def __init__(self, base_dir=None):
        if base_dir is None:
            self.base_dir = Path(os.getcwd()) / "app/data"
        else:
            self.base_dir = Path(base_dir)

    def get_data(self, filename: str) -> dict | list | None:
        file_path = self.base_dir / filename

        with open(file_path, "r", encoding="utf-8") as f:
            file_data = json.load(f)
            return file_data
