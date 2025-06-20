import pygame
import random
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 1000, 500
CELL_SIZE = 20
FPS = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 雙人貪吃蛇對戰")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# 顏色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)     # Player 1
BLUE = (0, 100, 255)    # Player 2
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 食物產生
def random_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return [x, y]

# 初始設定
snake1 = [[100, 100]]
dir1 = [CELL_SIZE, 0]
snake2 = [[400, 300]]
dir2 = [-CELL_SIZE, 0]

foods = [random_food() for _ in range(5)]  # 多顆食物
score1 = 0
score2 = 0
game_over = False
winner_text = ""

# 主迴圈
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # 控制 Player 1 (WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dir1 != [0, CELL_SIZE]:
            dir1 = [0, -CELL_SIZE]
        elif keys[pygame.K_s] and dir1 != [0, -CELL_SIZE]:
            dir1 = [0, CELL_SIZE]
        elif keys[pygame.K_a] and dir1 != [CELL_SIZE, 0]:
            dir1 = [-CELL_SIZE, 0]
        elif keys[pygame.K_d] and dir1 != [-CELL_SIZE, 0]:
            dir1 = [CELL_SIZE, 0]

        # 控制 Player 2 (↑↓←→)
        if keys[pygame.K_UP] and dir2 != [0, CELL_SIZE]:
            dir2 = [0, -CELL_SIZE]
        elif keys[pygame.K_DOWN] and dir2 != [0, -CELL_SIZE]:
            dir2 = [0, CELL_SIZE]
        elif keys[pygame.K_LEFT] and dir2 != [CELL_SIZE, 0]:
            dir2 = [-CELL_SIZE, 0]
        elif keys[pygame.K_RIGHT] and dir2 != [-CELL_SIZE, 0]:
            dir2 = [CELL_SIZE, 0]

        # 移動
        new_head1 = [snake1[0][0] + dir1[0], snake1[0][1] + dir1[1]]
        new_head2 = [snake2[0][0] + dir2[0], snake2[0][1] + dir2[1]]
        snake1.insert(0, new_head1)
        snake2.insert(0, new_head2)

        # 吃食物
        for food in foods[:]:
            if new_head1 == food:
                score1 += 1
                foods.remove(food)
                foods.append(random_food())
                break
        else:
            snake1.pop()

        for food in foods[:]:
            if new_head2 == food:
                score2 += 1
                foods.remove(food)
                foods.append(random_food())
                break
        else:
            snake2.pop()

        # 判斷死亡（超出邊界）
        def is_dead(head, snake_self, snake_enemy):
            if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT):
                return True
            if head in snake_self[1:] or head in snake_enemy:
                return True
            return False

        dead1 = is_dead(new_head1, snake1, snake2)
        dead2 = is_dead(new_head2, snake2, snake1)

        # 頭碰頭 → 雙亡
        if new_head1 == new_head2:
            dead1 = True
            dead2 = True

        if dead1 and dead2:
            game_over = True
            winner_text = "no win"
        elif dead1:
            game_over = True
            winner_text = "player 2 win"
        elif dead2:
            game_over = True
            winner_text = "player 1 win"

    # 畫面更新
    screen.fill(BLACK)

    for f in foods:
        pygame.draw.rect(screen, RED, (*f, CELL_SIZE, CELL_SIZE))

    for s in snake1:
        pygame.draw.rect(screen, GREEN, (*s, CELL_SIZE, CELL_SIZE))
    for s in snake2:
        pygame.draw.rect(screen, BLUE, (*s, CELL_SIZE, CELL_SIZE))

    # 分數顯示
    score_txt1 = font.render(f"P1: {score1}", True, WHITE)
    score_txt2 = font.render(f"P2: {score2}", True, WHITE)
    screen.blit(score_txt1, (10, 10))
    screen.blit(score_txt2, (WIDTH - 100, 10))

    # 結束文字
    if game_over:
        text = font.render(winner_text, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.flip()
