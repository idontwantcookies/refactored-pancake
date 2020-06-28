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

	def assert_vector_equal(self, first, second):
		if len(first) != len(second):
			self.fail(f'{first} and {second} have different sizes.')
		for x, y in zip(first, second):
			if x != y:
				self.fail(f'{first} != {second}')

	def test_sum_2_vectors(self):
		self.assert_vector_equal(self.v1 + self.v2, [4, 6])

	def test_sum_vector_and_number(self):
		self.assert_vector_equal(self.v1 + 1, [2, 3])

	def test_negative(self):
		self.assert_vector_equal(-self.v1, [-1, -2])

	def test_subtract_2_vectors(self):
		self.assert_vector_equal(self.v1 - self.v2, [-2, -2])

	def test_subtract_vector_and_number(self):
		self.assert_vector_equal(self.v1 - 1, [0, 1])

	def test_multiply_2_vectors(self):
		self.assert_vector_equal(self.v1 * self.v2, [3, 8])

	def test_multiply_vector_and_number(self):
		self.assert_vector_equal(self.v1 * 2, [2, 4])

	def test_matmul_vector_and_vector(self):
		self.assertEqual(self.v1 @ self.v2, 11)

	def test_divide_2_vectors(self):
		self.assert_vector_equal(self.v2 / self.v1, [3, 2])

	def test_divide_vector_and_number(self):
		self.assert_vector_equal(self.v2 / 2, [1.5, 2])

	def test_power_2_vectors(self):
		self.assert_vector_equal(self.v1 ** self.v2, [1, 16])

	def test_power_vector_to_a_number(self):
		self.assert_vector_equal(self.v1 ** 2, [1, 4])

	def test_floor_division_2_vectors(self):
		self.assert_vector_equal(self.v2 // self.v1, [3, 2])

	def test_floor_division_vector_and_number(self):
		self.assert_vector_equal(self.v2 // 2, [1, 2])

	def test_mod_2_vectors(self):
		self.assert_vector_equal(self.v2 % self.v1, [0, 0])

	def test_mod_vector_and_number(self):
		self.assert_vector_equal(self.v2 % 2, [1, 0])

	def test_divmod_2_vectors(self):
		q, r = divmod(self.v2, self.v1)
		self.assert_vector_equal(q, [3, 2])
		self.assert_vector_equal(r, [0, 0])

	def test_divmod_vector_and_number(self):
		q, r = divmod(self.v2, 2)
		self.assert_vector_equal(q, [1, 2])
		self.assert_vector_equal(r, [1, 0])

	def test_lshift_2_vectors(self):
		self.assert_vector_equal(self.v1 << self.v2, [8, 32])

	def test_lshift_vector_and_number(self):
		self.assert_vector_equal(self.v1 << 2, [4, 8])

	def test_rshift_2_vectors(self):
		self.assert_vector_equal(self.v2 >> self.v1, [1, 1])

	def test_rshift_vector_and_number(self):
		self.assert_vector_equal(self.v2 >> 1, [1, 2])

	def test_and_2_vectors(self):
		self.assert_vector_equal(self.b1 & self.b2, [True, False, False, False])

	def test_or_2_vectors(self):
		self.assert_vector_equal(self.b1 | self.b2, [True, True, True, False])

	def test_xor_2_vectors(self):
		self.assert_vector_equal(self.b1 ^ self.b2, [False, True, True, False])

	def test_different_sizes_not_equal(self):
		with self.assertRaises(AssertionError):
			self.assert_vector_equal([1, 2, 3], [1, 2])

	def test_different_vectors_not_equal(self):
		with self.assertRaises(AssertionError):
			self.assert_vector_equal(self.v1, self.v2)

	def test_eq(self):
		self.assert_vector_equal(self.v1 == self.v1, [True, True])

	def test_lt(self):
		self.assert_vector_equal(self.v1 < self.v2, [True, True])

	def test_le(self):
		self.assert_vector_equal(self.v1 <= [1, 1], [True, False])

	def test_gt(self):
		self.assert_vector_equal(self.v1 > [1, 1], [False, True])

	def test_ge(self):
		self.assert_vector_equal(self.v1 >= [2, 2], [False, True])

	def test_ne(self):
		self.assert_vector_equal(self.v1 != [1, 1], [False, True])

	def test_rmethods(self):
		# guarantees that radd does the same as add (and all other r-magic methods)
		for method in ('add', 'sub', 'mul', 'matmul', 'truediv', 'floordiv', 'mod', 'divmod', 'pow', 'lshift', 'rshift', 'and', 'xor', 'or'):
			left = getattr(self.v1, f'__{method}__')
			right = getattr(self.v2, f'__r{method}__')
			self.assertEqual(left(self.v2), right(self.v1))

	def test_as_bool(self):
		self.assert_vector_equal(self.v3.as_bool(), [False, True, True, True, True, False])


class MatrixTestCase(TestCase):
	def generate_random_matrix(self, m:int, n:int):
		out = Matrix()
		for i in range(m):
			row = Vector()
			for j in range(n):
				row.append(randint(-50, 50))
			out.append(row)
		return out

	def assert_matrix_equal(self, first, second):
		if len(first) != len(second):
			self.fail(f'{first} and {second} have different sizes.')
		i = 0
		for x, y in zip(first, second):
			if len(x) != len(y):
				self.fail(f'Mismatched sizes on rows {i}: {x} != {y}')
			if any(x != y):
				self.fail(f'Different rows on index {i}: {x} != {y}')
			i += 1


	def test_transposition(self):
		m = self.generate_random_matrix(4, 3)
		self.assert_matrix_equal(m, m.transpose().transpose())

if __name__ == '__main__':
	main()
