"""
Pygame visualization functions for Grid, Graph (Romania), and Vacuum worlds.
"""

import sys

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
    'obstacle': (100, 100, 100),
    'start': (0, 150, 255)
}


def wait_for_close():
    if not PYGAME_AVAILABLE:
        return
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                return
        pygame.time.wait(50)


def visualize_vacuum(problem, explored, frontier, current, came_from):
    if not PYGAME_AVAILABLE:
        return
    screen = pygame.display.set_mode((600, 380))
    screen.fill(COLORS['bg'])
    font = pygame.font.SysFont(None, 28)
    small = pygame.font.SysFont(None, 22)
    loc, dirty_a, dirty_b = current
    rooms = {'A': (50, 60), 'B': (310, 60)}
    dirt = {'A': dirty_a, 'B': dirty_b}

    for name, (x, y) in rooms.items():
        rect = pygame.Rect(x, y, 240, 200)
        bg_col = (220, 255, 220) if not dirt[name] else COLORS['bg']
        pygame.draw.rect(screen, bg_col, rect)
        pygame.draw.rect(screen, COLORS['grid'], rect, 2)
        screen.blit(font.render(f"Room {name}", True, COLORS['grid']), (x + 10, y + 10))

        if dirt[name]:
            for dx, dy in [(60, 150), (100, 170), (150, 145), (190, 175), (80, 120)]:
                pygame.draw.circle(screen, (120, 80, 40), (x + dx, y + dy), 8)

        if loc == name:
            pygame.draw.circle(screen, COLORS['current'], (x + 120, y + 100), 30)
            screen.blit(small.render("Robot", True, COLORS['bg']), (x + 97, y + 92))

    info = f"State: {current} | Explored: {len(explored)} | Frontier: {len(frontier)}"
    screen.blit(small.render(info, True, COLORS['grid']), (50, 290))
    if problem.is_goal(current):
        screen.blit(font.render("Goal reached: both rooms clean!", True, (0, 150, 0)), (50, 320))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit(0)


def visualize_graph(problem, explored, frontier, current, came_from):
    if not PYGAME_AVAILABLE:
        return
    screen = pygame.display.set_mode((900, 650))
    screen.fill(COLORS['bg'])
    font = pygame.font.SysFont(None, 18)

    drawn = set()
    for city, neighbors in problem.graph.items():
        for neighbor, cost in neighbors:
            edge = frozenset((city, neighbor))
            if edge in drawn:
                continue
            drawn.add(edge)
            p1, p2 = problem.positions[city], problem.positions[neighbor]
            pygame.draw.line(screen, COLORS['grid'], p1, p2, 1)
            mid = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
            screen.blit(font.render(str(cost), True, (120, 120, 120)), mid)

    for city, pos in problem.positions.items():
        if city == current:
            color = COLORS['current']
        elif city == problem.goal:
            color = COLORS['goal']
        elif city == problem.get_start_state():
            color = COLORS['start']
        elif city in explored:
            color = COLORS['explored']
        elif city in frontier:
            color = COLORS['frontier']
        else:
            color = COLORS['bg']
        pygame.draw.circle(screen, color, pos, 14)
        pygame.draw.circle(screen, COLORS['grid'], pos, 14, 1)
        screen.blit(font.render(city, True, COLORS['grid']), (pos[0] + 16, pos[1] - 8))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit(0)


def visualize_grid(problem, explored, frontier, current, came_from):
    if not PYGAME_AVAILABLE:
        return
    from algorithms import reconstruct_path
    screen = pygame.display.set_mode((problem.grid_size * CELL_SIZE, problem.grid_size * CELL_SIZE))
    screen.fill(COLORS['bg'])

    for x in range(problem.grid_size):
        for y in range(problem.grid_size):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS['grid'], rect, 1)
            state = (x, y)
            if state in problem.obstacles:
                pygame.draw.rect(screen, COLORS['obstacle'], rect)
            elif state == problem.get_start_state():
                pygame.draw.rect(screen, COLORS['start'], rect)
            elif state == problem.goal:
                pygame.draw.rect(screen, COLORS['goal'], rect)
            elif state in explored:
                pygame.draw.rect(screen, COLORS['explored'], rect)
            elif state in frontier:
                pygame.draw.rect(screen, COLORS['frontier'], rect)

    path = None
    if current is not None and problem.is_goal(current):
        path = reconstruct_path(came_from, current)
        for px, py in path:
            if (px, py) != problem.start and (px, py) != problem.goal:
                rect = pygame.Rect(px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS['path'], rect)
                pygame.draw.rect(screen, COLORS['grid'], rect, 1)
        centers = [(px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2) for px, py in path]
        if len(centers) > 1:
            pygame.draw.lines(screen, (200, 150, 0), False, centers, 6)

    if current and path is None:
        rect = pygame.Rect(current[0] * CELL_SIZE, current[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLORS['current'], rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit(0)
def visualize_water_jugs(problem, explored, frontier, current, came_from):
    if not PYGAME_AVAILABLE:
        return
    screen = pygame.display.set_mode((500, 450))
    screen.fill(COLORS['bg'])
    font = pygame.font.SysFont(None, 26)
    small = pygame.font.SysFont(None, 20)

    j1, j2 = current

    # Dimensions
    jug1_rect = (100, 120, 100, 200)
    jug2_rect = (280, 170, 100, 150)

    # Outlines
    pygame.draw.rect(screen, COLORS['grid'], jug1_rect, 3)
    pygame.draw.rect(screen, COLORS['grid'], jug2_rect, 3)

    # Water fills
    fill1_h = int((j1 / 4.0) * 200)
    fill2_h = int((j2 / 3.0) * 150)
    water_color = (65, 145, 255)

    if fill1_h > 0:
        pygame.draw.rect(screen, water_color, (100 + 3, 120 + 200 - fill1_h, 100 - 6, fill1_h))
    if fill2_h > 0:
        pygame.draw.rect(screen, water_color, (280 + 3, 170 + 150 - fill2_h, 100 - 6, fill2_h))

    # Text
    screen.blit(font.render(f"4L Jug: {j1}L", True, COLORS['grid']), (100 + 10, 330))
    screen.blit(font.render(f"3L Jug: {j2}L", True, COLORS['grid']), (280 + 10, 330))

    info = f"State: {current} | Explored: {len(explored)} | Frontier: {len(frontier)}"
    screen.blit(small.render(info, True, COLORS['grid']), (40, 370))

    if problem.is_goal(current):
        screen.blit(font.render("Goal reached: 2L in 4L jug!", True, (0, 150, 0)), (40, 400))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit(0)