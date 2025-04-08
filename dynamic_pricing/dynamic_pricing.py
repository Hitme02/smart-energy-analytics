import pandas as pd
import numpy as np
from datetime import datetime
import os

print("⚙️ Calculating Dynamic Pricing Based on Time and Load...")

# Resolve path to cleaned data relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "cleaned_energy_data.csv")

# Load cleaned data
df = pd.read_csv(data_path, parse_dates=['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.date

# Define base price and factors
base_price = 0.15  # base price per kWh
peak_hours = range(17, 21)  # 5pm to 8pm

# Calculate average hourly usage
hourly_usage = df.groupby('hour')['energy_kwh'].mean()

# Vectorized dynamic pricing calculation
df['hourly_avg_usage'] = df['hour'].map(hourly_usage)
df['load_factor'] = df['hour'].apply(lambda h: 1.5 if h in peak_hours else 1.0)
df['usage_factor'] = 1 + (df['hourly_avg_usage'] / hourly_usage.max())
df['dynamic_price'] = (base_price * df['load_factor'] * df['usage_factor']).round(4)

# Save result
output_path = os.path.join(script_dir, "..", "output", "dynamic_pricing_output.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df[['timestamp', 'energy_kwh', 'dynamic_price']].to_csv(output_path, index=False)

print("💰 Dynamic pricing output saved to output/dynamic_pricing_output.csv")