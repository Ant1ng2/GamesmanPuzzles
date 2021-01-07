from .solver import Solver
from ..util import PuzzleValue, PuzzleException
import queue as q
import progressbar

class GeneralSolver(Solver):

    def __init__(self, puzzle):
        self.remoteness = {}
        self.puzzle = puzzle
    
    def getRemoteness(self, puzzle):
        """Returns remoteness of puzzle. Automatically solves if memory isn't set"""
        if not self.remoteness: print("Warning: No memory found. Please make sure that `solve` was called.")
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return PuzzleValue.UNSOLVABLE

    def solve(self, verbose=False):
        """Traverse the entire puzzle tree and classifies all the 
        positions with values and remoteness
        """
        queue = q.Queue()
        solutions = self.puzzle.generateSolutions()
        if len(list(solutions)) == 0:
            # CSP - the position generated by the __init__ method is starting position
            self.cspGenerateSolutions(queue, verbose)
        else:
            # Not a CSP - use generateSolutions()
            for solution in solutions: 
                # Check if all the solutions are SOLVABLE
                assert solution.primitive() == PuzzleValue.SOLVABLE, "`generateSolutions` contains an UNSOLVABLE position"
                self.remoteness[hash(solution)] = 0
                queue.put(solution)
                
        # Progressbar
        if verbose: 
            print('Solving: {}{}'.format(self.puzzle.name, self.puzzle.variant))
            bar = progressbar.ProgressBar()
            bar.max_value = self.puzzle.numPositions

        # BFS for remoteness classification                        
        while not queue.empty():
            if verbose: bar.update(len(self.remoteness))
            puzzle = queue.get()
            for move in puzzle.generateMoves('undo'):
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in self.remoteness:
                    assert nextPuzzle.primitive() != PuzzleValue.SOLVABLE, """
                        Found a state where primitive was SOLVABLE while traversing Puzzle tree
                    """
                    self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                    queue.put(nextPuzzle)
        if verbose: bar.finish()
        
    def cspGenerateSolutions(self, queue, verbose=False):
        """
        Traverse the puzzle tree, starting from the position returned from __init__,
        placing primitive positions found in queue.
        """
        # Progressbar
        if verbose:
            print("Finding primitive positions: {}{}".format(self.puzzle.name, self.puzzle.variant))
            bar = progressbar.ProgressBar()
            bar.max_value = self.puzzle.numPositions
            
        queue_2, found = q.Queue(), set()
        queue_2.put(self.puzzle)
        found.add(hash(self.puzzle))
        
        # BFS search for primitive positions
        # TODO (maybe not?): Make this only require one search
        i = 1
        while not queue_2.empty():
            if verbose: bar.update(i)
            puzzle = queue_2.get()
            if puzzle.primitive() == PuzzleValue.SOLVABLE:
                self.remoteness[hash(puzzle)] = 0
                queue.put(puzzle)
            for move in puzzle.generateMoves('legal'):
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in found:
                    found.add(hash(nextPuzzle))
                    queue_2.put(nextPuzzle)
            i += 1
        if verbose: bar.finish()
