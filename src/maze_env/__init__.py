from gymnasium.envs.registration import register

from .envs.MazeEnv import MazeEnv

__all__ = [MazeEnv]

register(
    id="maze_env/Maze-v0",
    entry_point="maze_env.envs.MazeEnv:MazeEnv",
    reward_threshold=100
)
