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



int negamax(uint64_t me, uint64_t opp, int depth, int alpha, int beta){
    int score = 0;
    int best;
    uint64_t child_me, child_opp;
    
    if (is_won(me) || depth == 0){
        return evaluate(me, opp);
    }

    best = -10000;
    uint64_t m = 1;
    while (m != 68719476736) {
        for (int i = 0; i < 4; i++){
            uint64_t child_me = me | m;
            
            child_me = rotate_board_aclockwise(child_me, i);
            child_opp = rotate_board_aclockwise(opp, i);
        
            score = -negamax(child_opp, child_me, depth-1, -alpha, -beta);
            if (score >= beta){ 
                return score; 
            }
            if (score > best){
                best = score;
            }
            if (score > alpha){
                alpha = score;
            }
            if (alpha >= beta){
                break;
            }
            
            child_me = rotate_board_clockwise(child_me, i);
            child_opp = rotate_board_clockwise(opp, i);
            
            score = -negamax(child_opp, child_me, depth-1, -alpha, -beta);
            if (score >= beta){ 
                return score; 
            }
            if (score > best){
                best = score;
            }
            if (score > alpha){
                alpha = score;
            }
            if (alpha >= beta){
                break;
            }

        }
        m <<= 1;
    }
    return best;
}

struct move get_best_move(uint64_t me, uint64_t opp, int depth){
    int best = -10000;
    int score = 0;
    uint64_t child_me, child_opp;
    struct move best_move;

    uint64_t m = 1;
    while (m != 68719476736) {      // 68719476736 = 2**36
        for (int i = 0; i < 4; i++){
            child_me = me | m;
        
            child_me = rotate_board_aclockwise(child_me, i);
            child_opp = rotate_board_aclockwise(opp, i);
                
            score = -negamax(child_opp, child_me, depth-1, -10000, 10000);

            if (score > best){
                best = score;
                best_move.pos = m;
                best_move.quadrant = i;
                best_move.clockwise = 0;
                }

            child_me = rotate_board_clockwise(child_me, i);
            child_opp = rotate_board_clockwise(opp, i);
            
            score = -negamax(child_opp, child_me, depth-1, -10000, 10000);

            if (score > best){
                best = score;
                best_move.pos = m;
                best_move.quadrant = i;
                best_move.clockwise = 1;
            }
            
        }
        m <<= 1; // multiply by two
    }
    return best_move;
}