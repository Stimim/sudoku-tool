load("@rules_python//python:defs.bzl", "py_binary")

py_library(
  name = "basic-lib",
  srcs = [
    "board.py",
    "constants.py",
    "position.py",
  ],
  visibility = ['//visibility:public']
)

py_test(
  name = "board_unittest",
  srcs = [ "board_unittest.py" ],
  deps = [
    "basic-lib"
  ]
)

py_test(
  name = "position_unittest",
  srcs = [ "position_unittest.py" ],
  deps = [
    "basic-lib"
  ]
)
