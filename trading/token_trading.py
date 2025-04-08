import pandas as pd
import os

print("⚡ Calculating Token Balances...")

# Set paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "cleaned_energy_data.csv")

# Load data
df = pd.read_csv(data_path, parse_dates=['timestamp'])

# Group by home_id and sum energy usage
home_energy = df.groupby('home_id')['energy_kwh'].sum().reset_index()

# Token value per kWh
token_rate = 0.15  # 1 kWh = 0.15 tokens

# Calculate token balances
home_energy['token_balance'] = (home_energy['energy_kwh'] * token_rate).round(3)
token_balances = home_energy[['home_id', 'token_balance']].copy()

print("\n⚡ Initial Token Balances:")
print(token_balances)

# Show available home IDs
print("\n🏠 Available Home IDs:")
print(token_balances['home_id'].unique())

# Simulate a token transfer
from_id = "Home_1"
to_id = "Home_2"
transfer_amount = 5

print(f"\n🔁 Transferring {transfer_amount} tokens from {from_id} to {to_id}...")

if from_id in token_balances['home_id'].values and to_id in token_balances['home_id'].values:
    from_index = token_balances[token_balances['home_id'] == from_id].index[0]
    to_index = token_balances[token_balances['home_id'] == to_id].index[0]

    if token_balances.at[from_index, 'token_balance'] >= transfer_amount:
        token_balances.at[from_index, 'token_balance'] -= transfer_amount
        token_balances.at[to_index, 'token_balance'] += transfer_amount
        print("✅ Transfer successful.")
    else:
        print("❌ Transfer failed: Insufficient tokens.")
else:
    print("❌ Transfer failed: One or both home_ids do not exist.")

# Print updated balances
print("\n💰 Updated Token Balances:")
print(token_balances)

# Save updated balances
output_path = os.path.join(script_dir, "..", "output", "token_balances.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
token_balances.to_csv(output_path, index=False)
print(f"\n📦 Updated token balances saved to {output_path}")
