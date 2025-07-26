import pygame
import random
import math
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Vertical")

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
SHIP_IMG = pygame.image.load(os.path.join(ASSET_DIR, "ship.png"))
SHIP_IMG = pygame.transform.scale(SHIP_IMG, (50, 40))
SHIP2_IMG = pygame.image.load(os.path.join(ASSET_DIR, "ship2.png"))
SHIP2_IMG = pygame.transform.scale(SHIP2_IMG, (50, 40))
METEOR_IMG = pygame.image.load(os.path.join(ASSET_DIR, "meteor.png"))
METEOR_IMG = pygame.transform.scale(METEOR_IMG, (40, 40))
ENEMY_IMG = pygame.image.load(os.path.join(ASSET_DIR, "enemy.png"))
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (50, 40))
ENEMY_ZIGZAG_IMG = pygame.image.load(os.path.join(ASSET_DIR, "enemy_zigzag.png"))
ENEMY_ZIGZAG_IMG = pygame.transform.scale(ENEMY_ZIGZAG_IMG, (50, 40))
ENEMY_SHOOTER_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "enemy_shooter.png")), (50, 40))
ENEMY_BOMBER_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "enemy_bomber.png")), (50, 40))
BG_IMG = pygame.image.load(os.path.join(ASSET_DIR, "space_bg.png"))
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))
LEVEL2_BG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "level2_bg.jpg")), (WIDTH, HEIGHT))
LEVEL3_BG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "level3_bg.png")), (WIDTH, HEIGHT))
LEVEL4_BG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "level4_bg.png")), (WIDTH, HEIGHT))
LEVEL5_BG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "level5_bg.jpg")), (WIDTH, HEIGHT))
BOSSSHIP_IMG = pygame.image.load(os.path.join(ASSET_DIR, "bossship1.png"))
BOSSSHIP_IMG = pygame.transform.scale(BOSSSHIP_IMG, (50, 40))
BOSS2_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boss2.png")), (120, 60))
BOSS3_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "boss3.png")), (100, 80))
GREG_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "greg.png")), (120, 60))
OVERLORD_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "overlord.png")), (180, 100))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW= (255, 255, 0)
BUTTON_COLOR = (30, 144, 255)
BUTTON_HOVER = (65, 105, 225)

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 40
PLAYER_SPEED = 5
BULLET_WIDTH, BULLET_HEIGHT = 8, 12
BULLET_SPEED = 10
METEOR_WIDTH, METEOR_HEIGHT = 40, 40
METEOR_SPEED_MIN = 3
METEOR_SPEED_MAX = 6
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 40
ENEMY_SPEED = 4

FONT = pygame.font.SysFont("Arial", 24)
BIG_FONT = pygame.font.SysFont("Arial", 48)
clock = pygame.time.Clock()

def draw_player(x, y, img):
    WIN.blit(img, (x, y))

def draw_bullet(x, y):
    pygame.draw.rect(WIN, YELLOW, (x, y, BULLET_WIDTH, BULLET_HEIGHT))

def draw_meteor(x, y, angle):
    rotated = pygame.transform.rotate(METEOR_IMG, math.degrees(angle))
    rect = rotated.get_rect(center=(int(x), int(y)))
    WIN.blit(rotated, rect.topleft)

def draw_enemy(x, y):
    WIN.blit(ENEMY_IMG, (x, y))

def draw_button(text, x, y, w, h, mouse_pos, mouse_click):
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(WIN, color, rect)
    pygame.draw.rect(WIN, WHITE, rect, 2)
    label = FONT.render(text, True, WHITE)
    WIN.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    if rect.collidepoint(mouse_pos) and mouse_click:
        return True
    return False

def game_loop(multiplayer=False):
    player1_score = 0
    player1_lives = 3
    player2_score = 0
    player2_lives = 3 if multiplayer else 0

    player1_x = WIDTH // 3 - PLAYER_WIDTH // 2 if multiplayer else WIDTH // 2 - PLAYER_WIDTH // 2
    player1_y = HEIGHT - PLAYER_HEIGHT - 20
    player1_rect = pygame.Rect(player1_x, player1_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_bullets = []
    if multiplayer:
        player2_x = WIDTH * 2 // 3 - PLAYER_WIDTH // 2
        player2_y = HEIGHT - PLAYER_HEIGHT - 20
        player2_rect = pygame.Rect(player2_x, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        player2_bullets = []
        player2_shoot_cooldown = 0
    meteors = []
    enemies = []
    meteor_timer = 0
    enemy_timer = 0
    run = True
    game_over = False
    level = 1
    zigzag_enemies = []
    zigzag_spawn_timer = 0

    # Boss 1 variables
    boss_active = False
    boss_intro = False
    boss_intro_timer = 0
    boss_name = "The Crimson Triad"
    boss_health = 60
    boss_x = WIDTH // 2
    boss_y = -100
    boss_speed = 2
    boss_bullets = []
    boss_fire_timer = 0
    boss_burst_count = 0
    boss_burst_pause = 0
    boss_defeated = False

    # Level 2 boss variables
    boss2_active = False
    boss2_health = 40
    boss2_img = BOSS2_IMG
    boss2_bombs = []
    boss2_bomb_timer = 0
    boss2_bomb_drops = 0
    boss2_vx = 6
    boss2_y = random.randint(0, HEIGHT//2)
    boss2_x = random.choice([0, WIDTH-120])
    boss2_direction = 1 if boss2_x == 0 else -1
    boss2_defeated = False

    # Level 3 variables
    shooter_enemies = []
    shooter_respawn_timer = 0
    boss3_active = False
    boss3_health = 50
    boss3_img = BOSS3_IMG
    boss3_x = random.choice([0, WIDTH-100])
    boss3_y = -80
    boss3_vy = 5
    boss3_bullets = []
    boss3_shoot_timer = 0
    boss3_defeated = False
    boss3_name = "The Charger"
    level_score = 0
    level3_score = 0

    # Level 4 variables
    bomber_enemy = None
    bomber_respawn_timer = 0
    greg_active = False
    greg_health = 60
    greg_x = 0
    greg_y = 60
    greg_vx = 10
    greg_particles = []
    greg_particle_timer = 0
    greg_defeated = False
    level4_score = 0

    # Level 5/final boss variables
    overlord_active = False
    overlord_health = 120
    overlord_x = WIDTH // 2 - 90
    overlord_y = 40
    overlord_vx = 6
    overlord_bullets = []
    overlord_homing = []
    overlord_shoot_timer = 0
    overlord_defeated = False
    level5_score = 0

    while run:
        clock.tick(60)
        # Background switch
        if level == 2:
            WIN.blit(LEVEL2_BG, (0, 0))
        elif level == 3:
            WIN.blit(LEVEL3_BG, (0, 0))
        elif level == 4:
            WIN.blit(LEVEL4_BG, (0, 0))
        elif level == 5:
            WIN.blit(LEVEL5_BG, (0, 0))
        else:
            WIN.blit(BG_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # --- Boss Trigger ---
        if not boss_active and not boss_defeated and level == 1:
            if (not multiplayer and player1_score >= 50) or (multiplayer and player1_score + player2_score >= 50):
                boss_active = True
                boss_intro = True
                boss_intro_timer = 120

        if not boss2_active and not boss2_defeated and level == 2:
            if (not multiplayer and level_score >= 50) or (multiplayer and level_score >= 50):
                boss2_active = True
                boss2_bomb_timer = 0
                boss2_bomb_drops = 0
                boss2_health = 40
                boss2_y = random.randint(0, HEIGHT//2)
                boss2_x = random.choice([0, WIDTH-120])
                boss2_direction = 1 if boss2_x == 0 else -1

        if not boss3_active and not boss3_defeated and level == 3:
            if (not multiplayer and level3_score >= 50) or (multiplayer and level3_score >= 50):
                boss3_active = True
                boss3_health = 50
                boss3_x = random.randint(0, WIDTH-100)
                boss3_y = -80
                boss3_vy = 5
                boss3_bullets = []
                boss3_shoot_timer = 0

        if not greg_active and not greg_defeated and level == 4:
            if (not multiplayer and level4_score >= 50) or (multiplayer and level4_score >= 50):
                greg_active = True
                greg_health = 60
                greg_x = 0
                greg_y = 60
                greg_vx = 10
                greg_particles = []
                greg_particle_timer = 0

        if not overlord_active and not overlord_defeated and level == 5:
            if (not multiplayer and level5_score >= 50) or (multiplayer and level5_score >= 50):
                overlord_active = True
                overlord_health = 120
                overlord_x = WIDTH // 2 - 90
                overlord_y = 40
                overlord_vx = 6
                overlord_bullets = []
                overlord_homing = []
                overlord_shoot_timer = 0

        # --- Player Controls ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player1_x > 0:
            player1_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player1_x < WIDTH - PLAYER_WIDTH:
            player1_x += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            if len(player1_bullets) == 0 or player1_bullets[-1][1] < player1_y - 20:
                player1_bullets.append([player1_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player1_y])
        player1_rect.x = player1_x

        if multiplayer:
            if keys[pygame.K_a] and player2_x > 0:
                player2_x -= PLAYER_SPEED
            if keys[pygame.K_d] and player2_x < WIDTH - PLAYER_WIDTH:
                player2_x += PLAYER_SPEED
            if player2_shoot_cooldown > 0:
                player2_shoot_cooldown -= 1
            if keys[pygame.K_LSHIFT]:
                if (len(player2_bullets) == 0 or player2_bullets[-1][1] < player2_y - 20) and player2_shoot_cooldown == 0:
                    player2_bullets.append([player2_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player2_y])
                    player2_shoot_cooldown = 10
            player2_rect.x = player2_x

        # --- Level 1: Normal Enemies and Meteors ---
        if not boss_active and not boss_defeated and level == 1:
            meteor_timer += 1
            if meteor_timer > 30:
                meteor_timer = 0
                mx = random.randint(0, WIDTH - METEOR_WIDTH)
                angle = random.uniform(math.radians(75), math.radians(105))
                speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX)
                meteors.append([mx, -METEOR_HEIGHT, angle, speed])

            for m in meteors[:]:
                m[0] += m[3] * math.cos(m[2])
                m[1] += m[3] * math.sin(m[2])
                meteor_rect = pygame.Rect(m[0] - METEOR_WIDTH//2, m[1] - METEOR_HEIGHT//2, METEOR_WIDTH, METEOR_HEIGHT)
                draw_meteor(m[0], m[1], m[2])
                if meteor_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    meteors.remove(m)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and meteor_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    meteors.remove(m)
                    if player2_lives <= 0:
                        game_over = True
                elif m[1] > HEIGHT:
                    meteors.remove(m)

            enemy_timer += 1
            if enemy_timer > 90:
                enemy_timer = 0
                ex = random.randint(0, WIDTH - ENEMY_WIDTH)
                enemies.append([ex, -ENEMY_HEIGHT])

            for e in enemies[:]:
                e[1] += ENEMY_SPEED
                enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                draw_enemy(e[0], e[1])
                if enemy_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    enemies.remove(e)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and enemy_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    enemies.remove(e)
                    if player2_lives <= 0:
                        game_over = True
                elif e[1] > HEIGHT:
                    enemies.remove(e)

        # --- Boss 1 Logic ---
        if boss_active:
            # Dramatic entrance
            if boss_intro:
                boss_y += boss_speed
                if boss_y >= 80:
                    boss_y = 80
                    boss_intro_timer -= 1
                    name_text = BIG_FONT.render(boss_name, True, (255, 50, 50))
                    WIN.blit(name_text, (WIDTH//2 - name_text.get_width()//2, boss_y - 60))
                    if boss_intro_timer <= 0:
                        boss_intro = False
                else:
                    name_text = BIG_FONT.render(boss_name, True, (255, 50, 50))
                    WIN.blit(name_text, (WIDTH//2 - name_text.get_width()//2, boss_y - 60))
            else:
                for i in range(-1, 2):
                    WIN.blit(BOSSSHIP_IMG, (boss_x + i*60 - BOSSSHIP_IMG.get_width()//2, boss_y))
                if boss_burst_pause > 0:
                    boss_burst_pause -= 1
                else:
                    boss_fire_timer += 1
                    if boss_fire_timer > 15:
                        boss_fire_timer = 0
                        boss_burst_count += 1
                        for i in range(-1, 2):
                            boss_bullets.append([boss_x + i*60, boss_y + BOSSSHIP_IMG.get_height(), 7])
                        if boss_burst_count >= 3:
                            boss_burst_pause = 60
                            boss_burst_count = 0
                boss_x += random.choice([-1, 0, 1]) * 2
                boss_x = max(90, min(WIDTH-90, boss_x))
                for b in boss_bullets[:]:
                    b[1] += b[2]
                    pygame.draw.rect(WIN, (255, 50, 50), (b[0], b[1], 12, 18))
                    if pygame.Rect(b[0], b[1], 12, 18).colliderect(player1_rect):
                        player1_lives -= 1
                        boss_bullets.remove(b)
                        if player1_lives <= 0:
                            game_over = True
                    elif multiplayer and pygame.Rect(b[0], b[1], 12, 18).colliderect(player2_rect):
                        player2_lives -= 1
                        boss_bullets.remove(b)
                        if player2_lives <= 0:
                            game_over = True
                    elif b[1] > HEIGHT:
                        boss_bullets.remove(b)
                for b in player1_bullets[:]:
                    for i in range(-1, 2):
                        boss_rect = pygame.Rect(boss_x + i*60 - BOSSSHIP_IMG.get_width()//2, boss_y, BOSSSHIP_IMG.get_width(), BOSSSHIP_IMG.get_height())
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(boss_rect):
                            player1_bullets.remove(b)
                            boss_health -= 1
                            player1_score += 10
                            break
                if multiplayer:
                    for b in player2_bullets[:]:
                        for i in range(-1, 2):
                            boss_rect = pygame.Rect(boss_x + i*60 - BOSSSHIP_IMG.get_width()//2, boss_y, BOSSSHIP_IMG.get_width(), BOSSSHIP_IMG.get_height())
                            bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                            if bullet_rect.colliderect(boss_rect):
                                player2_bullets.remove(b)
                                boss_health -= 1
                                player2_score += 10
                                break
                if boss_health <= 0:
                    WIN.blit(BG_IMG, (0, 0))
                    win_text = BIG_FONT.render("Boss Defeated!", True, (255, 50, 50))
                    WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                    score1_text = FONT.render(f"P1 Score: {player1_score}", True, WHITE)
                    WIN.blit(score1_text, (WIDTH//2 - score1_text.get_width()//2, HEIGHT//2))
                    if multiplayer:
                        score2_text = FONT.render(f"P2 Score: {player2_score}", True, WHITE)
                        WIN.blit(score2_text, (WIDTH//2 - score2_text.get_width()//2, HEIGHT//2 + 30))
                    pygame.display.flip()
                    pygame.time.wait(2500)
                    boss_active = False
                    boss_defeated = True
                    level = 2
                    meteors.clear()
                    enemies.clear()
                    zigzag_enemies.clear()
                    continue

        # --- Level 2: Meteors, Regular Enemies, Zigzag Enemies ---
        if not boss2_active and not boss2_defeated and level == 2:
            meteor_timer += 1
            if meteor_timer > 30:
                meteor_timer = 0
                mx = random.randint(0, WIDTH - METEOR_WIDTH)
                angle = random.uniform(math.radians(75), math.radians(105))
                speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX)
                meteors.append([mx, -METEOR_HEIGHT, angle, speed])

            for m in meteors[:]:
                m[0] += m[3] * math.cos(m[2])
                m[1] += m[3] * math.sin(m[2])
                meteor_rect = pygame.Rect(m[0] - METEOR_WIDTH//2, m[1] - METEOR_HEIGHT//2, METEOR_WIDTH, METEOR_HEIGHT)
                draw_meteor(m[0], m[1], m[2])
                if meteor_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    meteors.remove(m)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and meteor_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    meteors.remove(m)
                    if player2_lives <= 0:
                        game_over = True
                elif m[1] > HEIGHT:
                    meteors.remove(m)

            enemy_timer += 1
            if enemy_timer > 90:
                enemy_timer = 0
                ex = random.randint(0, WIDTH - ENEMY_WIDTH)
                enemies.append([ex, -ENEMY_HEIGHT])

            for e in enemies[:]:
                e[1] += ENEMY_SPEED
                enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                draw_enemy(e[0], e[1])
                if enemy_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    enemies.remove(e)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and enemy_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    enemies.remove(e)
                    if player2_lives <= 0:
                        game_over = True
                elif e[1] > HEIGHT:
                    enemies.remove(e)

            zigzag_spawn_timer += 1
            if zigzag_spawn_timer > 60:
                zigzag_spawn_timer = 0
                from_left = random.choice([True, False])
                if from_left:
                    x = 0
                    vx = 5
                else:
                    x = WIDTH - 50
                    vx = -5
                # Spawn only in upper half, not too low
                y = random.randint(40, HEIGHT // 2 - 60)
                vy = random.choice([3, 4])
                zigzag_enemies.append([x, y, vx, vy])

            for z in zigzag_enemies[:]:
                z[0] += z[2]
                z[1] += z[3]
                if z[0] <= 0 or z[0] >= WIDTH - 50:
                    z[2] *= -1
                if z[1] > HEIGHT:
                    zigzag_enemies.remove(z)
                    continue
                WIN.blit(ENEMY_ZIGZAG_IMG, (z[0], z[1]))
                zigzag_rect = pygame.Rect(z[0], z[1], 50, 40)
                if zigzag_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    zigzag_enemies.remove(z)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and zigzag_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    zigzag_enemies.remove(z)
                    if player2_lives <= 0:
                        game_over = True

        # --- Level 3: Shooter Enemies ---
        if not boss3_active and not boss3_defeated and level == 3:
            # Only two shooter ships at a time, one on each side
            if len(shooter_enemies) < 2 and shooter_respawn_timer <= 0:
                shooter_enemies.clear()
                shooter_enemies.append([0, 100, 1, 0, 0])  # x, y, direction, shoot_timer, burst_count
                shooter_enemies.append([WIDTH-50, 100, -1, 0, 0])
                shooter_respawn_timer = 0
            else:
                shooter_respawn_timer = max(0, shooter_respawn_timer - 1)

            for s in shooter_enemies[:]:
                s[0] += s[2]*2
                if s[0] < 0 or s[0] > WIDTH-50:
                    s[2] *= -1
                WIN.blit(ENEMY_SHOOTER_IMG, (s[0], s[1]))
                # Shooting logic
                s[3] += 1
                if s[3] > 30 and s[4] < 3:
                    s[3] = 0
                    s[4] += 1
                    # Shoot 3 bullets at player(s)
                    for px, py in [(player1_x, player1_y)] + ([(player2_x, player2_y)] if multiplayer else []):
                        dx = (px + PLAYER_WIDTH//2) - (s[0] + 25)
                        dy = (py + PLAYER_HEIGHT//2) - (s[1] + 40)
                        length = math.hypot(dx, dy)
                        if length == 0: length = 1
                        vx = dx / length * 7
                        vy = dy / length * 7
                        meteors.append([s[0]+25, s[1]+40, math.atan2(vy, vx), 8])
                if s[4] >= 3 and s[3] > 60:
                    s[4] = 0
                    s[3] = 0
                # Collision
                shooter_rect = pygame.Rect(s[0], s[1], 50, 40)
                if shooter_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    shooter_enemies.remove(s)
                    shooter_respawn_timer = 180
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and shooter_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    shooter_enemies.remove(s)
                    shooter_respawn_timer = 180
                    if player2_lives <= 0:
                        game_over = True

            # Player bullets hit shooter enemies
            for b in player1_bullets[:]:
                hit = False
                for s in shooter_enemies[:]:
                    shooter_rect = pygame.Rect(s[0], s[1], 50, 40)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(shooter_rect):
                        shooter_enemies.remove(s)
                        player1_bullets.remove(b)
                        player1_score += 15
                        level3_score += 15
                        shooter_respawn_timer = 180
                        hit = True
                        break
                if hit:
                    continue
            if multiplayer:
                for b in player2_bullets[:]:
                    hit = False
                    for s in shooter_enemies[:]:
                        shooter_rect = pygame.Rect(s[0], s[1], 50, 40)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(shooter_rect):
                            shooter_enemies.remove(s)
                            player2_bullets.remove(b)
                            player2_score += 15
                            level3_score += 15
                            shooter_respawn_timer = 180
                            hit = True
                            break
                    if hit:
                        continue

        # --- Level 4: Bomber Enemy ---
        if not greg_active and not greg_defeated and level == 4:
            # Only one bomber alive at a time, respawn after 4 seconds
            if not bomber_enemy and bomber_respawn_timer <= 0:
                bomber_enemy = [0, 80, 3, 0]  # x, y, vx, bomb_timer
                bomber_respawn_timer = 0
            elif not bomber_enemy:
                bomber_respawn_timer = max(0, bomber_respawn_timer - 1)
            if bomber_enemy:
                bomber_enemy[0] += bomber_enemy[2]
                if bomber_enemy[0] > WIDTH:
                    bomber_enemy[0] = 0
                WIN.blit(ENEMY_BOMBER_IMG, (bomber_enemy[0], bomber_enemy[1]))
                bomber_enemy[3] += 1
                if bomber_enemy[3] > 40:
                    bomber_enemy[3] = 0
                    meteors.append([bomber_enemy[0]+25, bomber_enemy[1]+40, math.radians(90), 7])
                bomber_rect = pygame.Rect(bomber_enemy[0], bomber_enemy[1], 50, 40)
                if bomber_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    bomber_enemy = None
                    bomber_respawn_timer = 240
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and bomber_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    bomber_enemy = None
                    bomber_respawn_timer = 240
                    if player2_lives <= 0:
                        game_over = True
            # Player bullets hit bomber
            for b in player1_bullets[:]:
                if bomber_enemy:
                    bomber_rect = pygame.Rect(bomber_enemy[0], bomber_enemy[1], 50, 40)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(bomber_rect):
                        bomber_enemy = None
                        bomber_respawn_timer = 240
                        player1_bullets.remove(b)
                        player1_score += 25
                        level4_score += 25
                        break
            if multiplayer:
                for b in player2_bullets[:]:
                    if bomber_enemy:
                        bomber_rect = pygame.Rect(bomber_enemy[0], bomber_enemy[1], 50, 40)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(bomber_rect):
                            bomber_enemy = None
                            bomber_respawn_timer = 240
                            player2_bullets.remove(b)
                            player2_score += 25
                            level4_score += 25
                            break

        # --- Level 4 Boss ("Greg") Logic ---
        if greg_active and not greg_defeated and level == 4:
            WIN.blit(LEVEL4_BG, (0, 0))
            WIN.blit(GREG_IMG, (greg_x, greg_y))
            greg_x += greg_vx
            if greg_x < 0 or greg_x > WIDTH-120:
                greg_vx *= -1
            greg_particle_timer += 1
            if greg_particle_timer > 20:
                greg_particle_timer = 0
                # Drop 5 slow particles spaced out
                for i in range(5):
                    px = greg_x + 10 + i*20
                    greg_particles.append([px, greg_y+60, 0, 3])
            for p in greg_particles[:]:
                p[1] += p[3]
                pygame.draw.rect(WIN, (100, 255, 255), (p[0], p[1], 16, 16))
                particle_rect = pygame.Rect(p[0], p[1], 16, 16)
                if particle_rect.colliderect(player1_rect):
                    player1_lives -= 1
                    greg_particles.remove(p)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and particle_rect.colliderect(player2_rect):
                    player2_lives -= 1
                    greg_particles.remove(p)
                    if player2_lives <= 0:
                        game_over = True
                elif p[1] > HEIGHT:
                    greg_particles.remove(p)
            # Player bullets hit boss
            for b in player1_bullets[:]:
                boss_rect = pygame.Rect(greg_x, greg_y, 120, 60)
                bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                if bullet_rect.colliderect(boss_rect):
                    player1_bullets.remove(b)
                    greg_health -= 1
                    player1_score += 10
                    break
            if multiplayer:
                for b in player2_bullets[:]:
                    boss_rect = pygame.Rect(greg_x, greg_y, 120, 60)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(boss_rect):
                        player2_bullets.remove(b)
                        greg_health -= 1
                        player2_score += 10
                        break
            if greg_health <= 0:
                WIN.blit(LEVEL4_BG, (0, 0))
                win_text = BIG_FONT.render("Boss Defeated!", True, (255, 50, 50))
                WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                pygame.display.flip()
                pygame.time.wait(2500)
                greg_active = False
                greg_defeated = True
                level = 5
                meteors.clear()
                enemies.clear()
                zigzag_enemies.clear()
                shooter_enemies.clear()
                bomber_enemy = None
                greg_particles.clear()
                level4_score = 0
                continue

        # --- Level 5 Final Boss ("The Overlord") ---
        if overlord_active and not overlord_defeated and level == 5:
            WIN.blit(LEVEL5_BG, (0, 0))
            WIN.blit(OVERLORD_IMG, (overlord_x, overlord_y))
            overlord_x += overlord_vx
            if overlord_x < 0 or overlord_x > WIDTH-180:
                overlord_vx *= -1
            overlord_shoot_timer += 1
            # Bullet spread every 40 frames
            if overlord_shoot_timer % 40 == 0:
                for angle in [-0.5, -0.25, 0, 0.25, 0.5]:
                    overlord_bullets.append([overlord_x+90, overlord_y+100, 8*math.sin(angle), 8*math.cos(angle)])
            # Homing shot every 90 frames
            if overlord_shoot_timer % 90 == 0:
                for px, py in [(player1_x, player1_y)] + ([(player2_x, player2_y)] if multiplayer else []):
                    dx = (px + PLAYER_WIDTH//2) - (overlord_x + 90)
                    dy = (py + PLAYER_HEIGHT//2) - (overlord_y + 100)
                    length = math.hypot(dx, dy)
                    if length == 0: length = 1
                    vx = dx / length * 7
                    vy = dy / length * 7
                    overlord_homing.append([overlord_x+90, overlord_y+100, vx, vy])
            # Move and draw bullets
            for b in overlord_bullets[:]:
                b[0] += b[2]
                b[1] += b[3]
                pygame.draw.rect(WIN, (255, 100, 0), (b[0], b[1], 14, 20))
                if pygame.Rect(b[0], b[1], 14, 20).colliderect(player1_rect):
                    player1_lives -= 1
                    overlord_bullets.remove(b)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and pygame.Rect(b[0], b[1], 14, 20).colliderect(player2_rect):
                    player2_lives -= 1
                    overlord_bullets.remove(b)
                    if player2_lives <= 0:
                        game_over = True
                elif b[1] > HEIGHT or b[0] < 0 or b[0] > WIDTH:
                    overlord_bullets.remove(b)
            # Move and draw homing
            for h in overlord_homing[:]:
                h[0] += h[2]
                h[1] += h[3]
                pygame.draw.rect(WIN, (0, 255, 255), (h[0], h[1], 12, 18))
                if pygame.Rect(h[0], h[1], 12, 18).colliderect(player1_rect):
                    player1_lives -= 1
                    overlord_homing.remove(h)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and pygame.Rect(h[0], h[1], 12, 18).colliderect(player2_rect):
                    player2_lives -= 1
                    overlord_homing.remove(h)
                    if player2_lives <= 0:
                        game_over = True
                elif h[1] > HEIGHT or h[0] < 0 or h[0] > WIDTH:
                    overlord_homing.remove(h)
            # Player bullets hit boss
            for b in player1_bullets[:]:
                boss_rect = pygame.Rect(overlord_x, overlord_y, 180, 100)
                bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                if bullet_rect.colliderect(boss_rect):
                    player1_bullets.remove(b)
                    overlord_health -= 1
                    player1_score += 10
                    break
            if multiplayer:
                for b in player2_bullets[:]:
                    boss_rect = pygame.Rect(overlord_x, overlord_y, 180, 100)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(boss_rect):
                        player2_bullets.remove(b)
                        overlord_health -= 1
                        player2_score += 10
                        break
            if overlord_health <= 0:
                WIN.blit(LEVEL5_BG, (0, 0))
                win_text = BIG_FONT.render("You Win!", True, (255, 255, 0))
                WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                pygame.display.flip()
                pygame.time.wait(4000)
                overlord_active = False
                overlord_defeated = True
                meteors.clear()
                enemies.clear()
                zigzag_enemies.clear()
                shooter_enemies.clear()
                bomber_enemy = None
                greg_particles.clear()
                overlord_bullets.clear()
                overlord_homing.clear()
                return "restart"

        # --- Player Bullets ---
        for b in player1_bullets[:]:
            b[1] -= BULLET_SPEED
            draw_bullet(b[0], b[1])
            if b[1] < -BULLET_HEIGHT:
                player1_bullets.remove(b)
            else:
                hit = False
                # Regular enemies
                for e in enemies[:]:
                    enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(enemy_rect):
                        enemies.remove(e)
                        player1_bullets.remove(b)
                        player1_score += 5
                        if level == 2:
                            level_score += 5
                        if level == 3:
                            level3_score += 5
                        if level == 4:
                            level4_score += 5
                        if level == 5:
                            level5_score += 5
                        hit = True
                        break
                if hit:
                    continue
                # Zigzag enemies
                for z in zigzag_enemies[:]:
                    zigzag_rect = pygame.Rect(z[0], z[1], 50, 40)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(zigzag_rect):
                        zigzag_enemies.remove(z)
                        player1_bullets.remove(b)
                        player1_score += 10
                        if level == 2:
                            level_score += 10
                        if level == 3:
                            level3_score += 10
                        if level == 4:
                            level4_score += 10
                        if level == 5:
                            level5_score += 10
                        hit = True
                        break

        if multiplayer:
            for b in player2_bullets[:]:
                b[1] -= BULLET_SPEED
                draw_bullet(b[0], b[1])
                if b[1] < -BULLET_HEIGHT:
                    player2_bullets.remove(b)
                else:
                    hit = False
                    # Regular enemies
                    for e in enemies[:]:
                        enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(enemy_rect):
                            enemies.remove(e)
                            player2_bullets.remove(b)
                            player2_score += 5
                            if level == 2:
                                level_score += 5
                            if level == 3:
                                level3_score += 5
                            if level == 4:
                                level4_score += 5
                            if level == 5:
                                level5_score += 5
                            hit = True
                            break
                    if hit:
                        continue
                    # Zigzag enemies
                    for z in zigzag_enemies[:]:
                        zigzag_rect = pygame.Rect(z[0], z[1], 50, 40)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(zigzag_rect):
                            zigzag_enemies.remove(z)
                            player2_bullets.remove(b)
                            player2_score += 10
                            if level == 2:
                                level_score += 10
                            if level == 3:
                                level3_score += 10
                            if level == 4:
                                level4_score += 10
                            if level == 5:
                                level5_score += 10
                            hit = True
                            break

        # --- Draw Players ---
        draw_player(player1_x, player1_y, SHIP_IMG)
        if multiplayer:
            draw_player(player2_x, player2_y, SHIP2_IMG)

        # --- Draw Lives ---
        for i in range(player1_lives):
            WIN.blit(SHIP_IMG, (10 + i * (PLAYER_WIDTH + 5), HEIGHT - PLAYER_HEIGHT - 5))
        if multiplayer:
            for i in range(player2_lives):
                WIN.blit(SHIP2_IMG, (WIDTH - (i + 1) * (PLAYER_WIDTH + 5), HEIGHT - PLAYER_HEIGHT - 5))

        # --- Draw Scores ---
        score1_text = FONT.render(f"P1 Score: {player1_score}", True, WHITE)
        WIN.blit(score1_text, (10, HEIGHT - PLAYER_HEIGHT - 35))
        if multiplayer:
            score2_text = FONT.render(f"P2 Score: {player2_score}", True, WHITE)
            WIN.blit(score2_text, (WIDTH - score2_text.get_width() - 10, HEIGHT - PLAYER_HEIGHT - 35))

        # --- Game Over ---
        if player1_lives <= 0 or (multiplayer and player2_lives <= 0):
            if level == 2:
                WIN.blit(LEVEL2_BG, (0, 0))
            elif level == 3:
                WIN.blit(LEVEL3_BG, (0, 0))
            elif level == 4:
                WIN.blit(LEVEL4_BG, (0, 0))
            elif level == 5:
                WIN.blit(LEVEL5_BG, (0, 0))
            else:
                WIN.blit(BG_IMG, (0, 0))
            over_text = BIG_FONT.render("Game Over!", True, WHITE)
            WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
            score1_text = FONT.render(f"P1 Score: {player1_score}", True, WHITE)
            WIN.blit(score1_text, (WIDTH//2 - score1_text.get_width()//2, HEIGHT//2))
            if multiplayer:
                score2_text = FONT.render(f"P2 Score: {player2_score}", True, WHITE)
                WIN.blit(score2_text, (WIDTH//2 - score2_text.get_width()//2, HEIGHT//2 + 30))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]
            if draw_button("Restart", WIDTH//2 - 75, HEIGHT//2 + 80, 150, 50, mouse_pos, mouse_click):
                return "restart"
            pygame.display.flip()
            pygame.time.wait(100)
            continue

        pygame.display.flip()

def mode_menu():
    while True:
        WIN.blit(BG_IMG, (0, 0))
        title = BIG_FONT.render("Select Mode", True, WHITE)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if draw_button("Single Player", WIDTH//2 - 150, HEIGHT//2, 140, 50, mouse_pos, mouse_click):
            return False
        if draw_button("Multiplayer", WIDTH//2 + 10, HEIGHT//2, 140, 50, mouse_pos, mouse_click):
            return True
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.time.wait(100)

def main_menu():
    while True:
        WIN.blit(BG_IMG, (0, 0))
        title = BIG_FONT.render("Space Shooter", True, WHITE)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if draw_button("Start", WIDTH//2 - 75, HEIGHT//2, 150, 50, mouse_pos, mouse_click):
            return
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.time.wait(100)

def main():
    while True:
        main_menu()
        pygame.time.wait(200)
        pygame.event.clear()
        multiplayer = mode_menu()
        result = game_loop(multiplayer)
        if result == "quit":
            break

if __name__ == "__main__":
    main()
