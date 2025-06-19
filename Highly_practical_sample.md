# 

What I want to do

**１．品目コード列でマージ（＝一致する行のみ抽出）**

**２．そのうえで「df_isp」のCP列と、「df_flag」のBECPBACA列を比べて一致していない行だけを抽出したい**

```Python
import pandas as pd


# ファイル読み込み
df_isp = pd.read_excel(isp_path, sheet_name=0)
df_flag = pd.read_excel(flag_path, sheet_name=0)

# 品目コードでマージ（品目コードが一致するもののみ）
df_merged = pd.merge(df_isp, df_flag, on='品目コード', how='inner', suffixes=('_isp', '_flag'))

# さらにCP列とBECPBACA列が「一致していない」行だけ抽出
df_not_equal = df_merged[df_merged['CP'] != df_merged['BECPBACA']]
```
