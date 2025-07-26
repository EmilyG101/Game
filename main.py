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
        if boss_active and not boss_defeated and level == 1:
            WIN.blit(BOSSSHIP_IMG, (boss_x, boss_y))
            if boss_intro:
                boss_intro_timer -= 1
                if boss_intro_timer <= 0:
                    boss_intro = False
            else:
                if boss_y < HEIGHT // 4:
                    boss_y += boss_speed
                else:
                    boss_y = HEIGHT // 4
                if boss_x < player1_x:
                    boss_x += boss_speed
                elif boss_x > player1_x + PLAYER_WIDTH:
                    boss_x -= boss_speed
                if boss_y >= 0 and boss_y < HEIGHT // 4:
                    boss_speed += 0.001
                if boss_speed > 2:
                    boss_speed = 2

            # Boss shooting
            boss_fire_timer += 1
            if boss_fire_timer > 20:
                boss_fire_timer = 0
                if random.random() < 0.5:
                    # Single bullet
                    dx = (player1_x + PLAYER_WIDTH // 2) - (boss_x + 25)
                    dy = (player1_y + PLAYER_HEIGHT // 2) - (boss_y + 40)
                    length = math.hypot(dx, dy)
                    if length == 0: length = 1
                    vx = dx / length * 5
                    vy = dy / length * 5
                    boss_bullets.append([boss_x + 25, boss_y + 40, vx, vy])
                else:
                    # Burst of 3 bullets
                    for angle in [-0.3, 0, 0.3]:
                        vx = 5 * math.sin(angle)
                        vy = 5 * math.cos(angle)
                        boss_bullets.append([boss_x + 25, boss_y + 40, vx, vy])

            for b in boss_bullets[:]:
                b[0] += b[2]
                b[1] += b[3]
                pygame.draw.rect(WIN, (255, 0, 255), (b[0], b[1], 14, 20))
                if pygame.Rect(b[0], b[1], 14, 20).colliderect(player1_rect):
                    player1_lives -= 1
                    boss_bullets.remove(b)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and pygame.Rect(b[0], b[1], 14, 20).colliderect(player2_rect):
                    player2_lives -= 1
                    boss_bullets.remove(b)
                    if player2_lives <= 0:
                        game_over = True
                elif b[1] > HEIGHT or b[0] < 0 or b[0] > WIDTH:
                    boss_bullets.remove(b)

            # Player bullets hit boss
            for b in player1_bullets[:]:
                boss_rect = pygame.Rect(boss_x, boss_y, 50, 40)
                bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                if bullet_rect.colliderect(boss_rect):
                    player1_bullets.remove(b)
                    boss_health -= 1
                    player1_score += 10
                    break
            if multiplayer:
                for b in player2_bullets[:]:
                    boss_rect = pygame.Rect(boss_x, boss_y, 50, 40)
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
                pygame.display.flip()
                pygame.time.wait(2500)
                boss_active = False
                boss_defeated = True
                level = 2
                meteors.clear()
                enemies.clear()
                zigzag_enemies.clear()
                boss_bullets.clear()
                continue

        # --- Level 2 Boss Logic ---
        if boss2_active and not boss2_defeated and level == 2:
            WIN.blit(boss2_img, (boss2_x, boss2_y))
            boss2_x += boss2_vx * boss2_direction
            if boss2_x <= 0 or boss2_x >= WIDTH - 120:
                boss2_direction *= -1
            boss2_bomb_timer += 1
            if boss2_bomb_timer > 60:
                boss2_bomb_timer = 0
                boss2_bombs.append([boss2_x + 60, boss2_y + 60, 6])
            for bomb in boss2_bombs[:]:
                bomb[1] += bomb[2]
                pygame.draw.rect(WIN, (255, 200, 0), (bomb[0], bomb[1], 16, 24))
                if pygame.Rect(bomb[0], bomb[1], 16, 24).colliderect(player1_rect):
                    player1_lives -= 1
                    boss2_bombs.remove(bomb)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and pygame.Rect(bomb[0], bomb[1], 16, 24).colliderect(player2_rect):
                    player2_lives -= 1
                    boss2_bombs.remove(bomb)
                    if player2_lives <= 0:
                        game_over = True
                elif bomb[1] > HEIGHT:
                    boss2_bombs.remove(bomb)
            # Player bullets hit boss2
            for b in player1_bullets[:]:
                boss2_rect = pygame.Rect(boss2_x, boss2_y, 120, 60)
                bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                if bullet_rect.colliderect(boss2_rect):
                    player1_bullets.remove(b)
                    boss2_health -= 1
                    player1_score += 10
                    break
            if multiplayer:
                for b in player2_bullets[:]:
                    boss2_rect = pygame.Rect(boss2_x, boss2_y, 120, 60)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(boss2_rect):
                        player2_bullets.remove(b)
                        boss2_health -= 1
                        player2_score += 10
                        break
            if boss2_health <= 0:
                WIN.blit(LEVEL2_BG, (0, 0))
                win_text = BIG_FONT.render("Boss Defeated!", True, (255, 50, 50))
                WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                pygame.display.flip()
                pygame.time.wait(2500)
                boss2_active = False
                boss2_defeated = True
                level = 3
                meteors.clear()
                enemies.clear()
                zigzag_enemies.clear()
                boss2_bombs.clear()
                level_score = 0
                continue

        # --- Level 2: Meteors, Regular Enemies, Zigzag Enemies ---
        if not boss2_active and not boss2_defeated and level == 2:
            # Meteors
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

            # Regular enemies
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

            # Zigzag enemies
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

        # --- Level 3 Boss Logic ---
        if boss3_active and not boss3_defeated and level == 3:
            WIN.blit(boss3_img, (boss3_x, boss3_y))
            boss3_y += boss3_vy
            if boss3_y < 60:
                boss3_vy = abs(boss3_vy)
            elif boss3_y > HEIGHT // 2:
                boss3_vy = -abs(boss3_vy)
            boss3_shoot_timer += 1
            if boss3_shoot_timer > 30:
                boss3_shoot_timer = 0
                # Shoot 3 bullets in a spread
                for angle in [-0.3, 0, 0.3]:
                    vx = 8 * math.sin(angle)
                    vy = 8 * math.cos(angle)
                    boss3_bullets.append([boss3_x + 50, boss3_y + 80, vx, vy])
            for b in boss3_bullets[:]:
                b[0] += b[2]
                b[1] += b[3]
                pygame.draw.rect(WIN, (255, 0, 255), (b[0], b[1], 14, 20))
                if pygame.Rect(b[0], b[1], 14, 20).colliderect(player1_rect):
                    player1_lives -= 1
                    boss3_bullets.remove(b)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and pygame.Rect(b[0], b[1], 14, 20).colliderect(player2_rect):
                    player2_lives -= 1
                    boss3_bullets.remove(b)
                    if player2_lives <= 0:
                        game_over = True
                elif b[1] > HEIGHT or b[0] < 0 or b[0] > WIDTH:
                    boss3_bullets.remove(b)
            # Player bullets hit boss3
            for b in player1_bullets[:]:
                boss3_rect = pygame.Rect(boss3_x, boss3_y, 100, 80)
                bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                if bullet_rect.colliderect(boss3_rect):
                    player1_bullets.remove(b)
                    boss3_health -= 1
                    player1_score += 10
                    break
            if multiplayer:
                for b in player2_bullets[:]:
                    boss3_rect = pygame.Rect(boss3_x, boss3_y, 100, 80)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(boss3_rect):
                        player2_bullets.remove(b)
                        boss3_health -= 1
                        player2_score += 10
                        break
            if boss3_health <= 0:
                WIN.blit(LEVEL3_BG, (0, 0))
                win_text = BIG_FONT.render("Boss Defeated!", True, (255, 50, 50))
                WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                pygame.display.flip()
                pygame.time.wait(2500)
                boss3_active = False
                boss3_defeated = True
                level = 4
                meteors.clear()
                enemies.clear()
                zigzag_enemies.clear()
                shooter_enemies.clear()
                boss3_bullets.clear()
                level3_score = 0
                continue

        # --- Level 3: Shooter Enemies ---
        if not boss3_active and not boss3_defeated and level == 3:
            # Meteors
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

            # Regular enemies
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

            # Zigzag enemies
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

            # Shooter enemies with individual respawn timers
            for s in shooter_enemies:
                if not s['alive']:
                    s['respawn_timer'] -= 1
                    if s['respawn_timer'] <= 0:
                        s['x'] = 0 if s['dir'] == 1 else WIDTH-50
                        s['y'] = 100
                        s['shoot_timer'] = 0
                        s['burst_count'] = 0
                        s['alive'] = True
                else:
                    s['x'] += s['dir']*2
                    if s['x'] < 0 or s['x'] > WIDTH-50:
                        s['dir'] *= -1
                    WIN.blit(ENEMY_SHOOTER_IMG, (s['x'], s['y']))
                    # Shooting logic
                    s['shoot_timer'] += 1
                    if s['shoot_timer'] > 30 and s['burst_count'] < 3:
                        s['shoot_timer'] = 0
                        s['burst_count'] += 1
                        for px, py in [(player1_x, player1_y)] + ([(player2_x, player2_y)] if multiplayer else []):
                            dx = (px + PLAYER_WIDTH//2) - (s['x'] + 25)
                            dy = (py + PLAYER_HEIGHT//2) - (s['y'] + 40)
                            length = math.hypot(dx, dy)
                            if length == 0: length = 1
                            vx = dx / length * 7
                            vy = dy / length * 7
                            meteors.append([s['x']+25, s['y']+40, math.atan2(vy, vx), 8])
                    if s['burst_count'] >= 3 and s['shoot_timer'] > 60:
                        s['burst_count'] = 0
                        s['shoot_timer'] = 0
                    # Collision
                    shooter_rect = pygame.Rect(s['x'], s['y'], 50, 40)
                    if shooter_rect.colliderect(player1_rect):
                        player1_lives -= 1
                        s['alive'] = False
                        s['respawn_timer'] = 180
                        if player1_lives <= 0:
                            game_over = True
                    elif multiplayer and shooter_rect.colliderect(player2_rect):
                        player2_lives -= 1
                        s['alive'] = False
                        s['respawn_timer'] = 180
                        if player2_lives <= 0:
                            game_over = True

            # Player bullets hit shooter enemies
            for b in player1_bullets[:]:
                hit = False
                for s in shooter_enemies:
                    if s['alive']:
                        shooter_rect = pygame.Rect(s['x'], s['y'], 50, 40)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(shooter_rect):
                            s['alive'] = False
                            s['respawn_timer'] = 180
                            player1_bullets.remove(b)
                            player1_score += 15
                            level3_score += 15
                            hit = True
                            break
                if hit:
                    continue
            if multiplayer:
                for b in player2_bullets[:]:
                    hit = False
                    for s in shooter_enemies:
                        if s['alive']:
                            shooter_rect = pygame.Rect(s['x'], s['y'], 50, 40)
                            bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                            if bullet_rect.colliderect(shooter_rect):
                                s['alive'] = False
                                s['respawn_timer'] = 180
                                player2_bullets.remove(b)
                                player2_score += 15
                                level3_score += 15
                                hit = True
                                break
                    if hit:
                        continue

        # --- Level 4: Bomber Enemy ---
        if not boss3_active and not boss3_defeated and level == 4:
            # Meteors
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

            # Regular enemies
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

            # Zigzag enemies
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

            # Bomber enemy
            if bomber_enemy is None:
                if bomber_respawn_timer == 0:
                    bomber_x = random.randint(0, WIDTH - 50)
                    bomber_y = -50
                    bomber_enemy = [bomber_x, bomber_y, 3]
            else:
                bomber_enemy[1] += bomber_enemy[2]
                if bomber_enemy[1] > HEIGHT:
                    bomber_enemy = None
                    bomber_respawn_timer = 180
                else:
                    WIN.blit(ENEMY_BOMBER_IMG, (bomber_enemy[0], bomber_enemy[1]))
                    # Bomb dropping logic
                    if random.random() < 0.02:
                        bomb_x = bomber_enemy[0] + 17
                        bomb_y = bomber_enemy[1] + 40
                        bomb_vy = 4
                        meteors.append([bomb_x, bomb_y, math.pi/2, bomb_vy])

        # --- Level 4 Boss ("Greg") Logic ---
        if greg_active and not greg_defeated and level == 4:
            WIN.blit(GREG_IMG, (greg_x, greg_y))
            greg_x += greg_vx
            if greg_x <= 0 or greg_x >= WIDTH - 120:
                greg_vx *= -1
            greg_particle_timer += 1
            if greg_particle_timer > 2:
                greg_particle_timer = 0
                greg_particles.append([greg_x + 60, greg_y + 30, random.uniform(-1, 1) * 2, random.uniform(-1, 1) * 2])
            for p in greg_particles[:]:
                p[0] += p[2]
                p[1] += p[3]
                pygame.draw.circle(WIN, (255, 255, 255), (int(p[0]), int(p[1])), 3)
                if p[0] < 0 or p[0] > WIDTH or p[1] < 0 or p[1] > HEIGHT:
                    greg_particles.remove(p)

            # Greg shooting
            if random.random() < 0.05:
                dx = (player1_x + PLAYER_WIDTH // 2) - (greg_x + 60)
                dy = (player1_y + PLAYER_HEIGHT // 2) - (greg_y + 40)
                length = math.hypot(dx, dy)
                if length == 0: length = 1
                vx = dx / length * 4
                vy = dy / length * 4
                meteors.append([greg_x + 60, greg_y + 40, math.atan2(vy, vx), 6])

            for b in meteors[:]:
                if b[0] >= greg_x and b[0] <= greg_x + 120 and b[1] >= greg_y and b[1] <= greg_y + 60:
                    meteors.remove(b)
                    greg_health -= 1
                    player1_score += 10
                    if greg_health <= 0:
                        greg_defeated = True
                        WIN.blit(LEVEL4_BG, (0, 0))
                        win_text = BIG_FONT.render("Greg Defeated!", True, (255, 50, 50))
                        WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                        pygame.display.flip()
                        pygame.time.wait(2500)
                        level = 5
                        continue

        # --- Level 5 Final Boss ("The Overlord") ---
        if overlord_active and not overlord_defeated and level == 5:
            WIN.blit(OVERLORD_IMG, (overlord_x, overlord_y))
            overlord_x += overlord_vx
            if overlord_x <= 0 or overlord_x >= WIDTH - 180:
                overlord_vx *= -1
            overlord_shoot_timer += 1
            if overlord_shoot_timer > 20:
                overlord_shoot_timer = 0
                if random.random() < 0.5:
                    # Single homing bullet
                    dx = (player1_x + PLAYER_WIDTH // 2) - (overlord_x + 90)
                    dy = (player1_y + PLAYER_HEIGHT // 2) - (overlord_y + 50)
                    length = math.hypot(dx, dy)
                    if length == 0: length = 1
                    vx = dx / length * 3
                    vy = dy / length * 3
                    overlord_bullets.append([overlord_x + 90, overlord_y + 50, vx, vy])
                else:
                    # Burst of 3 bullets
                    for angle in [-0.3, 0, 0.3]:
                        vx = 5 * math.sin(angle)
                        vy = 5 * math.cos(angle)
                        overlord_bullets.append([overlord_x + 90, overlord_y + 50, vx, vy])

            for b in overlord_bullets[:]:
                b[0] += b[2]
                b[1] += b[3]
                pygame.draw.rect(WIN, (255, 0, 0), (b[0], b[1], 18, 26))
                if pygame.Rect(b[0], b[1], 18, 26).colliderect(player1_rect):
                    player1_lives -= 1
                    overlord_bullets.remove(b)
                    if player1_lives <= 0:
                        game_over = True
                elif multiplayer and pygame.Rect(b[0], b[1], 18, 26).colliderect(player2_rect):
                    player2_lives -= 1
                    overlord_bullets.remove(b)
                    if player2_lives <= 0:
                        game_over = True
                elif b[1] > HEIGHT or b[0] < 0 or b[0] > WIDTH:
                    overlord_bullets.remove(b)
            # Player bullets hit overlord
            for b in player1_bullets[:]:
                overlord_rect = pygame.Rect(overlord_x, overlord_y, 180, 100)
                bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                if bullet_rect.colliderect(overlord_rect):
                    player1_bullets.remove(b)
                    overlord_health -= 1
                    player1_score += 10
                    break
            if multiplayer:
                for b in player2_bullets[:]:
                    overlord_rect = pygame.Rect(overlord_x, overlord_y, 180, 100)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(overlord_rect):
                        player2_bullets.remove(b)
                        overlord_health -= 1
                        player2_score += 10
                        break
            if overlord_health <= 0:
                WIN.blit(LEVEL5_BG, (0, 0))
                win_text = BIG_FONT.render("You Defeated the Overlord!", True, (255, 50, 50))
                WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
                pygame.display.flip()
                pygame.time.wait(2500)
                overlord_active = False
                overlord_defeated = True
                continue

        # --- Player Bullets ---
        for b in player1_bullets[:]:
            b[1] -= BULLET_SPEED
            if b[1] < 0:
                player1_bullets.remove(b)

        if multiplayer:
            for b in player2_bullets[:]:
                b[1] -= BULLET_SPEED
                if b[1] < 0:
                    player2_bullets.remove(b)

        # --- Draw Players ---
        draw_player(player1_x, player1_y, SHIP_IMG)
        if multiplayer:
            draw_player(player2_x, player2_y, SHIP2_IMG)

        # --- Draw Lives ---
        for i in range(player1_lives):
            pygame.draw.rect(WIN, WHITE, (10 + i * 25, 10, 20, 30))
        if multiplayer:
            for i in range(player2_lives):
                pygame.draw.rect(WIN, WHITE, (WIDTH - 30 - i * 25, 10, 20, 30))

        # --- Draw Scores ---
        score_text = FONT.render(f"Score: {player1_score}", True, WHITE)
        WIN.blit(score_text, (10, 50))
        if multiplayer:
            score_text = FONT.render(f"Score: {player2_score}", True, WHITE)
            WIN.blit(score_text, (WIDTH - 150, 50))

        # --- Game Over ---
        if game_over:
            over_text = BIG_FONT.render("Game Over", True, (255, 0, 0))
            WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
            retry_text = FONT.render("Retry", True, WHITE)
            quit_text = FONT.render("Quit", True, WHITE)
            if draw_button("Retry", WIDTH//2 - 75, HEIGHT//2, 150, 50, pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]):
                return
            if draw_button("Quit", WIDTH//2 - 75, HEIGHT//2 + 60, 150, 50, pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]):
                pygame.quit()
                exit()

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

