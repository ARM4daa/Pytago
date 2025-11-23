#include <stdbool.h>
#include <stdint.h>
#include <Python.h>

#include "core.h"


static PyObject* py_rotate_board_clockwise(PyObject* self, PyObject* args) {
    uint64_t board;
    int quadrant;

    if (!PyArg_ParseTuple(args, "Ki", &board, &quadrant)) {
        return NULL;
    }

    uint64_t result = rotate_board_clockwise(board, quadrant);
    return PyLong_FromUnsignedLongLong(result);
}


static PyObject* py_rotate_board_aclockwise(PyObject* self, PyObject* args) {
    uint64_t board;
    int quadrant;

    if (!PyArg_ParseTuple(args, "Ki", &board, &quadrant))
        return NULL;

    uint64_t result = rotate_board_aclockwise(board, quadrant);
    return PyLong_FromUnsignedLongLong(result);
}


static PyObject* py_place_marble(PyObject *self, PyObject *args) {
    uint64_t board, pos;

    if(!PyArg_ParseTuple(args, "KK", &board, &pos))
        return NULL;

    uint64_t result = place_marble(board, pos);
    return PyLong_FromUnsignedLongLong(result);
}


static PyObject* py_is_won(PyObject* self, PyObject* args) {
    uint64_t board;

    if (!PyArg_ParseTuple(args, "K", &board))
        return NULL;

    bool won = is_won(board);
    if (won) Py_RETURN_TRUE;
    else     Py_RETURN_FALSE;
}


static PyMethodDef PytagoMethods[] = {
    {"rotate_board_clockwise", py_rotate_board_clockwise, METH_VARARGS, "Rotate board at index i clockwise"},
    {"rotate_board_aclockwise", py_rotate_board_aclockwise, METH_VARARGS, "Rotate board at index i aclockwise"},
    {"place_marble", py_place_marble, METH_VARARGS, "Place a marble on the board"},
    {"is_won", py_is_won, METH_VARARGS, "Check if a board is a winning state"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef pytagomodule = {
    PyModuleDef_HEAD_INIT,
    "pytago",
    "High-speed Pytago core",
    -1,
    PytagoMethods
};


PyMODINIT_FUNC PyInit_pentago(void) {
    return PyModule_Create(&pentagomodule);
};
