### fillna

**概要:** `fillna` は pandas の欠損値（NaN）を補完するためのメソッドで、指定した値や方法でデータ中の欠損値を他の値に置き換えます。

**主な用途:**
- 特定の値で埋める
- 他の統計値（平均など）で埋める
- 前後の値で埋める（ffill/bfill）

**基本構文:**
```python
df.fillna(value)
df.fillna({"col1": value1, "col2": value2})
df.fillna(method='ffill')
```

**注意点:** `inplace=True` を指定しないと元のデータは更新されません。文字列列に数値を埋めると型が object になります。

---

### contains

**概要:** `contains` は pandas の文字列列における部分一致検索メソッド。`str.contains()` として使います。

**主な用途:**
- 特定の文字列を含む行を抽出する
- パターンマッチによるフィルタ

**基本構文:**
```python
df["col"].str.contains("keyword", na=False)
```

**注意点:**
- NaN を含む列に対しては `na=False` を指定しないとエラーになることがあります。
- デフォルトでは正規表現として解釈されるので、特殊文字を検索する際は `regex=False` を使うと安全です。