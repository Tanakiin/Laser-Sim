class Beam:
    beam_dir = {"u":"▴", "r":"▸", "d":"▾", "l":"◂"}

    def __init__(self, direction):
        if direction not in self.beam_dir.keys():
            raise ValueError("Invalid direction. Valid directions are 'u', 'r', 'd', 'l'.")
        self.direction = direction
        self.type = "b"
    
    def __repr__(self):
        return self.beam_dir[self.direction]