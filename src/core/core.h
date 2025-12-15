/**
 * @file core.h
 * @brief Core primitives for Pentago board operations.
 *
 * This module provides highly optimized bitboard operations for Pentago:
 * - Quadrant rotation (clockwise and anticlockwise)
 * - Marble placement
 * - Win detection
 *
 * The board is represented as a 36-bit integer with a custom layout:
 * corners, sides, and center bits are arranged for maximum rotation efficiency.
 *
 * All functions are declared `static inline` to allow aggressive inlining
 * and performance optimization by the compiler.
 *
 * Dependencies:
 * - masks.h: provides precomputed rotation and winning masks
 */


#ifndef CORE_H
#define CORE_H

#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#include "masks.h"


/**
 * @brief Rotates a 64-bit board clockwise at a specified index.
 *
 * This function applies a clockwise rotation to a quadrant using a set of
 * precomputed masks. It handles both corner and side bits using bitwise
 * operations.
 *
 * @param board The 64-bit board to be modified.
 * @param index The quadrant to rotate.
 * @return uint64_t The resulting board after clockwise rotation.
 *
 * @note This function is declared `static inline` for performance, and relies
 *       on the arrays `BASE_MASK_ROT_CLOCK_CORNERS1`,
 *       `BASE_MASK_ROT_CLOCK_CORNERS2`, `BASE_MASK_ROT_CLOCK_SIDES1`, and
 *       `BASE_MASK_ROT_CLOCK_SIDES2` to define rotation masks.
 */
static inline uint64_t rotate_board_clockwise(uint64_t board, int index) {
    uint64_t mask1 = BASE_MASK_ROT_CLOCK_CORNERS1[index];
    uint64_t mask2 = BASE_MASK_ROT_CLOCK_CORNERS2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) >> 1) | ((board & mask2) << 3);

    mask1 = BASE_MASK_ROT_CLOCK_SIDES1[index];
    mask2 = BASE_MASK_ROT_CLOCK_SIDES2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) >> 1) | ((board & mask2) << 3);

    return board;
}


/**
 * @brief Rotates a 64-bit board anticlockwise at a specified index.
 *
 * This function applies an anticlockwise rotation to a quadrant using a set of
 * precomputed masks. It handles both corner and side bits using bitwise
 * operations.
 *
 * @param board The 64-bit board to be modified.
 * @param index The quadrant to rotate.
 * @return uint64_t The resulting board after anticlockwise rotation.
 *
 * @note This function is declared `static inline` for performance, and relies
 *       on the arrays `BASE_MASK_ROT_ACLOCK_CORNERS1`,
 *       `BASE_MASK_ROT_ACLOCK_CORNERS2`, `BASE_MASK_ROT_ACLOCK_SIDES1`, and
 *       `BASE_MASK_ROT_ACLOCK_SIDES2` to define rotation masks.
 */
static inline uint64_t rotate_board_aclockwise(uint64_t board, int index) {
    uint64_t mask1 = BASE_MASK_ROT_ACLOCK_CORNERS1[index];
    uint64_t mask2 = BASE_MASK_ROT_ACLOCK_CORNERS2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) << 1) | ((board & mask2) >> 3);

    mask1 = BASE_MASK_ROT_ACLOCK_SIDES1[index];
    mask2 = BASE_MASK_ROT_ACLOCK_SIDES2[index];
    board = (board & ~(mask1 | mask2)) | ((board & mask1) << 1) | ((board & mask2) >> 3);

    return board;
}


/**
 * @brief Places a marble on the board at a specified position.
 *
 * This function sets the bit corresponding to the position of the marble on the
 * 64-bit board using a bitwise OR operation.
 *
 * @param board The 64-bit board to be modified.
 * @param pos  A 64-bit value with a single bit set at the marble's position.
 * @return uint64_t The resulting board with the marble placed.
 */
static inline uint64_t place_marble(uint64_t board, uint64_t pos) {
    return board | pos;
}


/**
 * @brief Checks if the board has a winning configuration.
 *
 * This function iterates through a set of precomputed winning masks and
 * determines if all bits for any winning pattern are set on the board.
 *
 * @param board The 64-bit board to check.
 * @return true if the board contains a winning pattern.
 * @return false otherwise.
 *
 * @note Relies on the `WIN_MASKS` array, which should contain all possible
 *       winning bit patterns.
 */
static inline bool is_won(uint64_t board) {
    for (size_t i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        if ((board & mask) == mask)
            return true;
    }
    return false;
}


#endif
