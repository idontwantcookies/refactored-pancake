from random import randint

from pytest import fixture, raises, mark

from cake import Vector, Matrix


@fixture
def v1():
    return Vector([1, 2])


@fixture
def v2():
    return Vector([3, 4])


@fixture
def v3():
    return Vector([0, -10, 1.4, 12, "string", ""])


@fixture
def b1():
    return Vector([True, True, False, False])


@fixture
def b2():
    return Vector([True, False, True, False])


def test_sum_2_vectors(v1, v2):
    assert all(v1 + v2 == [4, 6])


def test_sum_vector_and_number(v1):
    assert all(v1 + 1 == [2, 3])


def test_negative(v1):
    assert all(-v1 == [-1, -2])


def test_subtract_2_vectors(v1, v2):
    assert all(v1 - v2 == [-2, -2])


def test_subtract_vector_and_number(v1):
    assert all(v1 - 1 == [0, 1])


def test_multiply_2_vectors(v1, v2):
    assert all(v1 * v2 == [3, 8])


def test_multiply_vector_and_number(v1):
    assert all(v1 * 2 == [2, 4])


def test_matmul_vector_and_vector(v1, v2):
    assert v1 @ v2 == 11


def test_divide_2_vectors(v1, v2):
    assert all(v2 / v1 == [3, 2])


def test_divide_vector_and_number(v2):
    assert all(v2 / 2 == [1.5, 2])


def test_power_2_vectors(v1, v2):
    assert all(v1 ** v2 == [1, 16])


def test_power_vector_to_a_number(v1):
    assert all(v1 ** 2 == [1, 4])


def test_floor_division_2_vectors(v1, v2):
    assert all(v2 // v1 == [3, 2])


def test_floor_division_vector_and_number(v2):
    assert all(v2 // 2 == [1, 2])


def test_mod_2_vectors(v1, v2):
    assert all(v2 % v1 == [0, 0])


def test_mod_vector_and_number(v2):
    assert all(v2 % 2 == [1, 0])


def test_divmod_2_vectors(v1, v2):
    q, r = divmod(v2, v1)
    assert all(q == [3, 2])
    assert all(r == [0, 0])


def test_divmod_vector_and_number(v2):
    q, r = divmod(v2, 2)
    assert all(q == [1, 2])
    assert all(r == [1, 0])


def test_lshift_2_vectors(v1, v2):
    assert all(v1 << v2 == [8, 32])


def test_lshift_vector_and_number(v1):
    assert all(v1 << 2 == [4, 8])


def test_rshift_2_vectors(v1, v2):
    assert all(v2 >> v1 == [1, 1])


def test_rshift_vector_and_number(v2):
    assert all(v2 >> 1 == [1, 2])


def test_and_2_vectors(b1, b2):
    assert all(b1 & b2 == [True, False, False, False])


def test_or_2_vectors(b1, b2):
    assert all(b1 | b2 == [True, True, True, False])


def test_xor_2_vectors(b1, b2):
    assert all(b1 ^ b2 == [False, True, True, False])


def test_different_vectors_not_equal(v1, v2):
    with raises(AssertionError):
        assert all(v1 == v2)


def test_eq(v1, v2):
    assert all((v1 == v1) == [True, True])


def test_lt(v1, v2):
    assert all((v1 < v2) == [True, True])


def test_le(v1):
    assert all((v1 <= [1, 1]) == [True, False])


def test_gt(v1):
    assert all((v1 > [1 == 1]) == [False, True])


def test_ge(v1):
    assert all((v1 >= [2, 2]) == [False, True])


def test_ne(v1):
    assert all((v1 != [1 == 1]) == [False, True])


@mark.parametrize(
    "method",
    [
        "add",
        "sub",
        "mul",
        "matmul",
        "truediv",
        "floordiv",
        "mod",
        "divmod",
        "pow",
        "lshift",
        "rshift",
        "and",
        "xor",
        "or",
    ],
)
def test_rmethods(v1, v2, method):
    # guarantees that radd does the same as (left) add
    # (and all other r-magic methods)
    v1_left_op = getattr(v1, f"__{method}__")
    v2_right_op = getattr(v2, f"__r{method}__")
    comparison = v1_left_op(v2) == v2_right_op(v1)
    if type(comparison) is bool:
        assert comparison
    else:
        assert all(v1_left_op(v2) == v2_right_op(v1))


def test_as_bool(v3):
    assert all(v3.as_bool() == [False, True, True, True, True, False])


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
