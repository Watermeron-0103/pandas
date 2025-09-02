## １．整理したテキスト（内容まとめ）

### 1. 記録者（担当者）ごとにファイルを分割

```python
import os
import pandas as pd

input_file = "Inspector/日報記録_YYYYMMDD.xlsx"
output_dir = "Inspector/by_inspector"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_excel(input_file)

# 記録者ごとにExcel保存
inspectors = df['記録者'].unique()
for inspector in inspectors:
    df_inspector = df[df['記録者'] == inspector]
    file_name = f"{inspector}.xlsx"
    df_inspector.to_excel(os.path.join(output_dir, file_name), index=False)

print("記録者ごとのExcelファイルを by_inspector フォルダに保存しました。")
```

---

### 2. 検査種別ごとにファイルを分割

```python
import os
import pandas as pd

df = pd.read_excel("日報記録_YYYYMMDD.xlsx")
validation_types = df['検査種別'].dropna().unique()

output_dir = "validation_by_type"
os.makedirs(output_dir, exist_ok=True)

for validation in validation_types:
    filtered_df = df[df['検査種別'] == validation]
    safe_filename = str(validation).replace("/", "_").replace("\\", "_")
    filtered_df.to_excel(os.path.join(output_dir, f"{safe_filename}.xlsx"), index=False)

print("検査種別ごとのExcelファイルを validation_by_type フォルダに保存しました。")
```

---

### 3. 検査種別ごとにシート分割（1ファイルにまとめる）

```python
import pandas as pd

df = pd.read_excel("日報記録_YYYYMMDD.xlsx")
validation_types = df['検査種別'].dropna().unique()

output_file = "検査種別ごと分割.xlsx"

with pd.ExcelWriter(output_file) as writer:
    for validation in validation_types:
        filtered_df = df[df['検査種別'] == validation]
        sheet_name = str(validation)[:31].replace("/", "_").replace("\\", "_")
        filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"検査種別ごとにシートを分けたExcelファイルを {output_file} に保存しました。")
```
