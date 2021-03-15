#include <Python.h>

#include "Hanoic.h"

static struct PyModuleDef puzzlesolverc = {
    PyModuleDef_HEAD_INIT, "puzzlesolverc",
    "C-extension interface for Puzzlesolver", -1,
    NULL
};

PyMODINIT_FUNC PyInit__puzzlesolverc(void) {
    PyObject* module = PyModule_Create(&puzzlesolverc);
    
    if (PyModule_AddPuzzle(module) < 0) {
        PyModule_RemovePuzzle();
        return NULL;
    }
    else if (PyModule_AddServerPuzzle(module) < 0) {
        PyModule_RemoveServerPuzzle();
        return NULL;
    }
    else if (PyModule_AddHanoi(module, ServerPuzzleTypePtr) < 0) {
        PyModule_RemoveHanoi();
        return NULL;
    }

    PyModule_AddStringMacro(module, UNSOLVABLE);
    PyModule_AddStringMacro(module, SOLVABLE);
    PyModule_AddStringMacro(module, UNDECIDED);

    return module;
}