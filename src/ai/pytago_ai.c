#include <stdint.h>
#include <stdio.h>
#include "core.h"
#include "masks.h"
#include "pytago_ai.h"

static const int puissance_of_5[6] = {1, 5, 25, 125, 625, 3125};

static inline int nb_bit(uint64_t board) {
    return __builtin_popcountll(board);
}

static inline int evaluate(uint64_t board_me, uint64_t board_opp) {
    int score_me = 0;
    int score_opp = 0;
    int p = 0;

    for (int i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        p = nb_bit(board_me & mask);
        if (p != 0) {
            score_me += puissance_of_5[p];
        }
    }

    for (int i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        p = nb_bit(board_opp & mask);
        if (p != 0) {
            score_opp += puissance_of_5[p];
        }
    }

    return score_me - score_opp;
}


#define TT_SIZE 4000003

typedef struct {
    uint64_t key_me;
    uint64_t key_opp;
    int depth;
    int score;
} TTEntry;

TTEntry tt[TT_SIZE];

static inline uint64_t hash_board(uint64_t me, uint64_t opp) {
    return (me * 0x9E3779B97F4A7C15ULL ^ opp) % TT_SIZE;
}

int tt_lookup(uint64_t me, uint64_t opp, int depth, int *score) {
    uint64_t idx = hash_board(me, opp);
    if (tt[idx].key_me == me && tt[idx].key_opp == opp && tt[idx].depth >= depth) {
        *score = tt[idx].score;
        return 1;
    }
    return 0;
}

void tt_store(uint64_t me, uint64_t opp, int depth, int score) {
    uint64_t idx = hash_board(me, opp);
    tt[idx].key_me = me;
    tt[idx].key_opp = opp;
    tt[idx].depth = depth;
    tt[idx].score = score;
}


int negamax(uint64_t me, uint64_t opp, int depth, int alpha, int beta){
    int score;

    if (tt_lookup(me, opp, depth, &score)) {
        return score;
    }

    if (is_won(me) || depth == 0){
        score = evaluate(me, opp);
        tt_store(me, opp, depth, score);
        return score;
    }

    int best = -10000;
    uint64_t child_me, child_opp;
    uint64_t m = 1;
    uint64_t board = me | opp;

    while (m != 68719476736) {
        if ((m & board) == 0) {
            for (int i = 0; i < 4; i++){
                child_me = rotate_board_aclockwise(me | m, i);
                child_opp = rotate_board_aclockwise(opp, i);

                score = -negamax(child_opp, child_me, depth-1, -alpha, -beta);
                if (score >= beta){ 
                    tt_store(me, opp, depth, score);
                    return score; 
                }
                if (score > best) best = score;
                if (score > alpha) alpha = score;

                child_me = rotate_board_clockwise(me | m, i);
                child_opp = rotate_board_clockwise(opp, i);

                score = -negamax(child_opp, child_me, depth-1, -alpha, -beta);
                if (score >= beta){ 
                    tt_store(me, opp, depth, score);
                    return score; 
                }
                if (score > best) best = score;
                if (score > alpha) alpha = score;
            }
        }
        m <<= 1;
    }

    tt_store(me, opp, depth, best);
    return best;
}

struct move get_best_move(uint64_t me, uint64_t opp, int depth){
    int best = -10000;
    int score = 0;
    uint64_t child_me, child_opp;
    struct move best_move;

    uint64_t m = 1;
    uint64_t board = me | opp;

    while (m != 68719476736) {      // 2**36
        if ((m & board) == 0) {
            for (int i = 0; i < 4; i++){
                child_me = rotate_board_aclockwise(me | m, i);
                child_opp = rotate_board_aclockwise(opp, i);

                score = -negamax(child_opp, child_me, depth-1, -10000, 10000);
                if (score > best){
                    best = score;
                    best_move.pos = m;
                    best_move.quadrant = i;
                    best_move.clockwise = 0;
                }

                child_me = rotate_board_clockwise(me | m, i);
                child_opp = rotate_board_clockwise(opp, i);

                score = -negamax(child_opp, child_me, depth-1, -10000, 10000);
                if (score > best){
                    best = score;
                    best_move.pos = m;
                    best_move.quadrant = i;
                    best_move.clockwise = 1;
                }
            }
        }
        m <<= 1;
    }

    return best_move;
}