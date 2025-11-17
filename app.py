import streamlit as st
import numpy as np
import pandas as pd 
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Import all functions from the utility file
from apputil import (
    update_board, 
    recursive_game_of_life, 
    knapsack, 
    knapsack_with_items
)

# --- Global Configuration ---
BOARD_SIZE = 10 
st.set_page_config(layout="wide", page_title="Week 12 Assignments")
st.write('# 💻 Week 12: Advanced Python Assignments')

# --- Section 1: Exercise 1: Rules of Conway's Game of Life ---
st.header("1. Exercise 1: Understanding Conway's Game of Life")

st.markdown("""
The Game of Life is a zero-player game, meaning its evolution is determined by its initial state, requiring no further input. It follows four simple rules:

1.  **Underpopulation:** Any live cell with fewer than two live neighbors dies (as if by loneliness).
2.  **Survival:** Any live cell with two or three live neighbors lives on to the next generation.
3.  **Overpopulation:** Any live cell with more than three live neighbors dies (as if by overpopulation).
4.  **Reproduction:** Any dead cell with exactly three live neighbors becomes a live cell (as if by reproduction).
""")
st.markdown("---")

# --- Section 2: Exercise 2 & Bonus 3: Game of Life Simulation ---
st.header(f"2. Exercise 2 & Bonus 3: Game of Life Simulation ({BOARD_SIZE}x{BOARD_SIZE} Board)")

st.subheader("Exercise 2: Iterative Game Update (`update_board`)")
st.markdown("""
This function uses **NumPy array manipulation** (padding, shifting, and vectorized boolean logic) to efficiently calculate the next state of the board in a single, non-recursive step. This approach is highly performant compared to using nested Python loops.
""")

st.subheader("Bonus Exercise 3: Recursive Game of Life (`recursive_game_of_life`)")
st.markdown("""
This function solves the Game of Life using **recursion**. It works by defining a base case (when the step count reaches zero) and a recursive step where it calls the `update_board` function and then calls *itself* with the updated board and one fewer step remaining.
""")

# Initialize or reset the random game board
if 'game_board' not in st.session_state:
    st.session_state['game_board'] = np.random.randint(2, size=(BOARD_SIZE, BOARD_SIZE))

# --- Controls for Game of Life ---
col1, col2 = st.columns([1, 1])

with col1:
    sim_mode = st.radio("Select Implementation Mode:", 
                        ('Iterative (Ex 2)', 'Recursive (Bonus 3)'), 
                        index=0, 
                        key='sim_mode')
with col2:
    n_steps = st.number_input("Number of steps to run:", 
                              value=5, 
                              step=1, 
                              min_value=1,
                              key='n_steps', 
                              format="%d")

# Create a container for the plot to update dynamically
plot_placeholder = st.empty()


if st.button("Run Simulation", key='run_sim'):
    if sim_mode == 'Iterative (Ex 2)':
        st.info(f"Running **Iterative** simulation for {n_steps} steps...")
        current_board = st.session_state['game_board'].copy()
        
        # Iterative Loop (Ex 2 demonstration)
        for step in range(n_steps):
            current_board = update_board(current_board)

            # Update visualization
            with plot_placeholder.container():
                st.subheader(f'State at Step {step + 1}')
                fig, ax = plt.subplots(figsize=(5, 5)) 
                sns.heatmap(current_board, 
                            cmap='plasma', 
                            cbar=False, 
                            square=True, 
                            ax=ax,
                            linewidths=.5, 
                            linecolor='black')
                ax.set_xticks([])
                ax.set_yticks([])
                st.pyplot(fig)
                plt.close(fig)

            time.sleep(0.5)

        st.session_state['game_board'] = current_board # Save final state

    elif sim_mode == 'Recursive (Bonus 3)':
        st.info(f"Running **Recursive** simulation for {n_steps} steps...")
        
        # Recursive Call (Bonus 3)
        final_board = recursive_game_of_life(board=st.session_state['game_board'].copy(), n_steps=n_steps)
        st.session_state['game_board'] = final_board # Save final state
        
        # Display the final state from the recursive call
        with plot_placeholder.container():
            st.subheader(f'Final State (after {n_steps} Recursive Steps)')
            fig, ax = plt.subplots(figsize=(5, 5))
            sns.heatmap(final_board, 
                        cmap='plasma', 
                        cbar=False, 
                        square=True, 
                        ax=ax,
                        linewidths=.5,
                        linecolor='black')
            ax.set_xticks([])
            ax.set_yticks([])
            st.pyplot(fig)
            plt.close(fig)

    st.success("Simulation finished!")

if st.button(f"Start New Random {BOARD_SIZE}x{BOARD_SIZE} Board", key='reset_board'):
    st.session_state['game_board'] = np.random.randint(2, size=(BOARD_SIZE, BOARD_SIZE))
    st.rerun()

st.markdown("---")

# --- Section 3: Exercise 4 & Optional: Knapsack Problem ---

st.header("3. Exercise 4 & Optional Challenge: 0/1 Knapsack Problem")

st.subheader("What is the 0/1 Knapsack Problem?")
st.markdown("""
The 0/1 Knapsack Problem is a classic optimization problem. Given a set of items, each with a weight and a value, the goal is to determine the number of each item to include in a collection (the "knapsack") so that the total weight is less than or equal to a given capacity $W$, and the total value is as large as possible.

The **0/1** rule means you can either take an item (1) or not take it (0)—you cannot take a fraction of any item. This problem is solved efficiently here using the **Dynamic Programming** paradigm.
""")

st.subheader("Exercise 4: Dynamic Programming Solution (`knapsack`)")
st.markdown("""
The `knapsack` function builds a 2D table where rows represent items and columns represent capacity. By iteratively checking whether to include or exclude the current item, it fills the table with the maximum value achievable at every possible capacity. The final answer is the bottom-right cell of the table.
""")


# Define example data for the Knapsack problem
KNAPSACK_CAPACITY = 15 
KNAPSACK_WEIGHTS = [10, 20, 30, 15]
KNAPSACK_VALUES = [60, 100, 120, 70]
KNAPSACK_NAMES = ["Laptop", "Books", "Camera", "Headphones"]

st.markdown(f"""
### Sample Data for Solution
Capacity ($W$): **{KNAPSACK_CAPACITY} kg**

| Item Name | Weight (kg) | Value ($) |
| :--- | :---: | :---: |
| {KNAPSACK_NAMES[0]} | {KNAPSACK_WEIGHTS[0]} | {KNAPSACK_VALUES[0]} |
| {KNAPSACK_NAMES[1]} | {KNAPSACK_WEIGHTS[1]} | {KNAPSACK_VALUES[1]} |
| {KNAPSACK_NAMES[2]} | {KNAPSACK_WEIGHTS[2]} | {KNAPSACK_VALUES[2]} |
| {KNAPSACK_NAMES[3]} | {KNAPSACK_WEIGHTS[3]} | {KNAPSACK_VALUES[3]} |
""")

if st.button("Solve Knapsack Problem (Ex 4 & Optional)", key='solve_knapsack'):
    
    # --- Step 1: Calculate Max Value and get the DP Table (Exercise 4) ---
    st.subheader("Max Value Result (Exercise 4)")
    with st.spinner("Calculating maximum value and DP table..."):
        # Get the full DP table from the knapsack function
        dp_table = knapsack(KNAPSACK_CAPACITY, KNAPSACK_WEIGHTS, KNAPSACK_VALUES, return_table=True)
        max_val = dp_table[-1][-1]
        st.success(f"The maximum total value achievable is: **${max_val}**")

    # --- Step 2: Show the Mathematical Calculation (The DP Table) ---
    st.subheader("Mathematical Calculation: Dynamic Programming Table")
    st.markdown(f"""
    With a capacity $W=15$, the table has **16 columns** (0 to 15). Notice that only the 'Laptop' and 'Headphones' items could possibly fit in this smaller knapsack.
    """)
    
    # Prepare the DataFrame for display
    item_labels = ["No Item"] + [f"{name} (W={w}, V={v})" for name, w, v in zip(KNAPSACK_NAMES, KNAPSACK_WEIGHTS, KNAPSACK_VALUES)]
    capacity_labels = [f"Cap {i}" for i in range(KNAPSACK_CAPACITY + 1)]
    
    df = pd.DataFrame(dp_table, index=item_labels, columns=capacity_labels)
    
    # Highlight the final result cell (bottom right)
    def highlight_max_value(s):
        is_max = pd.Series(data=False, index=s.index)
        is_max.iloc[-1] = True
        return ['background-color: yellow' if is_max.any() else '' for v in s]

    st.dataframe(df.style.apply(highlight_max_value, axis=1), width='stretch')


    # --- Step 3: Track Optimal Items (Optional Challenge) ---
    st.subheader("Optimal Items Result (Optional Challenge)")
    st.markdown("The `knapsack_with_items` function uses the same DP approach but adds a **backtracking** step to identify which specific items led to the maximum value.")
    
    with st.spinner("Determining optimal items..."):
        # Optional Challenge: Track Items (DP + Backtracking)
        items_included, tracked_max_val = knapsack_with_items(KNAPSACK_CAPACITY, KNAPSACK_WEIGHTS, KNAPSACK_VALUES, KNAPSACK_NAMES)
        
        if items_included:
            total_weight = sum([KNAPSACK_WEIGHTS[KNAPSACK_NAMES.index(item)] for item in items_included])
            
            st.info(f"""
            - **Optimal Items:** `{', '.join(items_included)}`
            - **Total Value:** **${tracked_max_val}**
            - **Total Weight Used:** **{total_weight} kg**
            """)
        else:
            st.warning("No items could be included given the capacity.")
