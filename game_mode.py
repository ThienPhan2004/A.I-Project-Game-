from enum import Enum

class GameMode(Enum):
    # Định nghĩa các chế độ trò chơi
    MANUAL = 1  # Chế độ điều khiển thủ công
    BFS = 2     # Chế độ tìm kiếm theo chiều rộng (Breadth-First Search)
    ASTAR = 3   # Chế độ tìm kiếm A* (A-Star)
    GENETIC = 4 # Chế độ thuật toán di truyền
    BACKTRACKING = 5  # Chế độ quay lui (Backtracking) 