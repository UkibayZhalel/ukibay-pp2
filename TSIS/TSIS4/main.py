import pygame
import random
import json
import os
import db

# --- Constants & Config ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS_BASE = 10


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake TSIS 4")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 24)
        self.big_font = pygame.font.SysFont("Verdana", 50)

        db.init_db()
        self.load_settings()
        self.state = "MENU"
        self.username = ""
        self.reset_game_data()

    def load_settings(self):
        # Define default settings
        defaults = {"color": [0, 255, 0], "grid": True, "sound": True}

        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    loaded = json.load(f)
                    # Merge loaded settings with defaults to ensure no missing keys
                    self.settings = {**defaults, **loaded}
            except:
                self.settings = defaults
        else:
            self.settings = defaults

        self.save_settings()

    def save_settings(self):
        with open("settings.json", "w") as f: json.dump(self.settings, f)

    def reset_game_data(self):
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.shield_active = False
        self.powerup = None  # {pos, type, timer}
        self.active_effect = {"type": None, "end_ticks": 0}
        self.spawn_food()
        self.spawn_poison()

    def spawn_food(self):
        while True:
            self.food = [random.randrange(1, WIDTH // GRID_SIZE) * GRID_SIZE,
                         random.randrange(1, HEIGHT // GRID_SIZE) * GRID_SIZE]
            if self.food not in self.snake and self.food not in self.obstacles: break

    def spawn_poison(self):
        while True:
            self.poison = [random.randrange(1, WIDTH // GRID_SIZE) * GRID_SIZE,
                           random.randrange(1, HEIGHT // GRID_SIZE) * GRID_SIZE]
            if self.poison not in self.snake and self.poison not in self.obstacles: break

    def spawn_powerup(self):
        p_type = random.choice(["SPEED", "SLOW", "SHIELD"])
        while True:
            pos = [random.randrange(1, WIDTH // GRID_SIZE) * GRID_SIZE,
                   random.randrange(1, HEIGHT // GRID_SIZE) * GRID_SIZE]
            if pos not in self.snake and pos not in self.obstacles:
                self.powerup = {"pos": pos, "type": p_type, "expiry": pygame.time.get_ticks() + 8000}
                break

    def create_obstacles(self):
        self.obstacles = []
        for _ in range(self.level * 2):
            obs = [random.randrange(1, WIDTH // GRID_SIZE) * GRID_SIZE,
                   random.randrange(1, HEIGHT // GRID_SIZE) * GRID_SIZE]
            if obs not in self.snake: self.obstacles.append(obs)

    def draw_text(self, text, font, color, x, y, center=True):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
        self.screen.blit(img, rect)

    # --- Screens ---
    def menu_screen(self):
        self.screen.fill((20, 20, 20))
        self.draw_text("SNAKE ADVENTURE", self.big_font, (0, 255, 0), WIDTH // 2, 100)
        self.draw_text(f"Username: {self.username}|", self.font, (255, 255, 255), WIDTH // 2, 250)
        self.draw_text("[ENTER] Play  [L] Leaderboard  [S] Settings", self.font, (200, 200, 200), WIDTH // 2, 400)

    def leaderboard_screen(self):
        self.screen.fill((10, 10, 30))
        self.draw_text("TOP 10 SCORES", self.font, (255, 255, 0), WIDTH // 2, 50)
        scores = db.get_top_scores()
        for i, (name, sc, lvl, date) in enumerate(scores):
            self.draw_text(f"{i + 1}. {name} - {sc} pts (Lvl {lvl})", self.font, (255, 255, 255), WIDTH // 2,
                           100 + i * 40)
        self.draw_text("Press [ESC] to Back", self.font, (150, 150, 150), WIDTH // 2, 550)

    def settings_screen(self):
        self.screen.fill((30, 10, 10))
        self.draw_text("SETTINGS", self.font, (255, 255, 255), WIDTH // 2, 100)
        grid_txt = "ON" if self.settings['grid'] else "OFF"
        self.draw_text(f"[G] Grid Overlay: {grid_txt}", self.font, (0, 255, 255), WIDTH // 2, 200)
        self.draw_text(f"[C] Change Snake Color (Current: {self.settings['color']})", self.font, (0, 255, 255),
                       WIDTH // 2, 260)
        self.draw_text("Press [B] to Save and Back", self.font, (0, 255, 0), WIDTH // 2, 400)

    def game_over_screen(self):
        self.screen.fill((50, 0, 0))
        self.draw_text("GAME OVER", self.big_font, (255, 255, 255), WIDTH // 2, 150)
        self.draw_text(f"Score: {self.score} | Level: {self.level}", self.font, (255, 255, 0), WIDTH // 2, 250)
        self.draw_text("Press [SPACE] to Retry or [M] for Menu", self.font, (255, 255, 255), WIDTH // 2, 350)

    # --- Main Loop ---
    def run(self):
        running = True
        personal_best = 0
        while running:
            # Handle Timing for Powerups
            now = pygame.time.get_ticks()
            if self.state == "GAME":
                if not self.powerup and random.random() < 0.005: self.spawn_powerup()
                if self.powerup and now > self.powerup['expiry']: self.powerup = None
                if self.active_effect['type'] and now > self.active_effect['end_ticks']:
                    self.active_effect = {"type": None, "end_ticks": 0}

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False

                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key == pygame.K_RETURN and self.username:
                            personal_best = db.get_user_best(self.username)
                            self.reset_game_data()
                            self.state = "GAME"
                        elif event.key == pygame.K_l:
                            self.state = "LEADERBOARD"
                        elif event.key == pygame.K_s:
                            self.state = "SETTINGS"
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += event.unicode

                    elif self.state == "GAME":
                        if event.key == pygame.K_UP and self.direction != "DOWN": self.direction = "UP"
                        if event.key == pygame.K_DOWN and self.direction != "UP": self.direction = "DOWN"
                        if event.key == pygame.K_LEFT and self.direction != "RIGHT": self.direction = "LEFT"
                        if event.key == pygame.K_RIGHT and self.direction != "LEFT": self.direction = "RIGHT"

                    elif self.state == "LEADERBOARD":
                        if event.key == pygame.K_ESCAPE: self.state = "MENU"

                    elif self.state == "SETTINGS":
                        if event.key == pygame.K_g: self.settings['grid'] = not self.settings['grid']
                        if event.key == pygame.K_c: self.settings['color'] = [random.randint(0, 255) for _ in range(3)]
                        if event.key == pygame.K_b: self.save_settings(); self.state = "MENU"

                    elif self.state == "GAMEOVER":
                        if event.key == pygame.K_SPACE: self.reset_game_data(); self.state = "GAME"
                        if event.key == pygame.K_m: self.state = "MENU"

            # Logic Update (Game Only)
            if self.state == "GAME":
                head = list(self.snake[0])
                if self.direction == "UP":
                    head[1] -= GRID_SIZE
                elif self.direction == "DOWN":
                    head[1] += GRID_SIZE
                elif self.direction == "LEFT":
                    head[0] -= GRID_SIZE
                elif self.direction == "RIGHT":
                    head[0] += GRID_SIZE

                # Collision Check
                wall_hit = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
                self_hit = head in self.snake
                obs_hit = head in self.obstacles

                if wall_hit or self_hit or obs_hit:
                    if self.shield_active:
                        self.shield_active = False
                    else:
                        db.save_score(self.username, self.score, self.level)
                        self.state = "GAMEOVER"
                        continue

                self.snake.insert(0, head)

                # Eat Food
                if head == self.food:
                    self.score += 10
                    if self.score % 50 == 0:
                        self.level += 1
                        if self.level >= 3: self.create_obstacles()
                    self.spawn_food()
                # Eat Poison
                elif head == self.poison:
                    self.snake.pop();
                    self.snake.pop()  # Shorten by 2 segments
                    if len(self.snake) <= 1:
                        db.save_score(self.username, self.score, self.level)
                        self.state = "GAMEOVER"
                    self.spawn_poison()
                # Powerup
                elif self.powerup and head == self.powerup['pos']:
                    p_type = self.powerup['type']
                    if p_type == "SHIELD":
                        self.shield_active = True
                    else:
                        self.active_effect = {"type": p_type, "end_ticks": now + 5000}
                    self.powerup = None
                else:
                    self.snake.pop()

            # Drawing
            if self.state == "MENU":
                self.menu_screen()
            elif self.state == "LEADERBOARD":
                self.leaderboard_screen()
            elif self.state == "SETTINGS":
                self.settings_screen()
            elif self.state == "GAMEOVER":
                self.game_over_screen()
            elif self.state == "GAME":
                self.screen.fill((0, 0, 0))
                if self.settings['grid']:
                    for x in range(0, WIDTH, GRID_SIZE): pygame.draw.line(self.screen, (30, 30, 30), (x, 0),
                                                                          (x, HEIGHT))
                    for y in range(0, HEIGHT, GRID_SIZE): pygame.draw.line(self.screen, (30, 30, 30), (0, y),
                                                                           (WIDTH, y))

                # Draw Objects
                pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, GRID_SIZE, GRID_SIZE))  # Food
                pygame.draw.circle(self.screen, (100, 0, 0), (self.poison[0] + 10, self.poison[1] + 10), 8)  # Poison
                for obs in self.obstacles: pygame.draw.rect(self.screen, (100, 100, 100),
                                                            (*obs, GRID_SIZE, GRID_SIZE))  # Walls

                if self.powerup:  # Powerup icon
                    c = (255, 255, 0) if self.powerup['type'] == "SPEED" else (0, 0, 255)
                    pygame.draw.rect(self.screen, c, (*self.powerup['pos'], GRID_SIZE, GRID_SIZE))

                # Draw Snake
                for i, pos in enumerate(self.snake):
                    color = self.settings['color'] if i > 0 else (255, 255, 255)
                    if self.shield_active: color = (180, 0, 255)
                    pygame.draw.rect(self.screen, color, (*pos, GRID_SIZE, GRID_SIZE))

                # HUD
                self.draw_text(f"Score: {self.score}  Lvl: {self.level}  Best: {personal_best}", self.font,
                               (255, 255, 255), 10, 10, False)

            pygame.display.update()

            # Tick logic (Variable speed)
            current_fps = FPS_BASE + (self.level * 2)
            if self.active_effect['type'] == "SPEED":
                current_fps += 10
            elif self.active_effect['type'] == "SLOW":
                current_fps = max(5, current_fps - 7)
            self.clock.tick(current_fps)

        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()