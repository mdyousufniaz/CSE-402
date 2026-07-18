import numpy as np

from utils import *

def execute_example_1() -> None:
    # the coefficient matrix 3x3
    A = np.array(
        (
            (25, 5, 1),
            (64, 8, 1),
            (144, 12, 1)
        )
    )

    # the constant tuple
    b = np.array((106.8, 177.2, 279.2))
    print(gauss_elimination(A, b))

def execute_example_2() -> None:
    A = np.array(
        (
            (20, 15, 10),
            (-3, -2.249, 7),
            (5, 1, 3)
        )
    )

    b = np.array((45, 1.751, 9))
    print(gauss_elimination(A, b, partial_pivot=True))

def execute_example_3() -> None:
    M = np.array(
        (
           (5, -1, 5),
           (-3, 2.099, -6),
           (-10, 7, 0) 
        )
    )

    print(det_by_gauss_elim(M))

def execute_example_4() -> None:
    A = np.array(
        (
            (3, -0.1, -0.2),
            (0.1, 7, -0.3),
            (0.3, -0.2, 10)
        )
    )

    b = np.array((7.85, -19.3, 71.4))
    gauss_jordan_elim(A, b)

def execute_example_5() -> None:
    A = np.array(
        (
            (25, 5, 1),
            (64, 8, 1),
            (144, 12, 1)
        )
    )

    C = np.array((106.8, 177.2, 279.2))

    inv_mat_using_LU_decompose(A)

def execute_example_6() -> None:
    A = np.array(
        (
            (3.556, -1.778, 0),
            (-1.778, 3.556, -1.778),
            (0, -1.778, 3.556) 
        )
    )

    power_1st(A, 4)

if __name__ == '__main__':
    execute_example_6()
    
