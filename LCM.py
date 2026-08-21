from typing import Generator
from functools import partial

def lcm(
    x_0: int, # seed
    a: int,
    m: int, # upper bound
    c: int = 0,
    ndigits: int = 2
) -> Generator[tuple[int, float], None, None]:
    x_i = x_0
    while True:
        x_i = ((a * x_i + c) % m)
        yield x_i, round(x_i / m, ndigits)

def example_1(n: int = 3) -> None:
    rng = lcm(x_0=27, a=17, m=100, c=43)

    print(*(next(rng)[1] for _ in range(n)), sep=' ')

def example_2(n: int = 4) -> None:
    base_rng = partial(lcm, a=13, m=64)

    for x_0 in range(1, n + 1):
        print(f"{x_0 = }: ", end='')
        rng = base_rng(x_0)

        count = 0
        period = ''
        while (x_i := next(rng)[0]) != x_0:
            count += 1
            period += f'{x_i} '
        
        print(f"{period}{x_0}, count = {count + 1}")

def example_3(n: int = 3) -> None:
    rng = lcm(x_0=123457, a=7 ** 5, m=2 ** 31 - 1, ndigits=4)

    print(*(next(rng) for _ in range(n)), sep=' ')

def main() -> None:
    # example_1()
    # example_2(10)
    example_3()

if __name__ == '__main__': main()