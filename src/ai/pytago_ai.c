#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "core.h"
#include "masks.h"
#include "pytago_ai.h"


#define TT_SIZE 4000003
#define WIN_SCORE 10000
#define MAX_MOVES 288


/**
 * @brief Stock a game move with all information necessary
 * 
 * pos : Position of marble (bitmask 64b)
 * quadrant : wicht Quadrant rotation (0-3)
 * clockwise : the direction in which the board turned, 0=left, 1=right
 * score : Score of the position give by NegaMax/évaluation
 */
struct scored_move {
    uint64_t pos;
    int quadrant;
    int clockwise;
    int score;
};


/**
* @brief Store 2**n with n ranging from 0 to 5
*/
static const int puissance_of_5[6] = {1, 5, 25, 125, 625, 3125};


/**
 * @brief Transposition table bound flags.
 * 
 * Indicates stored score precision: exact or bound type.
 * 
 * @arg EXACT      Exact score (alpha <= score <= beta)
 * @arg LOWERBOUND Lower bound (score >= beta, beta-cutoff)
 * @arg UPPERBOUND Upper bound (score <= alpha, alpha-cutoff)
 */
typedef enum { EXACT, LOWERBOUND, UPPERBOUND } TTFlag;


/**
* @brief Define an element of the array TTEntry
* 
* key_me is the current board
* key_opp is the opponent's board
* depth is the depth at which the position was stored
* score is the score of the position
*/
typedef struct {
    uint64_t key_me;
    uint64_t key_opp;
    int depth;
    int score;
    TTFlag flag;
} TTEntry;


TTEntry tt[TT_SIZE];  // Define the size of the table TTEntry


/**
 * @brief Counts the number of bits set in a number.
 *
 * This function counts the number of marble in a board with the function
 * __builtin_popcountll() for performance.
 *
 * @param board 
 * @return int the number bits set in a number
 */
static inline int nb_bit(uint64_t board) {
    return __builtin_popcountll(board);
}


/**
* @brief Give the score to a board
*
* This function calculates the score for my board and the score for the 
* opposing board. To calculate a score, it compares the position of the 
* board with the WIN_MASK list, which contains all the winning positions 
* and allows you to know how many balls are aligned, and returns 2**n, where n 
* is the number of balls aligned.
*
* @param board_me current board
* @param board_opp opponent's board
* @return int the difference between my board and my opponent's board
*/
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


/**
* @brief hash the game state to compute TTIndex
*
* This function calculates the hash of the current position.
* This hash serves as an index for the TTEntry array. The hash is calculated
* by multiplying the current board by the Knuth number, then XORing the 
* result with the opponent's board, and then performing a modulo operation 
* with TT_SIZE so that the index does not exceed the maximum size of the array.
*
* @param me current board
* @param opp opponent's board
* @return int the index to store 
*/
static inline uint64_t hash_board(uint64_t me, uint64_t opp) {
    return (me * 0x9E3779B97F4A7C15ULL ^ opp) % TT_SIZE;
}


/**
 * @brief Lookup score in transposition table.
 * 
 * Searches for a score that has already been calculated in the transposition
 * table (TT) to avoid recalculating the position.
 * Returns 1 if usable score found, fills score via pointer.
 * Applies alpha-beta cutoff conditions.
 * 
 * @param me Player board state
 * @param opp Opponent board state  
 * @param depth Search depth
 * @param alpha Lower bound
 * @param beta Upper bound
 * @param[out] score Retrieved score (if found)
 * @return int 1=hit (score valid), 0=miss
 */
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


/**
 * @brief Stores search result in transposition table with bound type detection.
 * 
 * Computes hash index, stores position keys and evaluation result.
 * Automatically determines flag type based on alpha-beta window:
 * 
 * **Flag Logic:**
 *  - `score >= beta` → `LOWERBOUND` : Beta cutoff occurred, score is optimistic
 *    (future searches with β ≤ score can prune immediately via tt_lookup)
 *  - `score <= alpha` → `UPPERBOUND` : Alpha cutoff occurred, score is 
 *     pessimistic 
 *    (future searches with α ≥ score can prune immediately)
 *  - `alpha < score < beta` → `EXACT` : Precise value within current window
 * 
 * **Replacement Policy:** Always overwrites slot (no depth/age check).
 * This is correct for iterative deepening (deeper always replaces).
 * 
 * **Hash Collisions:** Uses Zobrist-like probing. Collision overwrites
 * previous entry (replacement acceptable due to depth priority).
 * 
 * @param me     Player's current board (64-bit bitboard)
 * @param opp    Opponent's current board (64-bit bitboard)  
 * @param depth  Search depth reached for this evaluation
 * @param score  Raw negamax score (-WIN_SCORE..+WIN_SCORE)
 * @param alpha  Current lower bound (improved during search)
 * @param beta   Current upper bound (decreased during search)
 * 
 * @note Called from `negamax()` after every node evaluation:
 *       - Terminal positions (win/loss/draw)
 *       - Leaf nodes (quiescence/evaluate)  
 *       - Internal nodes (after move loop completion)
 */
void tt_store(uint64_t me, uint64_t opp, int depth, int score, int alpha, int beta) {
    uint64_t idx = hash_board(me, opp);
    TTEntry *e = &tt[idx];
    e->key_me = me;
    e->key_opp = opp;
    e->depth = depth;
    e->score = score;

    // Determine bound type for future cutoff detection
    if (score >= beta) e->flag = LOWERBOUND; // Beta cutoff: optimistic bound
    else if (score <= alpha) e->flag = UPPERBOUND; // Alpha cutoff: pessimistic bound
    else e->flag = EXACT;
}


/**
 * @brief NegaMax search with alpha-beta pruning and transposition table.
 * 
 * Principal recursive search algorithm for Pytago AI. Explores game tree
 * using bitboard rotations as moves. Returns best score for current player.
 * 
 * **Search Flow:**
 * 1. TT lookup → return if hit
 * 2. Terminal test → win/loss/draw
 * 3. Leaf evaluation → heuristic score  
 * 4. Move generation → 36 positions × 8 rotations = 288 max moves
 * 5. Recursive search → MAXIMIZING player (negamax transformation)
 * 6. Alpha-beta update → pruning + window tightening
 * 7. TT store → result + bound type
 * 
 * **Scoring:**
 *  - Win:  `+WIN_SCORE - depth` (earlier win = better)
 *  - Loss: `-WIN_SCORE + depth` (later loss = better) 
 *  - Draw: `-depth` (shorter = better)
 * 
 * **Move Order:** Sequential (bit 0→35, 4 quadrants, ACW/CW rotations)
 * No move ordering → améliorable avec MVV/LVA ou TT scores.
 * 
 * @param me    Player's current board (64-bit bitboard)
 * @param opp   Opponent's current board (64-bit bitboard)
 * @param depth Remaining depth to search
 * @param alpha Lower bound (best MAX score found so far)  
 * @param beta  Upper bound (best MIN score opponent can force)
 * @return int Best achievable score for player-to-move
 */
int negamax(uint64_t me, uint64_t opp, int depth, int alpha, int beta) {
    int score;

    // 1. Transposition Table lookup (fail = continue search)
    if (tt_lookup(me, opp, depth, alpha, beta, &score)) return score;

    int alpha_orig = alpha; // Keep original bounds for TT store

    // 2. Terminal positions
    if (is_won(me) && is_won(opp)) {   // Draw (both completed lines)
        score = -depth;
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }
    if (is_won(me)) {    // Immediate win
        score = WIN_SCORE - depth;
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }
    if (is_won(opp)) {  // Immediate loss 
        score = -WIN_SCORE + depth;
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }
    // 3. Leaf node → static evaluation
    if (depth == 0) {
        score = evaluate(me, opp);
        tt_store(me, opp, depth, score, alpha, beta);
        return score;
    }

    // 4. Internal node → generate moves
    int best = -10000;
    uint64_t child_me, child_opp;
    uint64_t m = 1; // Bit position iterator (0→3
    uint64_t board = me | opp; // Occupied positions

    // 5. Explore all legal moves: 36 positions × 8 rotations
    while (m != 68719476736ULL) {
        if ((m & board) == 0) { // Empty position found
            for (int i = 0; i < 4; i++) { // 4 quadrants
                child_me = rotate_board_aclockwise(me | m, i);
                child_opp = rotate_board_aclockwise(opp, i);
                score = -negamax(child_opp, child_me, depth-1, -beta, -alpha);
                // Beta cutoff → immediate return (pruning!)
                if (score >= beta) {
                    tt_store(me, opp, depth, score, alpha_orig, beta);
                    return score;
                }
                // Update MAX bounds
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
        m <<= 1; // Next bit position
    }

    // 6. Store final result before return
    tt_store(me, opp, depth, best, alpha_orig, beta);
    return best;
}


/**
 * @brief Compare scored moves in descending order for qsort().
 * 
 * Sorts moves by score (highest first) to prioritize best moves first.
 * Enables better alpha-beta pruning (early cutoffs).
 * 
 * @param a First move pointer
 * @param b Second move pointer
 * @return int >0 if b better, <0 if a better, 0 if equal
 */
static int cmp_desc(const void *a, const void *b) {
    return ((struct scored_move*)b)->score - ((struct scored_move*)a)->score;
}


/**
 * @brief Applies scored move to generate child board states.
 * 
 * Places marble at position, then applies quadrant rotation.
 * Fills output pointers with resulting player/opponent boards.
 * 
 * @param me        Current player board
 * @param opp       Current opponent board  
 * @param mv        Move to apply (pos + quadrant + direction)
 * @param[out] child_me  Resulting player board after move
 * @param[out] child_opp Resulting opponent board after move
 */
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


/**
 * @brief Generates all legal root moves for current position.
 * 
 * Enumerates empty positions (36 bits) and generates 8 rotations per position:
 * 4 quadrants × 2 directions = **288 maximum moves**.
 * 
 * **Algorithm:**
 * - Iterate bits 0→35 (plateau hexagonal 6×6)
 * - Skip occupied positions (`m & board == 0`)
 * - For each free spot: 4 quadrants × (ACW + CW) = 8 moves
 * 
 * @param me    Current player board
 * @param opp   Opponent board  
 * @param[out] moves Array to fill with scored_move structs
 * @return int Number of legal moves generated (≤288)
 */
static int generate_root_moves(uint64_t me, uint64_t opp, struct scored_move *moves) {
    int count = 0;
    uint64_t board = me | opp; // All occupied positions
    uint64_t m = 1;           // Bit position iterator

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


/**
 * @brief Quick-scores root moves using transposition table hits.
 * 
 * Fills move.score from TT for current iteration depth **without recursion**.
 * Used in iterative deepening to order principal variation first.
 * 
 * **Scoring Logic:**
 * - Apply move → get child position
 * - `tt_lookup(depth-1)` → score si hit
 * - **Fallback 0** si miss (TODO: heuristic comme `evaluate()`)
 * 
 * **Bounds larges** (`±10000`) → accepts ALL TT hits (no cutoff).
 * 
 * @param me       Root player board
 * @param opp      Root opponent board
 * @param moves    Array of moves to score (from generate_root_moves)
 * @param count    Number of moves  
 * @param depth    Current iteration depth (pour tt_lookup)
 */
static void score_root_moves(uint64_t me, uint64_t opp, struct scored_move *moves, int count, int depth) {
    int alpha = 10000;  // Large bounds = accept all TT hits
    int beta  = -10000;

    for (int i = 0; i < count; i++) {
        uint64_t child_me, child_opp;
        apply_move(me, opp, &moves[i], &child_me, &child_opp);
        int score = 0;
        // TT hit → free score ! (else fallback 0)
        if (tt_lookup(child_me, child_opp, depth-1, alpha, beta, &score)) {
            moves[i].score = score;
        } else {
            moves[i].score = 0; // TODO: use heuristics as fallback
        }
    }
}


/**
 * @brief Principal AI decision function using Iterative Deepening.
 * 
 * Searches increasingly deeper (d=1→max_depth) and returns best root move.
 * 
 * **Iterative Deepening Algorithm:**
 * ```
 * for d = 1 to max_depth:
 *   1. score_root_moves() → TT scores for sorting
 *   2. qsort() descending → PV first
 *   3. Full α-β search on ALL moves (root = no β-cutoff!)
 *   4. Update best_move with new best
 * ```
 * 
 * **Why ID + TT perfect:**
 * - d=1 fast → approximate PV
 * - d=2 uses d1 TT → precise PV + pruning
 * - d=max_depth → optimal time-to-depth
 * 
 * 
 * @param me        Root player board
 * @param opp       Root opponent board
 * @param max_depth Maximum search depth (ex: 8-12)
 * @return Best root move (struct move)
 */
struct move get_best_move(uint64_t me, uint64_t opp, int max_depth) {
    struct move best_move = {0};
    int best_score = -10000;

    struct scored_move moves[MAX_MOVES];
    int move_count = generate_root_moves(me, opp, moves);

    // Iterative deepening loop
    for (int d = 1; d <= max_depth; d++) {
        // Phase 1: Score moves via TT hits (fast!)
        score_root_moves(me, opp, moves, move_count, d);

        // Phase 2: Sort best-first (alpha-beta killer!)
        qsort(moves, move_count, sizeof(struct scored_move), cmp_desc);

        // Phase 3: Full searches (root = no beta cutoff)
        int alpha = -10000;
        int beta = 10000;

        for (int i = 0; i < move_count; i++) {
            uint64_t child_me, child_opp;
            apply_move(me, opp, &moves[i], &child_me, &child_opp);

            // NegaMax with negated bounds (opponent perspective)
            int score = -negamax(child_opp, child_me, d-1, -beta, -alpha);

            // Update PV if bette
            if (score > best_score) {
                best_score = score;
                best_move.pos = moves[i].pos;
                best_move.quadrant = moves[i].quadrant;
                best_move.clockwise = moves[i].clockwise;
            }

            // Alpha update (no beta-cutoff at root)
            if (best_score > alpha) alpha = best_score;
        }
    }

    return best_move;
}

