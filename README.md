# refactored-pancake
Several miscellaneous tools for dealing with vectors, matrices and linear algebra.

## linalg module
This module provides the basic tools to work with linear algebra.

### Vector class
This class behaves a lot like python's built-in list. However, it behaves differently when it comes to operands; it has been refactored into a more math-friendly array that mimics a vector behaviour. Here are a few of the differences:

```python
>>> l = [1,2,3]	# a python list
>>> l + l
[1, 2, 3, 1, 2, 3]	# python concatenates lists when using the '+' sign.

>>> v = Vector([1, 2, 3])	# linalg Vector
>>> v + v
[2, 4, 6]	# linalg will sum each element from the vector instead of concatenating.

# You can still extend a vector like you would do with a python list:
>>> v.extend(v)
>>> print(v)
[1, 2, 3, 1, 2, 3]

# You can also do scalar multiplication:
>>> 2 * v
[2, 4, 6]

# For convenience, you can multiply 2 vectors:
>>> v * v
[1, 4, 9]

# But you can also use dot product:
>>> v @ v
14

# You can also use vectors to work with a sequence of booleans in a similar way
>>> b = Vector([True, False, True])
>>> b & [False, True, True]
[False, False, True]

# And you can compare each individual element easily:
>>> v < 2
[True, False False]
```

Every method from a python list is also avaiable inside a Vector, because it inherits from a UserList.
```python
>>> v = Vector()
>>> v.append(2)
>>> v.extend([0, -1, 5])
>>> print(v)
[2, 0, -1, 5]

>>> v.pop(1)
0
>>> print(v)
[2, -1, 5]
```
