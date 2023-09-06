load("@rules_python//python:defs.bzl", "py_binary")

py_library(
  name = "global-constraint-lib",
  srcs = [
    "circled_number.py",
  ],
  deps = [
    "//stimim/sudoku/basic:basic-lib"
  ],
  visibility = ['//visibility:public']
)

py_test(
  name = "circled_number_unittest",
  srcs = [ "circled_number_unittest.py" ],
  deps = [
    "global-constraint-lib"
  ]
)
