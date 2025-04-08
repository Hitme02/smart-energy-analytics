# processing/billing.py

from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value

def compute_encrypted_bill(usage_kwh, rate_per_kwh):
    ctx = get_ckks_context()
    encrypted_usage = encrypt_value(ctx, usage_kwh)
    encrypted_bill = encrypted_usage * rate_per_kwh
    return encrypted_bill, decrypt_value(encrypted_bill, ctx)

if __name__ == "__main__":
    usage = 103.5   # Replace with a sample value from your dataset
    rate = 0.18     # 18 cents per kWh
    encrypted_bill, decrypted_bill = compute_encrypted_bill(usage, rate)

    print(f"🔐 Encrypted bill: {encrypted_bill}")
    print(f"💰 Decrypted bill: ${decrypted_bill:.2f}")
