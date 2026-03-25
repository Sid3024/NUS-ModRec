import numpy as np
def softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    """
    Compute the softmax of a vector with optional temperature scaling.

    Softmax converts a vector of real values into a probability distribution,
    where each value lies in (0, 1) and the total sums to 1:

        softmax(x_i) = exp(x_i / T) / sum_j exp(x_j / T)

    where T is the temperature.

    Args:
        x (np.ndarray): Input array of real values.
        temperature (float, optional): Temperature parameter controlling the
            sharpness of the distribution. Defaults to 1.0.
            - T < 1.0 → sharper (more peaked) distribution
            - T > 1.0 → smoother (more uniform) distribution

    Returns:
        np.ndarray: Probability distribution of the same shape as x.

    Raises:
        ValueError: If temperature <= 0.

    Notes:
        - Applies a numerical stability trick by subtracting the maximum value
          from x before exponentiation to prevent overflow.
        - Input is cast to float64 for numerical precision.
        - Commonly used to normalize scores into probabilities (e.g., selection
          probabilities in recommendation or sampling systems).
    """
    if temperature <= 0:
        raise ValueError("temperature must be > 0 for softmax")
    x = np.asarray(x, dtype=np.float64)
    x = x / temperature
    x_shifted = x - np.max(x)
    x_exp = np.exp(x_shifted)
    return x_exp / np.sum(x_exp)