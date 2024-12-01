from collections import deque

from collections import deque

def get_neighbors(pos, snake_body, grid_width, grid_height):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # lên, xuống, trái, phải
    # up, down, left, right
    neighbors = []
    
    for dx, dy in directions:
        new_x = (pos[0] + dx) % grid_width
        new_y = (pos[1] + dy) % grid_height
        new_pos = (new_x, new_y)
        
        # Kiểm tra va chạm với thân rắn (trừ đuôi vì nó sẽ di chuyển)
        if new_pos not in snake_body[:-1]:
            neighbors.append((new_pos, (dx, dy)))  # Thêm vị trí lân cận vào danh sách
            
    return neighbors

def bfs_next_move(snake, food, grid_width, grid_height):
    start = snake.body[0]  # Lấy vị trí đầu rắn
    queue = deque([(start, [])])  # Khởi tạo hàng đợi với vị trí bắt đầu
    visited = {start}  # Đánh dấu vị trí đã thăm
    
    while queue:
        pos, path = queue.popleft()  # Lấy vị trí và đường đi từ hàng đợi
        
        # Tìm thấy thức ăn
        if pos == food.position:
            if not path:
                # Nếu đang ở vị trí thức ăn, giữ hướng hiện tại
                return snake.direction
            # Trả về hướng đầu tiên trong đường đi
            return path[0]
        
        # Lấy các ô lân cận hợp lệ
        neighbors = get_neighbors(pos, snake.body, grid_width, grid_height)
        for next_pos, direction in neighbors:
            if next_pos not in visited:
                visited.add(next_pos)  # Đánh dấu ô đã thăm
                new_path = path + [direction]  # Cập nhật đường đi
                queue.append((next_pos, new_path))  # Thêm ô lân cận vào hàng đợi
    
    # Không tìm thấy đường đến thức ăn, tìm đường đi an toàn nhất
    # Ưu tiên đi về phía có nhiều ô trống nhất
    head = snake.body[0]
    best_direction = snake.direction
    max_empty_spaces = -1
    
    for next_pos, direction in get_neighbors(head, snake.body, grid_width, grid_height):
        empty_spaces = count_empty_spaces(next_pos, snake.body, grid_width, grid_height)  # Đếm số ô trống
        # Count the number of empty spaces
        if empty_spaces > max_empty_spaces:
            max_empty_spaces = empty_spaces  # Cập nhật số ô trống tối đa
            best_direction = direction  # Cập nhật hướng tốt nhất
    
    return best_direction  # Trả về hướng tốt nhất

def count_empty_spaces(start, snake_body, grid_width, grid_height):
    """Đếm số ô trống có thể đi được từ một vị trí"""
    # Count the number of empty cells that can be reached from a position
    queue = deque([start])  # Khởi tạo hàng đợi với vị trí bắt đầu
    # Initialize the queue with the starting position
    visited = {start}  # Đánh dấu vị trí đã thăm
    
    while queue:
        pos = queue.popleft()  # Lấy vị trí từ hàng đợi
        for next_pos, _ in get_neighbors(pos, snake_body, grid_width, grid_height):
            if next_pos not in visited:
                visited.add(next_pos)  # Đánh dấu ô đã thăm
                queue.append(next_pos)  # Thêm ô lân cận vào hàng đợi
                
    return len(visited)  # Trả về số ô đã thăm