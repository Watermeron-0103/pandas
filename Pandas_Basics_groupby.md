# ① Basic aggregation (sum, mean, count, etc.)

```python
# 担当者ごとの作業時間合計
df.groupby('担当者')['作業時間'].sum()
```
```python
担当者
佐藤    60
山田    100
鈴木    35
```
```python
# 作業内容ごとの平均時間
df.groupby('作業内容')['作業時間'].mean()
```
