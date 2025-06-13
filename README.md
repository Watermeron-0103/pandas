# [pandas] test_list to json strings.
Pseudocode / Step-by-Step Plan:

Import pandas and json.

Load the first sheet of the Excel file src/受検S-235.xlsx into a DataFrame.

Group the data by '検査品番' (inspection part number) and collect non-null values of '測定具' (measuring tools) for each group into lists.

For each part number and its list of tools, serialize the tool list into JSON, and append a dictionary to rows.

Convert rows to a new DataFrame.

Export this DataFrame to Excel as tools_list_by_part.xlsx.

Short Explanation:
This code reads an Excel file, groups data by inspection part number, lists all measuring tools for each part (ignoring missing values), then saves the results in a new Excel file, with tool lists stored as JSON strings.

```
import pandas as pd
import json


file_path = "src/受検S-235.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

tool_dict = df.groupby('検査品番')["測定具"].apply(lambda x: [i for i in x if pd.notna(i)]).to_dict()

rows = []
for part_no, tools in tool_dict.items():
    tools_str = json.dumps(tools, ensure_ascii=False)
    rows.append({'検査品番': part_no, '検査具リスト': tools_str})

df_out = pd.DataFrame(rows)
df_out.to_excel("tools_list_by_part.xlsx", index=False)
```

