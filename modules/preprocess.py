"""
Data Preprocessing Module for DarkSentinel
Handles data cleaning, transformation, and feature engineering
"""

import pandas as pd
import re
import streamlit as st

@st.cache_data
def preprocess_data(df):
    """
    Preprocess the cybersecurity attack data
    Applies all cleaning and feature engineering steps from the notebook
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataframe
        
    Returns:
    --------
    pd.DataFrame
        Preprocessed dataframe
    """
    # Create a copy to avoid modifying original
    data = df.copy()
    
    # Handle Alerts/Warnings column
    data['Alerts/Warnings'] = data['Alerts/Warnings'].apply(
        lambda x: 'Alert Triggered' if x == 'Alert Triggered' else 'None'
    )
    
    # Replace NaN values with meaningful placeholders
    data['IDS/IPS Alerts'] = data['IDS/IPS Alerts'].apply(
        lambda x: 'No Data' if pd.isna(x) else x
    )
    
    data['Malware Indicators'] = data['Malware Indicators'].apply(
        lambda x: 'No Detection' if pd.isna(x) else x
    )
    
    data['Firewall Logs'] = data['Firewall Logs'].apply(
        lambda x: 'No Data' if pd.isna(x) else x
    )
    
    data['Proxy Information'] = data['Proxy Information'].apply(
        lambda x: 'No Proxy Data' if pd.isna(x) else x
    )
    
    # Extract Device/OS from Device Information
    data['Device/OS'] = data['Device Information'].apply(extract_device_os)
    
    # Extract Browser from Device Information
    data['Browser'] = data['Device Information'].str.split('/').str[0]
    
    # Convert Timestamp to datetime
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    
    # Extract time-based features
    data['Year'] = data['Timestamp'].dt.year
    data['Month'] = data['Timestamp'].dt.month
    data['MonthName'] = data['Timestamp'].dt.month_name()
    data['DayofWeek'] = data['Timestamp'].dt.dayofweek
    data['DayName'] = data['Timestamp'].dt.day_name()
    data['Day'] = data['Timestamp'].dt.day
    data['Hour'] = data['Timestamp'].dt.hour
    data['Minute'] = data['Timestamp'].dt.minute
    data['Second'] = data['Timestamp'].dt.second
    data['Date'] = data['Timestamp'].dt.date
    
    # Extract City and State from Geo-location Data
    if 'Geo-location Data' in data.columns:
        geo_split = data['Geo-location Data'].str.split(',', expand=True)
        data['City'] = geo_split[0].str.strip() if len(geo_split.columns) > 0 else None
        data['State'] = geo_split[1].str.strip() if len(geo_split.columns) > 1 else None
    
    return data

def extract_device_os(user_agent):
    """
    Extract device/OS information from user agent string
    
    Parameters:
    -----------
    user_agent : str
        User agent string
        
    Returns:
    --------
    str
        Detected device/OS or 'Unknown'
    """
    devices = [
        r'Windows',
        r'Linux',
        r'Android',
        r'iPad',
        r'iPod',
        r'iPhone',
        r'Macintosh'
    ]
    
    for device in devices:
        match_device = re.search(device, user_agent, re.I)
        if match_device:
            return match_device.group()
    
    return 'Unknown'

def filter_data(df, filters):
    """
    Apply filters to the dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    filters : dict
        Dictionary containing filter criteria
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    filtered = df.copy()
    
    if filters.get('years') and len(filters['years']) > 0:
        filtered = filtered[filtered['Year'].isin(filters['years'])]
    
    if filters.get('months') and len(filters['months']) > 0:
        filtered = filtered[filtered['Month'].isin(filters['months'])]
    
    if filters.get('attack_types') and len(filters['attack_types']) > 0:
        filtered = filtered[filtered['Attack Type'].isin(filters['attack_types'])]
    
    if filters.get('severity_levels') and len(filters['severity_levels']) > 0:
        filtered = filtered[filtered['Severity Level'].isin(filters['severity_levels'])]
    
    if filters.get('devices') and len(filters['devices']) > 0:
        filtered = filtered[filtered['Device/OS'].isin(filters['devices'])]
    
    if filters.get('protocols') and len(filters['protocols']) > 0:
        filtered = filtered[filtered['Protocol'].isin(filters['protocols'])]
    
    if filters.get('actions') and len(filters['actions']) > 0:
        filtered = filtered[filtered['Action Taken'].isin(filters['actions'])]
    
    return filtered
