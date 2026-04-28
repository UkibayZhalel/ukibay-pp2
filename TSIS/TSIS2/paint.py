import pygame, sys, datetime
from tools import draw_shape, flood_fill

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("TSIS 2 Paint")
clk = pygame.time.Clock()
fnt = pygame.font.SysFont("Verdana", 14)
text_fnt = pygame.font.SysFont("Arial", 32)  # Шрифт для инструмента "Текст"

surf = pygame.Surface((w, h))
surf.fill((255, 255, 255))

cc = (0, 0, 0)
tool = "brush"
size = 5
flag = False
x1, y1 = 0, 0
last_x, last_y = 0, 0  # Для непрерывной линии карандаша

# Переменные для текста
is_typing = False
text_input = ""
text_pos = (0, 0)

colors_gui = [
    (pygame.Rect(10, 10, 30, 30), (0, 0, 0)),
    (pygame.Rect(50, 10, 30, 30), (255, 0, 0)),
    (pygame.Rect(90, 10, 30, 30), (0, 255, 0)),
    (pygame.Rect(130, 10, 30, 30), (0, 0, 255))
]

# Обновленный интерфейс кнопок
tools_gui = [
    (pygame.Rect(200, 10, 60, 25), "brush"),
    (pygame.Rect(270, 10, 60, 25), "eraser"),
    (pygame.Rect(340, 10, 60, 25), "rect"),
    (pygame.Rect(410, 10, 60, 25), "circle"),
    (pygame.Rect(480, 10, 60, 25), "line"),
    (pygame.Rect(550, 10, 60, 25), "text"),

    (pygame.Rect(200, 40, 60, 25), "square"),
    (pygame.Rect(270, 40, 60, 25), "r_tri"),
    (pygame.Rect(340, 40, 60, 25), "eq_tri"),
    (pygame.Rect(410, 40, 60, 25), "rhomb"),
    (pygame.Rect(480, 40, 60, 25), "fill")
]


def render_ui():
    # Шапка интерфейса
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, w, 80))

    for r, c in colors_gui:
        pygame.draw.rect(screen, c, r)
        if c == cc and tool != "eraser":
            pygame.draw.rect(screen, (255, 255, 255), r, 3)

    for r, t in tools_gui:
        bg = (150, 150, 150) if t == tool else (100, 100, 100)
        pygame.draw.rect(screen, bg, r)
        txt = fnt.render(t, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=r.center))

    # Подсказки
    info_txt = fnt.render(f"Size (1,2,3): {size} | Save: Ctrl+S", True, (50, 50, 50))
    screen.blit(info_txt, (10, 50))


while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

        elif e.type == pygame.KEYDOWN:
            if is_typing:
                if e.key == pygame.K_RETURN:
                    # Применяем текст
                    txt_surface = text_fnt.render(text_input, True, cc)
                    surf.blit(txt_surface, text_pos)
                    is_typing = False
                    text_input = ""
                elif e.key == pygame.K_ESCAPE:
                    is_typing = False
                    text_input = ""
                elif e.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += e.unicode
            else:
                # Изменение размера кисти
                if e.key == pygame.K_1:
                    size = 2
                elif e.key == pygame.K_2:
                    size = 5
                elif e.key == pygame.K_3:
                    size = 10

                # Сохранение (Ctrl+S)
                elif e.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"canvas_{now}.png"
                    pygame.image.save(surf, filename)
                    print(f"Saved: {filename}")

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if e.pos[1] < 80:  # Зона UI
                    for r, c in colors_gui:
                        if r.collidepoint(e.pos):
                            cc = c
                            if tool == "eraser": tool = "brush"

                    for r, t in tools_gui:
                        if r.collidepoint(e.pos):
                            tool = t
                else:
                    # Зона холста
                    if tool == "fill":
                        flood_fill(surf, e.pos, cc)
                    elif tool == "text":
                        is_typing = True
                        text_input = ""
                        text_pos = e.pos
                    else:
                        flag = True
                        x1, y1 = e.pos
                        last_x, last_y = e.pos

        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1 and flag:
                flag = False
                if tool not in ["brush", "eraser"]:
                    draw_shape(surf, tool, cc, x1, y1, e.pos[0], e.pos[1], size)

        elif e.type == pygame.MOUSEMOTION:
            if flag:
                if tool == "brush":
                    pygame.draw.line(surf, cc, (last_x, last_y), e.pos, size)
                    last_x, last_y = e.pos
                elif tool == "eraser":
                    pygame.draw.line(surf, (255, 255, 255), (last_x, last_y), e.pos, size * 4)
                    last_x, last_y = e.pos

    # Отрисовка
    screen.blit(surf, (0, 0))

    # Предпросмотр фигур при зажатой мышке
    if flag and tool not in ["brush", "eraser"]:
        mx, my = pygame.mouse.get_pos()
        draw_shape(screen, tool, cc, x1, y1, mx, my, size)

    # Отрисовка текста в реальном времени
    if is_typing:
        txt_surface = text_fnt.render(text_input + "|", True, cc)
        screen.blit(txt_surface, text_pos)

    # Интерфейс рендерится поверх предпросмотра
    render_ui()

    pygame.display.update()
    clk.tick(120)