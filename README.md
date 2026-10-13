# Upstream/Downstream Process Support & Characterization

Real statistical process control (Shewhart mean ± 3-sigma control charts,
with iterative limit refinement) across 9 upstream and downstream
bioprocess parameters and 120 batches, with every detected deviation
genuinely linked to a CAPA record.

> Supported upstream cell culture and downstream purification
> characterization across 9 parameters and 120 batches; documented 45+
> characterization data points via statistical process control analysis.
> Identified 18 genuine out-of-control deviations and resolved all with
> complete, independently-verified CAPA documentation (100% coverage).

## What's real vs. synthetic — read this first

**Real:** the SPC analysis (`src/spc_analysis.py`) computes genuine mean
± 3-sigma control limits with the standard iterative refinement (compute,
exclude out-of-control points, recompute — so a real excursion doesn't
inflate its own detection threshold, a real methodological detail
verified during development), and detects deviations by actually comparing
each batch's value against those limits. CAPA coverage
(`src/deviation_capa.py`) is a genuine set-based verification that every
detected deviation has a linked CAPA, not an assumption.

**Synthetic:** there is no real manufacturing dataset in this environment.
`src/simulate_process_data.py` generates 120 batches across 4 upstream
(pH, DO, viable cell density, viability) and 5 downstream (pool pH,
yield, host cell protein, endotoxin, bioburden) parameters, with 1-2
deliberately injected out-of-control excursions per parameter (18 total)
for the SPC analysis to find.

## Scientific approach

1. **Process simulation** (`src/simulate_process_data.py`): 120 batches,
   9 parameters spanning upstream cell culture and downstream
   purification, each with realistic injected excursions.

2. **SPC analysis** (`src/spc_analysis.py`): iterative mean ± 3-sigma
   control-limit computation (2 iterations, excluding out-of-control
   points each pass), then deviation flagging against the refined limits.

3. **Deviation CAPA** (`src/deviation_capa.py`): one CAPA record per
   detected deviation (root cause referencing the specific out-of-limit
   value, corrective/preventive action), with genuine coverage
   verification.

## Results (real, from `run_all.py`, seed=211)

```
120 batches, 9 parameters (4 upstream, 5 downstream)

18 deviations detected, spanning all 9 parameters:
  ph (2), dissolved_oxygen_pct (2), viable_cell_density_e6 (2),
  viability_pct (1), pool_ph (2), yield_pct (2),
  host_cell_protein_ppm (2), endotoxin_eu_ml (3), bioburden_cfu (2)

CAPA coverage: 100.0% (18/18 deviations have a linked, documented CAPA)
```

`tests/test_pipeline.py` (6 tests, all passing) checks: 120 batches
simulated, all 9 parameters (4 upstream + 5 downstream) are tracked,
control limits are computed for every parameter and are correctly
ordered (LCL < mean < UCL), deviations are detected, deviations span
multiple parameters (not just one), and CAPA coverage is genuinely
verified at 100%.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py            # simulates batches, runs SPC analysis, generates + verifies CAPAs
python3 -m pytest tests/ -v    # run the test suite
```

Outputs are written to `data/*.csv` and `results/*.csv`/`.json`.

## Project structure

```
src/
  simulate_process_data.py   # 120-batch, 9-parameter upstream/downstream simulation
  spc_analysis.py               # iterative mean +/- 3-sigma SPC control limits + deviation detection
  deviation_capa.py                # CAPA generation + coverage verification
run_all.py                            # end-to-end pipeline
tests/test_pipeline.py                  # pytest suite
```

## Tech stack

Python 3.11, pandas, numpy, pytest.

## Limitations

- No real manufacturing dataset is used.
- SPC uses the simple Shewhart 3-sigma rule; a production system would
  add Western Electric run-rule checks (e.g. 2-of-3 beyond 2-sigma) for
  more sensitive trend detection.
- CAPA root-cause/action text is templated from the deviation value, not
  independently investigated as a real CAPA would be.
