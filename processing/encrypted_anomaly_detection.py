import time
import random
from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value
from utils.compression_utils import compress_data, decompress_data
from privacy.differential_privacy import add_laplace_noise

# Initialize CKKS encryption context
context = get_ckks_context()

print("🚨 Real-Time Encrypted Anomaly Detection with Compression + Differential Privacy")

while True:
    # Simulate real-time energy usage in kWh
    usage_kwh = round(random.uniform(1.0, 8.0), 2)

    # Encrypt usage data
    encrypted_usage = encrypt_value(context, usage_kwh)

    # Compress the encrypted value (simulate storing encrypted+compressed data)
    compressed = compress_data({'usage_kwh': usage_kwh})

    # Decompress and decrypt
    decompressed = decompress_data(compressed)
    decrypted_usage = float(decompressed['usage_kwh'])

    # ✅ Apply differential privacy to the decrypted usage
    noisy_usage = add_laplace_noise(decrypted_usage, epsilon=1.0)

    # Simulate anomaly detection (dummy logic)
    is_anomaly = noisy_usage > 9.0 or noisy_usage < 0.5
    status = "🚨 Anomaly" if is_anomaly else "✅ Normal"

    # Show output
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ⚡ Usage (DP): {round(noisy_usage, 2)} kWh {status}")

    time.sleep(1)
