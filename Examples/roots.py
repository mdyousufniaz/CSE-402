from math import trunc, log10
from typing import Callable

def get_sf(abs_eplison_a: float) -> int:
    return trunc(log10(2 * abs_eplison_a))

def find_root(
    method: str = 'bi-section',
    f: Callable[[float], float],
    x_l: float,
    x_u: float,
    m: int,
    print_as_table: bool = True
) -> float:

    if f(x_l) * f(x_u) >= 0:
        raise ValueError("f(x_l) * f(x_u) must be < 0")

    if m < 0:
        raise ValueError(f"m must be >= 0, found{m = }")

    prev_x_new = None

    print()
    while True:
        x_new = round(
            (x_l + x_u) / 2
            if method == 'bi-section'
            else (x_l * f(x_u) - x_u * f(x_l) / (f(x_u) - f(x_l))),
            5
        )

        abs_eplison_a = (
            None
            if prev_x_new is None
            else round((x_new - prev_x_new) / x_new, 2)
        )



        if (result := (f(x_l) * f(x_new))) == 0: return x_new
        elif result < 0: x_u = x_new


    
    
    while (
        prev_x_new is None
        and get_sf(abs_eplison_a) < m
    ):
        x_new = round(
            (x_l + x_u) / 2
            if method == 'bi-section'
            else (x_l * f(x_u) - x_u * f(x_l) / (f(x_u) - f(x_l))),
            5
        )

        if prev_x_new is not None:
            abs_eplison_a = (x_new - prev_x_new) / x_new
        
        prev_x_new = x_new

        if (result := (f(x_l) * f(x_new))) == 0:
            return x_new, abs_eplison_a
        
    

f_of_x = lambda x: x ** 3 - 0.165 * x ** 2 + 3.993e-4
