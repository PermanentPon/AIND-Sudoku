import logging
from utils import *

logging.basicConfig(level=logging.ERROR)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # Go over every unit
    for unit in unitlist:
        # Save values of a unit
        unit_values = dict((x, values[x]) for x in unit)
        # Find twins in values for a unit
        seen = set()
        uniq = []
        twins = []
        for x in unit_values.values():
            if x not in seen:
                uniq.append(x)
                seen.add(x)
            elif len(x) == 2:
                twins.append(x)
        # Go over every twin
        if len(twins) > 0:
            for twin in twins:
                twin_peers = []
                # Get all peers for a twin in a unit
                for key, value in unit_values.items():
                    if value != twin:
                        twin_peers.append(key)
                # Go over all peer for a twin
                for twin_peer in twin_peers:
                    # Go over all(2) digits in a twin
                    for character in twin:
                        # Delete digits from peers
                        if len(values[twin_peer]) > 1:
                            assign_value(values, twin_peer, values[twin_peer].replace(character, ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        logging.info(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': logging.info(line)
    logging.info("")

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for key, value in values.items():
        if len(value) == 1:
            for peer in peers[key]:
                assign_value(values, peer, values[peer].replace(value, ''))
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        logging.info("Before eliminate:")
        display(values)
        values = eliminate(values)
        # Use the Only Choice Strategy
        logging.info("Before the Only Choice:")
        display(values)
        values = only_choice(values)
        # Use the Naked Twins Strategy
        logging.info("Before the Naked Twins:")
        display(values)
        values = naked_twins(values)
        logging.info("After the Naked Twins:")
        display(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    min_value = 11
    min_box = ''
    logging.debug(values)
    for key, value in values.items():
        if min_value > len(value) and len(value) > 1:
            min_value = len(value)
            min_box = key
            logging.debug(min_value, key)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    logging.debug(min_box)
    logging.debug(values[min_box])
    for i in values[min_box]:
        new_sudoku = values.copy()
        new_sudoku[min_box] = i
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        logging.warning('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
