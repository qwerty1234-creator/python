import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodgeball Battle")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 4 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 7
player_hp = 3
score = 0
player_ball = None  # Ball held by player

# Computer settings
computer_width = 50
computer_height = 50
computer_x = 3 * WIDTH // 4 - computer_width // 2
computer_y = HEIGHT - computer_height - 10
computer_speed = 5
computer_hp = 3  # Computer's health
computer_ball = None  # Ball held by computer

# Other settings
balls = []  # Balls in the background
ball_radius = 20
last_ball_time = time.time()  # Time tracker for ball creation
ball_speed = 5  # Ball falling speed

# Font settings
font = pygame.font.SysFont(None, 30)

# Draw text
def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Draw player
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

# Draw computer
def draw_computer(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, computer_width, computer_height))

# Draw balls
def draw_balls():
    # Draw background balls
    for ball in balls:
        pygame.draw.circle(screen, RED, (ball[0], ball[1]), ball_radius)
    # Draw player's ball
    if player_ball is not None:
        pygame.draw.circle(screen, RED, (player_ball[0], player_ball[1]), ball_radius)
    # Draw computer's ball
    if computer_ball is not None:
        pygame.draw.circle(screen, RED, (computer_ball[0], computer_ball[1]), ball_radius)

# Collision detection
def check_collision(ball, x, y, width, height):
    return x < ball[0] < x + width and y < ball[1] < y + height

# Main game function
def game_loop():
    global player_x, player_y, player_hp, score, player_ball
    global computer_x, computer_y, computer_hp, computer_ball, computer_speed, balls
    global last_ball_time

    running = True
    while running:
        clock.tick(60)
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Every 10 seconds generate a ball
        if time.time() - last_ball_time >= 10:
            last_ball_time = time.time()  # Update last ball creation time
            # Randomly generate a background ball
            ball_x = random.randint(0, WIDTH)
            balls.append([ball_x, 0])  # Ball position starts from the top

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Catch ball (Press Shift)
        if keys[pygame.K_LSHIFT] and player_ball is None:
            for ball in balls[:]:
                if check_collision(ball, player_x, player_y, player_width, player_height):
                    balls.remove(ball)
                    player_ball = ball
                    break

        # Throw ball (Press Space)
        if keys[pygame.K_SPACE] and player_ball is not None:
            # Player throws ball toward computer
            ball = player_ball
            ball[0] = player_x + player_width // 2
            ball[1] = player_y
            balls.append(ball)
            player_ball = None
            score += 1  # Successful throw

        # Computer controls
        if computer_ball is None:
            if random.random() < 0.02:  # Control throw frequency
                ball_x = random.randint(0, WIDTH)
                balls.append([ball_x, 0])  # Computer throws a ball

        # Computer catches ball
        for ball in balls[:]:
            if check_collision(ball, computer_x, computer_y, computer_width, computer_height):
                balls.remove(ball)
                computer_ball = ball
                break

        # Computer moves to catch ball
        if computer_ball is None:
            if balls:
                nearest_ball = min(balls, key=lambda b: abs(b[0] - computer_x))
                if nearest_ball[0] < computer_x:
                    computer_x -= computer_speed
                elif nearest_ball[0] > computer_x:
                    computer_x += computer_speed

        # Computer throws ball
        if computer_ball is not None:
            computer_ball[0] = computer_x + computer_width // 2
            computer_ball[1] = computer_y
            balls.append(computer_ball)
            computer_ball = None
            score += 1  # Successful throw

        # Move balls
        for ball in balls[:]:
            ball[1] += ball_speed  # Move down each frame
            if ball[1] > HEIGHT:  # Ball falls out of the screen
                balls.remove(ball)

        # Check if player or computer is hit
        for ball in balls[:]:
            if check_collision(ball, player_x, player_y, player_width, player_height):
                player_hp -= 1
                balls.remove(ball)
                if player_hp <= 0:
                    draw_text("You Lost!", WIDTH // 2 - 50, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    running = False  # Player lost, end game

            if check_collision(ball, computer_x, computer_y, computer_width, computer_height):
                computer_hp -= 1
                balls.remove(ball)
                if computer_hp <= 0:
                    draw_text("You Won!", WIDTH // 2 - 50, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    running = False  # Computer lost, end game

        # Draw objects
        draw_player(player_x, player_y)
        draw_computer(computer_x, computer_y)
        draw_balls()

        # Display score and health
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Player Health: {player_hp}", 10, 40)
        draw_text(f"Computer Health: {computer_hp}", WIDTH - 150, 40)

        # Update the screen
        pygame.display.flip()

# Start the game
game_loop()
