"""
Recent Critical Attacks Component
Replaces terminal feed with clean, professional table
"""

import streamlit as st
import pandas as pd

COLORS = {
    'cyan': '#4dd0e1',
    'purple': '#7b2ff7',
    'pink': '#ff006e',
    'green': '#00ff88',
    'orange': '#ffaa00',
}

def create_recent_attacks_table(df, n=10):
    """
    Create clean table showing top N critical attacks
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
    n : int
        Number of attacks to show
        
    Returns:
    --------
    str
        HTML for recent attacks table
    """
    
    # Get top attacks by financial loss
    top_attacks = df.nlargest(n, 'Financial Loss (in Million $)')
    
    table_html = f"""
    <div style="
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(77, 208, 225, 0.3);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    ">
        <div style="
            color: {COLORS['cyan']};
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
            font-family: 'Orbitron', sans-serif;
        ">
            🚨 TOP {n} CRITICAL ATTACKS BY FINANCIAL IMPACT
        </div>
        
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: rgba(77, 208, 225, 0.1); border-bottom: 2px solid {COLORS['cyan']};">
                    <th style="padding: 12px; text-align: left; color: {COLORS['cyan']}; font-weight: 600;">Year</th>
                    <th style="padding: 12px; text-align: left; color: {COLORS['cyan']}; font-weight: 600;">Country</th>
                    <th style="padding: 12px; text-align: left; color: {COLORS['cyan']}; font-weight: 600;">Attack Type</th>
                    <th style="padding: 12px; text-align: left; color: {COLORS['cyan']}; font-weight: 600;">Industry</th>
                    <th style="padding: 12px; text-align: right; color: {COLORS['cyan']}; font-weight: 600;">Loss ($M)</th>
                    <th style="padding: 12px; text-align: right; color: {COLORS['cyan']}; font-weight: 600;">Affected Users</th>
                    <th style="padding: 12px; text-align: center; color: {COLORS['cyan']}; font-weight: 600;">Severity</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, row in top_attacks.iterrows():
        # Determine severity color
        severity_score = row.get('Severity_Score', row['Financial Loss (in Million $)'] / 10)
        if severity_score >= 8:
            severity_color = COLORS['pink']
            severity_icon = '🔴'
            severity_label = 'CRITICAL'
        elif severity_score >= 5:
            severity_color = COLORS['orange']
            severity_icon = '🟡'
            severity_label = 'HIGH'
        else:
            severity_color = COLORS['green']
            severity_icon = '🟢'
            severity_label = 'MEDIUM'
        
        table_html += f"""
            <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.1); transition: background 0.3s;" 
                onmouseover="this.style.background='rgba(77, 208, 225, 0.05)'" 
                onmouseout="this.style.background='transparent'">
                <td style="padding: 12px; color: white;">{row['Year']}</td>
                <td style="padding: 12px; color: {COLORS['purple']}; font-weight: 600;">{row['Country']}</td>
                <td style="padding: 12px; color: {COLORS['pink']};">{row['Attack Type']}</td>
                <td style="padding: 12px; color: #b8c5d6;">{row['Target Industry']}</td>
                <td style="padding: 12px; text-align: right; color: {COLORS['orange']}; font-weight: bold;">
                    ${row['Financial Loss (in Million $)']:.2f}M
                </td>
                <td style="padding: 12px; text-align: right; color: white;">
                    {row['Number of Affected Users']:,}
                </td>
                <td style="padding: 12px; text-align: center;">
                    <span style="
                        background: rgba(255, 255, 255, 0.1);
                        padding: 4px 12px;
                        border-radius: 20px;
                        color: {severity_color};
                        font-size: 11px;
                        font-weight: 600;
                        border: 1px solid {severity_color};
                    ">
                        {severity_icon} {severity_label}
                    </span>
                </td>
            </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    return table_html

def create_attack_summary_cards(df):
    """Create summary cards for quick insights"""
    
    total_loss = df['Financial Loss (in Million $)'].sum()
    total_users = df['Number of Affected Users'].sum()
    avg_resolution = df['Incident Resolution Time (in Hours)'].mean()
    most_targeted = df['Target Industry'].mode()[0] if len(df) > 0 else 'N/A'
    
    cards_html = f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px;">
        <div style="
            background: rgba(255, 0, 110, 0.1);
            border: 1px solid {COLORS['pink']};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        ">
            <div style="color: {COLORS['pink']}; font-size: 12px; font-weight: 600;">TOTAL LOSS</div>
            <div style="color: white; font-size: 24px; font-weight: bold; margin-top: 5px;">
                ${total_loss/1000:.1f}B
            </div>
        </div>
        
        <div style="
            background: rgba(123, 47, 247, 0.1);
            border: 1px solid {COLORS['purple']};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        ">
            <div style="color: {COLORS['purple']}; font-size: 12px; font-weight: 600;">AFFECTED USERS</div>
            <div style="color: white; font-size: 24px; font-weight: bold; margin-top: 5px;">
                {total_users/1000000:.1f}M
            </div>
        </div>
        
        <div style="
            background: rgba(255, 170, 0, 0.1);
            border: 1px solid {COLORS['orange']};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        ">
            <div style="color: {COLORS['orange']}; font-size: 12px; font-weight: 600;">AVG RESOLUTION</div>
            <div style="color: white; font-size: 24px; font-weight: bold; margin-top: 5px;">
                {avg_resolution:.0f}h
            </div>
        </div>
        
        <div style="
            background: rgba(77, 208, 225, 0.1);
            border: 1px solid {COLORS['cyan']};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        ">
            <div style="color: {COLORS['cyan']}; font-size: 12px; font-weight: 600;">TOP TARGET</div>
            <div style="color: white; font-size: 18px; font-weight: bold; margin-top: 5px;">
                {most_targeted}
            </div>
        </div>
    </div>
    """
    
    return cards_html
