# How to use merge

- Extract items with matching on = "document number" in merge
  - *how='inner' は、pandas の merge や join で「内部結合（inner join）」を指定するための引数です。*
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
