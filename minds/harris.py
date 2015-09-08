# !/usr/bin/env python
import random
import cells
import math

__author__ = 'matthew harris'


class AgentMind(object):
    def __init__(self, junk):
        self.my_plant = None
        self.mode = 1
        self.radius = 5
        self.gate = 1
        self.target_range = random.randrange(50, 100)

    def act(self, view, msg):
        debug = "off"
        me = view.get_me()
        pos = (mx, my) = me.get_pos()
        radius = self.radius
        gate = self.gate
        self.get_plant(view)
        terrain = view.get_terr().values

        # Eat if hungry or if this is an exceptionally energy-rich spot.
        full = me.energy >= (cells.ENERGY_CAP / 2)
        hungry = (me.energy < self.target_range)
        energy_here = view.get_energy().get(mx, my)
        food = (energy_here > 0)
        if not full and ((hungry and food) or energy_here > 100):
            debug = "eat1"
            action = cells.ACT_EAT
        elif hungry:
            #(mx, my) = self.my_plant.get_pos()
            #(dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
            (dx, dy) = dir_to(pos, self.my_plant.get_pos())
            pos = (mx + dx, my + dy)
            debug = "move1"
            action = cells.ACT_MOVE
            while not can_move(view, pos):
                (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                pos = (mx + dx, my + dy)
                debug = "move1.1"
        elif self.my_plant:
            plant_pos = self.my_plant.get_pos()
            plant_dist = length(
                abs(pos[0] - plant_pos[0]),
                abs(pos[1] - plant_pos[1]))
            if (not me.loaded and
                    # (plant_dist % radius or abs(mx - plant_pos[0]) < gate) and
                    (plant_dist > radius or (plant_dist < radius and plant_dist < terrain[mx][my])) and
                    can_lift(view)):
                # always lift towards the plant
                # Check that the lift won't take too much dirt
                debug = "lift1"
                action = cells.ACT_LIFT
            elif (me.loaded and
                      ((plant_dist == radius and abs(mx - plant_pos[0]) >= gate) or
                      terrain[mx][my] < plant_dist < radius)):
                # always drop away from the plant
                # Make sure that the drop won't leave it stranded on the wall (may be done as another check elsewhere)
                debug = "drop1"
                action = cells.ACT_DROP
            else:
                plant_pos = self.my_plant.get_pos()
                (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                plant_dist = length(
                   abs(pos[0] + dx - plant_pos[0]),
                   abs(pos[1] + dy - plant_pos[1]))
                if plant_dist > (1.5 * radius):     # Move back towards the plant if too far away
                   (dx, dy) = (dx * -1, dy * -1)
                pos = (mx + dx, my + dy)
                action = cells.ACT_MOVE
                debug = "move2"
                while not can_move(view, pos):
                    debug = "move2.1"
                    (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                    pos = (mx + dx, my + dy)
        else:
            (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
            pos = (mx + dx, my + dy)
            action = cells.ACT_MOVE
            debug = "move3"
            while not can_move(view, pos):
                debug = "move3.1"
                (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                pos = (mx + dx, my + dy)

        #if me.get_team() == 0:
        print(self.display(view, action, pos))
        print(debug)
            #(dir_x, dir_y) = dir_to(pos, self.my_plant.get_pos())
            #print("Me: %d Plant: %d" % (my_terrain, plant_dist))
            #print("dir_to: %d, %d" % (dir_x, dir_y))
            #values = view.get_terr().values
            #(cur_x, cur_y) = me.get_pos()
            #print("\t%d" % values[cur_x][cur_y + 1])
            #print("%d\t%d\t%d" % (values[cur_x - 1][cur_y], values[cur_x][cur_y], values[cur_x + 1][cur_y]))
            #print("\t%d" % values[cur_x][cur_y - 1])
        return cells.Action(action, pos)

    def display(self, view, action, pos):
        me = view.get_me()
        (mx, my) = me.get_pos()
        (dx, dy) = pos
        local_energy = view.get_energy().get(mx, my)
        if self.my_plant:
            my_plant = self.my_plant
        else:
            my_plant = "None"
        output = "\n%s" % (me)
        output += "\nRange(%d) Energy(%d) Action(%s) new(%d, %d)" % ( self.target_range, local_energy, cells.ACTIONS[action], dx, dy)
        output += "\n%s" % (my_plant)
        output += "\n" + self.display_plant(view)
        return output;

    def get_plant(self, view):
        # Attach to the strongest plant found.
        for plant in view.get_plants():
            if not self.my_plant:
                self.my_plant = plant
            elif self.my_plant.eff < plant.eff:
                self.my_plant = plant

    def display_plant(self, view):
        plant = self.my_plant
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

    def find_move(self, view):
        (mx, my) = view.get_me().get_pos
        (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
        if self.my_plant:
            (px, py) = self.my_plant.get_pos
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

def can_move(view, pos):
    (mx, my) = view.get_me().get_pos()
    (dx, dy) = pos
    map = view.get_terr()
    if (map.in_range(mx, my) and map.in_range(dx, dy) and
            abs(map.values[dx][dy] - map.values[mx][my]) <= cells.HEIGHT_DIFF):
        return True
    else:
        return False


def can_lift(view):       # Check if this is becoming a pit
    me = view.get_me()
    (mx, my) = me.get_pos()
    terrain = view.get_terr().values
    map = view.get_terr()
    my_terrain = terrain[mx][my]
    if (check_terr(map, mx + 1, my, my_terrain) and
            check_terr(map, mx - 1, my, my_terrain) and
            check_terr(map, mx, my, my_terrain + 1) and
            check_terr(map, mx, my, my_terrain - 1)):
        return False
    elif map.in_range(mx, my) and terrain[mx][my] > 0:
        return True
    else:
        return False


def check_terr(map, x, y, my_terrain):
    if map.in_range(x, y):
        if my_terrain - map.values[x][y] < -1:
            return True
        else:
            return False
    else:
        return True


def dir_to(cur_pos, new_pos):
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


def length(a, b):
    return int(math.sqrt((a * a) + (b * b)))
