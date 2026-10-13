"""Simulate 120 batches tracked across 9 upstream and downstream process
parameters, with a few genuine, deliberately injected out-of-control
excursions -- the setting for real statistical process control (SPC)
deviation detection."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_BATCHES = 120
SEED = 211

UPSTREAM_PARAMS = {
    "ph": (7.0, 0.1), "dissolved_oxygen_pct": (45, 5), "viable_cell_density_e6": (8, 1.2),
    "viability_pct": (97, 1.5),
}
DOWNSTREAM_PARAMS = {
    "pool_ph": (3.8, 0.15), "yield_pct": (85, 4), "host_cell_protein_ppm": (50, 15),
    "endotoxin_eu_ml": (0.05, 0.02), "bioburden_cfu": (1, 0.8),
}
ALL_PARAMS = {**UPSTREAM_PARAMS, **DOWNSTREAM_PARAMS}


def simulate(n: int = N_BATCHES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    data = {"batch_id": [f"B-{i:03d}" for i in range(n)]}
    for param, (mean, std) in ALL_PARAMS.items():
        data[param] = rng.normal(mean, std, n)

    df = pd.DataFrame(data)

    # inject a handful of genuine out-of-control excursions (real
    # deviations, ~1-2 per parameter) at known batch indices
    for param, (mean, std) in ALL_PARAMS.items():
        n_excursions = rng.integers(1, 3)
        idx = rng.choice(df.index, size=n_excursions, replace=False)
        direction = rng.choice([-1, 1], n_excursions)
        df.loc[idx, param] = mean + direction * rng.uniform(4, 6, n_excursions) * std

    return df


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
