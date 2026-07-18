import numpy as np
from math import log10

def gauss_elimination(
    coff_mat: np.ndarray,
    const_arr: np.ndarray,
    partial_pivot: bool = False
) -> list[np.float64]:
    # initial variables
    n = coff_mat.shape[0]
    pivot_row_index = 0
    aug_mat = np.hstack((coff_mat, const_arr.reshape(-1, 1)))
    
    # forward elimination
    while pivot_row_index < n - 1:
        if partial_pivot:
            max_pivot_row_index = np.argmax(
                np.abs(
                    aug_mat[
                        pivot_row_index:,
                        pivot_row_index
                    ]
                )
            ) + pivot_row_index

            if max_pivot_row_index != pivot_row_index:
                aug_mat[
                    [pivot_row_index, max_pivot_row_index]
                ] = aug_mat[
                    [max_pivot_row_index, pivot_row_index]
                ]

        starting_row_index = pivot_row_index + 1
        pivot_val = aug_mat[pivot_row_index, pivot_row_index]

        for row_index, _ in enumerate(aug_mat[starting_row_index:], starting_row_index):
            m = aug_mat[row_index, pivot_row_index] / pivot_val
            aug_mat[row_index] -= m * aug_mat[pivot_row_index]

        pivot_row_index += 1

    # back substitution
    coff_mat, const_mat = np.split(
        aug_mat, (n, ),
        axis=1
    )

    roots = []
    curr_row_index = n - 1

    while curr_row_index >= 0:
        root = (
            (
                const_mat[curr_row_index, 0]
                - sum(
                    coff_mat[curr_row_index, n - 1 - root_index] * root for root_index, root in enumerate(roots)
                )
            )
            / coff_mat[curr_row_index, curr_row_index]
        )
        roots.append(root)
        curr_row_index -= 1
    
    return roots[::-1]

def det_by_gauss_elim(
    mat: np.ndarray
) -> float:
    mat = mat.astype(float).copy()
    n = mat.shape[0]
    pivot_row_index = 0
    is_positive = True

    # forward elimination
    while pivot_row_index < n - 1:
        max_pivot_row_index = np.argmax(
            np.abs(
                mat[
                    pivot_row_index:,
                    pivot_row_index
                ]
            )
        ) + pivot_row_index

        if max_pivot_row_index != pivot_row_index:
            is_positive = not is_positive
            mat[
                [pivot_row_index, max_pivot_row_index]
            ] = mat[
                [max_pivot_row_index, pivot_row_index]
            ]

        starting_row_index = pivot_row_index + 1
        pivot_val = mat[pivot_row_index, pivot_row_index]

        for row_index, _ in enumerate(mat[starting_row_index:], starting_row_index):
            m = mat[row_index, pivot_row_index] / pivot_val
            mat[row_index] -= m * mat[pivot_row_index]
        
        pivot_row_index += 1

    return (
        (det := np.prod(np.diag(mat)))
        if is_positive else -det
    ) 

def gauss_jordan_elim(
    coff_mat: np.ndarray,
    const_arr: np.ndarray,
    partial_pivot: bool = True
) -> None:
    n = coff_mat.shape[0]
    aug_mat = np.hstack(
        (
            coff_mat,
            const_arr.reshape(-1, 1)
        )
    )

    for row_index in range(n):
        if partial_pivot:
            max_pivot_row_index = np.argmax(
                np.abs(
                    aug_mat[
                        row_index:,
                        row_index
                    ]
                )
            ) + row_index

            if max_pivot_row_index != row_index:
                aug_mat[
                    [row_index, max_pivot_row_index]
                ] = aug_mat[
                    [max_pivot_row_index, row_index]
                ]
        aug_mat[row_index] /= aug_mat[row_index, row_index]
        for other_row_index in set(range(n)) - {row_index}:
            aug_mat[other_row_index] -= aug_mat[other_row_index, row_index] * aug_mat[row_index]

    print(aug_mat)

def back_substitution(
    curr: int,
    n: int,
    U: np.ndarray,
    C: np.ndarray
) -> list[float]:
    if curr < n:
        roots = back_substitution(
            curr + 1,
            n, U, C
        )

    elif curr == n: 
        roots = [C[n] / U[n, n]]
        return roots

    x = (
        C[curr]
        - sum(
            U[curr, curr + 1 + x_in] * x
            for x_in, x in enumerate(roots)
        )
    ) / U[curr, curr]
    roots.insert(0, x)
    return roots

def front_substitution(
    L: np.ndarray,
    C: np.ndarray | list[float],
    initial: int
) -> list[float]:
    X = []
    for c_in, c_val in enumerate(C):
        x = (
            c_val
            - sum(
                L[c_in, x_in] * x_val
                for x_in, x_val in enumerate(X)
            )
        ) / L[c_in, c_in]
        X.append(x)

    return X

def LU_decompose(
    A: np.ndarray,
    C: np.ndarray
):
    A = A.astype(float).copy()
    n = A.shape[0]
    L = np.identity(3)

    pivot_row_index = 0

    for pivot_row_index in range(n - 1):
        pivot_val = A[pivot_row_index, pivot_row_index]

        for row_index in range(pivot_row_index + 1, n):
            m = A[curr_idx := (row_index, pivot_row_index)] / pivot_val
            A[row_index] -= m * A[pivot_row_index]
            L[curr_idx] = m

    return L, A

    # # front substitution
    # Z = front_substitution(L, C, 0)
    # print(Z)

    # X = back_substitution(0, n - 1, A, Z)
    # print(X)

def inv_mat_using_LU_decompose(
    A: np.ndarray
) -> np.ndarray:
    n = A.shape[0]
    L, U = LU_decompose(A, None)

    I = np.identity(n)
    B = []
    for col in I.T:
        Z = front_substitution(L, col, 0)
        X = back_substitution(0, n - 1, U, Z)
        B.append(X)

    B = np.array(B).T
    print(B)

def significant_digits(abs_epsilon_a: float) -> int:
    print(abs_epsilon_a)
    return -log10(2 * abs_epsilon_a)

def power_1st(
    A: np.ndarray,
    sig_digits: int
) -> np.ndarray:
    n = A.shape[0]
    # x_0 = np.random.rand(n, 1)
    x_0 = np.array(
        (1, 1, 1)
    ).reshape(-1, 1)
    print(f"{x_0 = }")

    abs_epsilon_a = prev_lambda = None
    iter = 0
    print(
        "iter",
        "x_k",
        "lambda",
        "|e_a|",
        sep='\t'
    )
    print(
        iter,
        x_0,
        None,
        abs_epsilon_a,
        sep='\t'
    )

    prev_eigen_vector = x_0

    while (
        abs_epsilon_a is None
        or significant_digits(abs_epsilon_a) < sig_digits
    ):
        y_k = A @ prev_eigen_vector
        y_k /= (curr_lambda := y_k.flat[np.abs(y_k).argmax()])

        if prev_lambda is not None:
            abs_epsilon_a = abs(
                1 - (prev_lambda / curr_lambda)
            )

        iter += 1

        print(
            iter,
            y_k,
            curr_lambda,
            abs_epsilon_a,
            sep='\t'
        )

        prev_lambda = curr_lambda
        prev_eigen_vector = y_k

    print(f"eigen_value = {prev_lambda}")




    

    
    
    


    

    


        

