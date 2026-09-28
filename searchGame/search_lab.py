"""
Main entry point for AI Search Algorithms Assignment.
"""

import argparse
from problems import GridProblem, RomaniaProblem, VacuumProblem, WaterJugsProblem
from algorithms import bfs, dfs, ucs, greedy, astar, path_cost
from visualization import (
    visualize_grid,
    visualize_graph,
    visualize_vacuum,
    visualize_water_jugs,
    wait_for_close,
    PYGAME_AVAILABLE,
)


def main():
    parser = argparse.ArgumentParser(description="AI Search Algorithms Assignment")
    parser.add_argument('--strategy', required=True, choices=['bfs', 'dfs', 'ucs', 'greedy', 'astar'])
    parser.add_argument('--problem', type=int, required=True, choices=[1, 2, 5, 6],
                        help="1: Grid, 2: Romania, 5: Water Jugs, 6: Vacuum World")
    parser.add_argument('--speed', type=float, default=0.5)
    args = parser.parse_args()

    if PYGAME_AVAILABLE:
        import pygame
        pygame.init()

    # Problems 1, 2, 5, and 6
    problems = {
        1: GridProblem(),
        2: RomaniaProblem(),
        5: WaterJugsProblem(),
        6: VacuumProblem()
    }
    visualizers = {
        1: visualize_grid,
        2: visualize_graph,
        5: visualize_water_jugs,
        6: visualize_vacuum
    }

    problem = problems[args.problem]
    visualize = visualizers[args.problem] if PYGAME_AVAILABLE else None

    strategies = {
        'bfs': bfs,
        'dfs': dfs,
        'ucs': ucs,
        'greedy': greedy,
        'astar': astar
    }

    search_func = strategies[args.strategy]
    path, expanded, max_f = search_func(problem, visualize, args.speed)

    print(f"\nPath: {path}\nExpanded: {expanded}\nMax Frontier: {max_f}")
    if path:
        print(f"Cost: {path_cost(problem, path)}")

    if PYGAME_AVAILABLE:
        wait_for_close()


if __name__ == "__main__":
    main()