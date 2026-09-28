"""
Challenge 1: Problem 1 path visualization with yellow path terminal fallback.
"""

import sys
import time
import heapq

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

CELL_SIZE = 100
COLORS = {
    'bg': (255, 255, 255),
    'grid': (0, 0, 0),
    'explored': (200, 200, 200),
    'frontier': (0, 0, 255),
    'current': (255, 0, 0),
    'goal': (0, 255, 0),
    'path': (255, 255, 0),      
    'path_line': (200, 160, 0),
    'obstacle': (80, 80, 80),
    'start': (0, 150, 255)
}

class GridProblem:
    def __init__(self):
        self.grid_size = 5
        self.start = (0, 0)
        self.goal = (4, 4)
        self.obstacles = {(1, 1), (2, 2), (3, 3)}

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        x, y = state
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        succ = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and (nx, ny) not in self.obstacles:
                succ.append(((nx, ny), 1))
        return succ

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]

def print_terminal_grid(problem, path):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"

    path_set = set(path) if path else set()
    print("\n--- Problem 1 Grid (Final Path in Yellow) ---")
    for y in range(problem.grid_size):
        row = []
        for x in range(problem.grid_size):
            st = (x, y)
            if st == problem.start:
                row.append(f"{BLUE}[ S ]{RESET}")
            elif st == problem.goal:
                row.append(f"{GREEN}[ G ]{RESET}")
            elif st in problem.obstacles:
                row.append(f"{GRAY}[ X ]{RESET}")
            elif st in path_set:
                row.append(f"{YELLOW}[ * ]{RESET}")
            else:
                row.append("[   ]")
        print(" ".join(row))
    print(f"\n{YELLOW}[ * ] = Yellow Solution Path{RESET}\n")

def run_astar():
    problem = GridProblem()
    start = problem.get_start_state()
    frontier = [(problem.heuristic(start), 0, 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()
    counter = 0

    goal_node = None
    while frontier:
        _, _, g, current = heapq.heappop(frontier)
        if current in explored:
            continue
        explored.add(current)

        if problem.is_goal(current):
            goal_node = current
            break

        for nxt, cost in problem.get_successors(current):
            new_g = g + cost
            if nxt not in cost_so_far or new_g < cost_so_far[nxt]:
                cost_so_far[nxt] = new_g
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (new_g + problem.heuristic(nxt), counter, new_g, nxt))

    path = reconstruct_path(came_from, goal_node)
    print(f"Goal Reached!\nFinal Path: {path}\nTotal Cost: {len(path) - 1}")

    if PYGAME_AVAILABLE:
        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Challenge 1: A* Path in Yellow")
        # Draw grid & yellow path
        screen.fill(COLORS['bg'])
        for x in range(problem.grid_size):
            for y in range(problem.grid_size):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS['grid'], rect, 1)
                st = (x, y)
                if st in problem.obstacles:
                    pygame.draw.rect(screen, COLORS['obstacle'], rect)
                elif st == problem.start:
                    pygame.draw.rect(screen, COLORS['start'], rect)
                elif st == problem.goal:
                    pygame.draw.rect(screen, COLORS['goal'], rect)
                elif st in path:
                    pygame.draw.rect(screen, COLORS['path'], rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
    else:
        print_terminal_grid(problem, path)

if __name__ == "__main__":
    run_astar()
