
部品番号列が重複していて、さらにサプライヤ列が別々の部品を抽出

# The part number column is duplicated, and the supplier column extracts different parts.
```python
import pandas as pd


df = pd.read_excel("受入れ検査品リスト_filtered.xlsx")

# 1. Count the number of different suppliers for each part number
supplier_counts = df.groupby('部品番号')['サプライヤ'].nunique()

# 2. Extract only part numbers with two or more suppliers
multi_supplier_parts = supplier_counts[supplier_counts > 1].index

# 3. Extract all lines for that part number
result = df[df["部品番号"].isin(multi_supplier_parts)]
```
