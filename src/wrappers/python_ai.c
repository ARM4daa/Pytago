/**
 * @file python_ai.c
 * @brief CPython wrapper for the Pytago AI.
 *
 * This file exposes the AI C function that seach the game tree for the best
 * move to Python via the CPython API.
 *
 * The point of these wrappers is to enable the Python GUI to get the best next
 * move from current state and enable the AI player.
 */


#include <stdint.h>
#include <Python.h>

#include "pytago_ai.h"


/**
 * @brief Python wrapper for rotate_board_clockwise().
 *
 * Rotates a 64-bit board clockwise at the specified quadrant.
 *
 * @param self Not used.
 * @param args Python tuple containing:
 *             - board (Python int): 64-bit board representation.
 *             - quadrant (Python int): Quadrant index (0–3) to rotate.
 * @return PyObject* Python int representing the rotated board.
 */
static PyObject* py_get_best_move(PyObject* self, PyObject* args) {
    uint64_t me, opp;
    int depth;

    if (!PyArg_ParseTuple(args, "KKi", &me, &opp, &depth)) {
        return NULL;
    }

    struct move best_move = get_best_move(me, opp, depth);

    PyObject* py_pos = PyLong_FromUnsignedLongLong(best_move.pos);
    PyObject* py_quadrant = PyLong_FromLong(best_move.quadrant);
    PyObject* py_clockwise = PyLong_FromLong(best_move.clockwise);

    return PyTuple_Pack(3, py_pos, py_quadrant, py_clockwise);
}


/**
 * @brief Method table for the Pytago AI Python module.
 *
 * Maps Python function name to C function.
 */
static PyMethodDef PytagoAIMethods[] = {
    {"get_best_move", py_get_best_move, METH_VARARGS, "Find best move from current position"},
    {NULL, NULL, 0, NULL}
};


/**
 * @brief Python module definition for Pytago AI.
 */
static struct PyModuleDef pytagoaimodule = {
    PyModuleDef_HEAD_INIT,
    "pytago_ai",
    "AI for Pytago",
    -1,
    PytagoAIMethods
};


/**
 * @brief Module initialization function.
 *
 * Called when Python imports the module.
 *
 * @return PyObject* Python module object.
 */
PyMODINIT_FUNC PyInit_pytago_ai(void) {
    return PyModule_Create(&pytagoaimodule);
};
