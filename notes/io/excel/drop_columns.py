import pandas as pd
from pathlib import Path


def drpp_columns_by_list(
        src_path: str,
        list_path: str,
        out_path: str | None = None,
        list_sheet_name=0,
        list_col_name='削除対象列名',
):
    """不要カラムリストExcelを見て、本体Excelから対象カラムを削除する"""

    src_path = Path(src_path)
    list_path = Path(list_path)

    # 1) 本体のデータ読み込み
    df = pd.read_excel(src_path)

    # 2) 不要カラムリスト読み込み
    drop_list_df = pd.read_excel(list_path, sheet_name=list_sheet_name)

    # 3) リストからカラム名リストを作成（NaNは無視）
    drop_cols = (
        drop_list_df[list_col_name]
        .dropna()
        .astype(str)
        .tolist()
    )

    # 4) 本体に実在するカラムだけに絞る（Typo対策）
    drop_cols_existing = [c for c in drop_cols if c in df.columns]
    drop_cols_not_found = [c for c in drop_cols if c not in df.columns]

    print(f"★削除対象（存在するカラム）:", drop_cols_existing)
    if drop_cols_not_found:
        print(f"★本体に存在しなかったカラム:", drop_cols_not_found)

    # 5) 削除
    df_drop = df.drop(columns=drop_cols_existing)

    # 6) 保存先パス（指定がなければ「元ファイル名_削除後.xlsx」）
    if out_path is None:
        out_path = src_path.with_name(src_path.stem + '_削除後.xlsx')

    df_drop.to_excel(out_path, index=False)
    print(f"★保存しました → {out_path}")

    return df_drop

if __name__ == '__main__':
    drpp_columns_by_list(
        src_path ="source/imart_返品管理表_2025-11-24_2025-11-28.xlsx",
        list_path = "source/drop_columns_list.xlsx",
        list_col_name='削除対象列名',
    )