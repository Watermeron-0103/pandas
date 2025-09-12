# 受入れ検査リストと重要部品フラグの突き合わせ

## 目的
- **ケース①**: 受入れ検査リストの中から、重要部品フラグに登録されている品目だけを抽出する。  
- **ケース②**: 両方の情報を突き合わせ、受入れ検査リストに重要部品フラグの情報を付与する。  
- **ケース③**: 双方のリストで不一致（どちらか片方にしか存在しない品目）を抽出する。  

## サンプルコード

```python
import pandas as pd

# ファイル読み込み
df_flag = pd.read_excel("品目マスタ_BABE.xlsx")    # 「品目コード」列あり
df_list = pd.read_excel("受入リスト_BABE.xlsx")    # 「品目no」列あり

# 列名を統一（マージ用）
df_flag = df_flag.rename(columns={"品目コード": "品目"})
df_list = df_list.rename(columns={"品目no": "品目"})

# ------------------------------------------------
# ケース①: 重要部品フラグに存在する品目だけを抽出
# ------------------------------------------------
df_filtered = df_list[df_list["品目"].isin(df_flag["品目"])]

# 結果保存
df_filtered.to_excel("受入リスト_重要部品のみ.xlsx", index=False)

# ------------------------------------------------
# ケース②: 両方の情報を突き合わせて結合
# ------------------------------------------------
df_merged = pd.merge(df_list, df_flag, on="品目", how="inner")

# 結果保存
df_merged.to_excel("受入リスト_マスター付き.xlsx", index=False)

# ------------------------------------------------
# ケース③: 不一致の抽出
# ------------------------------------------------
# 方法1: isin を使う
df_list_unmatched = df_list[~df_list["品目"].isin(df_flag["品目"])]  # 受入リストにあってマスタにない
df_flag_unmatched = df_flag[~df_flag["品目"].isin(df_list["品目"])]  # マスタにあって受入リストにない

# 方法2: merge を使って indicator=True で確認
df_outer = pd.merge(df_list, df_flag, on="品目", how="outer", indicator=True)
df_left_only  = df_outer[df_outer["_merge"] == "left_only"]   # 受入リストだけ
df_right_only = df_outer[df_outer["_merge"] == "right_only"]  # マスタだけ

# 保存（必要に応じて）
df_list_unmatched.to_excel("受入リスト_不一致.xlsx", index=False)
df_flag_unmatched.to_excel("品目マスタ_不一致.xlsx", index=False)
