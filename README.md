# Optimal Transportation Cost Calculator using Vogel’s Approximation Method (VAM)
This Streamlit application is a tool for solving transportation problems in operations research using the Vogel’s Approximation Method (VAM). With this app, users can input custom supply and demand values, along with a cost matrix, to compute the initial feasible solution that minimizes total transportation costs.

### Collaborators
* [Chaitanya Birla](https://github.com/chaitanyabirla)
* [Kanishk Saleria](https://github.com/kanishksaleria)

# About the Project
The Vogel’s Approximation Method is a widely-used algorithm in operations research to determine a cost-effective distribution solution between suppliers and demand points. This application offers a user-friendly interface to input supply, demand, and cost matrices and receive optimal results using VAM.

# Features
* **Custom Input Options:** Users can enter number of supply and demand points, supply and demand values as well as cost matrix.
* **Cost matrix for transportation costs.**
* **Validation Checks:** Ensures that all inputs are properly formatted and align with the specified number of supply and demand points.
* **Real-Time Calculation:** On button click, calculates the basic feasible solution using VAM.
* **Interactive UI:** Displays input data and optimal transportation cost with a friendly UI, including success messages and celebratory animations.

# Prerequisites
To run this application, you will need:
* Python 3.8 or higher
* Streamlit
* Numpy

# Usage
* Start the Streamlit app:
```bash
streamlit run Calculator.py
```
* Open the local Streamlit server URL in your browser.
* Enter the number of supply and demand points, supply and demand values, and the cost matrix.
* Click on the “Calculate Optimal Cost” button.
* The app will display the input data and the calculated minimum transportation cost.

# How It Works
The application leverages VAM to determine the initial feasible solution for transportation problems by following these steps:
* **Penalty Calculation:** The app calculates penalties for each row and column in the cost matrix.
* **Maximum Penalty Selection:** The row or column with the highest penalty is selected for cost-saving opportunities.
* **Allocation and Adjustment:** Supplies are allocated to the lowest-cost cell within the selected row or column, updating the matrix until all supplies and demands are met.

# Core Functions
* `Diff_step(grid)`: Computes row and column penalties based on differences between the smallest costs in each row and column.
* `solve_transportation_problem(grid, supply, demand, n, m)`: Executes the VAM algorithm to iteratively allocate supplies, update the matrix, and calculate total cost.
