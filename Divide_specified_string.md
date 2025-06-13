# Divide by the specified string

```python
# Get unique assignees in the 'Assignee' column
inspectors = df['記録者'].unique()

for inspector in inspectors:
    # Filter by agent
    df_inspector = df[df['記録者'] == inspector]
```

# +Create a folder for each one and store them

```python
import os
import pandas as pd


input_file = "Inspector/日報記録_YYYYMMDD.xlsx"
output_dir = "Inspector/by_inspector"

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

df = pd.read_excel(input_file)

# Get unique assignees in the 'Assignee' column
inspectors = df['記録者'].unique()

for inspector in inspectors:
    # Filter by agent
    df_inspector = df[df['記録者'] == inspector]
    # Change the file name to person_name.xlsx
    file_name = f"{inspector}.xlsx"
    # save
    df_inspector.to_excel(os.path.join(output_dir, file_name), index=False)

print("The Excel files for each inspector were saved in the by_inspector folder.")
```
