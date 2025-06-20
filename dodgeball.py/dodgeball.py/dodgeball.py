# 函式庫載入區
import pygame          # 遊戲開發
import sys             # 系統控制
import random as rd    # 隨機


# 初始化及參數設置
pygame.init()  # 初始化並啟動各種模組

width, height =  800, 600                          # 設定畫面長寬數值
screen = pygame.display.set_mode((width, height))  # 回傳畫面物件
pygame.display.set_caption("Game")                 # 設定畫面標題

def menu_screen():
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 40)

    while True:
        screen.fill((255, 255, 255))
        title = font.render("Dodging Ball Game", True, (0, 0, 0))
        screen.blit(title, (width // 2 - title.get_width() // 2, 150))

        # 按鈕設定
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(width // 2 - 100, 300, 200, 60)
        is_hover = button_rect.collidepoint(mouse_x, mouse_y)

        pygame.draw.rect(screen, (100, 100, 255) if is_hover else (200, 200, 200), button_rect, border_radius=15)
        btn_text = small_font.render("Start", True, (0, 0, 0))
        text_x = button_rect.x + (button_rect.width - btn_text.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - btn_text.get_height()) // 2
        screen.blit(btn_text, (text_x, text_y))

        # 檢查事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hover:
                return
            
        pygame.display.update()

def main_game_loop():
    skill_not_using = True
    
    speed_boost_duration = 300
    is_speed_boost = False
    speed_boost_timer = 0
    speed_boost_used = False

    hp_protect_duration = 180
    is_hp_protect = False
    hp_protect_timer = 0
    hp_protect_used = False

    radius_small_duration = 300
    is_radius_small = False
    radius_small_timer = 0
    radius_small_used = False


    # 設定顏色
    white = (255, 255, 255)  
    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    circle_radius = 15  # 設定圓形的半徑
    speed = 2           # 設定移動速度

    player_x = width // 2         # 設定玩家 x 座標
    player_y = (3 * height) // 4  # 設定玩家 y 座標

    ai_x = width // 2         # 設定電腦 x 座標
    ai_y = (1 * height) // 4  # 設定電腦 y 座標
    ai_dx = 0                 # 設定電腦變化方向
    ai_dy = 0                 # 設定電腦變化方向
    ai_change_time = 90       # 設定電腦變化時間
    ai_timer = 0              # 變化計時器

    red_radius = 10        # 設定準心圓形的半徑
    ball_owner = 'player'  # 設定球權

    clock = pygame.time.Clock()  # 畫面更新計時器

    bullet = None            # 初始化玩家躲避球
    bullet_speed = 5         # 玩家躲避球移動速度

    ai_bullet = None        # 初始化電腦躲避球
    ai_bullet_speed = 5     # 電腦躲避球移動速度

    # 血量設定
    player_hp = 3
    ai_hp = 3

    ai_cooldown = 120 # 兩秒發射一次
    ai_cooldown_timer = 0 # 發射計時器

    winner = None # 勝利者

    # 遊戲主要運行
    while True:
        for event in pygame.event.get():   # 取得發生事件
            if event.type == pygame.QUIT:  # 偵測有無退出
                pygame.quit()  # 關閉遊戲畫面
                sys.exit()     # 關閉程式

            # 偵測左鍵有無按下
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ball_owner == 'player' and bullet is None:
                    # 計算方向
                    dx = mouse_x - player_x
                    dy = mouse_y - player_y
                    length = (dx ** 2 + dy ** 2) ** 0.5
                    if length != 0:
                        dx /= length
                        dy /= length
                        bullet = {
                            'x': player_x,
                            'y': player_y,
                            'dx': dx,
                            'dy': dy
                        }

            if event.type == pygame.KEYDOWN:
                if skill_not_using:
                    if event.key == pygame.K_e and not is_speed_boost and not speed_boost_used:
                        is_speed_boost = True
                        speed_boost_timer = speed_boost_duration
                        speed_boost_used = True
                        skill_not_using = False
                    if event.key == pygame.K_c and not is_hp_protect and not hp_protect_used:
                        is_hp_protect = True
                        hp_protect_timer = hp_protect_duration
                        hp_protect_used = True
                        skill_not_using = False
                    if event.key == pygame.K_q and not is_radius_small and not radius_small_used:
                        circle_radius = 10
                        radius_small_timer = radius_small_duration
                        is_radius_small = True
                        radius_small_used = True
                        skill_not_using = False

        current_speed = speed * 2 if is_speed_boost else speed

        if is_speed_boost:
            speed_boost_timer -= 1
            if speed_boost_timer <= 0:
                is_speed_boost = False
                skill_not_using = True

        if is_hp_protect:
            hp_protect_timer -= 1
            if hp_protect_timer <=0:
                is_hp_protect = False
                skill_not_using = True

        if is_radius_small:
            radius_small_timer -= 1
            if radius_small_timer <= 0:
                circle_radius = 15
                is_radius_small = False
                skill_not_using = True



        # 電腦有球權自動計算方向
        if ball_owner == 'ai':
            ai_cooldown_timer += 1
            if ai_cooldown_timer >= ai_cooldown and ai_bullet is None:
                dx = player_x - ai_x
                dy = player_y - ai_y
                length = (dx ** 2 + dy ** 2) ** 0.5
                if length != 0:
                    dx /= length
                    dy /= length
                    ai_bullet = {
                        'x': ai_x,
                        'y': ai_y,
                        'dx': dx,
                        'dy': dy
                    }
                    ai_cooldown_timer = 0


        keys = pygame.key.get_pressed()  # 取得鍵盤輸入
        if keys[pygame.K_w] and player_y - circle_radius > height // 2:
            player_y -= current_speed  # 向上移動
        if keys[pygame.K_s] and player_y + circle_radius < height:
            player_y += current_speed  # 向下移動
        if keys[pygame.K_a] and player_x - circle_radius > 0:
            player_x -= current_speed  # 向左移動
        if keys[pygame.K_d] and player_x + circle_radius < width:
            player_x += current_speed  # 向右移動

        mouse_x, mouse_y = pygame.mouse.get_pos()  # 取得滑鼠座標

        # 限制準心 y 座標
        if mouse_y - red_radius < 0:
            mouse_y = red_radius
        elif mouse_y + red_radius > height // 2:
            mouse_y = height // 2 - red_radius

        # 時間到隨機變化方向
        ai_timer += 1
        if ai_timer >= ai_change_time or (ai_dx == 0 and ai_dy == 0):
            ai_dx = rd.choice([-1, 0, 1])
            ai_dy = rd.choice([-1, 0, 1])
            ai_timer = 0

        # 更新電腦變化後座標
        ai_x += ai_dx * speed
        ai_y += ai_dy * speed

        # 檢查電腦 x 座標有無超範圍
        if ai_x - circle_radius < 0:
            ai_x = circle_radius
            ai_dx *= -1
        elif ai_x + circle_radius > width:
            ai_x = width - circle_radius
            ai_dx *= -1

        # 檢查電腦 y 座標有無超範圍
        if ai_y - circle_radius < 0:
            ai_y = circle_radius
            ai_dy *= -1
        elif ai_y + circle_radius > height // 2:
            ai_y = height // 2 - circle_radius
            ai_dy *= -1

        # 更新玩家躲避球位置
        if bullet:
            bullet['x'] += bullet['dx'] * bullet_speed
            bullet['y'] += bullet['dy'] * bullet_speed

            # 球飛出邊界就轉移球權給電腦
            if (
                bullet['x'] < 0 or bullet['x'] > width or
                bullet['y'] < 0 or bullet['y'] > height
            ):
                bullet = None
                ball_owner = 'ai' 

        # 更新電腦躲避球位置
        if ai_bullet:
            ai_bullet['x'] += ai_bullet['dx'] * ai_bullet_speed
            ai_bullet['y'] += ai_bullet['dy'] * ai_bullet_speed
            
            # 球飛出邊界就轉移球權給玩家
            if (
                ai_bullet['x'] < 0 or ai_bullet['x'] > width or
                ai_bullet['y'] < 0 or ai_bullet['y'] > height
            ):
                ai_bullet = None
                ball_owner = 'player'
        
        if bullet:
            # 檢查是否擊中電腦
            dist = ((bullet['x'] - ai_x) ** 2 + (bullet['y'] - ai_y) ** 2) ** 0.5
            if dist < circle_radius:
                bullet = None
                ai_hp -= 1
                if ai_hp <= 0:
                    winner = 'player'
                    player_hp = 3
                    ai_hp = 3

        if ai_bullet:
            if not is_hp_protect:
                # 檢查是否擊中玩家
                dist = ((ai_bullet['x'] - player_x) ** 2 + (ai_bullet['y'] - player_y) ** 2) ** 0.5
                if dist < circle_radius:
                    ai_bullet = None
                    player_hp -= 1
                    if player_hp <= 0:
                        winner = 'ai'
                        player_hp = 3
                        ai_hp = 3

        screen.fill(white)  # 設定畫面背景顏色
        
        # 顯示電腦血量（左上角）
        for i in range(ai_hp):
            pygame.draw.circle(screen, red, (20 + i * 20, 20), 8)
        # 顯示玩家血量（右下角）
        for i in range(player_hp):
            pygame.draw.circle(screen, red, (width - 20 - i * 20, height - 20), 8)

        # 繪製分割線
        pygame.draw.line(screen, black, (0, height // 2), (width, height // 2), 2) 
        # 繪製玩家
        pygame.draw.circle(screen, blue, (player_x, player_y), circle_radius, width = 2)
        if ball_owner == 'player':
            pygame.draw.circle(screen, blue, (player_x, player_y), circle_radius)
        # 繪製電腦
        pygame.draw.circle(screen, green, (ai_x, ai_y), circle_radius, width = 2)
        if ball_owner == 'ai':
            pygame.draw.circle(screen, green, (ai_x, ai_y), circle_radius)
        # 繪製準心
        if ball_owner == 'player':
            pygame.draw.circle(screen, red, (mouse_x, mouse_y), red_radius, width = 2)
        # 繪製躲避球
        if bullet:
            pygame.draw.circle(screen, black, (int(bullet['x']), int(bullet['y'])), 5)
        if ai_bullet:
            pygame.draw.circle(screen, black, (int(ai_bullet['x']), int(ai_bullet['y'])), 5)



        pygame.display.update()  # 更新畫面
        clock.tick(60)           # 設定畫面更新率(次 / 秒)

        if winner:
            return winner
        
def end_screen(winner):
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 40)

    while True:
        screen.fill((255, 255, 255))
        title = font.render(f"{winner.upper()} Win!", True, (0, 0, 0))
        screen.blit(title, (width // 2 - title.get_width() // 2, 150))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_width = 220
        button_height = 60
        gap = 40

        total_width = button_width * 2 + gap
        start_x = (width - total_width) // 2

        retry_rect = pygame.Rect(start_x, 300, button_width, button_height)
        home_rect = pygame.Rect(start_x + button_width + gap, 300, button_width, button_height)
        
        for rect, text in [(retry_rect, "Play again"), (home_rect, "Back home")]:
            hover = rect.collidepoint(mouse_x, mouse_y)
            pygame.draw.rect(screen, (100, 255, 100) if hover else (200, 200, 200), rect, border_radius=15)
            label = small_font.render(text, True, (0, 0, 0))
            text_x = rect.x + (rect.width - label.get_width()) // 2
            text_y = rect.y + (rect.height - label.get_height()) // 2
            screen.blit(label, (text_x, text_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(mouse_x, mouse_y):
                        return 'retry'
                    elif home_rect.collidepoint(mouse_x, mouse_y):
                        return 'menu'
                    
        pygame.display.update()


while True:
    menu_screen()
    while True:
        winner = main_game_loop()
        action = end_screen(winner)
        if action == 'menu':
            break
        elif action == 'retry':
            continue