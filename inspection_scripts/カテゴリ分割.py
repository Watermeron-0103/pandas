import os
import re
import math
import pandas as pd


# === 入出力設定 ===
SRC_FILE = "2501-2507/不適合の表_2025101-20250703.xlsx"
SRC_SHEET = "総合183"
OUT_DIR   = "out"
OUT_FILE  = os.path.join(OUT_DIR, "不良カテゴリ別_ブック.xlsx")

os.makedirs(OUT_DIR, exist_ok=True)

# === ユーティリティ ===
def sanitize_sheet_name(name: str) -> str:
    """
    Excelのシート名に使えない文字の除去、31文字制限、空→'Sheet'に置き換え。
    """
    # 禁止文字: : \ / ? * [ ]
    name = re.sub(r'[:\\/\?\*\[\]]', '_', str(name))
    name = name.replace("'", "’")  # HYPERLINK参照のためシングルクォートは避ける
    name = name.strip() or "Sheet"
    return name[:31]

def unique_name(base: str, used: set) -> str:
    """
    同名シート回避（末尾に _2, _3 ...）
    """
    name = base
    i = 2
    while name in used:
        suffix = f"_{i}"
        name = (base[:(31 - len(suffix))] + suffix) if len(base) + len(suffix) > 31 else base + suffix
        i += 1
    used.add(name)
    return name

def best_fit_widths(df: pd.DataFrame, max_width=60):
    """
    簡易オートフィット（文字数→列幅）
    """
    widths = []
    for col in df.columns:
        max_len = max(
            [len(str(col))] + [len(str(v)) for v in df[col].head(500).tolist()]  # 全件は重いのでサンプル
        )
        # 全角対策でちょい広めに
        widths.append(min(max_len + 2, max_width))
    return widths

# === データ読み込み ===
df = pd.read_excel(SRC_FILE, sheet_name=SRC_SHEET)
# カテゴリ欠損は除外（必要ならここをコメントアウト）
df = df.copy()
df["不良カテゴリ"] = df["不良カテゴリ"].astype(str)
df = df[df["不良カテゴリ"].notna() & (df["不良カテゴリ"].str.strip() != "")]

# === 集計（カテゴリ別件数・割合） ===
counts = df["不良カテゴリ"].value_counts(dropna=False)
total = int(counts.sum())
summary = (
    counts.rename("件数")
    .to_frame()
    .assign(割合=lambda x: (x["件数"] / total * 100).round(1))
    .reset_index()
    .rename(columns={"index": "不良カテゴリ"})
)

# === Excel書き出し ===
with pd.ExcelWriter(OUT_FILE, engine="xlsxwriter") as writer:
    workbook  = writer.book

    # 1) 一覧シート
    summary_sheet = "カテゴリ一覧"
    summary.to_excel(writer, index=False, sheet_name=summary_sheet)
    ws_summary = writer.sheets[summary_sheet]

    # 列幅調整
    widths = best_fit_widths(summary)
    for i, w in enumerate(widths):
        ws_summary.set_column(i, i, w)

    # 件数・割合に書式
    fmt_int = workbook.add_format({"num_format": "#,##0"})
    fmt_pct = workbook.add_format({"num_format": "0.0\"%\""})
    ws_summary.set_column(1, 1, None, fmt_int)  # 件数
    ws_summary.set_column(2, 2, None, fmt_pct)  # 割合

    # 2) カテゴリごとにシート作成
    used_names = set()
    link_col = summary.columns.get_loc("不良カテゴリ")  # 0列目
    link_target_col = 3  # 一覧シートのD列あたりにリンク列を作る

    ws_summary.write(0, link_target_col, "シートへ")

    for r, row in summary.iterrows():
        category = row["不良カテゴリ"]
        cat_df = df[df["不良カテゴリ"] == category].reset_index(drop=True)

        # シート名を安全化 + 重複回避
        base = sanitize_sheet_name(category)
        sheet_name = unique_name(base, used_names)

        # シート書き出し
        cat_df.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]

        # フィルタ、ヘッダ固定、列幅
        ws.autofilter(0, 0, len(cat_df), len(cat_df.columns) - 1)
        ws.freeze_panes(1, 0)
        widths_cat = best_fit_widths(cat_df)
        for i, w in enumerate(widths_cat):
            ws.set_column(i, i, w)

        # 一覧から該当シートA1へ飛ぶハイパーリンク
        # 例: =HYPERLINK("#'加工不良'!A1","→ジャンプ")
        link_formula = f"=HYPERLINK(\"#'{sheet_name}'!A1\",\"→ジャンプ\")"
        ws_summary.write(r + 1, link_target_col, link_formula)

    # 一覧シートのヘッダ固定
    ws_summary.freeze_panes(1, 0)

print(f"✅ 出力完了: {OUT_FILE} （{len(summary)}カテゴリ, 合計 {total} 件）")
