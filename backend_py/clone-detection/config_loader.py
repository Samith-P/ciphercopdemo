from __future__ import annotations
import yaml
from pathlib import Path

class AppConfig:
    def __init__(self, root: Path):
        self.root = root
        self.app = self._load_yaml(root / "config" / "app.yaml")
        self.auth = self._load_yaml(root / "config" / "authorized_sites.yaml")

    def _load_yaml(self, p: Path):
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def weights(self): return self.app.get("weights", {})
    @property
    def thresholds(self): return self.app.get("thresholds", {})
    @property
    def limits(self): return self.app.get("limits", {})
    @property
    def brands(self): return self.auth.get("brands", [])
