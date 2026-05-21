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
import glob

def load_baseline():
    baseline_path = Path("baselines/default.json")
    if baseline_path.exists():
        with open(baseline_path) as f:
            return json.load(f)
    # Default baseline
    return {
        "min_disk_gb": 25,
        "max_memory_percent": 85,
        "mecm_installed": True,
        "power_plan": "Balanced"
    }

def check_drift(client_data, baseline):
    drift = []
    system = client_data.get("system", {})
    disk = client_data.get("disk", {})
    memory = client_data.get("memory", {})
    mecm = client_data.get("mecm", {})

    checks = [
        ("Disk Free Space (GB)", disk.get("free_gb"), baseline.get("min_disk_gb"), 
         lambda a, e: a is not None and a >= e),
        ("Memory Usage (%)", memory.get("percent_used"), baseline.get("max_memory_percent"), 
         lambda a, e: a is not None and a <= e),
        ("MECM Client Installed", mecm.get("installed"), baseline.get("mecm_installed"), 
         lambda a, e: a == e),
    ]

    for name, actual, expected, compare_func in checks:
        if actual is None or expected is None:
            status = "Unknown"
        elif compare_func(actual, expected):
            status = "✅ Good"
        else:
            status = "⚠️ Drift"
        
        drift.append({
            "Setting": name,
            "Expected": expected,
            "Actual": actual,
            "Status": status
        })
    
    return drift

def generate_html_report(client_data, drift_results, output_path):
    hostname = client_data["system"]["hostname"]
    
    html = f"""<!DOCTYPE html>
<html>
<head><title>Drift Report - {hostname}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }}
    h1 {{ color: #0078D4; }}
    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
    th {{ background: #0078D4; color: white; }}
    .drift {{ background: #fff3cd; }}
    .good {{ background: #d4edda; }}
</style>
</head>
<body>
    <h1>MECM Configuration Drift Report</h1>
    <p><strong>Client:</strong> {hostname} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    
    <h2>Drift Summary</h2>
    <table>
        <tr><th>Setting</th><th>Expected</th><th>Actual</th><th>Status</th></tr>
"""
    for item in drift_results:
        row_class = ' class="drift"' if "Drift" in item['Status'] else ' class="good"'
        html += f"<tr{row_class}><td>{item['Setting']}</td><td>{item['Expected']}</td><td>{item['Actual']}</td><td>{item['Status']}</td></tr>"
    
    html += "</table></body></html>"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description="MECM Configuration Drift Detector")
    parser.add_argument("--latest", action="store_true", help="Use most recent report")
    parser.add_argument("--client", help="Path to specific client JSON file")
    args = parser.parse_args()

    if args.client:
        client_path = Path(args.client)
    else:
        reports = sorted(glob.glob("reports/*.json"), reverse=True)
        if not reports:
            print("❌ No reports found in ./reports/")
            return
        client_path = reports[0]

    with open(client_path) as f:
        client_data = json.load(f)

    baseline = load_baseline()
    drift_results = check_drift(client_data, baseline)

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    
    report_path = output_dir / f"drift_{client_data['system']['hostname']}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    generate_html_report(client_data, drift_results, report_path)

    print(f"✅ Drift report generated for {client_data['system']['hostname']}")
    print(f"   → {report_path}")
    print("   Open the HTML file in your browser.")

if __name__ == "__main__":
    main()
