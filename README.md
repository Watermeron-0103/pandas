# pandas
project
<pre>```python</pre>
import pandas as pd
import json


file_path = "src/佐野受検マスタS-235(20250610).xlsx"
df = pd.read_excel(file_path, sheet_name=0)

tool_dict = df.groupby('検査計画書品番')["測定具"].apply(lambda x: [i for i in x if pd.notna(i)]).to_dict()

rows = []
for part_no, tools in tool_dict.items():
    tools_str = json.dumps(tools, ensure_ascii=False)
    rows.append({'検査計画書品番': part_no, '検査具リスト': tools_str})

df_out = pd.DataFrame(rows)
df_out.to_excel("tools_list_by_part.xlsx", index=False)
