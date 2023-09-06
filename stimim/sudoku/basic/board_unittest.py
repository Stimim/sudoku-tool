#!/usr/bin/env python
import unittest

from stimim.sudoku.basic import board
from stimim.sudoku.basic import constants
from stimim.sudoku.basic import position


class SudokuBoardTest(unittest.TestCase):
  def setUp(self):
    self.board = board.SudokuBoard()

  def test_same_number_in_a_row(self):
    digit = 2
    b = self.board.set_digit(position.Coord(0, 0), digit)

    for row, col in [(0, 8), (8, 0), (1, 1)]:
      with self.assertRaises(board.NotInCandidate):
        b.set_digit(position.Coord(row, col), digit)

  def test_copy_on_write(self):
    digit = 2
    new_board = self.board.set_digit(position.Coord(0, 0), digit)
    self.board.set_digit(position.Coord(0, 8), digit)  # this is okay

    self.assertEqual(new_board.cells[0].digit, digit)

  def test_basic_elimination(self):
    digit = 2
    for row, col in [(0, 0), (3, 4), (7, 5)]:
      row = 0
      col = 0
      coord = position.Coord(row, col)
      b = self.board.set_digit(coord, digit)

      for i in range(constants.BOARD_SIZE):
        index = position.coord_to_index(i, col)
        if index == coord.to_index():
          continue
        self.assertNotIn(digit, b.cells[index].candidates)

      for j in range(constants.BOARD_SIZE):
        index = position.coord_to_index(row, j)
        if index == coord.to_index():
          continue
        self.assertNotIn(digit, b.cells[index].candidates)

      base_row = coord.get_box_row_base()
      base_col = coord.get_box_col_base()
      for i in range(constants.BOX_SIZE):
        for j in range(constants.BOX_SIZE):
          index = position.coord_to_index(base_row + i, base_col + j)
          if index == coord.to_index():
            continue
          self.assertNotIn(digit, b.cells[index].candidates)


if __name__ == '__main__':
  unittest.main()
