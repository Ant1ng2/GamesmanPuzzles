import os
from ctypes import *
from puzzlesolver.puzzles import Hanoi, Peg, LightsOut, Chairs
import time

puzzlecls = Hanoi.generateStartPosition("3_12")
puzzle = puzzlecls

lib = PyDLL("./bin/libsolver.so")
init = lib.init
init.restype = c_void_p

setRemoteness = lib.setRemotenessPyObject
setRemoteness.argtypes = [ c_void_p, py_object, c_int ]

getRemoteness = lib.getRemotenessPyObject
getRemoteness.argtypes = [ c_void_p, py_object ]

solve = lib.solve
solve.argtypes = [ c_void_p, py_object ]

clear = lib.clear
clear.argtypes = [ c_void_p ]

ptr = init()
print("Init     : ", ptr)
print("Solve    : ", solve(ptr, puzzle))
print("Getting  : ", getRemoteness(ptr, puzzle))
print("Clearing : ", clear(ptr))