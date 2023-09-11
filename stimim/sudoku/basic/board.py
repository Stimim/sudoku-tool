import logging

from stimim.sudoku.basic import constants
from stimim.sudoku.basic import position


BOX_SIZE = constants.BOX_SIZE
BOARD_SIZE = constants.BOARD_SIZE

Index = position.Index
Coord = position.Coord


class NoCandidatesLeft(Exception):
  pass


class NotInCandidate(Exception):
  pass


class DigitAlreadySet(Exception):
  pass


class _SudokuCell:
  __slots__ = [
    'candidates', 'digit'
  ]
  def __init__(self, cs: set[int] | None = None, digit: int | None = None):
    if cs is not None:
      self.candidates = cs
    else:
      self.candidates = set(range(1, 10))
    self.digit = digit

  def remove_candidate(self, digit: int):
    cs = self.candidates - {digit}
    if not cs:
      raise NoCandidatesLeft
    return self.__class__(cs, self.digit)

  def set_digit(self, digit: int):
    if self.digit is not None:
      raise DigitAlreadySet

    if digit not in self.candidates:
      raise NotInCandidate(f'{digit} is not my candidate')

    result = self.__class__(self.candidates, digit)
    return result


class SudokuBoard:
  __slots__ = [
    'cells'
  ]

  def __init__(self, cells: list[_SudokuCell] | None = None):
    if cells is not None:
      self.cells = cells
    else:
      self.cells = [_SudokuCell() for _ in range(BOARD_SIZE * BOARD_SIZE)]

  def set_digit(self, coord: Coord, digit: int):
    index = coord.to_index()
    if digit not in self.cells[index].candidates:
      raise NotInCandidate(f'{digit} is not a candidate of {coord}')
    new_board = self.copy()
    new_board.cells[index] = new_board.cells[index].set_digit(digit)
    new_board = new_board.eliminate_by_given_digit(coord, digit)
    return new_board

  def copy(self):
    cells = [cell for cell in self.cells]
    return self.__class__(cells)

  def eliminate_by_given_digit(self, coord: Coord, digit: int):
    result = [cell for cell in self.cells]

    row = coord.row
    col = coord.col

    for i in range(BOARD_SIZE):
      index = position.coord_to_index(i, col)
      if result[index].digit is None:
        result[index] = result[index].remove_candidate(digit)

    for i in range(BOARD_SIZE):
      index = position.coord_to_index(row, i)
      if result[index].digit is None:
        result[index] = result[index].remove_candidate(digit)

    base_row = coord.get_box_row_base()
    base_col = coord.get_box_col_base()
    for i in range(BOX_SIZE):
      for j in range(BOX_SIZE):
        index = position.coord_to_index(base_row + i, base_col + j)
        if result[index].digit is None:
          result[index] = result[index].remove_candidate(digit)
    return self.__class__(result)

  def __str__(self):
    output = ''
    for row in range(constants.BOARD_SIZE):
      for col in range(constants.BOARD_SIZE):
        index = position.coord_to_index(row, col)
        if self.cells[index].digit:
          output += f' {self.cells[index].digit} '
        else:
          output += ' ? '
      output += '\n'
    return output

  def show(self):
    logging.info(str(self))
