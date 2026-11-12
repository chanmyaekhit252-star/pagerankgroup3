
import math
import numpy as np
from scipy.sparse import coo_matrix


# ==========================================
# V1: NORMALIZED IN-DEGREE CITATION RANKING
# ==========================================

def v1_indegree_rank(V, edges):
    """
    Stage 1: Normalized in-degree citation ranking.
    """

    if V <= 0:
        raise ValueError("V must be positive")

    in_degree = [0] * V

    for source, destination in edges:
        if not (1 <= source <= V and 1 <= destination <= V):
            raise ValueError("Invalid page number")

        in_degree[destination - 1] += 1

    total_links = sum(in_degree)

    if total_links == 0:
        return [0.0] * V

    normalized_scores = [
        degree / total_links for degree in in_degree
    ]

    return normalized_scores


# Test V1
V1 = 4

edges_v1 = [
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 1),
    (3, 4),
    (4, 4)
]

scores = v1_indegree_rank(V1, edges_v1)

print("V1: Normalized In-Degree Ranking")

for page, score in enumerate(scores, start=1):
    print(f"Page {page}: {score:.4f}")


# ==========================================
# V2: RAW MARKOV POWER ITERATION
# ==========================================

def v2_raw_markov_power(V, edges, num_iters):
    """
    Stage 2: Markov power iteration.
    Dangling-node probability is redistributed equally.
    """

    if not V:
        raise ValueError("V must contain at least one page")

    if num_iters < 0:
        raise ValueError("Number of iterations cannot be negative")

    adjacency = {page: [] for page in V}

    for source, destination in edges:
        if source not in adjacency or destination not in adjacency:
            raise ValueError("Invalid page number")

        adjacency[source].append(destination)

    n = len(V)
    pi = {page: 1 / n for page in V}

    for iteration in range(num_iters):

        new_pi = {page: 0.0 for page in V}

        dangling_probability = 0.0

        for page in V:
            outgoing = adjacency[page]

            if outgoing:
                probability = pi[page] / len(outgoing)

                for destination in outgoing:
                    new_pi[destination] += probability
            else:
                dangling_probability += pi[page]

        # Redistribute dangling probability equally
        for page in V:
            new_pi[page] += dangling_probability / n

        pi = new_pi

    return pi


# Test V2
V2 = [1, 2, 3, 4]

edges_v2 = [
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 1),
    (3, 4),
    (4, 4)
]

result = v2_raw_markov_power(V2, edges_v2, 1)

print("\nV2: PageRank After 1 Iteration")

for page, probability in result.items():
    print(f"Page {page}: {probability:.4f}")

print("Total probability:", sum(result.values()))


# ==========================================
# Q3: SPARSE MATRIX AND DANGLING-NODE
# CORRECTION
# ==========================================

def solve_q3():

    n = 4
    alpha = 0.8

    edges = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 0),
        (2, 3)
    ]

    out_degree = np.zeros(n)

    for source, destination in edges:
        if not (0 <= source < n and 0 <= destination < n):
            raise ValueError("Invalid page index")

        out_degree[source] += 1

    rows = []
    cols = []
    values = []

    for source, destination in edges:
        probability = 1 / out_degree[source]

        rows.append(destination)
        cols.append(source)
        values.append(probability)

    P = coo_matrix(
        (values, (rows, cols)),
        shape=(n, n)
    ).tocsr()

    # Initial PageRank vector
    rank = np.ones(n) / n

    # Identify dangling nodes
    dangling = np.where(out_degree == 0)[0]

    # Total probability belonging to dangling nodes
    S_D = np.sum(rank[dangling])

    # Dangling-node and teleportation correction
    epsilon = (
        alpha * S_D + (1 - alpha)
    ) / n

    # Calculate PageRank after one iteration
    new_rank = alpha * (P @ rank) + epsilon

    print("\nQ3: Sparse Matrix and Dangling-Node Correction")

    print("Initial vector:", rank)
    print("Dangling nodes:", dangling + 1)
    print("Dangling probability:", S_D)
    print(f"Epsilon: {epsilon:.4f}")
    print("Final PageRank:", new_rank)
    print("Probability sum:", np.sum(new_rank))


# ==========================================
# PART 3: ITERATION COMPLEXITY
# ==========================================

def iteration_complexity():

    epsilon = 0.000001

    print("\nPart 3: Iteration Complexity")

    for alpha in [0.85, 0.99]:

        k = math.log(2 / epsilon) / (-math.log(alpha))

        iterations = math.ceil(k)

        print("\nDamping factor:", alpha)
        print(f"Calculated iterations: {k:.4f}")
        print("Required iterations (rounded up):", iterations)


# ==========================================
# PART 4: MEMORY USAGE COMPARISON
# ==========================================

def memory_comparison():

    V = 100000
    E = 500000

    # Dense adjacency matrix
    dense = V * V

    # Sparse representation: actual links
    sparse = E

    ratio = dense / sparse

    print("\nPart 4: Memory Usage Comparison")

    print(f"Number of pages (V): {V:,}")
    print(f"Number of links (E): {E:,}")

    print(f"Dense matrix entries: {dense:,}")
    print(f"Sparse link entries: {sparse:,}")

    print(f"Memory entry ratio: {ratio:,.0f}:1")

    print(
        "Note: Sparse storage also requires indexing "
        "and other O(V) data."
    )


# ==========================================
# GAUSS-SEIDEL PAGERANK
# ==========================================

def pagerank_gauss_seidel():

    n = 4
    alpha = 0.8
    tolerance = 1e-6
    max_iterations = 10000

    edges = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 0),
        (2, 3),
        (3, 3)
    ]

    out_degree = np.zeros(n)

    for source, destination in edges:
        if not (0 <= source < n and 0 <= destination < n):
            raise ValueError("Invalid page index")

        
        out_degree[source] += 1

    # Build a list of incoming links for each page
    incoming = [[] for _ in range(n)]

    for source, destination in edges:
        incoming[destination].append(source)

    # Initial PageRank vector
    rank = np.ones(n) / n

    # Gauss-Seidel iteration
    for iteration in range(max_iterations):

        old_rank = rank.copy()

        for page in range(n):

            link_sum = 0.0

            for source in incoming[page]:
                link_sum += rank[source] / out_degree[source]

            rank[page] = (
                alpha * link_sum
                + (1 - alpha) / n
            )

        # Check convergence
        error = np.max(np.abs(rank - old_rank))

        if error < tolerance:
            break

    print("\nGauss-Seidel PageRank")
    print("Number of iterations:", iteration + 1)

    for page, score in enumerate(rank, start=1):
        print(f"Page {page}: {score:.6f}")

    print("Probability sum:", np.sum(rank))
    print("Final error:", error)


# ==========================================
# RUN ALL ASSIGNMENT PARTS
# ==========================================

solve_q3()

iteration_complexity()

memory_comparison()

pagerank_gauss_seidel()
        