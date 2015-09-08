import math
import cells
import random

__author__ = 'matthew harris'


class Helper:

    def can_move(self, view, pos):
        (mx, my) = view.get_me().get_pos()
        (dx, dy) = pos
        map = view.get_terr()
        if map.in_range(mx, my) and map.in_range(dx, dy):
            if (view.get_me().loaded and
                    abs(map.values[dx][dy] - map.values[mx][my]) < cells.HEIGHT_DIFF): # < so it can still get down
                return True
            elif (not view.get_me().loaded and
                          abs(map.values[dx][dy] - map.values[mx][my]) <= cells.HEIGHT_DIFF):
                return True
            else:
                return False
        else:
            return False

    def can_lift(self, view):       # Check if this is becoming a pit
        me = view.get_me()
        (mx, my) = me.get_pos()
        terrain = view.get_terr().values
        map = view.get_terr()
        my_terrain = terrain[mx][my]
        if (self.check_terr(map, mx + 1, my, my_terrain) and
                self.check_terr(map, mx - 1, my, my_terrain) and
                self.check_terr(map, mx, my + 1, my_terrain) and
                self.check_terr(map, mx, my - 1, my_terrain)):
            return False
        elif map.in_range(mx, my) and terrain[mx][my] > 0:
            return True
        else:
            return False

    def check_terr(self, map, x, y, my_terrain):
        if map.in_range(x, y):
            if my_terrain - map.values[x][y] < -1:
                return True
            else:
                return False
        else:
            return True

    def dir_to(self, cur_pos, new_pos):
        (x, y) = cur_pos
        (nx, ny) = new_pos
        (dx, dy) = (nx - x, ny - y)
        if dx == 0:
            dir_x = 0
        else:
            dir_x = dx / abs(dx)
        if dy == 0:
            dir_y = 0
        else:
            dir_y = dy / abs(dy)
        return dir_x, dir_y

    def length(self, a, b):
        return int(math.sqrt((a * a) + (b * b)))

    def display_plant(self, view, plant):
        if not plant:
            return ""
        output = ""
        map = view.get_terr()
        terrain = view.get_terr().values
        pos = plant.get_pos()
        for y in range(-7, 7):
            for x in range(-7, 7):
                if map.in_range(pos[0] + x, pos[1] + y):
                    output += "%d\t" % map.values[pos[0] + x][pos[1] + y]
                else:
                    output += "\t"
            output += "\n"
        return output

    def find_move(self, view, plant):
        (mx, my) = view.get_me().get_pos
        (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
        if plant:
            (px, py) = plant.get_pos
            if mx > px:
                if my > py:
                    (dx, dy) = (0, 0)
                else:
                    (dx, dy) = (0, 0)
            else:
                if my > py:
                    (dx, dy) = (0, 0)
                else:
                    (dx, dy) = (0, 0)
        return dx, dy

    def display(self, view, action, pos, mind):
        me = view.get_me()
        (mx, my) = me.get_pos()
        (dx, dy) = pos
        local_energy = view.get_energy().get(mx, my)
        if mind.my_plant:
            my_plant = mind.my_plant
        else:
            my_plant = "None"
        output = "\n%s" % (me)
        output += "\nRange(%d) Energy(%d) Action(%s) new(%d, %d)" % ( mind.target_range, local_energy, cells.ACTIONS[action], dx, dy)
        output += "\n%s" % (my_plant)
        output += "\n" + self.display_plant(view, my_plant)
        return output;