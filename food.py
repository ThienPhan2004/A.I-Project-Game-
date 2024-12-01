import random
import time
from constants import GRID_WIDTH, GRID_HEIGHT

class Food:
    def __init__(self, snake, is_big=False):
        # Khởi tạo các thuộc tính của Food
        self.is_big = is_big
        self.spawn_time = time.time()
        self.time_limit = 10
        self.position = self.generate_position(snake)
        
    def generate_position(self, snake):
        # Tạo ra vị trí ngẫu nhiên mà không trùng với vị trí rắn cho thức ăn
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), 
                  random.randint(0, GRID_HEIGHT-1)) # Vị trí ngẫu nhiên trong lưới
            if self.is_big:
                # Nếu là đồ ăn to, đảm bảo chúng không xuất hiện ở biên
                if pos[0] == GRID_WIDTH-1 or pos[1] == GRID_HEIGHT-1:
                    continue
                positions = [
                    pos,
                    (pos[0]+1, pos[1]),
                    (pos[0], pos[1]+1),
                    (pos[0]+1, pos[1]+1)
                ]
                # Kiểm tra nếu có vị trí nào trùng với vị trí của rắn
                if not any(p in snake.body for p in positions):
                    return pos # Trả về vị trí khả dụng
            else:
                # Các đồ ăn nhỏ, chỉ kiểm tra ở vị trí trống
                if pos not in snake.body:
                    return pos # Trả về vị trí khả dụng
                    
    def get_remaining_time(self):
        # Tính thời gian còn lại của đồ ăn
        if not self.is_big:
            return 1.0 # Đồ ăn bình thường có thời gian còn lại cố định
        elapsed_time = time.time() - self.spawn_time # Tính toán thời gian đã trôi qua
        remaining_ratio = max(0, (self.time_limit - elapsed_time) / self.time_limit)
        return remaining_ratio  # trả về tỉ lệ thời gian còn lại