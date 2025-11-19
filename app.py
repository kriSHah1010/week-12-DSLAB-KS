import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def update_board(current_board):
    """
    Executes one step of Conway's Game of Life for the given binary NumPy array.
    Uses periodic (toroidal) boundary conditions.
    """
    rows, cols = current_board.shape
    
    # Initialize the neighbor count array to zeros
    neighbors = np.zeros_like(current_board, dtype=int)
    
    # Count all 8 neighbors using roll with periodic boundaries
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
    updated_board[(current_board == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    updated_board[(current_board == 0) & (neighbors == 3)] = 1
    
    return updated_board, neighbors

def main():
    st.title("Game of Life Debugger")
    st.subheader("Test the specific cases the autograder is checking")
    
    # Test case 1: Cell with 4 neighbors
    st.header("Test 2.2: Cell with 4 neighbors should die")
    st.write("Create a pattern where a cell has exactly 4 live neighbors")
    
    # Create a pattern where center has 4 neighbors
    board_4_neighbors = np.array([
        [1, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ])
    
    st.write("**Initial board (center has 4 neighbors):**")
    st.write(board_4_neighbors)
    
    next_board, neighbors = update_board(board_4_neighbors)
    st.write("**Neighbor counts:**")
    st.write(neighbors)
    st.write("**Next state:**")
    st.write(next_board)
    
    center_survives = next_board[1, 1] == 1
    st.write(f"**Center cell survives:** {center_survives}")
    st.write(f"**Test 2.2 PASS:** {not center_survives}")
    
    # Test case 2: Empty cell with 3 neighbors
    st.header("Test 2.3: Empty cell with 3 neighbors should revive")
    
    board_3_neighbors_empty = np.array([
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 0]
    ])
    
    st.write("**Initial board (center empty with 3 neighbors):**")
    st.write(board_3_neighbors_empty)
    
    next_board, neighbors = update_board(board_3_neighbors_empty)
    st.write("**Neighbor counts:**")
    st.write(neighbors)
    st.write("**Next state:**")
    st.write(next_board)
    
    center_revives = next_board[1, 1] == 1
    st.write(f"**Center cell revives:** {center_revives}")
    st.write(f"**Test 2.3 PASS:** {center_revives}")
    
    # Test case 3: Full 3x3 board
    st.header("Test 2.4: Full 3x3 board → only corners survive")
    
    full_board = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ])
    
    st.write("**Initial full 3x3 board:**")
    st.write(full_board)
    
    next_board, neighbors = update_board(full_board)
    st.write("**Neighbor counts:**")
    st.write(neighbors)
    st.write("**Next state:**")
    st.write(next_board)
    
    expected_result = np.array([
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1]
    ])
    
    st.write("**Expected result (only corners):**")
    st.write(expected_result)
    
    corners_only = np.array_equal(next_board, expected_result)
    st.write(f"**Test 2.4 PASS:** {corners_only}")
    
    # Interactive tester
    st.header("Interactive Tester")
    st.write("Create your own 3x3 board to test:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        a11 = st.checkbox("(0,0)", value=True)
        a12 = st.checkbox("(0,1)", value=True)
        a13 = st.checkbox("(0,2)", value=True)
    
    with col2:
        a21 = st.checkbox("(1,0)", value=True)
        a22 = st.checkbox("(1,1)", value=True)
        a23 = st.checkbox("(1,2)", value=True)
    
    with col3:
        a31 = st.checkbox("(2,0)", value=True)
        a32 = st.checkbox("(2,1)", value=True)
        a33 = st.checkbox("(2,2)", value=True)
    
    custom_board = np.array([
        [a11, a12, a13],
        [a21, a22, a23],
        [a31, a32, a33]
    ], dtype=int)
    
    st.write("**Your custom board:**")
    st.write(custom_board)
    
    if st.button("Test Custom Board"):
        next_board, neighbors = update_board(custom_board)
        st.write("**Neighbor counts:**")
        st.write(neighbors)
        st.write("**Next state:**")
        st.write(next_board)

if __name__ == "__main__":
    main()
