from random import randint

from pytest import raises

from cake import Matrix, Vector


def generate_random_matrix(m: int, n: int):
    out = Matrix()
    for i in range(m):
        row = Vector()
        for j in range(n):
            row.append(randint(-50, 50))
        out.append(row)
    return out


def assert_matrix_equality(first, second):
    assert len(first) == len(second)
    i = 0
    for x, y in zip(first, second):
        assert len(x) == len(y)
        assert all(x == y)
        i += 1


def test_fail_different_row_sizes():
    with raises(AssertionError):
        A = generate_random_matrix(2, 2)
        B = generate_random_matrix(1, 2)
        assert_matrix_equality(A, B)


def test_fail_different_col_sizes():
    with raises(AssertionError):
        A = generate_random_matrix(1, 2)
        B = generate_random_matrix(1, 1)
        assert_matrix_equality(A, B)


def test_fail_different_values():
    with raises(AssertionError):
        A = Matrix([[1, 1], [0, 1]])
        B = Matrix([[1, 1], [1, 1]])
        assert_matrix_equality(A, B)


def test_str():
    m = generate_random_matrix(2, 2)
    assert "\n" in m.__repr__()


def test_setitem_encapsulates_as_vector():
    m = generate_random_matrix(2, 2)
    m[0] = [2, 1]
    assert type(m[0]) is Vector


def test_append_encapsulates_as_vector():
    m = generate_random_matrix(2, 2)
    m.append([2, 1])
    assert type(m[2]) is Vector


def test_transposition():
    m = generate_random_matrix(4, 3)
    assert_matrix_equality(m, m.transpose().transpose())


def test_matmul():
    A = Matrix([[2, 3], [-1, 4]])
    B = Matrix([[1, 2, 3], [4, 5, 6]])
    assert_matrix_equality(A @ B, [[14, 19, 24], [15, 18, 21]])
    assert_matrix_equality(B.transpose() @ A, [[-2, 19], [-1, 26], [0, 33]])


def test_rmatmul():
    A = [[2, 3], [-1, 4]]
    B = Matrix([[1, 2, 3], [4, 5, 6]])
    assert_matrix_equality(A @ B, [[14, 19, 24], [15, 18, 21]])


def test_deep_copy():
    A = Matrix([[2, 1], [-1, 5]])
    B = A.copy()
    B[0][0] = 3
    assert A[0][0] == 2
    assert B[0][0] != A[0][0]
