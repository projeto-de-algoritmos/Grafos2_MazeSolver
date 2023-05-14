import numpy as np
from collections import deque
import random

def generate_maze(size):
    def in_bounds(x, y):
        return 0 <= x < size and 0 <= y < size

    def recursive_backtracker(x, y):
        maze[y, x] = 0
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy

            if in_bounds(nx, ny) and maze[ny, nx] == 1:
                maze[y + dy, x + dx] = 0
                recursive_backtracker(nx, ny)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    maze = np.ones((size, size), dtype=int)

    start = (0, 1)
    end = (size - 1, size - 2)

    recursive_backtracker(1, 1)

    maze[start] = 0
    maze[end] = 0

    return start, end, maze


def bfs(maze, start, end):
    rows, cols = maze.shape
    visited = np.zeros_like(maze, dtype=bool)
    queue = deque([(start, [])])

    while queue:
        (y, x), path = queue.popleft()

        if (y, x) == end:
            return path + [(y, x)]

        if not visited[y, x]:
            visited[y, x] = True
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and not visited[ny, nx] and maze[ny, nx] == 0:
                    queue.append(((ny, nx), path + [(y, x)]))

    return None
