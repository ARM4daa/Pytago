#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include "core.h"
#include "masks.h"


struct move {
    uint64_t pos;
    int quadrant;
    int clockwise;
};

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
            score_me += (int)pow(5, p);
        }
    }

    for (int i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        p = nb_bit(board_opp & mask);
        if (p != 0) {
            score_opp += (int)pow(5, p);
        }
    }

    return score_me - score_opp;
}



int negamax(uint64_t me, uint64_t opp, int depth, int alpha, int beta){
    int score = 0;
    int best;
    uint64_t child_me, child_opp;
    
    if (is_won(me) | depth == 0){
        return evaluate(me, opp);
    }

    best = -10000;
    uint64_t m = 1;
    while (m != 68719476736) {
        for (int i = 0; i < 4; i++){
            for (int c = 0; c < 2; c++) {
                uint64_t child_me = me | m;
                if (c){
                    child_me = rotate_board_clockwise(child_me, i);
                    child_opp = rotate_board_clockwise(opp, i);
                }else{
                    child_me = rotate_board_aclockwise(child_me, i);
                    child_opp = rotate_board_aclockwise(opp, i);
                
                }
                score = -negamax(child_opp, child_me, depth-1, -alpha, -beta);
                if (score >= beta){ 
                    return score; 
                }
                best = fmax(best, score);
                alpha = fmax(alpha, score);
                if (alpha >= beta){
                    break;
                }
            }
        }
        m <<= 1;
    }
    return best;
}

struct move get_next_move(uint64_t me, uint64_t opp, int depth){
    int best = -10000;
    int score = 0;
    uint64_t child_me, child_opp;
    struct move best_move;

    uint64_t m = 1;
    while (m != 68719476736) {      // 68719476736 = 2**36
        for (int i = 0; i < 4; i++){
            for (int c = 0; c < 2; c++) {
                child_me = me | m;
                if (c){
                    child_me = rotate_board_clockwise(child_me, i);
                    child_opp = rotate_board_clockwise(opp, i);
                }else{
                    child_me = rotate_board_aclockwise(child_me, i);
                    child_opp = rotate_board_aclockwise(opp, i);
                }
                score = -negamax(child_opp, child_me, depth-1, -10000, 10000);

                if (score > best){
                    best = score;
                    best_move.pos = m;
                    best_move.quadrant = i;
                    best_move.clockwise = c;
                }
            }
        }
        m <<= 1; // multiply by two
    }
    return best_move;
}