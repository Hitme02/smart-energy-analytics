# utils/privacy_utils.py

import random

def add_differential_privacy_noise(value, epsilon=1.0, sensitivity=1.0):
    """
    Add Laplace noise to the value for differential privacy.
    """
    scale = sensitivity / epsilon
    noise = random.gauss(0, scale)
    return value + noise
