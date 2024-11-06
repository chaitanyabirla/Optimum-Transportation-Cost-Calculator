import streamlit as st
import numpy as np

# Define INF for unreachable routes or very high costs
INF = 10**5

# Function to get difference arrays for row and column
def Diff_step(grid): 
  rowdiff=[]# Compute the difference step in the x-direction
  coldiff=[]# ''''----Opposite
  for i in range(len(grid)):
     arr = grid[i][:]
     arr.sort()
     rowdiff.append(arr[1]-arr[0])# finding difference
  
  col=0
  while col < len(grid[0]):
    arr=[]

    for i in range(len(grid)):
      arr.append(grid[i][col])#pick up first values from each row
    arr.sort()
    col += 1
    coldiff.append(arr[1]-arr[0])# finding difference columnwise
  return rowdiff,coldiff

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 2em;
            color: #12984F;
            text-align: center;
            margin-top: -50px;
        }
        .input-section {
            margin-top: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .result {
            font-size: 1.5em;
            color: #12984F;
            text-align: center;
        }
        .stButton>button {
            width: 100%;
            height: 50px;
            font-size: 1.2em;
            background-color: #12984F;
            color: white;
            border-radius: 10px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #12984F;
        }
    </style>
""", unsafe_allow_html=True)

# Title and instructions
st.markdown('<h1 class="title">Optimal Transportation Cost Calculator</h1>', unsafe_allow_html=True)
st.write("Enter the required details below to calculate the optimal transportation cost using Vogel's approximation method.")

# Step 1: Input for supply and demand points
with st.container():
    cols = st.columns(2)
    n = cols[0].number_input("Number of Supply Points:", min_value=1, step=1)
    m = cols[1].number_input("Number of Demand Points:", min_value=1, step=1)

# Step 2: Input for supply and demand amounts in comma-separated format
#st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.subheader("Supply and Demand Inputs")
cols = st.columns(2)
supply_input = cols[0].text_input("Supply amounts (comma-separated):", value="20, 30, 50")
demand_input = cols[1].text_input("Demand amounts (comma-separated):", value="10, 40, 30, 20")

# Parse and validate supply and demand inputs
try:
    supply = list(map(int, supply_input.split(",")))
    demand = list(map(int, demand_input.split(",")))
    if len(supply) != n or len(demand) != m:
        st.error(f"Error: Supply and demand entries must match the specified number of supply ({n}) and demand ({m}) points.")
        st.stop()
except ValueError:
    st.error("Error: Supply and demand values must be integers, separated by commas.")
    st.stop()

st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Input for cost matrix as text area
#st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.subheader("Cost Matrix Input")
st.write("Enter the cost matrix with rows separated by newlines and values separated by commas.")
matrix_input = st.text_area("Cost Matrix", value="8, 6, 10, 9\n9, 12, 13, 7\n14, 9, 16, 5")

# Parse and validate cost matrix
try:
    grid = [list(map(int, row.split(","))) for row in matrix_input.splitlines() if row]
    if len(grid) != n or any(len(row) != m for row in grid):
        st.error(f"Error: Cost matrix must have {n} rows and {m} columns.")
        st.stop()
except ValueError:
    st.error("Error: Cost matrix values must be integers, with rows separated by newlines and values by commas.")
    st.stop()

st.markdown('</div>', unsafe_allow_html=True)

# Display and confirm the input data
st.write("### Input Data Confirmation")
st.write("**Supply:**", supply)
st.write("**Demand:**", demand)
st.write("**Cost Matrix:**")
st.table(grid)

# Main logic to solve the transportation problem
def solve_transportation_problem(grid, supply, demand, n, m):
    ans = 0
    while max(supply) != 0 or max(demand) != 0:
        row, col = Diff_step(grid)
        maxi1 = max(row)
        maxi2 = max(col)

        if maxi1 >= maxi2:
            for ind, val in enumerate(row):
                if val == maxi1:
                    mini1 = min(grid[ind])
                    for ind2, val2 in enumerate(grid[ind]):
                        if val2 == mini1:
                            mini2 = min(supply[ind], demand[ind2])
                            ans += mini2 * mini1
                            supply[ind] -= mini2
                            demand[ind2] -= mini2
                            if demand[ind2] == 0:
                                for r in range(n):
                                    grid[r][ind2] = INF
                            else:
                                grid[ind] = [INF for _ in range(m)]
                            break
                    break
        else:
            for ind, val in enumerate(col):
                if val == maxi2:
                    mini1 = INF
                    for j in range(n):
                        mini1 = min(mini1, grid[j][ind])
                    for ind2 in range(n):
                        if grid[ind2][ind] == mini1:
                            mini2 = min(supply[ind2], demand[ind])
                            ans += mini2 * mini1
                            supply[ind2] -= mini2
                            demand[ind] -= mini2
                            if demand[ind] == 0:
                                for r in range(n):
                                    grid[r][ind] = INF
                            else:
                                grid[ind2] = [INF for _ in range(m)]
                            break
                    break
    return ans

# Calculate and display result in a formal popup
if st.button("Calculate Optimal Cost"):
    grid_copy = [row[:] for row in grid]
    supply_copy = supply[:]
    demand_copy = demand[:]
    result = solve_transportation_problem(grid_copy, supply_copy, demand_copy, n, m)

    # Formal success message without balloons
    st.success(f"Calculation Complete! 🎯 The Basic Feasible Solution is: ₹{result}")
    st.toast("Calculation Complete! 🎉 Optimal transportation cost calculated.")