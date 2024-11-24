from constants import GRID_WIDTH, GRID_HEIGHT

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)
        self.grow = False
        self.map_type = 0

    def reset(self):
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)
        self.grow = False
        
    def move(self):
        head = self.body[0]
        new_x = (head[0] + self.direction[0]) % GRID_WIDTH
        new_y = (head[1] + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        self.body.insert(0, new_head)
        
    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:] 