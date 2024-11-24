import random
import time
from constants import GRID_WIDTH, GRID_HEIGHT

class Food:
    def __init__(self, snake, is_big=False):
        self.is_big = is_big
        self.spawn_time = time.time()
        self.time_limit = 10
        self.position = self.generate_position(snake)
        
    def generate_position(self, snake):
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), 
                  random.randint(0, GRID_HEIGHT-1))
            if self.is_big:
                if pos[0] == GRID_WIDTH-1 or pos[1] == GRID_HEIGHT-1:
                    continue
                positions = [
                    pos,
                    (pos[0]+1, pos[1]),
                    (pos[0], pos[1]+1),
                    (pos[0]+1, pos[1]+1)
                ]
                if not any(p in snake.body for p in positions):
                    return pos
            else:
                if pos not in snake.body:
                    return pos
                    
    def get_remaining_time(self):
        if not self.is_big:
            return 1.0
        elapsed_time = time.time() - self.spawn_time
        remaining_ratio = max(0, (self.time_limit - elapsed_time) / self.time_limit)
        return remaining_ratio 