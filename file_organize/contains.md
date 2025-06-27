# "測定具番号"列に「検査項目」が含まれている行だけ抽出
```python
import pandas as pd

df = pd.read_excel("build/佐野受検マスタS-239(20250626).xlsx_完成後.xlsx")

# "測定具番号"列に「検査項目」が含まれている行だけ抽出
result = df[df["測定具番号"].astype(str).str.contains("検査項目", na=False)]

print(result)

# 必要ならExcelに保存
result.to_excel("検査項目を含む測定具番号のみ.xlsx", index=False)
```
