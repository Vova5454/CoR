import pygame as pg
import pygame.freetype as pgft
import os
from time import sleep
from interaction import process_interactions
from consts import WIDTH, HEIGHT, FPS, save_folder
from func import file_thing, save, default, sfx, mus, fill_out_six_files, def_game, def_dia
from func import setup_dialogue, setup_game, animate, settings
from game import process_game


#os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"
"This command makes each pixel 1x1 instead the default 2x2"
"Usually, pygame makes each pixel 2 times wider and higher."
"If you remove the # from the line above that won't happen."

pg.init()
pgft.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("CoR")
clock = pg.time.Clock()
screen.blit(pg.image.load('res/loading.png'), (0, 0))
pg.display.flip()

movement = {
    'start': {'bathroom': pg.Rect(305, 98, 99, 206),
              'living_room': pg.Rect(652, 188, 48, 262)},
    'bathroom': {'kitchen': pg.Rect(395, 3, 147, 225),
                 'start': pg.Rect(0, 550, 800, 50)},
    'his_place': {},
    'kitchen': {'bathroom': pg.Rect(0, 550, 800, 50),
                'entry': pg.Rect(760, 0, 40, 600)},
    'entry': {"7's_room": pg.Rect(720, 0, 80, 600),
              'kitchen': pg.Rect(0, 0, 40, 600),
              'hall': pg.Rect(187, 534, 322, 65)},
    'hall': {"6's_room": pg.Rect(14, 120, 160, 347),
             "5's_room": pg.Rect(293, 96, 106, 269),
             "4's_room": pg.Rect(486, 87, 85, 225),
             "1's_room": pg.Rect(668, 91, 94, 260),
             'entry': pg.Rect(0, 525, 800, 75)},
    'living_room': {"1's_room": pg.Rect(170, 57, 157, 255),
                    "2's_room": pg.Rect(597, 124, 75, 350),
                    'start': pg.Rect(0, 0, 25, 600)},
    "1's_room": {'hall': pg.Rect(31, 200, 61, 311),
                 'living_room': pg.Rect(699, 260, 47, 273)},
    "2's_room": {'living_room': pg.Rect(111, 189, 115, 316),
                 "3's_room": pg.Rect(513, 173, 103, 188)},
    "3's_room": {"2's_room": pg.Rect(0, 550, 800, 50)},
    "4's_room": {"hall": pg.Rect(0, 550, 800, 50)},
    "5's_room": {"hall": pg.Rect(0, 550, 800, 50)},
    "6's_room": {'hall': pg.Rect(0, 550, 800, 50)},
    "7's_room": {"entry": pg.Rect(0, 0, 50, 600)},
    "intersection1": {"entry": pg.Rect(260, 520, 285, 80),
                      "neighborhood1": pg.Rect(325, 74, 236, 324),
                      "LefterTop": pg.Rect(0, 0, 50, 600), 
                      "LongAlley": pg.Rect(750, 0, 50, 600)},
    "LongAlley": {"BehindHouse": pg.Rect(216, 92, 263, 261),
                  "intersection1": pg.Rect(0, 550, 800, 50)},
    "BehindHouse": {"LongAlley": pg.Rect(750, 0, 50, 600)},
    "LefterTop": {"Arcade": pg.Rect(300, 232, 62, 204),
                  "FarWall": pg.Rect(182, 261, 69, 65),
                  "intersection1": pg.Rect(750, 0, 50, 600)},
    "Arcade": {"LefterTop": pg.Rect(0, 0, 50, 600)},
    "FarWall": {"LefterTop": pg.Rect(0, 500, 800, 100)},
    "neighborhood1": {"intersection2": pg.Rect(315, 225, 120, 104),
                      "intersection1": pg.Rect(750, 0, 50, 600)},
    "intersection2": {"DatCorner": pg.Rect(750, 0, 50, 600),
                      "LCPE": pg.Rect(0, 0, 50, 600),
                      "neighborhood1": pg.Rect(0, 550, 800, 50)},
    "LCPE": {"LCE": pg.Rect(655, 173, 144, 282),
             "intersection2": pg.Rect(0, 550, 800, 50)},
    "DatCorner": {"intersection2": pg.Rect(0, 0, 50, 600),
                  "CasinoEntrance": pg.Rect(53, 162, 80, 183),
                  "DatCornerR": pg.Rect(750, 0, 50, 600)},
    "DatCornerR": {"DatCorner": pg.Rect(0, 0, 50, 600),
                   "DatCornerRB": pg.Rect(0, 550, 800, 50)},
    "DatCornerRB": {"DatCornerR": pg.Rect(0, 550, 800, 50),
                    "Shop": pg.Rect(553, 165, 79, 157)},
    "Arcade1": {"Arcade": pg.Rect(0, 550, 800, 50),
                "Arcade2": pg.Rect(750, 0, 50, 600)},
    "Arcade2": {"Arcade1": pg.Rect(0, 0, 50, 600)},
    "CasinoEntrance": {"DatCorner": pg.Rect(0, 550, 800,50),
                       "Roulette": pg.Rect(241, 216, 255, 255),
                       "CasinoSlot": pg.Rect(750, 0, 50, 600)},
    "Roulette": {},
    "CasinoSlot": {"CasinoEntrance": pg.Rect(0, 0, 50, 600),
                   "CasinoBlackjack": pg.Rect(750, 0, 50, 600)},
    "CasinoBlackjack": {"CasinoSlot": pg.Rect(0, 0, 50, 600)},
    "LCE": {"LCPE": pg.Rect(0, 0, 800, 600)}
}

interactions = {
    'bathroom': [(pg.Rect(660, 124, 81, 91), 'blowhorn')],
    'kitchen': [(pg.Rect(107, 360, 200, 200), 'talk_to_him'),
                (pg.Rect(698, 337, 64, 73), 'eat_banana')],
    'his_place': [(pg.Rect(300, 200, 200, 200), 'talk_to_him')],
    'entry': [(pg.Rect(324, 39, 140, 227), 'leave')],
    'living_room': [(pg.Rect(32, 207, 87, 97), 'view_hubert')],
    "1's_room": [(pg.Rect(155, 274, 35, 32), 'steal_money'),
                 (pg.Rect(287, 250, 36, 60), 'view_him'),
                 (pg.Rect(515, 351, 104, 37), 'read_book'),
                 (pg.Rect(192, 254, 43, 13), 'read_note')],
    "2's_room": [(pg.Rect(35, 282, 39, 157), '2VIhotel'),
                 (pg.Rect(172, 12, 102, 81), '2VIarcade'),
                 (pg.Rect(255, 139, 50, 148), '2VIzoo'),
                 (pg.Rect(365, 168, 83, 67), '2VIrmaze'),
                 (pg.Rect(556, 20, 75, 117), '2VIguardpos'),
                 (pg.Rect(673, 212, 73, 63), '2VIlandmine')],
    "3's_room": [(pg.Rect(44, 179, 85, 165), "3TV"),
                  (pg.Rect(189, 333, 187, 137), "3Couch"),
                  (pg.Rect(211, 203, 150, 71), "3Candles"),
                  (pg.Rect(338, 37, 138, 76), "3Chandelier"),
                  (pg.Rect(395, 440, 268, 57), "3Mattress"),
                  (pg.Rect(406, 162, 142, 247), "3")],
    "4's_room": [(pg.Rect(104, 76, 94, 89), "4HA"),
                 (pg.Rect(310, 74, 99, 94), "4Fatass"),
                 (pg.Rect(464, 76, 200, 92), "410"),
                 (pg.Rect(106, 216, 80, 86), "4Dead"),
                 (pg.Rect(222, 213, 84, 86), "4Eat"),
                 (pg.Rect(351, 216, 89, 88), "4ToS"),
                 (pg.Rect(504, 218, 100, 103), "4Exit"),
                 (pg.Rect(126, 316, 189, 178), "4NoExit"),
                 (pg.Rect(384, 353, 240, 95), "4LongText")],
    "5's_room": [(pg.Rect(613, 153, 187, 279), "5HUBERT"),
                 (pg.Rect(101, 124, 33, 82), "5L"),
                 (pg.Rect(16, 181, 71, 217), "5L"),
                 (pg.Rect(109, 223, 68, 161), "5L"),
                 (pg.Rect(16, 397, 159, 38), "5L"),
                 (pg.Rect(9, 36, 76, 168), "5L"),
                 (pg.Rect(13, 430, 163, 123), "5L"),
                 (pg.Rect(160, 140, 96, 90), "5R"),
                 (pg.Rect(194, 245, 242, 88), "5R"),
                 (pg.Rect(297, 155, 144, 70), "5R"),
                 (pg.Rect(486, 170, 104, 55), "5R"),
                 (pg.Rect(468, 252, 110, 50), "5R"),
                 (pg.Rect(205, 315, 225, 105), "5R")],
    "6's_room": [(pg.Rect(265, 229, 64, 78), "Lay's Chips #6"),
                 (pg.Rect(556, 99, 62, 53), "6SpiderWeb")],
    "7's_room": [(pg.Rect(50, 0, 750, 600), "7")],
    "BehindHouse": [(pg.Rect(302, 225, 42, 33), "HELP!")],
    "Arcade": [(pg.Rect(356, 289, 84, 114), "Arcade")],
    "neighborhood1": [(pg.Rect(196, 173, 67, 291), "1's_house")], ##
    'intersection2': [(pg.Rect(273, 97, 213, 243), "Dummy!")],
    "LCPE": [(pg.Rect(161, 0, 214, 139), "BrickWall")],
    "DatCorner": [(pg.Rect(544, 136, 133, 189), "EnterGCH"), ##
                  (pg.Rect(231, 270, 146, 131), "chips")], ##
    "DatCornerR": [(pg.Rect(449, 168, 113, 168), "EnterRestuarant")], ##
    "DatCornerRB": [(pg.Rect(4, 90, 371, 259), "Dumpster")],
    "Arcade1": [(pg.Rect(96, 153, 115, 286), "ArcadeGame1"),
                (pg.Rect(297, 143, 126, 298), "ArcadeGame2"), 
                (pg.Rect(536, 140, 132, 307), "ArcadeGame3")],
    "Arcade2": [(pg.Rect(262, 73, 201, 438), "ArcadeGame4")],
    "CasinoSlot": [(pg.Rect(297, 0, 196, 475), "CasinoSlot")],
    "CasinoBlackjack": [(pg.Rect(174, 84, 471, 332), "Blackjack")]
}

images = {
    "start": pg.image.load(file_thing('res/start.png')).convert_alpha(),
    "bathroom": pg.image.load(file_thing('res/bathroom.png')).convert_alpha(),
    'kitchen': pg.image.load(file_thing('res/kitchen.png')).convert_alpha(),
    'his_place': pg.image.load(file_thing('res/white.png')),
    'kitchen+b': pg.image.load(file_thing('res/kitchen+b.png')).convert_alpha(),
    'entry': pg.image.load(file_thing('res/entry.png')).convert_alpha(),
    'hall': pg.image.load(file_thing('res/hall.png')).convert_alpha(),
    'living_room': pg.image.load(file_thing('res/living_room.png')).convert_alpha(),
    "1's_room": pg.image.load(file_thing("res/1's_room.png")).convert_alpha(),
    "2's_room": pg.image.load(file_thing("res/2's_room.png")).convert_alpha(),
    "2's_room+p": pg.image.load(file_thing("res/2's_room+p.png")).convert_alpha(),
    "3's_room": pg.image.load(file_thing("res/3's_room.png")).convert_alpha(),
    "4's_room": pg.image.load(file_thing("res/4's_room.png")).convert_alpha(),
    "5's_room": pg.image.load(file_thing("res/5's_room.png")).convert_alpha(),
    "6's_room": pg.image.load(file_thing("res/6's_room.png")).convert_alpha(),
    "6's_room+C": pg.image.load(file_thing("res/6's_room+C.png")).convert_alpha(),
    "7's_room": pg.image.load(file_thing("res/7's_room.png")).convert_alpha(),
    "intersection1": pg.image.load(file_thing("res/intersection1.png")).convert_alpha(),
    "LongAlley": pg.image.load(file_thing("res/LongAlley.png")).convert_alpha(),
    "BehindHouse": pg.image.load(file_thing("res/BehindHouse.png")).convert_alpha(),
    "LefterTop": pg.image.load(file_thing("res/LefterTop.png")).convert_alpha(),
    "Arcade": pg.image.load(file_thing("res/Arcade.png")).convert_alpha(),
    "FarWall": pg.image.load(file_thing("res/FarWall.png")).convert_alpha(),
    "neighborhood1": pg.image.load(file_thing("res/neighborhood1.png")).convert_alpha(),
    "intersection2": pg.image.load(file_thing("res/intersection2.png")).convert_alpha(),
    "LCPE": pg.image.load(file_thing('res/LCPE.png')).convert_alpha(),
    "DatCorner": pg.image.load(file_thing('res/DatCorner.png')).convert_alpha(),
    "DatCornerR": pg.image.load(file_thing('res/DatCornerR.png')).convert_alpha(),
    "DatCornerRB": pg.image.load(file_thing('res/DatCornerRB.png')).convert_alpha(),
    "Arcade1": pg.image.load(file_thing('res/arcade1.png')).convert_alpha(),
    "ppu": pg.image.load(file_thing('res/ping_pong_you.png')).convert_alpha(),
    "pph": pg.image.load(file_thing('res/ping_pong_him.png')).convert_alpha(),
    "Arcade2": pg.image.load(file_thing('res/Arcade2.png')).convert_alpha(),
    "CasinoEntrance": pg.image.load(file_thing('res/CasinoEntrance.png')).convert_alpha(),
    "Roulette": pg.image.load(file_thing('res/roulette.png')).convert_alpha(),
    "CasinoSlot": pg.image.load(file_thing('res/CasinoSlot.png')).convert_alpha(),
    "CSM": pg.image.load(file_thing('res/CasinoSlotMachine.png')).convert_alpha(),
    "Casino/SlotMachine/empty": pg.image.load(file_thing("res/Casino/SlotMachine/empty.png")).convert_alpha(),
    "LCE": pg.image.load(file_thing("res/LCE.png")).convert_alpha(),
    "CasinoBlackjack": pg.image.load(file_thing("res/CasinoBlackjack.png")).convert_alpha()
}

icons = {
    'key': pg.image.load(file_thing("res/icons/key.png")).convert_alpha(),
    'null': pg.image.load(file_thing('res/icons/null.png')).convert_alpha(),
    'error': pg.image.load(file_thing('res/icons/error.png')).convert_alpha()
}

plus = pg.image.load(file_thing("res/dummy_plus.png"))
minus = pg.image.load(file_thing("res/dummy_minus.png"))
frames = [pg.image.load(file_thing(f'res/frames/{x}.png')) for x in range(10)]
strongest = frames[9]
inv_left = pg.image.load(file_thing("res/inv_left.png")).convert_alpha()
inv_right = pg.image.load(file_thing("res/inv_right.png")).convert_alpha()

pg.mixer.init()

saved = pg.mixer.Sound(file_thing('res/sound/saved.mp3'))
bye = pg.mixer.Sound(file_thing('res/sound/bye.mp3'))

musID = {
    'home': pg.mixer.Sound(file_thing('res/sound/cor1.wav')),
    '1': pg.mixer.Sound(file_thing("res/sound/1s_room.mp3")),
    '2': pg.mixer.Sound(file_thing("res/sound/2s_room.mp3")),
    '3': pg.mixer.Sound(file_thing("res/sound/3s_room.mp3")),
    '4': pg.mixer.Sound(file_thing("res/sound/4s_room.mp3")),
    '5': pg.mixer.Sound(file_thing("res/sound/5s_room.mp3")),
    '6': pg.mixer.Sound(file_thing("res/sound/6s_room.mp3")),
    '7': pg.mixer.Sound(file_thing("res/sound/7s_room.mp3")),
    'CoR1': pg.mixer.Sound(file_thing("res/sound/outside.mp3")),
    'Arcade': pg.mixer.Sound(file_thing("res/sound/arcade.mp3")),
    'Ping-Pong': pg.mixer.Sound(file_thing('res/sound/PingPong.mp3')),
    "Space-Invaders": pg.mixer.Sound(file_thing('res/sound/SpaceInvaders.mp3')),
    "PingPongWV": pg.mixer.Sound(file_thing("res/sound/PingPong_WV.mp3")),
    "Casino": pg.mixer.Sound(file_thing("res/sound/Casino.mp3"))
}

playing = {music: float('-inf') for music in musID}

font = pg.font.Font(None, 72)
errortext = font.render("BG not found :(", True, (0, 0, 0))
mmmfont = pgft.Font(None, 36)
casino_font = pgft.SysFont("Bell MT", 24)

savem = False
current = None
deleto = False
framei = 0
inspired = []
mmmfont_read = -1500
filerects0 = [pg.Rect(200+150*x, 50, 100, 50) for x in range(3)]
filerects1 = [pg.Rect(200+150*x, 500, 100, 50) for x in range(3)]
filerects = filerects0 + filerects1
slick = False
mbuttons = [pg.Rect(300, 150*x+37.5, 200, 75) for x in range(4)]
mbuttonstext = ["Back", "Save", "Main Menu", "Quit"]
save_file_page = 0
mm = True
m = False
need_error = False
mmbuttons = [pg.Rect(300, 150*x+75, 200, 75) for x in range(4)]
mmbuttonstext = ["Start", "Load", "QUIT", "Delete"]
savefile = None

in_inventory = False
inventory_page = 0

dialogue = def_dia()

six_files = [[None, None, None, None, None, None] for _ in range(256)]

game = def_game()

frame = 0
holding = False
run = True
while run:
    rdud = {}
    pressing = set()
    frame += 1
    framei += 1
    if framei == 30:
        framei = 0
    if framei % 3 == 0:
        strongest = animate(frames, framei//3)
    now = pg.time.get_ticks()
    need_pic = False
    screen.fill((255, 255, 255))
    
    try:
        if current:
            if current['loc'] == 'kitchen' and current['atebanana']:
                screen.blit(images['kitchen+b'], (0, 0))
            elif current['loc'] == "2's_room" and current['poster']:
                screen.blit(images["2's_room+p"], (0, 0))
            elif current['6Chips'] and current['loc'] == "6's_room":
                screen.blit(images["6's_room+C"], (0, 0))
            else:
                screen.blit(images[current['loc']], (0, 0))
    except Exception:
        need_pic = True
        screen.blit(errortext, (200, 100))
    clciked = False
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            bye.set_volume(sfx)
            bye.play()
            sleep(bye.get_length())
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and not mm and not dialogue['on'] and not game['on']:
                m = {True: False, False: True}[m]
            if event.key == pg.K_0: pressing.add(0)
            if event.key == pg.K_1: pressing.add(1)
            if event.key == pg.K_2: pressing.add(2)
            if event.key == pg.K_3: pressing.add(3)
            if event.key == pg.K_4: pressing.add(4)
            if event.key == pg.K_5: pressing.add(5)
            if event.key == pg.K_6: pressing.add(6)
            if event.key == pg.K_7: pressing.add(7)
            if event.key == pg.K_8: pressing.add(8)
            if event.key == pg.K_9: pressing.add(9)
            if event.key == pg.K_BACKSPACE: pressing.add('backspace')
            if event.key == pg.K_MINUS: pressing.add('-')
            if event.key == pg.K_CAPSLOCK: pressing.add('CAPSLOCK')
            if event.key == pg.K_SPACE: pressing.add(' ')
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0] and not holding:
                clciked = True
    for music in musID.values():
        music.set_volume(mus)
    now = pg.time.get_ticks()
    if m:
        screen.fill((25, 150, 50))
        for i in range(len(mbuttonstext)):
            pg.draw.rect(screen, (255, 127, 0), mbuttons[i])
            mmmfont.render_to(screen, (310, 150*i+75), mbuttonstext[i], (255, 255, 255))
        for recti in range(len(mbuttons)):
            if mbuttons[recti].collidepoint(mouse) and clciked:
                if recti == 0:
                    m = False
                elif recti == 1:
                    save(savefile, current)
                    saved.set_volume(sfx)
                    saved.play()
                elif recti == 2:
                    current = None
                    m = False
                    mm = True
                    savefile = None
                    deleto = False
                    savem = False
                    slick = True
                    for _, music in musID.items():
                        music.stop()
                    for played in playing:
                        playing[played] = float('-inf')
                else:
                    bye.set_volume(sfx)
                    bye.play()
                    sleep(bye.get_length())
                    run = False
        pg.draw.rect(screen, (127, 127, 127), pg.Rect(600, 50, 150, 50))
        pg.draw.rect(screen, (127, 127, 127), pg.Rect(600, 150, 150, 50))
        screen.blit(plus, (600, 50))
        screen.blit(plus, (600, 150))
        screen.blit(minus, (700, 50))
        screen.blit(minus, (700, 150))
        sfxe = 0
        muse = 0
        if pg.Rect(600, 50, 50, 50).collidepoint(mouse) and (clciked or pg.mouse.get_pressed()[2]):
            sfxe += 0.01
        if pg.Rect(700, 50, 50, 50).collidepoint(mouse) and (clciked or pg.mouse.get_pressed()[2]):
             sfxe -= 0.01
        if pg.Rect(600, 150, 50, 50).collidepoint(mouse) and (clciked or pg.mouse.get_pressed()[2]):
            muse += 0.01
        if pg.Rect(700, 150, 50, 50).collidepoint(mouse) and (clciked or pg.mouse.get_pressed()[2]):
            muse -= 0.01
        settings['sfx'] += sfxe
        settings['mus'] += muse
        if settings['sfx'] < 0: settings['sfx'] = 0
        if settings['mus'] < 0: settings['mus'] = 0
        if pg.key.get_pressed()[pg.K_BACKSPACE]:
            settings['sfx'] = 1
            settings['mus'] = 1
        minifont = pgft.SysFont(None, 12)
        minifont.render_to(screen, (660, 60), str((settings['sfx']*100)//1), (255, 255, 255))
        minifont.render_to(screen, (660, 160), str((settings['mus']*100)//1), (255, 255, 255))
        save("settings.json", settings)
        sfx = settings['sfx']
        mus = settings['mus']
        clciked = False
    if mm:
        screen.fill((200, 200, 200))
        for i in range(len(mmbuttonstext)):
          pg.draw.rect(screen, (0, 0, 0), mmbuttons[i])
          mmmfont.render_to(screen, (350, 150*i+100), mmbuttonstext[i], (255, 255, 255))
        for recti in range(len(mmbuttons)):
            if mmbuttons[recti].collidepoint(mouse) and clciked and not savem and not deleto:
                clciked = False
                if recti == 2:
                    bye.set_volume(sfx)
                    bye.play()
                    sleep(bye.get_length())
                    run = False
                elif recti == 1:
                    savem = True
                    filled_out_six_files = False
                    fill_out_six_files(six_files)
                elif recti == 0:
                    mmmfont_read = now
                    
                elif recti == 3:
                    deleto = True
                    fill_out_six_files(six_files)
                    screen.fill((200, 255, 255))
        if slick:
            savem = False
            slick = False
            deleto = False
            mm = True
            m = False
        if savem:
            screen.fill((200, 255, 255))
            for i in range(len(filerects)):
                file = six_files[save_file_page][i]
                if file:
                    if file.get("image", False):
                        image = pg.transform.scale(
                        pg.image.load(file_thing(
                            os.path.expanduser(file['image']))), filerects[i].size)
                        screen.blit(image, filerects[i].topleft)
                    elif file.get("color", False):
                        pg.draw.rect(screen, file['color'], filerects[i])
                    else:
                        pg.draw.rect(screen, (0, 255, 0), filerects[i])
                else:
                    pg.draw.rect(screen, (0, 0, 0), filerects[i])
                if not file.get("Remove_Slot_Index", False):
                    text, rect = mmmfont.render(str(i+1+6*save_file_page), (255, 255, 255))
                    rect.center = filerects[i].center
                    screen.blit(text, rect)
            mmmfont.render_to(screen, (400, 10), str(save_file_page+1))
            screen.blit(minus, (0, 0))
            screen.blit(plus, (800-plus.get_width(), 0))
            if pg.Rect(0, 0, minus.get_width(), minus.get_height()).collidepoint(
                mouse) and (clciked or pg.mouse.get_pressed()[2]):
                save_file_page -= 1
            if pg.Rect(800-plus.get_width(), 0, plus.get_width(), plus.get_height()).collidepoint(
                mouse) and (clciked or pg.mouse.get_pressed()[2]):
                save_file_page += 1
            if save_file_page == -1: save_file_page = 255
            if save_file_page == 256: save_file_page = 0

            for rect in range(len(filerects)):
                if filerects[rect].collidepoint(mouse) and clciked:
                    savem = False
                    savefile = f'data{rect+1+6*save_file_page}.json'
                    playing['home'] = float('-inf')
                    dialogue = def_dia()
                    current = save(savefile)
                    if current == {}:
                        save(savefile, default)
                        current = default
                    if os.path.exists(savefile) and os.path.getsize(savefile) == 0:
                        save(savefile, default)
                        current = default
                    for elem in default:
                        if current.get(elem, default[elem]) == default[elem]:
                            current[elem] = default[elem]
                    save(savefile, current)
                    mm = False
                    inspired = []
                    clciked = False
        if deleto:
            screen.fill((110, 20, 20))
            for i in range(len(filerects)):
                file = six_files[save_file_page][i]
                if file:
                    if file.get('image', False):
                        image = pg.transform.scale(
                        pg.image.load(file_thing(
                        os.path.expanduser(file['image']))), filerects[i].size)
                        screen.blit(image, filerects[i].topleft)
                    elif file.get('color', False):
                        pg.draw.rect(screen, file['color'], filerects[i])
                    else:
                        pg.draw.rect(screen, (0, 255, 0), filerects[i])
                else:
                    pg.draw.rect(screen, (0, 0, 0), filerects[i])
                if not file.get('Remove_Slot_Index', False):
                    text, rect = mmmfont.render(str(i+1+6*save_file_page), (255, 255, 255))
                    rect.center = filerects[i].center
                    screen.blit(text, rect)
            mmmfont.render_to(screen, (400, 10), str(save_file_page+1))
            screen.blit(minus, (0, 0))
            screen.blit(plus, (800-plus.get_width(), 0))
            if pg.Rect(0, 0, minus.get_width(), minus.get_height()).collidepoint(
                mouse) and (clciked or pg.mouse.get_pressed()[2]):
                save_file_page -= 1
            if pg.Rect(800-plus.get_width(), 0, plus.get_width(), plus.get_height()).collidepoint(
                mouse) and (clciked or pg.mouse.get_pressed()[2]):
                save_file_page += 1
            if save_file_page == -1: save_file_page = 255
            if save_file_page == 256: save_file_page = 0

            for rect in range(len(filerects)):
                if filerects[rect].collidepoint(mouse) and clciked:
                    clciked = False
                    savem = False
                    if os.path.exists(os.path.join(save_folder, f'data{rect+1+6*save_file_page}.json')):
                        os.remove(os.path.join(save_folder, f'data{rect+1+6*save_file_page}.json'))
                    deleto = False
    if now - mmmfont_read < 1500 and mm and not savem:
        mmmfont.render_to(screen,
            (0, 300),
            "Select load to pick a save file or delete one",
            (255, 0, 0))
    if need_error and not m and not mm:
        mmmfont.render_to(screen, (300, 200), 'Error! You are stuck.', (255, 0, 0))
    now = pg.time.get_ticks()
    if current is not None and not m and not mm:
        if current['loc'] in ['start', 'kitchen', 'bathroom', 'his_place',
                              'entry', 'living_room', 'hall']:
            current['mus'] = 'home'
        elif current['loc'][1:] == "'s_room":
            current['mus'] = f'{current['loc'][0]}'
        elif current['loc'] in ["intersection1", "Arcade", "DatCorner"]:
            current['mus'] = 'CoR1'
        elif current['loc'] == "Arcade1" and not game['on']:
            current['mus'] = 'Arcade'
        elif current['loc'] == "CasinoEntrance":
            current['mus'] = "Casino"
        for id, music in musID.items():
            if id != current['mus']:
                playing[id] = float('-inf')
                music.stop()
        try:
            need_error = False
            for des, rec in movement[current['loc']].items():
                if rec.collidepoint(mouse) and not dialogue['on'] and not game['on']:
                    sur = pg.Surface((rec.width, rec.height), pg.SRCALPHA)
                    sur.fill((0, 0, 0, 127))
                    screen.blit(sur, (rec.x, rec.y))
                    if clciked:
                        current['loc'] = des
                        clciked = False
        except Exception:
            need_error = True
        if need_pic:
            mmmfont.render_to(screen, (400, 300), str(current['loc']), (0, 0, 0))
        if current:
            if now-playing[current['mus']]>=musID[current['mus']].get_length()*1000:
                musID[current['mus']].set_volume(mus)
                musID[current['mus']].play()
                playing[current['mus']] = now
        if current['loc'] in interactions and not dialogue['on'] and not game['on']:
            for ntc, interaction in interactions[current['loc']]:
                if ntc.collidepoint(mouse) and clciked:
                    process_interactions(interaction, current, sfx, now, musID, playing,
                    savefile, frame, FPS, game, dialogue, inspired)
                    clciked = False
        if not game['on'] and not dialogue['on'] and not in_inventory:
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(700, 0, 100, 50))
            mmmfont.render_to(screen, (710, 10), "inv.", (255, 255, 255))
            if pg.Rect(700, 0, 100, 50).collidepoint(mouse) and clciked:
                in_inventory = True
                continue
        if game['on'] or dialogue['on']: in_inventory = False
        inventory_inspection = 'null'
        if in_inventory:
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, 100, 800, 1))
            pg.draw.rect(screen, (255, 255, 255), pg.Rect(50, 0, 600, 100))
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(700, 0, 100, 100))
            mmmfont.render_to(screen, (710, 10), "inv.", (255, 255, 255))
            if pg.Rect(700, 0, 100, 100).collidepoint(mouse) and clciked:
                in_inventory = False
            if inventory_page*6>len(current['inventory']):
                inventory_page -= 1
            if inventory_page < 0: inventory_page = 0
            start_pos = 50
            if len(current['inventory'])>0:
                for i in range(6):
                    temp_is_error = False
                    if i+6*inventory_page<len(current['inventory']):
                        try:
                            screen.blit(icons[current['inventory'][i+6*inventory_page]],
                            (start_pos, 0))
                        except KeyError:
                            print(current['inventory'], i, inventory_page)
                            screen.blit(icons['error'],
                            (start_pos, 0))
                            temp_is_error = True                    
                        if pg.Rect(start_pos, 0, 100, 100).collidepoint(mouse) and clciked:
                            if temp_is_error:
                                inventory_inspection = 'error'
                            else:
                                inventory_inspection = current['inventory'][i+6*inventory_page]
                            iiid = i+6*inventory_page
                    else:
                        screen.blit(icons['null'], (start_pos, 0))
                    start_pos += 100
            screen.blit(inv_left, (0, 0))
            if pg.Rect(0, 0, 50, 100).collidepoint(mouse) and clciked:
                inventory_page -= 1
            screen.blit(inv_right, (650, 0))
            if pg.Rect(650, 0, 50, 100).collidepoint(mouse) and clciked:
                inventory_page += 1
        if inventory_inspection and inventory_inspection != 'null':
            if inventory_inspection == 'key':
                setup_dialogue(dialogue, ["It's a key!", "What could it be for?"],
                                          font=pgft.SysFont(None, 32))
            elif inventory_inspection == 'error':
                setup_dialogue(dialogue, ["An error occured :("])
        if current['loc'] in ['kitchen', 'his_place']:
            if current['loc'] == 'kitchen':
                screen.blit(strongest, (107, 360))
            else:
                screen.blit(strongest, (300, 200))
        if current['loc'] == "Roulette" and not game['on']:
            pg.draw.rect(screen, (64, 64, 64), pg.Rect(600, 400, 150, 50))
            casino_font.render_to(screen, (610, 410), "EXIT", (186, 186, 186))
            if pg.Rect(600, 400, 150, 50).collidepoint(mouse) and clciked:
                current['loc'] = "CasinoEntrance"
            pg.draw.rect(screen, (100, 100, 200), pg.Rect(600, 100, 150, 50))
            casino_font.render_to(screen, (610, 110), "Start", (120, 50, 60))
            if pg.Rect(600, 100, 150, 50).collidepoint(mouse) and clciked:
                setup_game(game, "CasinoGame", 1,
                    {"ball": pg.Rect(388, 288, 24, 24)},
                    {},
                    {"start": False, "bet": 0, "text": [float('-inf'), ""],
                    "betting_on": False, "starttime": float('-inf'),
                    "ISTM": False, "toast": [False for _ in range(37)]},
                    {"dist": 175, "def": FPS, "FPS": float('inf')})
                clciked = False
        if dialogue['on']:
            if not dialogue['name']:
                pg.draw.rect(screen, (0, 0, 0), pg.Rect(50, 300, 700, 250))
                smr = pg.Rect(60, 310, 680, 230)
                pg.draw.rect(screen, (255, 255, 255), smr)
            else:
                pg.draw.rect(screen, (0, 0, 0), pg.Rect(50, 250, 700, 260))
                smr = pg.Rect(60, 260, 680, 240)
                pg.draw.rect(screen, (255, 255, 255), smr)
                pg.draw.rect(screen, (0, 0, 0), pg.Rect(60, 310, 680, 5))
                dialogue['font'].render_to(screen, (65, 265), dialogue['name'], (0, 0, 0))
            if not dialogue['inoptions']:
                if dialogue['JSR']:
                    clciked = False
                    if dialogue['diaID'] == 1:
                        if dialogue['responses'][-1] == 0:
                            current['loc'] = 'kitchen'
                        else:
                            dialogue['text'] = ["No? Alright."]
                            dialogue['processID'] = 0
                    elif dialogue['diaID'] == 2:
                        if dialogue['responses'][-1] == 0:
                            if not current['touched_money']:
                                new_words = ['Woah there, buddy!',
                                            'How dare you try to take me?!',
                                            'How would you feel if I took you, huh?',
                                            "Put me down now!"]
                                current['touched_money'] = True
                                dialogue['text'] += new_words
                            else:
                                new_words = ['Hey what did I say about touching me?!',
                                             'Put me down!!!']
                                dialogue['text'] += new_words
                        else:
                            dialogue['text'].append("You left the money there.")
                    elif dialogue['diaID'] == 3:
                        if dialogue['responses'][-1] == 1:
                            dialogue['text'] = []
                            dialogue['your_options'] = []
                    elif dialogue['diaID'] == -1:
                        if dialogue['responses'][-1] == 0:
                            dialogue['text'].append("Excellent")
                            current['poster'] = True
                            save(savefile, current)
                        else:
                            dialogue['text'] += ["Pathetic"]
                    elif dialogue['diaID'] == 4:
                        if dialogue['responses'][-1] == 0:
                            current['6Chips'] = True
                            dialogue['text'] += ["Yummers"]
                        else:
                            dialogue['text'] += ["Then you shall starve...", "JK"]
                    elif dialogue['diaID'] == 5:
                        if dialogue['responses'][-1] == 0:
                            current['inventory'].append("key")
                            current['got_key'] = True
                            dialogue['text'].append("You got the key.")
                    elif dialogue['diaID'] == 6:
                        if dialogue['responses'][-1] == 0:
                            setup_game(game, "TEMPE", None, {"WTR": 1})
                    dialogue['JSR'] = False
                try:
                    opt_split = dialogue['text'][dialogue['processID']]
                except IndexError:
                    dialogue['on'] = False
                    dialogue['processID'] = 0
                    opt_split = 1
                    if not dialogue['JSR']:
                        continue
                if opt_split is None:
                    dialogue['inoptions'] = True
                    continue

                box_lines = []
                temp = ''
                tall_boi = dialogue['font'].size
                dfont = dialogue['font']
                text = dialogue['text'][dialogue['processID']]
                text = text.split()
                for word in text:
                    if dfont.get_rect(f'{temp+word}').width > 660:
                        box_lines.append(temp)
                        temp = word + ' '
                    else:
                        temp += word
                        temp += ' '
                    
                if temp:
                    box_lines.append(temp)
                inde = -1
                locat = 320
                for text in box_lines:
                    dfont.render_to(screen, (70, locat), text, (0, 0, 0))
                    locat += tall_boi
                if smr.collidepoint(mouse) and clciked:
                    dialogue['processID'] += 1
                    clciked = False
            else:
                options = dialogue['your_options'][dialogue['processID']]
                if len(options) == 0:
                    dialogue['inoptions'] = False
                    dialogue['processID'] += 1
                if len(options) > 6:
                    options = options[:6]
                elif len(options) > 3:
                    opt1 = options[:3]
                    opt2 = options[3:]
                else:
                    opt1 = options
                    opt2 = None
                rec1 = pg.Rect(85, 320, 200, 50)
                rec2 = pg.Rect(295, 320, 200, 50)
                rec3 = pg.Rect(505, 320, 200, 50)
                rec4 = pg.Rect(85, 480, 200, 50)
                rec5 = pg.Rect(295, 480, 200, 50)
                rec6 = pg.Rect(505, 480, 200, 50)
                b = [rec1, rec2, rec3, rec4, rec5, rec6]
                b = b[:len(options)]
                for rec in range(len(b)):
                    pg.draw.rect(screen, (0, 0, 0), b[rec])
                    dialogue['font'].render_to(screen, (b[rec].x+5, b[rec].y+5), options[rec], (255, 255, 255))
                    if clciked and b[rec].collidepoint(mouse):
                        dialogue['responses'].append(rec)
                        dialogue['JSR'] = True
                        dialogue['processID'] += 1
                        dialogue['inoptions'] = False
                        clciked = False
        now = pg.time.get_ticks()
        if game['on']:
            FPS = process_game(game, screen, images, clciked, now, current, frame, sfx, mouse,
            pressing, savefile, FPS)
    holding = pg.mouse.get_pressed()[0]
    pg.display.flip()
    clock.tick(FPS)