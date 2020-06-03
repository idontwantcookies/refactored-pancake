from collections import UserList

class Vector(UserList):
	def _apply_op(self, other, op):
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
		return self._apply_op(other, lambda x, y: x / y)

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
		return self._apply_od(other, lambda x, y: x or y)
