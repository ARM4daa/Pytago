/**
 * @file masks.h
 * @brief Precomputed masks for Pentago board operations.
 *
 * These arrays contain bit patterns used for rotating quadrants
 * and checking winning lines.
 */


#ifndef MASKS_H
#define MASKS_H

#include <stdint.h>


/**
 * @brief Clockwise rotation masks for quadrant corners (group 1).
 *
 * This arrays contains the masks used to extract the first three bits to shift
 * to the right by one position.
 */
extern const uint64_t BASE_MASK_ROT_CLOCK_CORNERS1[4];

/**
 * @brief Clockwise rotation masks for quadrant corners (group 2).
 *
 * This arrays contains the masks used to extract the last bit to shift to the
 * left by three positions.
 */
extern const uint64_t BASE_MASK_ROT_CLOCK_CORNERS2[4];

/**
 * @brief Clockwise rotation masks for quadrant sides (group 1).
 *
 * This arrays contains the masks used to extract the first three bits to shift
 * to the right by one position.
 */
extern const uint64_t BASE_MASK_ROT_CLOCK_SIDES1[4];

/**
 * @brief Clockwise rotation masks for quadrant sides (group 2).
 *
 * This arrays contains the masks used to extract the last bit to shift to the
 * left by three positions.
 */
extern const uint64_t BASE_MASK_ROT_CLOCK_SIDES2[4];

/**
 * @brief Anticlockwise rotation masks for quadrant corners (group 1).
 *
 * This arrays contains the masks used to extract the last three bits to shift
 * to the left by one position.
 */
extern const uint64_t BASE_MASK_ROT_ACLOCK_CORNERS1[4];

/**
 * @brief Anticlockwise rotation masks for quadrant corners (group 2).
 *
 * This arrays contains the masks used to extract the first bit to shift to the
 * right by three positions.
 */
extern const uint64_t BASE_MASK_ROT_ACLOCK_CORNERS2[4];

/**
 * @brief Anticlockwise rotation masks for quadrant sides (group 1).
 *
 * This arrays contains the masks used to extract the last three bits to shift
 * to the left by one position.
 */
extern const uint64_t BASE_MASK_ROT_ACLOCK_SIDES1[4];

/**
 * @brief Anticlockwise rotation masks for quadrant sides (group 2).
 *
 * This arrays contains the masks used to extract the first bit to shift to the
 * right by three positions.
 */
extern const uint64_t BASE_MASK_ROT_ACLOCK_SIDES2[4];

/**
 * @brief All possible winning bit patterns on the 36-bit Pentago board.
 *
 * WIN_MASKS[i] represents one line of 5 connected positions that would
 * constitute a win.
 * It may also be used for any task requiring to list all five-in-a-row
 * positions, such as an evaluate() function for a bot player.
 */
extern const uint64_t WIN_MASKS[32];


#endif
