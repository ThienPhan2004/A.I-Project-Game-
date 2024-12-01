def backtracking_next_move(snake, food, grid_width, grid_height):
    def is_safe(x, y, visited):
        # Kiểm tra điểm (x,y) có an toàn không
        return (
            0 <= x < grid_width and 
            0 <= y < grid_height and 
            (x, y) not in visited and 
            (x, y) not in snake.body[1:]  # Không được đi qua thân rắn
        )
    
    def find_path(curr_x, curr_y, food_x, food_y, visited):
        # Đã tìm thấy thức ăn
        # If the current position is the food's position
        if curr_x == food_x and curr_y == food_y:
            return True, []
            
        # Thử các hướng có thể đi
        directions = [(0,1), (1,0), (0,-1), (-1,0)]  # up, right, down, left
        for dx, dy in directions:
            next_x = curr_x + dx
            next_y = curr_y + dy
            
            if is_safe(next_x, next_y, visited):
                visited.add((next_x, next_y))  # Đánh dấu vị trí đã thăm
                # Mark the position as visited
                found, path = find_path(next_x, next_y, food_x, food_y, visited)
                
                if found:
                    path.insert(0, (dx, dy))  # Thêm bước đi vào đường đi
                    # Add the move to the path
                    return True, path
                    
                visited.remove((next_x, next_y))  # Bỏ đánh dấu nếu không tìm thấy đường đi
                
        return False, []

    # Lấy vị trí đầu rắn và thức ăn
    head = snake.body[0]
    visited = set(snake.body)  # Avoid crossing the snake's body
    
    # Find the path to the food
    found, path = find_path(head[0], head[1], food.position[0], food.position[1], visited)
    
    if found and path:
        return path[0]  # Trả về bước đi đầu tiên

    else:
        # Nếu không tìm thấy đường đi, tìm hướng an toàn
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in directions:
            next_x = (head[0] + dx) % grid_width
            next_y = (head[1] + dy) % grid_height
            if (next_x, next_y) not in snake.body:
                return (dx, dy)  # Trả về hướng an toàn
                
        return snake.direction  # Giữ hướng hiện tại nếu không có hướng an toàn