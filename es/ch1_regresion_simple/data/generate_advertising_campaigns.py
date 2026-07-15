"""Regenerates advertising_campaigns.csv from the same draw used by simulations/linear_reg/best_line.py.

Kept alongside the CSV so the frozen dataset is reproducible and its provenance is explicit.
Run manually if the CSV ever needs to be regenerated; it is not called at book-build time.
"""
import numpy as np
import pandas as pd

DATA_SEED = 42
rng = np.random.default_rng(DATA_SEED)

n_points = 140
X = rng.uniform(0, 20, size=n_points)

true_beta0 = 10.0
true_beta1 = 2.0
sigma_noise = 8.0
Y = true_beta0 + true_beta1 * X + rng.normal(0, sigma_noise, size=n_points)

df = pd.DataFrame({
    "budget_usd_k": X,
    "revenue_usd_k": Y,
})
df.to_csv("advertising_campaigns.csv", index=False)
