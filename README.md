# WALL-E and EVE's Signal — Autonomous Search Agent

**VinnovateIT Round 1 | AIML Project**

## 1. Project Overview

This project implements an autonomous search agent inspired by WALL-E's mission to locate EVE in a simulated grid environment.

The agent navigates around obstacles, gathers clues, updates its belief about EVE's location, plans its movement and manages limited battery resources. The project evaluates its performance against a random-walk baseline.

## 2. Features

- Configurable grid environment using JSON.
- Obstacle-aware path planning using Breadth-First Search (BFS).
- Clue-based belief updates for locating EVE.
- Battery and maximum-step constraints.
- Mission path visualization using Matplotlib.
- Mission logs and JSON reports.
- Multi-run evaluation and baseline comparison.
- CSV results and performance graphs.

## 3. Technologies Used

- Python 3
- NumPy
- Matplotlib
- JSON and CSV
- PyCharm

## 4. Project Structure

```text
wall_e_eve_agent/
├── config/
│   └── mission.json
├── outputs/
│   ├── path_visualization.png
│   ├── performance_graph.png
│   ├── agent_comparison.png
│   ├── agent_comparison.csv
│   ├── agent_comparison_summary.json
│   ├── evaluation.csv
│   ├── evaluation_summary.json
│   ├── mission_log.txt
│   └── mission_report.json
├── reports/
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── baseline.py
│   ├── environment.py
│   ├── evaluate_agents.py
│   ├── main.py
│   ├── planner.py
│   └── visualization.py
├── tests/
├── requirements.txt
└── README.md
```

## 5. Setup and Installation

Clone the repository and enter the project directory:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd wall_e_eve_agent
```

Create and activate a virtual environment on macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## 6. Running the Project

Run the main simulation:

```bash
python -m src.main
```

Run the agent comparison experiment:

```bash
python -m src.evaluate_agents
```

The generated outputs are saved in the `outputs/` directory.

## 7. Path Visualization

The path visualization displays WALL-E's starting position, obstacles, clue locations, movement trajectory and EVE's location.

The graph provides a visual representation of the search process and demonstrates how the agent navigates the simulated environment.

## 8. Experimental Evaluation

The initial baseline comparison was conducted over 20 mission runs.

| Metric | WALL-E | Random baseline |
|---|---:|---:|
| Number of runs | 20 | 20 |
| Success rate | 100% | 60% |
| Average steps | 54.8 | 104.7 |

In this experiment, the clue-based agent achieved a 40-percentage-point higher success rate and used approximately 47.7% fewer steps on average than the random baseline.

These results apply to the tested simulation configurations. Additional testing on unseen environments is required to evaluate generalization.

## 9. Evaluation Outputs

- `path_visualization.png` — simulated mission path.
- `performance_graph.png` — mission cost and cumulative success.
- `agent_comparison.png` — comparison of success rates and average steps.
- `agent_comparison.csv` — individual run results.
- `agent_comparison_summary.json` — aggregate comparison metrics.
- `mission_log.txt` — recorded mission activity.
- `mission_report.json` — mission outcome and report.
- `evaluation_summary.json` — evaluation statistics.

## 10. Future Improvements

- Evaluate performance across different obstacle densities.
- Compare BFS planning with alternative search algorithms.
- Test different battery capacities and mission limits.
- Improve uncertainty handling and clue interpretation.
- Add statistical summaries across more random seeds.
- Extend the simulator with noisy observations and more realistic environments.

## 11. Conclusion

This project demonstrates a simulated autonomous agent that combines path planning, clue-based search, resource management and quantitative evaluation. Comparing it with a random baseline provides an initial way to measure the benefits of informed decision-making.

**Project:** WALL-E and EVE's Signal — Autonomous Search Agent  
**Club:** VinnovateIT  
**Round:** Round 1 — AIML