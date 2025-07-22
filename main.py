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

def draw_player(x, y):
    WIN.blit(SHIP_IMG, (x, y))

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

def game_loop():
    score = 0
    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - PLAYER_HEIGHT - 20
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    bullets = []
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
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:
            player_x += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            if len(bullets) == 0 or bullets[-1][1] < player_y - 20:
                bullets.append([player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player_y])

        player_rect.x = player_x

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
            if meteor_rect.colliderect(player_rect):
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
            if enemy_rect.colliderect(player_rect):
                game_over = True
            if e[1] > HEIGHT:
                enemies.remove(e)

        # Bullets shoot up
        for b in bullets[:]:
            b[1] -= BULLET_SPEED
            draw_bullet(b[0], b[1])
            if b[1] < -BULLET_HEIGHT:
                bullets.remove(b)
            else:
                for e in enemies[:]:
                    enemy_rect = pygame.Rect(e[0], e[1], ENEMY_WIDTH, ENEMY_HEIGHT)
                    bullet_rect = pygame.Rect(b[0], b[1], BULLET_WIDTH, BULLET_HEIGHT)
                    if bullet_rect.colliderect(enemy_rect):
                        enemies.remove(e)
                        if b in bullets:
                            bullets.remove(b)
                        score += 5

        draw_player(player_x, player_y)
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
        result = game_loop()
        if result == "quit":
            break

if __name__ == "__main__":
    main()

