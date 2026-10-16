
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.environment import MissionConfig, GridEnvironment
from src.agent import WallEAgent
from src.baseline import RandomWalkAgent


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs"


def make_config(seed, base):
    return MissionConfig(
        rows=base.rows,
        cols=base.cols,
        start=base.start,
        eve=base.eve,
        battery_capacity=base.battery_capacity,
        max_steps=base.max_steps,
        obstacle_density=base.obstacle_density,
        seed=seed,
    )


def evaluate():
    OUTPUT.mkdir(exist_ok=True)

    config_data = json.loads(
        (ROOT / "config" / "mission.json").read_text()
    )
    config_data["start"] = tuple(config_data["start"])
    config_data["eve"] = tuple(config_data["eve"])
    base = MissionConfig(**config_data)

    rows = []

    for seed in range(1, 21):
        # Identical map settings for both agents.
        env_smart = GridEnvironment(make_config(seed, base))
        env_random = GridEnvironment(make_config(seed, base))

        smart = WallEAgent(env_smart).run()
        random_result = RandomWalkAgent(env_random).run()

        rows.append({
            "seed": seed,
            "smart_success": int(smart["success"]),
            "smart_steps": smart["steps"],
            "smart_energy": smart["energy_used"],
            "random_success": int(random_result["success"]),
            "random_steps": random_result["steps"],
            "random_energy": random_result["energy_used"],
        })

    csv_path = OUTPUT / "agent_comparison.csv"

    with csv_path.open("w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=list(rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)

    summary = {
        "runs": total,
        "smart_success_rate_percent": round(
            100 * sum(r["smart_success"] for r in rows) / total, 2
        ),
        "random_success_rate_percent": round(
            100 * sum(r["random_success"] for r in rows) / total, 2
        ),
        "smart_average_steps": round(
            sum(r["smart_steps"] for r in rows) / total, 2
        ),
        "random_average_steps": round(
            sum(r["random_steps"] for r in rows) / total, 2
        ),
    }

    (OUTPUT / "agent_comparison_summary.json").write_text(
        json.dumps(summary, indent=2)
    )

    labels = ["WALL-E (clue-based)", "Random baseline"]
    success_rates = [
        summary["smart_success_rate_percent"],
        summary["random_success_rate_percent"],
    ]
    average_steps = [
        summary["smart_average_steps"],
        summary["random_average_steps"],
    ]

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    axes[0].bar(labels, success_rates)
    axes[0].set_title("Success Rate Comparison")
    axes[0].set_ylabel("Success rate (%)")
    axes[0].set_ylim(0, 105)
    axes[0].tick_params(axis="x", rotation=10)

    axes[1].bar(labels, average_steps)
    axes[1].set_title("Average Steps per Mission")
    axes[1].set_ylabel("Steps")
    axes[1].tick_params(axis="x", rotation=10)

    fig.tight_layout()
    fig.savefig(OUTPUT / "agent_comparison.png", dpi=160)
    plt.close(fig)

    print("\nAGENT COMPARISON RESULTS")
    print(json.dumps(summary, indent=2))
    print("\nSaved:")
    print(OUTPUT / "agent_comparison.csv")
    print(OUTPUT / "agent_comparison_summary.json")
    print(OUTPUT / "agent_comparison.png")


if __name__ == "__main__":
    evaluate()
