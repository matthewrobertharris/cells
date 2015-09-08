# !/usr/bin/env python
import random

import cells
from harris.helpers import Helper

__author__ = 'matthew harris'


class AgentMind(object):
    def __init__(self, junk):
        self.my_plant = None
        self.mode = 1
        self.radius = 5
        self.gate = 1
        self.target_range = random.randrange(50, 100)
        self.helper = Helper()


    def act(self, view, msg):
        debug = "off"
        me = view.get_me()
        pos = (mx, my) = me.get_pos()
        radius = self.radius
        gate = self.gate
        self.get_plant(view)
        terrain = view.get_terr().values
        helper = self.helper

        # Eat if hungry or if this is an exceptionally energy-rich spot.
        full = me.energy >= (cells.ENERGY_CAP / 2)
        hungry = (me.energy < self.target_range)
        energy_here = view.get_energy().get(mx, my)
        food = (energy_here > 0)
        if not full and ((hungry and food) or energy_here > 100):
            debug = "eat1"
            action = cells.ACT_EAT
        elif hungry:
            (dx, dy) = helper.dir_to(pos, self.my_plant.get_pos())
            pos = (mx + dx, my + dy)
            debug = "move1"
            action = cells.ACT_MOVE
            while not helper.can_move(view, pos):
                pos = self.hungry_move(view)
                debug = "move1.1"
        elif self.my_plant:
            plant_pos = (px, py) = self.my_plant.get_pos()
            plant_terrain = terrain[px][py]
            plant_dist = helper.length(
                abs(pos[0] - plant_pos[0]),
                abs(pos[1] - plant_pos[1]))
            if (not me.loaded and
                    (plant_dist > radius or (plant_dist < radius and plant_dist < terrain[mx][my])) and
                    #(plant_dist > radius or (plant_dist < radius and plant_dist + plant_terrain < terrain[mx][my])) and
                    #(plant_dist > radius or (plant_dist < radius and plant_dist + terrain[mx][my]) >  radius) and
                    helper.can_lift(view)):
                # always lift towards the plant
                # Check that the lift won't take too much dirt
                debug = "lift1"
                action = cells.ACT_LIFT
            elif (me.loaded and
                        ((plant_dist == radius and abs(mx - plant_pos[0]) >= gate) or
                        terrain[mx][my] < plant_dist < radius)):
                        #(plant_dist < radius and plant_dist + plant_terrain > terrain[mx][my]))):
                      #terrain[mx][my] + plant_dist < radius)):
                # always drop away from the plant
                # Make sure that the drop won't leave it stranded on the wall (may be done as another check elsewhere)
                debug = "drop1"
                action = cells.ACT_DROP
            else:
                plant_pos = self.my_plant.get_pos()
                (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                plant_dist = helper.length(
                   abs(pos[0] + dx - plant_pos[0]),
                   abs(pos[1] + dy - plant_pos[1]))
                if plant_dist > (1.5 * radius):     # Move back towards the plant if too far away
                   (dx, dy) = (dx * -1, dy * -1)
                pos = (mx + dx, my + dy)
                action = cells.ACT_MOVE
                debug = "move2"
                while not helper.can_move(view, pos):
                    debug = "move2.1"
                    (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                    pos = (mx + dx, my + dy)
        else:
            (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
            pos = (mx + dx, my + dy)
            action = cells.ACT_MOVE
            debug = "move3"
            while not helper.can_move(view, pos):
                debug = "move3.1"
                (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                pos = (mx + dx, my + dy)

        print(helper.display(view, action, pos, self))
        print(debug)

        return cells.Action(action, pos)

    def get_plant(self, view):
        # Attach to the strongest plant found.
        for plant in view.get_plants():
            if not self.my_plant:
                self.my_plant = plant
            elif self.my_plant.eff < plant.eff:
                self.my_plant = plant

    def hungry_move(self, view):
        pos = (mx, my) = view.get_me().get_pos()
        (dx, dy) = (0, 0)
        if not self.my_plant:
            # There is no plant, so no walls, so unknown to why it is stuck
            (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
            print("no plant")
        else:
            plant_pos = (px, py) = self.my_plant.get_pos()
            plant_dist = self.helper.length(
                abs(mx - px),
                abs(my - py))
            if plant_dist > self.radius:
                # Then it is likely to be outside the walls
                if mx == px:
                    # gate entry
                    (dx, dy) = self.helper.dir_to(pos, plant_pos)
                    print("at gate")
                elif mx > px:
                    if my > py:
                        # top right corner
                        (dx, dy) = (-1, 1)
                        print("top right")
                        new_pos = (mx + dx, my + dy)
                        if not self.helper.can_move(view, new_pos):
                            (dx, dy) = (0, 1)
                            print("top right stuck")
                    else:
                        # bottom right corner
                        (dx, dy) = (-1, -1)
                        print("bottom right")
                        new_pos = (mx + dx, my + dy)
                        if not self.helper.can_move(view, new_pos):
                            (dx, dy) = (0, -1)
                            print("bottom right stuck")
                else:
                    if my > py:
                        # top left corner
                        (dx, dy) = (1, 1)
                        print("top left")
                        new_pos = (mx + dx, my + dy)
                        if not self.helper.can_move(view, new_pos):
                            (dx, dy) = (0, 1)
                            print("top left stuck")
                    else:
                        # bottom left corner
                        (dx, dy) = (1, -1)
                        print("bottom left")
                        new_pos = (mx + dx, my + dy)
                        if not self.helper.can_move(view, new_pos):
                            (dx, dy) = (0, -1)
                            print("bottom left stuck")
            else:
                # Unknown to why it is stuck
                (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
                print("stuck")

        # if this wasn't successful then just randomly move
        new_pos = (mx + dx, my + dy)
        if not self.helper.can_move(view, new_pos):
            (dx, dy) = (random.randrange(-1, 2), random.randrange(-1, 2))
            print("still stuck")

        return mx + dx, my + dy