import random
from encryption.ckks_utils import get_ckks_context, encrypt_value, decrypt_value

# Setup CKKS context
context = get_ckks_context()

# Simulate buyer demands and seller supplies (in kWh)
buyers = {f"buyer_{i}": round(random.uniform(1.0, 5.0), 2) for i in range(5)}
sellers = {f"seller_{i}": round(random.uniform(2.0, 5.0), 2) for i in range(5)}

# Encrypt the values
enc_buyers = {b: encrypt_value(context, val) for b, val in buyers.items()}
enc_sellers = {s: encrypt_value(context, val) for s, val in sellers.items()}

print("🔌 Buyers' demand (kWh):")
for b, val in buyers.items():
    print(f"{b}: {val} kWh")

print("\n⚡ Sellers' supply (kWh):")
for s, val in sellers.items():
    print(f"{s}: {val} kWh")

print("\n🔄 Matching Buyers and Sellers (Encrypted Simulation):")

# Match buyers with sellers
buyer_index = 0
seller_index = 0
buyer_keys = list(enc_buyers.keys())
seller_keys = list(enc_sellers.keys())

while buyer_index < len(buyer_keys) and seller_index < len(seller_keys):
    buyer = buyer_keys[buyer_index]
    seller = seller_keys[seller_index]

    # Decrypt values for comparison (only locally in simulation)
    b_demand = decrypt_value(context, enc_buyers[buyer])
    s_supply = decrypt_value(context, enc_sellers[seller])

    if s_supply >= b_demand:
        print(f"{seller} sells {b_demand:.2f} kWh to {buyer}")
        enc_sellers[seller] = encrypt_value(context, s_supply - b_demand)
        buyer_index += 1
    else:
        print(f"{seller} sells {s_supply:.2f} kWh to {buyer}")
        enc_buyers[buyer] = encrypt_value(context, b_demand - s_supply)
        seller_index += 1
