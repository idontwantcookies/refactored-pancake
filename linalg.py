from typing import Callable, Any, Iterable
from collections import UserList

class Vector(UserList):
	'''
	Extends python's internal type list() in order to make it behave as you 
	would expect from a vector.

	>>> a = Vector([1,2,3])
	>>> a + a
	[2, 4, 6]

	>>> 10 * a
	[10, 20, 30]

	Dot product is supported through matmul:
	>>> a @ a 	# 1*1 + 2*2 + 3*3
	11

	Multiplication is supported for convenience:
	>>> a * a
	[1, 4, 9]

	Every operation supported by lists is also supported by class Vector.

	Vector WILL override another class' behaviour if it is on the right-side
	of an operand: Like so:
	>>> [1, 2, 3] + a
	[2, 4, 6]
	>>> a + [1, 2, 3]
	[2, 4, 6]

	Using different-sized vectors WILL clip the remaining elements without 
	warning, following python's default zip() behaviour:
	>>> a + [1,2,3,4]
	[2, 4, 6]
	'''

	def apply(self, op:Callable[[Any], Any]):
		'''
		Applies a uniary operation through all the vector and returns a copy of
		it with transformed elements.

		Example:
		>>> a = Vector([2, 1])
		>>> a.apply(lambda x: x**2)
		[4, 1]
		'''

		return Vector([op(x) for x in self])

	def apply_bin(self, other:Any, op:Callable[[Any, Any], Any]):
		'''
		Applies op() into each element of self and other, using the zip() method
		to concatenate them. That means	that the exceeding elements from either
		will be clipped without warning.

		Example:
		>>> a = Vector([2, 2])
		>>> b = Vector([3, 4, 1])
		>>> a.apply(b, op=lambda x, y: x + y)	# sums each element of a and b
		[5, 6]	# b[2] was truncated
		'''

		try:
			return self.__class__([op(x, y) for x, y in zip(self, other)])
		except TypeError:
			return self.__class__([op(x, other) for x in self])

	def __add__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x + y)

	def __radd__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y + x)

	def __neg__(self):
		return self.apply(lambda x: -x)

	def __sub__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x - y)

	def __rsub__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y - x)

	def __mul__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x * y)

	def __rmul__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y * x)

	def __matmul__(self, other:Iterable[Any]):
		return sum(self * other)

	def __rmatmul__(self, other:Iterable[Any]):
		return sum(other * self)

	def __truediv__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x / y)

	def __rtruediv__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y / x)

	def __floordiv__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x // y)

	def __rfloordiv__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y // x)

	def __mod__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x % y)

	def __rmod__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y % x)

	def __divmod__(self, other:Iterable[Any]):
		return self // other, self % other

	def __rdivmod__(self, other:Iterable[Any]):
		return other // self, other % self

	def __pow__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x**y)

	def __rpow__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y**x)

	def __lshift__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x << y)

	def __rlshift__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y << x)

	def __rshift__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x >> y)

	def __rrshift__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y >> x)

	def __and__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x & y)

	def __rand__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y & x)

	def __xor__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x ^ y)

	def __rxor__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y ^ x)

	def __or__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x | y)

	def __ror__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: y | x)

	def __eq__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x == y)

	def __lt__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x < y)

	def __le__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x <= y)

	def __gt__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x > y)

	def __ge__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x >= y)

	def __ne__(self, other:Iterable[Any]):
		return self.apply_bin(other, lambda x, y: x != y)

	def as_bool(self):
		return self.apply(bool)


class Matrix(Vector):
	def __init__(self, data:Iterable[Iterable[Any]]=None):
		m = Vector()
		if data is not None:
			for row in data:
				m.append(Vector(row))
		super().__init__(m)

	def append(self, obj, /):
		super().append(Vector(obj))

	def __setitem__(self, key, value, /):
		super().__setitem__(key, Vector(value))

	def __str__(self):
		# Similar to list's __str__, but adds newline for each row
		return '[' + '\n ' .join(str(row) for row in self) + ']'

	def __repr__(self):
		return self.__str__()

	def col(self, col_number:int) -> Vector:
		'''
		Returns a copy of a column as a Vector.

		----------
		Parameters
		col_number: int
			Number of the column being read
		----------
		Returns
		out: Vector
			Column as a vector (1d)
		'''

		out = Vector()
		for row in self:
			out.append(row[col_number])
		return out

	def transpose(self) -> 'Matrix':
		'''
		Returns a copy of this matrix, but swapping rows for columns.

		----------
		Returns
		out: Matrix
			Transposed matrix
		'''
		out = Matrix()
		i = 0
		while True:
			try:
				out.append(self.col(i))
				i += 1
			except IndexError:
				break
		return out
