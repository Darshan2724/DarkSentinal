"""
Visualizations for Global Cybersecurity Threats Dataset
Professional charts optimized for the new data structure
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Updated color scheme
COLORS = {
    'bg': '#050816',
    'cyan': '#4dd0e1',
    'cyan_bright': '#00f5ff',
    'purple': '#7b2ff7',
    'pink': '#ff006e',
    'green': '#00ff88',
    'orange': '#ffaa00',
    'text': '#b8c5d6',
}

def apply_theme(fig, title=None, height=None):
    """Apply theme to figure with optional title and height"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255, 255, 255, 0.03)',
        font=dict(color=COLORS['text'], family='Rajdhani, sans-serif', size=12),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor=COLORS['cyan'],
            zerolinecolor='rgba(255, 255, 255, 0.1)',
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor=COLORS['cyan'],
            zerolinecolor='rgba(255, 255, 255, 0.1)',
        ),
        hoverlabel=dict(
            bgcolor='rgba(0, 0, 0, 0.8)',
            font_size=12,
            font_family='Rajdhani'
        )
    )
    if title:
        fig.update_layout(title={'text': title, 'font': {'size': 20, 'color': COLORS['cyan'], 'family': 'Orbitron'}})
    if height:
        fig.update_layout(height=height)
    return fig

def create_defense_effectiveness_chart(defense_stats, title='🛡️ Defense Mechanism Effectiveness'):
    """
    Create horizontal bar chart showing defense mechanism effectiveness
    Replaces the confusing radar chart
    """
    # Sort by effectiveness score
    defense_stats = defense_stats.sort_values('Effectiveness_Score', ascending=True)
    
    fig = go.Figure()
    
    # Add effectiveness score bars
    fig.add_trace(go.Bar(
        y=defense_stats['Defense_Mechanism'],
        x=defense_stats['Effectiveness_Score'],
        orientation='h',
        name='Effectiveness Score',
        marker=dict(
            color=defense_stats['Effectiveness_Score'],
            colorscale=[[0, COLORS['pink']], [0.5, COLORS['orange']], [1, COLORS['green']]],
            showscale=True,
            colorbar=dict(title="Score", thickness=15)
        ),
        text=defense_stats['Effectiveness_Score'].round(1),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                      'Effectiveness Score: %{x:.1f}/100<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Effectiveness Score (0-100)',
        yaxis_title='Defense Mechanism',
        showlegend=False
    )
    
    apply_theme(fig, title=title, height=400)
    
    return fig

def create_defense_metrics_comparison(defense_stats, title='📊 Defense Mechanism Metrics Comparison'):
    """Create grouped bar chart comparing defense metrics"""
    
    fig = go.Figure()
    
    # Normalize metrics to 0-100 scale for comparison
    max_loss = defense_stats['Avg_Financial_Loss'].max()
    max_users = defense_stats['Avg_Affected_Users'].max()
    max_time = defense_stats['Avg_Resolution_Time'].max()
    
    defense_stats['Loss_Score'] = (1 - defense_stats['Avg_Financial_Loss'] / max_loss) * 100
    defense_stats['Users_Score'] = (1 - defense_stats['Avg_Affected_Users'] / max_users) * 100
    defense_stats['Time_Score'] = (1 - defense_stats['Avg_Resolution_Time'] / max_time) * 100
    
    fig.add_trace(go.Bar(
        name='Financial Protection',
        x=defense_stats['Defense_Mechanism'],
        y=defense_stats['Loss_Score'],
        marker_color=COLORS['green']
    ))
    
    fig.add_trace(go.Bar(
        name='User Protection',
        x=defense_stats['Defense_Mechanism'],
        y=defense_stats['Users_Score'],
        marker_color=COLORS['cyan']
    ))
    
    fig.add_trace(go.Bar(
        name='Response Speed',
        x=defense_stats['Defense_Mechanism'],
        y=defense_stats['Time_Score'],
        marker_color=COLORS['purple']
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title='Defense Mechanism',
        yaxis_title='Performance Score (0-100)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    apply_theme(fig, title=title, height=450)
    
    return fig

def create_yearly_trend_chart(yearly_data, title='📈 Yearly Attack Trends (2015-2024)'):
    """Create line chart showing yearly trends"""
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Attack Count & Financial Loss', 'Affected Users'),
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
        vertical_spacing=0.15
    )
    
    # Attack count - Primary y-axis
    fig.add_trace(go.Scatter(
        x=yearly_data['Year'],
        y=yearly_data['Total_Attacks'],
        name='Total Attacks',
        line=dict(color=COLORS['cyan'], width=4, shape='spline'),
        mode='lines+markers',
        marker=dict(size=10, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(77, 208, 225, 0.2)',
        hovertemplate='<b>Year %{x}</b><br>Attacks: %{y:,}<extra></extra>'
    ), row=1, col=1, secondary_y=False)
    
    # Financial loss - Secondary y-axis
    fig.add_trace(go.Scatter(
        x=yearly_data['Year'],
        y=yearly_data['Total_Financial_Loss'],
        name='Financial Loss ($M)',
        line=dict(color=COLORS['pink'], width=4, shape='spline'),
        mode='lines+markers',
        marker=dict(size=10, symbol='diamond'),
        hovertemplate='<b>Year %{x}</b><br>Loss: $%{y:,.0f}M<extra></extra>'
    ), row=1, col=1, secondary_y=True)
    
    # Affected users
    fig.add_trace(go.Bar(
        x=yearly_data['Year'],
        y=yearly_data['Total_Affected_Users'],
        name='Affected Users',
        marker_color=COLORS['purple'],
        hovertemplate='<b>Year %{x}</b><br>Users: %{y:,}<extra></extra>'
    ), row=2, col=1)
    
    # Update axes
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_yaxes(title_text="Attack Count", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Financial Loss ($M)", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Affected Users", row=2, col=1)
    
    # Ensure y-axis starts from 0 for attack count
    fig.update_yaxes(rangemode='tozero', row=1, col=1, secondary_y=False)
    
    apply_theme(fig, title=title, height=600)
    
    return fig

def create_attack_type_distribution(df, title='⚠️ Attack Type Distribution'):
    """Create pie chart for attack types"""
    
    attack_counts = df['Attack Type'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=attack_counts.index,
        values=attack_counts.values,
        hole=0.4,
        marker=dict(
            colors=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                   COLORS['green'], COLORS['orange'], COLORS['cyan_bright']],
            line=dict(color='#000000', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    apply_theme(fig, title=title, height=450)
    
    return fig

def create_country_heatmap(df, title='🌍 Attack Distribution by Country'):
    """Create bar chart for country distribution"""
    
    country_data = df.groupby('Country').agg({
        'Attack Type': 'count',
        'Financial Loss (in Million $)': 'sum',
        'Number of Affected Users': 'sum'
    }).reset_index()
    country_data.columns = ['Country', 'Attack_Count', 'Financial_Loss', 'Affected_Users']
    country_data = country_data.sort_values('Attack_Count', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=country_data['Country'],
        x=country_data['Attack_Count'],
        orientation='h',
        marker=dict(
            color=country_data['Financial_Loss'],
            colorscale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]],
            showscale=True,
            colorbar=dict(title="Financial Loss ($M)")
        ),
        text=country_data['Attack_Count'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                      'Attacks: %{x}<br>' +
                      'Financial Loss: $%{marker.color:.1f}M<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Number of Attacks',
        yaxis_title='Country'
    )
    
    apply_theme(fig, title=title, height=500)
    
    return fig

def create_industry_sunburst(df, title='🏢 Industry Attack Breakdown'):
    """Create sunburst chart for industry analysis"""
    
    industry_data = df.groupby(['Target Industry', 'Attack Type']).size().reset_index(name='count')
    
    fig = px.sunburst(
        industry_data,
        path=['Target Industry', 'Attack Type'],
        values='count',
        color='count',
        color_continuous_scale=[[0, COLORS['cyan']], [0.5, COLORS['purple']], [1, COLORS['pink']]]
    )
    
    apply_theme(fig, title=title, height=500)
    
    return fig

def create_vulnerability_analysis(df, title='🔓 Security Vulnerability Analysis'):
    """Create stacked bar chart for vulnerability types"""
    
    vuln_data = df.groupby(['Security Vulnerability Type', 'Attack Source']).size().reset_index(name='count')
    
    fig = px.bar(
        vuln_data,
        x='Security Vulnerability Type',
        y='count',
        color='Attack Source',
        title=title,
        labels={'count': 'Number of Attacks'},
        color_discrete_sequence=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], COLORS['orange']]
    )
    
    apply_theme(fig, title=title, height=450)
    
    return fig

def create_financial_impact_chart(df, title='💰 Financial Impact by Attack Type'):
    """Create waterfall chart for financial impact"""
    
    attack_loss = df.groupby('Attack Type')['Financial Loss (in Million $)'].sum().sort_values(ascending=False)
    
    fig = go.Figure(go.Waterfall(
        name="Financial Loss",
        orientation="v",
        measure=["relative"] * len(attack_loss),
        x=attack_loss.index.tolist(),
        y=attack_loss.values.tolist(),
        connector={"line": {"color": COLORS['cyan']}},
        increasing={"marker": {"color": COLORS['pink']}},
        decreasing={"marker": {"color": COLORS['green']}},
    ))
    
    fig.update_layout(
        xaxis_title="Attack Type",
        yaxis_title="Financial Loss (Million $)"
    )
    
    apply_theme(fig, title=title, height=450)
    
    return fig

def create_resolution_time_box(df, title='⏱️ Resolution Time Distribution'):
    """Create box plot for resolution times"""
    
    fig = px.box(
        df,
        x='Defense Mechanism Used',
        y='Incident Resolution Time (in Hours)',
        color='Defense Mechanism Used',
        title=title,
        color_discrete_sequence=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                                COLORS['green'], COLORS['orange']]
    )
    
    fig.update_layout(showlegend=False)
    
    apply_theme(fig, title=title, height=450)
    
    return fig

def create_3d_globe_global(df, title='🌍 Global Attack Distribution'):
    """Create 3D globe visualization for global dataset"""
    
    # Country coordinates
    country_coords = {
        'USA': {'lat': 37.0902, 'lon': -95.7129},
        'UK': {'lat': 55.3781, 'lon': -3.4360},
        'Germany': {'lat': 51.1657, 'lon': 10.4515},
        'France': {'lat': 46.2276, 'lon': 2.2137},
        'China': {'lat': 35.8617, 'lon': 104.1954},
        'India': {'lat': 20.5937, 'lon': 78.9629},
        'Brazil': {'lat': -14.2350, 'lon': -51.9253},
        'Russia': {'lat': 61.5240, 'lon': 105.3188},
        'Australia': {'lat': -25.2744, 'lon': 133.7751},
        'Japan': {'lat': 36.2048, 'lon': 138.2529},
    }
    
    # Aggregate data by country
    country_data = df.groupby('Country').agg({
        'Attack Type': 'count',
        'Financial Loss (in Million $)': 'sum',
        'Number of Affected Users': 'sum'
    }).reset_index()
    country_data.columns = ['Country', 'Attack_Count', 'Financial_Loss', 'Affected_Users']
    
    # Add coordinates
    country_data['lat'] = country_data['Country'].map(lambda x: country_coords.get(x, {}).get('lat', 0))
    country_data['lon'] = country_data['Country'].map(lambda x: country_coords.get(x, {}).get('lon', 0))
    
    # Marker sizing: scale by attack count with sizeref to avoid oversized bubbles
    max_count = max(country_data['Attack_Count'].max(), 1)
    desired_max_px = 28  # max bubble diameter in pixels
    sizeref = 2.0 * max_count / (desired_max_px ** 2)

    # Customdata for hover (attack count, financial loss)
    customdata = np.stack([
        country_data['Attack_Count'].values,
        country_data['Financial_Loss'].values
    ], axis=-1)

    # Create 3D scatter on globe
    fig = go.Figure(data=go.Scattergeo(
        lon=country_data['lon'],
        lat=country_data['lat'],
        text=country_data['Country'],
        mode='markers',
        marker=dict(
            size=country_data['Attack_Count'],
            sizemode='area',
            sizeref=sizeref,
            sizemin=4,
            opacity=0.85,
            color=country_data['Financial_Loss'],
            colorscale=[[0, COLORS['green']], [0.5, COLORS['orange']], [1, COLORS['pink']]],
            colorbar=dict(title="Financial Loss ($M)", thickness=15),
            line=dict(width=0.6, color=COLORS['cyan']),
            showscale=True
        ),
        customdata=customdata,
        hovertemplate='<b>%{text}</b><br>' +
                      'Attacks: %{customdata[0]:,}<br>' +
                      'Financial Loss: $%{customdata[1]:,.1f}M<extra></extra>'
    ))
    
    fig.update_geos(
        projection_type='orthographic',
        showcountries=True,
        countrycolor=COLORS['cyan'],
        showcoastlines=True,
        coastlinecolor=COLORS['purple'],
        showland=True,
        landcolor='rgba(10, 15, 30, 0.8)',
        showocean=True,
        oceancolor='rgba(5, 8, 22, 0.9)',
        bgcolor='rgba(0,0,0,0)',
    )
    
    apply_theme(fig, title=title, height=600)
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    
    return fig

def create_3d_attack_correlation(df, title='🔮 3D Attack Correlation Analysis'):
    """Create 3D scatter plot showing attack correlations"""
    
    # Sample data for performance
    sample_df = df.sample(min(500, len(df)))
    
    fig = px.scatter_3d(
        sample_df,
        x='Financial Loss (in Million $)',
        y='Number of Affected Users',
        z='Incident Resolution Time (in Hours)',
        color='Attack Type',
        size='Financial Loss (in Million $)',
        hover_data=['Country', 'Target Industry', 'Year'],
        title=title,
        labels={
            'Financial Loss (in Million $)': 'Financial Loss ($M)',
            'Number of Affected Users': 'Affected Users',
            'Incident Resolution Time (in Hours)': 'Resolution Time (h)'
        },
        color_discrete_sequence=[COLORS['cyan'], COLORS['purple'], COLORS['pink'], 
                                COLORS['green'], COLORS['orange'], COLORS['cyan_bright']]
    )
    
    apply_theme(fig, title=title, height=700)
    
    return fig

def create_attack_flow_sankey(df, title='🔀 Attack Flow Diagram'):
    """Create Sankey diagram showing attack flow"""
    
    # Create flow: Attack Source -> Attack Type -> Target Industry
    flow_data = df.groupby(['Attack Source', 'Attack Type', 'Target Industry']).size().reset_index(name='count')
    
    # Create node labels
    sources = df['Attack Source'].unique().tolist()
    attack_types = df['Attack Type'].unique().tolist()
    industries = df['Target Industry'].unique().tolist()
    
    all_nodes = sources + attack_types + industries
    
    # Create links
    source_indices = []
    target_indices = []
    values = []
    
    # Source -> Attack Type
    for _, row in flow_data.iterrows():
        source_indices.append(all_nodes.index(row['Attack Source']))
        target_indices.append(all_nodes.index(row['Attack Type']))
        values.append(row['count'])
    
    # Attack Type -> Industry (aggregate)
    industry_flow = df.groupby(['Attack Type', 'Target Industry']).size().reset_index(name='count')
    for _, row in industry_flow.iterrows():
        source_indices.append(all_nodes.index(row['Attack Type']))
        target_indices.append(all_nodes.index(row['Target Industry']))
        values.append(row['count'])
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color=COLORS['cyan'], width=0.5),
            label=all_nodes,
            color=[COLORS['orange']] * len(sources) + 
                  [COLORS['cyan']] * len(attack_types) + 
                  [COLORS['purple']] * len(industries)
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color='rgba(77, 208, 225, 0.2)'
        )
    )])
    
    fig.update_layout(
        font=dict(size=12, color=COLORS['text'])
    )
    apply_theme(fig, title=title, height=600)
    
    return fig
