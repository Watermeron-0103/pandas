````markdown
# 📘 pandas 基礎操作メモ

## 1. 列名の確認
```python
import pandas as pd

df = pd.read_excel("sample.xlsx", sheet_name=0)

# 全列名を確認
print(df.columns)

# リストとして取得
print(df.columns.to_list())
````

---

## 2. 列の削除

```python
# 1列だけ削除
df = df.drop("削除したい列名", axis=1)

# 複数列を削除
df = df.drop(["列名1", "列名2"], axis=1)

# 存在しない列があってもエラーを出さない
df = df.drop(["列名1", "列名2"], axis=1, errors="ignore")
```

👉 よくある例：

```python
df = df.drop([f"Unnamed: {i}" for i in range(32, 111)], axis=1)
```

---

## 3. 列名の変更

```python
# 全部まとめて変更
df.columns = ["新しいカラム1", "新しいカラム2", ...]

# 辞書で一部だけ変更
df = df.rename(columns={
    "部品番号\nPart number": "部品番号",
    "名称\nPart name": "名称"
})

# inplace=True を付けると直接反映
df.rename(columns={"種類 Type": "種類"}, inplace=True)
```

---

## 4. DataFrameの型確認

```python
print(type(df))   # pandas.core.frame.DataFrame かどうか
```

---

## 5. 行の抽出（条件付き）

### 5.1 特定の文書番号を除外

```python
df = df[df["文書番号"] != "PA-IP00-000"]
```

### 5.2 複数の文書番号をまとめて除外

```python
exclude_list = ["PA-IP27-442", "PA-IP27-444", "PA-IP25-657"]
df = df[~df["文書番号"].isin(exclude_list)]
```

### 5.3 「認定」列が NaN の行を抽出

```python
df = df[df["認定"].isna()]
```

---

## まとめ

* 列操作は **`df.columns` / `df.drop` / `df.rename`** が基本
* 条件抽出は **`isin`** と **`isna`** を覚えると便利
* pandasは **「列ごとの処理」** と **「行の条件抽出」** が基礎の核

```


