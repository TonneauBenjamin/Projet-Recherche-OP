# Projet-Recherche-OP

## Overview
**Projet-Recherche-OP** (Operations Research Project) is a Python-based project focused on the design, implementation, and complexity analysis of operational research algorithms. Developed as part of the engineering curriculum at EFREI Paris, it processes various problem instances and evaluates the performance and execution traces of different algorithmic approaches.

## Project Structure

### Core Modules
*   **`main.py`**: The primary entry point for the application [cite: 2].
*   **`algorithmes.py`**: Contains the core logic and implementations of the operation research algorithms [cite: 2].
*   **`process_checkpoint.py`**: Handles checkpoint processing and state management during execution [cite: 2].

### Complexity Analysis
A significant portion of the project is dedicated to analyzing algorithmic complexity [cite: 2]:
*   **`complexite.py`** / **`complexite_simple.py`**: Core complexity evaluation logic [cite: 2].
*   **`lancer_complexite.py`**: Script to launch the complexity benchmarking [cite: 2].
*   **`menu_complexite.py`**: Interactive menu for selecting and running specific complexity tests [cite: 2].

### Data Directories
*   **`entrees/`**: Contains the input datasets (`probleme1.txt` through `probleme12.txt`) that serve as test cases and configurations for the algorithms [cite: 2].
*   **`traces/`**: Stores execution trace logs (e.g., `9-4-trace1-bh.txt`, `9-4-trace1-no.txt`) [cite: 2]. These are used for debugging and comparing algorithm performance across different heuristics.

## Prerequisites
*   Python 3.12 or higher (based on `__pycache__` signatures) [cite: 2].

## How to Run
To execute the main algorithm sequence, run:
```bash
python main.py
```

To run the complexity analysis tools and open the interactive menu, execute:
```bash
python menu_complexite.py
```
