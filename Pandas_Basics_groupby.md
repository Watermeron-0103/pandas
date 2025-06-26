#Groupby is useful, and here's an example of how to use it:

- "groupby" in pandas is a function that allows you to "group" data by specific conditions (categories or columns) and aggregate and analyze each group.
    ```python
    import pandas as pd
    
    
    data = {
        '店舗': ['東京', '東京', '大阪', '大阪', '東京'],
        '商品名': ['りんご', 'みかん', 'りんご', 'みかん', 'りんご'],
        '売上': [100, 150, 120, 130, 110]
    }
    df = pd.DataFrame(data)
    
    # 店舗ごとの売上合計を集計する
    result = df.groupby('店舗')['売上'].sum()
    
    print(result)
    ```
Execution result
    ```python
    店舗
    大阪    250
    東京    360
    ```
Grouping image (diagram)
Image of "grouping" the original data:

```css
データセット
｜
├─ 東京 ── [100, 150, 110]
│
└─ 大阪 ── [120, 130]
```
- Basic Writing Structure
    ```python
    df.groupby('グループ化する列')['集計対象列'].集計関数()
    ```
    Here are some examples

# ① Basic aggregation (sum, mean, count, etc.)

    ```python
    # 担当者ごとの作業時間合計
    df.groupby('担当者')['作業時間'].sum()
    ```
Execution result
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

# ② Aggregation by multiple columns (Multi-index)

```python
# 担当者ごとに、作業内容ごとの作業時間合計
df.groupby(['担当者', '作業内容'])['作業時間'].sum()
```
Execution result
```python
担当者  作業内容
佐藤    検査      60
山田    報告      25
       検査      30
       記録      45
鈴木    検査      20
       記録      15
```

# ③ Apply multiple aggregation functions together

```python
# 担当者ごとに作業時間の合計・平均・回数をまとめて算出
df.groupby('担当者')['作業時間'].agg(['sum', 'mean', 'count'])
```
Execution result
```python
        sum   mean  count
担当者                    
佐藤      60  60.00      1
山田     100  33.33      3
鈴木      35  17.50      2
```


# ④ Get the maximum and minimum rows for each category (idxmax, idxmin)

```python
# 担当者ごとに作業時間が最大の行を取得
idx = df.groupby('担当者')['作業時間'].idxmax()
df.loc[idx]
```
Execution result
```python
  担当者 作業内容  作業時間
0   山田    検査     30
2   鈴木    検査     20
5   佐藤    検査     60

```

# ⑤ Transforming data

```python
# 担当者ごとの作業時間平均を元データに追加
df['担当者平均'] = df.groupby('担当者')['作業時間'].transform('mean')
```
Execution result
```python
| 担当者 | 作業内容 | 作業時間 | 担当者平均 |
| --- | ---- | ---- | ----- |
| 山田  | 検査   | 30   | 33.33 |
| 山田  | 記録   | 45   | 33.33 |
| 鈴木  | 検査   | 20   | 17.50 |
```

⑥ Loop through each group

```python
# 担当者ごとに処理をループ
for name, group in df.groupby('担当者'):
    print(f"担当者: {name}")
    print(group)
```
