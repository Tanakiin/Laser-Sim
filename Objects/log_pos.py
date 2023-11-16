class LogPosition:
    def __init__(self):
        self.log_pos = {"l": [], "m": []}

    def __repr__(self):
        l = f"Laser at {self.log_pos['l']}"
        m = f"Mirrors at {self.log_pos['m']}"
        return l+"\n"+m
    
    def add_pos(self, type, position):
        self.log_pos[type].append(position)

    def get_las(self):
        return self.log_pos['l'] if self.log_pos['l'] else []
    
    def get_mir(self):
        return self.log_pos['m'] if self.log_pos['m'] else []
    