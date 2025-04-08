import time
import random
from utils.compression_utils import compress_data, decompress_data
from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value

print("📊 Real-Time Peak Load Forecasting with Encryption & Compression")

context = get_ckks_context()

def generate_usage():
    return round(random.uniform(1.0, 10.0), 2)

window_size = 5
usage_window = []

while True:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    usage = generate_usage()

    # Encryption & Compression
    encrypted_usage = encrypt_value(context, usage)
    compressed_data = compress_data({
        'timestamp': timestamp,
        'usage_kwh': usage
    })

    # Decompression & Decryption (simulated)
    decompressed_data = decompress_data(compressed_data)
    decrypted_usage = decrypt_value(context, encrypted_usage)

    usage_window.append(decrypted_usage)
    if len(usage_window) > window_size:
        usage_window.pop(0)

    # Forecasting peak usage in window
    peak = max(usage_window)
    print(f"[{timestamp}] ⚡ Current: {decrypted_usage:.2f} kWh | 🔺 Forecasted Peak (next): {peak:.2f} kWh")

    time.sleep(1)
