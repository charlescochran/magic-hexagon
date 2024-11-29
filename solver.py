# Indices layout:
#                   _____
#                  /     \
#            _____/   2   \_____
#           /     \       /     \
#     _____/   1   \_____/   6   \_____
#    /     \       /     \       /     \
#   /   0   \_____/   5   \_____/  11   \
#   \       /     \       /     \       /
#    \_____/   4   \_____/  10   \_____/
#    /     \       /     \       /     \
#   /   3   \_____/   9   \_____/  15   \
#   \       /     \       /     \       /
#    \_____/   8   \_____/  14   \_____/
#    /     \       /     \       /     \
#   /   7   \_____/  13   \_____/  18   \
#   \       /     \       /     \       /
#    \_____/  12   \_____/  17   \_____/
#          \       /     \       /
#           \_____/  16   \_____/
#                 \       /
#                  \_____/

# Magic constant (every row sums to this)
M = 38
# A set of all the numbers!
NUMS = set(range(1, 20))
# Indices of the outer ring (in clockwise order)
OUTER_INDICES = [0, 1, 2, 6, 11, 15, 18, 17, 16, 12, 7, 3]
# Indices of the inner ring in (clockwise order)
INNER_INDICES = [4, 5, 10, 14, 13, 8]

def solve(ring=[]):
    # Recursively create outer rings, passing valid ones (where all 3-rows add
    # to M) to solve_inner() to finish them.
    if not ring:
        # Start with each number in cell 0.
        for first in NUMS:
            solve([first])
        return
    # Given the first of three numbers in this outer edge, choose an available second.
    for second in NUMS - set(ring):
        # Calculate the third number necessary to complete the magic sum.
        third = M - ring[-1] - second
        # If we've completed the outer ring, create a hive from it and continue to solve.
        if len(ring) == 11 and third == ring[0]:
            hive = [0] * 19
            for i, n in zip(OUTER_INDICES, ring + [second]):
                hive[i] = n
            solve_inner(hive)
        # Otherwise, if the third is valid, recurse to the next outer edge.
        elif third < 20 and third not in ring + [second]:
            solve(ring + [second, third])

def solve_inner(hive):
    # Given a hive with the outer ring filled in, complete it with all possible
    # valid inner rings and center values.
    # Choose each available number for cell 4.
    outer_nums = set(hive)
    for n4 in NUMS - outer_nums:
        # Fill in the inner ring, completing the magic sums in the 4-rows.
        n5 = M - hive[3] - n4 - hive[6]
        n10 = M - hive[1] - n5 - hive[15]
        n14 = M - hive[6] - n10 - hive[17]
        n13 = M - hive[15] - n14 - hive[12]
        n8 = M - hive[17] - n13 - hive[3]
        # Ensure cell 8 is the same when calculated the other way.
        assert n8 == M - hive[1] - n4 - hive[12]
        # Reject inner rings using duplicate/unavailable numbers.
        ring = (n4, n5, n10, n14, n13, n8)
        inner_nums = set(ring)
        center_nums = NUMS - outer_nums - inner_nums
        if len(inner_nums) != 6 or len(center_nums) != 1:
            continue
        # Fill out the rest of the hive.
        hive2 = hive.copy()
        for i, n in zip(INNER_INDICES, ring):
            hive2[i] = n
        hive2[9] = center_nums.pop()  # The center must be the only remaining number.
        # Ensure the 5-rows add up.
        assert hive2[0] + hive2[4] + hive2[9] + hive2[14] + hive2[18] == M
        assert hive2[2] + hive2[5] + hive2[9] + hive2[13] + hive2[16] == M
        assert hive2[7] + hive2[8] + hive2[9] + hive2[10] + hive2[11] == M
        # We have a valid solution: print it!
        print(hive2)

solve()
