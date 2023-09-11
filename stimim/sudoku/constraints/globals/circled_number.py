import logging

from stimim.sudoku.basic import board
from stimim.sudoku.basic import constants
from stimim.sudoku.basic import position


class CircledNumberConstraintViolation(Exception):
  pass


class CircledNumberConstraint:
  __slots__ = [
    'positions',
    'allowed_digits',
    'in_circle_count',
    'out_circle_count',
  ]

  def __init__(self, positions: set[position.Index], digits: set[int]):
    self.positions = positions
    self.allowed_digits = digits
    if sum(self.allowed_digits) != len(self.positions):
      raise CircledNumberConstraintViolation(
          f'{self.allowed_digits} cannot occupy {len(self.positions)} circles')
    # Digits that are already filled in any of the circled cells.
    self.in_circle_count = {
      digit: 0 for digit in digits
    }
    # Digits that are already filled in any of the non-circled cells.
    self.out_circle_count = {
      digit: 0 for digit in digits
    }

  def initialize(self, b: board.SudokuBoard):
    b = b.copy()

    for index in self.positions:
      for digit in constants.ALL_DIGITS - self.allowed_digits:
        b.cells[index] = b.cells[index].remove_candidate(digit)

    if 9 in self.allowed_digits:
      for index in range(len(b.cells)):
        if index in self.positions:
          continue
        b.cells[index] = b.cells[index].remove_candidate(9)

    return b

  def eliminate_by_given_digit(self, b: board.SudokuBoard,
                               coord: position.Coord, digit: int):
    retval = self.copy()
    if coord.to_index() in self.positions:
      b = retval._eliminate_in_circle_digit(b, digit)
    else:
      b = retval._eliminate_out_circle_digit(b, digit)
    return b, retval

  def _eliminate_in_circle_digit(self, b, digit):
    if digit not in self.allowed_digits:
      raise CircledNumberConstraintViolation(
          f'{digit} cannot appear in the circled cells')
    if self.in_circle_count[digit] == digit:
      # this should not happen, but worth checking
      raise CircledNumberConstraintViolation(
          f'{digit} cannot appear in the circled cells')
    self.in_circle_count[digit] += 1
    if self.in_circle_count[digit] < digit:
      return b

    logging.info('We have found all %d that are in circled cells. '
                 'Removing all %d in other circles', digit, digit)
    cells = [cell for cell in b.cells]
    for index in self.positions:
      if cells[index].digit is None:
        cells[index] = cells[index].remove_candidate(digit)
    return b.__class__(cells)

  def _eliminate_out_circle_digit(self, b, digit):
    if digit not in self.allowed_digits:
      # We don't care.
      return b
    if self.out_circle_count[digit] + digit == constants.BOARD_SIZE:
      # this should not happen, but worth checking
      raise CircledNumberConstraintViolation(
          f'{digit} cannot appear out of the circled cells')

    self.out_circle_count[digit] += 1
    if self.out_circle_count[digit] + digit != constants.BOARD_SIZE:
      return b

    logging.info('We have found all %d that are not in circled cells. '
                 'Removing all %d in other non-circled cells', digit, digit)
    cells = [cell for cell in b.cells]
    for index in range(constants.BOARD_SIZE * constants.BOARD_SIZE):
      if index in self.positions:
        continue
      if cells[index].digit is None:
        cells[index] = cells[index].remove_candidate(digit)
    return b.__class__(cells)

  def copy(self):
    retval = self.__class__(self.positions, self.allowed_digits)
    retval.in_circle_count = {
      k: v for k, v in self.in_circle_count.items()
    }
    retval.out_circle_count = {
      k: v for k, v in self.out_circle_count.items()
    }
    return retval
