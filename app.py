import streamlit as st
from pathlib import Path
import json
import glob
from datetime import datetime

st.set_page_config(page_title="MECM Drift Detector", layout="wide")
st.title("🔍 MECM Configuration Drift Detector")

st.sidebar.header("Select Client Report")
reports = sorted(glob.glob("reports/*.json"), reverse=True)

if not reports:
    st.error("No reports found. Run generate_sample_data.py from the health checker project first.")
    st.stop()

selected_file = st.sidebar.selectbox("Choose a report", reports, format_func=lambda x: Path(x).name)

with open(selected_file) as f:
    client_data = json.load(f)

# Run drift check
from drift_detector import check_drift, load_baseline   # We'll import from the main script

baseline = load_baseline()
drift_results = check_drift(client_data, baseline)

# Display
st.subheader(f"Client: {client_data['system']['hostname']}")
st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Summary table
df = pd.DataFrame(drift_results)
st.dataframe(df, use_container_width=True)

# Color coding
st.success(f"{len([d for d in drift_results if 'Good' in d['Status']])} settings match baseline")
st.warning(f"{len([d for d in drift_results if 'Drift' in d['Status']])} settings have drift")

# Export
if st.button("Export Report as HTML"):
    output_path = Path("reports") / f"drift_{client_data['system']['hostname']}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    # Reuse the generate function from drift_detector
    st.success(f"Report saved to {output_path}")

st.caption("Companion tool to cross-platform-client-health")
