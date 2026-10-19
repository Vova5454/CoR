import pygame as pg


pg.init()

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

image_name = "GCHRBehind"
IMAGE = pg.image.load(f'res/{image_name}.png').convert_alpha()

rects = [pg.Rect(325, 340, 150, 250), pg.Rect(150, 340, 150, 250), pg.Rect(500, 340, 150, 250),
         pg.Rect(325, 10, 150, 250), pg.Rect(150, 10, 150, 250), pg.Rect(500, 10, 150, 250)]
rects = [pg.Rect(412, 340, 150, 250), pg.Rect(238, 340, 150, 250),
         pg.Rect(412, 10, 150, 250), pg.Rect(238, 10, 150, 250)]
rects = [pg.Rect(0, 0, 700, 100)]
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