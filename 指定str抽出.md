# 📘 Python学習メモ: 3GMS指定部品の抽出とExcel出力

## 目的
Excelファイルから「3GMSが指定されている部品番号」を抽出し、リストをExcelに出力する。

---

## ポイント

### 1. Excelファイルの読み込み
```python
df = pd.read_excel("ファイル名.xlsx", sheet_name="受検マスタ", header=3)
```
- `sheet_name="受検マスタ"` でシートを指定
- `header=3` → Excelの4行目を列名として使う

---

### 2. 行に「3GMS」が含まれるか判定
```python
mask = df.apply(lambda row: any(isinstance(cell, str) and "3GMS" in cell for cell in row), axis=1)
```
- `apply(..., axis=1)` → 各行に処理を適用
- `any(...)` → 1つでも "3GMS" を含んでいれば True

---

### 3. 部品番号を抽出
```python
parts_with_3gms = df.loc[mask, "部番(MCF登録品目コード）"].dropna().unique()
```
- `loc[mask, 列名]` → 3GMSを含む行の部品番号だけを抽出
- `dropna()` → 欠損値を除外
- `unique()` → 重複を除外

---

### 4. Excelに出力
```python
result_df = pd.DataFrame(parts_with_3gms, columns=["部番(MCF登録品目コード）"])
result_df.to_excel("out/3GMS指定部品リスト.xlsx", index=False)
```
- DataFrameに変換して出力
- `index=False` で余計な行番号を入れない

---

## まとめ
- **any** を使うと「1つでも条件を満たすか」を判定できる  
- **unique** で重複を削除できる  
- **to_excel** で簡単に出力できる  

👉 これで「3GMSが指定された部品リスト」をExcelに保存できる！
