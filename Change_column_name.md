#Check the columns and change them
How to check a column
```
import pandas as pd


file_path = "受入れ検査品リスト.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

# check column
print(df.columns)

# If you want to get the column names in a list:
print(df.columns.to_list())

# Rename columns in a DataFrame
df.columns = ['新しいカラム1', '新しいカラム2', ...]

# Rename specific columns using a dictionary
df = df.rename(columns={'部品番号\nPart number': '部品番号'})

# You can also make multiple changes at the same time.
df = df.rename(columns={'名称\nPart name': '名称', '文書番号\nDocument number': '文書番号'})

# Directly modify the original DataFrame with inplace=True
df.rename(columns={'種類 Type\n  クリティカル    Critical\n  非クリティカル Non-Critical': '種類'}, inplace=True)
```

