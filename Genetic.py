import pygame
import random
import numpy as np

# Khởi tạo Pygame
pygame.init()

# Màn hình và các thông số
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BLOCK_SIZE = 20
FPS = 100  # FPS ban đầu

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Khởi tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game with Genetic Algorithm')

# Lớp Rắn
class Snake:
    def __init__(self, genome=None):
        self.body = [(100, 100)]  # Vị trí ban đầu của rắn
        self.direction = (BLOCK_SIZE, 0)  # Di chuyển sang phải
        self.alive = True
        self.score = 0
        
        # Nếu không có genome, tạo ra genome ngẫu nhiên
        if genome is None:
            self.genome = np.random.uniform(-1, 1, size=4)  # 4 gene cho các đầu vào
        else:
            self.genome = genome
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body = [new_head] + self.body[:-1]
        
    def grow(self):
        # Thêm một phần vào đuôi
        tail = self.body[-1]
        self.body.append(tail)
        self.score += 1

    def collision(self):
        head = self.body[0]
        # Kiểm tra nếu rắn đâm vào tường hoặc tự đụng phải mình
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

    def get_state(self, food_position):
        head = self.body[0]
        # Tính toán khoảng cách đến các đối tượng cần thiết
        dist_x = food_position[0] - head[0]
        dist_y = food_position[1] - head[1]

        # Kiểm tra tường và phần cơ thể rắn
        wall_left = head[0] < BLOCK_SIZE
        wall_right = head[0] >= SCREEN_WIDTH - BLOCK_SIZE
        wall_up = head[1] < BLOCK_SIZE
        wall_down = head[1] >= SCREEN_HEIGHT - BLOCK_SIZE
        
        # Trạng thái sẽ bao gồm thông tin về vị trí thức ăn, tường và cơ thể rắn
        return np.array([dist_x, dist_y, self.direction[0], self.direction[1], wall_left, wall_right, wall_up, wall_down])

    def act(self, state):
        # Dựa trên genome để quyết định hành động
        # Tính toán hành động dựa trên trạng thái
        '''
        state[0]: Khoảng cách giữa rắn và thức ăn trên trục X.
        state[1]: Khoảng cách giữa rắn và thức ăn trên trục Y.
        state[4]: Trạng thái có va chạm với tường trái (True nếu va chạm).
        state[5]: Trạng thái có va chạm với tường phải (True nếu va chạm).
        state[6]: Trạng thái có va chạm với tường trên (True nếu va chạm).
        state[7]: Trạng thái có va chạm với tường dưới (True nếu va chạm).
        '''
        if state[4] and self.direction[0] < 0:  # Tránh tường trái
            self.direction = (BLOCK_SIZE, 0)  # Di chuyển sang phải
        elif state[5] and self.direction[0] > 0:  # Tránh tường phải
            self.direction = (-BLOCK_SIZE, 0)  # Di chuyển sang trái
        elif state[6] and self.direction[1] < 0:  # Tránh tường trên
            self.direction = (0, BLOCK_SIZE)  # Di chuyển xuống
        elif state[7] and self.direction[1] > 0:  # Tránh tường dưới
            self.direction = (0, -BLOCK_SIZE)  # Di chuyển lên
        elif state[0] > 0 and self.direction[0] != -BLOCK_SIZE:
            self.direction = (BLOCK_SIZE, 0)  # Di chuyển sang phải
        elif state[0] < 0 and self.direction[0] != BLOCK_SIZE:
            self.direction = (-BLOCK_SIZE, 0)  # Di chuyển sang trái
        elif state[1] > 0 and self.direction[0] != -BLOCK_SIZE:
            self.direction = (0, BLOCK_SIZE)  # Di chuyển xuống
        elif state[1] < 0 and self.direction[0] != BLOCK_SIZE:
            self.direction = (0, -BLOCK_SIZE)  # Di chuyển lên

# Sinh ra quần thể
def create_population(size):
    population = []
    for _ in range(size):
        population.append(Snake())
    return population

# Chọn lọc tự nhiên (Tournament Selection)
def select_parents(population, num_parents=2, tournament_size=5):
    parents = []
    for _ in range(num_parents):
        tournament = random.sample(population, tournament_size)  # Chọn ngẫu nhiên các con tham gia tournament
        parent = max(tournament, key=lambda snake: snake.score)  # Chọn cá thể có điểm cao nhất trong tournament
        parents.append(parent)
    return parents

# Lai ghép các genome của cha mẹ (Uniform Crossover)
def crossover(parent1, parent2):
    child_genome = []
    for i in range(len(parent1.genome)):
        if random.random() > 0.5:
            child_genome.append(parent1.genome[i])
        else:
            child_genome.append(parent2.genome[i])
    
    return np.array(child_genome)

# Đột biến genome
def mutate(genome, mutation_rate=0.1):
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome[i] += np.random.uniform(-0.5, 0.5)
    return genome

# Hàm chính để chạy trò chơi
def run_game(output_file='output.txt', overwrite=True):
    global FPS
    clock = pygame.time.Clock()
    population_size = 10
    generations = 10
    population = create_population(population_size)

    # Mở file để ghi
    mode = 'w' if overwrite else 'a'
    with open(output_file, mode) as f:
        for generation in range(generations):
            for snake in population:
                food_position = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                                 random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

                while snake.alive:
                    screen.fill(BLACK)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return

                    state = snake.get_state(food_position)
                    snake.act(state)
                    snake.move()
                    if snake.collision():
                        snake.alive = False
                        f.write(f"Generation {generation + 1}, Best score: {snake.score}\n")

                    if snake.body[0] == food_position:
                        snake.grow()
                        while True:
                            new_food_position = (
                                random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                                random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                            )
                            if new_food_position not in snake.body:
                                food_position = new_food_position
                                break

                    # Vẽ rắn và thức ăn
                    for segment in snake.body:
                        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

                    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))
                    pygame.display.update()
                    clock.tick(FPS)

            # Sau mỗi thế hệ, chọn lọc cha mẹ và tạo thế hệ mới
            parents = select_parents(population)
            parent1, parent2 = parents[0], parents[1]
            child_genome = crossover(parent1, parent2)
            child_genome = mutate(child_genome)

            # Thay thế cá thể yếu nhất bằng cá thể mới
            population = sorted(population, key=lambda snake: snake.score, reverse=True)
            population[-1] = Snake(child_genome)

            f.write(f"Generation {generation + 1}, Best score: {population[0].score}\n")

if __name__ == "__main__":
    run_game()
