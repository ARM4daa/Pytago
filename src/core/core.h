#ifndef CORE_H
#define CORE_H

#include <stdbool.h>
#include <stdint.h>


inline uint64_t rotate_board_clockwise(uint64_t board, int index)
    __attribute__((always_inline));

inline uint64_t rotate_board_aclockwise(uint64_t board, int index)
    __attribute__((always_inline));

inline uint64_t place_marble(uint64_t board, uint64_t pos)
    __attribute__((always_inline));

inline bool is_won(uint64_t board)
    __attribute__((always_inline));


#endif
