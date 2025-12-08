from pathlib import Path
import pandas as pd

# 元のExcelファイル
EXCEL_PATH = Path("out/受入れ検査品リスト_削除後.xlsx")

# 部品名称の列名（実際のヘッダー名に合わせてね）
COL_NAME = "部品名称"   # 例: "品名" とかならそこに変える

# ヘッダー行が2行目にあるなら header=1 とかにする
df = pd.read_excel(EXCEL_PATH, sheet_name=0, header=1, dtype=str)

# 「部品名称」に「先端キャップ」を含む行だけTrueになるマスク
mask = df[COL_NAME].str.contains("先端キャップ", na=False)

# マスクでフィルタ（コピーしておくと安心）
sentan_df = df[mask].copy()

print(f"ヒット件数: {len(sentan_df)} 件")

# 結果を別ファイルに出力
OUT_PATH = Path("out/先端キャップ_抽出リスト.xlsx")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
sentan_df.to_excel(OUT_PATH, index=False)

print(f"抽出結果を保存しました → {OUT_PATH}")
