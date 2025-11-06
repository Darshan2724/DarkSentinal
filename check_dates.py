import pandas as pd

df = pd.read_csv('cybersecurity_large_synthesized_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(f'Start Date: {df["timestamp"].min()}')
print(f'End Date: {df["timestamp"].max()}')
print(f'Total Days: {(df["timestamp"].max() - df["timestamp"].min()).days}')
print(f'Years Covered: {sorted(df["timestamp"].dt.year.unique())}')
print(f'Date Range: {df["timestamp"].min().date()} to {df["timestamp"].max().date()}')
