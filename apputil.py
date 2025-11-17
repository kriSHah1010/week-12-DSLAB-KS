import numpy as np
import time
import seaborn as sns
import matplotlib.pyplot as plt

# --- Exercise 2: Conway's Game of Life Step ---

def update_board(current_board):
    """
    Executes one step of Conway's Game of Life on a binary NumPy array (1=live, 0=dead). 
    Uses array manipulation with 'wrap' padding for toroidal (wrapping) boundary conditions.
    """
    # Create a copy for the updated state to avoid changing the board mid-calculation
    updated_board = current_board.copy()
    rows, cols = current_board.shape

    # Pad the board using 'wrap' (toroidal) mode to correctly count neighbors at the edges
    padded_board = np.pad(current_board, 1, mode='wrap')

    # Initialize neighbor count array
    neighbors = np.zeros_like(padded_board, dtype=int)

    # Calculate neighbor sum efficiently by summing 8 shifted versions of the padded array
    for i in range(3):
        for j in range(3):
            # Exclude the current cell itself (i=1, j=1 corresponds to a 0 shift)
            if i != 1 or j != 1:
                # np.roll shifts the entire array efficiently:
                neighbors += np.roll(np.roll(padded_board, i - 1, axis=0), j - 1, axis=1)

    # Extract the relevant center portion (un-pad it)
    neighbors = neighbors[1:rows+1, 1:cols+1]

    # --- Apply the Game of Life Rules (Vectorized) ---

    # 1 & 3. Death: Live cells (==1) die if neighbors < 2 (under) or neighbors > 3 (over)
    live_cells_to_die = (current_board == 1) & ((neighbors < 2) | (neighbors > 3))
    updated_board[live_cells_to_die] = 0

    # 4. Birth: Dead cells (==0) become live if neighbors == 3 (reproduction)
    dead_cells_to_live = (current_board == 0) & (neighbors == 3)
    updated_board[dead_cells_to_live] = 1

    return updated_board

# --- Bonus Exercise 3: Recursive Game of Life ---

def recursive_game_of_life(board=None, n_steps=10):
    """
    Plays Conway's Game of Life recursively for a given number of steps.
    """
    # 1. Initialization
    if board is None:
        board = np.random.randint(2, size=(10, 10))

    # 2. Base Case: Stop recursion when steps are complete
    if n_steps <= 0:
        return board

    # 3. Recursive Step: Update the board and call itself with one less step
    next_board = update_board(board)
    return recursive_game_of_life(board=next_board, n_steps=n_steps - 1)


# --- Exercise 4 & Optional Challenge: Knapsack Problem ---

def knapsack(W, weights, values, return_table=False):
    """
    Solves the 0/1 Knapsack Problem using Dynamic Programming.

    Parameters
    ----------
    W : int
        The maximum weight capacity of the knapsack.
    weights : list or array
        The weight of each item.
    values : list or array
        The value of each item.
    return_table : bool, optional
        If True, returns the full DP table instead of just the max value.

    Returns
    -------
    int or list[list[int]]
        The maximum value or the full DP table.
    """
    n = len(values)
    # 1. Initialize the DP table: (n+1) rows for items, (W+1) columns for capacity.
    # table[i][j] stores the max value with first i items and capacity j.
    table = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # 2. Fill the DP table row by row (i: current item index, j: current capacity)
    for i in range(1, n + 1):
        for j in range(1, W + 1):
            # Item indices in weights/values lists are (i-1)
            item_weight = weights[i-1]
            item_value = values[i-1]

            # Case 1: If the current item's weight fits within the current capacity (j)
            if item_weight <= j:
                # Option A (Include the item):
                # Value is the item's value + the max value from the previous row (i-1)
                # using the remaining capacity (j - item_weight).
                value_with_item = item_value + table[i-1][j - item_weight]
                
                # Option B (Exclude the item):
                # Value is simply the max value from the previous row (i-1) at the same capacity (j).
                value_without_item = table[i-1][j]
                
                # Store the best choice (max of Option A and Option B)
                table[i][j] = max(value_with_item, value_without_item)

            # Case 2: Item does not fit (item_weight > j)
            else:
                # Value must be the same as the previous item's max value at this capacity.
                table[i][j] = table[i-1][j]
    
    # Check if the user wants the full table or just the max value
    if return_table:
        return table
    
    # The maximum value is at the bottom-right cell
    return table[n][W]


def knapsack_with_items(W, weights, values, names):
    """
    Solves the 0/1 Knapsack problem using DP and tracks the included items (Optional Challenge).
    """
    n = len(values)
    # 1. Initialize and fill the DP table (same as knapsack function)
    table = knapsack(W, weights, values, return_table=True)

    # --- 2. Backtracking to find included items ---
    final_max_value = table[n][W]
    included_items = []
    current_value = final_max_value
    current_capacity = W

    # Iterate backward from the last item (n) to the first (1)
    for i in range(n, 0, -1):
        # Check if the max value for this item (i) is different from the max value
        # without this item (i-1). If they differ, item 'i' was included.
        if current_value != table[i-1][current_capacity]:
            # Item i was included. Record its name and update the state.
            included_items.append(names[i-1])

            # Update the required residual value and capacity
            current_value -= values[i-1]
            current_capacity -= weights[i-1]

    included_items.reverse() # Reverse to show items in original order
    return included_items, final_max_value


def show_game(game_board, n_steps=10, pause=0.5):
    """
    Placeholder for the Jupyter Notebook testing function.
    """
    pass
