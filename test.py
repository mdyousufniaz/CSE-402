from functools import partial
from math import floor, sqrt

from LCM import lcm

round_2 = partial(round, ndigits=2)

def k_s_test(data: tuple[float]) -> float:
    N = len(data)
    N_inverse = i_by_N = 1 / N
    data = tuple(sorted(data))

    D_plus = N_inverse - data[0]
    D_minus = data[0]

    tab_sep_print = partial(print, sep='\t')

    tab_sep_print('i', 'i/N', "D+ = i/N - R[i]", '(i - 1)/N', "D- = R[i] - (i - 1)/N")
    tab_sep_print(1, round_2(i_by_N), round_2(D_plus), 0.0, D_minus)
    max_D = max(D_plus, D_minus)

    for i, datum in enumerate(data[1:], 2):
        i_minus_1_by_N = i_by_N
        i_by_N = i / N
        D_plus = i_by_N - datum
        D_minus = datum - i_minus_1_by_N

        tab_sep_print(i, round_2(i_by_N), round_2(D_plus), round_2(i_minus_1_by_N), round_2(D_minus))
        max_D = max(max_D, D_plus, D_minus)
    
    return max_D

def chi_square_test(
    data: tuple[float],
    nbins: int
) -> float:
    N = len(data)
    E_i = N / nbins
    divider = 1 / E_i
    O = [0 for _ in range(nbins)]

    for datum in data:
        index = min(9, floor(datum / divider))
        O[index] += 1
    
    return round_2(
        sum(
            ((o - E_i) ** 2) / E_i
            for o in O
        )
    )

def auto_corr_test(
    data: tuple[float],
    i: int,
    l: int
) -> float:
    N = len(data)
    M = ((N - i) // l) - 1
    M_plus_1 = (M + 1)

    row_il = (
        sum(
            data[i + k * l - 1] * data[i + (k + 1) * l - 1]
            for k in range(M_plus_1)
        )
    ) / (M_plus_1) - 0.25
    std_deviation = sqrt(13 * M + 7) / (12 * (M_plus_1))

    return round_2(row_il / std_deviation)
    
    
def example_1() -> None:
    data = (0.44, 0.81, 0.14, 0.05, 0.93)
    max_D = k_s_test(data)
    print(f"{max_D = }")

def example_2() -> None:
    rng = lcm(x_0=123457, a=7 ** 5, m=2 ** 31 - 1, ndigits=4)
    data = tuple(
        next(rng)[1] for _ in range(100)
    )

    chi_square_val = chi_square_test(data, 10)
    print(f"{chi_square_val = }")

def example_3() -> None:
    dummy_data = [0] * 30
    for k, datum in zip(
        range(2, 31, 5),
        (0.23, 0.28, 0.33, 0.27, 0.05, 0.36)
    ): dummy_data[k] = datum

    Z_0 = auto_corr_test(dummy_data, 3, 5)
    print(f"{Z_0 = }")


if __name__ == '__main__':
    example_3()
