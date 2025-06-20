import pygame
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("吃方塊得分遊戲")

# 顏色
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 玩家
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 6

# 食物
food_size = 30
food_x = random.randint(0, WIDTH - food_size)
food_y = random.randint(0, HEIGHT - food_size)

# 分數
score = 0
font = pygame.font.SysFont(None, 36)

# 主迴圈
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # 判斷有無碰到食物
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    food_rect = pygame.Rect(food_x, food_y, food_size, food_size)
    if player_rect.colliderect(food_rect):
        score += 1
        food_x = random.randint(0, WIDTH - food_size)
        food_y = random.randint(0, HEIGHT - food_size)

    # 畫面更新
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, RED, food_rect)

    # 顯示分數
    score_text = font.render(f"score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()