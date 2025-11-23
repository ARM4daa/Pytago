#ifndef CORE_H
#define CORE_H

#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#include "masks.h"


inline uint64_t rotate_board_clockwise(uint64_t board, int index)
    __attribute__((always_inline));
uint64_t rotate_board_clockwise(uint64_t board, int index) {
    uint64_t mask1 = BASE_MASK_ROT_CLOCK_CORNERS1[index];
    uint64_t mask2 = BASE_MASK_ROT_CLOCK_CORNERS2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) >> 1) | ((board & mask2) << 3);

    mask1 = BASE_MASK_ROT_CLOCK_SIDES1[index];
    mask2 = BASE_MASK_ROT_CLOCK_SIDES2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) >> 1) | ((board & mask2) << 3);

    return board;
}


inline uint64_t rotate_board_aclockwise(uint64_t board, int index)
    __attribute__((always_inline));
uint64_t rotate_board_aclockwise(uint64_t board, int index) {
    uint64_t mask1 = BASE_MASK_ROT_ACLOCK_CORNERS1[index];
    uint64_t mask2 = BASE_MASK_ROT_ACLOCK_CORNERS2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) << 1) | ((board & mask2) >> 3);

    mask1 = BASE_MASK_ROT_ACLOCK_SIDES1[index];
    mask2 = BASE_MASK_ROT_ACLOCK_SIDES2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) << 1) | ((board & mask2) >> 3);

    return board;
}

inline uint64_t place_marble(uint64_t board, uint64_t pos)
    __attribute__((always_inline));
uint64_t place_marble(uint64_t board, uint64_t pos) {
    return board | pos;
}


inline bool is_won(uint64_t board)
    __attribute__((always_inline));
bool is_won(uint64_t board) {
    for (size_t i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        if ((board & mask) == mask)
            return true;
    }
    return false;
}


#endif
