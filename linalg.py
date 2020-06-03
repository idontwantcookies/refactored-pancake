from typing import Callable, Any
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


	def _apply_op(self, other:Any, op:Callable[[Any, Any], Any]):
		'''
		For internal use only. This method will apply op() into each element of
		self and other, using the zip() method to concatenate them. That means
		that the exceeding elements from either will be clipped without 
		warning.
		'''

		try:
			return Vector([op(x, y) for x, y in zip(self, other)])
		except TypeError:
			return Vector([op(x, other) for x in self])

	def __add__(self, other):
		return self._apply_op(other, lambda x, y: x + y)

	def __neg__(self):
		return self._apply_op(None, lambda x, y: -x)

	def __sub__(self, other):
		return self._apply_op(other, lambda x, y: x - y)

	def __mul__(self, other):
		return self._apply_op(other, lambda x, y: x * y)

	def __matmul__(self, other):
		return sum(self * other)

	def __truediv__(self, other):
		return self._apply_op(other, lambda x, y: x / y)

	def __floordiv__(self, other):
		return self._apply_op(other, lambda x, y: x // y)

	def __mod__(self, other):
		return self._apply_op(other, lambda x, y: x % y)

	def __divmod__(self, other):
		return self // other, self % other

	def __pow__(self, other):
		return self._apply_op(other, lambda x, y: x**y)

	def __lshift__(self, other):
		return self._apply_op(other, lambda x, y: x << y)

	def __rshift__(self, other):
		return self._apply_op(other, lambda x, y: x >> y)

	def __and__(self, other):
		return self._apply_op(other, lambda x, y: x and y)

	def __xor__(self, other):
		return self._apply_op(other, lambda x, y: (x and not y) or (not x and y))

	def __or__(self, other):
		return self._apply_op(other, lambda x, y: x or y)
