import numpy as np
from IPython.display import clear_output
import time
import seaborn as sns
import matplotlib.pyplot as plt

# --- Exercise 2: Iterative Game of Life Update ---

def update_board(current_board):
    """
    Executes one step of Conway's Game of Life for the given binary NumPy array.
    Uses periodic (toroidal) boundary conditions.

    Parameters
    ----------
    current_board : numpy.ndarray
        A binary array (0s and 1s) representing the current state of the board.

    Returns
    -------
    numpy.ndarray
        The board after one step of the Game of Life.
    """
    rows, cols = current_board.shape
    
    # Initialize the neighbor count array to zeros
    neighbors = np.zeros_like(current_board, dtype=int)
    
    # Count all 8 neighbors using roll with periodic boundaries
    # This approach correctly handles toroidal boundaries
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # Skip the center cell itself
            # Roll the board and add to neighbor count
            rolled = np.roll(current_board, dx, axis=0)
            rolled = np.roll(rolled, dy, axis=1)
            neighbors += rolled
    
    # Create a copy for the updated state
    updated_board = np.zeros_like(current_board)
    
    # Apply Conway's Game of Life rules:
    # 1. Any live cell with 2 or 3 live neighbors survives
    # 2. Any dead cell with exactly 3 live neighbors becomes alive
    # 3. All other live cells die, all other dead cells stay dead
    
    # Live cells survive if they have exactly 2 or 3 neighbors
    updated_board[(current_board == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    
    # Dead cells become alive if they have exactly 3 neighbors
    updated_board[(current_board == 0) & (neighbors == 3)] = 1
    
    return updated_board

def show_game(game_board, n_steps=10, pause=0.5):
    """
    Show `n_steps` of Conway's Game of Life (for notebook testing).
    """
    for step in range(n_steps):
        clear_output(wait=True)

        # update board
        game_board = update_board(game_board)

        # show board
        sns.heatmap(game_board, cmap='plasma', cbar=False, square=True)
        plt.title(f'Board State at Step {step + 1}')
        plt.show()

        # wait for the next step
        if step + 1 < n_steps:
            time.sleep(pause)

# --- Bonus Exercise 3: Recursive Game of Life ---

def recursive_game_of_life(board=None, n_steps=10):
    """
    Plays Conway's Game of Life recursively for a given number of steps.
    """
    # 1. Initialization and Base Case Check
    if board is None:
        # Initial call: Create a new random 10x10 board
        board = np.random.randint(2, size=(10, 10))

    if n_steps <= 0:
        # Base Case: Stop recursion when steps are complete
        return board

    # 2. Recursive Step
    # a. Update the board state for one step
    next_board = update_board(board)

    # b. Recursively call the function with the updated board and one less step
    return recursive_game_of_life(board=next_board, n_steps=n_steps - 1)

# --- Exercise 4: 0/1 Knapsack Problem (Dynamic Programming) ---

def knapsack(W, weights, values, full_table=False, return_table=False):
    """
    Solves the 0/1 Knapsack problem using Dynamic Programming.
    Finds the maximum value that can be placed in a knapsack of capacity W.

    Parameters
    ----------
    W : int
        The maximum weight capacity of the knapsack.
    weights : list
        List of weights of the items.
    values : list
        List of values of the items.
    full_table : bool, optional
        A deprecated argument, retained for compatibility.
    return_table : bool, optional
        If True, the full DP table is returned instead of just the max value.

    Returns
    -------
    int or list[list[int]]
        The maximum achievable value, or the full DP table.
    """
    # Get the total number of items to be considered (n).
    n = len(values)
    # Initialize a 2D table (n+1 rows for items, W+1 columns for capacity) with all zeros.
    # table[i][j] will store the max value using the first 'i' items with capacity 'j'.
    table = [[0 for x in range(W + 1)] for x in range(n + 1)]

    # Initialize the DP table: first row and first column should be 0
    for i in range(n + 1):
        for j in range(W + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif weights[i-1] <= j:
                # Value if item IS included: item's value + max value from previous item (i-1) with remaining capacity (j - weight).
                value_with_item = values[i-1] + table[i-1][j - weights[i-1]]
                # Value if item is EXCLUDED: max value from previous item (i-1) with the same capacity (j).
                value_without_item = table[i-1][j]
                
                # The cell's value is the maximum of the two options.
                table[i][j] = max(value_with_item, value_without_item)
            else:
                # If the current item's weight is greater than the current capacity (j),
                # The item cannot be included. The maximum value is the same as the previous item's value at this capacity.
                table[i][j] = table[i-1][j]

    # Return the full table if requested, otherwise return the maximum value (bottom-right cell).
    if return_table or full_table:
        return table

    return table[n][W]

# --- Optional Challenge: Knapsack with Item Tracking (DP + Backtracking) ---

def knapsack_with_items(W, weights, values, names):
    """
    Solves the 0/1 Knapsack problem, finds the maximum value, and tracks the included items.
    """
    n = len(values)
    
    # 1. Build the DP Table (uses the knapsack function logic internally)
    table = knapsack(W, weights, values, return_table=True)
    
    # --- 2. Backtracking to find included items ---
    
    # Start at the bottom-right cell (max value)
    max_value = table[n][W]
    included_items = []
    current_capacity = W
    
    # Iterate backward from the last item (n) to the first (1)
    for i in range(n, 0, -1):
        # If the value at table[i][current_capacity] is DIFFERENT from table[i-1][current_capacity],
        # it means item 'i' was included in the optimal solution for this capacity.
        if table[i][current_capacity] != table[i-1][current_capacity]:
            # Item 'i' (index i-1) was included
            included_items.append(names[i-1])
            
            # Update the capacity by subtracting the weight of the included item
            current_capacity = current_capacity - weights[i-1]
            
    # The items are found in reverse order of processing, so reverse the list for readability
    included_items.reverse()
    
    return included_items, max_value
