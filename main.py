"""Run one WALL-E mission and save the required outputs."""
from pathlib import Path
import csv, json, sys
from .environment import MissionConfig, GridEnvironment
from .agent import WallEAgent
from .visualization import plot_mission, plot_evaluation

ROOT = Path(__file__).resolve().parents[1]

def load_config():
    data = json.loads((ROOT / "config" / "mission.json").read_text())
    data["start"] = tuple(data["start"])
    data["eve"] = tuple(data["eve"])
    return MissionConfig(**data)

def run_many(n=20):
    base = load_config()
    results = []
    for seed in range(1, n + 1):
        config = MissionConfig(
            rows=base.rows, cols=base.cols, start=base.start, eve=base.eve,
            battery_capacity=base.battery_capacity, max_steps=base.max_steps,
            obstacle_density=base.obstacle_density, seed=seed
        )
        env = GridEnvironment(config)
        result = WallEAgent(env).run()
        results.append({k: result[k] for k in
                        ("success", "steps", "energy_used", "battery_remaining", "clues_found")})
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    with (out / "evaluation.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    plot_evaluation(results, out / "performance_graph.png")
    success_rate = 100 * sum(r["success"] for r in results) / len(results)
    summary = {
        "runs": n,
        "success_rate_percent": round(success_rate, 2),
        "average_steps": round(sum(r["steps"] for r in results) / n, 2),
        "average_energy_used": round(sum(r["energy_used"] for r in results) / n, 2),
        "average_clues_found": round(sum(r["clues_found"] for r in results) / n, 2)
    }
    (out / "evaluation_summary.json").write_text(json.dumps(summary, indent=2))
    print("Evaluation summary")
    print(json.dumps(summary, indent=2))

def main():
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    config = load_config()
    env = GridEnvironment(config)
    result = WallEAgent(env).run()
    plot_mission(env, result, out / "path_visualization.png")
    (out / "mission_log.txt").write_text("\n".join(result["log"]) + "\n")
    report = {
        "success": result["success"],
        "steps": result["steps"],
        "energy_used": result["energy_used"],
        "battery_remaining": result["battery_remaining"],
        "clues_found": result["clues_found"],
        "final_position": list(result["path"][-1])
    }
    (out / "mission_report.json").write_text(json.dumps(report, indent=2))
    print("Mission report")
    print(json.dumps(report, indent=2))
    print(f"\nSaved path visualization: {out / 'path_visualization.png'}")
    print(f"Saved decision log: {out / 'mission_log.txt'}")
    print("\nStarting 20-run evaluation...")
    run_many(20)

if __name__ == "__main__":
    main()
