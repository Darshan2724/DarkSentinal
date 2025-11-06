"""
Generate Large Cybersecurity Threats Dataset (50,000+ records)
Maintains same structure as original but with more realistic volume
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define all possible values (same as original)
COUNTRIES = ['Australia', 'Brazil', 'China', 'France', 'Germany', 'India', 'Japan', 'Russia', 'UK', 'USA']

ATTACK_TYPES = ['DDoS', 'Malware', 'Man-in-the-Middle', 'Phishing', 'Ransomware', 'SQL Injection']

TARGET_INDUSTRIES = ['Banking', 'Education', 'Government', 'Healthcare', 'IT', 'Retail', 'Telecommunications']

ATTACK_SOURCES = ['Hacker Group', 'Insider', 'Nation-state', 'Unknown']

VULNERABILITIES = ['Social Engineering', 'Unpatched Software', 'Weak Passwords', 'Zero-day']

DEFENSE_MECHANISMS = ['AI-based Detection', 'Antivirus', 'Encryption', 'Firewall', 'VPN']

# Generate 50,000 records
NUM_RECORDS = 50000

print(f"Generating {NUM_RECORDS:,} cybersecurity attack records...")
print("This may take a few minutes...\n")

# Generate data
data = {
    'Country': [],
    'Year': [],
    'Attack Type': [],
    'Target Industry': [],
    'Financial Loss (in Million $)': [],
    'Number of Affected Users': [],
    'Attack Source': [],
    'Security Vulnerability Type': [],
    'Defense Mechanism Used': [],
    'Incident Resolution Time (in Hours)': []
}

# Generate records in batches for better performance
batch_size = 5000
for batch in range(NUM_RECORDS // batch_size):
    print(f"Generating batch {batch + 1}/{NUM_RECORDS // batch_size}...")
    
    for _ in range(batch_size):
        # Country (weighted towards major cyber targets)
        country_weights = [0.08, 0.10, 0.12, 0.09, 0.10, 0.11, 0.09, 0.07, 0.11, 0.13]
        country = random.choices(COUNTRIES, weights=country_weights)[0]
        
        # Year (2015-2024)
        year = random.randint(2015, 2024)
        
        # Attack Type (weighted by commonality)
        attack_weights = [0.20, 0.15, 0.10, 0.25, 0.18, 0.12]  # Phishing and DDoS most common
        attack_type = random.choices(ATTACK_TYPES, weights=attack_weights)[0]
        
        # Target Industry (weighted by attack frequency)
        industry_weights = [0.18, 0.12, 0.15, 0.14, 0.16, 0.13, 0.12]
        target_industry = random.choices(TARGET_INDUSTRIES, weights=industry_weights)[0]
        
        # Financial Loss (realistic distribution)
        # Most attacks: $0.5M - $20M (80%)
        # Medium attacks: $20M - $50M (15%)
        # Major attacks: $50M - $100M (5%)
        loss_category = random.random()
        if loss_category < 0.80:
            financial_loss = round(random.uniform(0.5, 20.0), 2)
        elif loss_category < 0.95:
            financial_loss = round(random.uniform(20.0, 50.0), 2)
        else:
            financial_loss = round(random.uniform(50.0, 99.99), 2)
        
        # Number of Affected Users (correlated with financial loss)
        if financial_loss < 10:
            affected_users = random.randint(1000, 300000)
        elif financial_loss < 30:
            affected_users = random.randint(200000, 600000)
        else:
            affected_users = random.randint(500000, 999999)
        
        # Attack Source (weighted)
        source_weights = [0.35, 0.15, 0.25, 0.25]
        attack_source = random.choices(ATTACK_SOURCES, weights=source_weights)[0]
        
        # Vulnerability Type (weighted by prevalence)
        vuln_weights = [0.35, 0.30, 0.20, 0.15]
        vulnerability = random.choices(VULNERABILITIES, weights=vuln_weights)[0]
        
        # Defense Mechanism (weighted by usage)
        defense_weights = [0.15, 0.20, 0.20, 0.25, 0.20]
        defense = random.choices(DEFENSE_MECHANISMS, weights=defense_weights)[0]
        
        # Resolution Time (correlated with attack severity)
        if financial_loss < 10:
            resolution_time = random.randint(1, 24)
        elif financial_loss < 30:
            resolution_time = random.randint(12, 48)
        else:
            resolution_time = random.randint(24, 72)
        
        # Add to data
        data['Country'].append(country)
        data['Year'].append(year)
        data['Attack Type'].append(attack_type)
        data['Target Industry'].append(target_industry)
        data['Financial Loss (in Million $)'].append(financial_loss)
        data['Number of Affected Users'].append(affected_users)
        data['Attack Source'].append(attack_source)
        data['Security Vulnerability Type'].append(vulnerability)
        data['Defense Mechanism Used'].append(defense)
        data['Incident Resolution Time (in Hours)'].append(resolution_time)

print("\nCreating DataFrame...")
df = pd.DataFrame(data)

# Shuffle the data
print("Shuffling records...")
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
output_file = 'Global_Cybersecurity_Threats_2015-2024_LARGE.csv'
print(f"\nSaving to {output_file}...")
df.to_csv(output_file, index=False)

print("\n" + "="*70)
print("✅ DATASET GENERATION COMPLETE!")
print("="*70)
print(f"\nDataset Statistics:")
print(f"  Total Records: {len(df):,}")
print(f"  Columns: {len(df.columns)}")
print(f"  File: {output_file}")
print(f"  Size: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
print(f"\nDate Range: 2015-2024")
print(f"Countries: {df['Country'].nunique()}")
print(f"Attack Types: {df['Attack Type'].nunique()}")
print(f"Industries: {df['Target Industry'].nunique()}")
print(f"\nFinancial Impact:")
print(f"  Total Loss: ${df['Financial Loss (in Million $)'].sum()/1000:.2f} Billion")
print(f"  Average Loss: ${df['Financial Loss (in Million $)'].mean():.2f} Million")
print(f"  Max Loss: ${df['Financial Loss (in Million $)'].max():.2f} Million")
print(f"\nAffected Users:")
print(f"  Total: {df['Number of Affected Users'].sum():,}")
print(f"  Average: {df['Number of Affected Users'].mean():,.0f}")
print(f"\nTop 5 Countries by Attack Count:")
print(df['Country'].value_counts().head())
print(f"\nTop 5 Attack Types:")
print(df['Attack Type'].value_counts().head())
print("\n" + "="*70)
print("✅ Ready to use with your dashboard!")
print("="*70)
