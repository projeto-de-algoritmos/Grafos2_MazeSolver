import numpy as np
from collections import deque
import random
import heapq


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


def get_neighbors(maze, node):
    rows, cols = maze.shape
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = []
    for dr, dc in directions:
        r, c = node
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


def reconstruct_path(distances, start, end):
    path = [end]
    current_node = end
    while current_node != start:
        current_node = distances[current_node][1]
        path.append(current_node)
    path.reverse()
    return path


def dijkstra(maze, start, end):
    rows, cols = maze.shape
    distances = {(r, c): (float('inf'), None) for r in range(rows) for c in range(cols)}
    distances[start] = (0, None)

    queue = [(0, start)]
    heapq.heapify(queue)

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        if current_distance > distances[current_node][0]:
            continue

        neighbors = get_neighbors(maze, current_node)
        for neighbor in neighbors:
            neighbor_distance = current_distance + 1  
            if neighbor_distance < distances[neighbor][0]:
                distances[neighbor] = (neighbor_distance, current_node)
                heapq.heappush(queue, (neighbor_distance, neighbor))

    path = reconstruct_path(distances, start, end)
    return path
