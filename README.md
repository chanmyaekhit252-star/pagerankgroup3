# PageRank Algorithm – Data Structures and Algorithms

## Project Description

This project implements different versions of the PageRank algorithm to calculate the importance of web pages based on their incoming and outgoing links.

It demonstrates how PageRank develops through different stages, including in-degree ranking, Markov power iteration, sparse matrix calculations, iteration complexity, memory comparison, and the Gauss-Seidel method.

## Requirements

The project uses Python and the following libraries:

- NumPy – for numerical and matrix calculations.
- SciPy – for sparse matrix representation and calculations.
- Math – for logarithmic and mathematical calculations (built into Python).

## Installation

Install the required libraries using:

```bash
python -m pip install numpy scipy
```

## How to Run

1. Open the project folder.
2. Open a terminal in that folder.
3. Run the following command:

```bash
python pagerank.py
```

4. The program will display the calculations and results in the terminal.

## Project Sections

### 1. Normalized In-Degree Ranking (V1)

- Counts the incoming links for each page.
- Calculates the total number of links.
- Normalizes the scores to show each page's proportion of incoming links.

### 2. Raw Markov Power Iteration (V2)

- Creates an adjacency list.
- Initializes equal probability for every page.
- Distributes probability through outgoing links.
- Redistributes probability from dangling nodes.
- Calculates PageRank after the specified number of iterations.

### 3. Sparse Matrix and Dangling-Node Correction (Q3)

- Builds a sparse transition matrix using SciPy.
- Identifies dangling nodes.
- Calculates dangling-node probability.
- Applies the correction term.
- Calculates the updated PageRank vector.

### 4. Iteration Complexity (Part 3)

- Uses the damping factors 0.85 and 0.99.
- Estimates the number of iterations required.
- Uses a logarithmic formula to calculate the iteration count.
- Rounds the result up to the nearest whole iteration.

### 5. Memory Usage Comparison (Part 4)

- Compares dense matrix storage with sparse representation.
- Calculates the number of entries required by each representation.
- Calculates the memory entry ratio.

### 6. Gauss-Seidel PageRank

- Constructs the Google matrix.
- Applies sequential Gauss-Seidel updates.
- Calculates the residual after each iteration.
- Checks whether the algorithm has converged.
- Displays the final PageRank scores.

## Expected Results

The program demonstrates:

- Normalized in-degree scores.
- PageRank probabilities after iterations.
- Dangling-node correction.
- Iteration estimates for different damping factors.
- Dense and sparse storage comparison.
- Final Gauss-Seidel PageRank scores and convergence information.

## Notes

- PageRank scores represent the relative importance of pages.
- The damping factor controls the probability of following links rather than randomly jumping to another page.
- Sparse representation stores actual links instead of allocating space for every possible connection.
- The iteration complexity calculation is an estimate, while the Gauss-Seidel method checks numerical convergence.

## Author

Data Structures and Algorithms – PageRank Assignment