# pandasでユニークな品目コードを抽出する方法

本メモでは、pandas を使ってデータの中から **重複行を削除**したり、**ユニークな値だけを抽出**するための基本的なメソッドを紹介します。品目コードを例に挙げていますが、他の列名でも同じ方法が使えます。

## `drop_duplicates()` — ユニークな行を返す

`drop_duplicates()` は、指定した列において重複する行を取り除き、ユニークな行だけを返すメソッドです。ポイントは次の通りです。

- **`subset` 引数で判定に使う列を指定します。** 例では `['品目コード']` を指定し、品目コードが同じ行を重複とみなします。
- **`keep` 引数でどの重複行を残すか選べます。** `keep='first'`（既定）は最初の出現を残し、`keep='last'` は最後の出現を残します。`keep=False` を指定すると重複行をすべて削除し、完全にユニークな値のみ残ります。
- **返り値は行単位の `DataFrame`** であり、重複を取り除いた表になります。

### 例: 最初の1件だけ残す

```python
import pandas as pd

# ExcelやCSVからデータを読み込む
df = pd.read_excel("品目一覧.xlsx")

# 品目コードが重複する行を削除（最初の出現を残す）
df_unique = df.drop_duplicates(subset=["品目コード"])

# 結果を保存
df_unique.to_excel("品目一覧_unique_first.xlsx", index=False)
```

### 例: 完全にユニークな行だけ残す

```python
df_unique_only = df.drop_duplicates(subset=["品目コード"], keep=False)
```

`keep=False` を指定すると重複している品目コードを持つ行はすべて削除されます。ユニークな値だけを確認したい場合に便利です。

## `duplicated()` — 重複フラグを返す

`duplicated()` は、各行が指定列に対して重複かどうかを示す **True / False のブール値の `Series`** を返します。`drop_duplicates()` が行を返すのに対し、`duplicated()` は重複の有無をチェックしたいときに使います。

### 例: 重複行の抽出

```python
# 品目コードが重複しているかを判定（2回目以降が True）
mask = df["品目コード"].duplicated()

# 重複行のみ抽出（初回も含めて抽出する場合は keep=False）
df_duplicates = df[df["品目コード"].duplicated(keep=False)]
```

- `df["品目コード"].duplicated()` → 2回目以降の出現が True になります。
- `df["品目コード"].duplicated(keep=False)` → 重複している全ての行が True になります。

## 使い分け

|目的|メソッド|説明|
|---|---|---|
|重複を取り除きユニークな行一覧を作る|`drop_duplicates()`|指定列の重複行を削除し、表全体を返す。|
|どの行が重複しているかをチェックしたい|`duplicated()`|True / False のフラグを返す。True は重複と判定された行。|
|完全にユニークな行だけ残したい|`drop_duplicates(keep=False)`|重複行をすべて削除し、1回しか出現しない行のみを残す。|

## 応用例 — ファイル入出力を含めたスクリプト

以下は Excel/CSV に対応し、指定列でユニークな行を抽出する簡単なスクリプトです。

```python
import pandas as pd
from pathlib import Path

def extract_unique(input_path: Path, code_column: str = "品目コード", keep: str | bool = "first"):
    """指定列の重複を削除してユニークな行を抽出する。

    Parameters
    ----------
    input_path : Path
        入力ファイルのパス（Excel または CSV）。
    code_column : str
        重複判定に使う列名。デフォルトは "品目コード"。
    keep : {"first", "last", False}
        重複行のどれを残すか。False 指定で完全ユニーク行のみ残す。
    """
    # ファイル読み込み
    if input_path.suffix.lower() in {'.xlsx', '.xlsm', '.xls'}:
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)

    # ユニーク行の抽出
    df_unique = df.drop_duplicates(subset=[code_column], keep=keep)

    # 出力ファイル名の作成
    suffix = "_unique" if keep else "_unique_only"
    output_path = input_path.with_name(input_path.stem + suffix + input_path.suffix)

    # 保存
    if output_path.suffix.lower() in {'.xlsx', '.xlsm', '.xls'}:
        df_unique.to_excel(output_path, index=False)
    else:
        df_unique.to_csv(output_path, index=False)

    return output_path

# 使い方例
# output = extract_unique(Path("品目一覧.xlsx"), code_column="品目コード", keep="first")
# print(f"ユニーク行を保存しました: {output}")
```

この関数を使えば、Excel でも CSV でも柔軟にユニーク行を抽出して保存できます。