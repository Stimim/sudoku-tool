import unittest

from stimim.sudoku.basic import constants
from stimim.sudoku.basic import position


class CoordUnittest(unittest.TestCase):
  def test_coord_to_index(self):
    index = 0
    for row in range(constants.BOARD_SIZE):
      for col in range(constants.BOARD_SIZE):
        coord = position.Coord(row, col)
        self.assertEqual(coord.to_index(), index)
        index += 1


if __name__ == '__main__':
  unittest.main()
