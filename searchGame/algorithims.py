"""
Implements graph search algorithms: BFS, DFS, UCS, Greedy, and A*.
"""

from collections import deque
import heapq
import time


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]


def path_cost(problem, path):
    if not path:
        return 0
    total = 0
    for a, b in zip(path, path[1:]):
        for next_state, _, cost in problem.get_successors(a):
            if next_state == b:
                total += cost
                break
    return total


def bfs(problem, visualize_func, speed):
    start = problem.get_start_state()
    frontier = deque([start])
    came_from = {start: None}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        current = frontier.popleft()
        explored.add(current)
        nodes_expanded += 1
        if visualize_func:
            visualize_func(problem, explored, set(frontier), current, came_from)
            time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier

        for next_state, _, _ in problem.get_successors(current):
            if next_state not in came_from:
                frontier.append(next_state)
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))

    return None, nodes_expanded, max_frontier


def dfs(problem, visualize_func, speed):
    start = problem.get_start_state()
    frontier = [start]
    came_from = {start: None}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        current = frontier.pop()
        explored.add(current)
        nodes_expanded += 1
        if visualize_func:
            visualize_func(problem, explored, set(frontier), current, came_from)
            time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier

        for next_state, _, _ in problem.get_successors(current):
            if next_state not in came_from:
                frontier.append(next_state)
                came_from[next_state] = current
                max_frontier = max(max_frontier, len(frontier))

    return None, nodes_expanded, max_frontier


def best_first_search(problem, visualize_func, speed, priority):
    start = problem.get_start_state()
    counter = 0
    frontier = [(priority(0, start), counter, 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        _, _, g, current = heapq.heappop(frontier)
        if current in explored:
            continue

        explored.add(current)
        nodes_expanded += 1
        frontier_states = {item[3] for item in frontier}
        if visualize_func:
            visualize_func(problem, explored, frontier_states, current, came_from)
            time.sleep(speed)

        if problem.is_goal(current):
            return reconstruct_path(came_from, current), nodes_expanded, max_frontier

        for next_state, _, step_cost in problem.get_successors(current):
            new_g = g + step_cost
            if next_state not in cost_so_far or new_g < cost_so_far[next_state]:
                cost_so_far[next_state] = new_g
                came_from[next_state] = current
                counter += 1
                heapq.heappush(frontier, (priority(new_g, next_state), counter, new_g, next_state))
                max_frontier = max(max_frontier, len(frontier))

    return None, nodes_expanded, max_frontier


def ucs(problem, visualize_func, speed):
    return best_first_search(problem, visualize_func, speed, lambda g, s: g)


def greedy(problem, visualize_func, speed):
    return best_first_search(problem, visualize_func, speed, lambda g, s: problem.heuristic(s))


def astar(problem, visualize_func, speed):
    return best_first_search(problem, visualize_func, speed, lambda g, s: g + problem.heuristic(s))