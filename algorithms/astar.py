import heapq

def manhattan_distance(pos1, pos2):
    # Tính khoảng cách Manhattan giữa hai vị trí
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_valid_directions(current_direction):
    """Trả về các hướng hợp lệ dựa trên hướng hiện tại"""
    # Mapping của các hướng có thể đi được (không quay đầu)
    valid_moves = {
        (0, -1): [(0, -1), (-1, 0), (1, 0)],  # Đang đi lên -> có thể đi lên, trái, phải
        (0, 1): [(0, 1), (-1, 0), (1, 0)],    # Đang đi xuống -> có thể đi xuống, trái, phải
        (-1, 0): [(-1, 0), (0, -1), (0, 1)],  # Đang đi trái -> có thể đi trái, lên, xuống
        (1, 0): [(1, 0), (0, -1), (0, 1)]     # Đang đi phải -> có thể đi phải, lên, xuống
    }
    return valid_moves[current_direction]  # Trả về các hướng hợp lệ

def get_neighbors(pos, snake_body, grid_width, grid_height, current_direction):
    # Lấy các vị trí hàng xóm hợp lệ cho vị trí hiện tại
    valid_directions = get_valid_directions(current_direction)  # Lấy các hướng hợp lệ
    neighbors = []  # Danh sách lưu trữ các hàng xóm hợp lệ
    
    for dx, dy in valid_directions:
        new_x = (pos[0] + dx) % grid_width  # Tính toán vị trí mới theo chiều ngang
        new_y = (pos[1] + dy) % grid_height  # Tính toán vị trí mới theo chiều dọc
        new_pos = (new_x, new_y)  # Tạo vị trí mới
        
        if new_pos not in snake_body:  # Kiểm tra xem vị trí mới có nằm trong thân rắn không
            neighbors.append((new_pos, (dx, dy)))  # Thêm vị trí mới vào danh sách hàng xóm
            
    return neighbors  # Trả về danh sách hàng xóm hợp lệ

def astar_next_move(snake, food, grid_width, grid_height):
    # Tìm nước đi tiếp theo cho rắn sử dụng thuật toán A*
    start = snake.body[0]  # Lấy vị trí đầu của rắn
    goal = food.position  # Lấy vị trí của thức ăn
    current_direction = snake.direction  # Lấy hướng hiện tại của rắn
    
    frontier = [(0, start, [])]  # Danh sách ưu tiên cho các vị trí cần khám phá
    came_from = {start: None}  # Lưu trữ vị trí đã đến từ đâu
    cost_so_far = {start: 0}  # Chi phí để đến vị trí hiện tại
    
    while frontier:  # Trong khi còn vị trí để khám phá
        _, current, path = heapq.heappop(frontier)  # Lấy vị trí có chi phí thấp nhất
        
        if current == goal:  # Nếu đã đến vị trí thức ăn
            if not path:
                return current_direction  # Nếu không có đường đi, trả về hướng hiện tại
            return path[0]  # Trả về hướng đầu tiên trong đường đi
            
        for next_pos, direction in get_neighbors(current, snake.body, grid_width, grid_height, current_direction):
            new_cost = cost_so_far[current] + 1  # Tính toán chi phí mới
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:  # Nếu chi phí mới thấp hơn
                cost_so_far[next_pos] = new_cost  # Cập nhật chi phí
                priority = new_cost + manhattan_distance(next_pos, goal)  # Tính toán độ ưu tiên
                new_path = path + [direction] if not path else [direction]  # Cập nhật đường đi
                heapq.heappush(frontier, (priority, next_pos, new_path))  # Thêm vào danh sách ưu tiên
                came_from[next_pos] = current  # Lưu trữ vị trí đã đến từ đâu
    
    # Nếu không tìm thấy đường đến thức ăn, tìm đường đi an toàn nhất
    if frontier:
        _, _, path = frontier[0]  # Lấy đường đi từ vị trí đầu tiên trong danh sách
        if path:
            return path[0]  # Trả về hướng đầu tiên trong đường đi
    
    # Nếu không tìm được đường đi nào, tiếp tục theo hướng hiện tại nếu an toàn
    next_head = ((start[0] + current_direction[0]) % grid_width,
                 (start[1] + current_direction[1]) % grid_height)  # Tính toán vị trí đầu tiếp theo
    if next_head not in snake.body:  # Kiểm tra xem vị trí tiếp theo có an toàn không
        return current_direction  # Nếu an toàn, trả về hướng hiện tại
        
    # Nếu không an toàn, thử tìm một hướng an toàn khác
    for dx, dy in get_valid_directions(current_direction):
        next_head = ((start[0] + dx) % grid_width,
                    (start[1] + dy) % grid_height)  # Tính toán vị trí tiếp theo
        if next_head not in snake.body:  # Kiểm tra xem vị trí tiếp theo có an toàn không
            return (dx, dy)  # Trả về hướng an toàn đầu tiên
            
    return current_direction  # Không còn lựa chọn nào khác