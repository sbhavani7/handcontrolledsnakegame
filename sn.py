import cv2
import mediapipe as mp
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up game variables
width, height = 1000, 500
snake_size = 20
snake_speed = 15
food_size = 15
score = 0

# Set up colors
white = (255, 255, 255)
green = (60, 179, 113)
red = (255, 0, 0)

# Set up the Pygame screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gesture Snake Game")

# Set up the snake
snake = [(width // 2, height // 2)]
snake_dir = (1, 0)

# Set up the food
food = (random.randint(0, width - food_size), random.randint(0, height - food_size))

# Set up MediaPipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set up Pygame mixer
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("appleEatSound.wav")  # Replace "eat_sound.wav" with the actual file path
hit_edge_sound = pygame.mixer.Sound("hit_edge.wav")  # Replace "hit_edge_sound.wav" with the actual file path
start_sound = pygame.mixer.Sound("start.wav")

# Open the camera
cap = cv2.VideoCapture(0)

# Create a Pygame clock to control frame rate
clock = pygame.time.Clock()

game_over_font = pygame.font.Font(None, 72)
score_font = pygame.font.Font(None, 36)
start_font = pygame.font.Font(None, 48)

# Display "Press SPACE to Start" message
start_text = start_font.render("START GAME -Press SPACE to Start", True, green)
screen.blit(start_text, (width // 2 - 300, height // 2 - 50))
start_sound.play()
pygame.display.flip()

# Wait for SPACE key press to start the game
waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting_for_start = False

# Main game loop
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        x, y = int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)
        snake_dir = (x - snake[0][0], y - snake[0][1])

    # Check for collisions with food
    if (
        food[0] < snake[0][0] < food[0] + food_size
        and food[1] < snake[0][1] < food[1] + food_size
    ):
        score += 5
        food = (random.randint(0, width - food_size), random.randint(0, height - food_size))
        eat_sound.play()  # Play the eat sound

        # Add a new segment at the tail of the snake
        tail = snake[-1]
        snake.append((tail[0], tail[1]))

    # Check for collisions with the boundaries
    if (
        snake[0][0] < 0
        or snake[0][0] >= width
        or snake[0][1] < 0
        or snake[0][1] >= height
    ):
        hit_edge_sound.play()  # Play the hit edge sound
        break

    # Update snake position
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])
    snake[0] = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    # Draw the game elements
    screen.fill(white)
    pygame.draw.rect(screen, red, (*food, food_size, food_size))
    for segment in snake:
        pygame.draw.rect(screen, green, (*segment, snake_size, snake_size))

    # Display the score
    score_text = score_font.render(f"Score: {score}", True, green)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Set the frame rate
    clock.tick(snake_speed)

# Display "Game Over" and final score
game_over_text = game_over_font.render("Game Over", True, red)
screen.blit(game_over_text, (width // 2 - 150, height // 2 - 50))

final_score_text = score_font.render(f"Your Score: {score}", True, green)
screen.blit(final_score_text, (width // 2 - 120, height // 2 + 20))

# Display "Excellent!" if the score is greater than 25
if score > 100:
    excellent_text = score_font.render("Excellent!", True, green)
    screen.blit(excellent_text, (width // 2 - 90, height // 2 + 90))

pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
