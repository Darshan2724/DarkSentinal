import pandas as pd

df = pd.read_csv('cybersecurity_large_synthesized_data.csv')

print(f'Total Records: {len(df):,}')
print(f'\nColumns ({len(df.columns)}):')
for col in df.columns:
    print(f'  - {col}')

print(f'\nData Types:')
print(df.dtypes)

print(f'\nDate Range:')
print(f'  From: {df["timestamp"].min()}')
print(f'  To: {df["timestamp"].max()}')

print(f'\nUnique Values:')
print(f'  Attack Types: {df["attack_type"].nunique()} - {sorted(df["attack_type"].unique())}')
print(f'  Target Systems: {df["target_system"].nunique()} - {sorted(df["target_system"].unique())}')
print(f'  Locations: {df["location"].nunique()} - {sorted(df["location"].unique())}')
print(f'  Industries: {df["industry"].nunique()} - {sorted(df["industry"].unique())}')
print(f'  Outcomes: {df["outcome"].nunique()} - {sorted(df["outcome"].unique())}')
print(f'  User Roles: {df["user_role"].nunique()} - {sorted(df["user_role"].unique())}')
print(f'  Security Tools: {df["security_tools_used"].nunique()} - {sorted(df["security_tools_used"].unique())}')
print(f'  Mitigation Methods: {df["mitigation_method"].nunique()} - {sorted(df["mitigation_method"].unique())}')

print(f'\nNumerical Statistics:')
print(f'  Data Compromised (GB): {df["data_compromised_GB"].min():.2f} - {df["data_compromised_GB"].max():.2f} (avg: {df["data_compromised_GB"].mean():.2f})')
print(f'  Attack Duration (min): {df["attack_duration_min"].min():.0f} - {df["attack_duration_min"].max():.0f} (avg: {df["attack_duration_min"].mean():.0f})')
print(f'  Attack Severity: {df["attack_severity"].min()} - {df["attack_severity"].max()} (avg: {df["attack_severity"].mean():.1f})')
print(f'  Response Time (min): {df["response_time_min"].min():.0f} - {df["response_time_min"].max():.0f} (avg: {df["response_time_min"].mean():.0f})')

print(f'\nMissing Values:')
print(df.isnull().sum())
