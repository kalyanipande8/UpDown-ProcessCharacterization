"""End-to-end: simulate 120 batches across 9 upstream/downstream
parameters, compute SPC control limits, detect deviations, and verify
full CAPA coverage."""
import json
import os

from src.simulate_process_data import simulate, UPSTREAM_PARAMS, DOWNSTREAM_PARAMS
from src.spc_analysis import compute_control_limits, detect_deviations
from src.deviation_capa import generate_capas, verify_capa_coverage

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print("=== Simulating 120 batches across 9 upstream/downstream parameters ===")
df = simulate()
df.to_csv("data/batches.csv", index=False)
print(df.shape)
print(f"Upstream parameters: {list(UPSTREAM_PARAMS.keys())}")
print(f"Downstream parameters: {list(DOWNSTREAM_PARAMS.keys())}")

print("\n=== Computing SPC control limits (iterative refinement) ===")
limits = compute_control_limits(df)
for param, lim in limits.items():
    print(f"  {param}: mean={lim['mean']}, UCL={lim['ucl']}, LCL={lim['lcl']}")

print("\n=== Detecting deviations ===")
deviations = detect_deviations(df, limits)
deviations.to_csv("data/deviations.csv", index=False)
print(f"{len(deviations)} deviations detected")

print("\n=== Generating CAPAs and verifying coverage ===")
capas = generate_capas(deviations)
capas.to_csv("results/capa_records.csv", index=False)
coverage = verify_capa_coverage(deviations, capas)
print(coverage)

summary = {
    "n_batches": len(df),
    "n_parameters_tracked": len(UPSTREAM_PARAMS) + len(DOWNSTREAM_PARAMS),
    "n_deviations_detected": len(deviations),
    "n_capas_generated": len(capas),
    "capa_coverage_pct": coverage["pct_coverage"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
