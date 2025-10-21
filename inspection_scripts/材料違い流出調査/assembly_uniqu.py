import re, unicodedata
from pathlib import Path
import pandas as pd


# ====== settings ======
FILE_MA = "材料ASSYBOM_照合_3出力.xlsx"
SHEET_MAT = "1_材料(単品)+assemblyフラグ"
SHEET_ASSY = "2_ASSYBOM+材料フラグ"
COL_MAT = "部品No."
COL_ASSY = "部品No."

OUT_FILE   = "材料ASSYBOM_照合_3出力_ユニーク付与.xlsx"
# ======================

def normalize_part_code(s, drop_spaces=True, unify_dash=True, case="upper"):
    if s is None:
        return ""
    x = unicodedata.normalize("NFKC", str(s))
    x = x.replace("\u3000", " ").strip()                           # 全角空白→半角、前後スペース除去
    x = re.sub(r"[\u00A0\u200B-\u200D\uFEFF]", "", x)              # NBSP/ゼロ幅除去
    if unify_dash:
        x = re.sub(r"[\u2212\u2010-\u2015\u2500\uFF0D]", "-", x)   # 各種ダッシュ→'-'
    x = re.sub(r"\s+", "" if drop_spaces else " ", x)              # 空白：削除（あなたの仕様）
    if case == "upper":
        x = x.upper()
    elif case == "lower":
        x = x.lower()
    return x


def mark_unique(path, sheet, col, seen_global: set):
    df = pd.read_excel(path, sheet_name=sheet, dtype=object)
    key = df[col].map(lambda v: normalize_part_code(v))

    # シート内で最初の出現だけ True
    df["ユニーク_シート内"] = ~key.duplicated(keep="first")

    # ファイル全体（シート横断）で最初の出現だけ True
    flags = []
    for k in key:
        if not k:                      # 空欄は False（必要なら pd.NA にしてもOK）
            flags.append(False)
        elif k in seen_global:
            flags.append(False)
        else:
            seen_global.add(k)
            flags.append(True)
    df["ユニーク_全体"] = flags

    # デバッグ用に正規化キーを残す（最終出力で不要なら drop 可）
    df["正規化キー"] = key
    return df

seen = set()
df_mat  = mark_unique(FILE_MA, SHEET_MAT,  COL_MAT,  seen)
df_assy = mark_unique(FILE_MA, SHEET_ASSY, COL_ASSY, seen)

with pd.ExcelWriter(OUT_FILE, engine="openpyxl") as w:
    df_mat.to_excel(w,  sheet_name=SHEET_MAT,  index=False)
    df_assy.to_excel(w, sheet_name=SHEET_ASSY, index=False)