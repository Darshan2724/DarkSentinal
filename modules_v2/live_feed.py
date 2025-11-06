"""
Live Attack Feed Module
Terminal-style scrolling feed of recent attacks
"""

import streamlit as st
import pandas as pd
from datetime import datetime

COLORS = {
    'cyan': '#00f5ff',
    'purple': '#7b2ff7',
    'pink': '#ff006e',
    'green': '#00ff88',
    'orange': '#ffaa00',
}

def create_terminal_feed(df, n_recent=20):
    """
    Create terminal-style live attack feed
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
    n_recent : int
        Number of recent attacks to show
        
    Returns:
    --------
    str
        HTML for terminal feed
    """
    
    # Get most recent attacks
    recent_attacks = df.nlargest(n_recent, 'timestamp')
    
    feed_html = f"""
    <div style="
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid {COLORS['cyan']};
        border-radius: 10px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
    ">
        <div style="color: {COLORS['cyan']}; font-weight: bold; margin-bottom: 15px; font-size: 16px;">
            🖥️ LIVE ATTACK FEED - TERMINAL MODE
        </div>
        <div style="color: {COLORS['green']}; margin-bottom: 10px;">
            ┌─[darksentinel@security]─[~]
        </div>
    """
    
    for idx, attack in recent_attacks.iterrows():
        # Determine severity color
        severity = attack['attack_severity']
        if severity >= 8:
            sev_color = COLORS['pink']
            sev_icon = '🔴'
        elif severity >= 5:
            sev_color = COLORS['orange']
            sev_icon = '🟡'
        else:
            sev_color = COLORS['green']
            sev_icon = '🟢'
        
        # Determine outcome color
        outcome_color = COLORS['pink'] if attack['outcome'] == 'Success' else COLORS['green']
        outcome_icon = '⚠️' if attack['outcome'] == 'Success' else '✓'
        
        timestamp_str = attack['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        feed_html += f"""
        <div style="margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.02); border-left: 3px solid {sev_color}; border-radius: 5px;">
            <div style="color: {COLORS['cyan']};">
                └─$ [{timestamp_str}] {sev_icon} SEVERITY: {severity}/10
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ TYPE: <span style="color: {COLORS['pink']};">{attack['attack_type']}</span>
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ TARGET: <span style="color: white;">{attack['target_system']}</span> @ {attack['location']}
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ SOURCE: <span style="color: {COLORS['orange']};">{attack['attacker_ip']}</span> → {attack['target_ip']}
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ DATA LOSS: <span style="color: {COLORS['pink']};">{attack['data_compromised_GB']:.2f} GB</span>
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ DURATION: {attack['attack_duration_min']} min | RESPONSE: {attack['response_time_min']} min
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                ├─ MITIGATION: <span style="color: {COLORS['green']};">{attack['mitigation_method']}</span>
            </div>
            <div style="color: {COLORS['purple']}; margin-left: 20px;">
                └─ STATUS: <span style="color: {outcome_color};">{outcome_icon} {attack['outcome']}</span>
            </div>
        </div>
        """
    
    feed_html += """
        <div style="color: #00ff88; margin-top: 15px;">
            └─[EOF] End of feed
        </div>
    </div>
    
    <style>
        /* Custom scrollbar for terminal */
        div::-webkit-scrollbar {
            width: 8px;
        }
        div::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.5);
        }
        div::-webkit-scrollbar-thumb {
            background: #00f5ff;
            border-radius: 4px;
        }
        div::-webkit-scrollbar-thumb:hover {
            background: #7b2ff7;
        }
    </style>
    """
    
    return feed_html

def create_attack_ticker(df, n_items=5):
    """
    Create scrolling ticker of critical attacks
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
    n_items : int
        Number of items in ticker
        
    Returns:
    --------
    str
        HTML for ticker
    """
    
    # Get critical attacks (severity >= 8)
    critical = df[df['attack_severity'] >= 8].nlargest(n_items, 'timestamp')
    
    ticker_items = []
    for idx, attack in critical.iterrows():
        ticker_items.append(
            f"🚨 {attack['attack_type']} on {attack['target_system']} "
            f"in {attack['location']} - {attack['data_compromised_GB']:.1f}GB lost"
        )
    
    ticker_text = " | ".join(ticker_items)
    
    ticker_html = f"""
    <div style="
        background: linear-gradient(90deg, rgba(255, 0, 110, 0.2), rgba(123, 47, 247, 0.2));
        border: 1px solid {COLORS['pink']};
        border-radius: 10px;
        padding: 15px;
        overflow: hidden;
        white-space: nowrap;
        position: relative;
    ">
        <div style="
            display: inline-block;
            padding-left: 100%;
            animation: scroll-left 30s linear infinite;
            color: white;
            font-weight: 600;
            font-size: 14px;
        ">
            {ticker_text}
        </div>
    </div>
    
    <style>
        @keyframes scroll-left {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-100%); }}
        }}
    </style>
    """
    
    return ticker_html

def create_status_board(df):
    """
    Create real-time status board
    
    Parameters:
    -----------
    df : pd.DataFrame
        Attack data
        
    Returns:
    --------
    str
        HTML for status board
    """
    
    # Calculate real-time stats
    total_attacks = len(df)
    active_threats = (df['outcome'] == 'Success').sum()
    critical_count = (df['attack_severity'] >= 8).sum()
    total_data_loss = df['data_compromised_GB'].sum()
    
    # Threat level calculation
    threat_percentage = (active_threats / total_attacks * 100) if total_attacks > 0 else 0
    
    if threat_percentage >= 70:
        threat_level = "CRITICAL"
        threat_color = COLORS['pink']
        threat_icon = "🔴"
    elif threat_percentage >= 40:
        threat_level = "ELEVATED"
        threat_color = COLORS['orange']
        threat_icon = "🟡"
    else:
        threat_level = "MODERATE"
        threat_color = COLORS['green']
        threat_icon = "🟢"
    
    status_html = f"""
    <div style="
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid {threat_color};
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 30px {threat_color};
    ">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 48px;">{threat_icon}</div>
            <div style="color: {threat_color}; font-size: 24px; font-weight: bold; margin-top: 10px;">
                THREAT LEVEL: {threat_level}
            </div>
            <div style="color: {COLORS['cyan']}; font-size: 14px; margin-top: 5px;">
                System Status: OPERATIONAL
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 3px solid {COLORS['cyan']};">
                <div style="color: {COLORS['cyan']}; font-size: 12px;">TOTAL ATTACKS</div>
                <div style="color: white; font-size: 28px; font-weight: bold;">{total_attacks:,}</div>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 3px solid {COLORS['pink']};">
                <div style="color: {COLORS['pink']}; font-size: 12px;">SUCCESSFUL ATTACKS</div>
                <div style="color: white; font-size: 28px; font-weight: bold;">{active_threats:,}</div>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 3px solid {COLORS['orange']};">
                <div style="color: {COLORS['orange']}; font-size: 12px;">CRITICAL SEVERITY</div>
                <div style="color: white; font-size: 28px; font-weight: bold;">{critical_count:,}</div>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border-left: 3px solid {COLORS['purple']};">
                <div style="color: {COLORS['purple']}; font-size: 12px;">DATA COMPROMISED</div>
                <div style="color: white; font-size: 28px; font-weight: bold;">{total_data_loss/1024:.1f} TB</div>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding: 10px; background: rgba(0, 245, 255, 0.1); border-radius: 8px; text-align: center;">
            <div style="color: {COLORS['cyan']}; font-size: 12px;">
                ⚡ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </div>
    """
    
    return status_html
