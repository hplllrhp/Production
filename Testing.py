#*- coding: utf-8 -*-

"""
Testing to matrix module functions.

author: MIT License, Copyright (c) 2017 Sergio H.
version: 1.0
"""

from Matrix import *

def column_input():
    return int(raw_input('Enter the column index: '))

def row_input():
    return int(raw_input('Enter the row index: '))

def order_input():
    order = raw_input('Enter the mxn order of the matrix: ')
    m, n = order.split('x')
    return int(m), int(n)

def matrix_input(m, n):
    matrix = create_matrix(m, n)
    for i in range(0, m):
        for j in range(0, n):
            matrix[i][j] = float(raw_input('Enter item a%i%i: '%(i, j)))
    return matrix

def main():
    m, n = order_input()
    matrix = matrix_input(m, n)

    print ('\nNow select an option:')
    print()
    print( '0)Get submatrix')
    print( '1)Get determinant')
    print( '2)Get cofactors matrix')
    print( '3)Get transposed matrix')
    print( '4)Get inverse matrix')
    print( '5)Solve equation system')

    option = int(raw_input('Option: '))

    if option == 0:
        i = row_input()
        j = column_input()

        print (get_submatrix(i, j, matrix))

    elif option == 1:
        print (get_determinant(matrix))

    elif option == 2:
        print (get_cofactors_matrix(matrix))

    elif  option == 3:
        print (get_transposed_matrix(matrix))

    elif option == 4:
        print (get_inverse_matrix(matrix))

    elif option == 5:
        a = remove_column((len(matrix[0])-1), matrix)
        b = matrix
        while len(b[0]) > 1:
            b = remove_column(0, b)

        print (solve(a, b))

    else:
        print ('Invalid input')

if __name__ == '__main__':
    main()