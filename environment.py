"""Grid-world environment for the WALL-E and EVE search project."""
from dataclasses import dataclass
import random

@dataclass
class MissionConfig:
    rows: int = 12
    cols: int = 12
    start: tuple = (0, 0)
    eve: tuple = (10, 10)
    battery_capacity: int = 160
    max_steps: int = 180
    obstacle_density: float = 0.16
    seed: int = 7

class GridEnvironment:
    def __init__(self, config: MissionConfig):
        self.config = config
        self.rng = random.Random(config.seed)
        self.start = tuple(config.start)
        self.eve = tuple(config.eve)
        self.obstacles = set()
        protected = {self.start, self.eve}
        # Keep a simple guaranteed corridor so every generated mission is solvable.
        corridor = {(r, 0) for r in range(config.rows)}
        corridor |= {(config.rows - 1, c) for c in range(config.cols)}
        corridor |= {(r, config.cols - 1) for r in range(config.rows)}
        for r in range(config.rows):
            for c in range(config.cols):
                cell = (r, c)
                if cell not in protected | corridor and self.rng.random() < config.obstacle_density:
                    self.obstacles.add(cell)
        self.clues = self._make_clues()

    def _make_clues(self):
        candidates = [
            (r, c) for r in range(self.config.rows)
            for c in range(self.config.cols)
            if (r, c) not in self.obstacles and (r, c) not in {self.start, self.eve}
        ]
        self.rng.shuffle(candidates)
        return set(candidates[:max(3, len(candidates) // 18)])

    def in_bounds(self, cell):
        r, c = cell
        return 0 <= r < self.config.rows and 0 <= c < self.config.cols

    def is_open(self, cell):
        return self.in_bounds(cell) and cell not in self.obstacles

    def neighbors(self, cell):
        r, c = cell
        options = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
        return [p for p in options if self.is_open(p)]

    def observe(self, cell):
        """Return observations available only when the agent visits a cell."""
        if cell == self.eve:
            return {"eve_found": True, "clue": False}
        found_clue = cell in self.clues
        if found_clue:
            self.clues.remove(cell)
        # A clue gives a directional hint: EVE is in the same general half of the map.
        r, c = cell
        er, ec = self.eve
        hint = "north" if er < r else "south" if er > r else "same-row"
        hint += "-" + ("west" if ec < c else "east" if ec > c else "same-column")
        return {"eve_found": False, "clue": found_clue, "hint": hint if found_clue else None}
