import pygame
from collections import deque

def flood_fill(surface, start_pos, fill_color):
    """Алгоритм заливки (Поиск в ширину - BFS)"""
    target_color = surface.get_at(start_pos)
    # Если кликнули по тому же цвету, ничего не делаем
    if target_color == fill_color:
        return

    w, h = surface.get_width(), surface.get_height()
    queue = deque([start_pos])
    surface.set_at(start_pos, fill_color)

    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            # Проверка границ экрана
            if 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny)) == target_color:
                    surface.set_at((nx, ny), fill_color)
                    queue.append((nx, ny))

def draw_shape(surface, t, c, start_x, start_y, end_x, end_y, s):
    """Универсальная функция отрисовки фигур"""
    if t == "line":
        pygame.draw.line(surface, c, (start_x, start_y), (end_x, end_y), s)
    elif t == "rect":
        # Используем normalize, чтобы можно было рисовать справа налево и снизу вверх
        rect = pygame.Rect(start_x, start_y, end_x - start_x, end_y - start_y)
        rect.normalize()
        pygame.draw.rect(surface, c, rect, s)
    elif t == "circle":
        r = int(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5)
        pygame.draw.circle(surface, c, (start_x, start_y), r, s)
    elif t == "square":
        side = max(abs(end_x - start_x), abs(end_y - start_y))
        sx = 1 if end_x > start_x else -1
        sy = 1 if end_y > start_y else -1
        rect = pygame.Rect(start_x, start_y, side * sx, side * sy)
        rect.normalize()
        pygame.draw.rect(surface, c, rect, s)
    elif t == "r_tri":
        pygame.draw.polygon(surface, c, [(start_x, start_y), (start_x, end_y), (end_x, end_y)], s)
    elif t == "eq_tri":
        mid_x = start_x + (end_x - start_x) // 2
        pygame.draw.polygon(surface, c, [(mid_x, start_y), (start_x, end_y), (end_x, end_y)], s)
    elif t == "rhomb":
        mid_x = start_x + (end_x - start_x) // 2
        mid_y = start_y + (end_y - start_y) // 2
        pygame.draw.polygon(surface, c, [(mid_x, start_y), (end_x, mid_y), (mid_x, end_y), (start_x, mid_y)], s)