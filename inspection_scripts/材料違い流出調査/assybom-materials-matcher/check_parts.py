#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
材料確認品目.xlsx(単品/品目(Ver無)) と ASSYBOM.xlsx(部品No.) の照合
出力:
  1_材料(単品)+assemblyフラグ … 材料の“元データのまま”末尾に True/False
  2_ASSYBOM+材料フラグ         … ASSYBOM 側にも True/False
  3_照合結果                   … サマリー＋ユニオン（両方/片側のみ）
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd

# ====== 設定（必要に応じて書き換え可） ======
FILE_MAT = "材料確認品目.xlsx"    # 軸
SHEET_MAT = "単品"
COL_MAT = "品目(Ver無)"

FILE_ASSY = "ASSYBOM.xlsx"
COL_ASSY = "部品No."

OUTPUT_XLSX = "材料ASSYBOM_照合_3出力.xlsx"
# ========================================


def nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def clean_header_token(x) -> str:
    """列名どうしの比較用に NFKC + 空白除去 + 大文字化"""
    if pd.isna(x):
        return ""
    s = nfkc(str(x)).strip()
    return re.sub(r"\s+", "", s).upper()


def normalize_key(x) -> str | None:
    """照合キーの正規化（全角→半角、空白除去、各種ダッシュ統一、英字大文字化）"""
    if pd.isna(x):
        return None
    s = nfkc(str(x)).strip()
    s = re.sub(r"\s+", "", s)
    s = (
        s.replace("‐", "-")
        .replace("－", "-")
        .replace("―", "-")
        .replace("—", "-")
        .replace("ー", "-")
    ).upper()
    return s if s else None


def read_with_header_detection_df(df_raw: pd.DataFrame, expected_col: str | None = None) -> pd.DataFrame:
    """シート内でヘッダ行が上部以外にある場合に、expected_col が含まれる行をヘッダとして採用"""
    expected_norm = clean_header_token(expected_col) if expected_col else None
    header_row_idx = None
    if expected_norm:
        for i in range(len(df_raw)):
            row_norm = [clean_header_token(v) for v in df_raw.iloc[i].tolist()]
            if expected_norm in row_norm:
                header_row_idx = i
                break
    if header_row_idx is None:
        header_row_idx = 0  # フォールバック

    header_vals = [("" if pd.isna(v) else str(v)) for v in df_raw.iloc[header_row_idx].tolist()]
    df = df_raw.iloc[header_row_idx + 1 :].copy()
    df.columns = [v.strip() for v in header_vals]
    # 文字列扱いに統一
    for c in df.columns:
        try:
            df[c] = df[c].astype(str)
        except Exception:
            pass
    return df


def read_with_header_detection(path: Path, sheet_name=None, expected_col: str | None = None) -> pd.DataFrame:
    """
    sheet_name が None なら全シート探索して expected_col を含むヘッダ行が見つかったシートを優先採用。
    """
    if sheet_name is not None:
        df_raw = pd.read_excel(path, sheet_name=sheet_name, header=None, dtype=str)
        return read_with_header_detection_df(df_raw, expected_col=expected_col)
    else:
        sheets = pd.read_excel(path, sheet_name=None, header=None, dtype=str)
        for _, df_raw in sheets.items():
            try:
                df = read_with_header_detection_df(df_raw, expected_col=expected_col)
                mapping = {c: clean_header_token(c) for c in df.columns}
                if clean_header_token(expected_col) in mapping.values():
                    return df
            except Exception:
                continue
        # 見つからなければ最初のシートで
        first_df = next(iter(sheets.values()))
        return read_with_header_detection_df(first_df, expected_col=expected_col)


def find_column(df: pd.DataFrame, target_name: str) -> str:
    """列名のゆらぎ（全角/半角/空白/大小）に強い一致"""
    target_norm = clean_header_token(target_name)
    mapping = {c: clean_header_token(c) for c in df.columns}
    # 完全一致
    for orig, normed in mapping.items():
        if normed == target_norm:
            return orig
    # 部分一致（例：VER無 を含む）
    for orig, normed in mapping.items():
        if target_norm in normed:
            return orig
    raise KeyError(f"列 {target_name} が見つかりません。実際: {list(df.columns)}")


def main():
    base = Path(".")
    file_mat = base / FILE_MAT
    file_assy = base / FILE_ASSY

    if not file_mat.exists():
        raise FileNotFoundError(file_mat)
    if not file_assy.exists():
        raise FileNotFoundError(file_assy)

    # --- 読み込み ---
    # 材料（軸）：単品シートで expected_col をヘッダ検出
    mat_df = read_with_header_detection(file_mat, sheet_name=SHEET_MAT, expected_col=COL_MAT)
    # ASSYBOM：全シート探索で expected_col をヘッダ検出
    assy_df = read_with_header_detection(file_assy, sheet_name=None, expected_col=COL_ASSY)

    # --- 列の特定 ---
    col_mat = find_column(mat_df, COL_MAT)
    col_assy = find_column(assy_df, COL_ASSY)

    # --- 正規化キー作成 ---
    mat_df["_key"] = mat_df[col_mat].apply(normalize_key)
    assy_df["_key"] = assy_df[col_assy].apply(normalize_key)

    # --- ユニーク化（重複件数と原文サンプルも把握） ---
    mat_g = (
        mat_df.groupby("_key", dropna=True)
        .agg(mat_count=(col_mat, "size"), mat_sample=(col_mat, "first"))
        .reset_index()
    )
    assy_g = (
        assy_df.groupby("_key", dropna=True)
        .agg(assy_count=(col_assy, "size"), assy_sample=(col_assy, "first"))
        .reset_index()
    )

    mat_keys = set(mat_g["_key"])
    assy_keys = set(assy_g["_key"])

    # ===== 1) 材料→ASSYBOM：材料“単品”元データに assemblyフラグを付ける（元列はそのまま） =====
    materials_with_flag = mat_df.drop(columns=["_key"]).copy()
    materials_with_flag["assemblyフラグ"] = mat_df["_key"].apply(
        lambda k: (k in assy_keys) if k is not None else False
    )

    # ===== 2) ASSYBOM→材料：ASSYBOM 元データに 材料フラグ を付ける =====
    assy_with_flag = assy_df.drop(columns=["_key"]).copy()
    assy_with_flag["材料フラグ"] = assy_df["_key"].apply(
        lambda k: (k in mat_keys) if k is not None else False
    )

    # ===== 3) 照合結果（サマリー＋ユニオン） =====
    all_keys = pd.DataFrame({"_key": sorted(mat_keys.union(assy_keys))})
    union = all_keys.merge(mat_g, on="_key", how="left").merge(assy_g, on="_key", how="left")

    union["in_材料確認品目"] = ~union["mat_count"].isna()
    union["in_ASSYBOM"] = ~union["assy_count"].isna()

    def status_row(row):
        if row["in_材料確認品目"] and row["in_ASSYBOM"]:
            return "完全一致（両方に存在）"
        if row["in_材料確認品目"] and not row["in_ASSYBOM"]:
            return "材料のみ"
        if not row["in_材料確認品目"] and row["in_ASSYBOM"]:
            return "ASSYBOMのみ"
        return "不明"

    union["status"] = union.apply(status_row, axis=1)

    union_view = union[[
        "_key","status","in_材料確認品目","mat_count","mat_sample",
        "in_ASSYBOM","assy_count","assy_sample"
    ]].rename(columns={
        "_key": "照合キー（正規化）",
        "mat_count": "材料内件数",
        "mat_sample": "材料側サンプル値",
        "assy_count": "ASSYBOM内件数",
        "assy_sample": "ASSYBOM側サンプル値",
    })

    summary = pd.DataFrame({
        "項目": [
            "材料のユニーク件数",
            "ASSYBOMのユニーク件数",
            "完全一致の件数",
            "材料のみの件数",
            "ASSYBOMのみの件数",
        ],
        "値": [
            len(mat_keys),
            len(assy_keys),
            int((union_view["status"] == "完全一致（両方に存在）").sum()),
            int((union_view["status"] == "材料のみ").sum()),
            int((union_view["status"] == "ASSYBOMのみ").sum()),
        ]
    })

    # --- Excel 出力 ---
    try:
        writer = pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter")
    except Exception:
        writer = pd.ExcelWriter(OUTPUT_XLSX)  # openpyxl など

    with writer as w:
        materials_with_flag.to_excel(w, sheet_name="1_材料(単品)+assemblyフラグ", index=False)
        assy_with_flag.to_excel(w, sheet_name="2_ASSYBOM+材料フラグ", index=False)
        summary.to_excel(w, sheet_name="3_照合結果", index=False, startrow=0)
        union_view.to_excel(w, sheet_name="3_照合結果", index=False, startrow=len(summary) + 3)

    print(f"出力しました -> {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
