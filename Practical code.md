
# The part number column is duplicated, and the supplier column extracts different parts.
  - 部品番号列が重複していて、さらにサプライヤ列が別々の部品を抽出
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


# Categorize parts by multiple values ​​specified from part names
  - 部品名称から指定した複数の値でジャンル分け
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

# If there are too many part names, you can also automatically classify them using partial matching (keyword-based).
**[新column追加version]**
  - 部分一致で高度なジャンル分け[新column追加version]
    ```python
    import pandas as pd
    
    
    file_path = "20250616_受入れ検査品リストVer1_2021.5.31  .xlsx"
    df = pd.read_excel(file_path, sheet_name=0)
    
    def assign_genre(name):
        if any(x in name for x in ['取扱説明書', '取説', 'MANUAL', 'manual', 'マニュアル']):
            return '取扱説明書-マニュアル'
        elif any(x in name for x in ['Oリング', 'Oリング']):
            return 'Oリング'
        elif any(x in name for x in ['コネクタ', 'ケーブル']):
            return '電気部品'
        else:
            return 'その他'
    
    df['ジャンル'] = df['部品名称'].apply(assign_genre)
    
    df.to_excel("ジャンル分け済_受入れ検査品リスト.xlsx", index=False)
    print("ジャンル分けして保存しました！")
    ```
