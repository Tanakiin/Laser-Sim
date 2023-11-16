class Laser:
    las_dir = {"u":"△", "r":"▷", "d":"▽", "l":"◁"}

    def __init__(self, direction):
        if direction not in self.las_dir.keys():
            raise ValueError("Invalid direction. Valid directions are 'u', 'r', 'd', 'l'.")
        self.direction = direction
        self.type = "l"

    def __repr__(self):
        return self.las_dir[self.direction]