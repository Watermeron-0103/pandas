# How to use merge

- Extract items with matching on = "document number" in merge
    ```Python
    import pandas as pd
    
    # ファイル読み込み
    df_doc = pd.read_excel('Inspection_man-hours/Extract_matching_doc_num.xlsx')
    df_target = pd.read_excel('Man-hours_per_person/Classification/抜取検査.xlsx')
    
    # doc_num列と文書番号列の一致でinner join
    df_matched = pd.merge(df_doc, df_target, on='文書番号', how='inner')
    
    # 結果を保存
    df_matched.to_excel('Man-hours_per_person/Divide_by_person_in_charge.xlsx', index=False)
    
    print(df_matched.head())

    ```
  - *how='inner' は、pandas の merge や join で「内部結合（inner join）」を指定するための引数です。*

- Extract items with matching on = "document number" in merge
    ```Python
    file1 = "Classification_of_part_number/src/受入れ検査品リスト_列削除済.xlsx"
    file2 = "Inspection_man-hours/Extract_matching_doc_num.xlsx"
    df1 = pd.read_excel(file1, sheet_name=0)
    df2 = pd.read_excel(file2, sheet_name=1)
    
    # Merge df1 and df2 on '部品番号' and '部品番号_2'
    merged_df = pd.merge(df1, df2, on='文書番号', how='left')
    ```
  - *how='left' は、pandas の merge や join で「左外部結合（left join）」を指定するための引数です。*

- Example of using merge *[full code]*
    ```PYTHON
    import pandas as pd
    
    isp_path = '受入れ検査品リスト.xlsx'
    flag_path = '重要部品フラグ.xlsx'
    
    # ファイル読み込み
    df_isp = pd.read_excel(isp_path, sheet_name=0)
    df_flag = pd.read_excel(flag_path, sheet_name=0)
    
    # 品目コードでマージ（品目コードが一致するもののみ）
    df_merged = pd.merge(df_isp, df_flag, on='品目コード', how='inner', suffixes=('_isp', '_flag'))
    
    # さらにCP列とBECPBACA列が「一致していない」行だけ抽出
    df_not_equal = df_merged[df_merged['CP'] != df_merged['BECPBACA']]
    
    # 出力
    df_not_equal.to_excel('品目コード一致_CP不一致リスト.xlsx', index=False)

    ```
