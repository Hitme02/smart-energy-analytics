# prediction/demand_prediction.py

import pandas as pd
import numpy as np
from collections import defaultdict

def create_states(usages, num_bins=5):
    bins = np.linspace(min(usages), max(usages), num_bins + 1)
    return np.digitize(usages, bins) - 1, bins

def build_markov_chain(states):
    transition_matrix = defaultdict(lambda: defaultdict(int))

    for (current, nxt) in zip(states, states[1:]):
        transition_matrix[current][nxt] += 1

    # Normalize into probabilities
    for current in transition_matrix:
        total = sum(transition_matrix[current].values())
        for nxt in transition_matrix[current]:
            transition_matrix[current][nxt] /= total

    return transition_matrix

def predict_next(state, transition_matrix):
    if state not in transition_matrix:
        return state
    next_states = list(transition_matrix[state].keys())
    probs = list(transition_matrix[state].values())
    return np.random.choice(next_states, p=probs)

def run_prediction():
    df = pd.read_csv("data/cleaned_energy_data.csv")
    usages = df["energy_kwh"].values
    states, bins = create_states(usages)

    transition_matrix = build_markov_chain(states)

    current_state = states[-1]
    predictions = []

    print("📈 Predicting next 10 time steps:")
    for _ in range(10):
        next_state = predict_next(current_state, transition_matrix)
        # Convert bin back to estimated kWh usage
        usage_range = (bins[next_state], bins[next_state + 1])
        predicted_usage = np.mean(usage_range)
        predictions.append(predicted_usage)
        print(f"🔮 Predicted Usage: {predicted_usage:.2f} kWh")
        current_state = next_state

if __name__ == "__main__":
    run_prediction()
