from enum import Enum

class GameState(Enum):
    # Định nghĩa các trạng thái của trò chơi
    MAIN_MENU = 1        # Trạng thái menu chính
    MODE_SELECT = 2      # Trạng thái chọn chế độ chơi
    MAP_SELECT = 3       # Trạng thái chọn bản đồ
    PLAYING = 4          # Trạng thái đang chơi
    PAUSED = 5           # Trạng thái tạm dừng
    GAME_OVER = 6        # Trạng thái kết thúc trò chơi
    RULES = 7            # Trạng thái hiển thị luật chơi
    HIGH_SCORES = 8      # Trạng thái hiển thị điểm cao
    CREDITS = 9          # Trạng thái hiển thị thông tin về trò chơi
    PERFORMANCE = 10     # Trạng thái hiển thị hiệu suất 