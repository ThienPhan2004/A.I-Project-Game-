import random
import numpy as np
from collections import deque

class GeneticSnake:
    def __init__(self, population_size=50):
        # Khởi tạo kích thước quần thể
        self.population_size = population_size
        self.num_weights = 24
        self.population = self.initialize_population()
        self.current_chromosome = random.choice(self.population)
        self.generation = 0
        self.moves_without_food = 0
        self.max_moves_without_food = 100
        self.previous_positions = deque(maxlen=20)
        
    def initialize_population(self):
         # Khởi tạo quần thể với các trọng số ngẫu nhiên
        return [np.random.uniform(-1, 1, (6, 4)) for _ in range(self.population_size)]
    
    def calculate_inputs(self, snake, food, grid_width, grid_height):
        head = snake.body[0]
        
        # Tính khoảng cách Manhattan đến thức ăn
        food_x = min((food.position[0] - head[0]) % grid_width,
                    (head[0] - food.position[0]) % grid_width)
        food_y = min((food.position[1] - head[1]) % grid_height,
                    (head[1] - food.position[1]) % grid_height)
        
        # Kiểm tra nguy hiểm ở 4 hướng
        dangers = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_x = (head[0] + dx) % grid_width
            next_y = (head[1] + dy) % grid_height
            danger = 1.0 if (next_x, next_y) in snake.body[1:] else 0.0
            dangers.append(danger)
            
        return np.array([food_x/grid_width, food_y/grid_height] + dangers)
    
    def get_next_move(self, snake, food, grid_width, grid_height):
        head = snake.body[0]
        
        # Kiểm tra nếu rắn đang đi vòng tròn
        self.previous_positions.append(head)
        if len(self.previous_positions) == 20:
            positions_set = set(self.previous_positions)
            if len(positions_set) < 5:
                self.current_chromosome = random.choice(self.population)
                self.previous_positions.clear()
        
        self.moves_without_food += 1
        
        if self.moves_without_food >= self.max_moves_without_food:
            self.current_chromosome = random.choice(self.population)
            self.moves_without_food = 0
            self.previous_positions.clear()
        
        # Tính toán hướng di chuyển tiếp theo
        inputs = self.calculate_inputs(snake, food, grid_width, grid_height)
        outputs = np.dot(inputs.reshape(1, -1), self.current_chromosome).flatten()
        
        # Chọn hướng di chuyển
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        current_direction = snake.direction
        
        # Tránh đi ngược lại
        valid_moves = []
        for i, direction in enumerate(directions):
            if direction[0] != -current_direction[0] or direction[1] != -current_direction[1]:
                valid_moves.append((i, outputs[i]))
        
        if not valid_moves:
            return current_direction
            
        # Chọn hướng tốt nhất trong các hướng hợp lệ
        best_move = max(valid_moves, key=lambda x: x[1])
        return directions[best_move[0]]
    
    def evolve(self, fitness_scores):
        self.moves_without_food = 0
        self.previous_positions.clear()
        
        # Chọn lọc
        parents = self.selection(fitness_scores)
        
        # Tạo thế hệ mới
        new_population = []
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            new_population.extend([child1, child2])
        
        self.population = new_population[:self.population_size]
        self.current_chromosome = random.choice(self.population)
        self.generation += 1
    
    def selection(self, fitness_scores):
        selected = []
        for _ in range(self.population_size):
            tournament = random.sample(list(enumerate(fitness_scores)), 3)
            winner = max(tournament, key=lambda x: x[1])[0]
            selected.append(self.population[winner])
        return selected
    
    def crossover(self, parent1, parent2):
        # Matrix crossover
        mask = np.random.rand(*parent1.shape) < 0.5
        child1 = np.where(mask, parent1, parent2)
        child2 = np.where(mask, parent2, parent1)
        return child1, child2
    
    def mutate(self, chromosome):
        # Matrix mutation
        mutation_mask = np.random.rand(*chromosome.shape) < 0.1
        mutation = np.random.uniform(-0.5, 0.5, chromosome.shape)
        chromosome[mutation_mask] += mutation[mutation_mask]
        return chromosome