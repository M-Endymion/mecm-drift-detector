import streamlit as st
import pandas as pd
from pathlib import Path
import json
import glob
from datetime import datetime

# Import from drift_detector
from drift_detector import check_drift, load_baseline, generate_html_report

st.set_page_config(page_title="MECM Drift Detector", layout="wide")
st.title("🔍 MECM Configuration Drift Detector")

st.sidebar.header("Data")

# Generate Sample Data Button
if st.sidebar.button("📊 Generate Sample Data"):
    from generate_sample_data import generate_sample_data
    generate_sample_data(8)
    st.sidebar.success("✅ Sample data generated!")
    st.rerun()

reports = sorted(glob.glob("reports/*.json"), reverse=True)

if not reports:
    st.info("👋 No reports found yet. Click **'Generate Sample Data'** in the sidebar to get started.")
    st.stop()

selected_file = st.sidebar.selectbox("Choose a report", reports, format_func=lambda x: Path(x).name)

with open(selected_file) as f:
    client_data = json.load(f)

baseline = load_baseline()
drift_results = check_drift(client_data, baseline)

st.subheader(f"Client: {client_data['system']['hostname']}")
st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

df = pd.DataFrame(drift_results)
st.dataframe(df, use_container_width=True)

good = len([d for d in drift_results if "Good" in d["Status"]])
drift_count = len([d for d in drift_results if "Drift" in d["Status"]])

col1, col2 = st.columns(2)
col1.success(f"✅ {good} Settings Match")
col2.warning(f"⚠️ {drift_count} Settings Have Drift")

if st.button("Export Report as HTML"):
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = output_dir / f"drift_{client_data['system']['hostname']}_{timestamp}.html"
    
    generate_html_report(client_data, drift_results, report_path)
    
    st.success(f"Report saved!")
    with open(report_path, "rb") as f:
        st.download_button("⬇️ Download HTML Report", f, report_path.name, "text/html")

st.caption("Companion tool to cross-platform-client-health • Built by Jason Ray")
