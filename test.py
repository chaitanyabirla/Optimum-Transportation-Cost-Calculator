import streamlit as st
import numpy as np

# Define INF for unreachable routes or very high costs
INF = 10**5

# Function to calculate row and column differences
def calculate_differences(grid):
    row_diff = [max(row) - min(row) for row in grid]
    col_diff = [max(col) - min(col) for col in np.transpose(grid)]
    return row_diff, col_diff

# Function to solve the transportation problem using Vogel's approximation
def solve_transportation_problem(grid, supply, demand):
    ans = 0
    n, m = len(supply), len(demand)
    
    # Clone inputs to avoid mutation during calculations
    supply = supply[:]
    demand = demand[:]
    grid = [row[:] for row in grid]

    while max(supply) != 0 or max(demand) != 0:
        # Calculate row and column differences
        row_diff, col_diff = calculate_differences(grid)
        max_row_diff = max(row_diff)
        max_col_diff = max(col_diff)

        # Decide whether to process row or column based on maximum difference
        if max_row_diff >= max_col_diff:
            chosen_index = row_diff.index(max_row_diff)
            min_cost = min(grid[chosen_index])
            min_cost_index = grid[chosen_index].index(min_cost)
            allocation = min(supply[chosen_index], demand[min_cost_index])
            ans += allocation * min_cost
            supply[chosen_index] -= allocation
            demand[min_cost_index] -= allocation

            # Invalidate row or column based on exhausted supply or demand
            if demand[min_cost_index] == 0:
                for i in range(n):
                    grid[i][min_cost_index] = INF
            if supply[chosen_index] == 0:
                grid[chosen_index] = [INF] * m
        else:
            chosen_index = col_diff.index(max_col_diff)
            min_cost = min(row[chosen_index] for row in grid)
            min_cost_row = next(i for i, row in enumerate(grid) if row[chosen_index] == min_cost)
            allocation = min(supply[min_cost_row], demand[chosen_index])
            ans += allocation * min_cost
            supply[min_cost_row] -= allocation
            demand[chosen_index] -= allocation

            # Invalidate row or column based on exhausted supply or demand
            if demand[chosen_index] == 0:
                for i in range(n):
                    grid[i][chosen_index] = INF
            if supply[min_cost_row] == 0:
                grid[min_cost_row] = [INF] * m

    return ans

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 2em;
            color: #4CAF50;
            text-align: center;
        }
        .input-section {
            margin-top: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title and instructions
st.markdown('<h1 class="title">Optimal Transportation Cost Calculator</h1>', unsafe_allow_html=True)

# Input for supply and demand
st.markdown('<div class="input-section">', unsafe_allow_html=True)
n = st.number_input("Number of Supply Points", min_value=1, step=1, value=3)
m = st.number_input("Number of Demand Points", min_value=1, step=1, value=4)
supply_input = st.text_input("Supply amounts (comma-separated)", value="300, 400, 500")
demand_input = st.text_input("Demand amounts (comma-separated)", value="250, 350, 400, 200")

# Parse and validate supply and demand inputs
try:
    supply = list(map(int, supply_input.split(",")))
    demand = list(map(int, demand_input.split(",")))
    if len(supply) != n or len(demand) != m:
        st.error(f"Error: Supply and demand entries must match the specified number of points.")
        st.stop()
except ValueError:
    st.error("Supply and demand values must be integers, separated by commas.")
    st.stop()

# Input for cost matrix
st.markdown('<div class="input-section">', unsafe_allow_html=True)
matrix_input = st.text_area("Cost Matrix (comma-separated rows)", value="8, 6, 10, 9\n9, 12, 13, 7\n14, 9, 16, 5")
try:
    grid = [list(map(int, row.split(","))) for row in matrix_input.splitlines() if row]
    if len(grid) != n or any(len(row) != m for row in grid):
        st.error(f"Cost matrix must have {n} rows and {m} columns.")
        st.stop()
except ValueError:
    st.error("Matrix values must be integers with rows separated by newlines.")
    st.stop()
st.markdown('</div>', unsafe_allow_html=True)

# Button to calculate optimal cost
if st.button("Calculate Optimal Cost"):
    result = solve_transportation_problem(grid, supply, demand)
    st.success(f"The Basic Feasible Solution is: ₹{result}")
