from typing import Callable
from math import sin, pi
from functools import partial

from LCM import lcm

tab_sep_print = partial(print, sep='\t')
RNG = lcm(x_0=123457, a=7 ** 5, m=2 ** 31 - 1, ndigits=4)

def monte_carlo(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int
) -> float:
    b_minus_a = b - a
    total = 0.0

    for _ in range(n):
        rn = next(RNG)[1]
        x_i = a + b_minus_a * rn
        total += f(x_i)
    
    return round(
        (b_minus_a * total) / n,
        3
    )

def example_1() -> None:
    true_val = 2
    base_mc = partial(monte_carlo, f=sin, a=0, b=pi)

    tab_sep_print('n', 'Y^(n)', 'Error')
    for n in (10, 20, 40, 80, 160, 1000, 10000):
        y_i = base_mc(n=n)
        tab_sep_print(n, y_i, f"{abs(y_i - true_val):.4f}")

def example_2() -> None:
    tab_sep_print('n', 'pi_^')

    for p in range(2, 7):
        n = 10 ** p
        pi_cap = sum(
            (
                4
                if sum((next(RNG)[1]) ** 2 for _ in range(2)) <= 1
                else 0
            )
            for _ in range(n)
        ) / n
        tab_sep_print(n, round(pi_cap, 5))


if __name__ == '__main__': example_2()

