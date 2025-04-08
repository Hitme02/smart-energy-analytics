# processing/encrypted_batch_billing.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value

def process_bills(csv_path, rate_per_kwh=0.18, limit=10):
    # Load real energy usage
    df = pd.read_csv(csv_path).head(limit)  # limit for demo/testing

    ctx = get_ckks_context()

    print(f"\n🔒 Processing encrypted bills for {limit} smart meter readings:\n")

    results = []

    for idx, row in df.iterrows():
        usage = row["energy_kwh"]
        ts = row["timestamp"]

        encrypted_usage = encrypt_value(ctx, usage)
        encrypted_bill = encrypted_usage * rate_per_kwh
        bill_amount = decrypt_value(encrypted_bill, ctx)

        print(f"[{ts}] Usage: {usage:.2f} kWh → 💰 Encrypted Bill: ${bill_amount:.2f}")
        results.append((ts, usage, bill_amount))

    return results

if __name__ == "__main__":
    process_bills("data/cleaned_energy_data.csv", limit=10)
