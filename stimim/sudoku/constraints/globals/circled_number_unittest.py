#!/usr/bin/env python

import unittest

from stimim.sudoku.basic import board
from stimim.sudoku.basic import position
from stimim.sudoku.constraints.globals import circled_number


class CircledNumberConstraintUnittest(unittest.TestCase):
  def setUp(self):
    pos = [
      (0, 0),
      (1, 3), (1, 4), (1, 5),
      (3, 0), (3, 1),
      (6, 0), (6, 1), (6, 2),
    ]
    self.constraint = circled_number.CircledNumberConstraint(
      {position.coord_to_index(row, col) for row, col in pos},
      {2, 3, 4}
    )

  def _set_digit(self, b, c, coord: position.Coord, digit: int):
    b = b.set_digit(coord, digit)
    return c.eliminate_by_given_digit(b, coord, digit)

  def test_eliminate_ok(self):
    b = board.SudokuBoard()
    c = self.constraint

    steps = [
      ((0, 0), 4),
      ((1, 3), 4),
      ((1, 4), 3),
      ((1, 5), 2),
      ((3, 0), 3),
      ((3, 1), 4),
      ((6, 0), 2),
      ((6, 1), 3),
      ((6, 2), 4),
    ]
    for ((row, col), digit) in steps:
      b, c = self._set_digit(b, c, position.Coord(row, col), digit)

  def test_eliminate_too_many_in_circle_numbers(self):
    b = board.SudokuBoard()
    c = self.constraint

    steps = [
      ((0, 0), 2),
      ((1, 3), 4),
      ((1, 4), 3),
      ((1, 5), 2),
      ((3, 0), 3),
      ((3, 1), 4),  # ok
      ((6, 0), 2),  # fail
    ]
    for ((row, col), digit) in steps[:-1]:
      b, c = self._set_digit(b, c, position.Coord(row, col), digit)

    with self.assertRaises(board.NotInCandidate):
      ((row, col), digit) = steps[-1]
      b, c = self._set_digit(b, c, position.Coord(row, col), digit)

  def test_eliminate_too_many_out_circle_numbers(self):
    b = board.SudokuBoard()
    c = self.constraint

    steps = [
      ((0, 3), 4),
      ((1, 6), 4),
      ((2, 0), 4),
      ((3, 2), 4),
      ((4, 5), 4),  # ok
      ((5, 7), 4),  # fail
    ]
    for ((row, col), digit) in steps[:-1]:
      b, c = self._set_digit(b, c, position.Coord(row, col), digit)

    with self.assertRaises(board.NotInCandidate):
      ((row, col), digit) = steps[-1]
      b, c = self._set_digit(b, c, position.Coord(row, col), digit)


if __name__ == '__main__':
  unittest.main()
