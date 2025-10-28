import pandas as pd
import numpy as np

# Sample DataFrame simulating data read from an Excel file (with some missing values)
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', None, 'Dave', 'Eve'],
    'Age': [24, None, 30, None, 45],
    'City': ['New York', 'Los Angeles', 'New York', None, 'Chicago']
})
print("Original DataFrame:")
print(df)

# Fill missing 'Age' with the average age, and missing 'Name'/'City' with 'Unknown'
df.fillna({'Age': df['Age'].mean(), 'Name': 'Unknown', 'City': 'Unknown'}, inplace=True)
print("\nDataFrame after fillna:")
print(df)

# Use str.contains to find rows where 'City' contains the substring "York"
mask = df['City'].str.contains('York', na=False)
print("\nRows where 'City' contains 'York':")
print(df[mask])