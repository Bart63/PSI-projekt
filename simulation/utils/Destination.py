class Destination:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    
    def get_position(self):
        return self.x, self.y
