# "測定具番号"列に「検査項目」が含まれている行だけ抽出
```python
# "測定具番号"列に「検査項目」が含まれている行だけ抽出
result = df[df["測定具番号"].astype(str).str.contains("検査項目", na=False)]

print(result)
```
