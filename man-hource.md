# Calculate the total man-hours based on Inspection Man-hours.xlsx


- or Response
```python
import pandas as pd
import ast

df_tools = pd.read_excel('tools_list_by_part.xlsx')
df_kosu = pd.read_excel('src/検査工数.xlsx')

# 記号と標準工数の辞書
kosu_dict = df_kosu.set_index('記号')['標準工数'].to_dict()

results = []

for idx, row in df_tools.iterrows():
    plan_no = row['検査計画書品番']
    tools_list_str = row['検査具リスト']
    tools_list_raw = tools_list_str

    # NaN（空欄）の場合は合計0
    if pd.isna(tools_list_str):
        total_time = 0
    else:
        tools_list = ast.literal_eval(tools_list_str)
        total_time = 0
        for tool in tools_list:
            # "or"パターン
            if "or" in tool:
                options = [opt.strip() for opt in tool.split("or")]
                std_times = []
                for opt in options:
                    if opt in kosu_dict and pd.notna(kosu_dict[opt]):
                        std_times.append(float(kosu_dict[opt]))
                if std_times:  # 少なくとも1つ標準工数があれば平均を使う
                    avg_time = sum(std_times) / len(std_times)
                    total_time += avg_time
            else:
                if tool in kosu_dict and pd.notna(kosu_dict[tool]):
                    total_time += float(kosu_dict[tool])
    results.append({
        '検査計画書品番': plan_no,
        '検査具リスト': tools_list_raw,
        '合計標準工数': total_time
    })

# DataFrame化してExcel出力
df_result = pd.DataFrame(results)
df_result.to_excel('検査計画書品番_検査具リスト_合計標準工数.xlsx', index=False)

```

# How to change MM:DD:SS to ss
- Converting a string in HH:MM:SS format to a number of seconds (in decimal format) is easy.
    ```python
    import pandas as pd
    
    # Excelファイルを読み込む
    df = pd.read_excel("Divide_by_person_in_charge.xlsx")
    
    # 工数列（HH:MM:SS形式）を秒数に変換
    df['工数（秒）'] = pd.to_timedelta(df['工数']).dt.total_seconds()
    
    # 結果を確認
    print(df[['工数', '工数（秒）']])
    
    # Excelに保存
    df.to_excel("工数_秒数変換後.xlsx", index=False)

    ```

- Let's try "deleting _ and spaces ( ) from the Ver. column, concatenating the part number column and the Ver. column to create a new item code column."

    ```python
    import pandas as pd
    
    # ファイル読み込み
    df = pd.read_excel('20250619_受入れ検査品リストVer1_2021.5.31  .xlsx')
    
    # 「Ver.」列の「_」と「空白」を削除
    df['Ver.'] = df['Ver.'].astype(str).str.replace('_', '').str.replace(' ', '')
    
    # 「部品番号」列と「Ver.」列を連結して「品目コード」列を作成
    df['品目コード'] = df['部品番号'].astype(str) + df['Ver.']
    
    # 結果の確認
    print(df[['部品番号', 'Ver.', '品目コード']].head())
    
    # 保存
    df.to_excel('品目コード追加済.xlsx', index=False)

    ```
