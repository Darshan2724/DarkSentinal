"""
DarkSentinel V2 - Global Cybersecurity Threats Dashboard (2015-2024)
Complete redesign with improved UX and new dataset
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Import custom modules
from modules_v2.glassmorphism_theme import (
    apply_glassmorphism_theme, create_metric_card, create_header,
    create_section_header, COLORS
)
from modules_v2.data_loader_global import (
    load_global_data, get_data_summary, get_attack_statistics,
    filter_data, get_top_threats, get_yearly_trends, get_defense_effectiveness
)
from modules_v2.visuals_global import (
    create_defense_effectiveness_chart, create_defense_metrics_comparison,
    create_yearly_trend_chart, create_attack_type_distribution,
    create_country_heatmap, create_industry_sunburst,
    create_vulnerability_analysis, create_financial_impact_chart,
    create_resolution_time_box
)
from modules_v2.recent_attacks import (
    create_recent_attacks_table, create_attack_summary_cards
)

# Define text color for convenience
TEXT_COLOR = COLORS['text_secondary']

# Page configuration
st.set_page_config(
    page_title="DarkSentinel V2 | Cyber Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply glassmorphism theme
apply_glassmorphism_theme()

# Load data
@st.cache_data(ttl=3600)
def load_and_cache_data():
    return load_global_data()

# Main app
def main():
    # Header - Updated title without "Real-Time Intelligence"
    st.markdown(create_header(
        "DARKSENTINEL V2",
        "CYBER COMMAND CENTER"
    ), unsafe_allow_html=True)
    
    # Load data with loading animation
    with st.spinner('🔄 Initializing Threat Intelligence System...'):
        df = load_and_cache_data()
        time.sleep(0.3)
    
    # Sidebar - Advanced Filters with improved colors
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: {COLORS['text_primary']}; text-shadow: 0 0 10px rgba(77, 208, 225, 0.5);">
                ⚙️ CONTROL PANEL
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Year range filter - Updated for 2015-2024
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>📅 YEAR RANGE</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.selectbox(
                "From",
                options=sorted(df['Year'].unique()),
                index=0,
                label_visibility="visible"
            )
        with col2:
            end_year = st.selectbox(
                "To",
                options=sorted(df['Year'].unique()),
                index=len(df['Year'].unique())-1,
                label_visibility="visible"
            )
        
        # Quick preset buttons
        st.markdown("<p style='font-size: 12px; color: #b8c5d6; margin-top: 10px;'>Quick Filters:</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 Last Year", use_container_width=True):
                start_year = df['Year'].max()
                end_year = df['Year'].max()
        with col2:
            if st.button("📊 All Time", use_container_width=True):
                start_year = df['Year'].min()
                end_year = df['Year'].max()
        
        st.markdown("---")
        
        # Country filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🌍 COUNTRIES</p>", unsafe_allow_html=True)
        countries = st.multiselect(
            "Select countries",
            options=sorted(df['Country'].unique()),
            default=sorted(df['Country'].unique()),
            label_visibility="collapsed"
        )
        
        # Attack type filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>⚠️ ATTACK TYPES</p>", unsafe_allow_html=True)
        attack_types = st.multiselect(
            "Select attack types",
            options=sorted(df['Attack Type'].unique()),
            default=sorted(df['Attack Type'].unique()),
            label_visibility="collapsed"
        )
        
        # Industry filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🏢 INDUSTRIES</p>", unsafe_allow_html=True)
        industries = st.multiselect(
            "Select industries",
            options=sorted(df['Target Industry'].unique()),
            default=sorted(df['Target Industry'].unique()),
            label_visibility="collapsed"
        )
        
        # Attack source filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🎯 ATTACK SOURCE</p>", unsafe_allow_html=True)
        sources = st.multiselect(
            "Select sources",
            options=sorted(df['Attack Source'].unique()),
            default=sorted(df['Attack Source'].unique()),
            label_visibility="collapsed"
        )
        
        # Severity filter
        st.markdown(f"<p style='color: {COLORS['cyan']}; font-weight: 600;'>🚨 SEVERITY</p>", unsafe_allow_html=True)
        severity_cats = st.multiselect(
            "Select severity",
            options=['Low', 'Medium', 'High', 'Critical'],
            default=['Low', 'Medium', 'High', 'Critical'],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Apply filters button
        if st.button("🔍 APPLY FILTERS", use_container_width=True):
            st.rerun()
        
        # Reset filters button
        if st.button("🔄 RESET ALL", use_container_width=True):
            st.rerun()
    
    # Apply filters
    filters = {
        'year_range': (start_year, end_year),
        'countries': countries,
        'attack_types': attack_types,
        'industries': industries,
        'sources': sources,
        'severity_categories': severity_cats
    }
    
    filtered_df = filter_data(df, filters)
    
    # Display filter info
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(77, 208, 225, 0.1);
        border: 1px solid {COLORS['cyan']};
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        text-align: center;
    ">
        <div style="color: {COLORS['cyan']}; font-size: 14px; font-weight: 600;">
            FILTERED RECORDS
        </div>
        <div style="color: white; font-size: 28px; font-weight: bold; margin-top: 5px;">
            {len(filtered_df):,}
        </div>
        <div style="color: {TEXT_COLOR}; font-size: 12px; margin-top: 5px;">
            of {len(df):,} total
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    
    # Attack Summary Cards (replaces ticker)
    st.components.v1.html(create_attack_summary_cards(filtered_df), height=120)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Critical Attacks Table (replaces terminal feed and status board)
    st.components.v1.html(create_recent_attacks_table(filtered_df, n=10), height=600, scrolling=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Key Metrics Dashboard - SIMPLIFIED TO 5 CARDS IN SINGLE ROW
    st.markdown(create_section_header("📊 COMMAND CENTER METRICS", ""), unsafe_allow_html=True)
    
    # Calculate metrics
    total_attacks = len(filtered_df)
    total_data_loss = filtered_df['Financial Loss (in Million $)'].sum()
    avg_severity = filtered_df['Severity_Score'].mean() if 'Severity_Score' in filtered_df.columns else 5.0
    critical_attacks = len(filtered_df[filtered_df['Severity_Category'] == 'Critical']) if 'Severity_Category' in filtered_df.columns else 0
    total_affected = filtered_df['Number of Affected Users'].sum()
    
    # Display 5 metrics in single row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(create_metric_card(
            "TOTAL ATTACKS",
            f"{total_attacks:,}",
            icon="🎯"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "FINANCIAL LOSS",
            f"${total_data_loss/1000:.1f}B",
            icon="💰"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "AFFECTED USERS",
            f"{total_affected/1000000:.1f}M",
            icon="👥"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "AVG SEVERITY",
            f"{avg_severity:.1f}/10",
            icon="🚨"
        ), unsafe_allow_html=True)
    
    with col5:
        st.markdown(create_metric_card(
            "CRITICAL THREATS",
            f"{critical_attacks:,}",
            icon="🔴"
        ), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Yearly Trends
    st.markdown(create_section_header("📈 GLOBAL THREAT TRENDS (2015-2024)", ""), unsafe_allow_html=True)
    
    yearly_data = get_yearly_trends(filtered_df)
    fig_yearly = create_yearly_trend_chart(yearly_data)
    st.plotly_chart(fig_yearly, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attack Distribution
    st.markdown(create_section_header("⚠️ ATTACK ANALYSIS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_attack_dist = create_attack_type_distribution(filtered_df)
        st.plotly_chart(fig_attack_dist, use_container_width=True)
    
    with col2:
        fig_industry = create_industry_sunburst(filtered_df)
        st.plotly_chart(fig_industry, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Geographic Analysis with 3D Globe
    st.markdown(create_section_header("🌍 GEOGRAPHIC DISTRIBUTION", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Add 3D Globe visualization
        from modules_v2.visuals_global import create_3d_globe_global
        fig_globe = create_3d_globe_global(filtered_df)
        st.plotly_chart(fig_globe, use_container_width=True)
    
    with col2:
        fig_country = create_country_heatmap(filtered_df)
        st.plotly_chart(fig_country, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Defense Mechanism Analysis - REPLACED RADAR WITH BAR CHART
    st.markdown(create_section_header("🛡️ DEFENSE MECHANISM EFFECTIVENESS", ""), unsafe_allow_html=True)
    
    defense_stats = get_defense_effectiveness(filtered_df)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig_defense = create_defense_effectiveness_chart(defense_stats)
        st.plotly_chart(fig_defense, use_container_width=True)
    
    with col2:
        fig_defense_metrics = create_defense_metrics_comparison(defense_stats)
        st.plotly_chart(fig_defense_metrics, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Financial Impact
    st.markdown(create_section_header("💰 FINANCIAL IMPACT ANALYSIS", ""), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_financial = create_financial_impact_chart(filtered_df)
        st.plotly_chart(fig_financial, use_container_width=True)
    
    with col2:
        fig_vuln = create_vulnerability_analysis(filtered_df)
        st.plotly_chart(fig_vuln, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Resolution Time Analysis
    st.markdown(create_section_header("⏱️ INCIDENT RESOLUTION ANALYSIS", ""), unsafe_allow_html=True)
    
    fig_resolution = create_resolution_time_box(filtered_df)
    st.plotly_chart(fig_resolution, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3D Attack Correlation Analysis
    st.markdown(create_section_header("🔮 3D ATTACK CORRELATION ANALYSIS", ""), unsafe_allow_html=True)
    
    from modules_v2.visuals_global import create_3d_attack_correlation
    fig_3d_correlation = create_3d_attack_correlation(filtered_df)
    st.plotly_chart(fig_3d_correlation, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attack Flow Diagram
    st.markdown(create_section_header("🔀 ATTACK FLOW DIAGRAM", ""), unsafe_allow_html=True)
    
    from modules_v2.visuals_global import create_attack_flow_sankey
    fig_flow = create_attack_flow_sankey(filtered_df)
    st.plotly_chart(fig_flow, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Explorer
    st.markdown(create_section_header("🔍 THREAT INTELLIGENCE DATABASE", ""), unsafe_allow_html=True)
    
    # Search functionality
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_country = st.selectbox(
            "🌍 Filter by Country",
            ['All'] + sorted(filtered_df['Country'].unique().tolist())
        )
    
    with col2:
        search_attack = st.selectbox(
            "⚠️ Filter by Attack Type",
            ['All'] + sorted(filtered_df['Attack Type'].unique().tolist())
        )
    
    with col3:
        search_industry = st.selectbox(
            "🏢 Filter by Industry",
            ['All'] + sorted(filtered_df['Target Industry'].unique().tolist())
        )
    
    # Apply search filters
    display_df = filtered_df.copy()
    
    if search_country != 'All':
        display_df = display_df[display_df['Country'] == search_country]
    
    if search_attack != 'All':
        display_df = display_df[display_df['Attack Type'] == search_attack]
    
    if search_industry != 'All':
        display_df = display_df[display_df['Target Industry'] == search_industry]
    
    # Display dataframe
    st.dataframe(
        display_df[[
            'Year', 'Country', 'Attack Type', 'Target Industry',
            'Financial Loss (in Million $)', 'Number of Affected Users',
            'Attack Source', 'Security Vulnerability Type',
            'Defense Mechanism Used', 'Incident Resolution Time (in Hours)'
        ]].head(100),
        use_container_width=True,
        height=400
    )
    
    # Export functionality
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 EXPORT TO CSV",
            data=csv,
            file_name=f"darksentinel_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 30px;
        background: rgba(255, 255, 255, 0.02);
        border-top: 1px solid rgba(77, 208, 225, 0.2);
        border-radius: 10px;
    ">
        <div style="color: {COLORS['text_primary']}; font-size: 24px; font-weight: bold; margin-bottom: 10px; text-shadow: 0 0 10px rgba(77, 208, 225, 0.5);">
            🛡️ DARKSENTINEL V2
        </div>
        <div style="color: {COLORS['cyan']}; font-size: 14px; font-weight: 600;">
            Global Cybersecurity Threat Intelligence Platform (2015-2024)
        </div>
        <div style="color: {COLORS['purple']}; font-size: 12px; margin-top: 10px;">
            Powered by Advanced Analytics | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
