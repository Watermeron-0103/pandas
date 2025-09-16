# 品目コードの正規化と一致判定メモ

この備忘録では、2つのExcelファイルに含まれる品目コードを比較し、一致・不一致を判定するための正規化方法とPythonコード例をまとめます。

## 正規化の背景

品目コードにはバージョンやリビジョンを示す記号が付いている場合があり、同じ部品であっても末尾に `A` や `B1` などが付与されていることで不一致と判定されてしまうことがあります。また、一部の品目コードは冒頭が **数字2桁+アルファベット** で始まっており、桁数の違いも存在します。

一致判定を正しく行うために、品目コードを次のように正規化します。

### 正規化ルール

1. **先頭のゼロ埋め**  
   先頭が「数字2桁 + アルファベット」の場合、頭に `0` を付与して 3 桁化します。  
   例: `10B1289677_` → `010B1289677_`

2. **末尾のバージョン記号の削除**  
   品目コードの 10 文字目以降にアルファベットが現れたら、そのアルファベット以降をすべて削除します。  
   例:  
   - `123B123456A` → `123B123456`  
   - `108B1251098A1` → `108B1251098`  
   - `372N120051B` → `372N120051`  

   `_` や `.` などの記号は英字ではないため、このルールでは削除対象になりません。

3. **比較は正規化後の値で実施**  
   左右の Excel ファイルで正規化した品目コードをキーとして突合し、一致・右のみ・左のみを分類します。

## Pythonコード例

以下のコードでは、左ファイル（`一致品目抽出.xlsx`）と右ファイル（`品目コード_アルファ削除修正版.xlsx`）を読み込み、上記のルールで正規化したうえで突合し、一致状況を出力します。

```python
import pandas as pd
import re
from datetime import datetime

# ファイルパス
FILE_LEFT  = "一致品目抽出.xlsx"                  
FILE_RIGHT = "品目コード_アルファ削除修正版.xlsx"

# 正規化関数
def normalize_code(raw: str | float | int) -> str | None:
    """
    品目コードを比較用に正規化する。
    1) 文字列化＆前後空白除去
    2) 先頭が「数字2桁+英字」の場合、頭に '0' を付与（例: 10B... → 010B...）
    3) 10文字目以降に英字が現れたら、その英字以降を削除（英字自体も削除）
    """
    if pd.isna(raw):
        return None
    s = str(raw).strip()
    # 先頭が数字2桁+英字のときに 0 を付与
    if re.match(r"^\d{2}[A-Z]", s):
        s = "0" + s
    # 10文字目以降にアルファベットが出たらそこまでに切る
    if len(s) > 9:
        tail = s[9:]
        m = re.search(r"[A-Z]", tail)
        if m:
            s = s[:9 + m.start()]
    return s

# 左ファイル読み込みと正規化
left_df = pd.read_excel(FILE_LEFT)
left_key_col = next((col for col in ["品目", "品目コード"] if col in left_df.columns), left_df.columns[0])
left_df["比較用ベースコード"] = left_df[left_key_col].apply(normalize_code)

# 右ファイル読み込み（複数シートを連結）
right_book = pd.read_excel(FILE_RIGHT, sheet_name=None)
right_frames = []
for sheet_name, rdf in right_book.items():
    rdf = rdf.copy()
    right_key_col = next((col for col in ["削除後品目コード", "品目コード", "品目"] if col in rdf.columns), rdf.columns[0])
    rdf["比較用ベースコード"] = rdf[right_key_col].apply(normalize_code)
    rdf["__シート名__"] = sheet_name
    right_frames.append(rdf)

right_df = pd.concat(right_frames, ignore_index=True)

# 突合: 右を主語に左を突き合わせる
matched = pd.merge(
    right_df, left_df,
    on="比較用ベースコード",
    how="left",
    suffixes=("_右", "_左")
)
matched["一致フラグ"] = matched[left_key_col].notna()

# 不一致抽出
right_only = matched[matched[left_key_col].isna()].copy()
left_only = left_df[~left_df["比較用ベースコード"].isin(right_df["比較用ベースコード"])]

# 結果出力
out_file = f"比較結果_右主導_一致不一致_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
with pd.ExcelWriter(out_file, engine="openpyxl") as w:
    matched.to_excel(w, sheet_name="右主導_全件(一致フラグ付)", index=False)
    matched[matched["一致フラグ"]].to_excel(w, sheet_name="一致(右↔左)", index=False)
    right_only.to_excel(w, sheet_name="右のみ", index=False)
    left_only.to_excel(w, sheet_name="左のみ", index=False)

print(f"出力完了: {out_file}")
```

このコードでは、右ファイルのすべての行に対して左ファイルを突き合わせ、結果を 4 つのシートに分けて出力しています。`一致フラグ` 列が `True` の行が一致と判断された行です。

## 備考

- `BASE_POS_AFTER = 9` としており、10 文字目（1始まりで数えて）から後ろで最初に出現する英字を基準に切り落としています。基準位置を変更したい場合は関数 `normalize_code` の該当部分を調整します。
- `_` や `.` など記号を削除したい場合は、正規化関数に追加ルールを入れてください。
- 正規化した値をキーにすることで、バージョン記号や桁数の違いがある場合でも、同じ部品を一致させることができます。
