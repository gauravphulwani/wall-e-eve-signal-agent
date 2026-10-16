from src.environment import MissionConfig, GridEnvironment
from src.planner import shortest_path

def test_path_exists():
    env = GridEnvironment(MissionConfig(seed=7))
    path = shortest_path(env, env.start, env.eve)
    assert path
    assert path[0] == env.start
    assert path[-1] == env.eve

def test_neighbors_are_open():
    env = GridEnvironment(MissionConfig(seed=8))
    for cell in env.neighbors(env.start):
        assert env.is_open(cell)
