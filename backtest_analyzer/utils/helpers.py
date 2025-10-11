import os
from pathlib import Path


def ensure_dir_exists(path: str | Path) -> None:
    """
    Memastikan sebuah direktori ada, jika tidak, maka akan dibuat.
 
    Args:
        path (str | Path): Path ke direktori.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Mendapatkan path root dari direktori advanced_backtest."""
    return Path(__file__).parent.parent.resolve()