#!/usr/bin/env python3
"""
pattern1_filter.py
===================

このスクリプトは `受入れ検査品リスト.xlsx` と `filtered_columns.xlsx` を読み込み、
参照リストに含まれるカラム名と一致する列を元データから削除します。
削除後のデータは `pattern1_` というプレフィックス付きの Excel ファイルとして保存されます。

列名の比較では全角/半角の違い、前後の空白、大文字・小文字の違いを吸収するため、
NFKC 正規化とトリム、そして小文字化を行っています。

使い方:
    このファイルと同じディレクトリに `受入れ検査品リスト.xlsx` と `filtered_columns.xlsx` を置き、
    Python で実行してください。結果はカレントディレクトリに出力されます。

"""

from __future__ import annotations

import unicodedata
from pathlib import Path
import pandas as pd


def normalize_name(name: str) -> str:
    """Return a normalized form of a column name.

    Normalization removes leading/trailing whitespace, converts full‑width
    and half‑width characters to a common form, and lowercases the result.

    Args:
        name: The original column name.

    Returns:
        A normalized string suitable for comparison.
    """

    return unicodedata.normalize("NFKC", str(name)).strip().lower()


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
        .loc[lambda s: s != ""]
        .tolist()
    )
    return {normalize_name(name) for name in names}


def drop_columns(src_df: pd.DataFrame, ref_norm: set[str]) -> pd.DataFrame:
    """Drop columns from `src_df` whose normalized names appear in `ref_norm`.

    Args:
        src_df: Source DataFrame.
        ref_norm: Set of normalized column names to drop.

    Returns:
        A new DataFrame with the specified columns removed.
    """

    src_cols = list(src_df.columns)
    col_norm_map = {col: normalize_name(col) for col in src_cols}
    matched_cols = [col for col in src_cols if col_norm_map[col] in ref_norm]
    return src_df.drop(columns=matched_cols, errors="ignore")


def main() -> None:
    """Main entry point for command-line execution."""
    src_file = Path("受入れ検査品リスト.xlsx")
    ref_file = Path("filtered_columns.xlsx")
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
    main()