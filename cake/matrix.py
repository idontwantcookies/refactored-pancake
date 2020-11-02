from typing import Any, Iterable

from .vector import Vector


class Matrix(Vector):
    def __init__(self, data: Iterable[Iterable[Any]] = None):
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
        return "[" + "\n ".join(str(row) for row in self) + "]"

    def __repr__(self):
        return self.__str__()

    def __matmul__(self, other: Iterable[Iterable[Any]]):
        out = Matrix()
        other = Matrix(other).transpose()
        for row in self:
            new_row = Vector()
            for col in other:
                new_row.append(row @ col)
            out.append(new_row)
        return out

    def __rmatmul__(self, other: Iterable[Iterable[Any]]):
        return Matrix(other).__matmul__(self)

    def col(self, col_number: int) -> Vector:
        """
        Returns a copy of a column as a Vector.

        ----------
        Parameters
        col_number: int
            Number of the column being read
        ----------
        Returns
        out: Vector
            Column as a vector (1d)
        """

        out = Vector()
        for row in self:
            out.append(row[col_number])
        return out

    def copy(self):
        """
        Returns a deep copy of a matrix.
        """

        out = Matrix()
        for row in self:
            out.append(row.copy())
        return out

    def transpose(self) -> "Matrix":
        """
        Returns a copy of this matrix, but swapping rows for columns.

        ----------
        Returns
        out: Matrix
            Transposed matrix
        """
        out = Matrix()
        i = 0
        while True:
            try:
                out.append(self.col(i))
                i += 1
            except IndexError:
                break
        return out
