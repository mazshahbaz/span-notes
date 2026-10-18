"""First module of the walking skeleton. Replace with the project's real code."""


def simple_span_moment(w: float, L: float) -> float:
    """Midspan moment (kN·m) of a simple span under a UDL w (kN/m) over span L (m): wL^2/8."""
    return w * L**2 / 8
