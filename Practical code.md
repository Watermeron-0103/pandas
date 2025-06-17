
- 部品番号列が重複していて、さらにサプライヤ列が別々の部品を抽出
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

- 部品名称から指定した複数の値でジャンル分け
# Categorize parts by multiple values ​​specified from part names
  ```python
  import pandas as pd
  
  
  df = pd.read_excel("before_arrival2025.6.16~/compare_deli_isp_list.xlsx", sheet_name=0)
  
  keyword_list = ["Oリング", "ボタン軸", "カシメピン", "特殊止めねじ"]
  
  with pd.ExcelWriter("before_arrival2025.6.16~/compare_deli_isp_list.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
      for key in keyword_list:
          mask = df["名称"].astype(str).str.contains(key, na=False)
          filtered = df[mask].sort_values("名称")
          filtered.to_excel(writer, sheet_name=key, index=False)

  ```
