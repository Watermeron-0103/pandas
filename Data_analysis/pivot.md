# Visualize trends with cross tabulation (pivot)
```python
import pandas as pd

df = pd.read_excel("データ検査.xlsx")

# 必要に応じて「不良数」を数値型に変換
df["不良数"] = pd.to_numeric(df["不良数"], errors="coerce").fillna(0).astype(int)

# ピボットで「品目コード×サプライヤー×不良カテゴリ」ごとの不良数
pivot = pd.pivot_table(df, 
    index=["品目コード", "サプライヤー"], 
    columns="不良カテゴリ", 
    values="不良数", 
    aggfunc="sum",
    fill_value=0
)

print(pivot)
```
