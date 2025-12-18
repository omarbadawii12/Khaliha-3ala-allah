# Traveling Salesman Problem (TSP) 🚀

##  Project Overview 📝
***This project implements and compares several Artificial Intelligence search algorithms applied to the classic Traveling Salesman Problem (TSP) on randomly generated city graphs.
The goal is hands-on implementation, experimentation, and evaluation of multiple AI search techniques, giving a deeper understanding of algorithmic behavior, performance trade-offs, and heuristic design.
We focus on building a complete solution framework, analyzing algorithm efficiency, and comparing how different search strategies perform when attempting to minimize the total path cost between multiple cities.
The project is designed for university students studying Artificial Intelligence or Search Algorithms – providing practical experience with exact, heuristic, and metaheuristic methods.***
###
## Implemented Algorithms 🧩
  **Uniform-Cost Search (UCS) 📏**

- Uninformed search expanding nodes by lowest cumulative path cost.
- Guarantees optimal solutions
- Serves as a baseline for comparison

__A* Search ⭐__

- Informed search with heuristics (e.g., Euclidean distance or MST estimate) for efficient guidance.

__Hill Climbing Search ⛰️__

- Local search using iterative improvements like 2-opt swaps, with random restarts to escape local optima.
  
__Nearest Neighbor + 2-opt 🛤️__

- Greedy constructive heuristic followed by local optimization to eliminate edge crossings.
  
__Genetic Algorithm (GA) 🧬__

- Population-based evolutionary search with selection, crossover, and mutation for global exploration.
  

  ## 🎉 Key Features

- Random city generation (default: 20 cities) 🌍
- Euclidean distance matrix
- Tour visualization for each algorithm 📊
- Performance comparison (tour cost, execution time, solution quality)

## Project Outcomes 📊

- Comparative analysis of solution quality (tour cost), execution time, and scalability
- Visualization of generated tours for each algorithm
- Insights into the trade-offs between exact methods (optimal but slow) and heuristic/metaheuristic methods (fast but approximate)


  ## 📂 Project Structure
tsp-ai-project/     
 ├──  main.py               # Main script to run experiments, comparisons, and visualizations     
├── data/   
│   └── cities.py            # City generation, distance matrix, and cost function (shared foundation)     
├── algorithms/   
│   ├── ucs.py               # Uniform-Cost Search implementation    
│   ├── a_star.py            # A* Search implementation     
│   ├── hill_climbing.py     # Hill Climbing + 2-opt improvements      
│   ├── nearest_neighbor.py  # Nearest Neighbor + 2-opt     
│   └── genetic_algorithm.py # Genetic Algorithm implementation    
├── utils/
│   ├── visualization.py     # Plotting cities and tours (using matplotlib)    
│   └── comparison.py        # Functions for benchmarking (time, cost, nodes explored)     
├── results/                 # Output folder for plots and comparison reports (generated)     
├── requirements.txt         # Dependencies (numpy, matplotlib, etc.)    

└── README.md                # This file
