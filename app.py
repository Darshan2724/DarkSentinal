"""
DarkSentinel - Cybercrime Analytics Dashboard
Interactive Streamlit dashboard for analyzing cyber attack patterns
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import load_data, get_data_summary
from modules.preprocess import preprocess_data, filter_data
from modules import visuals
from modules.anomaly import (
    train_anomaly_detector, detect_anomalies, get_anomaly_summary,
    get_top_anomalies, detect_threshold_anomalies, get_anomaly_insights
)

# Page configuration
st.set_page_config(
    page_title="DarkSentinel | Cyber Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cyber-dark theme
st.markdown("""
<style>
    .main {
        background-color: #0b0f14;
        color: #d0d7de;
    }
    .stMetric {
        background-color: #1a1f26;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00e5ff;
    }
    .stMetric label {
        color: #00e5ff !important;
    }
    h1, h2, h3 {
        color: #00e5ff !important;
        font-family: 'Roboto Mono', monospace;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f26;
        border: 1px solid #00e5ff;
        color: #00e5ff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00e5ff;
        color: #0b0f14;
    }
</style>
""", unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_and_process():
    df = load_data('cybersecurity_attacks.csv')
    df_processed = preprocess_data(df)
    return df_processed

# Main app
def main():
    # Header
    st.title("🛡️ DarkSentinel")
    st.markdown("### Cybercrime Analytics Dashboard")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading cybersecurity data..."):
        df = load_and_process()
    
    # Sidebar filters
    st.sidebar.title("🔍 Filters")
    st.sidebar.markdown("---")
    
    # Year filter
    years = sorted(df['Year'].unique())
    selected_years = st.sidebar.multiselect(
        "📅 Select Year(s)",
        options=years,
        default=years
    )
    
    # Month filter
    months = sorted(df['Month'].unique())
    selected_months = st.sidebar.multiselect(
        "📆 Select Month(s)",
        options=months,
        default=months,
        format_func=lambda x: df[df['Month']==x]['MonthName'].iloc[0]
    )
    
    # Attack Type filter
    attack_types = sorted(df['Attack Type'].unique())
    selected_attacks = st.sidebar.multiselect(
        "⚠️ Attack Type",
        options=attack_types,
        default=attack_types
    )
    
    # Severity filter
    severity_levels = sorted(df['Severity Level'].unique())
    selected_severity = st.sidebar.multiselect(
        "🚨 Severity Level",
        options=severity_levels,
        default=severity_levels
    )
    
    # Device/OS filter
    devices = sorted(df['Device/OS'].unique())
    selected_devices = st.sidebar.multiselect(
        "💻 Device/OS",
        options=devices,
        default=devices
    )
    
    # Protocol filter
    protocols = sorted(df['Protocol'].unique())
    selected_protocols = st.sidebar.multiselect(
        "🌐 Protocol",
        options=protocols,
        default=protocols
    )
    
    # Apply filters
    filters = {
        'years': selected_years,
        'months': selected_months,
        'attack_types': selected_attacks,
        'severity_levels': selected_severity,
        'devices': selected_devices,
        'protocols': selected_protocols
    }
    
    filtered_df = filter_data(df, filters)
    
    # Display filter info
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Showing {len(filtered_df):,} of {len(df):,} records")
    
    # Create tabs
    tabs = st.tabs([
        "📊 Overview",
        "📈 Timeline & Trends",
        "🗺️ Geo & Heatmap",
        "🔍 Attack Explorer",
        "💻 Devices & Browsers",
        "🌐 Network & Protocols",
        "🛡️ IDS/Firewall",
        "⚡ Anomalies & Reports"
    ])
    
    # Tab 1: Overview
    with tabs[0]:
        st.header("📊 Overview Dashboard")
        
        # KPI Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Attacks", f"{len(filtered_df):,}")
        
        with col2:
            alerts = (filtered_df['Alerts/Warnings'] == 'Alert Triggered').sum()
            st.metric("Active Alerts", f"{alerts:,}")
        
        with col3:
            blocked_pct = (filtered_df['Action Taken'] == 'Blocked').mean() * 100
            st.metric("Blocked %", f"{blocked_pct:.1f}%")
        
        with col4:
            high_sev_pct = (filtered_df['Severity Level'] == 'High').mean() * 100
            st.metric("High Severity %", f"{high_sev_pct:.1f}%")
        
        with col5:
            unique_ips = filtered_df['Source IP Address'].nunique()
            st.metric("Unique Source IPs", f"{unique_ips:,}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = visuals.create_attack_type_chart(filtered_df, color_by='Year')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = visuals.create_severity_pie_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series
        fig = visuals.create_time_series_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Timeline & Trends
    with tabs[1]:
        st.header("📈 Timeline & Trends")
        
        # Monthly trends
        fig = visuals.create_monthly_trend_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Day of week distribution
            dow_data = filtered_df['DayName'].value_counts().reindex([
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
            ])
            fig = px.bar(
                x=dow_data.index,
                y=dow_data.values,
                title='Attacks by Day of Week',
                labels={'x': 'Day', 'y': 'Count'},
                color=dow_data.values,
                color_continuous_scale='Plasma'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Hourly distribution
            hour_data = filtered_df['Hour'].value_counts().sort_index()
            fig = px.line(
                x=hour_data.index,
                y=hour_data.values,
                title='Attacks by Hour of Day',
                labels={'x': 'Hour', 'y': 'Count'},
                markers=True
            )
            fig.update_traces(line_color=visuals.COLORS['primary'])
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap
        fig = visuals.create_hourly_heatmap(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Geo & Heatmap
    with tabs[2]:
        st.header("🗺️ Geographic Distribution")
        
        # Top locations
        fig = visuals.create_geo_map(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top states
            state_data = filtered_df['State'].value_counts().head(10)
            fig = px.bar(
                x=state_data.values,
                y=state_data.index,
                orientation='h',
                title='Top 10 States by Attack Count',
                labels={'x': 'Count', 'y': 'State'},
                color=state_data.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Attack types by state
            top_states = filtered_df['State'].value_counts().head(5).index
            state_attack_df = filtered_df[filtered_df['State'].isin(top_states)]
            fig = px.histogram(
                state_attack_df,
                x='State',
                color='Attack Type',
                title='Attack Types in Top 5 States',
                barmode='stack'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Attack Explorer
    with tabs[3]:
        st.header("🔍 Attack Explorer")
        
        # Search and filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_ip = st.text_input("🔎 Search by IP Address")
        
        with col2:
            search_user = st.text_input("👤 Search by User")
        
        with col3:
            search_signature = st.selectbox(
                "🔐 Attack Signature",
                ['All'] + list(filtered_df['Attack Signature'].unique())
            )
        
        # Apply search filters
        display_df = filtered_df.copy()
        
        if search_ip:
            display_df = display_df[
                display_df['Source IP Address'].str.contains(search_ip, case=False) |
                display_df['Destination IP Address'].str.contains(search_ip, case=False)
            ]
        
        if search_user:
            display_df = display_df[
                display_df['User Information'].str.contains(search_user, case=False)
            ]
        
        if search_signature != 'All':
            display_df = display_df[display_df['Attack Signature'] == search_signature]
        
        # Display table
        st.dataframe(
            display_df[[
                'Timestamp', 'Attack Type', 'Severity Level',
                'Source IP Address', 'Destination IP Address',
                'Protocol', 'Action Taken', 'IDS/IPS Alerts'
            ]].head(100),
            use_container_width=True,
            height=400
        )
        
        # Export button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="darksentinel_filtered_data.csv",
            mime="text/csv"
        )
        
        # Detailed view
        if len(display_df) > 0:
            st.markdown("---")
            st.subheader("🔬 Detailed Record View")
            
            record_idx = st.selectbox(
                "Select record to view details",
                range(min(50, len(display_df))),
                format_func=lambda x: f"Record {x+1}: {display_df.iloc[x]['Attack Type']} at {display_df.iloc[x]['Timestamp']}"
            )
            
            if record_idx is not None:
                record = display_df.iloc[record_idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🕐 Timestamp:**")
                    st.write(record['Timestamp'])
                    
                    st.markdown("**⚠️ Attack Type:**")
                    st.write(record['Attack Type'])
                    
                    st.markdown("**🚨 Severity:**")
                    st.write(record['Severity Level'])
                    
                    st.markdown("**🔐 Attack Signature:**")
                    st.write(record['Attack Signature'])
                    
                    st.markdown("**✅ Action Taken:**")
                    st.write(record['Action Taken'])
                
                with col2:
                    st.markdown("**📡 Source IP:**")
                    st.write(record['Source IP Address'])
                    
                    st.markdown("**🎯 Destination IP:**")
                    st.write(record['Destination IP Address'])
                    
                    st.markdown("**🌐 Protocol:**")
                    st.write(record['Protocol'])
                    
                    st.markdown("**📦 Packet Length:**")
                    st.write(f"{record['Packet Length']} bytes")
                    
                    st.markdown("**📊 Anomaly Score:**")
                    st.write(f"{record['Anomaly Scores']:.2f}")
                
                st.markdown("**📄 Payload Data:**")
                st.text_area("", record['Payload Data'], height=100)
    
    # Tab 5: Devices & Browsers
    with tabs[4]:
        st.header("💻 Device & Browser Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = visuals.create_device_os_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Browser distribution
            browser_data = filtered_df['Browser'].value_counts()
            fig = px.pie(
                values=browser_data.values,
                names=browser_data.index,
                title='Browser Distribution',
                hole=0.4
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Traffic type by browser
        fig = visuals.create_browser_traffic_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Average packet length by device
        col1, col2 = st.columns(2)
        
        with col1:
            device_packet = filtered_df.groupby('Device/OS')['Packet Length'].mean().sort_values(ascending=False)
            fig = px.bar(
                x=device_packet.values,
                y=device_packet.index,
                orientation='h',
                title='Average Packet Length by Device/OS',
                labels={'x': 'Avg Packet Length (bytes)', 'y': 'Device/OS'},
                color=device_packet.values,
                color_continuous_scale='Turbo'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Attack types by device
            fig = px.histogram(
                filtered_df,
                x='Device/OS',
                color='Attack Type',
                title='Attack Types by Device/OS',
                barmode='stack'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 6: Network & Protocols
    with tabs[5]:
        st.header("🌐 Network & Protocol Analysis")
        
        # Protocol distribution
        fig = visuals.create_protocol_attack_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Average packet length by protocol
            protocol_packet = filtered_df.groupby('Protocol')['Packet Length'].mean().sort_values(ascending=False)
            fig = px.bar(
                x=protocol_packet.index,
                y=protocol_packet.values,
                title='Average Packet Length by Protocol',
                labels={'x': 'Protocol', 'y': 'Avg Packet Length (bytes)'},
                color=protocol_packet.values,
                color_continuous_scale='Plasma'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Traffic type distribution
            traffic_data = filtered_df['Traffic Type'].value_counts()
            fig = px.pie(
                values=traffic_data.values,
                names=traffic_data.index,
                title='Traffic Type Distribution'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Sankey diagram
        st.subheader("🔀 Attack Flow Diagram")
        fig = visuals.create_sankey_diagram(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Packet length distribution
        fig = visuals.create_packet_length_distribution(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 7: IDS/Firewall Analytics
    with tabs[6]:
        st.header("🛡️ IDS/Firewall Analytics")
        
        # Action taken distribution
        fig = visuals.create_action_taken_chart(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # IDS/IPS Alerts
            fig = visuals.create_ids_firewall_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Alerts/Warnings
            fig = px.histogram(
                filtered_df,
                x='Action Taken',
                color='Alerts/Warnings',
                title='Action Taken vs Alerts/Warnings',
                barmode='group'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Firewall logs
        col1, col2 = st.columns(2)
        
        with col1:
            firewall_data = filtered_df['Firewall Logs'].value_counts()
            fig = px.pie(
                values=firewall_data.values,
                names=firewall_data.index,
                title='Firewall Logs Distribution'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            log_source_data = filtered_df['Log Source'].value_counts()
            fig = px.pie(
                values=log_source_data.values,
                names=log_source_data.index,
                title='Log Source Distribution'
            )
            fig.update_layout(**visuals.PLOTLY_TEMPLATE['layout'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 8: Anomalies & Reports
    with tabs[7]:
        st.header("⚡ Anomaly Detection & Reports")
        
        # Train anomaly detector
        with st.spinner("Training anomaly detection model..."):
            model, scaler, features = train_anomaly_detector(filtered_df, contamination=0.1)
            df_with_anomalies = detect_anomalies(filtered_df, model, scaler, features)
        
        # Anomaly summary
        summary = get_anomaly_summary(df_with_anomalies)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{summary['total_records']:,}")
        
        with col2:
            st.metric("Anomalies Detected", f"{summary['anomaly_count']:,}")
        
        with col3:
            st.metric("Normal Records", f"{summary['normal_count']:,}")
        
        with col4:
            st.metric("Anomaly Rate", f"{summary['anomaly_percentage']:.2f}%")
        
        st.markdown("---")
        
        # Anomaly score distribution
        fig = visuals.create_anomaly_score_distribution(df_with_anomalies)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top anomalies
        st.subheader("🔝 Top Anomalous Records")
        
        n_anomalies = st.slider("Number of top anomalies to display", 5, 50, 10)
        top_anomalies = get_top_anomalies(df_with_anomalies, n=n_anomalies)
        
        st.dataframe(
            top_anomalies[[
                'Timestamp', 'Attack Type', 'Severity Level',
                'Source IP Address', 'Protocol', 'Packet Length',
                'Anomaly Scores', 'ML_Anomaly_Score'
            ]],
            use_container_width=True,
            height=400
        )
        
        # Anomaly insights
        st.markdown("---")
        st.subheader("📊 Anomaly Insights")
        
        insights = get_anomaly_insights(df_with_anomalies)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Most Common Attack Type:**")
            st.write(insights['most_common_attack_type'])
            
            st.markdown("**Most Common Severity:**")
            st.write(insights['most_common_severity'])
        
        with col2:
            st.markdown("**Most Common Device:**")
            st.write(insights['most_common_device'])
            
            st.markdown("**Most Common Protocol:**")
            st.write(insights['most_common_protocol'])
        
        with col3:
            st.markdown("**Avg Packet Length:**")
            st.write(f"{insights['avg_packet_length']:.2f} bytes")
            
            st.markdown("**Avg Anomaly Score:**")
            st.write(f"{insights['avg_anomaly_score']:.2f}")
        
        # Export anomalies
        st.markdown("---")
        anomaly_csv = top_anomalies.to_csv(index=False)
        st.download_button(
            label="📥 Download Top Anomalies as CSV",
            data=anomaly_csv,
            file_name="darksentinel_anomalies.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
