"""
This class provides a TUI for interaction with Solvers and Puzzles
"""
from .util import *

#Default to print Puzzle Info
def printInfo(turn, primitive, solver, solve, remoteness, puzzle):
    print("Turn:          ", turn), 
    print("Primitive:     ", primitive)
    if solver:
        print("Solver:        ", solve)
        print("Remoteness:    ", remoteness)
    print(str(puzzle))
    return turn + 1

class PuzzlePlayer:

    def __init__(self, puzzle, solver=None, auto=False, printPuzzleInfo=printInfo):
        self.base = puzzle
        self.puzzle = puzzle
        self.solver = solver
        self.auto = auto
        self.printInfo = printPuzzleInfo
        if solver:
            self.solver.solve(self.puzzle)

    # Starts the PuzzlePlayer
    def play(self):
        self.puzzle = self.base
        self.turn = 0
        while self.puzzle.primitive() == PuzzleValue.UNDECIDED:
            self.turn = self.printInfo(self.turn, self.puzzle.primitive(), self.solver, self.solver.solve(self.puzzle), self.solver.getRemoteness(self.puzzle), self.puzzle)
            self.printTurn()
        self.turn = self.printInfo(self.turn, self.puzzle.primitive(), self.solver, self.solver.solve(self.puzzle), self.solver.getRemoteness(self.puzzle), self.puzzle)
        print("Game Over")

    # Prompts for input and moves
    def printTurn(self):
        if self.auto: 
            move = self.generateBestMove()
            self.puzzle = self.puzzle.doMove(move)
        else:
            moves = self.puzzle.generateMoves(movetype="legal")
            print("Possible Moves:")
            for count, m in enumerate(moves):
                print(str(count) + " -> " + str(m))
            print("Enter Piece: ")
            index = int(input())
            if index >= len(moves):
                print("Not a valid move, try again")
            else:
                self.puzzle = self.puzzle.doMove(moves[index])
        print("----------------------------")

    # Generates best move from the solver
    def generateBestMove(self):
        remotes = {
            self.solver.getRemoteness(self.puzzle.doMove(move)) : move 
            for move in self.puzzle.generateMoves(movetype="legal")
        }
        return remotes[min(remotes.keys())]

