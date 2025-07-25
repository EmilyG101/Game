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
BG_IMG = pygame.image.load(os.path.join(ASSET_DIR, "space_bg.png"))
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))
BOSSSHIP_IMG = pygame.image.load(os.path.join(ASSET_DIR, "bossship1.png"))
BOSSSHIP_IMG = pygame.transform.scale(BOSSSHIP_IMG, (50, 40))

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

    # Boss variables
    boss_active = False
    boss_intro = False
    boss_intro_timer = 0
    boss_name = "The Crimson Triad"
    boss_health = 60  # Hidden from player
    boss_x = WIDTH // 2
    boss_y = -100
    boss_speed = 2
    boss_bullets = []
    boss_fire_timer = 0
    boss_burst_count = 0
    boss_burst_pause = 0
    boss_defeated = False

    while run:
        clock.tick(60)
        WIN.blit(BG_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # --- Boss Trigger ---
        if not boss_active and not boss_defeated:
            if (not multiplayer and player1_score >= 50) or (multiplayer and player1_score + player2_score >= 50):
                boss_active = True
                boss_intro = True
                boss_intro_timer = 120  # 2 seconds for dramatic entrance

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

        # --- Boss Logic ---
        if boss_active:
            # Dramatic entrance
            if boss_intro:
                boss_y += boss_speed
                if boss_y >= 80:
                    boss_y = 80
                    boss_intro_timer -= 1
                    # Show boss name
                    name_text = BIG_FONT.render(boss_name, True, (255, 50, 50))
                    WIN.blit(name_text, (WIDTH//2 - name_text.get_width()//2, boss_y - 60))
                    if boss_intro_timer <= 0:
                        boss_intro = False
                else:
                    # Show boss name while entering
                    name_text = BIG_FONT.render(boss_name, True, (255, 50, 50))
                    WIN.blit(name_text, (WIDTH//2 - name_text.get_width()//2, boss_y - 60))
            else:
                # Draw boss formation (3 bossship1.png in a line)
                for i in range(-1, 2):
                    WIN.blit(BOSSSHIP_IMG, (boss_x + i*60 - BOSSSHIP_IMG.get_width()//2, boss_y))
                # Boss fires in bursts: 3 volleys, then pause
                if boss_burst_pause > 0:
                    boss_burst_pause -= 1
                else:
                    boss_fire_timer += 1
                    if boss_fire_timer > 15:  # frames between shots in a burst
                        boss_fire_timer = 0
                        boss_burst_count += 1
                        for i in range(-1, 2):
                            boss_bullets.append([boss_x + i*60, boss_y + BOSSSHIP_IMG.get_height(), 7])
                        if boss_burst_count >= 3:  # 3 volleys per burst
                            boss_burst_pause = 60  # Pause for 1 second (60 frames)
                            boss_burst_count = 0
                # Move boss left/right slowly
                boss_x += random.choice([-1, 0, 1]) * 2
                boss_x = max(90, min(WIDTH-90, boss_x))
                # Boss bullets movement and collision
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
                # Player bullets hit boss
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
                # Boss defeated
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
                    continue

        # --- Level 2: Zigzag Enemies ---
        if boss_defeated and level == 2:
            zigzag_spawn_timer += 1
            if zigzag_spawn_timer > 60:  # spawn every second
                zigzag_spawn_timer = 0
                # Randomly choose left or right entry
                from_left = random.choice([True, False])
                if from_left:
                    x = 0
                    vx = 5
                else:
                    x = WIDTH - 50
                    vx = -5
                y = random.randint(50, HEIGHT // 2)
                vy = random.choice([3, 4])
                zigzag_enemies.append([x, y, vx, vy])

            for z in zigzag_enemies[:]:
                # Move
                z[0] += z[2]
                z[1] += z[3]
                # Bounce off left/right
                if z[0] <= 0 or z[0] >= WIDTH - 50:
                    z[2] *= -1
                # Remove if off bottom
                if z[1] > HEIGHT:
                    zigzag_enemies.remove(z)
                    continue
                # Draw
                WIN.blit(ENEMY_ZIGZAG_IMG, (z[0], z[1]))
                # Collisions with players
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

            # Player 1 bullets hit zigzag enemies
            for b in player1_bullets[:]:
                hit = False
                for z in zigzag_enemies[:]:
                    zigzag_rect = pygame.Rect(z[0], z[1], 50, 40)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(zigzag_rect):
                        zigzag_enemies.remove(z)
                        player1_bullets.remove(b)
                        player1_score += 15  # More points than normal enemy
                        hit = True
                        break
                if hit:
                    continue

            # Player 2 bullets hit zigzag enemies
            if multiplayer:
                for b in player2_bullets[:]:
                    hit = False
                    for z in zigzag_enemies[:]:
                        zigzag_rect = pygame.Rect(z[0], z[1], 50, 40)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(zigzag_rect):
                            zigzag_enemies.remove(z)
                            player2_bullets.remove(b)
                            player2_score += 15
                            hit = True
                            break
                    if hit:
                        continue

        # --- Player Bullets ---
        # --- Player 1 bullets ---
        for b in player1_bullets[:]:
            b[1] -= BULLET_SPEED
            draw_bullet(b[0], b[1])
            if b[1] < -BULLET_HEIGHT:
                player1_bullets.remove(b)
            else:
                hit = False
                for e in enemies[:]:
                    enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(enemy_rect):
                        enemies.remove(e)
                        player1_bullets.remove(b)
                        player1_score += 5
                        hit = True
                        break
                if hit:
                    continue

        # --- Player 2 bullets (if multiplayer) ---
        if multiplayer:
            for b in player2_bullets[:]:
                b[1] -= BULLET_SPEED
                draw_bullet(b[0], b[1])
                if b[1] < -BULLET_HEIGHT:
                    player2_bullets.remove(b)
                else:
                    hit = False
                    for e in enemies[:]:
                        enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(enemy_rect):
                            enemies.remove(e)
                            player2_bullets.remove(b)
                            player2_score += 5
                            hit = True
                            break
                    if hit:
                        continue

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
        # Add a short delay and clear events before showing mode menu
        pygame.time.wait(200)
        pygame.event.clear()
        multiplayer = mode_menu()
        result = game_loop(multiplayer)
        if result == "quit":
            break

if __name__ == "__main__":
    main()

