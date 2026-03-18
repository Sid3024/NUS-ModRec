import numpy as np
def softmax(x: np.ndarray, temperature: int = 1.0):
    if temperature <= 0:
        raise ValueError("temperature must be > 0 for softmax")
    x = np.asarray(x, dtype=np.float64)
    x = x / temperature
    x_shifted = x - np.max(x)
    x_exp = np.exp(x_shifted)
    return x_exp / np.sum(x_exp)