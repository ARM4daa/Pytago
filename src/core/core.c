#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


// masks
static const uint64_t base_mask_rot_clock_corners1[4] = {
    0b111000000000000000000000000000000000ULL >> (9*0),
    0b111000000000000000000000000000000000ULL >> (9*1),
    0b111000000000000000000000000000000000ULL >> (9*2),
    0b111000000000000000000000000000000000ULL >> (9*3)
};
static const uint64_t base_mask_rot_clock_corners2[4] = {
    0b000100000000000000000000000000000000ULL >> (9*0),
    0b000100000000000000000000000000000000ULL >> (9*1),
    0b000100000000000000000000000000000000ULL >> (9*2),
    0b000100000000000000000000000000000000ULL >> (9*3)
};
static const uint64_t base_mask_rot_clock_sides1[4] = {
    0b000011100000000000000000000000000000ULL >> (9*0),
    0b000011100000000000000000000000000000ULL >> (9*1),
    0b000011100000000000000000000000000000ULL >> (9*2),
    0b000011100000000000000000000000000000ULL >> (9*3)
};
static const uint64_t base_mask_rot_clock_sides2[4] = {
    0b000000010000000000000000000000000000ULL >> (9*0),
    0b000000010000000000000000000000000000ULL >> (9*1),
    0b000000010000000000000000000000000000ULL >> (9*2),
    0b000000010000000000000000000000000000ULL >> (9*3)
};


/*
Functions for sub-boards rotations.
Clockwise and anti-clockwise rotations are separated to avoid unnecessary
branching or list access.
*/
static inline uint64_t rotate_board_clockwise(uint64_t board, int index) {
    uint64_t mask1 = base_mask_rot_clock_corners1[index];
    uint64_t mask2 = base_mask_rot_clock_corners2[index];
    uint64_t corners = ((board & mask1) >> 1) | ((board & mask2) << 3);
    board &= ~(mask1 | mask2);
    board |= corners;

    mask1 = base_mask_rot_clock_sides1[index];
    mask2 = base_mask_rot_clock_sides2[index];
    uint64_t sides = ((board & mask1) >> 1) | ((board & mask2) << 3);
    board &= ~(mask1 | mask2);
    board |= sides;

    return board;
}


static inline uint64_t rotate_board_aclockwise(uint64_t board, int index) {
    uint64_t mask1 = base_mask_rot_clock_corners1[index];
    uint64_t mask2 = base_mask_rot_clock_corners2[index];
    uint64_t corners = ((board & mask1) << 1) | ((board & mask2) >> 3);
    board &= ~(mask1 | mask2);
    board |= corners;

    mask1 = base_mask_rot_clock_sides1[index];
    mask2 = base_mask_rot_clock_sides2[index];
    uint64_t sides = ((board & mask1) << 1) | ((board & mask2) >> 3);
    board &= ~(mask1 | mask2);
    board |= sides;

    return board;
}


static inline uint64_t place_marble(uint64_t board, uint64_t pos) {
    return board | pos;
}


/*
TODO: create WIN_MASKS
static inline bool is_won(uint64_t board) {
    for (size_t i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        if ((board & mask) == mask)
            return true;
    }
    return false;
}
*/
