import heapq

def manhattan_distance(pos1, pos2):
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
    return valid_moves[current_direction]

def get_neighbors(pos, snake_body, grid_width, grid_height, current_direction):
    valid_directions = get_valid_directions(current_direction)
    neighbors = []
    
    for dx, dy in valid_directions:
        new_x = (pos[0] + dx) % grid_width
        new_y = (pos[1] + dy) % grid_height
        new_pos = (new_x, new_y)
        
        if new_pos not in snake_body:
            neighbors.append((new_pos, (dx, dy)))
            
    return neighbors

def astar_next_move(snake, food, grid_width, grid_height):
    start = snake.body[0]
    goal = food.position
    current_direction = snake.direction
    
    frontier = [(0, start, [])]
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while frontier:
        _, current, path = heapq.heappop(frontier)
        
        if current == goal:
            if not path:
                return current_direction
            return path[0]
            
        for next_pos, direction in get_neighbors(current, snake.body, grid_width, grid_height, current_direction):
            new_cost = cost_so_far[current] + 1
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + manhattan_distance(next_pos, goal)
                new_path = path + [direction] if not path else [direction]
                heapq.heappush(frontier, (priority, next_pos, new_path))
                came_from[next_pos] = current
    
    # Nếu không tìm thấy đường đến thức ăn, tìm đường đi an toàn nhất
    if frontier:
        _, _, path = frontier[0]
        if path:
            return path[0]
    
    # Nếu không tìm được đường đi nào, tiếp tục theo hướng hiện tại nếu an toàn
    next_head = ((start[0] + current_direction[0]) % grid_width,
                 (start[1] + current_direction[1]) % grid_height)
    if next_head not in snake.body:
        return current_direction
        
    # Nếu không an toàn, thử tìm một hướng an toàn khác
    for dx, dy in get_valid_directions(current_direction):
        next_head = ((start[0] + dx) % grid_width,
                    (start[1] + dy) % grid_height)
        if next_head not in snake.body:
            return (dx, dy)
            
    return current_direction  # Không còn lựa chọn nào khác