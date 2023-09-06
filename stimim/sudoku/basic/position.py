from stimim.sudoku.basic import constants


def coord_to_index(row, col):
  return row * constants.BOARD_SIZE + col


class Index(int):
  def to_coord(self):
    row = self // constants.BOARD_SIZE
    col = self % constants.BOARD_SIZE
    return Coord(row, col)


class Coord:
  def __init__(self, row: int, col: int):
    self.row = row
    self.col = col

  def to_index(self):
    return coord_to_index(self.row, self.col)

  def get_box_row_base(self):
    return (self.row // 3) * 3

  def get_box_col_base(self):
    return (self.col // 3) * 3

  def __str__(self):
    return f'({self.row + 1}, {self.col + 1})'
