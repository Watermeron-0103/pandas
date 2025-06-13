#How to check a column

```
import pandas as pd


file_path = "受入れ検査品リスト.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

# check column
print(df.columns())

# If you want to get the column names in a list:
print(df.columns.to_list())
```
