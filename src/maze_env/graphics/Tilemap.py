import numpy as np

from .Tile import Tile


def is_outer_left_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_inner_left_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_top_left_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_outer_top_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_inner_top_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_top_right_wall(coords, maze):
    i, j = coords
    return maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_outer_right_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_inner_right_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_bottom_right_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_outer_bottom_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_inner_bottom_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_bottom_left_wall(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_left_to_right(coords, maze):
    i, j = coords
    return maze[i - 1][j] == Tile.EMPTY.value and \
        maze[i + 1][j] == Tile.EMPTY.value and \
        maze[i][j - 1] != Tile.EMPTY.value and \
        maze[i][j + 1] != Tile.EMPTY.value


def is_top_to_bottom(coords, maze):
    i, j = coords
    return maze[i - 1][j] != Tile.EMPTY.value and \
        maze[i + 1][j] != Tile.EMPTY.value and \
        maze[i][j - 1] == Tile.EMPTY.value and \
        maze[i][j + 1] == Tile.EMPTY.value


def is_center(coords, maze):
    i, j = coords
    return maze[i - 1][j] not in [Tile.EMPTY.value, Tile.PLATFORM.value] and \
        maze[i + 1][j] not in [Tile.EMPTY.value, Tile.PLATFORM.value] and \
        maze[i][j - 1] not in [Tile.EMPTY.value, Tile.PLATFORM.value] and \
        maze[i][j + 1] not in [Tile.EMPTY.value, Tile.PLATFORM.value]


class Tilemap:
    def __init__(self, maze, tileset, tilesize=(32, 32)):
        self.tileset = tileset
        self.width = len(maze)
        self.height = len(maze[0])
        self.tile_width, self.tile_height = tilesize
        self.tilemap = self._generate_map(maze)

    def render(self, surface):
        m, n = self.tilemap.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.tilemap[i][j]]
                surface.blit(tile, (i * 32, j * 32))

    @staticmethod
    def _generate_map(maze):
        maze = [[Tile.PATH.value if c == 0 else Tile.EMPTY.value for c in row]
                for row in maze]
        maze = np.pad(maze, 1, constant_values=Tile.EMPTY.value)

        for i in range(1, len(maze) - 1):
            for j in range(1, len(maze[0]) - 1):
                if maze[i][j] == Tile.PATH.value:
                    if is_outer_left_wall((i, j), maze):
                        maze[i][j] = Tile.OUTER_LEFT_WALL.value
                    if is_inner_left_wall((i, j), maze):
                        maze[i][j] = Tile.INNER_LEFT_WALL.value
                    if is_top_left_wall((i, j), maze):
                        maze[i][j] = Tile.TOP_LEFT_WALL.value
                    if is_outer_top_wall((i, j), maze):
                        maze[i][j] = Tile.OUTER_TOP_WALL.value
                    if is_inner_top_wall((i, j), maze):
                        maze[i][j] = Tile.INNER_TOP_WALL.value
                    if is_top_right_wall((i, j), maze):
                        maze[i][j] = Tile.TOP_RIGHT_WALL.value
                    if is_outer_right_wall((i, j), maze):
                        maze[i][j] = Tile.OUTER_RIGHT_WALL.value
                    if is_inner_right_wall((i, j), maze):
                        maze[i][j] = Tile.INNER_RIGHT_WALL.value
                    if is_bottom_right_wall((i, j), maze):
                        maze[i][j] = Tile.BOTTOM_RIGHT_WALL.value
                    if is_outer_bottom_wall((i, j), maze):
                        maze[i][j] = Tile.OUTER_BOTTOM_WALL.value
                    if is_inner_bottom_wall((i, j), maze):
                        maze[i][j] = Tile.INNER_BOTTOM_WALL.value
                    if is_bottom_left_wall((i, j), maze):
                        maze[i][j] = Tile.BOTTOM_LEFT_WALL.value
                    if is_left_to_right((i, j), maze):
                        maze[i][j] = Tile.LEFT_TO_RIGHT.value
                    if is_top_to_bottom((i, j), maze):
                        maze[i][j] = Tile.TOP_TO_BOTTOM.value
                    if is_center((i, j), maze):
                        maze[i][j] = Tile.CENTER.value

        for i in range(1, len(maze) - 1):
            for j in range(1, len(maze[0]) - 1):
                if maze[i][j] in [
                    Tile.OUTER_LEFT_WALL.value,
                    Tile.LEFT_TO_RIGHT.value,
                    Tile.BOTTOM_LEFT_WALL.value,
                    Tile.OUTER_BOTTOM_WALL.value,
                    Tile.INNER_BOTTOM_WALL.value,
                    Tile.BOTTOM_RIGHT_WALL.value,
                    Tile.OUTER_RIGHT_WALL.value
                ]:
                    maze[i + 1][j] = Tile.PLATFORM.value

        return maze

    def __str__(self):
        return f"{self.__class__.__name__}"
