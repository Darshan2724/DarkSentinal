# 🚀 DarkSentinel Quick Start Guide

## Running the Dashboard

### Option 1: Direct Python Command (Recommended)

```bash
python -m streamlit run app.py
```

### Option 2: Using Streamlit Command (if in PATH)

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501` or `http://localhost:8502`

## First Time Setup

1. **Install Dependencies** (one-time only)
   ```bash
   pip install streamlit pandas plotly scikit-learn
   ```

2. **Navigate to Project Directory**
   ```bash
   cd "C:\DAV project\Cyber_Crime_Analysis"
   ```

3. **Run the App**
   ```bash
   python -m streamlit run app.py
   ```

## Dashboard Navigation

### 📊 Overview Tab
- View KPIs: Total Attacks, Active Alerts, Blocked %, High Severity %, Unique IPs
- See attack type distribution by year
- Analyze severity level breakdown
- Track attacks over time

### 📈 Timeline & Trends Tab
- Monthly attack trends
- Day of week patterns
- Hourly distribution
- Interactive heatmap showing attack patterns by hour and day

### 🗺️ Geo & Heatmap Tab
- Top cities and states with most attacks
- Geographic distribution visualization
- Attack types by location

### 🔍 Attack Explorer Tab
- Search by IP address, user, or attack signature
- View detailed records with expandable details
- Export filtered data to CSV
- Examine payload data and attack signatures

### 💻 Devices & Browsers Tab
- Device/OS distribution
- Browser vulnerability analysis
- Traffic type by browser
- Average packet length by device

### 🌐 Network & Protocols Tab
- Protocol vs attack type analysis
- Sankey flow diagram (Protocol → Attack Type → Action)
- Packet length distribution
- Traffic type breakdown

### 🛡️ IDS/Firewall Tab
- Action taken distribution
- IDS/IPS alerts analysis
- Firewall logs overview
- Log source distribution

### ⚡ Anomalies & Reports Tab
- ML-based anomaly detection using Isolation Forest
- View top anomalous records
- Anomaly insights and patterns
- Export anomaly reports to CSV

## Using Filters

The sidebar contains powerful filters to drill down into the data:

1. **Year Filter**: Select one or multiple years (2020-2023)
2. **Month Filter**: Choose specific months
3. **Attack Type**: Filter by DDoS, Malware, or Intrusion
4. **Severity Level**: Low, Medium, or High
5. **Device/OS**: Windows, Linux, Macintosh, iPad, etc.
6. **Protocol**: TCP, UDP, ICMP

**Tip**: All filters work together - combine them for precise analysis!

## Exporting Data

### Export Filtered Data
1. Go to **Attack Explorer** tab
2. Apply your desired filters
3. Click **"📥 Download Filtered Data as CSV"**

### Export Anomalies
1. Go to **Anomalies & Reports** tab
2. Adjust the number of top anomalies to display
3. Click **"📥 Download Top Anomalies as CSV"**

## Performance Tips

- **Large Dataset**: If the app is slow, try filtering by year first
- **Anomaly Detection**: Runs automatically but may take 10-15 seconds
- **Refresh Data**: Use the sidebar menu → "Rerun" to reload data

## Keyboard Shortcuts

- `R` - Rerun the app
- `C` - Clear cache
- `Ctrl + K` - Open command palette

## Troubleshooting

### App Won't Start
```bash
# Check if Python is installed
python --version

# Reinstall dependencies
pip install --upgrade streamlit pandas plotly scikit-learn
```

### Port Already in Use
Streamlit will automatically try the next available port (8501, 8502, etc.)

### Data Not Loading
Ensure `cybersecurity_attacks.csv` is in the same directory as `app.py`

## Advanced Configuration

### Change Port
```bash
python -m streamlit run app.py --server.port 8080
```

### Disable Auto-Open Browser
```bash
python -m streamlit run app.py --server.headless true
```

### Enable Wide Mode by Default
Already configured in `app.py` with `layout="wide"`

## Next Steps

1. **Explore the Data**: Start with the Overview tab to get familiar
2. **Use Filters**: Try different filter combinations in the sidebar
3. **Analyze Anomalies**: Check the Anomalies tab for unusual patterns
4. **Export Reports**: Download data for further analysis
5. **Customize**: Edit `app.py` to add your own visualizations

## Support

For issues or questions:
- Check the main `README.md` for detailed documentation
- Review the Jupyter notebook `Cyber_crime_analysis.ipynb` for data insights
- Examine module files in the `modules/` folder for implementation details

---

**Happy Analyzing! 🛡️**

*DarkSentinel - Illuminating Cyber Threats*
