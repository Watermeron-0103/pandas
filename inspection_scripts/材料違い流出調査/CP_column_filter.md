# CP列のキーワード抽出備忘録

## 概要
受入れ検査品リストの **CP** 列から特定の文字列を含む行を抽出する方法をまとめた備忘録です。この例では `CP` 列に `'BA'` または `'BE'` を含む行を抽出します。

## ポイント
- `pandas` では列の部分一致検索に **`str.contains()`** を使用します。
- `CP` 列が数値や欠損値を含んでいる可能性があるため、先に **`.astype(str)`** で文字列化します。
- 正規表現 `"BA|BE"` は **`'BA'`または `'BE'`** のいずれかを含む行を抽出します。
- `na=False` を指定すると `NaN`（欠損値）は対象外となります。

## サンプルコード

```
import pandas as pd

# Excelファイルの読み込み
file_path = "受入れ検査品リストVer1_2021.5.31  .xlsx"
df = pd.read_excel(file_path)

# CP列から 'BA' または 'BE' を含む行を抽出（部分一致）
filtered_df = df[df["CP"].astype(str).str.contains("BA|BE", na=False)]

# 抽出結果の先頭5件を確認
print(filtered_df.head())

# 必要なら結果を別ファイルに保存
filtered_df.to_excel("\u53d7\u5165\u308c\u691c\u67fb\u54c1\u30ea\u30b9\u30c8_CP\u62bd\u51fa.xlsx", index=False)
```

## 従用
- 完全一致で抽出する場合は `==` 比較を使います。  
  例: `df[df["CP"].astype(str).isin(["BA", "BE"])]`
- 複数条件を組み合わせる場合は `|` (非志選べ), `&` (非志選) を使ってフィルタを組みます。
