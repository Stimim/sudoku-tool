load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
  name = "main",
  srcs = ["main.py"],
  deps = [
    "//stimim/sudoku/basic:basic-lib",
    "//stimim/sudoku/constraints/globals:global-constraint-lib",
  ]
)
