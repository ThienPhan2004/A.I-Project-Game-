import pygame
import os
import time
import math
import sys
from game_state import GameState
from game_mode import GameMode
from snake import Snake
from food import Food
from high_scores import HighScores
from constants import *
from algorithms.genetic import GeneticSnake
from algorithms.bfs import bfs_next_move
from algorithms.astar import astar_next_move
from algorithms.backtracking import backtracking_next_move

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Xenzia")

        # Load sounds
        self.menu_music = pygame.mixer.Sound(os.path.join(SOUND_DIR, "menu_music.mp3"))
        self.game_music = pygame.mixer.Sound(os.path.join(SOUND_DIR, "game_music.mp3"))
        self.eat_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "eat.wav"))
        self.death_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "death.wav"))

        # Load font
        # self.font = pygame.font.Font(os.path.join(FONT_DIR, "game_font.ttf"), 36)
        # self.small_font = pygame.font.Font(os.path.join(FONT_DIR, "game_font.ttf"), 24)
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.high_scores = HighScores()
        self.clock = pygame.time.Clock()
        self.small_food_count = 0  # Thm biến đếm đồ ăn nhỏ
        self.genetic_snake = GeneticSnake()  # Thêm đối tượng GA
        self.generation_scores = []  # Lưu điểm số của thế hệ hiện tại
        self.reset_game()
        self.glow_timer = 0  # Thêm biến đếm thời gian cho hiệu ứng
        
        # Load background image
        try:
            self.background_img = pygame.image.load(os.path.join(IMG_DIR, "background.png"))
            self.background_img = pygame.transform.scale(self.background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except:
            print("Warning: Could not load background image")
            self.background_img = None
        
        self.algorithm_stats = {
            'BFS': {'scores': [], 'times': []},
            'A*': {'scores': [], 'times': []},
            'Genetic': {'scores': [], 'times': []},
            'Backtracking': {'scores': [], 'times': []}
        }
        self.performance_graph = None
        
        self.performance_data = {
            'BFS': {'snake': None, 'food': None, 'score': 0, 'time': 0, 'moves': [], 'path': []},
            'A*': {'snake': None, 'food': None, 'score': 0, 'time': 0, 'moves': [], 'path': []},
            'Genetic': {'snake': None, 'food': None, 'score': 0, 'time': 0, 'moves': [], 'path': []},
            'Backtracking': {'snake': None, 'food': None, 'score': 0, 'time': 0, 'moves': [], 'path': []}
        }
        self.is_comparing = False
        self.comparison_start_time = 0
        self.pause_start_time = 0  # Thêm biến lưu thời điểm bắt đầu pause
        self.total_pause_time = 0  # Thêm biến lưu tổng thời gian đã pause
        
    def reset_game(self):
        self.state = GameState.MAIN_MENU
        self.mode = GameMode.MANUAL
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.game_time = 0
        self.start_time = 0
        self.game_speed = 10
        self.menu_music.play(-1) # Phát nhạc (-1 nghĩa là lặp vô hạn)
        self.small_food_count = 0  # Reset biến đếm
        if self.mode == GameMode.GENETIC:
            self.generation_scores.append(self.score)
            if len(self.generation_scores) >= 10:  # Sau 10 lần chơi
                self.genetic_snake.evolve(self.generation_scores)
                self.generation_scores = []
        self.pause_start_time = 0
        self.total_pause_time = 0
        
    def draw_button(self, text, pos, selected=False, is_hovered=False):
        # Tính toán kích thước nút dựa trên độ dài của text
        text_surface = self.font.render(text, True, BLACK)
        text_width = text_surface.get_width()
        button_width = max(200, text_width + 40)
        button_height = 50
        border_radius = 25  # Độ bo tròn của góc

        # Hiệu ứng hover animation
        hover_scale = 1.1 if is_hovered else 1.0
        hover_width = int(button_width * hover_scale)
        hover_height = int(button_height * hover_scale)
        
        # Màu nền của nút
        if selected:
            color = GREEN
        elif is_hovered:
            color = DARK_GREEN
        else:
            color = WHITE
        
        # Tính toán vị trí mới khi hover (để nút nằm giữa)
        x = pos[0] - hover_width//2
        y = pos[1] - hover_height//2
        
        # Vẽ nút với góc bo tròn và kích thước mới
        button_rect = pygame.Rect(x, y, hover_width, hover_height)
        
        # Vẽ bóng đổ khi hover
        if is_hovered:
            shadow_rect = button_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            pygame.draw.rect(self.screen, (100, 100, 100), shadow_rect, border_radius=border_radius)
        
        # Vẽ nền nút
        pygame.draw.rect(self.screen, color, button_rect, border_radius=border_radius)
        
        # Vẽ viền nút
        pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=border_radius)
        
        # Scale text khi hover
        if is_hovered:
            text_surface = pygame.transform.scale(text_surface, 
                (int(text_width * hover_scale), int(text_surface.get_height() * hover_scale)))
        
        # Vẽ text
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
        
    def show_rules(self):
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Tiêu đề
        title = self.font.render("Game Rules", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Nội dung luật chơi
        rules = [
            "1. Use arrow keys to control the snake",
            "2. Eat food to grow longer",
            "3. Avoid hitting walls and yourself",
            "4. Score increases with each food eaten",
            "5. Speed increases every 5 points",
            "6. BFS, A*, Genetic, Backtracking modes play automatically"
        ]
        
        # Vẽ các luật và lưu vị trí y của dòng cuối cùng
        last_rule_y = 0
        for i, rule in enumerate(rules):
            text = self.small_font.render(rule, True, WHITE)
            text_y = 200 + i*50
            self.screen.blit(text, (WINDOW_WIDTH//4, text_y))
            last_rule_y = text_y
        
        # Back button - đặt cách dòng luật cuối cùng 150 pixels
        button_y = last_rule_y + 150
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        temp_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, button_y - 25, 200, 50)
        is_hovered = temp_rect.collidepoint(mouse_pos)
        back_btn = self.draw_button("Back", (WINDOW_WIDTH//2, button_y), False, is_hovered)
        
        if back_btn.collidepoint(mouse_pos) and mouse_clicked:
            self.draw_button("Back", (WINDOW_WIDTH//2, button_y), True, True)
            pygame.display.flip()
            pygame.time.wait(100)
            self.state = GameState.MAIN_MENU
        
    def show_high_scores(self):
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Tiêu đề
        title = self.font.render("High Scores", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Vẽ header cho bảng
        headers = ["Score", "Mode", "Date"]
        col_widths = [150, 200, 150]  # Độ r���ng cho mỗi cột
        start_x = WINDOW_WIDTH//2 - sum(col_widths)//2
        y = 180
        
        # Vẽ đường kẻ ngang trên cùng
        pygame.draw.line(self.screen, WHITE, 
                        (start_x, y), 
                        (start_x + sum(col_widths), y), 2)
        
        # Vẽ headers
        y += 10
        current_x = start_x
        for i, header in enumerate(headers):
            text = self.font.render(header, True, GREEN)
            text_rect = text.get_rect(center=(current_x + col_widths[i]//2, y))
            self.screen.blit(text, text_rect)
            current_x += col_widths[i]
        
        # Vẽ đường kẻ ngang dưới headers
        y += 30
        pygame.draw.line(self.screen, WHITE, 
                        (start_x, y), 
                        (start_x + sum(col_widths), y), 2)
        
        # Hiển thị dữ liệu
        if not self.high_scores.scores:
            text = self.font.render("No scores yet!", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y + 50))
            self.screen.blit(text, text_rect)
        else:
            for i, score_data in enumerate(self.high_scores.scores):
                y += 40
                current_x = start_x
                
                # Score
                text = self.font.render(str(score_data['score']), True, WHITE)
                text_rect = text.get_rect(center=(current_x + col_widths[0]//2, y))
                self.screen.blit(text, text_rect)
                
                # Mode
                text = self.font.render(score_data['mode'], True, WHITE)
                text_rect = text.get_rect(center=(current_x + col_widths[0] + col_widths[1]//2, y))
                self.screen.blit(text, text_rect)
                
                # Date
                text = self.font.render(score_data['date'], True, WHITE)
                text_rect = text.get_rect(center=(current_x + col_widths[0] + col_widths[1] + col_widths[2]//2, y))
                self.screen.blit(text, text_rect)
        
        # Back button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        temp_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 600 - 25, 200, 50)
        is_hovered = temp_rect.collidepoint(mouse_pos)
        back_btn = self.draw_button("Back", (WINDOW_WIDTH//2, 600), False, is_hovered)
        
        if back_btn.collidepoint(mouse_pos) and mouse_clicked:
            self.draw_button("Back", (WINDOW_WIDTH//2, 600), True, True)
            pygame.display.flip()
            pygame.time.wait(100)
            self.state = GameState.MAIN_MENU
        
    def pause_menu(self):
        if self.pause_start_time == 0:  # Nếu mới bắt đầu pause
            self.pause_start_time = time.time()
            
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Tiêu đề
        title = self.font.render("PAUSED", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        # Buttons
        resume_btn = self.draw_button("Resume", (WINDOW_WIDTH//2, 300))
        main_menu_btn = self.draw_button("Main Menu", (WINDOW_WIDTH//2, 400))
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if resume_btn.collidepoint(mouse_pos) and mouse_clicked:
            # Tính tổng thời gian đã pause
            self.total_pause_time += time.time() - self.pause_start_time
            self.pause_start_time = 0
            self.state = GameState.PLAYING
        elif main_menu_btn.collidepoint(mouse_pos) and mouse_clicked:
            self.reset_game()
            
    def game_over_screen(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        title = self.font.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 300))
        self.screen.blit(score_text, score_rect)
        
        # Buttons
        retry_btn = self.draw_button("Try Again", (WINDOW_WIDTH//2, 400))
        main_menu_btn = self.draw_button("Main Menu", (WINDOW_WIDTH//2, 500))
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if retry_btn.collidepoint(mouse_pos) and mouse_clicked:
            self.snake.reset()
            self.food = Food(self.snake)
            self.score = 0
            self.game_speed = 10
            self.start_time = time.time()
            self.state = GameState.PLAYING
            self.game_music.play(-1) # Phát nhạc (-1 nghĩa là lặp vô hạn)
        elif main_menu_btn.collidepoint(mouse_pos) and mouse_clicked:
            self.reset_game()
            
    def main_menu(self):
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Điều chỉnh vị trí tiêu đề
        self.glow_timer += 0.09
        glow_value = (math.sin(self.glow_timer) + 1) / 2
        
        title_font = pygame.font.Font('freesansbold.ttf', 80)
        
        # Vẽ hiệu ứng hào quang (giữ nguyên code hiệu ứng)
        for i in range(12, 0, -1):
            alpha = int(45 * glow_value)
            glow_size = i * 3
            glow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            glow_color = (0, 255, 0, alpha)
            glow_text = title_font.render('SNAKE ZENXIA', True, glow_color)
            glow_rect = glow_text.get_rect(center=(WINDOW_WIDTH//2 + glow_size//2, 200))  # Điều chỉnh y từ 150 lên 200
            glow_surface.blit(glow_text, glow_rect)
            self.screen.blit(glow_surface, (0, 0))
        
        # Vẽ tiêu đề chính
        main_color = (
            int(50 + 205 * glow_value),
            255,
            int(50 + 205 * glow_value)
        )
        title_text = title_font.render('SNAKE ZENXIA', True, main_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 200))  # Điều chỉnh y từ 150 lên 200
        self.screen.blit(title_text, title_rect)
        
        # Căn chỉnh lại các nút với khoảng cách đều
        button_start_y = 350
        button_spacing = 70
        
        buttons = []
        button_texts = ["New Game", "Rules", "High Scores", "Performance", "Credits", "Exit"]
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for i, text in enumerate(button_texts):
            button_y = button_start_y + (i * button_spacing)
            # Tạo rect tạm thời để kiểm tra hover
            temp_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, button_y - 25, 200, 50)
            is_hovered = temp_rect.collidepoint(mouse_pos)
            buttons.append(self.draw_button(text, (WINDOW_WIDTH//2, button_y), False, is_hovered))
        
        # Handle clicks
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                if mouse_clicked:
                    # Thêm hiệu ứng khi click
                    self.draw_button(button_texts[i], (WINDOW_WIDTH//2, button_start_y + i * button_spacing), True, True)
                    pygame.display.flip()
                    pygame.time.wait(100)  # Tạm dừng để hiển thị hiệu ứng
                    
                    if i == 0:  # New Game
                        self.state = GameState.MODE_SELECT
                    elif i == 1:  # Rules
                        self.state = GameState.RULES
                    elif i == 2:  # High Scores
                        self.state = GameState.HIGH_SCORES
                    elif i == 3:  # Performance
                        self.state = GameState.PERFORMANCE
                    elif i == 4:  # Credits
                        self.state = GameState.CREDITS
                    elif i == 5:  # Exit
                        pygame.quit()
                        sys.exit()
                        
    def mode_select(self):
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw title with shadow effect
        title_shadow = self.font.render("Select Mode", True, DARK_GREEN)
        title = self.font.render("Select Mode", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw mode buttons - Điều chỉnh khoảng cách giữa các nút mode
        modes = ["Manual", "BFS", "A*", "Genetic", "Backtracking"]
        buttons = []
        for i, mode_name in enumerate(modes):
            pos = (WINDOW_WIDTH//2, 150 + i*60)  # Giảm khoảng cách giữa các nút từ 70 xuống 60
            selected = (self.mode == GameMode(i+1))
            temp_rect = pygame.Rect(pos[0] - 100, pos[1] - 25, 200, 50)
            is_hovered = temp_rect.collidepoint(mouse_pos)
            button_rect = self.draw_button(mode_name, pos, selected, is_hovered)
            buttons.append((button_rect, i+1))
        
        # Draw play and back buttons - Đặt thấp hơn
        play_pos = (WINDOW_WIDTH//3, 520)     # Tăng y-coordinate lên 520
        back_pos = (2 * WINDOW_WIDTH//3, 520) # Tăng y-coordinate lên 520
        
        temp_rect_play = pygame.Rect(play_pos[0] - 100, play_pos[1] - 25, 200, 50)
        temp_rect_back = pygame.Rect(back_pos[0] - 100, back_pos[1] - 25, 200, 50)
        
        is_play_hovered = temp_rect_play.collidepoint(mouse_pos)
        is_back_hovered = temp_rect_back.collidepoint(mouse_pos)
        
        play_button = self.draw_button("Play", play_pos, False, is_play_hovered)
        back_button = self.draw_button("Back to Menu", back_pos, False, is_back_hovered)
        
        # Handle clicks
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked:
            for button, mode_num in buttons:
                if button.collidepoint(mouse_pos):
                    self.mode = GameMode(mode_num)
                    pygame.time.wait(200)
                    
            if play_button.collidepoint(mouse_pos):
                if self.mode == GameMode.MANUAL:
                    self.state = GameState.MAP_SELECT
                else:
                    self.state = GameState.PLAYING
                self.snake.reset()
                self.food = Food(self.snake)
                self.score = 0
                self.game_speed = 10
                self.start_time = time.time()
                self.game_music.play(-1)
            
            elif back_button.collidepoint(mouse_pos):
                self.state = GameState.MAIN_MENU
            
    def game_screen(self):
        self.screen.fill(BLACK)
        
        # Draw toolbar
        pygame.draw.rect(self.screen, WHITE, (0, 0, WINDOW_WIDTH, 60))
        
        # Draw score and time
        score_text = self.small_font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 20))
        
        # Hiển thị thời gian đã chơi (trừ đi thời gian pause)
        if self.state == GameState.PAUSED:
            current_time = self.pause_start_time - self.start_time - self.total_pause_time
        else:
            current_time = time.time() - self.start_time - self.total_pause_time
            
        time_text = self.small_font.render(f"Time: {int(current_time)}s", True, BLACK)
        self.screen.blit(time_text, (200, 20))
        
        mode_text = self.small_font.render(f"Mode: {self.mode.name}", True, BLACK)
        self.screen.blit(mode_text, (400, 20))

        # Thêm nút Pause/Resume
        pause_text = self.small_font.render("Pause" if self.state == GameState.PLAYING else "Resume", True, BLACK)
        pause_rect = pause_text.get_rect()
        pause_rect.topright = (WINDOW_WIDTH - 150, 20)  # Đặt bên trái nút Back
        self.screen.blit(pause_text, pause_rect)
        
        # Nút Back to Menu
        back_text = self.small_font.render("Back to Menu", True, BLACK)
        back_rect = back_text.get_rect()
        back_rect.topright = (WINDOW_WIDTH - 20, 20)
        self.screen.blit(back_text, back_rect)
        
        # Draw snake with gradient and effects
        for i, segment in enumerate(self.snake.body):
            # Tính toán màu gradient từ đầu đến đuôi rắn
            gradient_factor = i / len(self.snake.body) if len(self.snake.body) > 1 else 0
            
            if i == 0:  # Đầu rắn
                # Vẽ đầu rắn với màu đặc biệt và to hơn một chút
                head_color = (0, 200, 255)  # Màu xanh dương nhạt
                pygame.draw.rect(self.screen, head_color,
                               (segment[0]*GRID_SIZE - 1, 
                                segment[1]*GRID_SIZE + 60 - 1,
                                GRID_SIZE, GRID_SIZE))
                
                # Vẽ mắt rắn
                eye_color = (255, 255, 255)  # Màu trắng cho mắt
                eye_size = GRID_SIZE // 5
                
                # Xác định vị trí mắt dựa trên hướng di chuyển
                if self.snake.direction == (1, 0):  # Đang đi sang phải
                    left_eye = (segment[0]*GRID_SIZE + GRID_SIZE*3//4, segment[1]*GRID_SIZE + 60 + GRID_SIZE//3)
                    right_eye = (segment[0]*GRID_SIZE + GRID_SIZE*3//4, segment[1]*GRID_SIZE + 60 + GRID_SIZE*2//3)
                elif self.snake.direction == (-1, 0):  # Đang đi sang trái
                    left_eye = (segment[0]*GRID_SIZE + GRID_SIZE//4, segment[1]*GRID_SIZE + 60 + GRID_SIZE//3)
                    right_eye = (segment[0]*GRID_SIZE + GRID_SIZE//4, segment[1]*GRID_SIZE + 60 + GRID_SIZE*2//3)
                elif self.snake.direction == (0, -1):  # Đang đi lên
                    left_eye = (segment[0]*GRID_SIZE + GRID_SIZE//3, segment[1]*GRID_SIZE + 60 + GRID_SIZE//4)
                    right_eye = (segment[0]*GRID_SIZE + GRID_SIZE*2//3, segment[1]*GRID_SIZE + 60 + GRID_SIZE//4)
                else:  # Đang đi xuống
                    left_eye = (segment[0]*GRID_SIZE + GRID_SIZE//3, segment[1]*GRID_SIZE + 60 + GRID_SIZE*3//4)
                    right_eye = (segment[0]*GRID_SIZE + GRID_SIZE*2//3, segment[1]*GRID_SIZE + 60 + GRID_SIZE*3//4)
                
                pygame.draw.circle(self.screen, eye_color, left_eye, eye_size)
                pygame.draw.circle(self.screen, eye_color, right_eye, eye_size)
                
                # Vẽ đồng tử
                pupil_color = (0, 0, 0)  # Màu đen cho đồng tử
                pygame.draw.circle(self.screen, pupil_color, left_eye, eye_size//2)
                pygame.draw.circle(self.screen, pupil_color, right_eye, eye_size//2)
                
            else:  # Thân rắn
                # Tạo màu gradient từ xanh lá đến xanh dương
                r = int(0 + gradient_factor * 0)    # Giữ R = 0
                g = int(255 - gradient_factor * 155)  # G giảm dần
                b = int(0 + gradient_factor * 255)    # B tăng dần
                segment_color = (r, g, b)
                
                # Vẽ phần thân với hiệu ứng bo tròn
                pygame.draw.rect(self.screen, segment_color,
                               (segment[0]*GRID_SIZE + 1, 
                                segment[1]*GRID_SIZE + 60 + 1,
                                GRID_SIZE-2, GRID_SIZE-2),
                               border_radius=3)
                
                # Thêm hiệu ứng bóng đổ nhẹ
                shadow_color = (r//2, g//2, b//2)
                pygame.draw.rect(self.screen, shadow_color,
                               (segment[0]*GRID_SIZE + 2,
                                segment[1]*GRID_SIZE + 60 + 2,
                                GRID_SIZE-4, GRID_SIZE-4),
                               border_radius=2)
            
        # Draw food
        if self.food.is_big:
            # Vẽ đồ ăn lớn
            pygame.draw.rect(self.screen, RED,
                            (self.food.position[0]*GRID_SIZE,
                             self.food.position[1]*GRID_SIZE + 60,
                             GRID_SIZE*2-2, GRID_SIZE*2-2))
            
            # Vẽ time bar
            remaining_time = self.food.get_remaining_time()
            if remaining_time > 0:
                # Vẽ khung time bar
                bar_width = GRID_SIZE * 3
                bar_height = 5
                bar_x = self.food.position[0]*GRID_SIZE
                bar_y = self.food.position[1]*GRID_SIZE + 60 - 10
                
                # Vẽ nền time bar (màu xám)
                pygame.draw.rect(self.screen, (100, 100, 100),
                               (bar_x, bar_y, bar_width, bar_height))
                
                # Vẽ phần còn lại của time bar (màu xanh -> vàng -> đỏ)
                if remaining_time > 0:
                    # Màu sắc thay đổi theo thời gian còn lại
                    if remaining_time > 0.6:
                        color = GREEN
                    elif remaining_time > 0.3:
                        color = YELLOW
                    else:
                        color = RED
                        
                    pygame.draw.rect(self.screen, color,
                                   (bar_x, bar_y, 
                                    bar_width * remaining_time, bar_height))
        else:
            pygame.draw.rect(self.screen, RED,
                            (self.food.position[0]*GRID_SIZE,
                             self.food.position[1]*GRID_SIZE + 60,
                             GRID_SIZE-2, GRID_SIZE-2))
        
        # Trả về rect của cả hai nút
        return back_rect, pause_rect
                         
    def handle_input(self):
        # Lấy vị trí chuột và trạng thái click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Left click
        
        # Kiểm tra click vào nút Back to Menu
        back_button_rect = pygame.Rect(WINDOW_WIDTH - 120, 20, 100, 30)
        if back_button_rect.collidepoint(mouse_pos) and mouse_clicked:
            self.reset_game()
            return
            
        # Kiểm tra click vào nút Pause/Resume
        pause_button_rect = pygame.Rect(WINDOW_WIDTH - 250, 20, 80, 30)
        if pause_button_rect.collidepoint(mouse_pos) and mouse_clicked:
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING
            # Đợi một chút để tránh double-click
            pygame.time.wait(200)
            return
        
        # Chỉ xử lý input di chuyển khi game đang chạy
        if self.state == GameState.PLAYING:
            if self.mode == GameMode.MANUAL:
                keys = pygame.key.get_pressed()
                current_direction = self.snake.direction
                
                if current_direction == (0, -1):  # Đang đi lên
                    if keys[pygame.K_LEFT]:
                        self.snake.direction = (-1, 0)
                    elif keys[pygame.K_RIGHT]:
                        self.snake.direction = (1, 0)
                elif current_direction == (0, 1):   # Đang đi xuống
                    if keys[pygame.K_LEFT]:
                        self.snake.direction = (-1, 0)
                    elif keys[pygame.K_RIGHT]:
                        self.snake.direction = (1, 0)
                elif current_direction == (-1, 0):  # Đang đi sang trái
                    if keys[pygame.K_UP]:
                        self.snake.direction = (0, -1)
                    elif keys[pygame.K_DOWN]:
                        self.snake.direction = (0, 1)
                elif current_direction == (1, 0):   # Đang đi sang phải
                    if keys[pygame.K_UP]:
                        self.snake.direction = (0, -1)
                    elif keys[pygame.K_DOWN]:
                        self.snake.direction = (0, 1)
            elif self.mode == GameMode.BFS:
                self.snake.direction = bfs_next_move(self.snake, self.food, GRID_WIDTH, GRID_HEIGHT)
            elif self.mode == GameMode.ASTAR:
                self.snake.direction = astar_next_move(self.snake, self.food, GRID_WIDTH, GRID_HEIGHT)
            elif self.mode == GameMode.GENETIC:
                self.snake.direction = self.genetic_snake.get_next_move(
                    self.snake, self.food, GRID_WIDTH, GRID_HEIGHT)
            elif self.mode == GameMode.BACKTRACKING:
                self.snake.direction = backtracking_next_move(
                    self.snake, self.food, GRID_WIDTH, GRID_HEIGHT)   
            
    def update_stats(self):
        if self.mode != GameMode.MANUAL:
            current_time = time.time() - self.start_time
            algorithm = self.mode.name
            self.algorithm_stats[algorithm]['scores'].append(self.score)
            self.algorithm_stats[algorithm]['times'].append(current_time)
            
    # def draw_performance_graph(self):
    #     plt.clf()
    #     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        
    #     # Plot scores
    #     for algo in self.algorithm_stats:
    #         if self.algorithm_stats[algo]['scores']:
    #             ax1.plot(self.algorithm_stats[algo]['times'], 
    #                     self.algorithm_stats[algo]['scores'],
    #                     label=algo)
    #     ax1.set_title('Score over Time')
    #     ax1.set_xlabel('Time (seconds)')
    #     ax1.set_ylabel('Score')
    #     ax1.legend()
    #     ax1.grid(True)
        
    #     # Plot average time per move
    #     avg_times = []
    #     labels = []
    #     for algo in self.algorithm_stats:
    #         if self.algorithm_stats[algo]['scores']:
    #             times = self.algorithm_stats[algo]['times']
    #             moves = len(times)
    #             if moves > 1:
    #                 avg_time = times[-1] / moves
    #                 avg_times.append(avg_time)
    #                 labels.append(algo)
        
    #     if avg_times:
    #         ax2.bar(labels, avg_times)
    #         ax2.set_title('Average Time per Move')
    #         ax2.set_ylabel('Time (seconds)')
    #         ax2.grid(True)
        
    #     # Save to a temporary file and load as pygame surface
    #     plt.savefig('temp_graph.png')
    #     plt.close(fig)
    #     return pygame.image.load('temp_graph.png')
        
    # def start_performance_comparison(self):
    #     # Reset và khởi tạo dữ liệu cho mỗi thuật toán
    #     initial_position = (GRID_WIDTH//2, GRID_HEIGHT//2)
    #     food_position = (GRID_WIDTH//4, GRID_HEIGHT//4)
        
    #     for algo in self.performance_data:
    #         self.performance_data[algo]['snake'] = Snake()
    #         self.performance_data[algo]['snake'].body = [initial_position]
    #         self.performance_data[algo]['food'] = Food(self.performance_data[algo]['snake'])
    #         self.performance_data[algo]['food'].position = food_position
    #         self.performance_data[algo]['score'] = 0
    #         self.performance_data[algo]['time'] = 0
    #         self.performance_data[algo]['moves'] = []
    #         self.performance_data[algo]['path'] = []

    #     self.is_comparing = True
    #     self.comparison_start_time = time.time()

    # def update_performance_comparison(self):
    #     if not self.is_comparing:
    #         return

    #     current_time = time.time() - self.comparison_start_time
        
    #     # Cập nhật từng thuật toán
    #     for algo in self.performance_data:
    #         data = self.performance_data[algo]
    #         snake = data['snake']
    #         food = data['food']
            
    #         # Xác định hướng di chuyển tiếp theo dựa trên thuật toán
    #         if algo == 'BFS':
    #             next_move = bfs_next_move(snake, food, GRID_WIDTH, GRID_HEIGHT)
    #         elif algo == 'A*':
    #             next_move = astar_next_move(snake, food, GRID_WIDTH, GRID_HEIGHT)
    #         elif algo == 'Genetic':
    #             next_move = self.genetic_snake.get_next_move(snake, food, GRID_WIDTH, GRID_HEIGHT)
    #         else:  # Backtracking
    #             next_move = backtracking_next_move(snake, food, GRID_WIDTH, GRID_HEIGHT)
            
    #         # Cập nhật vị trí rắn
    #         snake.direction = next_move
    #         snake.move()
            
    #         # Kiểm tra ăn thức ăn
    #         if snake.body[0] == food.position:
    #             data['score'] += 1
    #             snake.grow = True
    #             food.position = food.generate_position()
            
    #         # Lưu đường đi
    #         data['path'].append(snake.body[0])
    #         data['time'] = current_time
            
    #         # Kiểm tra va chạm
    #         if snake.check_collision():
    #             self.is_comparing = False

    # def draw_performance_comparison(self):
    #     self.screen.fill(BLACK)
        
    #     # Vẽ grid cho mỗi thuật toán
    #     grid_size = min(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
    #     algorithms = list(self.performance_data.keys())
        
    #     for i, algo in enumerate(algorithms):
    #         x = (i % 2) * (grid_size + 50) + WINDOW_WIDTH//4
    #         y = (i // 2) * (grid_size + 50) + 100
            
    #         # Vẽ khung
    #         pygame.draw.rect(self.screen, WHITE, (x, y, grid_size, grid_size), 1)
            
    #         # Vẽ tiêu đề
    #         title = self.font.render(f"{algo}: {self.performance_data[algo]['score']}", True, WHITE)
    #         self.screen.blit(title, (x, y - 30))
            
    #         # Vẽ rắn
    #         snake = self.performance_data[algo]['snake']
    #         scale = grid_size / GRID_WIDTH
    #         for segment in snake.body:
    #             pygame.draw.rect(self.screen, GREEN,
    #                 (x + segment[0] * scale,
    #                  y + segment[1] * scale,
    #                  scale - 1, scale - 1))
            
    #         # Vẽ thức ăn
    #         food = self.performance_data[algo]['food']
    #         pygame.draw.rect(self.screen, RED,
    #             (x + food.position[0] * scale,
    #              y + food.position[1] * scale,
    #              scale - 1, scale - 1))
        
    #     # Vẽ nút Back
    #     back_btn = self.draw_button("Back to Menu", (WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
        
    #     return back_btn

    # def show_performance(self):
    #     try:
    #         # Xử lý events trước
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_ESCAPE:
    #                     self.is_comparing = False
    #                     self.state = GameState.MAIN_MENU
    #                     return

    #         if not self.is_comparing:
    #             self.start_performance_comparison()
            
    #         # Giảm tốc độ cập nhật
    #         self.clock.tick(10)  # Giới hạn 10 FPS cho màn hình so sánh
            
    #         self.update_performance_comparison()
    #         back_btn = self.draw_performance_comparison()
            
    #         # Xử lý nút Back
    #         mouse_pos = pygame.mouse.get_pos()
    #         mouse_clicked = pygame.mouse.get_pressed()[0]
            
    #         if back_btn.collidepoint(mouse_pos) and mouse_clicked:
    #             self.is_comparing = False
    #             self.state = GameState.MAIN_MENU
    #             pygame.time.wait(200)
                
    #         pygame.display.flip()
            
    #     except Exception as e:
    #         print(f"Error in show_performance: {e}")
    #         self.state = GameState.MAIN_MENU

    def update(self):
        if self.state != GameState.PLAYING:
            return
            
        self.snake.move()
        
        # Kiểm tra thời gian tồn tại của đồ ăn lớn
        if self.food.is_big and self.food.get_remaining_time() <= 0:
            # Tạo đồ ăn nhỏ mới khi đồ ăn lớn hết thời gian
            self.food = Food(self.snake, is_big=False)
            self.small_food_count = 0
        
        # Check collision with food
        head = self.snake.body[0]
        if self.food.is_big:
            # Kiểm tra va chạm với đồ ăn to (2x2)
            food_positions = [
                self.food.position,
                (self.food.position[0]+1, self.food.position[1]),
                (self.food.position[0], self.food.position[1]+1),
                (self.food.position[0]+1, self.food.position[1]+1)
            ]
            if head in food_positions:
                self.score += 4  # 4 điểm cho đồ ăn to               
                self.snake.grow = True
                self.small_food_count = 0  # Reset biến đếm khi ăn đồ ăn to
                # Tạo đồ ăn mới (thường)
                self.food = Food(self.snake, is_big=False)
                self.eat_sound.play()
        else:
            if head == self.food.position:
                self.score += 1 # 1 điểm cho đồ ăn nhỏ
                self.snake.grow = True
                self.small_food_count += 1  # Tăng biến đếm
                # Kiểm tra xem có nên tạo đồ ăn to không
                if self.small_food_count >= 4:
                    self.food = Food(self.snake, is_big=True)  # Tạo đồ ăn to
                else:
                    self.food = Food(self.snake, is_big=False)  # Tạo đồ ăn nhỏ
                self.eat_sound.play()
                
        # Check collision with self
        if self.snake.check_collision():
            self.death_sound.play()
            self.game_music.stop()
            self.high_scores.add_score(self.score, self.mode.name)
            self.state = GameState.GAME_OVER
      
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        
            if self.state == GameState.MAIN_MENU:
                self.main_menu()
            elif self.state == GameState.MODE_SELECT:
                self.mode_select()
            elif self.state == GameState.MAP_SELECT:  # Thêm xử lý cho MAP_SELECT
                self.map_select()
            elif self.state == GameState.PLAYING:
                self.handle_input()
                self.update()
                self.game_screen()
            elif self.state == GameState.PAUSED:
                self.game_screen()
                self.pause_menu()
            elif self.state == GameState.GAME_OVER:
                self.game_screen()
                self.game_over_screen()
            elif self.state == GameState.RULES:
                self.show_rules()
            elif self.state == GameState.HIGH_SCORES:
                self.show_high_scores()
            elif self.state == GameState.CREDITS:  # Thêm xử lý cho Credits
                self.show_credits()
            elif self.state == GameState.PERFORMANCE:  # Thêm xử lý cho màn hình Performance
                self.show_performance()
                
            pygame.display.flip()
            self.clock.tick(self.game_speed)

    def map_select(self):
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw title
        title = self.font.render("Select Map", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw map buttons
        maps = ["Empty Map", "Map with Obstacles"]
        buttons = []
        for i, map_name in enumerate(maps):
            pos = (WINDOW_WIDTH//2, 250 + i*100)
            temp_rect = pygame.Rect(pos[0] - 100, pos[1] - 25, 200, 50)
            is_hovered = temp_rect.collidepoint(mouse_pos)
            button_rect = self.draw_button(map_name, pos, False, is_hovered)
            buttons.append((button_rect, i))
        
        # Draw play button
        play_pos = (WINDOW_WIDTH//2, 480)
        temp_rect = pygame.Rect(play_pos[0] - 100, play_pos[1] - 25, 200, 50)
        is_hovered = temp_rect.collidepoint(mouse_pos)
        play_button = self.draw_button("Play", play_pos, False, is_hovered)
        
        # Handle clicks
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked:
            for button, map_type in buttons:
                if button.collidepoint(mouse_pos):
                    self.map_type = map_type
                    pygame.time.wait(200)
                    
            if play_button.collidepoint(mouse_pos):
                self.state = GameState.PLAYING
                self.snake.reset()
                self.food = Food(self.snake)
                self.score = 0
                self.game_speed = 10
                self.start_time = time.time()
                self.game_music.play(-1)

    def show_credits(self):
        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Tiêu đề
        title = self.font.render("Credits", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Thông tin credits
        credits_info = [
            "Student Name:",
            "Phan Thanh Thien - 22110234",
            "Bui Le Anh Tan - 22110234",
            "Nguyen Hoang Vy - 22110234",
            "",
            "Algorithms Implementation:",
            "- BFS Algorithm",
            "- A* Algorithm", 
            "- Genetic Algorithm",
            "- Backtracking Algorithm",
            "",
            "Special Thanks:",
            "Supervisor/Mentor: Mrs.Phan Thi Huyen Trang",
            "",
        ]
        
        # Vẽ các dòng thông tin
        last_text_y = 0
        line_spacing = 40  # khoảng cách giữa các dòng
        start_y = 150  # Điều chỉnh vị trí bắt đầu
        
        for i, line in enumerate(credits_info):
            # font cho tiêu đề
            if i == 0 or i == 5 or i == 11:  # Các dòng tiêu đề
                text = self.font.render(line, True, GREEN)  # font lớn
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, start_y + i*line_spacing))
                self.screen.blit(text, text_rect)
            else:
                # kích thước font nội dung
                text = self.small_font.render(line, True, WHITE)
                # Scale text lên 1.2 lần
                scaled_text = pygame.transform.scale(text, 
                    (int(text.get_width() * 1.2), int(text.get_height() * 1.2)))
                text_rect = scaled_text.get_rect(center=(WINDOW_WIDTH//2, start_y + i*line_spacing))
                self.screen.blit(scaled_text, text_rect)
                
            last_text_y = start_y + i*line_spacing
        
        # Back button - đặt cách dòng text cuối cùng 100 pixels
        button_y = last_text_y + 40
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        temp_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, button_y - 25, 200, 50)
        is_hovered = temp_rect.collidepoint(mouse_pos)
        back_btn = self.draw_button("Back", (WINDOW_WIDTH//2, button_y), False, is_hovered)
        
        if back_btn.collidepoint(mouse_pos) and mouse_clicked:
            self.draw_button("Back", (WINDOW_WIDTH//2, button_y), True, True)
            pygame.display.flip()
            pygame.time.wait(100)
            self.state = GameState.MAIN_MENU