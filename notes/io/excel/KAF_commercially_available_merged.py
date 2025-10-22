import re, unicodedata, datetime
from pathlib import Path
import pandas as pd

# ========== settings ==========
FILE_CA = "out/検収品一覧.xlsx"
SHEET_CA = "品目コード"   # ←シート名（例）

FILE_KAF = "src/KAF品目入荷場所.xlsx"
SHEET_KAF = "SQL Results" # ←シート名（例）

# 各ファイルの「品目コード」列名（実際の列名に合わせて変更）
CODE_COL_CA  = "品目コード"
CODE_COL_KAF = "品目コード"
# ==============================

def nfck(text: str) -> str:
    """Unicode NFKC 正規化"""
    return unicodedata.normalize('NFKC', text)

def normalize_part_code(s, drop_spaces=True, unify_dash=True, case="upper"):
    """部品No.揺れ吸収キー: 空白除去, ダッシュ統一, NFKC, 大文字化"""
    if s is None:
        return ""
    x = unicodedata.normalize("NFKC", str(s))
    x = x.replace("\u3000", " ").strip()
    x = re.sub(r"[\u00A0\u200B-\u200D\uFEFF]", "", x)
    if unify_dash:
        x = re.sub(r"[\u2212\u2010-\u2015\u2500\uFF0D]", "-", x)
    x = re.sub(r"\s+", "" if drop_spaces else " ", x)
    if case == "upper":
        x = x.upper()
    elif case == "lower":
        x = x.lower()
    return x

def load_excel(path: str, sheet: str) -> pd.DataFrame:
    """Excelを文字列主体で読み込み（先頭ゼロ保持のため）"""
    return pd.read_excel(path, sheet_name=sheet, dtype=str)

def add_norm_key(df: pd.DataFrame, code_col: str, key_col: str = "__norm_key__") -> pd.DataFrame:
    if code_col not in df.columns:
        raise KeyError(f"列 '{code_col}' が見つかりません。存在する列: {list(df.columns)}")
    df = df.copy()
    df[code_col] = df[code_col].fillna("")
    df[key_col] = df[code_col].map(normalize_part_code)
    return df

def build_summary(df_ca, df_kaf, matched_ca, matched_kaf, key_col="__norm_key__") -> pd.DataFrame:
    # 基本カウント
    ca_rows_all   = len(df_ca)
    kaf_rows_all  = len(df_kaf)
    ca_rows_keep  = len(matched_ca)
    kaf_rows_keep = len(matched_kaf)
    ca_rows_drop  = ca_rows_all - ca_rows_keep
    kaf_rows_drop = kaf_rows_all - kaf_rows_keep

    # ユニーク件数
    ca_unique_all   = df_ca[key_col].nunique(dropna=False)
    kaf_unique_all  = df_kaf[key_col].nunique(dropna=False)
    ca_unique_keep  = matched_ca[key_col].nunique(dropna=False)
    kaf_unique_keep = matched_kaf[key_col].nunique(dropna=False)

    # 左右のユニーク集合
    ca_set = set(df_ca[key_col])
    kaf_set = set(df_kaf[key_col])
    inter  = ca_set & kaf_set
    only_ca = ca_set - kaf_set
    only_kaf = kaf_set - ca_set

    rows = [
        ["行数（元）",                 ca_rows_all,  kaf_rows_all],
        ["行数（一致のみ残し）",       ca_rows_keep, kaf_rows_keep],
        ["行数（削除された行数）",     ca_rows_drop, kaf_rows_drop],
        ["ユニーク品目数（元）",       ca_unique_all,  kaf_unique_all],
        ["ユニーク品目数（一致のみ）", ca_unique_keep, kaf_unique_keep],
        ["一致ユニーク品目数（共通）", len(inter),   len(inter)],
        ["不一致ユニーク（左のみ）",   len(only_ca),  ""],
        ["不一致ユニーク（右のみ）",   "",            len(only_kaf)],
    ]
    return pd.DataFrame(rows, columns=["項目", "CA", "KAF"])

def main():
    # 1) 読み込み
    df_ca  = load_excel(FILE_CA,  SHEET_CA)
    df_kaf = load_excel(FILE_KAF, SHEET_KAF)

    # 2) 正規化キー付与
    df_ca  = add_norm_key(df_ca,  CODE_COL_CA)
    df_kaf = add_norm_key(df_kaf, CODE_COL_KAF)

    key = "__norm_key__"

    # 3) 共通キー集合
    common_keys = set(df_ca[key]) & set(df_kaf[key])

    # 4) 一致のみ残す（元の重複は維持）
    df_ca_keep  = df_ca[df_ca[key].isin(common_keys)].copy()
    df_kaf_keep = df_kaf[df_kaf[key].isin(common_keys)].copy()

    # 5) 不一致（参考: サマリー確認用）
    df_ca_drop  = df_ca[~df_ca[key].isin(common_keys)].copy()
    df_kaf_drop = df_kaf[~df_kaf[key].isin(common_keys)].copy()

    # 6) サマリー
    summary = build_summary(df_ca, df_kaf, df_ca_keep, df_kaf_keep, key_col=key)

    # 7) 出力
    out_dir = Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    out_path = out_dir / f"品目コード比較_{stamp}.xlsx"

    # エクスポート前に作業列を落とす
    def drop_key(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=[key], errors="ignore")

    with pd.ExcelWriter(out_path, engine="openpyxl") as xw:
        summary.to_excel(xw, sheet_name="サマリー", index=False)
        drop_key(df_ca_keep).to_excel(xw, sheet_name="CA_一致のみ", index=False)
        drop_key(df_kaf_keep).to_excel(xw, sheet_name="KAF_一致のみ", index=False)
        drop_key(df_ca_drop).to_excel(xw, sheet_name="CA_不一致", index=False)
        drop_key(df_kaf_drop).to_excel(xw, sheet_name="KAF_不一致", index=False)

    # 8) コンソールにも軽く表示
    print(f"出力: {out_path}")
    print(summary)

if __name__ == "__main__":
    main()
