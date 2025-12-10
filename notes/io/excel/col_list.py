from pathlib import Path
import pandas as pd


EXCEL_PATH = Path('src/受入れ検査品リスト_2025-12-09.xlsx')
OUT_PATH = Path('out/0-1_col_clean.xlsx')

df = pd.read_excel(EXCEL_PATH, sheet_name='検査計画書', header=0, dtype=str)

col_df = pd.DataFrame({"col": df.columns})

col_df.to_excel(OUT_PATH, index=False)