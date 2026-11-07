"""
MARKETIX Data Loader Module
Handles loading of CSV and Excel marketing datasets with delimiter auto-detection.
"""

from pathlib import Path
import pandas as pd
import io
import logging

logger = logging.getLogger("marketix.loader")
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "marketing_campaign.csv"


def load_dataset(file_or_path=None) -> tuple[pd.DataFrame | None, str]:
    """
    Loads dataset from a file path or file-like object (uploaded file in Streamlit).
    Automatically handles comma, semicolon, and tab delimiters, as well as Excel files.
    """
    target = file_or_path if file_or_path is not None else DEFAULT_DATA_PATH
    
    try:
        if isinstance(target, (str, Path)):
            path = Path(target)
            if not path.exists():
                return None, f"File not found at: {path}"
            
            if path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(path)
            else:
                # Delimiter detection for CSV
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    first_line = f.readline()
                sep = ";" if ";" in first_line else ("\t" if "\t" in first_line else ",")
                df = pd.read_csv(path, sep=sep)
        else:
            # File-like object from Streamlit file_uploader
            file_name = getattr(target, "name", "uploaded_file.csv")
            if file_name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(target)
            else:
                content = target.read()
                if isinstance(content, bytes):
                    sample = content[:1024].decode("utf-8", errors="ignore")
                    target.seek(0)
                else:
                    sample = content[:1024]
                    target.seek(0)
                
                sep = ";" if ";" in sample else ("\t" if "\t" in sample else ",")
                df = pd.read_csv(target, sep=sep)
                
        return df, f"Successfully loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns."
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return None, f"Error loading file: {str(e)}"


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """Generates a comprehensive summary dictionary of the dataset."""
    missing_series = df.isnull().sum()
    missing_dict = missing_series[missing_series > 0].to_dict()
    
    return {
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "columns": df.columns.tolist(),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": missing_dict,
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
    }
