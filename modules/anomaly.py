"""
Anomaly Detection Module for DarkSentinel
Implements machine learning-based anomaly detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import streamlit as st

@st.cache_resource
def train_anomaly_detector(df, contamination=0.1):
    """
    Train Isolation Forest model for anomaly detection
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with features
    contamination : float
        Expected proportion of outliers in the dataset
        
    Returns:
    --------
    tuple
        (model, scaler, feature_columns)
    """
    # Select numerical features for anomaly detection
    feature_columns = ['Anomaly Scores', 'Packet Length', 'Source Port', 'Destination Port']
    
    # Prepare features
    X = df[feature_columns].copy()
    
    # Handle any missing values
    X = X.fillna(X.mean())
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    model.fit(X_scaled)
    
    return model, scaler, feature_columns

def detect_anomalies(df, model, scaler, feature_columns):
    """
    Detect anomalies in the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    model : IsolationForest
        Trained anomaly detection model
    scaler : StandardScaler
        Fitted scaler
    feature_columns : list
        List of feature column names
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with anomaly predictions (-1 for anomaly, 1 for normal)
    """
    # Prepare features
    X = df[feature_columns].copy()
    X = X.fillna(X.mean())
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Predict anomalies
    predictions = model.predict(X_scaled)
    
    # Add predictions to dataframe
    result_df = df.copy()
    result_df['Anomaly'] = predictions
    result_df['Is_Anomaly'] = result_df['Anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')
    
    # Calculate anomaly scores
    anomaly_scores = model.score_samples(X_scaled)
    result_df['ML_Anomaly_Score'] = -anomaly_scores  # Invert so higher = more anomalous
    
    return result_df

def get_anomaly_summary(df_with_anomalies):
    """
    Get summary statistics of detected anomalies
    
    Parameters:
    -----------
    df_with_anomalies : pd.DataFrame
        Dataframe with anomaly predictions
        
    Returns:
    --------
    dict
        Summary statistics
    """
    total_records = len(df_with_anomalies)
    anomaly_count = (df_with_anomalies['Anomaly'] == -1).sum()
    anomaly_percentage = (anomaly_count / total_records) * 100
    
    summary = {
        'total_records': total_records,
        'anomaly_count': anomaly_count,
        'normal_count': total_records - anomaly_count,
        'anomaly_percentage': anomaly_percentage
    }
    
    return summary

def get_top_anomalies(df_with_anomalies, n=10):
    """
    Get top N most anomalous records
    
    Parameters:
    -----------
    df_with_anomalies : pd.DataFrame
        Dataframe with anomaly predictions
    n : int
        Number of top anomalies to return
        
    Returns:
    --------
    pd.DataFrame
        Top N anomalous records
    """
    anomalies = df_with_anomalies[df_with_anomalies['Anomaly'] == -1]
    top_anomalies = anomalies.nlargest(n, 'ML_Anomaly_Score')
    
    return top_anomalies

def get_anomaly_by_attack_type(df_with_anomalies):
    """
    Get anomaly distribution by attack type
    
    Parameters:
    -----------
    df_with_anomalies : pd.DataFrame
        Dataframe with anomaly predictions
        
    Returns:
    --------
    pd.DataFrame
        Anomaly counts by attack type
    """
    anomaly_by_type = df_with_anomalies[df_with_anomalies['Anomaly'] == -1].groupby('Attack Type').size().reset_index(name='count')
    anomaly_by_type = anomaly_by_type.sort_values('count', ascending=False)
    
    return anomaly_by_type

def detect_threshold_anomalies(df, threshold_multiplier=2):
    """
    Detect anomalies based on threshold (mean + n*std)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    threshold_multiplier : float
        Multiplier for standard deviation
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with threshold-based anomaly flags
    """
    result_df = df.copy()
    
    mean_score = df['Anomaly Scores'].mean()
    std_score = df['Anomaly Scores'].std()
    threshold = mean_score + threshold_multiplier * std_score
    
    result_df['Threshold_Anomaly'] = result_df['Anomaly Scores'] > threshold
    result_df['Anomaly_Threshold'] = threshold
    
    return result_df

def get_anomaly_insights(df_with_anomalies):
    """
    Generate insights about detected anomalies
    
    Parameters:
    -----------
    df_with_anomalies : pd.DataFrame
        Dataframe with anomaly predictions
        
    Returns:
    --------
    dict
        Dictionary containing various insights
    """
    anomalies = df_with_anomalies[df_with_anomalies['Anomaly'] == -1]
    
    insights = {
        'most_common_attack_type': anomalies['Attack Type'].mode()[0] if len(anomalies) > 0 else 'N/A',
        'most_common_severity': anomalies['Severity Level'].mode()[0] if len(anomalies) > 0 else 'N/A',
        'most_common_device': anomalies['Device/OS'].mode()[0] if len(anomalies) > 0 else 'N/A',
        'most_common_protocol': anomalies['Protocol'].mode()[0] if len(anomalies) > 0 else 'N/A',
        'avg_packet_length': anomalies['Packet Length'].mean() if len(anomalies) > 0 else 0,
        'avg_anomaly_score': anomalies['Anomaly Scores'].mean() if len(anomalies) > 0 else 0
    }
    
    return insights
