import re
import unicodedata
from pathlib import Path
import pandas as pd


# ===== settings =====
FILE_UKEI = "src/受入れ検査品リスト.xlsx"
SHEET_UKEI = "検査計画書"
COL_UKEI = "検収対象品"

OUTPUT_XLSX = "out/検収品一覧.xlsx"
OUTPUT_SHEET = "市販品一覧"

# ===== functions =====
def nfkc(s) -> str:
    return unicodedata.normalize("NFKC", str(s)).strip()

def commercially_available_parts_list(file_path: str) -> pd.DataFrame:
    """行形状はそのまま、検収対象品が“非空の文字列”の行のみ残す"""
    df = pd.read_excel(file_path, sheet_name=SHEET_UKEI)

    # NaN は空文字に、その他は必ず文字列化して正規化
    df["_norm"] = df[COL_UKEI].apply(lambda x: "" if pd.isna(x) else nfkc(x))

    # 非空のみ採用（"1" も 1 も通る）
    mask = df["_norm"].ne("")
    out = df.loc[mask].drop(columns=["_norm"]).copy()
    return out

def main():
    Path("out").mkdir(exist_ok=True)

    out_df = commercially_available_parts_list(FILE_UKEI)
    print(f"抽出: {len(out_df)} 行")

    # 期待形で書き出し（毎回クリーンに上書き）
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as w:
        out_df.to_excel(w, sheet_name=OUTPUT_SHEET, index=False)
    print(f"Excel出力 -> {OUTPUT_XLSX}（シート: {OUTPUT_SHEET}）")

if __name__ == "__main__":
    main()
