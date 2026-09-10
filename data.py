import pygame as pg
import pygame.freetype as pgft


pg.init()
rec1 = pg.Rect(700, 600, 100, 600)
rec1.bottomleft = (700, 600)
rec2 = pg.Rect(0, 600, 100, 600)
rec2.bottomleft = (0, 600)

rec3 = pg.Rect(350, 100, 100, 100)
rec3.bottomleft = (350, 100)

loc = "0"

movement = {
    "0": {"1": rec1, "2": rec3},
    "1": {"0": rec2},
    "2": {"1": rec1}
}



def recty(lp, mouse, way=0):
    lc = min(lp[0], mouse[0])
    lr = min(lp[1], mouse[1])
    sizel = abs(lp[0]-mouse[0])
    sizer = abs(lp[1]-mouse[1])
    if way == 1:
        return f'pg.Rect({lc}, {lr}, {sizel}, {sizer})'
    return pg.Rect(lc, lr, sizel, sizer)

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Get Cords")
clock = pg.time.Clock()

image_name = "arcade1"
IMAGE = pg.image.load(f'res/{image_name}.png').convert_alpha()

rects = []
lp = None
run = True
while run:
    screen.fill((255, 255, 255))
    screen.blit(IMAGE, (0, 0))
    if lp:
        pg.draw.ellipse(screen, (255, 0, 0), pg.Rect(lp[0]-2.5, lp[1]-2.5, 5, 5))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            if lp:
                print(recty(lp, mouse, 1))
                rects.append(recty(lp, mouse))
                lp = None
            else:
                lp = mouse
    if rects:
        for rect in rects:
            pg.draw.rect(screen, (127, 127, 127), rect)
    pg.display.flip()
    clock.tick(30)