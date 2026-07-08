"""Minimal subject code exercising All Uses Coverage patterns."""


def compute_total(items, threshold):
    """C-Use, P-Use, and multiple definitions."""
    total = 0
    for item in items:
        if item > threshold:
            total = total + item
        else:
            total = total - item
    return total


def make_adder(base):
    """Cross-function use: base defined in outer scope, used in inner function."""

    def adder(value):
        return value + base

    return adder


def unreachable_branch(flag):
    x = 1
    if flag:
        return x + 2
    return x
