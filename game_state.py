from enum import Enum

class GameState(Enum):
    MAIN_MENU = 1
    MODE_SELECT = 2
    MAP_SELECT = 3
    PLAYING = 4
    PAUSED = 5
    GAME_OVER = 6
    RULES = 7
    HIGH_SCORES = 8
    CREDITS = 9
    PERFORMANCE = 10 