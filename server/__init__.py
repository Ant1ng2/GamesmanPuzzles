from .routes import app
from .main import init_data
from puzzlesolver.puzzles import PuzzleManager

# Test your server puzzle
def test_puzzle(puzzle):
    """Helper function to test any puzzle. Sets the PuzzleManager to only hold one Puzzle for testing"""
    from puzzlesolver.puzzles import PuzzleManagerClass
    global PuzzleManager
    puzzleList = {puzzle.id: puzzle}
    PuzzleManager = PuzzleManagerClass(puzzleList)
    init_data()
    app.run()
