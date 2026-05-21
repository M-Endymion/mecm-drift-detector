<div align="center">
  <img src="https://raw.githubusercontent.com/M-Endymion/mecm-drift-detector/main/thumbnail-drift-detector.png" alt="MECM Drift Detector" width="100%" />
</div>

<br>

# MECM Configuration Drift Detector

A practical tool to detect and report **configuration drift** between MECM/SCCM baselines and actual client state.

Built as a companion to my [`cross-platform-client-health`](https://github.com/M-Endymion/cross-platform-client-health) and [`mecm-health-dashboard`](https://github.com/M-Endymion/mecm-health-dashboard) projects.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## Features

- Detects drift in key settings (Disk Space, Memory, MECM Client, etc.)
- Generates clean HTML reports
- CLI + **Streamlit web dashboard** versions
- Easy to extend with your own baseline checks

---

## Quick Start

```bash
git clone https://github.com/M-Endymion/mecm-drift-detector.git
cd mecm-drift-detector
pip install -r requirements.txt
```

Generate sample data (optional):
```bash
python generate_sample_data.py
```

Run CLI version:
```bash
python drift_detector.py --latest
```

Run Web Dashboard:
```bash
streamlit run app.py
```

---

## How It Works

1. Uses client health reports from the cross-platform health checker
2. Compares against a baseline (baselines/default.json)
3. Highlights drift in an easy-to-read report
4. Exports beautiful HTML reports (with PDF coming soon)

---

## Project Structure

- ```drift_detector.py``` — Core CLI tool
- ```app.py``` — Streamlit web dashboard
- ```generate_sample_data.py``` — Creates test reports
- ```reports/``` — Generated HTML reports
- ```baselines/``` — Your configuration baselines

---

## Future Enhancements

- More policy checks (registry keys, services, compliance items)
- Direct MECM database / WMI integration
- Historical drift tracking
- PDF export with charts

---

**Jason Ray (M-Endymion)**
MECM/SCCM Automation Specialist

- **LinkedIn:** Jason Ray
- **Portfolio:** m-endymion.github.io

**Last Updated:** May 2026

---
