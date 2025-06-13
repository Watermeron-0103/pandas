Delete only the specified data, str

```python
import pandas as pd


# read the Excel file
file_path = "before_arrival2025.6.16~/source/original/受入れ検査品リストVer1_2021.5.31  .xlsx"
old_file_path = "before_arrival2025.6.16~/source/original/受入れ検査品リストVer1_2021.5.31  (旧文書).xlsx"
save_path = "before_arrival2025.6.16~/source/inspection_list.xlsx"

df = pd.read_excel(file_path, sheet_name=0)
df_old = pd.read_excel(old_file_path, sheet_name=0)

# Data inspection deleted 00-000
df = df[df["文書番号"] != "PA-IP00-000"]
df_old = df_old[df_old["文書番号"] != "PA-IP00-000"]

df = df[df["認定"].isna()]
df_old = df_old[df_old["認定"].isna()]

with pd.ExcelWriter(save_path, engine='openpyxl', mode='a', if_sheet_exists="replace") as writer:
    df.to_excel(writer, sheet_name='certification_data_isp_del', index=False)
    df_old.to_excel(writer, sheet_name='certification_data_isp_del_old', index=False)
```

Extract only the specified values
```python
import pandas as pd


file_path = "受入れ検査品リスト.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

keep_list = ["PA-IP22-610", "PA-IP19-903"]
df = df[df["文書番号"].isin(keep_list)]
```
