# [lambda式] ["1", "2", "3"] format

How to make lambda expression in the format ["1", "2", "3"]
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

