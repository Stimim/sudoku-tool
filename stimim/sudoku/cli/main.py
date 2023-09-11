#!/usr/bin/env python
import datetime
import logging
import sys

from stimim.sudoku.basic import board
from stimim.sudoku.basic import constants
from stimim.sudoku.basic import position
from stimim.sudoku.constraints.globals import circled_number


class FailureTracker:
  def __init__(self, period = 10000):
    self.fail_count = 0
    self.period = period
    self.start_time = datetime.datetime.now()

  def log_failure(self, kwargs):
    self.fail_count += 1
    if self.fail_count % self.period == 1:
      logging.critical('=== fail %d ===', self.fail_count)
      now = datetime.datetime.now()
      delta = now - self.start_time
      logging.critical('FPS: %f', (self.fail_count / delta.total_seconds()))
      logging.critical('%r', kwargs)


CIRCLE_MARKS = [
  0, 1, 0, 1, 0, 1, 0, 1, 0,
  1, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 1, 0, 1, 0, 1, 0, 1,
  1, 0, 0, 1, 0, 1, 0, 1, 0,
  0, 0, 1, 0, 1, 0, 1, 0, 1,
  1, 0, 0, 1, 0, 1, 0, 1, 0,
  0, 0, 1, 0, 1, 0, 1, 0, 1,
  1, 0, 0, 1, 0, 1, 0, 1, 0,
  0, 0, 1, 0, 1, 0, 1, 0, 1,
]

def init_circle_number_constraint():
  marks = CIRCLE_MARKS
  assert len(marks) == constants.BOARD_SIZE * constants.BOARD_SIZE
  pos = { position.Index(index) for index in range(81) if marks[index] == 1 }
  return circled_number.CircledNumberConstraint(pos, {1, 2, 4, 5, 6, 7, 8})


failure_tracker = FailureTracker()

ANSWER_FILE = '/usr/local/google/home/stimim/personal/sudoku-tool/answer.txt'

class SolutionFoundException(Exception):
  pass

def has_answer(b, i):
  if i == constants.BOARD_SIZE * constants.BOARD_SIZE:
    return True

  index = position.Index(i)
  next_i = i + 1

  if b.cells[index].digit is not None:
    return has_answer(b, next_i)

  for digit in b.cells[index].candidates:
    try:
      coord = index.to_coord()
      new_board = b.set_digit(coord, digit)
      if has_answer(new_board, next_i):
        return True
    except Exception:
      failure_tracker.log_failure(dict(i=i))
  return False


def dfs(b, c, i, dfs_order: list[position.Index]):
  if i == len(dfs_order):
    if has_answer(b, 0):
      b_str = str(b)
      with open(ANSWER_FILE, 'a') as f:
        f.write(b_str + '\n')
        f.write('--------------------' + '\n')
      logging.critical('\n' + b_str)
    return

  index = dfs_order[i]
  next_i = i + 1
  if b.cells[index].digit is not None:
    return dfs(b, c, next_i, dfs_order)

  for digit in b.cells[index].candidates:
    try:
      coord = index.to_coord()
      new_board = b.set_digit(coord, digit)
      new_board, new_constraint = c.eliminate_by_given_digit(new_board, coord, digit)
      dfs(new_board, new_constraint, next_i, dfs_order)
    except Exception:
      failure_tracker.log_failure(dict(i=i))

def main():
  with open(ANSWER_FILE, 'a') as f:
    f.write('starting... \n')
  b = board.SudokuBoard()
  c = init_circle_number_constraint()
  b = c.initialize(b)

  b = b.set_digit(position.Coord(1, 0), 8)
  b = b.set_digit(position.Coord(5, 1), 8)
  # b = b.set_digit(position.Coord(4, 6), 7)

  dfs_order = []
  for i, mark in enumerate(CIRCLE_MARKS):
    if mark == 1:
      dfs_order.append(position.Index(i))
  # for i, mark in enumerate(CIRCLE_MARKS):
    # if mark == 0:
      # dfs_order.append(position.Index(i))
  dfs(b, c, 0, dfs_order)

  print('orz')


if __name__ == '__main__':
  main()
