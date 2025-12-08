from pathlib import Path
import pandas as pd

# ① path を読み込む
EXCEL_PATH = Path("src/受入れ検査品リストVer1_2021.5.31  .xlsx")
REF_PATH = r"c:\Users\11064667.FFWIN\Documents\Mike-Tython\pandapandapanda\Hitman\受入情報分析\drop_col_UKEI\filtered_columns.xlsx"

# ② Excelファイルを読み込む
df = pd.read_excel(EXCEL_PATH, sheet_name=0)
ref_df = pd.read_excel(REF_PATH, sheet_name=0)

# ③ リストから「削除したい列名」の一覧を作る
drop_cols = drop_list_df["カラム名"].dropna().tolist()

# ④ 本体からそのカラムたちを削除する
df_after = df.drop(columns=drop_cols, errors='ignore')

# ⑤ 新しい名前をつけてExcelに保存
out_path = "out/受入れ検査品リスト_削除後.xlsx"
df_after.to_excel(out_path, index=False)

print("削除前の列:", list(df.columns))
print("削除後の列:", list(df_after.columns))
print("保存しました →", out_path)