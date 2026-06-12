"""
Industrial Motor Health Monitoring System
==========================================
Monitors key motor parameters (voltage, current, temperature, vibration, RPM)
and raises alerts when values exceed safe operating thresholds —
helping prevent unplanned downtime before failures occur.

Author  : Aditya Kumar
College : NIT Manipur | Electrical Engineering
Inspired by maintenance work at Banaras Locomotive Works (BLW)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── SAFE OPERATING THRESHOLDS ────────────────────────────────────────────────
# These are based on standard industrial motor safety limits
THRESHOLDS = {
    "voltage_V"      : {"min": 380,  "max": 440,  "unit": "V",    "label": "Voltage"},
    "current_A"      : {"min": 0,    "max": 80,   "unit": "A",    "label": "Current"},
    "temperature_C"  : {"min": 0,    "max": 85,   "unit": "°C",   "label": "Temperature"},
    "vibration_mm_s" : {"min": 0,    "max": 4.5,  "unit": "mm/s", "label": "Vibration"},
    "rpm"            : {"min": 1400, "max": 1510, "unit": "RPM",  "label": "Speed (RPM)"},
}

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data(filepath):
    """Load motor sensor data from CSV."""
    df = pd.read_csv(filepath, parse_dates=["timestamp"])
    print(f"✔  Loaded {len(df)} readings for {df['motor_id'].nunique()} motors.\n")
    return df


def check_thresholds(df):
    """
    Check every reading against safe thresholds.
    Flag the reading if any parameter is outside its safe range.
    """
    results = []

    for _, row in df.iterrows():
        alerts = []

        for param, limits in THRESHOLDS.items():
            value = row[param]
            if value < limits["min"] or value > limits["max"]:
                direction = "HIGH" if value > limits["max"] else "LOW"
                alerts.append(
                    f"{limits['label']} {direction}: {value}{limits['unit']} "
                    f"(Safe: {limits['min']}–{limits['max']}{limits['unit']})"
                )

        results.append({
            "timestamp"    : row["timestamp"],
            "motor_id"     : row["motor_id"],
            "motor_name"   : row["motor_name"],
            "voltage_V"    : row["voltage_V"],
            "current_A"    : row["current_A"],
            "temperature_C": row["temperature_C"],
            "vibration_mm_s": row["vibration_mm_s"],
            "rpm"          : row["rpm"],
            "alert_count"  : len(alerts),
            "is_alert"     : len(alerts) > 0,
            "alert_details": " | ".join(alerts) if alerts else "Normal",
        })

    return pd.DataFrame(results)


def print_report(result_df):
    """Print a clean alert summary to terminal."""
    alerts = result_df[result_df["is_alert"]]

    print("=" * 65)
    print("       MOTOR HEALTH MONITORING — ALERT REPORT")
    print("=" * 65)
    print(f"Total readings analyzed : {len(result_df)}")
    print(f"Alerts triggered        : {len(alerts)}")
    print(f"Motors with alerts      : {alerts['motor_id'].nunique()}")
    print("=" * 65)

    if alerts.empty:
        print("✅ All motors operating within safe parameters.")
        return

    for motor_id, group in alerts.groupby("motor_id"):
        motor_name = group["motor_name"].iloc[0]
        print(f"\n⚠  {motor_id} — {motor_name}")
        for _, row in group.iterrows():
            print(f"   Time    : {row['timestamp']}")
            print(f"   Issue   : {row['alert_details']}")
            print()

    print("=" * 65)


def plot_motor_dashboard(result_df):
    """
    For each motor, plot all 5 parameters over time.
    Red line = threshold limit. Red dot = alert reading.
    """
    motors = result_df["motor_id"].unique()
    params = list(THRESHOLDS.keys())
    param_labels = [THRESHOLDS[p]["label"] + f" ({THRESHOLDS[p]['unit']})" for p in params]

    for motor_id in motors:
        motor_data = result_df[result_df["motor_id"] == motor_id].copy()
        motor_name = motor_data["motor_name"].iloc[0]

        fig, axes = plt.subplots(len(params), 1, figsize=(12, 14), sharex=True)
        fig.suptitle(f"Motor Health Dashboard — {motor_id} ({motor_name})",
                     fontsize=13, fontweight="bold")

        for i, (param, label) in enumerate(zip(params, param_labels)):
            ax     = axes[i]
            limits = THRESHOLDS[param]

            normal = motor_data[~motor_data["is_alert"]]
            alerted = motor_data[motor_data["is_alert"]]

            ax.plot(motor_data["timestamp"], motor_data[param],
                    color="#1F4E79", linewidth=2, marker="o", markersize=4, zorder=2)

            # Highlight alert points in red
            ax.scatter(alerted["timestamp"], alerted[param],
                       color="red", s=80, zorder=3, label="Alert")

            # Draw threshold lines
            ax.axhline(limits["max"], color="orange", linestyle="--",
                       linewidth=1.2, label=f"Max: {limits['max']}")
            if limits["min"] > 0:
                ax.axhline(limits["min"], color="green", linestyle="--",
                           linewidth=1.2, label=f"Min: {limits['min']}")

            # Shade danger zone
            ax.axhspan(limits["max"], motor_data[param].max() * 1.1,
                       alpha=0.08, color="red")

            ax.set_ylabel(label, fontsize=8)
            ax.legend(fontsize=7, loc="upper right")
            ax.grid(True, alpha=0.3)

            # Annotate alert
            for _, row in alerted.iterrows():
                ax.annotate("⚠", xy=(row["timestamp"], row[param]),
                            xytext=(0, 8), textcoords="offset points",
                            color="red", fontsize=10, ha="center")

        axes[-1].set_xlabel("Timestamp", fontsize=9)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        out_path = os.path.join(OUTPUT_DIR, f"{motor_id}_dashboard.png")
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"✔  Dashboard saved → {out_path}")
        plt.close()


def plot_health_overview(result_df):
    """
    Overview bar chart — how many alerts each motor triggered.
    Green = healthy, Red = needs attention.
    """
    summary = result_df.groupby("motor_id")["alert_count"].sum().reset_index()
    summary["color"] = summary["alert_count"].apply(lambda x: "#C0392B" if x > 0 else "#27AE60")
    summary["motor_name"] = summary["motor_id"].map(
        result_df.drop_duplicates("motor_id").set_index("motor_id")["motor_name"]
    )
    labels = summary["motor_id"] + "\n" + summary["motor_name"]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(labels, summary["alert_count"], color=summary["color"], edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, summary["alert_count"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                str(val), ha="center", va="bottom", fontsize=10, fontweight="bold")

    healthy_patch = mpatches.Patch(color="#27AE60", label="Healthy (0 alerts)")
    alert_patch   = mpatches.Patch(color="#C0392B", label="Needs Attention")
    ax.legend(handles=[healthy_patch, alert_patch])

    ax.set_title("Motor Fleet Health Overview — Total Alerts per Motor",
                 fontweight="bold", fontsize=12)
    ax.set_ylabel("Number of Alerts")
    ax.set_ylim(0, summary["alert_count"].max() + 1)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "health_overview.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"✔  Health overview saved → {out_path}")
    plt.close()


def save_alert_csv(result_df):
    """Save all alert records to CSV for engineer review."""
    alerts   = result_df[result_df["is_alert"]]
    out_path = os.path.join(OUTPUT_DIR, "motor_alerts.csv")
    alerts.to_csv(out_path, index=False)
    print(f"✔  Alert records saved → {out_path}")


# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df        = load_data("motor_data.csv")
    result_df = check_thresholds(df)

    print_report(result_df)
    save_alert_csv(result_df)
    plot_motor_dashboard(result_df)
    plot_health_overview(result_df)

    print("\n✅  Monitoring complete. Check the 'output/' folder for dashboards.")
