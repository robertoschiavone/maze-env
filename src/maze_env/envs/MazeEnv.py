import gymnasium as gym
import labyrinthine
import numpy as np
import pygame

from importlib.resources import path
from typing import Any, Dict, Optional, SupportsFloat, Tuple

from gymnasium.core import ActType, ObsType, RenderFrame
from gymnasium import spaces

from maze_env.graphics.Tilemap import Tilemap
from maze_env.graphics.Tileset import Tileset


class MazeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, size: int | Tuple[int, int], render_mode: Optional[str] = None):
        super().__init__()

        if isinstance(size, int):
            size = (size, size)
        assert (size[0] % 2 == 1) and (size[1] % 2 == 1), \
            "Maze width and height must be odd"

        self.render_mode = render_mode

        with path("maze_env.resources.images", "tiles.png") as filename:
            self.tileset = Tileset(filename)
        self.size = size
        self.width = size[0] * 32 + 64
        self.height = size[1] * 32 + 64
        self.n_channels = 3
        self.n_discrete_actions = 4

        self.action_space = spaces.Discrete(self.n_discrete_actions)
        self.observation_space = spaces.Discrete(self.size[0] * self.size[1])

        self.reward_range = (-2, 1)
        self.spec = None

        self.surface = None
        self.clock = None

        self.agent = (0, 0)
        self.start = (0, 0)
        self.end = (self.size[1] - 1, self.size[0] - 1)
        self.state = None
        self.tilemap = None

        self.score = 0

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) \
            -> tuple[ObsType, dict[str, Any]]:
        super().reset(seed=seed)

        self.surface = None
        self.clock = None

        self.agent = (0, 0)

        self.score = 0
        self.state = labyrinthine.depth_first(self.size, seed=seed)
        self.tilemap = Tilemap(self.state, self.tileset)

        if self.render_mode is not None:
            self.render()

        observation = self._get_observation()
        info = self._get_info()

        return observation, info

    # 0 left
    # 1 up
    # 2 right
    # 3 down
    def step(self, action: ActType) \
            -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        reward = 0
        terminated = False
        truncated = False

        if self.render_mode in ["human", "rgb_array"]:
            self.clock.tick(self.metadata["render_fps"])

        if self.score == self.reward_range[0]:
            truncated = True
        elif action in list(range(4)) and self._move_agent(action):
            terminated = self.agent[0] == self.end[0] and self.agent[1] == self.end[1]
            reward = 1 if terminated else -1 / (self.size[0] * self.size[1])
            self.score += reward

        truncated = self.score <= self.reward_range[0]

        observation = self._get_observation()
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        if self.render_mode is None:
            return

        if self.surface is None:
            pygame.init()

            if self.render_mode == "human":
                pygame.display.init()
                pygame.display.set_caption("Maze")
                self.surface = pygame.display.set_mode((self.height, self.width),
                                                       pygame.SRCALPHA, 32)
            elif self.render_mode == "rgb_array":
                self.surface = pygame.Surface((self.height, self.width),
                                              pygame.SRCALPHA, 32)

        assert self.surface is not None, \
            "Something went wrong with pygame. This should never happen."

        if self.clock is None:
            self.clock = pygame.time.Clock()

        self._draw()

        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        elif self.render_mode == "rgb_array":
            return np.array(pygame.surfarray.pixels3d(self.surface))

    def _move_agent(self, action: int) -> bool:
        i, j = self.agent
        if action == 0:
            j = max(0, j - 1)
        elif action == 1:
            i = max(0, i - 1)
        elif action == 2:
            j = min(self.size[0] - 1, j + 1)
        elif action == 3:
            i = min(self.size[1] - 1, i + 1)

        if self.state[i][j] == 0:
            self.agent = (i, j)
            return True
        return False

    def _draw(self) -> None:
        self.surface.fill((33, 30, 29))
        self.tilemap.render(self.surface)
        self.surface.blit(self.tileset.tiles[12],
                          ((self.agent[0] + 1) * 32, (self.agent[1] + 1) * 32))

        self.surface.blit(self.tileset.tiles[13],
                          ((self.end[0] + 1) * 32, (self.end[1] + 1) * 32))

    def _get_observation(self) -> ObsType:
        return self.agent[0] * self.size[0] + self.agent[1]

    def _get_info(self) -> Dict[str, Any]:
        return {
            "agent": self.agent,
            "maze": self.state,
            "score": self.score
        }

    def close(self) -> None:
        if self.surface is not None:
            pygame.display.quit()
            pygame.quit()
