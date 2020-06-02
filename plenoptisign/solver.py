#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2019 Christopher Hahne <inbox@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import numpy as np


def solve_sle(A, b):
    """

    This function is an algebraic function solver for a system of linear equations of the general form :math:`Ax=b`.
    In this application, its purpose is to solve for intersecting ray functions.

    :param A: :math:`n \\times m` matrix
    :param b: :math:`n \\times 1` column vector
    :param x: :math:`m \\times 1` column vector
    :type A: :class:`~numpy:numpy.ndarray`
    :type b: :class:`~numpy:numpy.ndarray`
    :type x: :class:`~numpy:numpy.ndarray`

    :return: **x**

    """

    if is_square(A):
        A_inv = np.linalg.inv(A)
    else:
        A_inv = np.linalg.pinv(A)

    return np.dot(A_inv, b)


def is_square(A):
    """ check if matrix is square """

    return all(len(row) == len(A) for row in A)
