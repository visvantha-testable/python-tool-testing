"""Cross-function def-use patterns for Inter-procedural Tracking metric."""


def make_adder(base):
    """Defines base in outer scope; inner adder uses it."""

    def adder(value):
        return value + base

    return adder


def scale_values(values, factor):
    """Uses helper that shares def-use across function boundary."""

    def scaler(x):
        return x * factor

    return [scaler(v) for v in values]
