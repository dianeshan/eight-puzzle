import copy
import time

# Some default puzzles that can be used

none_misplaced = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

one_misplaced = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 0, 8]]

two_misplaced = [[1, 2, 0],
                 [4, 5, 3],
                 [7, 8, 6]]

few_misplaced = [[0, 2, 3],
                 [1, 5, 6],
                 [4, 7, 8]]

several_misplaced = [[2, 0, 3],
                     [1, 4, 5],
                     [7, 8, 6]]

lots_misplaced = [[2, 3, 1],
                  [8, 7, 4],
                  [0, 6, 5]]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


def main():
    mode = input(
        "Welcome to the Eight Puzzle! Play at your own risk... Type '1' to use a default puzzle or type '2' to input your own puzzle.\n")
    mode_int = int(mode)

    if mode_int == 1:
        puzzle = select_default_puzzle()
        select_algorithm(puzzle)

    if mode_int == 2:
        print("Enter a custom puzzle, using a '0' to represent the blank. Please enter only solvable 8-puzzles. Enter the puzzle by seperating the numbers with a space. Press ENTER when finished.\n")
        row_one = input("Enter first row (ex: 1 2 3): ")
        row_two = input("Enter second row (ex: 4 5 6): ")
        row_three = input("Enter third row (ex: 7 8 0): ")

        print("\n")

        # splits each line of input into a list
        # https://www.w3schools.com/python/ref_string_split.asp
        row_one = row_one.split()
        row_two = row_two.split()
        row_three = row_three.split()

        # turn each string in each row into an integer
        for i in range(3):
            row_one[i] = int(row_one[i])
            row_two[i] = int(row_two[i])
            row_three[i] = int(row_three[i])

        # put the three rows together into one array to create the puzzle
        the_puzzle = [row_one, row_two, row_three]
        select_algorithm(the_puzzle)

    return

# node class which stores the puzzle, the depth, the heuristic, 4 children (since the maximum number of options for moves is 4), and whether or not it is expanded
class node:
    def __init__(self, puzzle, heuristic, depth):
        self.puzzle = puzzle
        self.heuristic = heuristic
        self.depth = depth
        self.ch1 = None
        self.ch2 = None
        self.ch3 = None
        self.ch4 = None
        self.expanded = False


# select desired default puzzle to be used
def select_default_puzzle():
    selected_puzzle = input(
        "Please select your desired puzzle:\n(1) None misplaced\n(2) One misplaced\n(3) Two misplaced\n(4) Few misplaced\n(5) Several misplaced\n(6) Lots misplaced\n")

    if selected_puzzle == "1":
        print("None misplaced selected\n")
        return none_misplaced
    elif selected_puzzle == "2":
        print("One misplaced selected\n")
        return one_misplaced
    elif selected_puzzle == "3":
        print("Two misplaced selected\n")
        return two_misplaced
    elif selected_puzzle == "4":
        print("Few misplaced selected\n")
        return few_misplaced
    elif selected_puzzle == "5":
        print("Several misplaced selected\n")
        return several_misplaced
    elif selected_puzzle == "6":
        print("Lots misplaced selected\n")
        return lots_misplaced


# select search algorithm to use
def select_algorithm(puzzle):
    algorithm = input(
        "Select a search algorithm:\n(1) Uniform Cost Search\n(2) A* with the Misplaced Tile heuristic\n(3) A* with the Manhattan Distance heuristic\n")
    queueing_function = int(algorithm)

    if queueing_function == 1:
        print("Uniform cost selected\n")
    elif queueing_function == 2:
        print("Misplaced tile selected\n")
    elif queueing_function == 3:
        print("Manhattan distance selected\n")

    # running the search algorithm based off chosen algorithm
    print(generalsearch(puzzle, queueing_function))

# calculate the heuristic based on the queueing function
def calculate_heuristic(queueing_function, problem):
    if queueing_function == 1:
        heuristic = 0
    elif queueing_function == 2:
        heuristic = misplaced_tile(problem)
    elif queueing_function == 3:
        heuristic = manhattan_distance(problem)

    return heuristic


# main "driver" program from pseudocode in slides
def generalsearch(problem, queueing_function):

    start = time.perf_counter()

    nodes_visted = -1  # count of nodes visited
    q_size = 0  # queue size
    max_q_size = 0  # maximum queue size
    q = []  # for the queue
    visited = []  # all the puzzles that have been visited already

    # get the heuristic from the queueing function and the problem
    heuristic = calculate_heuristic(queueing_function, problem)

    # Make the starting node
    # Set the heuristic to the previously calculated heuristic and the depth to 0
    nodes = node(problem, heuristic, 0)

    # add the node to the queue and the puzzle to the visited array
    q.append(nodes)
    visited.append(nodes.puzzle)

    # increase the size of the queue by 1 and the max queue size by 1
    q_size += 1
    max_q_size += 1

    # keep going through the loop until we have solved the puzzle
    while True:

        # need to sort queue for lowest h(n) + g(n)
        if queueing_function != 1:
            # used https://docs.python.org/3/howto/sorting.html for how to sort
            # we first sort by heuristic + depth and then sort by depth
            q = sorted(q, key=lambda node: (
                node.heuristic + node.depth, node.depth))

        # if the queue is empty, then we failed
        if len(q) == 0:
            return "Awh shucks we failed!"

        # remove the first node in the queue
        n = q.pop(0)

        # if we haven't expanded yet on this node then increase nodes_visited
        # decrease the queue size by 1 and set expanded to be true
        if n.expanded is False:
            nodes_visted += 1
            n.expanded = True
        q_size -= 1

        # if we achieve the goal state, print it out, along with some stats!
        if goal_test(n.puzzle):
            end = time.perf_counter()
            return("\nYAY! We solved the puzzle!\nSolution depth was: " + str(n.depth) + "\nNumber of nodes expanded: " + str(nodes_visted) + "\nMax queue size: " + str(max_q_size) + "\nThe amount of time taken was: " + str(end - start))

        # shows the cost to goal and the heuristic each time along with the corresponding puzzle
        print('The best state to expand with a g(n) = ' + str(n.depth) + ' and h(n) = ' + str(n.heuristic)
              + ' is...')
        print_puzzle(n.puzzle)

        # expand through all possible states of node and put the states into the children of new node
        expanded_node = expand(n, visited)

        children = [expanded_node.ch1, expanded_node.ch2,
                    expanded_node.ch3, expanded_node.ch4]

        # goes through the children and calculates the heuristic
        for i in children:
            if i is not None:
                i.heuristic = calculate_heuristic(queueing_function, i.puzzle)

                # Add the child node to the queue and to the visited array if it is not none
                q.append(i)
                visited.append(i.puzzle)
                q_size += 1

        # Check to see if the queue size is bigger than the max queue size
        if q_size > max_q_size:
            max_q_size = q_size


# Expands through all possible states of puzzle passed in
def expand(n, visited):

    row = 0
    col = 0

    # first look for where 0 is in the current state
    for i in range(len(n.puzzle)):
        for j in range(len(n.puzzle)):
            if n.puzzle[i][j] == 0:
                row = i
                col = j
                break

    # find all possible moves for the blank to move
    # order is: left -> right -> up -> down (follows orders in slides)
    # the swaps in each of these if branches comes from: https://www.w3resource.com/python-exercises/python-basic-exercise-91.php
    # copy resource: https://docs.python.org/3/library/copy.html

    # if the column is not 0 (first column), then we know that we can go to the left
    if col > 0:
        # do a deep copy of the puzzle and save it into a left variable then do a swap
        left = copy.deepcopy(n.puzzle)

        left[row][col], left[row][col - 1] = left[row][col - 1], left[row][col]

        # if the new puzzle has not been visited before, then add it as a child and create a new node
        # initialize it with the left puzzle, heuristic as 0 (to be calculated later), and set the depth as parent's depth + 1
        if left not in visited:
            n.ch1 = node(left, 0, n.depth + 1)

    # if the column is not the last column in the puzzle, then we know that we can go to the right
    if col < len(n.puzzle) - 1:
        # do a deep copy of the puzzle and save it into a right variable then do a swap
        right = copy.deepcopy(n.puzzle)

        right[row][col], right[row][col +
                                    1] = right[row][col + 1], right[row][col]

        if right not in visited:
            n.ch2 = node(right, 0, n.depth + 1)

    # if the row is not 0 (first row), then we know that we can go up
    if row > 0:
        # do a deep copy of the puzzle and save it into an up variable then do a swap
        up = copy.deepcopy(n.puzzle)

        up[row][col], up[row - 1][col] = up[row - 1][col], up[row][col]

        if up not in visited:
            n.ch3 = node(up, 0, n.depth + 1)

    # if the row is not the last row in the puzzle then we can go down
    if row < len(n.puzzle) - 1:
        # do a deep copy of the puzzle and save it into a down variable then do a swap
        down = copy.deepcopy(n.puzzle)

        down[row][col], down[row + 1][col] = down[row + 1][col], down[row][col]

        if down not in visited:
            n.ch4 = node(down, 0, n.depth + 1)

    return n


# count the number of misplaced tiles (not including the blank)
def misplaced_tile(problem):
    count = 0

    for i in range(len(problem)):
        for j in range(len(problem)):
            if (problem[i][j] != goal_state[i][j] and problem[i][j] != 0):
                count += 1

    return count


# the sum of the distances from the current state to the goal state for each tile (not including the blank)
def manhattan_distance(problem):
    total_distance = 0
    row = 0
    col = 0
    goal_row = 0
    goal_col = 0

    for i in range(1, 9):
        for j in range(len(problem)):
            for k in range(len(problem)):
                if (problem[j][k] == i):
                    row = j
                    col = k
                if (goal_state[j][k] == i):
                    goal_row = j
                    goal_col = k

        # https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/
        distance = abs(row - goal_row) + abs(col - goal_col)
        total_distance = total_distance + distance

    return total_distance


# check to see if we have reached the goal state
def goal_test(puzzle):
    if puzzle == goal_state:
        return True
    return False

# function to print out the puzzle
def print_puzzle(puzzle):
    for i in range(3):
        print(puzzle[i])


if __name__ == "__main__":
    main()
