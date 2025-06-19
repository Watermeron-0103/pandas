# Divide by the specified string

```python
# Get unique assignees in the 'Assignee' column
inspectors = df['記録者'].unique()

for inspector in inspectors:
    # Filter by agent
    df_inspector = df[df['記録者'] == inspector]
```

# +Create a folder for each one and store them

```python
import os
import pandas as pd


input_file = "Inspector/日報記録_YYYYMMDD.xlsx"
output_dir = "Inspector/by_inspector"

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

df = pd.read_excel(input_file)

# Get unique assignees in the 'Assignee' column
inspectors = df['記録者'].unique()

for inspector in inspectors:
    # Filter by agent
    df_inspector = df[df['記録者'] == inspector]
    # Change the file name to person_name.xlsx
    file_name = f"{inspector}.xlsx"
    # save
    df_inspector.to_excel(os.path.join(output_dir, file_name), index=False)

print("The Excel files for each inspector were saved in the by_inspector folder.")
```

```python
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
