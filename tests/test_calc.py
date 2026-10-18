import pytest

from calc import simple_span_moment


def test_simple_span_moment_udl():
    # Source: hand calc, wL^2/8 = 10 x 20^2 / 8 = 500 kN·m
    assert simple_span_moment(10, 20) == pytest.approx(500)
