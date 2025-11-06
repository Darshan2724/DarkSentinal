"""
Data Loader Module for DarkSentinel
Handles loading and initial validation of cybersecurity attack data
"""

import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data(file_path='cybersecurity_attacks.csv'):
    """
    Load cybersecurity attack data from CSV file
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing attack data
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe with attack data
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {file_path}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

def get_data_summary(df):
    """
    Get basic summary statistics of the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Dictionary containing summary statistics
    """
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'date_range': (df['Timestamp'].min(), df['Timestamp'].max()) if 'Timestamp' in df.columns else None,
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    return summary
