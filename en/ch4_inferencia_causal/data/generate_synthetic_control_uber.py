"""Regenerates synthetic_control_uber_austin.csv from the same DGP used by
simulations/synthetic_control_weights/synthetic_control_weights.py's generate_scenario("full").

Kept alongside the CSV so the frozen dataset is reproducible and its provenance is explicit.
Run manually if the CSV ever needs to be regenerated; it is not called at book-build time.
"""
import numpy as np
import pandas as pd

CITY_NAMES = [
    "Nashville", "Charlotte", "Columbus", "Indianapolis", "Raleigh",
    "Sacramento", "Kansas City", "Cincinnati", "Salt Lake City", "Tucson",
    "Albuquerque", "Fresno", "Tulsa", "Omaha", "Louisville",
    "Richmond", "Boise", "Des Moines",
]
N_DONORS = len(CITY_NAMES)   # 18
T0 = 20                       # pre-intervention weeks
T_TOTAL = 32                  # 20 pre + 12 post
TRUE_EFFECT_PCT = 10          # dashboard's default true_effect

AUSTIN_Z = np.array([1.8, 72.0, 9.5, 38.0])   # population (M), income ($k), drivers (k), Lyft share (%)
THETA = np.array([18.0, 0.5, 3.2, -0.15])      # demographic loadings on the base ride level

# "full" donor pool demographics -- identical draw to generate_scenario("full")
rng = np.random.default_rng(42)
population = rng.uniform(0.4, 2.6, N_DONORS)
income = rng.uniform(45.0, 88.0, N_DONORS)
drivers = rng.uniform(2.0, 14.0, N_DONORS)
lyft_share = rng.uniform(20.0, 55.0, N_DONORS)
Z = np.column_stack([population, income, drivers, lyft_share])

weeks = np.arange(T_TOTAL)
trend = 2.0 + 0.15 * weeks

rng_noise = np.random.default_rng(123)
eps_donors = rng_noise.normal(0, 1.2, size=(N_DONORS, T_TOTAL))
eps_austin = rng_noise.normal(0, 1.2, size=T_TOTAL)

base_donors = Z @ THETA
base_austin = float(AUSTIN_Z @ THETA)

Y_donors = base_donors[:, None] + trend[None, :] + eps_donors
Y_austin_untreated = base_austin + trend + eps_austin

# Apply the true post-treatment lift to Austin only, same as apply_treatment() in the dashboard
Y_austin = Y_austin_untreated.copy()
Y_austin[T0:] = Y_austin[T0:] * (1 + TRUE_EFFECT_PCT / 100.0)

rows = []
for w in range(T_TOTAL):
    rows.append({
        "city": "Austin", "week": w + 1, "rides_thousands": Y_austin[w],
        "population_m": AUSTIN_Z[0], "income_k": AUSTIN_Z[1],
        "drivers_k": AUSTIN_Z[2], "lyft_share_pct": AUSTIN_Z[3],
        "is_treated_unit": 1, "post_period": int(w >= T0),
    })
for i, city in enumerate(CITY_NAMES):
    for w in range(T_TOTAL):
        rows.append({
            "city": city, "week": w + 1, "rides_thousands": Y_donors[i, w],
            "population_m": Z[i, 0], "income_k": Z[i, 1],
            "drivers_k": Z[i, 2], "lyft_share_pct": Z[i, 3],
            "is_treated_unit": 0, "post_period": int(w >= T0),
        })

df = pd.DataFrame(rows)
df.to_csv("synthetic_control_uber_austin.csv", index=False)
print(f"Wrote {len(df)} rows ({N_DONORS + 1} cities x {T_TOTAL} weeks). "
      f"True effect: {TRUE_EFFECT_PCT}% from week {T0 + 1}.")
