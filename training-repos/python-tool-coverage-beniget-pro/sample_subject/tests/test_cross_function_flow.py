from src.cross_function_flow import make_adder, scale_values


def test_make_adder():
    add5 = make_adder(5)
    assert add5(3) == 8


def test_scale_values():
    assert scale_values([1, 2, 3], 10) == [10, 20, 30]
