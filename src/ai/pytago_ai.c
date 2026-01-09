#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "core.h"
#include "masks.h"
#include "pytago_ai.h"


#define TT_SIZE 4000003
#define WIN_SCORE 10000
#define MAX_MOVES 288


struct scored_move {
    uint64_t pos;
    int quadrant;
    int clockwise;
    int score;
};

static const int puissance_of_5[6] = {1, 5, 25, 125, 625, 3125};

typedef enum { EXACT, LOWERBOUND, UPPERBOUND } TTFlag;

typedef struct {
    uint64_t key_me;
    uint64_t key_opp;
    int depth;
    int score;
    TTFlag flag;
} TTEntry;


TTEntry tt[TT_SIZE];


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
        if (p != 0) score_me += puissance_of_5[p];
    }

    for (int i = 0; i < 32; i++) {
        uint64_t mask = WIN_MASKS[i];
        p = nb_bit(board_opp & mask);
        if (p != 0) score_opp += puissance_of_5[p];
    }

    return score_me - score_opp;
}


static inline uint64_t hash_board(uint64_t me, uint64_t opp) {
    return (me * 0x9E3779B97F4A7C15ULL ^ opp) % TT_SIZE;
}


int tt_lookup(uint64_t me, uint64_t opp, int depth, int alpha, int beta, int *score) {
    uint64_t idx = hash_board(me, opp);
    TTEntry *e = &tt[idx];

    if (e->key_me != me || e->key_opp != opp || e->depth < depth)
        return 0;

    if (e->flag == EXACT) {
        *score = e->score;
        return 1;
    } else if (e->flag == LOWERBOUND && e->score >= beta) {
        *score = e->score;
        return 1;
    } else if (e->flag == UPPERBOUND && e->score <= alpha) {
        *score = e->score;
        return 1;
    }

    return 0;
}


void tt_store(uint64_t me, uint64_t opp, int depth, int score, int alpha, int beta) {
    uint64_t idx = hash_board(me, opp);
    TTEntry *e = &tt[idx];
    e->key_me = me;
    e->key_opp = opp;
    e->depth = depth;
    e->score = score;

    if (score >= beta) e->flag = LOWERBOUND;
    else if (score <= alpha) e->flag = UPPERBOUND;
    else e->flag = EXACT;
}


int negamax(uint64_t me, uint64_t opp, int depth, int alpha, int beta) {
    int score;

    if (tt_lookup(me, opp, depth, alpha, beta, &score)) return score;

    int alpha_orig = alpha;

    if (is_won(me) && is_won(opp)) {
        score = -depth;
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }
    if (is_won(me)) {
        score = WIN_SCORE - depth;
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }
    if (is_won(opp)) {
        score = -WIN_SCORE + depth;
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }
    if (depth == 0) {
        score = evaluate(me, opp);
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }

    int best = -10000;
    uint64_t child_me, child_opp;
    uint64_t m = 1;
    uint64_t board = me | opp;

    while (m != 68719476736ULL) {
        if ((m & board) == 0) {
            for (int i = 0; i < 4; i++) {
                child_me = rotate_board_aclockwise(me | m, i);
                child_opp = rotate_board_aclockwise(opp, i);
                score = -negamax(child_opp, child_me, depth-1, -beta, -alpha);
                if (score >= beta) {
                    tt_store(me, opp, depth, score, alpha_orig, beta);
                    return score;
                }
                if (score > best) best = score;
                if (score > alpha) alpha = score;

                child_me = rotate_board_clockwise(me | m, i);
                child_opp = rotate_board_clockwise(opp, i);
                score = -negamax(child_opp, child_me, depth-1, -beta, -alpha);
                if (score >= beta) {
                    tt_store(me, opp, depth, score, alpha_orig, beta);
                    return score;
                }
                if (score > best) best = score;
                if (score > alpha) alpha = score;
            }
        }
        m <<= 1;
    }

    tt_store(me, opp, depth, best, alpha_orig, beta);
    return best;
}


static int cmp_desc(const void *a, const void *b) {
    return ((struct scored_move*)b)->score - ((struct scored_move*)a)->score;
}


static void apply_move(uint64_t me, uint64_t opp, struct scored_move *mv,
                       uint64_t *child_me, uint64_t *child_opp) {
    if (mv->clockwise) {
        *child_me = rotate_board_clockwise(me | mv->pos, mv->quadrant);
        *child_opp = rotate_board_clockwise(opp, mv->quadrant);
    } else {
        *child_me = rotate_board_aclockwise(me | mv->pos, mv->quadrant);
        *child_opp = rotate_board_aclockwise(opp, mv->quadrant);
    }
}


static int generate_root_moves(uint64_t me, uint64_t opp, struct scored_move *moves) {
    int count = 0;
    uint64_t board = me | opp;
    uint64_t m = 1;

    while (m != 68719476736ULL) { // 2**36
        if ((m & board) == 0) {
            for (int q = 0; q < 4; q++) {
                moves[count++] = (struct scored_move){m, q, 0, 0};
                moves[count++] = (struct scored_move){m, q, 1, 0};
            }
        }
        m <<= 1;
    }
    return count;
}


static void score_root_moves(uint64_t me, uint64_t opp, struct scored_move *moves, int count, int depth) {
    int alpha = 10000;
    int beta  = -10000;

    for (int i = 0; i < count; i++) {
        uint64_t child_me, child_opp;
        apply_move(me, opp, &moves[i], &child_me, &child_opp);
        int score = 0;
        if (tt_lookup(child_me, child_opp, depth-1, alpha, beta, &score)) {
            moves[i].score = score;
        } else {
            moves[i].score = 0; // TODO: use heuristics as fallback
        }
    }
}


struct move get_best_move(uint64_t me, uint64_t opp, int max_depth) {
    struct move best_move = {0};
    int best_score = -10000;

    struct scored_move moves[MAX_MOVES];
    int move_count = generate_root_moves(me, opp, moves);

    for (int d = 1; d <= max_depth; d++) {
        score_root_moves(me, opp, moves, move_count, d);

        qsort(moves, move_count, sizeof(struct scored_move), cmp_desc);

        int alpha = -10000;
        int beta = 10000;

        for (int i = 0; i < move_count; i++) {
            uint64_t child_me, child_opp;
            apply_move(me, opp, &moves[i], &child_me, &child_opp);

            int score = -negamax(child_opp, child_me, d-1, -beta, -alpha);

            if (score > best_score) {
                best_score = score;
                best_move.pos = moves[i].pos;
                best_move.quadrant = moves[i].quadrant;
                best_move.clockwise = moves[i].clockwise;
            }

            if (best_score > alpha) alpha = best_score;
        }
    }

    return best_move;
}

