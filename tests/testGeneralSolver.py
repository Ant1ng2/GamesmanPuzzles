import pytest

from puzzlesolver.puzzles import GraphPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *
"""
def testSimple():
    forward = GraphPuzzle(name="f")
    bi = GraphPuzzle(name="b")
    undo = GraphPuzzle(name="u")
    sol = GraphPuzzle(name="s", 
        forwardChildren=[forward], 
        biChildren=[bi], 
        backwardChildren=[undo], 
        primitive=PuzzleValue.SOLVABLE)

    solver = GeneralSolver()
    solver.solve(sol)
    assert solver.getRemoteness(undo) == 1
    assert solver.getRemoteness(sol) == 0
    assert solver.getRemoteness(bi) == 1
    assert solver.getRemoteness(forward) == PuzzleValue.UNSOLVABLE
"""