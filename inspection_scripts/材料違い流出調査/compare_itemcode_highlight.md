# pandas + openpyxl で品目コードの一致/不一致を着色する方法

## 処理の目的
- 2つの Excel ファイルを読み込み、品目コード列を照合する。
- 一致する行は **薄い緑色** に塗りつぶし。
- 不一致の行は **グレーハッチング** でマーキング。

## ポイント
- 空白（半角/全角）を削除してから比較。
- 列名は「品目」「品目コード」「部品番号」「品番」などを自動検出。
- openpyxl の `PatternFill` を使ってセル塗りつぶし。

## サンプルコード
```python
# 主要部分のみ抜粋
green = PatternFill(fill_type="solid", fgColor="C6EFCE")
grayh = PatternFill(fill_type="gray125")

dfa["一致フラグ"] = dfa["_key"].isin(set(dfb["_key"]))
dfb["一致フラグ"] = dfb["_key"].isin(set(dfa["_key"]))

def apply_styles(path, flag_col="一致フラグ"):
    wb = load_workbook(path)
    ws = wb.active
    headers = {ws.cell(1, c).value: c for c in range(1, ws.max_column + 1)}
    cflag = headers[flag_col]
    for r in range(2, ws.max_row + 1):
        style = green if bool(ws.cell(r, cflag).value) else grayh
        for c in range(1, ws.max_column + 1):
            ws.cell(r, c).fill = style
    wb.save(path)
