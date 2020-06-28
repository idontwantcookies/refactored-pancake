from unittest import TestCase, main
from random import randint

from linalg import Vector, Matrix


class VectorTestCase(TestCase):
	def setUp(self):
		self.v1 = Vector([1,2])
		self.v2 = Vector([3,4])
		self.v3 = Vector([0, -10, 1.4, 12, 'string', ''])
		self.b1 = Vector([True, True, False, False])
		self.b2 = Vector([True, False, True, False])

	def assertVectorEqual(self, first, second):
		if len(first) != len(second):
			self.fail(f'{first} and {second} have different sizes.')
		for x, y in zip(first, second):
			if x != y:
				self.fail(f'{first} != {second}')

	def test_sum_2_vectors(self):
		self.assertVectorEqual(self.v1 + self.v2, [4, 6])

	def test_sum_vector_and_number(self):
		self.assertVectorEqual(self.v1 + 1, [2, 3])

	def test_negative(self):
		self.assertVectorEqual(-self.v1, [-1, -2])

	def test_subtract_2_vectors(self):
		self.assertVectorEqual(self.v1 - self.v2, [-2, -2])

	def test_subtract_vector_and_number(self):
		self.assertVectorEqual(self.v1 - 1, [0, 1])

	def test_multiply_2_vectors(self):
		self.assertVectorEqual(self.v1 * self.v2, [3, 8])

	def test_multiply_vector_and_number(self):
		self.assertVectorEqual(self.v1 * 2, [2, 4])

	def test_matmul_vector_and_vector(self):
		self.assertEqual(self.v1 @ self.v2, 11)

	def test_divide_2_vectors(self):
		self.assertVectorEqual(self.v2 / self.v1, [3, 2])

	def test_divide_vector_and_number(self):
		self.assertVectorEqual(self.v2 / 2, [1.5, 2])

	def test_power_2_vectors(self):
		self.assertVectorEqual(self.v1 ** self.v2, [1, 16])

	def test_power_vector_to_a_number(self):
		self.assertVectorEqual(self.v1 ** 2, [1, 4])

	def test_floor_division_2_vectors(self):
		self.assertVectorEqual(self.v2 // self.v1, [3, 2])

	def test_floor_division_vector_and_number(self):
		self.assertVectorEqual(self.v2 // 2, [1, 2])

	def test_mod_2_vectors(self):
		self.assertVectorEqual(self.v2 % self.v1, [0, 0])

	def test_mod_vector_and_number(self):
		self.assertVectorEqual(self.v2 % 2, [1, 0])

	def test_divmod_2_vectors(self):
		q, r = divmod(self.v2, self.v1)
		self.assertVectorEqual(q, [3, 2])
		self.assertVectorEqual(r, [0, 0])

	def test_divmod_vector_and_number(self):
		q, r = divmod(self.v2, 2)
		self.assertVectorEqual(q, [1, 2])
		self.assertVectorEqual(r, [1, 0])

	def test_lshift_2_vectors(self):
		self.assertVectorEqual(self.v1 << self.v2, [8, 32])

	def test_lshift_vector_and_number(self):
		self.assertVectorEqual(self.v1 << 2, [4, 8])

	def test_rshift_2_vectors(self):
		self.assertVectorEqual(self.v2 >> self.v1, [1, 1])

	def test_rshift_vector_and_number(self):
		self.assertVectorEqual(self.v2 >> 1, [1, 2])

	def test_and_2_vectors(self):
		self.assertVectorEqual(self.b1 & self.b2, [True, False, False, False])

	def test_or_2_vectors(self):
		self.assertVectorEqual(self.b1 | self.b2, [True, True, True, False])

	def test_xor_2_vectors(self):
		self.assertVectorEqual(self.b1 ^ self.b2, [False, True, True, False])

	def test_different_sizes_not_equal(self):
		with self.assertRaises(AssertionError):
			self.assertVectorEqual([1, 2, 3], [1, 2])

	def test_different_vectors_not_equal(self):
		with self.assertRaises(AssertionError):
			self.assertVectorEqual(self.v1, self.v2)

	def test_eq(self):
		self.assertVectorEqual(self.v1 == self.v1, [True, True])

	def test_lt(self):
		self.assertVectorEqual(self.v1 < self.v2, [True, True])

	def test_le(self):
		self.assertVectorEqual(self.v1 <= [1, 1], [True, False])

	def test_gt(self):
		self.assertVectorEqual(self.v1 > [1, 1], [False, True])

	def test_ge(self):
		self.assertVectorEqual(self.v1 >= [2, 2], [False, True])

	def test_ne(self):
		self.assertVectorEqual(self.v1 != [1, 1], [False, True])

	def test_rmethods(self):
		# guarantees that radd does the same as add (and all other r-magic methods)
		for method in ('add', 'sub', 'mul', 'matmul', 'truediv', 'floordiv', 'mod', 'divmod', 'pow', 'lshift', 'rshift', 'and', 'xor', 'or'):
			left = getattr(self.v1, f'__{method}__')
			right = getattr(self.v2, f'__r{method}__')
			self.assertEqual(left(self.v2), right(self.v1))

	def test_as_bool(self):
		self.assertVectorEqual(self.v3.as_bool(), [False, True, True, True, True, False])


class MatrixTestCase(TestCase):
	def generate_random_matrix(self, m:int, n:int):
		out = Matrix()
		for i in range(m):
			row = Vector()
			for j in range(n):
				row.append(randint(-50, 50))
			out.append(row)
		return out

	def assertMatrixEqual(self, first, second):
		if len(first) != len(second):
			self.fail(f'{first} and {second} have different sizes.')
		i = 0
		for x, y in zip(first, second):
			if len(x) != len(y):
				self.fail(f'Mismatched sizes on rows {i}: {x} != {y}')
			if any(x != y):
				self.fail(f'Different rows on index {i}: {x} != {y}')
			i += 1

	def test_fail_different_row_sizes(self):
		with self.assertRaises(AssertionError):
			A = self.generate_random_matrix(2, 2)
			B = self.generate_random_matrix(1, 2)
			self.assertMatrixEqual(A, B)

	def test_fail_different_col_sizes(self):
		with self.assertRaises(AssertionError):
			A = self.generate_random_matrix(1, 2)
			B = self.generate_random_matrix(1, 1)
			self.assertMatrixEqual(A, B)

	def test_fail_different_values(self):
		with self.assertRaises(AssertionError):
			A = Matrix([[1, 1], [0, 1]])
			B = Matrix([[1, 1], [1, 1]])
			self.assertMatrixEqual(A, B)

	def test_str(self):
		m = self.generate_random_matrix(2, 2)
		self.assertIn('\n', m.__repr__())

	def test_setitem_encapsulates_as_vector(self):
		m = self.generate_random_matrix(2, 2)
		m[0] = [2, 1]
		self.assertIs(type(m[0]), Vector)

	def test_append_encapsulates_as_vector(self):
		m = self.generate_random_matrix(2, 2)
		m.append([2, 1])
		self.assertIs(type(m[2]), Vector)

	def test_transposition(self):
		m = self.generate_random_matrix(4, 3)
		self.assertMatrixEqual(m, m.transpose().transpose())

	def test_matmul(self):
		A = Matrix([[2, 3], [-1, 4]])
		B = Matrix([[1, 2, 3], [4, 5, 6]])
		self.assertMatrixEqual(A @ B, [[14, 19, 24], [15, 18, 21]])
		self.assertMatrixEqual(B.transpose() @ A, [[-2, 19], [-1, 26], [ 0, 33]])

	def test_rmatmul(self):
		A = [[2, 3], [-1, 4]]
		B = Matrix([[1, 2, 3], [4, 5, 6]])
		self.assertMatrixEqual(A @ B, [[14, 19, 24], [15, 18, 21]])

	def test_deep_copy(self):
		A = Matrix([[2, 1], [-1, 5]])
		B = A.copy()
		B[0][0] = 3
		self.assertEqual(A[0][0], 2)
		self.assertNotEqual(B[0][0], A[0][0])


if __name__ == '__main__':
	main()
