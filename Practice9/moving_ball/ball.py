"""
ball.py — Ball entity with movement and boundary logic.

The Ball holds its own position, radius, and colour.
It exposes a single move(dx, dy) method that:
  - Computes the candidate new position
  - Rejects the move entirely if it would place any part of the ball
    outside the screen rectangle (requirement: ignore off-screen input)
  - Commits the move otherwise
"""

import pygame


class Ball:
    """
    A circle that can be moved with arrow keys on a bounded surface.

    Attributes
    ----------
    x, y      : int  — centre position (pixels)
    radius    : int  — circle radius (default 25 → 50 px diameter)
    color     : tuple[int, int, int]  — RGB fill colour
    step      : int  — pixels moved per key press (default 20)
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        x: int | None = None,
        y: int | None = None,
        radius: int = 25,
        color: tuple[int, int, int] = (220, 38, 38),   # vivid red
        step: int = 20,
    ) -> None:
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.radius = radius
        self.color  = color
        self.step   = step

        # Default: start at the centre of the screen
        self.x = x if x is not None else screen_width  // 2
        self.y = y if y is not None else screen_height // 2

        # Track the last move result for the UI to react to
        self.last_move_blocked = False

        # History of positions for a short ghost trail
        self._trail: list[tuple[int, int]] = []
        self._trail_length = 6

    # ------------------------------------------------------------------ #
    #  Movement                                                             #
    # ------------------------------------------------------------------ #

    def move(self, dx: int, dy: int) -> bool:
        """
        Attempt to move the ball by (dx, dy) pixels.

        Returns
        -------
        True  if the move was accepted and applied.
        False if the move was blocked (ball would leave screen bounds).
        """
        candidate_x = self.x + dx
        candidate_y = self.y + dy

        if self._within_bounds(candidate_x, candidate_y):
            # Commit: push current position onto the trail first
            self._trail.append((self.x, self.y))
            if len(self._trail) > self._trail_length:
                self._trail.pop(0)

            self.x = candidate_x
            self.y = candidate_y
            self.last_move_blocked = False
            return True
        else:
            self.last_move_blocked = True
            return False

    def _within_bounds(self, cx: int, cy: int) -> bool:
        """Return True when a circle centred at (cx, cy) fits entirely on screen."""
        return (
            cx - self.radius >= 0
            and cx + self.radius <= self.screen_width
            and cy - self.radius >= 0
            and cy + self.radius <= self.screen_height
        )

    # ------------------------------------------------------------------ #
    #  Rendering                                                            #
    # ------------------------------------------------------------------ #

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the trail, shadow, and ball onto *surface*."""
        # Ghost trail (fading circles)
        for i, (tx, ty) in enumerate(self._trail):
            alpha = int(40 * (i + 1) / self._trail_length)
            r     = max(3, self.radius - (self._trail_length - i) * 3)
            trail_surf = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(
                trail_surf,
                (*self.color, alpha),
                (r + 1, r + 1),
                r,
            )
            surface.blit(trail_surf, (tx - r - 1, ty - r - 1))

        # Soft shadow (slightly offset filled ellipse)
        shadow_surf = pygame.Surface(
            (self.radius * 2 + 20, self.radius + 14), pygame.SRCALPHA
        )
        pygame.draw.ellipse(
            shadow_surf,
            (0, 0, 0, 35),
            shadow_surf.get_rect(),
        )
        surface.blit(shadow_surf, (self.x - self.radius - 10, self.y + self.radius - 4))

        # Main ball body
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

        # Specular highlight (top-left white gleam)
        hi_x = self.x - self.radius // 3
        hi_y = self.y - self.radius // 3
        hi_r = max(3, self.radius // 4)
        hi_surf = pygame.Surface((hi_r * 2, hi_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(hi_surf, (255, 255, 255, 130), (hi_r, hi_r), hi_r)
        surface.blit(hi_surf, (hi_x - hi_r, hi_y - hi_r))

    # ------------------------------------------------------------------ #
    #  Convenience                                                          #
    # ------------------------------------------------------------------ #

    @property
    def rect(self) -> pygame.Rect:
        """Bounding rect (useful for collision detection extensions)."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def reset(self) -> None:
        """Return ball to the screen centre and clear the trail."""
        self.x = self.screen_width  // 2
        self.y = self.screen_height // 2
        self._trail.clear()
        self.last_move_blocked = False

    def __repr__(self) -> str:
        return f"Ball(x={self.x}, y={self.y}, r={self.radius})"
