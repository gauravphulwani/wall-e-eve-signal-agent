"""A simple autonomous agent with clue-based belief updates and resource tracking."""
from collections import Counter
from .planner import shortest_path

class WallEAgent:
    def __init__(self, env):
        self.env = env
        self.position = env.start
        self.battery = env.config.battery_capacity
        self.path = [self.position]
        self.visited = {self.position}
        self.steps = 0
        self.energy_used = 0
        self.log = []
        self.belief = {(r, c): 1.0 for r in range(env.config.rows)
                        for c in range(env.config.cols)
                        if (r, c) not in env.obstacles}
        self._normalize_belief()
        self.found = False
        self.clues_found = 0

    def _normalize_belief(self):
        total = sum(self.belief.values())
        if total:
            self.belief = {cell: val / total for cell, val in self.belief.items()}

    def update_belief(self, observation):
        # Visiting a cell without finding EVE rules that cell out.
        self.belief.pop(self.position, None)
        if observation["clue"]:
            self.clues_found += 1
            hint = observation["hint"]
            r0, c0 = self.position
            for cell in list(self.belief):
                r, c = cell
                consistent = (
                    (hint.startswith("north") and r < r0) or
                    (hint.startswith("south") and r > r0) or
                    (hint.startswith("same-row") and r == r0)
                ) and (
                    (hint.endswith("west") and c < c0) or
                    (hint.endswith("east") and c > c0) or
                    (hint.endswith("same-column") and c == c0)
                )
                # Keep a small probability floor so noisy or imperfect clues do not
                # collapse the entire belief distribution.
                self.belief[cell] *= 1.0 if consistent else 0.08
            self._normalize_belief()

    def _choose_goal(self):
        # Choose the highest-belief unvisited cell. If none remain, revisit the
        # highest-belief cell that is reachable.
        candidates = [c for c in self.belief if c not in self.visited]
        if not candidates:
            candidates = list(self.belief)
        if not candidates:
            return self.env.eve
        return max(candidates, key=lambda c: self.belief[c])

    def run(self):
        self.log.append(f"Mission start at {self.position}; battery={self.battery}")
        observation = self.env.observe(self.position)
        if observation["eve_found"]:
            self.found = True
            return self._result()
        self.update_belief(observation)

        while self.steps < self.env.config.max_steps and self.battery > 0:
            if self.position == self.env.eve:
                self.found = True
                break

            goal = self._choose_goal()
            route = shortest_path(self.env, self.position, goal)
            if not route or len(route) < 2:
                # Fall back to nearest unvisited open cell.
                options = [n for n in self.env.neighbors(self.position) if n not in self.visited]
                if not options:
                    break
                next_cell = options[0]
            else:
                next_cell = route[1]

            # One move consumes one battery unit. Scanning is free in this
            # baseline simulator; this assumption is stated in the README.
            self.position = next_cell
            self.path.append(next_cell)
            self.visited.add(next_cell)
            self.steps += 1
            self.battery -= 1
            self.energy_used += 1
            observation = self.env.observe(self.position)
            self.log.append(
                f"step={self.steps:03d} move={self.position} "
                f"clue={observation['clue']} battery={self.battery}"
            )
            if observation["eve_found"]:
                self.found = True
                self.log.append(f"EVE FOUND at {self.position} after {self.steps} moves.")
                break
            self.update_belief(observation)

        if not self.found:
            self.log.append("Mission ended: target not found within available resources.")
        return self._result()

    def _result(self):
        return {
            "success": self.found,
            "steps": self.steps,
            "energy_used": self.energy_used,
            "battery_remaining": self.battery,
            "clues_found": self.clues_found,
            "path": self.path,
            "visited": self.visited,
            "log": self.log,
            "belief": self.belief,
        }
