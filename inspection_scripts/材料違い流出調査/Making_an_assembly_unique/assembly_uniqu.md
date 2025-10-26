# assembly_uniqu.py

This script helps identify unique part codes across material and assembly sheets in an Excel workbook. It is designed to support quality control investigations where you need to check for duplicate components and trace them through different BOM (Bill of Materials) views.

日本語訳：  
このスクリプトは、Excelブック内の材料シートとアセンブリシート全体にわたって、固有の部品コードを識別するのに役立ちます。重複した部品の有無を確認し、複数のBOM（部品表）ビューで追跡する必要がある品質管理調査をサポートするように設計されています。


## How it works

1. **Input settings** – The script expects an Excel file (specified by `FILE_MA`) containing at least two worksheets:
   - A materials sheet (default name: `1_材料(単品)+assemblyフラグ`) which lists individual parts.
   - An assembly sheet (default name: `2_ASSYBOM+材料フラグ`) which lists assemblies and their constituent parts.
   - Both sheets must have a column named `部品No.` that contains the part numbers to analyse.

2. **Normalization** – Part numbers are cleaned and normalized using Unicode NFKC normalization.  Full‑width spaces are converted to half‑width, various kinds of dashes are unified to `'-'`, zero‑width and non‑breaking spaces are removed, and case is coerced to upper (or lower) if needed.  This ensures that visually similar part codes are treated the same.

3. **Uniqueness flags** – For each sheet, the script assigns two boolean flags:
   - `ユニーク_シート内` is `True` for the first occurrence of each normalized part number within that sheet.
   - `ユニーク_全体` is `True` for the first occurrence across **both** sheets; subsequent duplicates in either sheet are marked `False`.  Empty values are always marked `False`.

4. **Output** – The resulting data frames, including the original data and added columns `ユニーク_シート内`, `ユニーク_全体`, and the intermediate `正規化キー` (normalized key), are written back to a new Excel file (`材料ASSYBOM_照合_3出力_ユニーク付与.xlsx`).  Each sheet retains its original name.

## Usage　使用方法

Adjust the file names, sheet names and column names at the top of the script to match your workbook.  Then run the script with Python.  It will read the input workbook, compute the uniqueness flags, and output a new workbook in the same directory.

日本語訳：
スクリプトの先頭にあるファイル名、シート名、列名をワークブックに合わせて調整してください。その後、Pythonでスクリプトを実行します。入力ワークブックを読み取り、一意性フラグを計算し、同じディレクトリに新しいワークブックを出力します。
