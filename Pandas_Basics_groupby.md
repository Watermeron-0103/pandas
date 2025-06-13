# ① Basic aggregation (sum, mean, count, etc.)

```python
# 担当者ごとの作業時間合計
df.groupby('担当者')['作業時間'].sum()
```

