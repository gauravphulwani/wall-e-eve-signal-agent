"""Breadth-first path planning on known traversable grid cells."""
from collections import deque

def shortest_path(env, start, goal):
    if start == goal:
        return [start]
    queue = deque([start])
    previous = {start: None}
    while queue:
        current = queue.popleft()
        for nxt in env.neighbors(current):
            if nxt in previous:
                continue
            previous[nxt] = current
            if nxt == goal:
                path = [goal]
                while path[-1] != start:
                    path.append(previous[path[-1]])
                return list(reversed(path))
            queue.append(nxt)
    return []
