"""Generate map and performance plots."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_mission(env, result, output_path):
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_xlim(-0.5, env.config.cols - 0.5)
    ax.set_ylim(env.config.rows - 0.5, -0.5)
    ax.set_xticks(range(env.config.cols))
    ax.set_yticks(range(env.config.rows))
    ax.grid(True, alpha=0.35)
    for r, c in env.obstacles:
        ax.scatter(c, r, marker="s", s=260, color="dimgray")
    for r, c in env.clues:
        ax.scatter(c, r, marker="*", s=150, color="gold", edgecolors="black")
    path = result["path"]
    if path:
        ax.plot([c for r,c in path], [r for r,c in path], linewidth=2.5,
                marker="o", markersize=3, label="WALL-E path")
    sr, sc = env.start
    er, ec = env.eve
    ax.scatter(sc, sr, marker="s", s=180, color="dodgerblue", label="Start")
    ax.scatter(ec, er, marker="*", s=300, color="limegreen", edgecolors="black", label="EVE")
    ax.set_title(f"WALL-E Mission Path | success={result['success']} | steps={result['steps']}")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

def plot_evaluation(results, output_path):
    seeds = list(range(1, len(results) + 1))
    steps = [r["steps"] for r in results]
    energy = [r["energy_used"] for r in results]
    success = [1 if r["success"] else 0 for r in results]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].plot(seeds, steps, marker="o", label="Steps")
    axes[0].plot(seeds, energy, marker="s", label="Energy used")
    axes[0].set_title("Mission cost by run")
    axes[0].set_xlabel("Run")
    axes[0].set_ylabel("Count")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    running = [100 * sum(success[:i]) / i for i in range(1, len(success)+1)]
    axes[1].plot(seeds, running, marker="o")
    axes[1].set_ylim(-5, 105)
    axes[1].set_title("Cumulative success rate")
    axes[1].set_xlabel("Run")
    axes[1].set_ylabel("Success rate (%)")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
