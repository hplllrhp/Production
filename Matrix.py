# -*- coding: utf-8 -*-

"""
Provides functions that satisfy the operations with matrices of the linear algebra.

author: MIT License, Copyright (c) 2017 Sergio H.
version: 1.0
"""

def solve(a, b):
    """Solve a equation system by the inverse matrix method.

    Args:
        a ([[]]): A matrix.
        b ([[]]): B matrix.

    Returns:
        [[]]: the solution
    """
    if len(b[0]) == 1:
        return multiply(get_inverse_matrix(a), b)

def multiply(a, b):
    """Multiplying the matrix A and B.

    Args:
        a ([[]]): A matrix.
        b ([[]]): B matrix.

    Returns:
        [[]]: the result of multiply A and B.

    Raises:
        ValueError
    """
    if len(a[0]) == len(b):
        m = len(a)
        n = len(a[0])
        p = len(b[0])
        product = create_matrix(m, p)
        for i in range(0, m):
            for j in range(0, p):
                for k in range(0, n):
                    product[i][j] += (a[i][k]*b[k][j])
        return product
    else:
        raise ValueError('The number of columns of A must be equal at number of rows of B.')

def get_inverse_matrix(matrix):
    """Compute the inverse matrix of a matrix.

    Args:
        matrix ([[]]): the source  matrix.

    Returns:
        [[]]: the inverse matrix of the source matrix.

    Raises:
        ValueError
    """
    determinant = get_determinant(matrix)
    if determinant != 0:
        n = len(matrix)
        inverse_matrix = create_matrix(n, n)
        cofactors_matrix = get_cofactors_matrix(matrix)
        transposed_matrix = get_transposed_matrix(cofactors_matrix)
        for i in range(0, n):
            for j in range(0, n):
                inverse_matrix[i][j] = float(transposed_matrix[i][j]/determinant)
        return inverse_matrix
    else:
        raise ValueError('The determinant of the source matrix is zero.')

def get_transposed_matrix(matrix):
    """Compute the transposed matrix of a matrix.

    Args:
        matrix ([[]]): the source matrix.

    Returns:
        [[]]: the transposed matrix of the source matrix.
    """
    n = len(matrix)
    transposed_matrix = create_matrix(n, n)
    for i in range(0, n):
        for j in range(0, n):
            transposed_matrix[i][j] = matrix[j][i]
    return transposed_matrix

def get_cofactors_matrix(matrix):
    """Compute the cofactors matrix of a matrix.

    Args:
        matrix ([[]]): the source matrix.

    Returns:
        [[]]: the cofactors matrix of the source matrix.

    Raises:
        ValueError
    """
    n = len(matrix)
    cofactors_matrix = create_matrix(n, n)
    for i in range(0, n):
        for j in range(0, n):
            cofactors_matrix[i][j] = get_cofactor(i, j, matrix)
    return cofactors_matrix

def get_determinant(matrix):
    """Compute the determinant of a matrix.

    Args:
        matrix ([[]]): the source matrix.

    Returns:
        float: the determinant of the source matrix.

    Raises:
        ValueError
    """
    if len(matrix) != len(matrix[0]):
        raise ValueError('The matrix must be of nxn order.')

    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return float((matrix[0][0]*matrix[1][1])-(matrix[1][0]*matrix[0][1]))
    else:
        i = 0
        determinant = float(0)
        for j in range(0, len(matrix[0])):
            determinant += (matrix[i][j]*get_cofactor(i, j, matrix))
        return determinant

def get_cofactor(i, j, matrix):
    """Compute the cofactor of a matrix element.

    Args:
        i (int): row index.
        j (int): column index.
        matrix ([[]]): the source matrix.

    Returns:
        float: the cofactor of the specified element.

    Raises:
        IndexError
        ValueError
    """
    return ((-1)**(i+j))*get_less(i, j, matrix)

def get_less(i, j, matrix):
    """Compute the less of an element of a matrix.

    Args:
        i (int): row index.
        j (int): column index.
        matrix ([[]]): the source matrix.

    Returns:
        float: the less of the specified element.

    Raises:
        IndexError
        ValueError
    """
    return get_determinant(get_submatrix(i, j, matrix))

def get_submatrix(row_index, column_index, matrix):
    """Removes a row and a column of a matrix.

    Args:
        row_index (int): the row.
        column_index (int): the column.
        matrix ([[]]): the source matrix.

    Returns:
        [[]]: the matrix without the specified row and column.

    Raises:
        IndexError
    """
    return remove_column(column_index, remove_row(row_index, matrix))

def remove_column(column_index, matrix):
    """Removes a column of a matrix.

    Args:
        column_index (int): the column.
        matrix ([[]]): the source matrix.

    Returns:
        [[]]: the matrix without the specified column.

    Raises:
        IndexError
    """
    n = (len(matrix[0])-1)    
    if n >= column_index:
        m = len(matrix)
        submatrix = create_matrix(m, n)
        for i in range(0, m):
            column_counter = 0
            for j in range(0, len(matrix[0])):
                if j != column_index:
                    submatrix[i][column_counter] = matrix[i][j]
                    column_counter += 1
        return submatrix
    else:
        raise IndexError('column_index out of range.')

def remove_row(row_index, matrix):
    """Removes a row of a matrix.

    Args:
        row_index (int): the row.
        matrix ([[]]): the source matrix.

    Returns:
        [[]]: the matrix without the specified row.

    Raises:
        IndexError
    """
    m = (len(matrix)-1)
    if m >= row_index:
        n = len(matrix[0])
        submatrix = create_matrix(m, n)
        row_counter = 0
        for i in range(0, len(matrix)):
            if i != row_index:
                for j in range(0, n):
                    submatrix[row_counter][j] = matrix[i][j]
                row_counter += 1
        return submatrix
    else:
        raise IndexError('row_index out the range.')

def create_matrix(rows, columns):
    """Builds new matrix.

    Args:
        rows (int): number of rows.
        columns (int): number of columns.

    Returns:
        [[]]: matrix that containing data with float type.
    """
    matrix = []
    for i in range(rows):
        matrix.append([float(0)]*columns)
    return matrix

def main():
    pass

if __name__ == '__main__':
    main()