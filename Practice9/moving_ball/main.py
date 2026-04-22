

import sys
import math
import pygame

from ball import Ball



WINDOW_W  = 640
WINDOW_H  = 520
FPS       = 60
TITLE     = "Moving Ball Game"


BALL_RADIUS = 25
BALL_STEP   = 20
BALL_COLOR  = (220, 38, 38)


C_BG         = (248, 246, 240)
C_GRID       = (230, 226, 216)
C_PANEL      = (255, 252, 245)
C_BORDER     = (200, 195, 180)
C_ACCENT     = (220, 38,  38)
C_ACCENT2    = (39, 120, 200)
C_TEXT       = (40,  36,  30)
C_MUTED      = (160, 155, 140)
C_BLOCKED_BG = (255, 235, 235)
C_SUCCESS_BG = (235, 255, 240)



def make_grid_surface(w: int, h: int) -> pygame.Surface:
    surf = pygame.Surface((w, h))
    surf.fill(C_BG)
    spacing = 32
    for gx in range(0, w, spacing):
        for gy in range(0, h, spacing):
            pygame.draw.circle(surf, C_GRID, (gx, gy), 1)
    return surf




class FlashEffect:
    def __init__(self) -> None:
        self._timer   = 0
        self._color   = (255, 0, 0)
        self._max     = 12

    def trigger(self, color: tuple[int, int, int]) -> None:
        self._color = color
        self._timer = self._max

    def draw(self, surface: pygame.Surface) -> None:
        if self._timer <= 0:
            return
        alpha = int(60 * self._timer / self._max)
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((*self._color, alpha))
        surface.blit(overlay, (0, 0))
        self._timer -= 1




class HUD:
    def __init__(self, screen_w: int, screen_h: int) -> None:
        self.sw = screen_w
        self.sh = screen_h
        self.move_count   = 0
        self.blocked_count = 0
        self._load_fonts()

    def _load_fonts(self) -> None:
        def sf(name: str, size: int) -> pygame.font.Font:
            return pygame.font.SysFont(name, size) or pygame.font.Font(None, size)
        self.f_mono  = sf("dejavusansmono", 13)
        self.f_label = sf("dejavusans",     12)
        self.f_title = sf("dejavusans",     17)

    def draw(self, surface: pygame.Surface, ball: Ball) -> None:
        self._draw_top_bar(surface, ball)
        self._draw_bottom_bar(surface)
        self._draw_compass(surface, ball)

    def _draw_top_bar(self, surface: pygame.Surface, ball: Ball) -> None:
        bar = pygame.Rect(0, 0, self.sw, 44)
        pygame.draw.rect(surface, C_PANEL, bar)
        pygame.draw.line(surface, C_BORDER, (0, 43), (self.sw, 43))

        # Title
        title = self.f_title.render("●  Moving Ball", True, C_ACCENT)
        surface.blit(title, (16, 12))

        # Position readout
        pos_str = f"x: {ball.x:4d}   y: {ball.y:4d}"
        pos_s   = self.f_mono.render(pos_str, True, C_TEXT)
        surface.blit(pos_s, (self.sw // 2 - pos_s.get_width() // 2, 14))

        # Move counter
        stats = f"moves: {self.move_count}   blocked: {self.blocked_count}"
        st_s  = self.f_mono.render(stats, True, C_MUTED)
        surface.blit(st_s, (self.sw - st_s.get_width() - 16, 14))

    def _draw_bottom_bar(self, surface: pygame.Surface) -> None:
        bh   = 36
        bar  = pygame.Rect(0, self.sh - bh, self.sw, bh)
        pygame.draw.rect(surface, C_PANEL, bar)
        pygame.draw.line(surface, C_BORDER, (0, self.sh - bh), (self.sw, self.sh - bh))

        controls = [
            ("↑ ↓ ← →", "Move"),
            ("R", "Reset"),
            ("Q / Esc", "Quit"),
        ]
        x = 20
        for key, action in controls:
            k_s = self.f_mono.render(key, True, C_ACCENT2)
            a_s = self.f_label.render(f"  {action}", True, C_MUTED)
            surface.blit(k_s, (x, self.sh - bh + 10))
            x += k_s.get_width()
            surface.blit(a_s, (x, self.sh - bh + 11))
            x += a_s.get_width() + 28

    def _draw_compass(self, surface: pygame.Surface, ball: Ball) -> None:

        cx, cy = self.sw - 52, self.sh - 68
        r      = 22
        dirs   = {
            "U": (0,   -1,  ball.y - ball.radius - ball.step >= 0),
            "D": (0,    1,  ball.y + ball.radius + ball.step <= ball.screen_height),
            "L": (-1,   0,  ball.x - ball.radius - ball.step >= 0),
            "R": ( 1,   0,  ball.x + ball.radius + ball.step <= ball.screen_width),
        }

        pygame.draw.circle(surface, C_PANEL,  (cx, cy), r + 4)
        pygame.draw.circle(surface, C_BORDER, (cx, cy), r + 4, 1)

        arrow_pts = {
            "U": [(cx, cy-r+4), (cx-6, cy-r+14), (cx+6, cy-r+14)],
            "D": [(cx, cy+r-4), (cx-6, cy+r-14), (cx+6, cy+r-14)],
            "L": [(cx-r+4, cy), (cx-r+14, cy-6), (cx-r+14, cy+6)],
            "R": [(cx+r-4, cy), (cx+r-14, cy-6), (cx+r-14, cy+6)],
        }
        for d, (_, __, available) in dirs.items():
            color = C_ACCENT2 if available else C_BORDER
            pygame.draw.polygon(surface, color, arrow_pts[d])




class App:
    TOP_BAR    = 44
    BOTTOM_BAR = 36

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()


        self.grid_surf = make_grid_surface(WINDOW_W, WINDOW_H)


        play_cx = WINDOW_W  // 2
        play_cy = self.TOP_BAR + (WINDOW_H - self.TOP_BAR - self.BOTTOM_BAR) // 2

        self.ball = Ball(
            screen_width  = WINDOW_W,
            screen_height = WINDOW_H - self.TOP_BAR - self.BOTTOM_BAR,
            x             = play_cx,
            y             = play_cy - self.TOP_BAR,
            radius        = BALL_RADIUS,
            color         = BALL_COLOR,
            step          = BALL_STEP,
        )

        self.hud   = HUD(WINDOW_W, WINDOW_H)
        self.flash = FlashEffect()



    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False
                if event.key == pygame.K_r:
                    self.ball.reset()
                    self.hud.move_count    = 0
                    self.hud.blocked_count = 0
                self._handle_arrow(event.key)
        return True

    def _handle_arrow(self, key: int) -> None:
        ARROW_MAP = {
            pygame.K_UP:    ( 0, -self.ball.step),
            pygame.K_DOWN:  ( 0,  self.ball.step),
            pygame.K_LEFT:  (-self.ball.step, 0),
            pygame.K_RIGHT: ( self.ball.step, 0),
        }
        if key not in ARROW_MAP:
            return

        dx, dy = ARROW_MAP[key]
        moved  = self.ball.move(dx, dy)

        if moved:
            self.hud.move_count += 1
            self.flash.trigger((39, 120, 200))    # brief blue tint: success
        else:
            self.hud.blocked_count += 1
            self.flash.trigger((220, 38, 38))     # brief red tint: blocked



    def draw(self) -> None:

        self.screen.blit(self.grid_surf, (0, 0))


        play_rect = pygame.Rect(
            0,
            self.TOP_BAR,
            WINDOW_W,
            WINDOW_H - self.TOP_BAR - self.BOTTOM_BAR,
        )
        pygame.draw.rect(self.screen, C_BG, play_rect)

        for gx in range(0, WINDOW_W, 32):
            for gy in range(self.TOP_BAR, WINDOW_H - self.BOTTOM_BAR, 32):
                pygame.draw.circle(self.screen, C_GRID, (gx, gy), 1)

        pygame.draw.rect(self.screen, C_BORDER, play_rect, 1)


        play_surf = self.screen.subsurface(play_rect)
        self.ball.draw(play_surf)


        self.flash.draw(self.screen)

        self.hud.draw(self.screen, self.ball)



    def run(self) -> None:
        print(f"\n  {TITLE}")
        print("  ─────────────────────")
        print("  Arrow keys  Move ball 20 px")
        print("  R           Reset to centre")
        print("  Q / Esc     Quit\n")

        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit(0)




if __name__ == "__main__":
    App().run()
