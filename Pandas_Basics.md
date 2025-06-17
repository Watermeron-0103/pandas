Check the columns and change them

# *How to check a column*
    ```python
    import pandas as pd

    
    df = pd.read_excel(file_path, sheet_name=0)
    
    # check column
    print(df.columns)
    
    # If you want to get the column names in a list:
    print(df.columns.to_list())
    ```

# *Delete a column*
    ```python
    # 1列だけ削除
    df = df.drop('削除したい列名', axis=1)
    
    # 複数列を削除
    df = df.drop(['列名1', '列名2'], axis=1)
    
    # 存在しない列があってもエラーを出したくない場合
    df = df.drop(['列名1', '列名2'], axis=1, errors='ignore')
    ```

# *Change the column name*
    ```python
    # Rename columns in a DataFrame
    df.columns = ['新しいカラム1', '新しいカラム2', ...]
    
    # Rename specific columns using a dictionary
    df = df.rename(columns={'部品番号\nPart number': '部品番号'})
    
    # You can also make multiple changes at the same time.
    df = df.rename(columns={'名称\nPart name': '名称', '文書番号\nDocument number': '文書番号'})
    
    # Directly modify the original DataFrame with inplace=True
    df.rename(columns={'種類 Type\n  クリティカル    Critical\n  非クリティカル Non-Critical': '種類'}, inplace=True)
    ```

# *How to check the type*
    ```python
    print(type(df)
    
    ```
