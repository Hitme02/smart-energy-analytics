import time
import random
import csv
import os
from datetime import datetime
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from collections import deque

# Initialize rolling buffer
usage_buffer = deque(maxlen=30)
forecast_buffer = deque(maxlen=10)

CSV_FILE = "forecasting/peak_forecast_log.csv"
THRESHOLD = 5.5  # kWh for alert
SPIKE_THRESHOLD = 2.5  # sudden jump in usage
ANOMALY_STD_DEV_FACTOR = 2.0

# Ensure log file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Current Usage (kWh)", "Predicted Peak (kWh)", "Status", "Tags"])

print("📊 Real-Time Peak Load Forecasting with ARIMA, Alerts & Anomaly Detection")

while True:
    # Simulate current usage
    current_usage = round(random.uniform(2.0, 7.0), 2)
    usage_buffer.append(current_usage)

    # Forecast using ARIMA if enough data
    if len(usage_buffer) > 10:
        try:
            model = ARIMA(list(usage_buffer), order=(2, 1, 2))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)[0]
        except Exception as e:
            forecast = current_usage
    else:
        forecast = current_usage

    forecast_buffer.append(forecast)

    # Tagging
    tags = []
    status = "✅ Normal"

    if forecast > THRESHOLD:
        status = "🚨 High Forecasted Peak Load!"
        tags.append("High Forecast")

    if len(usage_buffer) >= 3:
        delta = current_usage - usage_buffer[-2]
        if abs(delta) > SPIKE_THRESHOLD:
            tags.append("🔥 High Usage Spike")

    # Anomaly detection
    if len(usage_buffer) >= 10:
        window = list(usage_buffer)[-10:]
        mean = np.mean(window)
        std = np.std(window)
        if std > 0:
            if current_usage > mean + ANOMALY_STD_DEV_FACTOR * std:
                tags.append("🟥 Anomaly: Sudden Spike")
            elif current_usage < mean - ANOMALY_STD_DEV_FACTOR * std:
                tags.append("🟥 Anomaly: Sudden Drop")

    # Logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ⚡ Current Usage: {current_usage} kWh | 📈 Predicted Peak Load: {round(forecast, 2)} kWh | {status}", end="")
    if tags:
        print(" | " + " | ".join(tags))
    else:
        print()

    with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, round(current_usage, 2), round(forecast, 2), status, " | ".join(tags)])

    time.sleep(1)
