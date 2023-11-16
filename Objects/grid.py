from .beam import Beam
from .laser import Laser
from .mirror import Mirror
from .log import Log
from .log_pos import LogPosition
from .log_dis import LogDisplay
import copy as c
import numpy as np


class Grid:
    las_dir = {"u":"△", "r":"▷", "d":"▽", "l":"◁"}
    mir_dir = {"r":"⟋", "l":"⟍"}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = np.full((x, y), 0 , dtype=object)
        self.log = Log()
        self.logpos = LogPosition()
        self.logdis = LogDisplay()
        self.log.add(f"created {x} x {y} grid")
        print(self.grid)

    def __repr__(self):
        return str(self.grid)
    
    def to_string(self):
        str = np.array2string(self.grid)
        return str
    
    def place_l(self, x, y, dir):
        if not self.grid[x,y]:
            self.grid[x,y] = Laser(dir)
        else:
            choice = input("That position is occupied! Do you want to overwrite? (y/n):").lower()
            if choice == "y":
                self.grid[x,y] = Laser(dir)
        self.log.add(f"placed laser at ({x},{y}) facing {self.las_dir[dir]}")
        self.logpos.add_pos("l", [x, y, dir])
        print(self.logpos)
        print(self.grid)
    
    def place_m(self, x, y, dir):
        dir = dir[0].lower()
        if not self.grid[x,y]:
            self.grid[x,y] = Mirror(dir)
        else:
            choice = input("That position is occupied! Do you want to overwrite? (y/n):").lower()
            if choice == "y":
                self.grid[x,y] = Mirror(dir)
        self.log.add(f"placed mirror at ({x},{y}) facing {self.mir_dir[dir]}")
        self.logpos.add_pos("m", [x, y, dir])
        print(self.grid)

    def remove(self, x, y):
        obj = self.grid[x,y]
        self.grid[x,y] = 0
        self.log.add(f"removed {obj} at ({x},{y})")
        print(self.grid)

    def get_laser(self):
        return self.logpos.get_las()[0]
    
    def get_mirror(self):
        return self.logpos.get_mir()
    
    def shoot(self):
        las_pos = c.copy(self.get_laser())
        self.log.log_ord.append(tuple(las_pos[0:2]))
        mir_pos = self.get_mirror()
        mir_pos_coord = [[i[0], i[1]] for i in mir_pos]
        hit_wall = False
        while not hit_wall and las_pos[0] >= 0 and las_pos[1] >= 0:
            print(self.logpos)
            if las_pos[-1] == "u":
                try:
                    las_pos[0] -= 1
                    if las_pos[0] < 0 or las_pos[1] < 0:
                        raise IndexError("Negative index not allowed")
                    if las_pos[0:2] in mir_pos_coord:
                        self.log.log_ord.append(tuple(las_pos[0:2]))
                        idx = mir_pos_coord.index(las_pos[0:2])
                        mdir = mir_pos[idx][-1]
                        if mdir == "r":
                            las_pos[1] += 1
                            las_pos[-1] = "r"
                            self.grid[las_pos[0], las_pos[1]] = Beam("r")
                        elif mdir == "l":
                            las_pos[1] -= 1
                            las_pos[-1] = "l"
                            if las_pos[0] < 0 or las_pos[1] < 0:
                                raise IndexError("Negative index not allowed")
                            self.grid[las_pos[0], las_pos[1]] = Beam("l")
                    else:
                        self.grid[las_pos[0], las_pos[1]] = Beam("u")

                except IndexError:
                    hit_wall = True
            if las_pos[-1] == "r":
                try:
                    las_pos[1] += 1
                    if las_pos[0] < 0 or las_pos[1] < 0:
                        raise IndexError("Negative index not allowed")
                    if las_pos[0:2] in mir_pos_coord:
                        self.log.log_ord.append(tuple(las_pos[0:2]))
                        idx = mir_pos_coord.index(las_pos[0:2])
                        mdir = mir_pos[idx][-1]
                        if mdir == "r":
                            las_pos[0] -= 1
                            las_pos[-1] = "u"
                            if las_pos[0] < 0 or las_pos[1] < 0:
                                raise IndexError("Negative index not allowed")
                            self.grid[las_pos[0], las_pos[1]] = Beam("u")
                        elif mdir == "l":
                            las_pos[0] += 1
                            las_pos[-1] = "d"
                            self.grid[las_pos[0], las_pos[1]] = Beam("d")
                    else:
                        self.grid[las_pos[0], las_pos[1]] = Beam("r")
                except IndexError:
                    hit_wall = True
            if las_pos[-1] == "d":
                try:
                    las_pos[0] += 1
                    if las_pos[0] < 0 or las_pos[1] < 0:
                        raise IndexError("Negative index not allowed")
                    if las_pos[0:2] in mir_pos_coord:
                        self.log.log_ord.append(tuple(las_pos[0:2]))
                        idx = mir_pos_coord.index(las_pos[0:2])
                        mdir = mir_pos[idx][-1]
                        if mdir == "r":
                            las_pos[1] -= 1
                            las_pos[-1] = "l"
                            if las_pos[0] < 0 or las_pos[1] < 0:
                                raise IndexError("Negative index not allowed")
                            self.grid[las_pos[0], las_pos[1]] = Beam("l")
                        elif mdir == "l":
                            las_pos[1] += 1
                            las_pos[-1] = "r"
                            self.grid[las_pos[0], las_pos[1]] = Beam("r")
                    else:
                        self.grid[las_pos[0], las_pos[1]] = Beam("d")
                except IndexError:
                    hit_wall = True
            if las_pos[-1] == "l":
                try:
                    las_pos[1] -= 1
                    if las_pos[0] < 0 or las_pos[1] < 0:
                        raise IndexError("Negative index not allowed")
                    if las_pos[0:2] in mir_pos_coord:
                        self.log.log_ord.append(tuple(las_pos[0:2]))
                        idx = mir_pos_coord.index(las_pos[0:2])
                        mdir = mir_pos[idx][-1]
                        if mdir == "r":
                            las_pos[0] += 1
                            las_pos[-1] = "d"
                            self.grid[las_pos[0], las_pos[1]] = Beam("d")
                        elif mdir == "l":
                            las_pos[0] -= 1
                            las_pos[-1] = "u"
                            if las_pos[0] < 0 or las_pos[1] < 0:
                                raise IndexError("Negative index not allowed")
                            self.grid[las_pos[0], las_pos[1]] = Beam("u")
                    else:
                        self.grid[las_pos[0], las_pos[1]] = Beam("l")
                except IndexError:
                    hit_wall = True
            temp_grid = c.copy(self.grid)
            self.logdis.add_dis(temp_grid)
        self.log.log_ord.append(tuple(las_pos[0:2]))
        self.log.add(f"shot the laser")


    def reset(self):
        self.grid = np.full((self.x, self.y), 0 , dtype=object)
        self.logpos = LogPosition()
        self.log.log_ord = []
        self.log.add(f"reset the grid")

        print(self.grid)
    
    def pl(self, x, y, dir):
        self.place_l(x, y, dir)
    
    def pm(self, x, y, dir):
        self.place_m(x, y, dir)

    def rm(self, x, y):
        self.remove(x, y)