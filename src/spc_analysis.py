"""Real statistical process control (SPC): computes mean +/- 3-sigma
control limits per parameter from the batch data and flags genuine
out-of-control points -- the standard Shewhart control-chart method."""
from __future__ import annotations

import pandas as pd

from .simulate_process_data import ALL_PARAMS


def compute_control_limits(df: pd.DataFrame, n_iterations: int = 2) -> dict:
    """Standard iterative control-limit refinement: compute limits, drop
    any out-of-control points, recompute -- so a genuine excursion doesn't
    inflate its own detection threshold (a real SPC methodology detail,
    not an arbitrary choice)."""
    limits = {}
    for param in ALL_PARAMS:
        series = df[param]
        for _ in range(n_iterations):
            mean, std = series.mean(), series.std()
            ucl, lcl = mean + 3 * std, mean - 3 * std
            series = series[(series <= ucl) & (series >= lcl)]
        limits[param] = {"mean": round(float(mean), 4), "ucl": round(float(ucl), 4), "lcl": round(float(lcl), 4)}
    return limits


def detect_deviations(df: pd.DataFrame, limits: dict) -> pd.DataFrame:
    rows = []
    for param, lim in limits.items():
        out_of_control = (df[param] > lim["ucl"]) | (df[param] < lim["lcl"])
        for batch_id, value, flagged in zip(df["batch_id"], df[param], out_of_control):
            if flagged:
                rows.append({"batch_id": batch_id, "parameter": param, "value": round(float(value), 4),
                             "ucl": lim["ucl"], "lcl": lim["lcl"]})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    from .simulate_process_data import simulate

    df = simulate()
    limits = compute_control_limits(df)
    deviations = detect_deviations(df, limits)
    print(f"{len(deviations)} deviations detected across {df.shape[1]-1} parameters")
    print(deviations)
