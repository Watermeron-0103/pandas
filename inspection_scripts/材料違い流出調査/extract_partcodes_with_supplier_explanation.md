# `extract_partcodes_with_supplier.py` の解説

この Python スクリプトは、人体接触部品の調査用 Excel ファイルに含まれる **複数シート** から、
各シートの「品目コード」とシート名（サプライヤ名）を組み合わせた一覧表を作成するものです。

## スクリプトの目的

- Excel ファイルにはサプライヤ別にシートが分かれており、各シートにそのサプライヤが扱う部品の一覧が記載されています。
- シート名がそのままサプライヤ名になっているため、各シートから **品目コード** 列を抽出し、
 それぞれのサプライヤ名を対応付ける形で 1 つの一覧表にまとめます。
- 抽出結果は重複を取り除いたうえで、新しい Excel ファイルとして出力します。

## コードの解説

以下に、重要な部分ごとにコードを解説します。実際のコードは後述のコードブロックをご参照ください。

1. **モジュールのインポート**

   ```python
   import pandas as pd
   ```

   - データ処理には Python ライブラリの `pandas` を使用します。

2. **関数 `extract_partcodes_with_supplier` の定義**

   ```python
   def extract_partcodes_with_supplier(file_path: str, output_path: str):
   ```

   - `file_path` には入力する Excel ファイルのパスを、
     `output_path` には出力する一覧ファイルのパスを指定します。

3. **Excel ファイルの全シート名を取得**

   ```python
   xls = pd.ExcelFile(file_path)
   
   for sheet in xls.sheet_names:
       ...
   ```

   - `pd.ExcelFile` を使うと、Excel ファイル内に含まれるシート名を取得できます。
   - `xls.sheet_names` はシート名のリストを返します。
   - 各シート名（サプライヤ名）を `sheet` 変数に入れ、後続の処理で利用します。

4. **各シートを読み込み、品目コードを抽出**

   ```python
   df = pd.read_excel(file_path, sheet_name=sheet)
   if "品目コード" in df.columns:
       subset = df[["品目コード"]].dropna()
       subset["サプライヤー"] = sheet
   ```

   - `pd.read_excel` でシートを DataFrame として読み込みます。
   - シートに "品目コード" 列が存在するかを確認し、存在すればその列を抜き出します。
   - `dropna()` により空セル（NaN）は削除しておきます。
   - `subset["サプライヤー"] = sheet` でシート名（サプライヤ名）を新しい列として追加します。

5. **抽出結果を結合し、重複を除去**

   ```python
   result = pd.concat(all_data, ignore_index=True)
   result = result.drop_duplicates()
   ```

   - 各シートから取得した部分集合をリスト `all_data` に追加しておき、最後に `pd.concat` で 1 つの DataFrame にまとめます。
   - 同じ部品コードが複数シートに存在する場合は重複を削除します。必要に応じてこの行は省略可能です。

6. **結果を Excel に保存**

   ```python
   result.to_excel(output_path, index=False)
   ```

   - 結合した結果を指定された `output_path` に出力します。`index=False` とすることで、行番号の列を作らずに保存します。

7. **メイン処理**

   ```python
   if __name__ == "__main__":
       input_file = "source/人体接触部品　調査(2024).xlsx"
       output_file = "out/調査(2024)_品目コード_サプライヤ一覧.xlsx"
       extract_partcodes_with_supplier(input_file, output_file)
   ```

   - スクリプトが直接実行された場合に実行される部分です。
   - 入力ファイルと出力ファイルのパスはプロジェクトのディレクトリ構造に合わせて指定しています。

## 完全なコード

以下が備忘録用の完全な Python スクリプトです。実行環境に応じてファイルパスなどを適宜調整してください。

```python
# coding: utf-8
"""
Excelファイルの全シートから「品目コード」と「サプライヤ名（シート名）」を抜き出すスクリプト
"""

import pandas as pd


def extract_partcodes_with_supplier(file_path: str, output_path: str):
    """指定された Excel ファイルの各シートから品目コードを抜き出し、
    シート名をサプライヤ名として対応付けて一覧を生成する。
    
    Args:
        file_path (str): 入力する Excel ファイルへのパス
        output_path (str): 出力する Excel ファイルへのパス
    """
    # Excelファイルの全シート名を取得
    xls = pd.ExcelFile(file_path)

    all_data = []

    # シートごとに処理
    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(file_path, sheet_name=sheet)
            # "品目コード" 列があるシートだけ処理
            if "品目コード" in df.columns:
                subset = df[["品目コード"]].dropna()
                # シート名をサプライヤ名として追加
                subset["サプライヤー"] = sheet
                all_data.append(subset)
        except Exception as e:
            print(f"シート {sheet} 読み込み中にエラー: {e}")

    if not all_data:
        print("対象の列（品目コード）が見つかりませんでした。")
        return

    # 全シート分を結合して一覧を作成
    result = pd.concat(all_data, ignore_index=True)

    # 重複を除去（必要に応じて省略可能）
    result = result.drop_duplicates()

    # 出力
    result.to_excel(output_path, index=False)
    print(f"一覧を保存しました → {output_path}")


if __name__ == "__main__":
    input_file = "source/人体接触部品　調査(2024).xlsx"   # 入力ファイル
    output_file = "out/調査(2024)_品目コード_サプライヤ一覧.xlsx"  # 出力ファイル
    extract_partcodes_with_supplier(input_file, output_file)
```

## 使い方のポイント

- **フォルダ構成の確認**: `input_file` や `output_file` のパスは、ご自身のリポジトリ構造に合わせて修正してください。
- **列名の変更**: Excel の列名が異なる場合（例: "部品番号"）、コード中の列名を実際のものに変更する必要があります。
- **重複処理**: 同じ品目コードが複数サプライヤに存在する場合、重複を残したい場合は `drop_duplicates()` を削除してください。
- **エラー出力**: シート読み込み時のエラーがあれば、`print` で知らせています。必要に応じてログ出力に置き換え可能です。

この備忘録が、材料違い流出調査の自動化スクリプト管理に役立てば幸いです.
