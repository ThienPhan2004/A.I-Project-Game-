from constants import GRID_WIDTH, GRID_HEIGHT

class Snake:
    def __init__(self):
        # Khởi tạo các thuộc tính của rắn
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]  # Vị trí ban đầu của rắn ở giữa lưới (tức giữa bản đồ)
        self.direction = (1, 0)  # Hướng di chuyển ban đầu (phải)
        self.grow = False  # Biến đánh dấu xem rắn có cần lớn lên hay không
        self.map_type = 0  # Loại bản đồ (có thể sử dụng cho các chế độ khác nhau)

    def reset(self):
        # Đặt lại trạng thái của rắn
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]  # Đặt lại vị trí ban đầu
        self.direction = (1, 0)  # Đặt lại hướng di chuyển
        self.grow = False  # Đặt lại trạng thái lớn lên

    def move(self):
        # Di chuyển rắn theo hướng hiện tại
        head = self.body[0]  # Lấy vị trí đầu của rắn
        new_x = (head[0] + self.direction[0]) % GRID_WIDTH  # Tính toán vị trí mới theo chiều ngang
        new_y = (head[1] + self.direction[1]) % GRID_HEIGHT  # Tính toán vị trí mới theo chiều dọc
        new_head = (new_x, new_y)  # Tạo vị trí đầu mới
        
        if not self.grow:
            self.body.pop()  # Nếu không cần lớn lên, xóa đuôi rắn
        else:
            self.grow = False  # Nếu cần lớn lên, đặt lại trạng thái lớn lên
            
        self.body.insert(0, new_head)  # Thêm đầu mới vào vị trí đầu rắn
        
    def check_collision(self):
        # Kiểm tra va chạm của rắn
        head = self.body[0]  # Lấy vị trí đầu của rắn
        return head in self.body[1:]  # Kiểm tra xem đầu rắn có va chạm với thân không