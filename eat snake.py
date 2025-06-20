import pygame
import random
import sys

# 初始化
pygame.init()

# 畫面大小與顏色
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 設定畫面
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 貪吃蛇 Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# 產生食物
def random_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return [x, y]

# 初始化蛇
snake = [[100, 100]]
direction = [CELL_SIZE, 0]  # 向右移動
food = random_food()
score = 0

# 遊戲主迴圈
running = True
while running:
    clock.tick(5)  # 每秒10幀（蛇的速度）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制方向
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != [0, CELL_SIZE]:
        direction = [0, -CELL_SIZE]
    elif keys[pygame.K_DOWN] and direction != [0, -CELL_SIZE]:
        direction = [0, CELL_SIZE]
    elif keys[pygame.K_LEFT] and direction != [CELL_SIZE, 0]:
        direction = [-CELL_SIZE, 0]
    elif keys[pygame.K_RIGHT] and direction != [-CELL_SIZE, 0]:
        direction = [CELL_SIZE, 0]

    # 移動蛇
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
    snake.insert(0, new_head)

    # 吃到食物
    if snake[0] == food:
        food = random_food()
        score += 1
    else:
        snake.pop()

    # 撞到邊界或自己 → 遊戲結束
    if (
        snake[0][0] < 0 or snake[0][0] >= WIDTH or
        snake[0][1] < 0 or snake[0][1] >= HEIGHT or
        snake[0] in snake[1:]
    ):
        text = font.render("Game Over!", True, RED)
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # 畫面更新
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    # 顯示分數
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.quit()
sys.exit()
