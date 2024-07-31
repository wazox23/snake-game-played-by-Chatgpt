Hi, you're a professional AI developer, I need you to help me program a snake game that will be controlled by the OpenAI api key. Snake game using the Pygame library. The game also integrates OpenAI's GPT-3.5-turbo model to assist in determining the snake's direction. It is really important to my career.

Imports and Initialization:

The script imports necessary libraries: pygame, random, sys, openai, dotenv, and os.
It loads environment variables using load_dotenv().
Constants:

GRID_SIZE, CELL_SIZE, SCREEN_SIZE, and FPS are defined to set up the game's grid, cell size, screen size, and frame rate.
Color constants are defined for WHITE, GREEN, RED, and BLACK.
Directional constants UP, DOWN, LEFT, and RIGHT are defined as tuples.
OpenAI API Setup:

The script retrieves the OpenAI API key from environment variables and sets up the API client.
Pygame Initialization:

Pygame is initialized, the game screen is set up with a caption "Snake Game", and a clock object is created for controlling the frame rate.
Game Functions:

initialize_game(): Initializes the snake's position, direction, and places the first apple.
place_apple(snake): Randomly places an apple on the grid ensuring it doesn't overlap with the snake.
update_game_state(snake, direction, apple): Updates the snake's position, checks for collisions, and handles apple consumption.
draw_game_state(snake, apple): Draws the current state of the game on the screen, including the snake and the apple.
get_llm_direction(snake, apple, current_direction): Uses OpenAI's GPT-3.5-turbo model to determine the next direction for the snake based on the current game state.
Detailed Explanation of get_llm_direction Function:

Within get_llm_direction, the current game state is sent to OpenAI's GPT-3.5-turbo model to decide the next direction for the snake.
The function starts by extracting the snake's head position and forming a game state dictionary containing the snake's body, apple position, current direction, and grid size.
A try-except block is used to handle potential errors during the API call.
The openai.ChatCompletion.create function is called with the following parameters:
model: Specifies the GPT-3.5-turbo model.
messages: A list of message objects, where:
The first message sets the system context, informing the model that it is an AI playing a Snake game and should navigate the snake to the apple while avoiding collisions.
The second message provides the current game state details, including the snake head, body, apple position, current direction, and grid size. It asks the model to suggest the next direction from 'UP', 'DOWN', 'LEFT', 'RIGHT'.
The response from the model is processed to extract the suggested direction.
The direction is mapped to the corresponding tuple using the direction_map function.
Main Game Loop:

The main() function initializes the game state and enters an infinite loop to handle game events, update the game state, and draw the game state.
The loop checks for the QUIT event to exit the game.
It calls get_llm_direction() to get the new direction for the snake, updates the game state, and breaks the loop if the snake collides.
The game state is drawn, and the frame rate is controlled using clock.tick(FPS).
Running the Game:

The script runs the main() function when executed directly.
This script integrates a classic Snake game with a modern AI approach using OpenAI's API to make decisions for the snake's movements. 
