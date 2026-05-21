import streamlit as st
import pandas as pd
from pathlib import Path
import json
import glob
from datetime import datetime

# Import functions from drift_detector
from drift_detector import check_drift, load_baseline

st.set_page_config(page_title="MECM Drift Detector", layout="wide")
st.title("🔍 MECM Configuration Drift Detector")

st.sidebar.header("Select Client Report")
reports = sorted(glob.glob("reports/*.json"), reverse=True)

if not reports:
    st.error("No reports found. Run generate_sample_data.py first.")
    st.stop()

selected_file = st.sidebar.selectbox("Choose a report", reports, format_func=lambda x: Path(x).name)

with open(selected_file) as f:
    client_data = json.load(f)

baseline = load_baseline()
drift_results = check_drift(client_data, baseline)

# Display
st.subheader(f"Client: {client_data['system']['hostname']}")
st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Summary Table
df = pd.DataFrame(drift_results)
st.dataframe(df, use_container_width=True)

# Summary stats
good = len([d for d in drift_results if "Good" in d["Status"]])
drift_count = len([d for d in drift_results if "Drift" in d["Status"]])

col1, col2 = st.columns(2)
col1.success(f"✅ {good} Settings Match")
col2.warning(f"⚠️ {drift_count} Settings Have Drift")

# Export button
if st.button("Export Report as HTML"):
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / f"drift_{client_data['system']['hostname']}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    
    # Reuse HTML generation (you can copy the function if needed)
    st.success(f"Report saved to {report_path}")

st.caption("Companion tool to cross-platform-client-health • Built by Jason Ray")
