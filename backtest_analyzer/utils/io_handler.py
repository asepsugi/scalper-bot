import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
 
from .helpers import ensure_dir_exists, get_project_root
 
 
def load_backtest_results(filename: str) -> List[Dict[str, Any]]:
    """
    Memuat hasil backtest dari file JSON di direktori root proyek.
 
    Args:
        filename (str): Nama file JSON (misal: 'metrics_BTCUSDT.json').
 
    Returns:
        List[Dict[str, Any]]: Daftar dictionary yang berisi metrik setiap strategi.
    """
    # Create a Path object from the filename and resolve it to an absolute path.
    # This correctly handles relative paths like '../metrics.json'.
    filepath = Path(filename).resolve()

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        print(f"✅ Berhasil memuat {len(data)} versi strategi dari '{filepath}'")
        return data
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' tidak ditemukan.")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: File '{filepath}' bukan file JSON yang valid.")
        return []
 
 
def save_output(data: pd.DataFrame, filename_base: str, output_dir: Path) -> None:
    """
    Menyimpan DataFrame ke file CSV dan JSON di direktori output.
 
    Args:
        data (pd.DataFrame): DataFrame yang akan disimpan.
        filename_base (str): Nama dasar untuk file (misal: 'summary').
        output_dir (Path): Direktori untuk menyimpan output.
    """
    ensure_dir_exists(output_dir)
    csv_path = output_dir / f"{filename_base}.csv"
    json_path = output_dir / f"{filename_base}.json"
 
    data.to_csv(csv_path, index=False)
    data.to_json(json_path, orient="records", indent=2)
    print(f"✅ Laporan disimpan ke '{csv_path}' dan '{json_path}'")