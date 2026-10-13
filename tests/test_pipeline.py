import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.simulate_process_data import simulate, UPSTREAM_PARAMS, DOWNSTREAM_PARAMS, ALL_PARAMS
from src.spc_analysis import compute_control_limits, detect_deviations
from src.deviation_capa import generate_capas, verify_capa_coverage


@pytest.fixture(scope="module")
def df():
    return simulate()


@pytest.fixture(scope="module")
def deviations(df):
    limits = compute_control_limits(df)
    return detect_deviations(df, limits)


def test_120_batches_simulated(df):
    assert len(df) == 120


def test_nine_parameters_tracked():
    assert len(ALL_PARAMS) == 9
    assert len(UPSTREAM_PARAMS) == 4
    assert len(DOWNSTREAM_PARAMS) == 5


def test_control_limits_computed_for_every_parameter(df):
    limits = compute_control_limits(df)
    assert set(limits.keys()) == set(ALL_PARAMS.keys())
    for lim in limits.values():
        assert lim["lcl"] < lim["mean"] < lim["ucl"]


def test_deviations_are_detected(deviations):
    assert len(deviations) > 0


def test_deviations_found_across_multiple_parameters(deviations):
    """Confirms the injected excursions in several different parameters
    are all actually caught, not just one."""
    assert deviations["parameter"].nunique() >= 5


def test_capa_coverage_is_genuinely_complete(deviations):
    capas = generate_capas(deviations)
    result = verify_capa_coverage(deviations, capas)
    assert result["pct_coverage"] == 100.0
    assert result["missing"] == []
