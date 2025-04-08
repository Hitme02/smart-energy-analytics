# data/load_real_data.py

import pandas as pd

def load_and_clean():
    df = pd.read_csv("data/household_power_consumption.txt", 
                     sep=';', 
                     parse_dates={'timestamp': ['Date', 'Time']},
                     infer_datetime_format=True,
                     na_values='?',
                     low_memory=False)

    df = df[['timestamp', 'Global_active_power']]
    df.dropna(inplace=True)
    df['Global_active_power'] = df['Global_active_power'].astype(float)
    df = df[df['Global_active_power'] > 0]
    df.rename(columns={'Global_active_power': 'energy_kwh'}, inplace=True)
    df['home_id'] = 'Home_1'

    df.to_csv("data/cleaned_energy_data.csv", index=False)
    print("✅ Cleaned data saved to data/cleaned_energy_data.csv")

if __name__ == "__main__":
    load_and_clean()
