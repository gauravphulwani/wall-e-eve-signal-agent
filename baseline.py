
import random


class RandomWalkAgent:
    """Baseline agent that moves randomly without using clues."""

    def __init__(self, env):
        self.env = env
        self.position = env.start
        self.visited = {self.position}
        self.steps = 0
        self.found = self.position == env.eve
        self.path = [self.position]

    def run(self):
        rng = random.Random(self.env.config.seed)

        while (
            not self.found
            and self.steps < self.env.config.max_steps
        ):
            if self.steps >= self.env.config.battery_capacity:
                break

            neighbors = self.env.neighbors(self.position)

            if not neighbors:
                break

            unvisited = [
                cell for cell in neighbors
                if cell not in self.visited
            ]

            # Prefer new cells; otherwise choose a valid neighbor.
            choices = unvisited if unvisited else neighbors
            self.position = rng.choice(choices)

            self.path.append(self.position)
            self.visited.add(self.position)
            self.steps += 1

            observation = self.env.observe(self.position)

            if observation["eve_found"]:
                self.found = True

        return {
            "success": self.found,
            "steps": self.steps,
            "energy_used": self.steps,
            "path": self.path,
        }
