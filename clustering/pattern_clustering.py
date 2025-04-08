import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import os

print("🔍 Clustering Energy Usage Patterns...")

# Load and preprocess data
df = pd.read_csv("data/historical_energy.csv", parse_dates=["timestamp"])
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.date
df.rename(columns={"usage_kWh": "usage_kwh"}, inplace=True)

# Create pivot: one row per day, columns = hourly usage
pivot = df.pivot_table(index='day', columns='hour', values='usage_kwh', aggfunc='mean').fillna(0)

# Normalize data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(pivot)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(data_scaled)
pivot['cluster'] = labels

# Reattach timestamps for aggregation
pivot['day'] = pivot.index

# Create summaries per cluster
summaries = []
for cluster_id in sorted(pivot['cluster'].unique()):
    cluster_days = pivot[pivot['cluster'] == cluster_id].index
    cluster_df = df[df['timestamp'].dt.date.isin(cluster_days)]

    hourly_means = cluster_df.groupby(cluster_df['timestamp'].dt.hour)['usage_kwh'].mean()
    avg_daily = cluster_df.groupby(cluster_df['timestamp'].dt.date)['usage_kwh'].sum().mean()

    # Detect peak usage period
    peak_hour = hourly_means.idxmax()
    peak_val = hourly_means.max()

    description = f"""
🔹 **Cluster {cluster_id + 1} Summary**
- Most active hour: {peak_hour}:00 ({peak_val:.2f} kWh)
- Average daily usage: {avg_daily:.2f} kWh
- Hourly breakdown:
"""
    for hour in range(24):
        usage = hourly_means.get(hour, 0.0)
        description += f"  - {hour:02d}:00 → {usage:.2f} kWh\n"
    summaries.append(description)

# Save readable summary
os.makedirs("output", exist_ok=True)
with open("output/cluster_summary_report.txt", "w", encoding="utf-8") as f:
    for summary in summaries:
        f.write(summary + "\n")

print("📄 Cluster summary report saved to output/cluster_summary_report.txt")