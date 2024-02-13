import numpy as np

# rounds 1.5 -> 2, 2.5 -> 3
def round_half_up(n, decimals=0):
    multiplier = 10**decimals
    return np.floor(n * multiplier + 0.5) / multiplier
