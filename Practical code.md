
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
    import pandas as pd
    
    
    file_path = "Classification_of_part_number/inner_join_result.xlsx"
    df = pd.read_excel(file_path, sheet_name=0)
    
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
        elif any(x in name for x in ['Oリング', 'Seal', 'パッキン', 'O-RING', 'Ｏリング']):
            return 'Oリング'
        elif any(x in name for x in ['先端本体']):
            return '先端本体'
        elif any(x in name for x in ['先端キャップ', '先端キ ャップ']):
            return '先端キャップ'
        elif any(x in name for x in ['ノズル']):
            return 'ノズル'
        elif any(x in name for x in ['鉗子栓', '鉗子栓']):
            return '鉗子栓'
        elif any(x in name for x in ['カシメピン']):
            return 'カシメピン'
        elif any(x in name for x in ['ピン', 'Pin, pin', 'PIN', '針']):
            return 'ピン'
        elif any(x in name for x in ['アングルゴム', 'ﾁｭｰﾌﾞ', 'チューブ', 'FCT-', 'Tube', 'パイプ', '管', 'pipe', 'tube', 'TUBE', 'hose', 'Hose']):
            return 'チューブ'
        elif any(x in name for x in ['IG軟性部']):
            return 'IG軟性部金物'
        elif any(x in name for x in ['コネクタ', 'ケーブル', '基板', 'CHA', 'ヒューズ']):
            return 'エレキ部品'
        elif any(x in name for x in ['バルーン', 'ﾊﾞﾙｰﾝ']):
            return '滅菌部品'
        elif any(x in name for x in ['ネジ', 'ナット', 'ボルト', 'ねじ', '座金', 'ワッシャー', 'ねじ類', 'ネジ類', 'ネジ類', 'ネジ類', 'ネジ類', 'ネジ類']):
            return 'ねじ類'
        elif any(x in name for x in ['スプリング', 'バネ', 'ばね', 'spring', 'SPRING']):
            return 'スプリング'
        elif any(x in name for x in ['軸受け', '軸受']):
            return '軸受'
        elif any(x in name for x in ['絶縁ブッシュ', '軸受']):
            return '絶縁ブッシュ'
        elif any(x in name for x in ['鉗子爪']):
            return '鉗子爪'
        elif any(x in name for x in ['リング', 'リング', 'RING', 'ring']):
            return 'リング'
        elif any(x in name for x in ['ナイフ']):
            return 'ナイフ'
        elif any(x in name for x in ['押さえ環']):
            return '押さえ環'
        elif any(x in name for x in ['スリーブ']):
            return 'スリーブ'
        elif any(x in name for x in ['ワイヤ', 'ワイヤー', 'wire', 'WIRE']):
            return 'ワイヤ'
        elif any(x in name for x in ['バルブ', 'Valve', 'valve']):
            return 'バルブ'
        elif any(x in name for x in ['電磁波吸収シート', '電磁波吸収']):
            return '電磁波吸収シート'
        elif any(x in name for x in ['口金', '口金']):
            return '口金'
        elif any(x in name for x in ['ラカン']):
            return 'ラカン'
        elif any(x in name for x in ['フード', 'フード']):
            return 'フード'
        elif any(x in name for x in ['先端ゴムキャップ']):
            return '先端ゴムキャップ'
        elif any(x in name for x in ['梱包材', '梱包資材', '梱包資材']):
            return '梱包材'
        elif any(x in name for x in ['ブラケット', 'Bracket', 'bracket', 'BRACKET', 'ブラケッ ト']):
            return 'ブラケット'
        elif any(x in name for x in ['把持ケース', 'Housing', 'housing']):
            return '把持ケース'
        elif supplire.startswith('スズキ'):
            return '取扱説明書-マニュアル, 機種銘板, ラベル'
        else:
            return 'その他'
    
    df['ジャンル'] = df.apply(assign_genre, axis=1)
    
    df.to_excel("Classification_of_part_number/ジャンル分け済_受入れ検査品リスト.xlsx", index=False)
    print("ジャンル分けして保存しました！")

    ```
