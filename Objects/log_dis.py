class LogDisplay:
    def __init__(self):
        self.log_dis = []

    def __repr__(self):
        out = "\n".join(self.log_dis)
        return out
    
    def add_dis(self, grid):
        self.log_dis.append(grid)
