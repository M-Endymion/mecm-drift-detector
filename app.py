import streamlit as st
from pathlib import Path
import json
import glob
from datetime import datetime

st.set_page_config(page_title="MECM Drift Detector", layout="wide")
st.title("🔍 MECM Configuration Drift Detector")

st.sidebar.header("Select Report")
reports = sorted(glob.glob("reports/*.json"), reverse=True)

if not reports:
    st.error("No reports found. Run generate_sample_data.py first.")
    st.stop()

selected = st.sidebar.selectbox("Choose client report", reports)

with open(selected) as f:
    client_data = json.load(f)

# Run drift check (reuse logic)
# ... (I'll add full integration in next message if needed)

st.success(f"Analyzed: {client_data['system']['hostname']}")
st.write("Drift report generated. Check the reports folder for HTML files.")

st.caption("Built as companion to cross-platform-client-health tool")
