import pygame
import random
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("純色方塊版：終極槍戰！")
clock = pygame.time.Clock()

# 顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 128, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 255)

# 字型
font = pygame.font.SysFont(None, 32)

# 玩家設定
player = pygame.Rect(50, HEIGHT // 2, 50, 50)
player_speed = 5
player_hp = 5
max_hp = 5
score = 0
level = 1

# 子彈
player_bullets = []
enemy_bullets = []

# 敵人
enemies = []
enemy_timer = 0
enemy_spawn_delay = 60

# Boss
boss_active = False
boss = None
boss_hp = 20

# 道具
powerups = []

def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_health():
    for i in range(player_hp):
        pygame.draw.rect(screen, RED, (10 + i * 30, 10, 20, 20))

# 主迴圈
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # --- 控制 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += player_speed
    if keys[pygame.K_SPACE]:
        if len(player_bullets) < 5:
            bullet = pygame.Rect(player.right, player.centery - 5, 10, 10)
            player_bullets.append(bullet)

    # --- 玩家子彈 ---
    for bullet in player_bullets[:]:
        bullet.x += 10
        if bullet.x > WIDTH:
            player_bullets.remove(bullet)

    # --- 敵人生成 ---
    if not boss_active:
        enemy_timer += 1
        if enemy_timer >= enemy_spawn_delay:
            enemy = pygame.Rect(WIDTH, random.randint(0, HEIGHT - 40), 40, 40)
            enemies.append({'rect': enemy, 'timer': random.randint(30, 90)})
            enemy_timer = 0

    # --- 敵人移動與攻擊 ---
    for enemy in enemies[:]:
        enemy['rect'].x -= 2
        enemy['timer'] -= 1
        if enemy['timer'] <= 0:
            bullet = pygame.Rect(enemy['rect'].left, enemy['rect'].centery, 10, 5)
            enemy_bullets.append(bullet)
            enemy['timer'] = random.randint(60, 100)
        if enemy['rect'].right < 0:
            enemies.remove(enemy)

    # --- 敵人子彈 ---
    for bullet in enemy_bullets[:]:
        bullet.x -= 8
        if bullet.x < 0:
            enemy_bullets.remove(bullet)
        elif bullet.colliderect(player):
            player_hp -= 1
            enemy_bullets.remove(bullet)

    # --- 玩家子彈碰撞 ---
    for bullet in player_bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy['rect']):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                if random.random() < 0.2:
                    powerup = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(50, HEIGHT - 50), 20, 20)
                    powerups.append(powerup)
                break

    # --- Boss ---
    if score >= level * 100 and not boss_active:
        boss_active = True
        boss_hp = 20 + level * 10
        boss = pygame.Rect(WIDTH, HEIGHT // 2 - 60, 100, 100)

    if boss_active:
        boss.x -= 1
        if random.randint(0, 30) == 0:
            bullet = pygame.Rect(boss.left, boss.centery, 10, 5)
            enemy_bullets.append(bullet)
        for bullet in player_bullets[:]:
            if bullet.colliderect(boss):
                boss_hp -= 1
                player_bullets.remove(bullet)
                if boss_hp <= 0:
                    score += 100
                    level += 1
                    boss_active = False
                    boss = None

    # --- 撿道具 ---
    for p in powerups[:]:
        if p.colliderect(player):
            if player_hp < max_hp:
                player_hp += 1
            powerups.remove(p)

    # --- 玩家死亡 ---
    if player_hp <= 0:
        draw_text("Game Over! Press ESC to exit", 300, 250, RED)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

    # --- 繪製 ---
    pygame.draw.rect(screen, BLUE, player)
    for bullet in player_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, GREEN, enemy['rect'])
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, BLACK, bullet)
    for p in powerups:
        pygame.draw.rect(screen, YELLOW, p)
    if boss_active and boss:
        pygame.draw.rect(screen, PURPLE, boss)

    draw_health()
    draw_text(f"Score: {score}", 10, 40)
    draw_text(f"Level: {level}", 10, 70)

    pygame.display.flip()
