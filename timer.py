class Timer:

    def __init__(self, refresh):
        self.frame = 0
        self.refresh = refresh
        self.default = self.refresh

    def tick(self):
        self.frame += 1
        if self.frame >= self.refresh:
            self.frame = 0

    def update(self, tick_rate):
        self.refresh = tick_rate

    def reset(self):
        self.frame = 0
        self.refresh = self.default

    def check(self):
        if self.frame == 0:
            return True
        else:
            return False
