# !/usr/bin/env python

import numpy
import pygame

from terrain.generator import TerrainGenerator

class MapLayer(object):
    def __init__(self, size, val=0, valtype=numpy.object_):
        self.size = self.width, self.height = size
        self.values = numpy.empty(size, valtype)
        self.values.fill(val)

    def get(self, x, y):
        if y >= 0 and x >= 0:
            try:
                return self.values[x, y]
            except IndexError:
                return None
        return None

    def set(self, x, y, val):
        self.values[x, y] = val

    def in_range(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


class ScalarMapLayer(MapLayer):
    def set_random(self, range, symmetric=True):
        self.values = TerrainGenerator().create_random(self.size, range,
                                                        symmetric)

    def set_streak(self, range, symmetric=True):
        self.values = TerrainGenerator().create_streak(self.size, range,
                                                        symmetric)

    def set_simple(self, range, symmetric=True):
        self.values = TerrainGenerator().create_simple(self.size, range,
                                                        symmetric)

    def set_perlin(self, range, symmetric=True):
        self.values = TerrainGenerator().create_perlin(self.size, range,
                                                        symmetric)

    def change(self, x, y, val):
        self.values[x, y] += val


class ObjectMapLayer(MapLayer):
    def __init__(self, size):
        MapLayer.__init__(self, size, None, numpy.object_)
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0, 0, 0))
        self.surf.fill((0, 0, 0))
        self.pixels = None

    #        self.pixels = pygame.PixelArray(self.surf)

    def lock(self):
        self.pixels = pygame.surfarray.pixels2d(self.surf)

    def unlock(self):
        self.pixels = None

    def get_small_view_fast(self, x, y):
        ret = []
        get = self.get
        append = ret.append
        width = self.width
        height = self.height
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx or dy):
                    continue
                try:
                    adj_x = x + dx
                    if not 0 <= adj_x < width:
                        continue
                    adj_y = y + dy
                    if not 0 <= adj_y < height:
                        continue
                    a = self.values[adj_x, adj_y]
                    if a is not None:
                        append(a.get_view())
                except IndexError:
                    pass
        return ret

    def get_view(self, x, y, r):
        ret = []
        for x_off in range(-r, r + 1):
            for y_off in range(-r, r + 1):
                if x_off == 0 and y_off == 0:
                    continue
                a = self.get(x + x_off, y + y_off)
                if a is not None:
                    ret.append(a.get_view())
        return ret

    def insert(self, list):
        for o in list:
            self.set(o.x, o.y, o)

    def set(self, x, y, val):
        MapLayer.set(self, x, y, val)
        if val is None:
            self.pixels[x][y] = 0
        #            self.surf.set_at((x, y), 0)
        else:
            self.pixels[x][y] = val.color
