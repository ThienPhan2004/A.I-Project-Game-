import os

WINDOW_WIDTH = 1024  # Chiều rộng cửa sổ
WINDOW_HEIGHT = 768  # Chiều cao cửa sổ
GRID_SIZE = 20  # Kích thước ô lưới
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE  # Số ô lưới theo chiều rộng
GRID_HEIGHT = (WINDOW_HEIGHT - 60) // GRID_SIZE  # Số ô lưới theo chiều cao (trừ thanh công cụ)

# Colors
WHITE = (255, 255, 255)  # Màu trắng
BLACK = (0, 0, 0)  # Màu đen
RED = (255, 0, 0)  # Màu đỏ
GREEN = (0, 255, 0)  # Màu xanh lá
BLUE = (0, 0, 255)  # Màu xanh dương
DARK_GREEN = (0, 100, 0)  # Màu xanh lá đậm
YELLOW = (255, 255, 0)  # Màu vàng

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")  # Thư mục chứa các tài nguyên
IMG_DIR = os.path.join(ASSET_DIR, "images")  # Thư mục chứa hình ảnh
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")  # Thư mục chứa âm thanh
FONT_DIR = os.path.join(ASSET_DIR, "fonts")  # Thư mục chứa phông chữ