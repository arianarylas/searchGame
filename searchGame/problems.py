"""
Defines the SearchProblem interface and problem formulations for:
- Problem 1: Grid Pathfinding
- Problem 2: Romania Map
- Problem 5: Vaccum Worlds
- Problem 6: Vacuum World (2 Rooms)
"""

class SearchProblem:
    def get_start_state(self):
        raise NotImplementedError

    def is_goal(self, state):
        raise NotImplementedError

    def get_successors(self, state):
        raise NotImplementedError

    def heuristic(self, state):
        return 0


class GridProblem(SearchProblem):
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
        successors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and (nx, ny) not in self.obstacles:
                successors.append(((nx, ny), f"Move ({dx}, {dy})", 1))
        return successors

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])


class RomaniaProblem(SearchProblem):
    def __init__(self):
        self.start = 'Arad'
        self.goal = 'Bucharest'
        self.graph = {
            'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
            'Zerind': [('Arad', 75), ('Oradea', 71)],
            'Oradea': [('Zerind', 71), ('Sibiu', 151)],
            'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
            'Timisoara': [('Arad', 118), ('Lugoj', 111)],
            'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
            'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
            'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
            'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
            'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
            'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
            'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
            'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
            'Giurgiu': [('Bucharest', 90)],
            'Urziceni': [('Bucharest', 85), ('Vaslui', 142), ('Hirsova', 98)],
            'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
            'Eforie': [('Hirsova', 86)],
            'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
            'Iasi': [('Vaslui', 92), ('Neamt', 87)],
            'Neamt': [('Iasi', 87)]
        }
        self.h = {
            'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242,
            'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151,
            'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
            'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193, 'Sibiu': 253,
            'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
        }
        self.positions = {
            'Arad': (53, 194), 'Zerind': (82, 124), 'Oradea': (115, 52),
            'Sibiu': (250, 257), 'Timisoara': (58, 342), 'Lugoj': (178, 398),
            'Mehadia': (184, 470), 'Drobeta': (178, 542), 'Craiova': (328, 562),
            'Rimnicu Vilcea': (294, 342), 'Fagaras': (417, 272), 'Pitesti': (442, 418),
            'Bucharest': (578, 491), 'Giurgiu': (536, 594), 'Urziceni': (673, 450),
            'Hirsova': (806, 450), 'Eforie': (853, 553), 'Vaslui': (763, 281),
            'Iasi': (702, 169), 'Neamt': (588, 113)
        }

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def get_successors(self, state):
        return [(city, f"Go to {city}", cost) for city, cost in self.graph.get(state, [])]

    def heuristic(self, state):
        return self.h.get(state, 0)


class VacuumProblem(SearchProblem):
    def __init__(self):

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        _, dirty_a, dirty_b = state
        return dirty_a == 0 and dirty_b == 0

    def get_successors(self, state):
        loc, dirty_a, dirty_b = state
        successors = []
        if loc == 'A' and dirty_a:
            successors.append((('A', 0, dirty_b), "Suck", 1))
        if loc == 'B' and dirty_b:
            successors.append((('B', dirty_a, 0), "Suck", 1))
        if loc == 'B':
            successors.append((('A', dirty_a, dirty_b), "Left", 1))
        if loc == 'A':
            successors.append((('B', dirty_a, dirty_b), "Right", 1))
        return successors

    def heuristic(self, state):
        _, dirty_a, dirty_b = state
        return dirty_a + dirty_b
class WaterJugsProblem(SearchProblem):
    def __init__(self):
        self.start = (0, 0)
        self.capacities = (4, 3)

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state[0] == 2

    def get_successors(self, state):
        j1, j2 = state
        cap1, cap2 = self.capacities
        succ = []

        # 1. Fill jugs
        if j1 < cap1:
            succ.append(((cap1, j2), "Fill 4L", 1))
        if j2 < cap2:
            succ.append(((j1, cap2), "Fill 3L", 1))

        # 2. Empty jugs
        if j1 > 0:
            succ.append(((0, j2), "Empty 4L", 1))
        if j2 > 0:
            succ.append(((j1, 0), "Empty 3L", 1))

        # 3. Pour 4L -> 3L
        pour_to_3 = min(j1, cap2 - j2)
        if pour_to_3 > 0:
            succ.append(((j1 - pour_to_3, j2 + pour_to_3), "Pour 4L to 3L", 1))

        # 4. Pour 3L -> 4L
        pour_to_4 = min(j2, cap1 - j1)
        if pour_to_4 > 0:
            succ.append(((j1 + pour_to_4, j2 - pour_to_4), "Pour 3L to 4L", 1))

        return succ

    def heuristic(self, state):
        # Admissible & consistent: 0 if at goal, 1 otherwise
        return 0 if state[0] == 2 else 1