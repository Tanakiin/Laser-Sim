class Log:
    def __init__(self):
        self.log_data = []
        self.log_ord = []
    def __repr__(self):
        out = [f"{i+1}. {x}" for i, x in enumerate(self.log_data)]
        return '\n'.join(out)

    def add(self, values):
        self.log_data.append(values)