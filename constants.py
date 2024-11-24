import os

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - 60) // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
IMG_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
FONT_DIR = os.path.join(ASSET_DIR, "fonts") 