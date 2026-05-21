#!/usr/bin/env python3
"""
MECM Configuration Drift Detector
Author: Jason Ray (M-Endymion)
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse

def load_baseline(baseline_path="baselines/default.json"):
    with open(baseline_path) as f:
        return json.load(f)

def check_drift(client_data, baseline):
    drift_report = []
    
    # Example checks - expand these!
    checks = [
        ("Power Plan", client_data.get("power_plan"), baseline.get("power_plan")),
        ("Firewall Enabled", client_data.get("firewall_enabled"), baseline.get("firewall_enabled")),
        ("Disk Free GB", client_data.get("disk_free_gb"), baseline.get("min_disk_gb")),
    ]
    
    for name, actual, expected in checks:
        status = "Match" if actual == expected else "Drift"
        drift_report.append({
            "Setting": name,
            "Expected": expected,
            "Actual": actual,
            "Status": status
        })
    
    return drift_report

def generate_html_report(client_data, drift_results, output_path):
    html = f"""<!DOCTYPE html>
<html>
<head><title>Drift Report - {client_data['hostname']}</title>
<style>
    body {{ font-family: Arial; margin: 40px; }}
    h1 {{ color: #0078D4; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 12px; }}
    th {{ background: #0078D4; color: white; }}
    .drift {{ background: #fff3cd; }}
</style>
</head>
<body>
    <h1>MECM Configuration Drift Report</h1>
    <p><strong>Client:</strong> {client_data['hostname']} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    
    <h2>Drift Summary</h2>
    <table>
        <tr><th>Setting</th><th>Expected</th><th>Actual</th><th>Status</th></tr>
"""
    for item in drift_results:
        row_class = ' class="drift"' if item['Status'] == "Drift" else ""
        html += f"<tr{row_class}><td>{item['Setting']}</td><td>{item['Expected']}</td><td>{item['Actual']}</td><td>{item['Status']}</td></tr>"
    
    html += "</table></body></html>"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, help="Path to client health JSON")
    args = parser.parse_args()

    # Load client data
    with open(args.client) as f:
        client_data = json.load(f)

    baseline = load_baseline()
    drift_results = check_drift(client_data, baseline)

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    
    report_path = output_dir / f"drift_{client_data['system']['hostname']}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    generate_html_report(client_data, drift_results, report_path)

    print(f"✅ Drift report generated: {report_path}")

if __name__ == "__main__":
    main()
