# Classification filterd
```Python
import os
import pandas as pd

# Excelファイルを読み込み
df = pd.read_excel("日報記録_YYYYMMDD.xlsx")

# 「検査種別」列でユニークな値を取得
validation_types = df['検査種別'].dropna().unique()

# 保存用ディレクトリ作成
output_dir = "validation_by_type"
os.makedirs(output_dir, exist_ok=True)

# 各「検査種別」の値ごとにフィルターしてExcel保存
for validation in validation_types:
    filtered_df = df[df['検査種別'] == validation]
    filename = f"{validation}.xlsx"
    # ファイル名に使えない文字を安全に置換
    safe_filename = filename.replace("/", "_").replace("\\", "_")
    # Excelファイルとして保存
    filtered_df.to_excel(os.path.join(output_dir, safe_filename), index=False)

print("検査種別ごとのExcelファイルを validation_by_type フォルダに保存しました。")
```
