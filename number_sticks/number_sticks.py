#!/usr/bin/env python
"""
Problem Statement:
    Given a formula of the form A + B = C, where A, B, C are natural numbers.
    Compute any possible combinations where the equation MIGHT be valid.

    Rules on modifying the equation:
    1) Each number is created by sticks like an LCD display of sticks.
    2) You can remove or add any segment or stick. Each removal or addition is
       1 move.
    3) The best solution is the one that is a valid equation from the original
       with the least moves.
    4) The input equation does not need to be valid, but all solutions must be.

Sides numbered from bottom going clockwise, for example:

      4
      _
   3 | | 5
   2 | | 6
      -
      1

    7 is across the middle.
"""
import re

# Any optimal solution shouldn't have a single move exceeding this amount.
DEFAULT_MOVE_CUTOFF = 4
# Limit from being abused by silly users.
MAX_VAL = 99999
# Each number is mapped from the digit to a set of "sticks" as above.
STICK_SETS = {
    0: {1, 2, 3, 4, 5, 6},
    1: {2, 3},
    2: {1, 2, 4, 5, 7},
    3: {1, 4, 7, 5, 6},
    4: {3, 7, 5, 6},
    5: {1, 4, 7, 3, 6},
    6: {1, 2, 3, 4, 6, 7},
    7: {4, 5, 6},
    8: {1, 2, 3, 4, 5, 6, 7},
    9: {1, 3, 4, 5, 6, 7},
}
FROM_TO_CACHE = {}


def compute_moves(from_val: int, to_val: int) -> int:
    """
    Compute the number of moves to transform from_val into to_val,
    using sticks of equal length.

    from_val: The number to start with.
    to_val: The number to transform from_val into.

    Returns: The total amount of moves.
    """
    from_sticks, to_sticks = STICK_SETS[from_val], STICK_SETS[to_val]
    sub = len(from_sticks - to_sticks)
    add = len(to_sticks - from_sticks)

    return sub + add


def populate_cache():
    """
    Pre compute all possible moves from any valid digit in base 10 to any other digit
    in accordance to display as sticks.
    """
    for from_val in range(0, 10):
        FROM_TO_CACHE[from_val] = {}
        for to_val in range(0, 10):
            FROM_TO_CACHE[from_val][to_val] = compute_moves(from_val, to_val)


def generate_numbers(positions: int):
    """
    Generator function.

    Generate all possible numbers in a list of form:
        [0, 1, 2], where the number in a list is given by positions.

    Return: One combination of numbers at a time until StopIteration reached.
    """
    if positions < 1:
        raise ValueError("Won't generate numbers below 1 position.")

    for val in range(0, 10 ** positions):
        yield [int(n) for n in list(str(val).zfill(positions))]


def candidate_numbers(target_num: int, move_cutoff: int = DEFAULT_MOVE_CUTOFF):
    """
    Take a target number and find all the candidates with least moves to make a new number.
    Returns a dictionary mapping the possible matches with least moves.
    """
    candidates = []
    candidate_moves = {}
    target_list = [int(n) for n in list(str(target_num))]
    positions = len(target_list)

    for possible in generate_numbers(positions):
        moves = 0
        for from_val, to_val in zip(target_list, possible):
            moves += compute_moves(from_val, to_val)

        # No reason to consider beyond the cutoff
        if moves > move_cutoff:
            continue

        candidate_num = int("".join([str(x) for x in possible]))
        candidates += [candidate_num]
        candidate_moves[candidate_num] = moves

    candidates = sorted(candidates, key=lambda x: candidate_moves[x])
    return candidates, candidate_moves


def find_lowest_sum(val1: int, val2: int, val_sum: int, *, total_cutoff: int = DEFAULT_MOVE_CUTOFF):
    """
    Taking the values of formula:
        a + b = c

    Attempt to find any combination that satisfies:
        a + b = c

    Track all possible solutions and the number of moves required.

    Returns: A list in order of solutions in increasing number of moves.
    """
    first_candidates, first_move_dict = candidate_numbers(val1, 4)
    second_candidates, second_move_dict = candidate_numbers(val2, 4)
    sum_candidates, sum_move_dict = candidate_numbers(val_sum, 4)

    answers, answers_map = [], {}
    for total in sum_candidates:
        for first in first_candidates:
            for second in second_candidates:
                if (first + second) == total:
                    move_total = first_move_dict[first] + second_move_dict[second] + sum_move_dict[total]
                    if move_total > total_cutoff:
                        continue

                    answer = f"{first} + {second} = {total}, takes {move_total} moves."
                    answers += [answer]
                    answers_map[answer] = move_total

    return sorted(answers, key=lambda x: answers_map[x])


def find_lowest_sub(val1: int, val2: int, target_sum: int, *, total_cutoff: int = DEFAULT_MOVE_CUTOFF):
    """
    Taking the values of formula:
        a + b = c

    Attempt to find any combination that satisfies:
        a - b = c

    Track all possible solutions and the number of moves required.
    N.B. 1 will be added to all moves due to swap from + -> -

    Returns: A list in order of solutions in increasing number of moves.
    """
    first_candidates, first_move_dict = candidate_numbers(val1, 4)
    second_candidates, second_move_dict = candidate_numbers(val2, 4)
    sum_candidates, sum_move_dict = candidate_numbers(target_sum, 4)

    answers, answers_map = [], {}
    for total in sum_candidates:
        for first in first_candidates:
            for second in second_candidates:
                if (first - second) == total:
                    # Add one to move total due to changing + -> - in problem
                    move_total = first_move_dict[first] + second_move_dict[second] + sum_move_dict[total] + 1
                    if move_total > total_cutoff:
                        continue

                    answer = f"{first} - {second} = {total}, takes {move_total} moves."
                    answers += [answer]
                    answers_map[answer] = move_total

    return sorted(answers, key=lambda x: answers_map[x])


def main():
    """
    Main entry.
    """
    populate_cache()

    total_cutoff = input("Please input the highest number of total moves allowed. An integer.\n\n")
    try:
        total_cutoff = int(total_cutoff)
        if total_cutoff < 1 or total_cutoff > 20:
            raise ValueError
    except ValueError as exc:
        raise ValueError("Incorrect usage, try again. I couldn't parse your expression.") from exc

    user_expression = input("Write query in form of: x + y = z\n\nExample: 59 + 12 = 98\n\n")
    match = re.match(r'(\d+)\s*[+]\s*(\d+)\s*[=]\s*(\d+)', user_expression)
    if not match or len(match.groups()) != 3:
        raise ValueError("Incorrect usage, try again. I couldn't parse your expression.")

    first = int(match.group(1))
    second = int(match.group(2))
    total = int(match.group(3))
    if first > MAX_VAL or second > MAX_VAL or total > MAX_VAL:
        raise ValueError("Computing the sticks for these high values may be very expensive. Choose lower values.")

    print("Top 25 possible sums with move cost.\n")
    for ind, cand in enumerate(find_lowest_sum(first, second, total, total_cutoff=total_cutoff))[:25]:
        print(cand)

    print("Top 25 Possible subtractions with move cost.\n1 move is taken to change to subtraction.\n")
    for cand in find_lowest_sub(first, second, total, total_cutoff=total_cutoff)[:25]:
        print(cand)


if __name__ == "__main__":
    main()
