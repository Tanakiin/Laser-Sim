class Mirror:
    mir_dir = {"r":"⟋", "l":"⟍"}

    def __init__(self, direction):
        if direction not in self.mir_dir.keys():
            raise ValueError("Invalid direction. Valid directions are 'r' and 'l'.")
        self.direction = direction
        self.type = "m"

    def __repr__(self):
        return self.mir_dir[self.direction]