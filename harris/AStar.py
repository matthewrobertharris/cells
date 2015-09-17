import heapq
import cells

__author__ = 'Matthew Harris'


class AStar(object):

    @staticmethod
    def heuristic(goal, next_move):
        x = abs(goal[0] - next_move[0])
        y = abs(goal[1] - next_move[1])
        return x + y

    @staticmethod
    def a_star_search(start, goal, graph):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + AStar.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        # return came_from, cost_so_far
        return AStar.reconstruct_path(came_from, start, goal)

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class SquareGrid:
    def __init__(self, map_layer, loaded):
        self.loaded = loaded
        self.map = map_layer
        self.size = self.width, self.height = map_layer.size

    def in_bounds(self, id):
        (x, y) = id
        return self.map.in_range(x, y)

    def passable(self, cur_pos, new_pos):
        (mx, my) = cur_pos
        (dx, dy) = new_pos
        if (self.loaded and
                abs(self.map.values[dx][dy] - self.map.values[mx][my]) < cells.HEIGHT_DIFF): # < so it can still get down
            return True
        elif (not self.loaded and
                      abs(self.map.values[dx][dy] - self.map.values[mx][my]) <= cells.HEIGHT_DIFF):
            return True
        else:
            return False

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1),
                   (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(lambda x: self.passable(id, x), results)
        return results

    def cost(self, current, next):
        if current[0] == next[0] or current[1] == next[1]:
            return 1
        else:
            return 1    # Change this to make diagonal moves cost more


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]