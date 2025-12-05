import unicodedata
import pandas as pd
from pathlib import Path


def normalize_name(name: str) -> str:
    return unicodedata.normalize("NFKC", str(name)).strip().casefold()


def load_reference_names(ref_path: Path) -> set[str]:
    """Load column names from the reference file and normalize them.

    The reference file is expected to be an Excel workbook where the
    first non‑empty column contains the names of columns to remove. Empty rows are ignored.

    Args:
        ref_path: Path to the reference Excel file.

    Returns:
        A set of normalized column names.
    """

    df = pd.read_excel(ref_path, dtype=str)
    first_col = None
    for col in df.columns:
        if df[col].notna().any():
            first_col = col
            break
    if first_col is None:
        return set()
    names = (
        df[first_col]
        .dropna()
        .astype(str)
        .map(str.strip)
        .loc[lambda s: s != '']
        .tolist()
    )
    return {normalize_name(name) for name in names}

def drop_columns(src_df: pd.DataFrame, ref_norm: set[str]) -> pd.DataFrame:
    src_cols = list(src_df.columns)
    col_norm_map = {col: normalize_name(col) for col in src_cols}
    matched_cols = [col for col in src_cols if col_norm_map[col] in ref_norm]
    return src_df.drop(columns=matched_cols, errors="ignore")


def main () -> None:
    src_file = Path("src/受入れ検査品リスト.xlsx")
    ref_file = Path("ref/filtered_columns.xlsx")
    if not src_file.exists():
        raise FileNotFoundError(f"Source file not found: {src_file}")
    if not ref_file.exists():
        raise FileNotFoundError(f"Reference file not found: {ref_file}")
    src_df = pd.read_excel(src_file, header=0, dtype=object)
    ref_norm = load_reference_names(ref_file)
    result_df = drop_columns(src_df, ref_norm)
    out_name = f"pattern1_{src_file.stem}_参照に一致する列を削除.xlsx"
    out_path = src_file.parent / out_name
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        result_df.to_excel(writer, index=False)
    print(f"Output written to: {out_path}")

if __name__ == "__main__":
    main ()