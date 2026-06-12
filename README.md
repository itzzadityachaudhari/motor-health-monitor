# 🔧 Industrial Motor Health Monitoring System

A Python-based monitoring tool that continuously checks key motor parameters — voltage, current, temperature, vibration, and RPM — and raises alerts when values exceed safe operating thresholds. Designed to prevent unplanned downtime before failures occur.

Inspired by hands-on maintenance work at **Banaras Locomotive Works (BLW)**, where motor failures caused costly unplanned downtime in railway locomotive operations.

---

## 🔍 Problem Statement

Industrial motors — especially in railway locomotives — run continuously under heavy load. When a motor overheats, draws excess current, or starts vibrating abnormally, it often leads to sudden failure. Manual inspection is periodic and can miss early warning signs.

This system automates continuous parameter monitoring and flags deviations **before** they become failures.

---

## ⚙️ How It Works

1. **Loads** sensor readings (voltage, current, temperature, vibration, RPM) from a CSV file
2. **Checks** every reading against predefined safe operating thresholds
3. **Flags** any reading that goes outside the safe range with a specific reason
4. **Generates** a per-motor dashboard showing all 5 parameters over time
5. **Exports** a CSV report of all alerts for engineer review

### Safe Operating Thresholds

| Parameter | Min | Max | Unit |
|---|---|---|---|
| Voltage | 380 | 440 | V |
| Current | 0 | 80 | A |
| Temperature | 0 | 85 | °C |
| Vibration | 0 | 4.5 | mm/s |
| Speed (RPM) | 1400 | 1510 | RPM |

---

## 📊 Output

| Output File | Description |
|---|---|
| `output/M001_dashboard.png` | Per-motor parameter trend with alert markers |
| `output/health_overview.png` | Fleet-wide bar chart — alerts per motor |
| `output/motor_alerts.csv` | CSV of all flagged readings with reasons |

### Sample Terminal Output

```
=================================================================
       MOTOR HEALTH MONITORING — ALERT REPORT
=================================================================
Total readings analyzed : 30
Alerts triggered        : 5
Motors with alerts      : 5
=================================================================

⚠  M001 — Traction Motor 1
   Time    : 2024-01-01 11:00:00
   Issue   : Temperature HIGH: 90°C (Safe: 0–85°C)

⚠  M002 — Traction Motor 2
   Time    : 2024-01-01 10:00:00
   Issue   : Voltage LOW: 290V (Safe: 380–440V)
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core language |
| Pandas | Data loading and threshold checking |
| Matplotlib | Dashboard charts and fleet overview |
| NumPy | Numerical operations |

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/motor-health-monitor.git
cd motor-health-monitor
```

### 2. Install dependencies
```bash
pip install pandas matplotlib numpy
```

### 3. Run the monitor
```bash
python monitor.py
```

---

## 📁 Project Structure

```
motor-health-monitor/
│
├── monitor.py           # Main monitoring script
├── motor_data.csv       # Sample dataset (5 motors, 6 readings each)
├── output/
│   ├── M001_dashboard.png
│   ├── M002_dashboard.png
│   ├── ...
│   ├── health_overview.png
│   └── motor_alerts.csv
└── README.md
```

---

## 💡 Real-World Context

During my internship at **Banaras Locomotive Works (BLW)**, I worked on maintenance, testing, and optimization of electrical systems in railway locomotives. Unplanned motor failures were a key challenge. This project is a direct conceptual extension of that experience — building a system that could have caught those failures early.

Achievements at BLW that this project addresses:
- Reduced unplanned downtime by **20%**
- Extended equipment lifespan by **25%**

---

## 👤 Author

**Aditya Kumar**  
B.Tech Electrical Engineering — NIT Manipur  
[LinkedIn](https://linkedin.com/in/aditya-kumar-565772274) | [GitHub](https://github.com/itzzadityachaudhari)
