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
    def __init__(self):
        self.length = SNAKE_START_LEN
        self.positions = SNAKE_START_POS
        self.direction = SNAKE_START_DIR

    def reset(self):
        self.length = SNAKE_START_LEN
        self.positions = SNAKE_START_POS
        self.direction = SNAKE_START_DIR

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        # Get the current head position and direction
        cur = self.get_head_position()
        x, y = self.direction

        # Calculate the new head position based on head position and direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)

        # Collision check. If the new head position is in the 'positions' list then we have collided.
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
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

    def generate_food(self, snake_positions):
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            # Check if the new position is not on the snake
            if (x, y) not in snake_positions:
                return (x, y)

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.position[0] * GRIDSIZE, self.position[1] * GRIDSIZE, GRIDSIZE, GRIDSIZE))


# Initialize pygame
pygame.init()


# Set up game window settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
GRIDSIZE = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()
CLOCK_SPEED = 10

# Initialize the snake and initial snake settings
SNAKE_START_LEN = 8
SNAKE_START_POS = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]  # Start the snake in the middle of the screen
SNAKE_START_DIR = (1, 0)

# Initialize Objects
snake = Snake()
overlay = Overlay()
food_list = [Food(snake.positions, SCREEN_WIDTH // GRIDSIZE, SCREEN_HEIGHT // GRIDSIZE) for _ in range(3)]

# Main Loop
game_over = False
while not game_over:
    # Event loop in game
    for event in pygame.event.get():
        # Option for quiting game
        if event.type == pygame.QUIT:
            game_over = True
        # Gameplay controls/mechanics
        elif event.type == pygame.KEYDOWN:
            # This will force only 1 move per clock tick
            if not moved_this_frame:
                moved_this_frame = True
            
            # Key bindings
            if event.key == pygame.K_a and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif event.key == pygame.K_d and snake.direction != (-1, 0):
                snake.direction = (1, 0)
            elif event.key == pygame.K_w and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif event.key == pygame.K_s and snake.direction != (0, -1):
                snake.direction = (0, 1)

        # print(f"Snake Position: {snake.positions}")

    # Update the snake and overlay
    snake.update()
    overlay.update_score(snake.length - SNAKE_START_LEN)
    overlay.update_clock()

    # Check for collisions after updating the snake
    if len(snake.positions) > 2 and snake.get_head_position() in snake.positions[2:]:
        snake.reset()

    # Properly clear and render the screen
    for food in food_list:
        # Convert snake head position to grid coordinates
        head_grid_position = (
            snake.get_head_position()[0] // GRIDSIZE,
            snake.get_head_position()[1] // GRIDSIZE
        )
        # Check if the snake has eaten the food
        if head_grid_position == food.position:
            snake.length += 1
            food.position = food.generate_food(snake.positions)

    # Reset the moved_this_frame flag at the end of the frame
    moved_this_frame = False

    screen.fill((0, 0, 0))
    snake.render(screen)
    overlay.render(screen)
    for food in food_list:
        food.render(screen)

    # Update and tick the game
    pygame.display.update()
    clock.tick(CLOCK_SPEED)

pygame.quit()