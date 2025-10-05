#!/usr/bin/env python3
"""
clean_columns.py

This script reads an Excel workbook and removes columns based on a list of
column names specified in another Excel file.

Usage example:
    python clean_columns.py \
        --input_file 受入れ検査品リスト.xlsx \
        --drop_list カラム名一覧.xlsx \
        --output_file 受入れ検査品リスト_trimmed.xlsx \
        --report_file 削除レポート.xlsx

The drop list file should contain the column names to drop in the first column
of the first sheet.  Column names are normalized before matching by
converting to NFKC form, stripping whitespace, and converting to lower case.

The script writes two output files: one containing the trimmed workbook and
another containing a report of what was dropped and what could not be found.
"""

import argparse
from pathlib import Path
import unicodedata

import pandas as pd


def normalize(name: str) -> str:
    """Normalize a column name for comparison.

    This helper function ensures that small differences in encoding or
    whitespace do not prevent a match.  It performs Unicode NFKC
    normalization, trims leading and trailing whitespace, and lowers the
    case of alphabetic characters.

    Args:
        name: The original column name.

    Returns:
        A normalized string suitable for matching.
    """
    return unicodedata.normalize("NFKC", str(name)).strip().lower()


def load_drop_list(path: Path) -> list[str]:
    """Load and normalize the list of column names to drop from a workbook.

    The drop list is expected to reside in the first column of the
    first sheet of the Excel file.  Empty or blank cells are ignored.

    Args:
        path: Path to the Excel file containing the drop list.

    Returns:
        A list of normalized column names to remove.
    """
    drop_df = pd.read_excel(path, dtype=str, header=0)
    candidates = []
    for value in drop_df.iloc[:, 0].dropna().tolist():
        text = str(value).strip()
        if text:
            candidates.append(normalize(text))
    return candidates


def drop_columns_with_report(df: pd.DataFrame, drops_norm: list[str]):
    """Remove columns from a DataFrame and produce a report.

    For each column in the DataFrame, a normalized key is computed using
    ``normalize``.  The function then determines which requested drop
    names exist in the DataFrame and which do not.  Matching columns
    are removed, and a report dictionary summarizing the results is
    returned.

    Args:
        df: Input DataFrame from which to remove columns.
        drops_norm: List of normalized column names requested for removal.

    Returns:
        A tuple (trimmed_df, report) where ``trimmed_df`` is the DataFrame
        after removal and ``report`` is a dictionary with details about
        the operation.
    """
    # Build a mapping of normalized names to their original names.
    norm_map: dict[str, str] = {}
    for col in df.columns:
        key = normalize(col)
        if key not in norm_map:
            norm_map[key] = col

    # Determine which normalized names exist in the DataFrame
    existing_norm = set(norm_map.keys())
    to_drop_norm = [d for d in drops_norm if d in existing_norm]
    not_found_norm = [d for d in drops_norm if d not in existing_norm]

    # Map normalized names back to original column names
    to_drop_original = [norm_map[n] for n in to_drop_norm]

    # Perform the actual drop
    trimmed = df.drop(columns=to_drop_original, errors="ignore")

    # Build report
    report = {
        "columns_before_count": len(df.columns),
        "columns_after_count": len(trimmed.columns),
        "dropped_count": len(to_drop_original),
        "not_found_count": len(not_found_norm),
        "dropped_columns_original": to_drop_original,
        "not_found_columns_requested": not_found_norm,
    }

    return trimmed, report


def main(args: argparse.Namespace) -> None:
    """Execute the column-drop workflow across all sheets in a workbook.

    Args:
        args: Parsed command-line arguments specifying input/output paths.
    """
    input_file = Path(args.input_file)
    drop_file = Path(args.drop_list)
    output_file = Path(args.output_file)
    report_file = Path(args.report_file)

    # Load the list of normalized drop candidates
    drop_candidates = load_drop_list(drop_file)

    # Read all sheets from the input workbook
    xls = pd.ExcelFile(input_file)
    out_sheets = {}
    reports = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=object)
        trimmed_df, report = drop_columns_with_report(df, drop_candidates)
        out_sheets[sheet_name] = trimmed_df
        reports[sheet_name] = report

    # Write the trimmed workbook
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for sheet_name, df in out_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Write the report workbook
    with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
        # Summary sheet
        summary = pd.DataFrame([
            {
                "シート名": name,
                "削除前": rpt["columns_before_count"],
                "削除後": rpt["columns_after_count"],
                "削除数": rpt["dropped_count"],
                "未検出数": rpt["not_found_count"],
            }
            for name, rpt in reports.items()
        ])
        summary.to_excel(writer, sheet_name="サマリー", index=False)

        # Detail sheets per input sheet
        for name, rpt in reports.items():
            pd.DataFrame({"削除したカラム": rpt["dropped_columns_original"]}).to_excel(
                writer, sheet_name=f"{name}_削除", index=False
            )
            pd.DataFrame({"未検出（正規化名）": rpt["not_found_columns_requested"]}).to_excel(
                writer, sheet_name=f"{name}_未検出", index=False
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove columns from an Excel file based on a drop list."
    )
    parser.add_argument(
        "--input_file",
        required=True,
        help="Path to the Excel file to process (e.g., 受入れ検査品リスト.xlsx)",
    )
    parser.add_argument(
        "--drop_list",
        required=True,
        help="Path to the Excel file containing names of columns to drop (first column)",
    )
    parser.add_argument(
        "--output_file",
        required=True,
        help="Output path for the trimmed Excel workbook",
    )
    parser.add_argument(
        "--report_file",
        required=True,
        help="Output path for the report workbook",
    )
    main(parser.parse_args())
