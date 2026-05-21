#!/usr/bin/env python3
"""
MECM Configuration Drift Detector
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
    return {"power_plan": "Balanced", "firewall_enabled": True, "min_disk_gb": 25}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", help="Path to client JSON file")
    parser.add_argument("--latest", action="store_true", help="Use most recent report")
    args = parser.parse_args()

    baseline = load_baseline()

    # Auto-find latest if --latest is used
    if args.latest or not args.client:
        reports = sorted(glob.glob("reports/*.json"), reverse=True)
        if not reports:
            print("No reports found in ./reports/")
            return
        client_path = reports[0]
    else:
        client_path = args.client

    with open(client_path) as f:
        client_data = json.load(f)

    print(f"Analyzing drift for: {client_data['system']['hostname']}")
    # ... (rest of logic coming in next update)

    print("✅ Drift check complete!")

if __name__ == "__main__":
    main()
