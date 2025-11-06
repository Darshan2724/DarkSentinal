import pandas as pd

df = pd.read_csv('Global_Cybersecurity_Threats_2015-2024.csv')

print("="*60)
print("DATASET ANALYSIS - Global Cybersecurity Threats 2015-2024")
print("="*60)

print(f'\n📊 BASIC INFO:')
print(f'Total Records: {len(df):,}')
print(f'Total Columns: {len(df.columns)}')
print(f'Memory Usage: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB')

print(f'\n📅 DATE RANGE:')
print(f'Years Covered: {sorted(df["Year"].unique())}')
print(f'Year Range: {df["Year"].min()} - {df["Year"].max()}')
print(f'Total Years: {df["Year"].max() - df["Year"].min() + 1}')

print(f'\n📋 COLUMNS:')
for i, col in enumerate(df.columns, 1):
    print(f'  {i}. {col}')

print(f'\n🔢 DATA TYPES:')
print(df.dtypes)

print(f'\n📈 UNIQUE VALUES:')
print(f'Countries: {df["Country"].nunique()} - {sorted(df["Country"].unique())}')
print(f'Attack Types: {df["Attack Type"].nunique()} - {sorted(df["Attack Type"].unique())}')
print(f'Target Industries: {df["Target Industry"].nunique()} - {sorted(df["Target Industry"].unique())}')
print(f'Attack Sources: {df["Attack Source"].nunique()} - {sorted(df["Attack Source"].unique())}')
print(f'Vulnerabilities: {df["Security Vulnerability Type"].nunique()} - {sorted(df["Security Vulnerability Type"].unique())}')
print(f'Defense Mechanisms: {df["Defense Mechanism Used"].nunique()} - {sorted(df["Defense Mechanism Used"].unique())}')

print(f'\n💰 NUMERICAL STATISTICS:')
print(f'Financial Loss (Million $):')
print(f'  Min: ${df["Financial Loss (in Million $)"].min():.2f}M')
print(f'  Max: ${df["Financial Loss (in Million $)"].max():.2f}M')
print(f'  Mean: ${df["Financial Loss (in Million $)"].mean():.2f}M')
print(f'  Total: ${df["Financial Loss (in Million $)"].sum():.2f}M')

print(f'\nAffected Users:')
print(f'  Min: {df["Number of Affected Users"].min():,}')
print(f'  Max: {df["Number of Affected Users"].max():,}')
print(f'  Mean: {df["Number of Affected Users"].mean():,.0f}')
print(f'  Total: {df["Number of Affected Users"].sum():,}')

print(f'\nResolution Time (Hours):')
print(f'  Min: {df["Incident Resolution Time (in Hours)"].min():.0f}h')
print(f'  Max: {df["Incident Resolution Time (in Hours)"].max():.0f}h')
print(f'  Mean: {df["Incident Resolution Time (in Hours)"].mean():.0f}h')

print(f'\n❌ MISSING VALUES:')
print(df.isnull().sum())

print(f'\n🔝 TOP 5 BY CATEGORY:')
print(f'\nTop 5 Countries by Attack Count:')
print(df['Country'].value_counts().head())

print(f'\nTop 5 Attack Types:')
print(df['Attack Type'].value_counts().head())

print(f'\nTop 5 Target Industries:')
print(df['Target Industry'].value_counts().head())

print(f'\nTop 5 Years by Attack Count:')
print(df['Year'].value_counts().sort_index(ascending=False).head())

print("\n" + "="*60)
