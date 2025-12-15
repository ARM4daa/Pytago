#ifndef PYTAGO_AI_H
#define PYTAGO_AI_H

#include <stdint.h>

struct move {
    uint64_t pos;
    int quadrant;
    int clockwise;
};

struct move get_best_move(uint64_t me, uint64_t opp, int depth);

#endif