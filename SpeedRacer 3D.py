import pygame
import random
import sys
import os

# ---------------- Initialisation ---------------- #
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpeedRacer 3D Pro")
clock = pygame.time.Clock()

# ---------------- Couleurs ---------------- #
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (30, 30, 30)

# ---------------- Polices ---------------- #
font_title = pygame.font.SysFont("Arial", 50)
font_text = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 20)

# ---------------- Variables globales ---------------- #
player_width, player_height = 60, 120
player_speed = 10
player_x = WIDTH//2 - player_width//2
player_y = HEIGHT - player_height - 10
obstacle_width, obstacle_height = 60, 120
score = 0
level = "Normal"
obstacles = []

# ---------------- Sons ---------------- #
try:
    pygame.mixer.music.load("./Musique/music.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Musique menu non trouvée.")

explosion_sound = None
try:
    explosion_sound = pygame.mixer.Sound("./Musique/explosion.wav.mp3")
except:
    print("Effet explosion non trouvé.")

# ---------------- Explosion frames ---------------- #
explosion_frames = []
explosion_folder = "explosion_frames"
if os.path.exists(explosion_folder):
    for i in range(1, 9):
        path = os.path.join(explosion_folder, f"explosion{i}.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            explosion_frames.append(pygame.transform.scale(img, (100, 100)))

# ---------------- Fonctions utilitaires ---------------- #
def draw_text(text, font, color, surface, x, y):
    surface.blit(font.render(text, True, color), (x, y))

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(surface, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, self.rect)
        draw_text(self.text, font_text, WHITE, surface, self.rect.x+10, self.rect.y+10)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ---------------- Dessin de la route ---------------- #
def draw_road(offset):
    # Fond route
    pygame.draw.rect(screen, DARK_GRAY, (200, 0, 400, HEIGHT))
    # Bordures
    pygame.draw.rect(screen, GREEN, (180, 0, 20, HEIGHT))
    pygame.draw.rect(screen, GREEN, (600, 0, 20, HEIGHT))
    # Ligne centrale blanche en pointillés
    for i in range(-50, HEIGHT, 50):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i + offset, 10, 30))

# ---------------- Menu Principal ---------------- #
def main_menu():
    global level
    level_btn = Button(300, 300, 200, 50, "Voir les niveaux", GREEN, ORANGE)
    quit_btn = Button(300, 400, 200, 50, "Quitter", RED, ORANGE)

    # Rejouer musique menu
    try:
        pygame.mixer.music.play(-1)
    except:
        pass

    running = True
    offset = 0
    while running:
        screen.fill(GRAY)
        offset = (offset + 5) % 50  # Pour animer la route
        draw_road(offset)

        draw_text("SpeedRacer 3D Pro & Ludo", font_title, WHITE, screen, WIDTH//2 - 180, 50)
        draw_text("Instructions: ← / → pour bouger", font_text, WHITE, screen, 50, 150)
        draw_text("Évitez les obstacles rouges", font_text, WHITE, screen, 50, 190)

        level_btn.draw(screen)
        quit_btn.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if level_btn.is_clicked(event):
                pygame.mixer.music.stop()
                levels_menu()
                return
            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

# ---------------- Menu Niveaux ---------------- #
def levels_menu():
    global level
    easy_btn = Button(150, 300, 150, 50, "Facile", GREEN, ORANGE)
    normal_btn = Button(325, 300, 150, 50, "Normal", ORANGE, RED)
    hard_btn = Button(500, 300, 150, 50, "Difficile", RED, ORANGE)

    running = True
    offset = 0
    while running:
        screen.fill(GRAY)
        offset = (offset + 5) % 50
        draw_road(offset)

        draw_text("Choisissez le niveau", font_title, WHITE, screen, WIDTH//2 - 200, 150)
        easy_btn.draw(screen)
        normal_btn.draw(screen)
        hard_btn.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if easy_btn.is_clicked(event):
                level = "Facile"
                start_game()
                return
            if normal_btn.is_clicked(event):
                level = "Normal"
                start_game()
                return
            if hard_btn.is_clicked(event):
                level = "Difficile"
                start_game()
                return

# ---------------- Jeu ---------------- #
def start_game():
    global player_x, obstacles, score
    obstacles = []
    score = 0
    player_x = WIDTH//2 - player_width//2
    obstacle_speed_level = {"Facile":6, "Normal":10, "Difficile":15}[level]
    explosions = []

    run = True
    offset = 0
    while run:
        screen.fill(GRAY)
        offset = (offset + 15) % 50
        draw_road(offset)

        # Obstacles
        if random.randint(0, 50) == 0:
            obs_x = random.choice([210, 330, 450, 570])
            obstacles.append(pygame.Rect(obs_x, -obstacle_height, obstacle_width, obstacle_height))

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mouvement joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_speed > 200:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed + player_width < 600:
            player_x += player_speed

        # Dessin joueur
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, BLUE, player_rect)

        # Dessin obstacles
        for obs in obstacles[:]:
            obs.y += obstacle_speed_level
            pygame.draw.rect(screen, RED, obs)
            if obs.y > HEIGHT:
                obstacles.remove(obs)
                score += 1
            if player_rect.colliderect(obs):
                if explosion_sound:
                    explosion_sound.play()
                explosions.append({"x":player_rect.centerx, "y":player_rect.centery, "frame":0})
                run = False

        # Explosion animation
        for e in explosions[:]:
            if e["frame"] < len(explosion_frames):
                frame_img = explosion_frames[e["frame"]]
                screen.blit(frame_img, (e["x"]-50, e["y"]-50))
                e["frame"] += 1
            else:
                explosions.remove(e)

        draw_text(f"Score: {score}", font_text, WHITE, screen, 10, 10)
        pygame.display.update()
        clock.tick(60)

    game_over()

# ---------------- Game Over ---------------- #
def game_over():
    replay_btn = Button(300, 300, 200, 50, "Reprendre", GREEN, ORANGE)
    menu_btn = Button(300, 370, 200, 50, "Menu Principal", BLUE, ORANGE)
    quit_btn = Button(300, 440, 200, 50, "Quitter", RED, ORANGE)

    running = True
    offset = 0
    while running:
        screen.fill(GRAY)
        offset = (offset + 15) % 50
        draw_road(offset)

        draw_text("Game Over!", font_title, RED, screen, WIDTH//2 - 120, HEIGHT//3)
        draw_text(f"Score Final: {score}", font_text, WHITE, screen, WIDTH//3, HEIGHT//2)

        replay_btn.draw(screen)
        menu_btn.draw(screen)
        quit_btn.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if replay_btn.is_clicked(event):
                start_game()
                return
            if menu_btn.is_clicked(event):
                main_menu()
                return
            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

# ---------------- Lancer le jeu ---------------- #
main_menu()
