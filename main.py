import pygame
from game import Game

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init() #khởi tạo mixer cho âm thanh
    game = Game() #tạo đối tượng game
    game.run() #chạy trò chơi