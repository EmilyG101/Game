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
BG_IMG = pygame.image.load(os.path.join(ASSET_DIR, "space_bg.png"))
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

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
    score = 0
    # Player 1
    player1_x = WIDTH // 3 - PLAYER_WIDTH // 2 if multiplayer else WIDTH // 2 - PLAYER_WIDTH // 2
    player1_y = HEIGHT - PLAYER_HEIGHT - 20
    player1_rect = pygame.Rect(player1_x, player1_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_bullets = []
    # Player 2 (if multiplayer)
    if multiplayer:
        player2_x = WIDTH * 2 // 3 - PLAYER_WIDTH // 2
        player2_y = HEIGHT - PLAYER_HEIGHT - 20
        player2_rect = pygame.Rect(player2_x, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        player2_bullets = []
    meteors = []
    enemies = []
    meteor_timer = 0
    enemy_timer = 0
    run = True
    game_over = False

    while run:
        clock.tick(60)
        WIN.blit(BG_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        # Player 1 controls
        if keys[pygame.K_LEFT] and player1_x > 0:
            player1_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player1_x < WIDTH - PLAYER_WIDTH:
            player1_x += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            if len(player1_bullets) == 0 or player1_bullets[-1][1] < player1_y - 20:
                player1_bullets.append([player1_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player1_y])
        player1_rect.x = player1_x

        # Player 2 controls (if multiplayer)
        if multiplayer:
            if keys[pygame.K_a] and player2_x > 0:
                player2_x -= PLAYER_SPEED
            if keys[pygame.K_d] and player2_x < WIDTH - PLAYER_WIDTH:
                player2_x += PLAYER_SPEED
            if keys[pygame.K_LSHIFT]:
                if len(player2_bullets) == 0 or player2_bullets[-1][1] < player2_y - 20:
                    player2_bullets.append([player2_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player2_y])
            player2_rect.x = player2_x

        # Meteors from top, angled down
        meteor_timer += 1
        if meteor_timer > 30:
            meteor_timer = 0
            mx = random.randint(0, WIDTH - METEOR_WIDTH)
            angle = random.uniform(math.radians(75), math.radians(105))  # Downward angle with spread
            speed = random.uniform(METEOR_SPEED_MIN, METEOR_SPEED_MAX)
            meteors.append([mx, -METEOR_HEIGHT, angle, speed])

        for m in meteors[:]:
            m[0] += m[3] * math.cos(m[2])
            m[1] += m[3] * math.sin(m[2])
            meteor_rect = pygame.Rect(m[0] - METEOR_WIDTH//2, m[1] - METEOR_HEIGHT//2, METEOR_WIDTH, METEOR_HEIGHT)
            draw_meteor(m[0], m[1], m[2])
            if meteor_rect.colliderect(player1_rect) or (multiplayer and meteor_rect.colliderect(player2_rect)):
                game_over = True
            if m[1] > HEIGHT:
                meteors.remove(m)
                score += 1

        # Enemies from top, straight down
        enemy_timer += 1
        if enemy_timer > 90:
            enemy_timer = 0
            ex = random.randint(0, WIDTH - ENEMY_WIDTH)
            enemies.append([ex, -ENEMY_HEIGHT])

        for e in enemies[:]:
            e[1] += ENEMY_SPEED
            enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
            draw_enemy(e[0], e[1])
            if enemy_rect.colliderect(player1_rect) or (multiplayer and enemy_rect.colliderect(player2_rect)):
                game_over = True
            if e[1] > HEIGHT:
                enemies.remove(e)

        # Player 1 bullets
        for b in player1_bullets[:]:
            b[1] -= BULLET_SPEED
            draw_bullet(b[0], b[1])
            if b[1] < -BULLET_HEIGHT:
                player1_bullets.remove(b)
            else:
                for e in enemies[:]:
                    enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(enemy_rect):
                        enemies.remove(e)
                        if b in player1_bullets:
                            player1_bullets.remove(b)
                        score += 5

        # Player 2 bullets (if multiplayer)
        if multiplayer:
            for b in player2_bullets[:]:
                b[1] -= BULLET_SPEED
                draw_bullet(b[0], b[1])
                if b[1] < -BULLET_HEIGHT:
                    player2_bullets.remove(b)
                else:
                    for e in enemies[:]:
                        enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                        bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                        if bullet_rect.colliderect(enemy_rect):
                            enemies.remove(e)
                            if b in player2_bullets:
                                player2_bullets.remove(b)
                            score += 5

        # Draw players
        draw_player(player1_x, player1_y, SHIP_IMG)
        if multiplayer:
            draw_player(player2_x, player2_y, SHIP2_IMG)

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

        if game_over:
            WIN.blit(BG_IMG, (0, 0))
            over_text = BIG_FONT.render("Game Over!", True, WHITE)
            score_text = FONT.render(f"Final Score: {score}", True, WHITE)
            WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
            WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]
            if draw_button("Restart", WIDTH//2 - 75, HEIGHT//2 + 60, 150, 50, mouse_pos, mouse_click):
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
        multiplayer = mode_menu()
        result = game_loop(multiplayer)
        if result == "quit":
            break

if __name__ == "__main__":
    main()

