import pandas as pd


def write_with_mode_w() -> None:
    """Overwrite an Excel file using mode="w".

    This function creates a simple DataFrame and writes it to
    ``example_mode_w.xlsx``. If the file already exists, its
    contents will be replaced entirely.

    mode="w" を使用して Excel ファイルを上書きします。

    この関数は単純な DataFrame を作成し、それを
    ``example_mode_w.xlsx`` に書き込みます。ファイルが既に存在する場合は、
    その内容全体が置き換えられます。
    """
    df = pd.DataFrame({"A": [1, 2, 3]})
    with pd.ExcelWriter("example_mode_w.xlsx", engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="initial", index=False)


def append_with_mode_a() -> None:
    """Append to an existing Excel file using mode="a".

    This function writes two DataFrames into ``example_mode_a.xlsx``. The
    first call uses mode="w" to create the file and write the first sheet.
    The second call opens the file in append mode and adds a second sheet.

    mode="a" を使用して既存の Excel ファイルに追加します。
    
    この関数は、2 つの DataFrame を ``example_mode_a.xlsx`` に書き込みます。
    最初の呼び出しでは、mode="w" を使用してファイルを作成し、最初のシートを書き込みます。
    2 番目の呼び出しでは、ファイルを追加モードで開き、2 番目のシートを追加します。
    """
    # First DataFrame and initial write
    df1 = pd.DataFrame({"A": [1, 2, 3]})
    with pd.ExcelWriter("example_mode_a.xlsx", engine="openpyxl", mode="w") as writer:
        df1.to_excel(writer, sheet_name="first", index=False)

    # Second DataFrame appended as a new sheet
    df2 = pd.DataFrame({"B": [4, 5, 6]})
    with pd.ExcelWriter(
        "example_mode_a.xlsx", engine="openpyxl", mode="a", if_sheet_exists="new"
    ) as writer:
        df2.to_excel(writer, sheet_name="second", index=False)


if __name__ == "__main__":
    write_with_mode_w()
    append_with_mode_a()
    print(
        "Written 'example_mode_w.xlsx' (overwritten) and 'example_mode_a.xlsx' (appended)."
    )
