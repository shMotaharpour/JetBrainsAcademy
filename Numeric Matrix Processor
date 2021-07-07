class Matrix:
    def __init__(self, in_matrix=''):
        self._determinant = None
        self._inverse = None
        if isinstance(in_matrix, str):
            self.get_matrix(in_matrix)
        else:
            if isinstance(in_matrix, list):
                if all(type(cl) in (int, float) for cl in in_matrix):
                    self._matrix = [in_matrix]
                    self._row, self._cl = 1, len(in_matrix)
                elif all(isinstance(cl, list) for cl in in_matrix):
                    if all(len(cl) == len(in_matrix[0]) for cl in in_matrix):
                        self._matrix = in_matrix
                        self._row, self._cl = len(in_matrix), len(in_matrix[0])
            elif isinstance(in_matrix, (int, float)):
                self._matrix = [[in_matrix]]
                self._row, self._cl = 1, 1
            else:
                raise UserWarning(1, 'Wrong matrix input format')

    def __getitem__(self, item):
        return self._matrix[item]

    def get_matrix(self, name: str):
        while True:
            try:
                self._row, self._cl = map(int, input(f'Enter size of {name} matrix:').split())
                break
            except:
                print('Enter two integer with space')
                continue
        self._matrix = []
        print(f'Enter {name} matrix:')
        for i in range(self._row):
            self._matrix.append(list(map(float, input().split())))

    @property
    def matrix(self):
        return self._matrix

    @property
    def size(self):
        return self._row, self._cl

    @property
    def determinant(self):
        if self._determinant is None:
            if self.size == (1, 1):
                self._determinant = self[0][0]
            else:
                self._try_determinant()
        return self._determinant

    def __str__(self):
        output_string = ''
        for row in self._matrix:
            line = ''
            for cl in row:
                line += f'{cl} '
            output_string += line + '\n'
        return output_string

    def __add__(self, other):
        if self.size != other.size:
            raise UserWarning(0)
        else:
            matrix = self._matrix.copy()
            for i in range(self._row):
                for j in range(self._cl):
                    matrix[i][j] += other._matrix[i][j]
        return Matrix(matrix)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.constant_multiply(other)
        elif isinstance(other, Matrix):
            if other.size == (1, 1):
                return self.constant_multiply(other[0][0])
            elif self.size == (1, 1):
                return other.constant_multiply(self[0][0])
            else:
                return self.matrix_multiply(other)
        else:
            raise UserWarning(0)

    def matrix_multiply(self, other):
        if self._cl == other._row:
            res = []
            for i in range(self._row):
                row = []
                for j in range(other._cl):
                    temp = 0
                    for k in range(self._cl):
                        temp += self.matrix[i][k] * other.matrix[k][j]
                    row.append(temp)
                res.append(row)
            return Matrix(res)

    def constant_multiply(self, cons):
        matrix = self._matrix
        for row in range(self._row):
            for clm in range(self._cl):
                matrix[row][clm] *= cons
        return Matrix(matrix)

    def transpose(self, com='1'):
        trans = []
        if com == '1':  # Main diagonal
            for cl in range(self._cl):
                row_temp = []
                for row in range(self._row):
                    row_temp.append(self.matrix[row][cl])
                trans.append(row_temp)
            return Matrix(trans)
        elif com == '2':  # Side diagonal
            mid_matrix = [row[::-1] for row in self.matrix]
            for cl in range(self._cl):
                row_temp = []
                for row in range(self._row):
                    row_temp.append(mid_matrix[row][cl])
                trans.append(row_temp)
            return Matrix([row[::-1] for row in trans])
        elif com == '3':  # Vertical line
            return Matrix([row[::-1] for row in self.matrix])
        elif com == '4':  # Horizontal line
            return Matrix(self.matrix[::-1])

    @staticmethod
    def _minor(minor_matrix, m, n):
        if len(minor_matrix) == 1:
            return 1
        else:
            dummy_mat = []
            for row in minor_matrix:
                dummy = row.copy()
                del dummy[n]
                dummy_mat.append(dummy)
            del dummy_mat[m]
            return dummy_mat

    @staticmethod
    def _calc_determinant(co_matrix):
        if len(co_matrix) == 1:  # must m == n
            return co_matrix[0][0]
        else:
            det = 0.0
            for row in range(len(co_matrix)):
                det += co_matrix[row][0] * \
                       Matrix._calc_determinant(Matrix._minor(co_matrix, row, 0)) * \
                       (-1) ** float(row + 2)
            return det

    def _try_determinant(self):
        if self._row != self._cl:
            self._determinant = 'Undefined'
        else:
            self._determinant = Matrix._calc_determinant(self.matrix)

    @property
    def inverse(self):
        if self._inverse is None:
            if self.size == (1, 1):
                self._inverse = self[0][0] ** -1 if self[0][0] else 'Undefined'
            else:
                self._try_inverse()
        return self._inverse

    def _try_inverse(self):
        if self.determinant == 0 or isinstance(self.determinant, str):
            self._inverse = 'Undefined'
        else:
            c_mat = self.adjugate_calculate()
            self._inverse = self.determinant ** -1 * c_mat

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other
        else:
            raise UserWarning(0)

    def adjugate_calculate(self):
        dummy_mat = []
        for row in range(self._row):
            dummy = []
            for cl in range(self._cl):
                dummy.append(
                    Matrix._calc_determinant(Matrix._minor(self._matrix, row, cl)) * (-1) ** float(row + cl + 2))
            dummy_mat.append(dummy)
        return Matrix(dummy_mat).transpose()


def print_result(res):
    print('The result is:')
    print(res)


if __name__ == '__main__':
    while True:
        try:
            command = input('1. Add matrices\n2. Multiply matrix by a constant\n' +
                            '3. Multiply matrices\n4. Transpose matrix\n' +
                            '5. Calculate a determinant\n6. Inverse matrix\n' +
                            '0. Exit\nYour choice: ')
            if command == '0':
                break
            if command == '1':
                mat1 = Matrix('first')
                mat2 = Matrix('second')
                print_result(mat1 + mat2)
            elif command == '2':
                mat1 = Matrix('')
                print_result(mat1.constant_multiply(int(input('Enter constant:'))))
            elif command == '3':
                mat1 = Matrix('first')
                mat2 = Matrix('second')
                print_result(mat1 * mat2)
            elif command == '4':
                text = '\n'.join(('1. Main diagonal', '2. Side diagonal',
                                  '3. Vertical line', '4. Horizontal line',
                                  'Your choice:'))
                command = input(text)
                if len(command) == 1 and command in '1234':
                    mat1 = Matrix('')
                    print_result(mat1.transpose(command))
                else:
                    break
            elif command == '5':
                mat1 = Matrix('')
                if isinstance(mat1.determinant, str):
                    raise UserWarning(0)
                else:
                    print_result(mat1.determinant)
                continue
            elif command == '6':
                mat1 = Matrix('')
                if isinstance(mat1.determinant, str) or not mat1.determinant:
                    raise UserWarning(1, "This matrix doesn't have an inverse.")
                else:
                    print_result(mat1.inverse)
                continue
            else:
                continue
        except UserWarning as err:
            if not err.args[0]:
                print('The operation cannot be performed.')
            else:
                print(err.args[1])
            continue
