# realtime/realtime_anomaly_stream.py

import time
import pandas as pd
from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value

def realtime_stream(csv_path, delay=2.0, window_size=50, threshold_factor=2.0):
    df = pd.read_csv(csv_path)
    ctx = get_ckks_context()

    print(f"📡 Starting real-time anomaly detection...\n")

    for i in range(window_size, len(df)):
        window = df.iloc[i - window_size:i]
        mean = window["energy_kwh"].mean()
        std = window["energy_kwh"].std()
        upper = mean + threshold_factor * std
        lower = mean - threshold_factor * std

        row = df.iloc[i]
        usage = row["energy_kwh"]
        ts = row["timestamp"]

        encrypted_usage = encrypt_value(ctx, usage)
        decrypted_usage = decrypt_value(encrypted_usage, ctx)

        if decrypted_usage > upper or decrypted_usage < lower:
            print(f"[{ts}] ⚠️ Anomaly Detected: {decrypted_usage:.2f} kWh")
        else:
            print(f"[{ts}] ✅ OK: {decrypted_usage:.2f} kWh")

        time.sleep(delay)

if __name__ == "__main__":
    realtime_stream("data/cleaned_energy_data.csv", delay=1.0)
