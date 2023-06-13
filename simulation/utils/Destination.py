class Destination:
    def __init__(self, id, x, y, is_last=False):
        self.id = id
        self.x = x
        self.y = y
        self.is_last = is_last
    
    def get_position(self):
        return self.x, self.y
