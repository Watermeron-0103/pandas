from pathlib import Path
import pandas as pd


EXCEL_PATH = Path("out/先端キャップ_抽出リスト.xlsx")
REF_PATH = Path("out/先端キャップ_可能.xlsx")

df = pd.read_excel(EXCEL_PATH, sheet_name=0, dtype=str)

ref_df = pd.read_excel(REF_PATH, sheet_name=0, dtype=str)

# 文書番号だけをユニークにしておくと重複マージを防げる
ref_key = ref_df[["文書番号"]].drop_duplicates()

df_joined = df.merge(
    ref_key,
    how="left",
    on=["文書番号"],
    indicator=True,      # ★ どこから来たかフラグ列 _merge を付ける
)

# _merge の内容： 'both' = 両方にいる, 'left_only' = dfにだけいる
df_joined["可能フラグ"] = df_joined["_merge"].map({
    "both": "可能",       # ref_df にもいたやつ
    "left_only": "対象外", # ref_df にはいなかったやつ
})

OUT_PATH = Path("out/先端キャップ_抽出リスト_可能.xlsx")

df_joined.to_excel(OUT_PATH, index=False)
