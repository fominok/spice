import copy


def print_matrix(matrix):
    print('=' * 20)
    for x in matrix:
        print(x)
    print('=' * 20)


def minor(matrix, i, j):

    """Pls start with 0"""
    if len(matrix) != len(matrix[0]):
        raise Exception('Non square matrix')

    cop = copy.deepcopy(matrix)
    for x in cop:
        del x[j]
    del cop[i]

    return cop


def determinant(matrix):
    if len(matrix) != len(matrix[0]):
        raise Exception('Non square matrix')

    res = 0

    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - \
                   matrix[0][1] * matrix[1][0]

    for j in range(len(matrix)):
        res += matrix[0][j] * (-1)**j * determinant(minor(matrix, 0, j))

    return res


def transpose(matrix):
    lnm = len(matrix)
    if lnm != len(matrix[0]):
        raise Exception('Non square matrix')

    cop = [[0 for x in range(lnm)] for x in range(lnm)]
    for i in range(lnm):
        for j in range(lnm):
            cop[i][j] = matrix[j][i]

    return cop


def gaussian_elimintaion(matrix_a, matrix_z) -> []:
    """Find inverse matrix A^-1 and multiply it with Z"""
