"""
Data Loader for Global Cybersecurity Threats 2015-2024
Handles loading and preprocessing of the global threat dataset
"""

import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data(ttl=3600)
def load_global_data(file_path='Global_Cybersecurity_Threats_2015-2024_LARGE.csv'):
    """
    Load global cybersecurity threat data from CSV file
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame
        Loaded and processed dataframe
    """
    try:
        df = pd.read_csv(file_path)
        
        # Create datetime column from Year
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
        
        # Add severity categories based on financial loss
        df['Severity_Category'] = pd.cut(
            df['Financial Loss (in Million $)'],
            bins=[0, 25, 50, 75, 100],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        # Add severity score (1-10) based on financial loss
        df['Severity_Score'] = (df['Financial Loss (in Million $)'] / 10).clip(1, 10).round(1)
        
        # Add resolution efficiency category
        df['Resolution_Category'] = pd.cut(
            df['Incident Resolution Time (in Hours)'],
            bins=[0, 24, 48, 72],
            labels=['Fast', 'Moderate', 'Slow']
        )
        
        # Add impact score (combination of financial loss and affected users)
        df['Impact_Score'] = (
            (df['Financial Loss (in Million $)'] / df['Financial Loss (in Million $)'].max()) * 50 +
            (df['Number of Affected Users'] / df['Number of Affected Users'].max()) * 50
        ).round(2)
        
        return df
        
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {file_path}")
        st.info("Please ensure 'Global_Cybersecurity_Threats_2015-2024.csv' is in the project directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

def get_data_summary(df):
    """
    Get comprehensive summary statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Summary statistics
    """
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'year_range_start': df['Year'].min(),
        'year_range_end': df['Year'].max(),
        'total_years': df['Year'].max() - df['Year'].min() + 1,
        'unique_countries': df['Country'].nunique(),
        'unique_attack_types': df['Attack Type'].nunique(),
        'total_financial_loss_billion': df['Financial Loss (in Million $)'].sum() / 1000,
        'avg_financial_loss_million': df['Financial Loss (in Million $)'].mean(),
        'total_affected_users': df['Number of Affected Users'].sum(),
        'avg_resolution_time_hours': df['Incident Resolution Time (in Hours)'].mean(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024**2)
    }
    return summary

def get_attack_statistics(df):
    """
    Get detailed attack statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Attack statistics
    """
    stats = {
        'by_country': df['Country'].value_counts().to_dict(),
        'by_attack_type': df['Attack Type'].value_counts().to_dict(),
        'by_industry': df['Target Industry'].value_counts().to_dict(),
        'by_source': df['Attack Source'].value_counts().to_dict(),
        'by_vulnerability': df['Security Vulnerability Type'].value_counts().to_dict(),
        'by_defense': df['Defense Mechanism Used'].value_counts().to_dict(),
        'by_year': df['Year'].value_counts().sort_index().to_dict(),
        'by_severity': df['Severity_Category'].value_counts().to_dict(),
    }
    return stats

def filter_data(df, filters):
    """
    Apply multiple filters to dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    filters : dict
        Filter criteria
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    filtered = df.copy()
    
    if filters.get('year_range'):
        start_year, end_year = filters['year_range']
        filtered = filtered[
            (filtered['Year'] >= start_year) &
            (filtered['Year'] <= end_year)
        ]
    
    if filters.get('countries'):
        filtered = filtered[filtered['Country'].isin(filters['countries'])]
    
    if filters.get('attack_types'):
        filtered = filtered[filtered['Attack Type'].isin(filters['attack_types'])]
    
    if filters.get('industries'):
        filtered = filtered[filtered['Target Industry'].isin(filters['industries'])]
    
    if filters.get('sources'):
        filtered = filtered[filtered['Attack Source'].isin(filters['sources'])]
    
    if filters.get('vulnerabilities'):
        filtered = filtered[filtered['Security Vulnerability Type'].isin(filters['vulnerabilities'])]
    
    if filters.get('defense_mechanisms'):
        filtered = filtered[filtered['Defense Mechanism Used'].isin(filters['defense_mechanisms'])]
    
    if filters.get('severity_categories'):
        filtered = filtered[filtered['Severity_Category'].isin(filters['severity_categories'])]
    
    return filtered

def get_top_threats(df, n=10):
    """
    Get top N threats by various criteria
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    n : int
        Number of top items to return
        
    Returns:
    --------
    dict
        Top threats
    """
    return {
        'by_financial_loss': df.nlargest(n, 'Financial Loss (in Million $)')[
            ['Year', 'Country', 'Attack Type', 'Target Industry', 'Financial Loss (in Million $)', 'Number of Affected Users']
        ].to_dict('records'),
        'by_affected_users': df.nlargest(n, 'Number of Affected Users')[
            ['Year', 'Country', 'Attack Type', 'Target Industry', 'Number of Affected Users', 'Financial Loss (in Million $)']
        ].to_dict('records'),
        'by_resolution_time': df.nlargest(n, 'Incident Resolution Time (in Hours)')[
            ['Year', 'Country', 'Attack Type', 'Incident Resolution Time (in Hours)', 'Defense Mechanism Used']
        ].to_dict('records'),
        'by_impact_score': df.nlargest(n, 'Impact_Score')[
            ['Year', 'Country', 'Attack Type', 'Target Industry', 'Impact_Score', 'Financial Loss (in Million $)']
        ].to_dict('records'),
    }

def get_yearly_trends(df):
    """
    Get year-over-year trends
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Yearly aggregated data
    """
    yearly = df.groupby('Year').agg({
        'Attack Type': 'count',
        'Financial Loss (in Million $)': 'sum',
        'Number of Affected Users': 'sum',
        'Incident Resolution Time (in Hours)': 'mean'
    }).reset_index()
    
    yearly.columns = ['Year', 'Total_Attacks', 'Total_Financial_Loss', 'Total_Affected_Users', 'Avg_Resolution_Time']
    
    return yearly

def get_defense_effectiveness(df):
    """
    Calculate defense mechanism effectiveness
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Defense effectiveness metrics
    """
    defense_stats = df.groupby('Defense Mechanism Used').agg({
        'Attack Type': 'count',
        'Financial Loss (in Million $)': 'mean',
        'Number of Affected Users': 'mean',
        'Incident Resolution Time (in Hours)': 'mean'
    }).reset_index()
    
    defense_stats.columns = ['Defense_Mechanism', 'Attack_Count', 'Avg_Financial_Loss', 'Avg_Affected_Users', 'Avg_Resolution_Time']
    
    # Calculate effectiveness score (lower is better)
    # Normalize metrics and create composite score
    defense_stats['Effectiveness_Score'] = (
        (1 - defense_stats['Avg_Financial_Loss'] / defense_stats['Avg_Financial_Loss'].max()) * 40 +
        (1 - defense_stats['Avg_Affected_Users'] / defense_stats['Avg_Affected_Users'].max()) * 30 +
        (1 - defense_stats['Avg_Resolution_Time'] / defense_stats['Avg_Resolution_Time'].max()) * 30
    ).round(2)
    
    return defense_stats.sort_values('Effectiveness_Score', ascending=False)
