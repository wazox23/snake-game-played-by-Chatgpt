import pygame
import random
import sys
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Constants
GRID_SIZE = 20
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
FPS = 10

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

def initialize_game():
    snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    direction = random.choice([UP, DOWN, LEFT, RIGHT])
    apple = place_apple(snake)
    return snake, direction, apple

def place_apple(snake):
    while True:
        apple = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if apple not in snake:
            return apple

def update_game_state(snake, direction, apple):
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    if new_head in snake or new_head[0] < 0 or new_head[0] >= GRID_SIZE or new_head[1] < 0 or new_head[1] >= GRID_SIZE:
        return snake, apple, True
    snake.insert(0, new_head)
    if new_head == apple:
        apple = place_apple(snake)
    else:
        snake.pop()
    return snake, apple, False

def draw_game_state(snake, apple):
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def get_llm_direction(snake, apple, current_direction):
    game_state = {
        'snake': snake,
        'apple': apple,
        'current_direction': current_direction,
        'grid_size': GRID_SIZE
    }
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI playing a Snake game. Navigate the snake to the apple while avoiding collisions."},
                {"role": "user", "content": f"Current game state: {game_state}. Suggest the next direction from 'UP', 'DOWN', 'LEFT', 'RIGHT'."}
            ]
        )
        direction_str = response['choices'][0]['message']['content'].strip().upper()
        direction_map = {
            'UP': UP,
            'DOWN': DOWN,
            'LEFT': LEFT,
            'RIGHT': RIGHT
        }
        return direction_map.get(direction_str, current_direction)
    except Exception as e:
        print(f"Error: {e}")
        return current_direction

def main():
    snake, direction, apple = initialize_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        direction = get_llm_direction(snake, apple, direction)
        snake, apple, collision = update_game_state(snake, direction, apple)
        
        if collision:
            break
        
        draw_game_state(snake, apple)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
