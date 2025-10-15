import re
import unicodedata
import pathlib
import pandas as pd


# ===== settings =====
FUKLE_UKEI = "src/受入れ検査品リスト.xlsx"
SHEET_UKEI = "検査計画書"
COL_UKEI = "検収対象品"

OUTPUT_XLSX = "out/検収品一覧.xlsx"

# ===== functions =====


def nfkc(s) -> str:
    return unicodedata.normalize("NFKC", str(s)).strip()


def commercially_available_parts_list(debug: bool=False) -> list[str]:
    df = pd.read_excel(FUKLE_UKEI, sheet_name=SHEET_UKEI, usecols=[COL_UKEI])
    if debug: print("raw rows:", len(df))

    s = df[COL_UKEI].dropna().map(nfkc)   # NFKC + strip
    s = s[s.ne("")]                       # 空文字だけ除外
    parts = sorted(pd.unique(s))          # ユニーク + ソート

    if debug:
        print("after dropna/normalize:", len(s))
        print("unique parts:", len(parts))
    return list(parts)



def main():
    parts = commercially_available_parts_list()
    print(f"市販品リスト: {len(parts)}件")

    # Excel出力
    pathlib.Path("out").mkdir(exist_ok=True)
    df_out = pd.DataFrame(parts, columns=["品名"])
    df_out.to_excel(OUTPUT_XLSX, index=False)
    print(f"Excel出力: {OUTPUT_XLSX}")

if __name__ == "__main__":
    main()
