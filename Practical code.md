
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
    - **Sorted by part name**
    ```python
    import pandas as pd

    
    # 元Excelファイル
    file_path = "20250616_受入れ検査品リストVer1_2021.5.31  .xlsx"
    df = pd.read_excel(file_path, sheet_name=0)
    
    # ジャンル分け関数（部分一致）
    def assign_genre(name):
        if any(x in str(name) for x in ['取扱説明書', '取説', 'MANUAL', 'manual', 'マニュアル']):
            return '取扱説明書-マニュアル'
        elif 'Oリング' in str(name):
            return 'Oリング'
        elif any(x in str(name) for x in ['コネクタ', 'ケーブル']):
            return '電気部品'
        else:
            return 'その他'
    
    # ジャンル列を追加
    df['ジャンル'] = df['部品名称'].apply(assign_genre)
    
    # ジャンル分け後のExcelとして保存
    df.to_excel("ジャンル分け済_受入れ検査品リスト.xlsx", index=False)
    
    print("ジャンル分けして保存しました！")

    ```
    
    - **Sorted by part name + part number**
    ```python
    def assign_genre(row):
        name = str(row['部品名称'])
        part_no = str(row['部品番号'])
        supplire = str(row['サプライヤ'])
    
        if part_no.startswith(('897N', '058B', '202B')):
            return '取扱説明書-マニュアル, 機種銘板, ラベル'
        if part_no.startswith('006B'):
            return '光学部品'
        elif part_no.startswith('000Y'):
            return '滅菌部品'
        elif len(part_no) > 3 and part_no[3] in ('Y', 'A'):
            return 'ASSY部品'
        elif len(part_no) > 3 and part_no[3] in ('K', 'M', 'S'):
            return 'K,M,S部品'
        elif part_no.startswith(('001B', '002B', '007B', '600N')):
            return '光学部品'
        elif part_no.startswith(('096B', '96B', '491N')):
            return '梱包材'
        elif any(x in name for x in ['取扱説明書', '取説', 'MANUAL', 'manual', 'マニュアル', '銘板', 'ラベル']):
            return '取扱説明書-マニュアル, 機種銘板, ラベル'
        elif any(x in name for x in ['レンズ', 'プリズム', 'LG', '鏡胴']):
            return '光学部品'
        ------                     省略                     ------
        elif any(x in name for x in ['梱包材', '梱包資材', '梱包資材']):
            return '梱包材'
        elif any(x in name for x in ['ブラケット', 'Bracket', 'bracket', 'BRACKET', 'ブラケッ ト']):
            return '把持ケース'
        elif supplire.startswith('スズキ'):
            return '取扱説明書-マニュアル, 機種銘板, ラベル'
        else:
            return 'その他'
    
    df['ジャンル'] = df.apply(assign_genre, axis=1)    
    ```
    - When there are many categories
    ```python
    # ---- 辞書やリストで分類条件をまとめる ----
    # 部品番号によるジャンル分け（優先順に記述）
    part_no_starts = [
        (('897N', '058B', '202B'), '取扱説明書-マニュアル, 機種銘板, ラベル'),
        ('006B', '光学部品'),
        ('000Y', '滅菌部品'),
        (('001B', '002B', '007B', '600N'), '光学部品'),
        (('096B', '96B', '491N'), '梱包材'),
    ]
    # 4文字目で分けるパターン
    part_no_fourth = {
        ('Y', 'A'): 'ASSY部品',
        ('K', 'M', 'S'): 'K,M,S部品',
    }
    
    # 部品名称のキーワード辞書（優先順にリスト化）
    name_keywords = [
        (['取扱説明書', '取説', 'MANUAL', 'manual', 'マニュアル', '銘板', 'ラベル'], '取扱説明書-マニュアル, 機種銘板, ラベル'),
        (['レンズ', 'プリズム', 'LG', '鏡胴'], '光学部品'),
        (['Oリング', 'Seal', 'パッキン', 'O-RING', 'Ｏリング'], 'Oリング'),
        ------                     省略                     ------
        (['軸受け', '軸受'], '軸受'),
        (['ブラケット', 'Bracket', 'bracket', 'BRACKET', 'ブラケッ ト'], 'ブラケット'),
        (['把持ケース', 'Housing', 'housing'], '把持ケース'),
    ]
    
    # サプライヤーで分ける
    supplier_starts = [
        ('スズキ', '取扱説明書-マニュアル, 機種銘板, ラベル'),
        ('オスコ', 'チューブ'),
    ]
    
    def assign_genre(row):
        name = str(row.get('部品名称', ''))
        part_no = str(row.get('部品番号', ''))
        supplier = str(row.get('サプライヤ', ''))

        # 最初の文字がアルファベットなら副資材
        if part_no and part_no[0].isalpha():
            return '副資材, ネジ類, 梱包材'
    
        # 部品番号で先頭一致判定（優先順）
        for prefix, genre in part_no_starts:
            if isinstance(prefix, tuple):
                if part_no.startswith(prefix):
                    return genre
            else:
                if part_no.startswith(prefix):
                    return genre
    
        # 4文字目で判定
        if len(part_no) > 3:
            for chars, genre in part_no_fourth.items():
                if part_no[3] in chars:
                    return genre
    
        # 部品名称の部分一致判定
        for keywords, genre in name_keywords:
            if any(k in name for k in keywords):
                return genre
    
        # サプライヤで判定
        for supplier_prefix, genre in supplier_starts:
            if supplier.startswith(supplier_prefix):
                return genre
    
        return 'その他'
    
    df['ジャンル'] = df.apply(assign_genre, axis=1)
    ```
      
