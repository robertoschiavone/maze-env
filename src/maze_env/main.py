import gymnasium as gym

from gymnasium.utils.play import play

import maze_env

play(gym.make("maze_env/Maze-v0", size=(31, 21), render_mode="rgb_array"),
     keys_to_action={
         "a": 0,
         "w": 1,
         "d": 2,
         "s": 3
     }, noop=-1)
