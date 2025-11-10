# 🛡️ DarkSentinel - Global Cyber Threat Intelligence Dashboard

> **A comprehensive cybersecurity threat analysis platform** that transforms global cyber attack data into actionable intelligence with advanced visualizations and real-time analytics.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-orange)

## 🌟 Key Features

### 📊 Interactive Visualizations
- **3D Globe View**: Geographic distribution of cyber attacks across 45 countries with interactive rotation and zoom
- **Temporal Analysis**: 6-year trends (2019-2024) with dynamic filtering
- **Attack Flow**: Interactive Sankey diagrams showing attack vector → type → industry
- **Correlation Analysis**: 3D scatter plots showing relationships between severity, impact, and response time

### 📈 Advanced Analytics
- **30,000 Records**: Comprehensive dataset of cyber incidents (2019-2024)
- **Multi-dimensional Filters**: Drill down by time period, location, attack type, industry, and severity

- **Interactive Dashboards**: Dashboard responds instantly to filter changes with glassmorphism UI

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Sleek, professional interface with cyber aesthetics
- **Responsive Layout**: Works on desktop and tablet
- **Dark/Light Mode**: Easy on the eyes during extended analysis
- **Interactive Elements**: Hover tooltips, zoomable charts, and export capabilities

## 📋 Dataset Overview

- **Records**: 30,000 cyber incidents (2019-2024)
- **Coverage**: 45 countries, 18 industries, 23 attack types
- **Financial Impact**: $1.2 billion total losses analyzed
- **Affected Users**: 65.7 million user accounts impacted
- **Data Compromised**: 1,512.7 TB total data breach volume

### Data Points Tracked
- **Attack Details**: Type, vector, origin, target industry, target system
- **Impact Metrics**: Financial loss (USD), affected users, data compromised (GB), attack duration
- **Response Analysis**: Response time, mitigation methods, incident outcomes
- **Geographic Data**: Global coverage across 45 countries
- **Temporal Data**: Timestamp, year, time-based patterns
8. **Anomalies & Reports** - ML-based anomaly detection with exportable reports

### 🎨 Visual Theme

- **Theme**: Cyber Dark Neon
- **Primary Color**: `#00e5ff` (Neon Cyan)
- **Secondary Color**: `#ff2f92` (Magenta)
- **Success Color**: `#7CFF00` (Neon Green)
- **Background**: `#0b0f14` (Dark)

### 🔍 Filters

Dynamic sidebar filters for:
- Time Period (2019-2024) with preset ranges
- Attack Types (23 types: Ransomware, Phishing, DDoS, APT, Zero-Day, etc.)
- Target Industries (18 sectors: Finance, Healthcare, Government, Technology, etc.)
- Locations (45 countries globally)
- Severity Range (1-10 scale)
- Outcomes (Success, Blocked, Mitigated, etc.)

## 📁 Project Structure

```
Cyber_Crime_Analysis2/
│
├── app_v2.py                                      # Main Streamlit application
├── requirements_v2.txt                            # Python dependencies
├── runtime.txt                                    # Python version (3.9.18)
├── Global_Cybersecurity_Threats_2015-2024.csv    # Dataset (30,000 records)
├── README.md                                      # This file
│
├── modules_v2/                                    # Application modules
│   ├── advanced_visuals.py                       # 3D globe, Sankey, charts
│   ├── data_loader_v2.py                         # Data loading & processing
│   ├── glassmorphism_theme.py                    # UI theme and styling
│   ├── live_feed.py                              # Attack ticker & live feed
│   ├── data_loader_global.py                     # Global dataset handler
│   ├── visuals_global.py                         # Global visualizations
│   └── recent_attacks.py                         # Recent attacks display
│
├── DEPLOYMENT.md                                  # Deployment guide
├── DEPLOYMENT_READINESS.md                        # Deployment analysis
└── deployment_backup/                             # Backed up development files
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download

```bash
cd "C:\DAV project\Cyber_Crime_Analysis"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements_v2.txt
```

### Step 3: Run the Dashboard

```bash
streamlit run app_v2.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

## 📊 Data Overview

**Dataset**: `Global_Cybersecurity_Threats_2015-2024.csv`
- **Records**: 30,000 cyber attack events
- **Time Range**: 2019-2024 (6 years)
- **Core Fields** (16 columns):
  - **Temporal**: timestamp, year
  - **Geographic**: location (45 countries)
  - **Attack Info**: attack_type (23 types), attack_vector, attacker_origin
  - **Target**: target_industry (18 sectors), target_system
  - **Severity**: attack_severity (1-10 scale), attack_duration_min
  - **Impact**: financial_impact_USD, affected_users, data_compromised_GB
  - **Response**: response_time_min, mitigation_method, outcome
- **Analytics**:
  - Real-time severity scoring
  - Geographic attack distribution
  - Industry-specific threat patterns
  - Mitigation effectiveness analysis
  - Time-based attack correlations

## 🧠 Data Processing

The data processing pipeline includes:

1. **Timestamp Processing**
   - Parse timestamps to datetime format
   - Extract year, month, day, hour for temporal analysis
   - Calculate time-based patterns and trends

2. **Severity Normalization**
   - Convert severity to numeric scale (1-10)
   - Identify critical threats (severity ≥ 8)
   - Calculate average severity across filters

3. **Impact Metrics**
   - Financial impact converted to USD
   - Data compromised tracked in GB
   - Affected users aggregated by attack type
   - Response time analyzed in minutes

4. **Geographic Processing**
   - 45 countries mapped for 3D globe visualization
   - Attack density by location
   - Cross-border threat analysis

5. **Data Validation**
   - No duplicate records (30,000 unique incidents)
   - All critical fields validated
   - Cached for performance optimization

## 🤖 Advanced Analytics

DarkSentinel provides comprehensive threat intelligence:

- **Severity Analysis**: Real-time severity scoring (1-10 scale) with critical threat identification
- **Mitigation Tracking**: Success rates of different mitigation methods
- **Correlation Analysis**: 3D visualization of attack_severity × data_compromised × response_time
- **Temporal Patterns**: Time-of-day and day-of-week attack distribution
- **Geographic Insights**: 3D globe showing global attack distribution across 45 countries
- **Industry Targeting**: Sunburst and treemap views of industry-specific threats

## 📈 Key Insights from Dataset

From the 30,000 attack records (2019-2024):

- **Time Range**: 6 years of comprehensive threat data (2019-2024)
- **Attack Distribution**: ~5,000 attacks per year (evenly distributed)
- **Geographic Coverage**: 45 countries across all continents
- **Attack Diversity**: 23 distinct attack types including:
  - Ransomware, Phishing, DDoS, APT
  - Zero-Day Exploits, SQL Injection, XSS
  - Cryptojacking, IoT Attacks, Supply Chain Attacks
- **Industry Impact**: 18 sectors targeted (Finance, Healthcare, Government, etc.)
- **Financial Impact**: $1.2B total with individual attacks ranging from thousands to millions
- **Data Breaches**: 1,512.7 TB total data compromised
- **Affected Users**: 65.7 million users impacted globally

## 🎯 Use Cases

1. **Security Operations Centers (SOC)**: Real-time threat monitoring
2. **Incident Response Teams**: Pattern analysis and anomaly investigation
3. **Cybersecurity Training**: Educational demonstrations
4. **Research & Analysis**: Attack trend studies
5. **Executive Reporting**: High-level security metrics

## 🔧 Customization

### Modify Theme Colors

Edit `modules_v2/glassmorphism_theme.py` color definitions:

```python
st.markdown("""
<style>
    .main {
        background-color: #0b0f14;  /* Change background */
        color: #d0d7de;             /* Change text color */
    }
    /* ... */
</style>
""", unsafe_allow_html=True)
```

### Add New Visualizations

Add functions to `modules_v2/advanced_visuals.py` or `modules_v2/visuals_global.py`:

```python
def create_custom_chart(df, title='My Chart'):
    fig = px.bar(df, x='column', y='value', title=title)
    fig.update_layout(**PLOTLY_TEMPLATE['layout'])
    return fig
```

### Adjust Severity Thresholds

Modify severity calculations in `app_v2.py`:

```python
# Critical attacks threshold
critical_attacks = (filtered_df['severity_num'] >= 8).sum()

# Adjust mitigation rate calculation
defensive_keywords = ['block', 'quarantine', 'prevent', 'stop', 'resolve']
mitigation_rate = (defensive_count / total_attacks * 100)
```

## 📦 Deployment Options

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements_v2.txt
EXPOSE 8501
CMD ["streamlit", "run", "app_v2.py"]
```

### Render / Railway / Heroku

Follow platform-specific deployment guides for Streamlit apps.

## 🛠️ Troubleshooting

### Issue: "Module not found"
```bash
pip install --upgrade -r requirements_v2.txt
```

### Issue: "Data file not found"
Ensure `Global_Cybersecurity_Threats_2015-2024.csv` is in the project root directory

### Issue: Slow performance
- Reduce data size by filtering years
- Adjust `@st.cache_data` decorators
- Use smaller contamination value for anomaly detection

## 📚 Technologies Used

- **Streamlit 1.30.0**: Web framework for interactive dashboards
- **Pandas 2.1.4**: Data manipulation and analysis
- **Plotly 5.18.0**: Interactive 3D visualizations and charts
- **NumPy 1.26.2**: Numerical computing
- **Matplotlib 3.8.2**: Additional plotting capabilities
- **Scikit-learn 1.3.2**: Data analysis and metrics

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Real-time data ingestion via API
- [ ] User authentication and role-based access
- [ ] PDF report generation
- [ ] Email alerting for high-severity anomalies
- [ ] Integration with SIEM tools
- [ ] Advanced ML models (LSTM, Autoencoders)

## 📄 License

This project is for educational and demonstration purposes.

## 👨‍💻 Author

Created as part of cybersecurity data analysis project.

## 🙏 Acknowledgments

- Dataset: Synthetic cybersecurity attack data
- Inspiration: Modern SOC dashboards and threat intelligence platforms
- Theme: Inspired by cyberpunk aesthetics

---

**⚡ DarkSentinel - Illuminating the Dark Web of Cyber Threats**

For questions or support, please open an issue in the repository.
