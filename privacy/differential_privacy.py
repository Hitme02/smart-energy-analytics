# privacy/differential_privacy.py

import random

def add_laplace_noise(value, sensitivity=1.0, epsilon=0.5):
    scale = sensitivity / epsilon
    noise = random.gauss(0, scale)
    return value + noise
