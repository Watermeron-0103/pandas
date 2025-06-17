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
    
- **Example of using drop **
    ``` python
    df = df.drop(['Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34', 'Unnamed: 35', 'Unnamed: 36', 'Unnamed: 37', 'Unnamed: 38', 'Unnamed: 39', 'Unnamed: 40', 'Unnamed: 41', 'Unnamed: 42', 'Unnamed: 43', 'Unnamed: 44', 'Unnamed: 45', 'Unnamed: 46', 'Unnamed: 47', 'Unnamed: 48', 'Unnamed: 49', 'Unnamed: 50', 'Unnamed: 51', 'Unnamed: 52', 'Unnamed: 53', 'Unnamed: 54', 'Unnamed: 55', 'Unnamed: 56', 'Unnamed: 57', 'Unnamed: 58', 'Unnamed: 59', 'Unnamed: 60', 'Unnamed: 61', 'Unnamed: 62', 'Unnamed: 63', 'Unnamed: 64', 'Unnamed: 65', 'Unnamed: 66', 'Unnamed: 67', 'Unnamed: 68', 'Unnamed: 69', 'Unnamed: 70', 'Unnamed: 71', 'Unnamed: 72', 'Unnamed: 73', 'Unnamed: 74', 'Unnamed: 75', 'Unnamed: 76', 'Unnamed: 77', 'Unnamed: 78', 'Unnamed: 79', 'Unnamed: 80', 'Unnamed: 81', 'Unnamed: 82', 'Unnamed: 83', 'Unnamed: 84', 'Unnamed: 85', 'Unnamed: 86', 'Unnamed: 87', 'Unnamed: 88', 'Unnamed: 89', 'Unnamed: 90', 'Unnamed: 91', 'Unnamed: 92', 'Unnamed: 93', 'Unnamed: 94', 'Unnamed: 95', 'Unnamed: 96', 'Unnamed: 97', 'Unnamed: 98', 'Unnamed: 99', 'Unnamed: 100', 'Unnamed: 101', 'Unnamed: 102', 'Unnamed: 103', 'Unnamed: 104', 'Unnamed: 105', 'Unnamed: 106', 'Unnamed: 107', 'Unnamed: 108', 'Unnamed: 109', 'Unnamed: 110'], axis=1)
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
