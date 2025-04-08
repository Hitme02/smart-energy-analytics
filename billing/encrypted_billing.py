# billing/encrypted_billing.py

import json
import time
import numpy as np
from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value
from utils.privacy_utils import add_differential_privacy_noise
from utils.compression_utils import compress_data, decompress_data

def simulate_usage():
    return round(np.random.uniform(2.0, 7.0), 2)  # Simulated usage in kWh

def calculate_bill(usage, rate_per_kwh=0.15):
    return round(usage * rate_per_kwh, 2)

if __name__ == "__main__":
    print("💸 Encrypted Real-Time Billing with Differential Privacy")
    context = get_ckks_context()

    for _ in range(10):
        usage = simulate_usage()
        encrypted_usage = encrypt_value(context, usage)
        bill = calculate_bill(decrypt_value(context, encrypted_usage))
        bill_with_noise = add_differential_privacy_noise(bill)

        data_packet = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "usage_kwh": usage,
            "bill": bill_with_noise,
            "device_id": "meter_001"
        }

        compressed = compress_data(data_packet)
        decompressed = decompress_data(compressed)

        print(f"[{decompressed['timestamp']}] ⚡ Usage: {usage} kWh | 💰 Bill (DP): ${bill_with_noise}")
        time.sleep(1)
