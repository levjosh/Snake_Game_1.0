import pygame
import sys
import datetime
import random

### How the Code Works ###
'''
- The game is split up into a big grid represented with the 'GRIDSIZE' variable and the 'SCREEN_WIDTH' and 'SCREEN_HEIGHT'
- The snake class uses the 'positions' attribute to identify the location of each 'snake block'
- The snake class handles collision checking, movement tracking, and snake updating
'''

# Initialize game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 500,500
GRIDSIZE = 20
CLOCK_SPEED = 15

# Initialize the snake and initial snake settings
SNAKE_START_LEN = 2
SNAKE_START_POS = [(SCREEN_WIDTH // 2) - (SCREEN_WIDTH // 2 % GRIDSIZE), (SCREEN_HEIGHT // 2) - (SCREEN_HEIGHT // 2 % GRIDSIZE)]  # Start the snake in the middle of the grid screen
SNAKE_START_DIR = (1, 0)

# Initialize the food and food settings
food_path = "images/apple2.png"
food_image = pygame.transform.scale(pygame.image.load(food_path), (GRIDSIZE, GRIDSIZE))


class Overlay:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)
        self.score = 0
        self.clock_start_time = pygame.time.get_ticks()

    def update_score(self, score):
        self.score = score

    def update_clock(self):
        # Calculate elapsed time in milliseconds
        elapsed_time = pygame.time.get_ticks() - self.clock_start_time
        # Convert elapsed time to a timedelta object
        elapsed_timedelta = datetime.timedelta(milliseconds=elapsed_time)
        # Format the timedelta as HH:MM:SS
        self.clock_text = elapsed_timedelta.total_seconds()

    def render(self, surface):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        clock_text = self.font.render(f"Time: {self.format_time()}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        surface.blit(clock_text, (10, 40))

    def format_time(self):
        elapsed_time = pygame.time.get_ticks() - self.clock_start_time
        elapsed_timedelta = datetime.timedelta(milliseconds=elapsed_time)
        # Format the timedelta as HH:MM:SS
        formatted_time = str(elapsed_timedelta).split(".")[0]
        return formatted_time


class Snake:
    def __init__(self, SNAKE_START_LEN, SNAKE_START_POS, SNAKE_START_DIR):
        self.length = SNAKE_START_LEN
        self.positions = [SNAKE_START_POS]
        self.direction = SNAKE_START_DIR
        self.render_initial_snake()
        
    def reset(self, SNAKE_START_LEN, SNAKE_START_POS, SNAKE_START_DIR):
        self.positions = None
        self.length = SNAKE_START_LEN
        self.positions = [SNAKE_START_POS]   # Create a new copy of the list
        self.direction = SNAKE_START_DIR
        self.render_initial_snake()

    def render_initial_snake(self):
        for i in range(self.length):
            self.update()

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        # Get the current head position and direction
        cur = self.get_head_position()
        x, y = self.direction

        # Calculate the new head position based on head position and direction
        new = [((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), ((cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)]

        # Collision check. If the new head position is in the 'positions' list then we have collided.
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset(SNAKE_START_LEN, SNAKE_START_POS, SNAKE_START_DIR)
        # If not collided, the new head position is inserted into the beginning of 'positions'. Pop the last
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # Does the actual drawing of the positions in pygame
    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, (0, 255, 0), (p[0], p[1], GRIDSIZE, GRIDSIZE))


class Food:
    def __init__(self, snake_positions, width, height):
        self.width = width
        self.height = height
        self.position = self.generate_food(snake_positions)

    def is_eaten_by(self, snake):
        # Convert snake head position to grid coordinates
        head_grid_position = (
            snake.get_head_position()[0] // GRIDSIZE,
            snake.get_head_position()[1] // GRIDSIZE
        )
        # Check if the snake has eaten the food
        if head_grid_position == self.position:
            snake.length += 1
            self.position = self.generate_food(snake.positions)

    def generate_food(self, snake_positions):
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            # Check if the new position is not on the snake
            if [x * GRIDSIZE, y * GRIDSIZE] not in snake_positions:
                return (x, y)

    def render(self, surface):
        surface.blit(food_image, (self.position[0] * GRIDSIZE, self.position[1] * GRIDSIZE))
        # pygame.draw.rect(surface, (255, 0, 0), (self.position[0] * GRIDSIZE, self.position[1] * GRIDSIZE, GRIDSIZE, GRIDSIZE))


# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

# Initialize Objects
snake = Snake(SNAKE_START_LEN, SNAKE_START_POS, SNAKE_START_DIR)
overlay = Overlay()
food_list = [Food(snake.positions, SCREEN_WIDTH // GRIDSIZE, SCREEN_HEIGHT // GRIDSIZE) for _ in range(3)]

# Main Loop
close_game = False
while not close_game:
    # Event loop in game
    key_pressed = False
    for event in pygame.event.get():
        # Option for quiting game
        if event.type == pygame.QUIT:
            close_game = True
        # Gameplay controls/mechanics
        elif event.type == pygame.KEYDOWN and not key_pressed:            
            # Key bindings
            if event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.direction = (-1, 0)
                key_pressed = True
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.direction = (1, 0)
                key_pressed = True
            elif event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.direction = (0, -1)
                key_pressed = True
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.direction = (0, 1)
                key_pressed = True

    # Update the snake and overlay
    snake.update()
    overlay.update_score(snake.length - SNAKE_START_LEN)
    overlay.update_clock()

    # Check if the food has been eaten by the snake
    for food in food_list:
        food.is_eaten_by(snake)

    # Refresh the screen
    screen.fill((0, 0, 0))
    snake.render(screen)
    overlay.render(screen)
    for food in food_list:
        food.render(screen)

    # Update and tick the game
    pygame.display.update()
    clock.tick(CLOCK_SPEED)


pygame.quit()