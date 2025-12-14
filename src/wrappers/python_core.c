/**
 * @file python_core.c
 * @brief CPython wrapper for the high-performance Pytago C core.
 *
 * This file exposes the optimized C functions for Pentago board manipulation
 * to Python via the CPython API. Functions include:
 * - rotate_board_clockwise(board, quadrant)
 * - rotate_board_aclockwise(board, quadrant)
 * - place_marble(board, pos)
 * - is_won(board)
 *
 * All functions convert Python integers to 64-bit C integers, call the core
 * functions, and convert the result back to Python integers.
 *
 * The point of these wrappers is to enable the Python GUI to manipulate the
 * game bitboards.
 */


#include <stdbool.h>
#include <stdint.h>
#include <Python.h>

#include "core.h"


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
static PyObject* py_rotate_board_clockwise(PyObject* self, PyObject* args) {
    uint64_t board;
    int quadrant;

    if (!PyArg_ParseTuple(args, "Ki", &board, &quadrant)) {
        return NULL;
    }

    uint64_t result = rotate_board_clockwise(board, quadrant);
    return PyLong_FromUnsignedLongLong(result);
}


/**
 * @brief Python wrapper for rotate_board_aclockwise().
 *
 * Rotates a 64-bit board anticlockwise at the specified quadrant.
 *
 * @param self Not used.
 * @param args Python tuple containing:
 *             - board (Python int): 64-bit board representation.
 *             - quadrant (Python int): Quadrant index (0–3) to rotate.
 * @return PyObject* Python int representing the rotated board.
 */
static PyObject* py_rotate_board_aclockwise(PyObject* self, PyObject* args) {
    uint64_t board;
    int quadrant;

    if (!PyArg_ParseTuple(args, "Ki", &board, &quadrant))
        return NULL;

    uint64_t result = rotate_board_aclockwise(board, quadrant);
    return PyLong_FromUnsignedLongLong(result);
}


/**
 * @brief Python wrapper for place_marble().
 *
 * Places a marble on the board at the specified position.
 *
 * @param self Not used.
 * @param args Python tuple containing:
 *             - board (Python int): Current 64-bit board.
 *             - pos (Python int): Single-bit 64-bit integer representing the marble position.
 * @return PyObject* Python int representing the board with the marble placed.
 */
static PyObject* py_place_marble(PyObject *self, PyObject *args) {
    uint64_t board, pos;

    if(!PyArg_ParseTuple(args, "KK", &board, &pos))
        return NULL;

    uint64_t result = place_marble(board, pos);
    return PyLong_FromUnsignedLongLong(result);
}


/**
 * @brief Python wrapper for is_won().
 *
 * Checks if the board has a winning configuration.
 *
 * @param self Not used.
 * @param args Python tuple containing:
 *             - board (Python int): 64-bit board to check.
 * @return PyObject* Py_True if the board contains a winning pattern,
 *                   Py_False otherwise.
 */
static PyObject* py_is_won(PyObject* self, PyObject* args) {
    uint64_t board;

    if (!PyArg_ParseTuple(args, "K", &board))
        return NULL;

    bool won = is_won(board);
    if (won) Py_RETURN_TRUE;
    else     Py_RETURN_FALSE;
}


/**
 * @brief Method table for the Pytago Python module.
 *
 * Maps Python function names to C functions.
 */
static PyMethodDef PytagoMethods[] = {
    {"rotate_board_clockwise", py_rotate_board_clockwise, METH_VARARGS, "Rotate board at index i clockwise"},
    {"rotate_board_aclockwise", py_rotate_board_aclockwise, METH_VARARGS, "Rotate board at index i aclockwise"},
    {"place_marble", py_place_marble, METH_VARARGS, "Place a marble on the board"},
    {"is_won", py_is_won, METH_VARARGS, "Check if a board is a winning state"},
    {NULL, NULL, 0, NULL}
};


/**
 * @brief Python module definition for Pytago core.
 */
static struct PyModuleDef pytagomodule = {
    PyModuleDef_HEAD_INIT,
    "pytago_core",
    "High-speed Pytago core",
    -1,
    PytagoMethods
};


/**
 * @brief Module initialization function.
 *
 * Called when Python imports the module.
 *
 * @return PyObject* Python module object.
 */
PyMODINIT_FUNC PyInit_pytago_core(void) {
    return PyModule_Create(&pytagomodule);
};
