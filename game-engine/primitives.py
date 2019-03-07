from enum import Enum


class Field:
    def __init__(self, dim=3):
        self.dim = dim
        self.grid = [[None for _ in range(self.dim)] for _ in range(self.dim)]

    def _validate_coordinates(self, x, y):
        assert 0 <= x < self.dim
        assert 0 <= y < self.dim

    def _check_horizontal(self, y, label):
        return self.grid[y].count(label) == self.dim

    def _check_vertical(self, x, label):
        return [self.grid[y][x] for y in range(self.dim)].count(label) == self.dim

    def _check_diagonal(self, x, y, label):
        # На гланой диагонали -- x == y
        # На побочной диагонали --

        # TODO: проверка -- лежит ли метка на диагонали
        if (x + y) & 1 == self.dim & 1:
            return False

        on_first_diagonal = [
            self.grid[d][d] for d in range(self.dim)
        ].count(label) == self.dim

        on_second_diagonal = [
                self.grid[y_][x_] for y_, x_ in zip(range(self.dim),
                                                    reversed(range(self.dim)))
        ].count(label) == self.dim

        return on_first_diagonal or on_second_diagonal

    def check(self, x, y, label):
        return self._check_horizontal(y, label) or \
               self._check_vertical(x, label) or \
               self._check_diagonal(x, y, label)

    def check_o(self, x, y):
        return self.check(x, y, Label.O_)

    def check_x(self, x, y):
        return self.check(x, y, Label.X_)

    def mark_as(self, x, y, label):
        self._validate_coordinates(x, y)
        self.grid[x][y] = label

    def mark_as_x(self, x, y):
        self.mark_as(x, y, Label.X_)

    def mark_as_o(self, x, y):
        self.mark_as(x, y, Label.O_)


class Label(Enum):
    O_ = 0
    X_ = 1


if __name__ == '__main__':
    field = Field(3)
    field.mark_as_x(0, 2)
    field.mark_as_x(1, 1)
    field.mark_as_x(2, 0)
    print(field.grid)
    print(field.check_x(0, 0))
