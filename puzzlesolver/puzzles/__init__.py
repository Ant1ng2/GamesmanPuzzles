from ._models import *
from ..solvers import IndexSolver, SqliteSolver
from ..util import PuzzleException

# Put your dependencies here
from .hanoi import Hanoi
from .lightsout import LightsOut
from .pegSolitaire.pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle
from .npuzzle import Npuzzle
from .chairs.chairs import Chairs
from .bishop.bishop import Bishop
from .topspin.topspin import TopSpin
from .hopNdrop.hopNdrop import HopNDrop
from .rubiks.rubiks import Rubiks                

class MetaPuzzle(object):
    def __init__(self, p_cls, **kwargs):
        allowed_keys = {'id', 'auth', 'name', 'desc', 'date', 'variants', 'test_variants'}

        self.p_cls = p_cls
        for k, v in kwargs.items():
            if k in allowed_keys: setattr(p_cls, k, v)
        if 'test_variants' not in kwargs:
            p_cls.test_variants = [list(p_cls.variants)[0]]

# Add your puzzle in the puzzleList
puzzleList = {
    Npuzzle.puzzleid: Npuzzle,
    Hanoi.puzzleid: Hanoi,
    LightsOut.puzzleid: LightsOut,
    Peg.puzzleid: Peg,
    Chairs.puzzleid: Chairs,
    Bishop.puzzleid: Bishop,
    TopSpin.puzzleid: TopSpin,
    HopNDrop.puzzleid: HopNDrop,
    # Rubiks.puzzleid: Rubiks
}

puzzleList = {
    'npuzzle': MetaPuzzle(
        Npuzzle,
        id              = 'npuzzle',
        auth            = 'Arturo Olvera',
        name            = "N x N '15'-puzzle",
        desc            = "Shift pieces to get puzzle in ascending order.",
        date            = "April 20, 2020",
        variants        = ["2", "3"]
    ),
    'hanoi': MetaPuzzle(
        Hanoi,
        id              = "hanoi",
        auth            = "Anthony Ling",
        name            = "Towers of Hanoi",
        desc            = "Move smaller discs ontop of bigger discs. Fill the rightmost stack.",
        date            = "April 2, 2020",
        variants        = [
            "2_1", 
            "3_1", "3_2", "3_3", "3_4", "3_5", "3_6", "3_7", "3_8", 
            "4_1", "4_2", "4_3", "4_4", "4_5", "4_6", "4_1", "4_2", "4_3", "4_4", "4_5", "4_6", 
            "5_1", "5_2", "5_3", "5_4"
        ],
        test_variants   = ["3_1", "3_2", "3_3"]
    ),
    'lights': MetaPuzzle(
        LightsOut,
        id              = "lights",
        auth            = "Anthony Ling",
        name            = "Lights Out",
        desc            = 'Click on the squares on the grid to turn it and adjacent squares off. Try to turn off all the squares!',
        date            = "April 6, 2020",
        variants        = ["2", "3", "4"]
    ),
    'peg': MetaPuzzle(
        Peg,
        id              = "peg",
        auth            = "Mark Presten",
        name            = "Peg Solitaire",
        desc            = "Jump over a peg with an adjacent peg, removing it from the board. Have one peg remaining by end of the game.",
        date            = "April 15, 2020",
        variants        = ["Triangle"]
    ),
    'chairs': MetaPuzzle(
        Chairs,
        id              = "chairs",
        auth            = "Mark Presten",
        name            = "Chairs",
        desc            = "Move all pieces from one side of the board to the other by hopping over adjacent pieces. The end result should be a flipped version of the starting state.",
        date            = "April 25, 2020",
        variants        = ["10"]
    ),
    'bishop': MetaPuzzle(
        Bishop,
        id              = "bishop",
        auth            = "Brian Delaney",
        name            = "Bishops",
        desc            = "Swap the locations of two sets of bishops on opposite ends of a chessboard, without moving them into threatened positions.",
        date            = "October 30, 2020",
        variants        = ["2x5", "2x7", "3x7"],
        test_variants   = ["2x5", "2x7"]
    ),
    'topspin': MetaPuzzle(
        TopSpin,
        id              = "topspin",
        auth            = "Yishu Chao",
        name            = "Top Spin",
        desc            = "Move the beads along the track and spin the ones in the spinner until the beads are in order clock-wise, with 1 in the first spot in the spinner.",
        date            = "November 23, 2020",
        variants        = ["6_2"],
    ),
    'hopdrop': MetaPuzzle(
        HopNDrop,
        id              = "hopdrop",
        auth            = "Mark Presten",
        name            = "Hop N' Drop",
        desc            = "Clear all platforms before reaching the goal tile. Don't get stuck or fall!",
        date            = "October 10, 2020",
        variants        = ["map1", "map2", "map3"]
    ),
    # 'rubiks': MetaPuzzle(
    #     Rubiks,
    #     id              = "rubiks",
    #     auth            = "Mark Presten",
    #     name            = "Rubik's Cube",
    #     desc            = "Solve the Rubik's cube by getting one color/number on each face using rotations.",
    #     date            = "Semptember 14, 2020",
    #     variants        = ["2x2"]
    # )
}

class PuzzleManagerClass:
    """Controls what type of solver is applicable for a Puzzle and its variant"""

    def __init__(self, puzzleList):
        self.puzzleList = puzzleList

    def getPuzzleIds(self):
        """Returns a list of all the Puzzle ids"""
        return self.puzzleList.keys()

    def getPuzzleClasses(self):
        """Returns a list of all the Puzzle classes"""
        return [p.p_cls for p in self.puzzleList.values()]

    def hasPuzzleId(self, puzzleid):
        """Checks if the puzzleid is located within the puzzleList"""
        return puzzleid in self.puzzleList
    
    def getPuzzleClass(self, puzzleid):
        """Basic getter method to "get" a Puzzle class"""
        return self.puzzleList[puzzleid].p_cls
    
    def getSolverClass(self, puzzleid, variantid=None, test=False):
        """Get Solver Class given the puzzleid"""
        if puzzleid in [Hanoi.puzzleid, LightsOut.puzzleid, Bishop.puzzleid, Npuzzle.puzzleid]:
            return IndexSolver
        return SqliteSolver
    
    def validate(self, puzzleid, variantid=None, positionid=None):
        """Checks if the positionid fits the rules set for the puzzle, as
        well as if it's supported by the app.
        
        Raises a PuzzleException for the following:
        - puzzleid is not implemented
        - variantid is not the proper Type
        - variantid is not part of the puzzle implementation
        - fromString doesn't raise a Exception

        Inputs:
            - puzzleid
            - positionid: 
            - variantid: 
        """
        if puzzleid not in puzzleList:
            raise PuzzleException("Invalid PuzzleID")

        puzzlecls = self.puzzleList[puzzleid]
        if variantid is not None:
            if not isinstance(variantid, str): 
                raise PuzzleException("Invalid VariantID")
            if variantid not in puzzlecls.variants:
                raise PuzzleException("Out of bounds VariantID")
        
        if positionid is not None:
            try:
                puzzle = puzzlecls.fromString(positionid)
            except (ValueError, TypeError):
                raise PuzzleException("Invalid PositionID")

            if variantid is not None and puzzle.variant != variantid:
                raise PuzzleException("VariantID doesn't match PuzzleID")

PuzzleManager = PuzzleManagerClass(puzzleList)