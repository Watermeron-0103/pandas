#!/usr/bin/env python3
"""
filtered_columns_script.py
==========================

This script reads `受入れ検査品リスト.xlsx` and `filtered_columns.xlsx`,
normalizes their column names (full-width/half-width, leading/trailing
whitespace, and case differences), and produces two output files:

1. A version of the source where all columns that match names in the
   reference list have been removed (pattern1).
2. A version of the source where only columns not found in the reference
   list remain (pattern2).

The two results are effectively identical, but both are output for
clarity.

Place this script in the same directory as the two input Excel files and run
it with a Python interpreter. The output files will be written to the
current directory with names beginning with `pattern1_` and `pattern2_`.

--- 日本語訳 ---
本スクリプトは `受入れ検査品リスト.xlsx` と `filtered_columns.xlsx` を読み込み、
列名を正規化（全角/半角の統一、前後の空白の除去、大小文字の差異の吸収）したうえで、
次の 2 種類の出力ファイルを作成します。

1. 参照リストの列名と一致する列をすべて削除した版（pattern1）。
2. 参照リストに存在しない列のみを残した版（pattern2）。

両者の結果は実質的に同一ですが、意図を明確にするため両方を出力します。

使い方：
このスクリプトを 2 つの入力 Excel ファイルと同じディレクトリに置き、Python で実行してください。
出力ファイルはカレントディレクトリに `pattern1_` および `pattern2_` で始まる名前で保存されます。
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
    first non‑empty column contains the names of columns to remove or
    keep. Empty rows are ignored.

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


def process_files(src_path: Path, ref_path: Path, out_dir: Path) -> tuple[Path, Path]:
    """Process the source and reference files and write pattern outputs.

    Args:
        src_path: Path to the source Excel file.
        ref_path: Path to the reference Excel file.
        out_dir: Directory where output files will be written.

    Returns:
        A tuple containing the paths to the pattern1 and pattern2 output files.
    """

    src_df = pd.read_excel(src_path, header=0, dtype=object)
    ref_norm = load_reference_names(ref_path)

    src_cols = list(src_df.columns)
    col_norm_map = {col: normalize_name(col) for col in src_cols}

    # Determine which columns match the reference list.
    matched_cols = [col for col in src_cols if col_norm_map[col] in ref_norm]
    mismatched_cols = [col for col in src_cols if col_norm_map[col] not in ref_norm]

    # Pattern 1: drop columns that matched (keep mismatched).
    pattern1_df = src_df.drop(columns=matched_cols, errors="ignore")
    # Pattern 2: keep columns that mismatched.
    pattern2_df = src_df[mismatched_cols]

    # Prepare output file names.
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern1_path = out_dir / f"pattern1_{src_path.stem}_参照に一致する列を削除.xlsx"
    pattern2_path = out_dir / f"pattern2_{src_path.stem}_参照に無い列だけ.xlsx"

    with pd.ExcelWriter(pattern1_path, engine="openpyxl") as writer:
        pattern1_df.to_excel(writer, index=False)
    with pd.ExcelWriter(pattern2_path, engine="openpyxl") as writer:
        pattern2_df.to_excel(writer, index=False)

    return pattern1_path, pattern2_path


def main() -> None:
    """Main entry point when run from the command line."""

    src_file = Path("受入れ検査品リスト.xlsx")
    ref_file = Path("filtered_columns.xlsx")
    out_dir = Path(".")

    if not src_file.exists():
        raise FileNotFoundError(f"Source file not found: {src_file}")
    if not ref_file.exists():
        raise FileNotFoundError(f"Reference file not found: {ref_file}")

    pattern1, pattern2 = process_files(src_file, ref_file, out_dir)
    print(f"Pattern1 output written to: {pattern1}")
    print(f"Pattern2 output written to: {pattern2}")


if __name__ == "__main__":
    main()