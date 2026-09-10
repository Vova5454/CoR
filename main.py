import pygame as pg
import pygame.freetype as pgft
import json
import os
from time import sleep
import random
import copy
from sprites import Player, Meteor, Buff, Laser


WIDTH = 800
HEIGHT = 600
FPS = 30

pg.init()
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
                "Arcade2": pg.Rect(750, 0, 50, 600)}
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
    'intersection2': [(pg.Rect(273, 97, 213, 243), "Dummy!")], ##
    "LCPE": [(pg.Rect(161, 0, 214, 139), "BrickWall")],
    "DatCorner": [(pg.Rect(544, 136, 133, 189), "EnterGCH")], ##
    "DatCornerR": [(pg.Rect(449, 168, 113, 168), "EnterRestuarant")], ##
    "DatCornerRB": [(pg.Rect(4, 90, 371, 259), "Dumpster")], ##
    "Arcade1": [(pg.Rect(96, 153, 115, 286), "ArcadeGame1"),
                (pg.Rect(297, 143, 126, 298), "ArcadeGame2"), ##
                (pg.Rect(536, 140, 132, 307), "ArcadeGame3")] ##
}

images = {
    "start": pg.image.load('res/start.png').convert_alpha(),
    "bathroom": pg.image.load('res/bathroom.png').convert_alpha(),
    'kitchen': pg.image.load('res/kitchen.png').convert_alpha(),
    'his_place': pg.image.load('res/white.png'),
    'kitchen+b': pg.image.load('res/kitchen+b.png').convert_alpha(),
    'entry': pg.image.load('res/entry.png').convert_alpha(),
    'hall': pg.image.load('res/hall.png').convert_alpha(),
    'living_room': pg.image.load('res/living_room.png').convert_alpha(),
    "1's_room": pg.image.load("res/1's_room.png").convert_alpha(),
    "2's_room": pg.image.load("res/2's_room.png").convert_alpha(),
    "2's_room+p": pg.image.load("res/2's_room+p.png").convert_alpha(),
    "3's_room": pg.image.load("res/3's_room.png").convert_alpha(),
    "4's_room": pg.image.load("res/4's_room.png").convert_alpha(),
    "5's_room": pg.image.load("res/5's_room.png").convert_alpha(),
    "6's_room": pg.image.load("res/6's_room.png").convert_alpha(),
    "6's_room+C": pg.image.load("res/6's_room+C.png").convert_alpha(),
    "7's_room": pg.image.load("res/7's_room.png").convert_alpha(),
    "intersection1": pg.image.load("res/intersection1.png").convert_alpha(),
    "LongAlley": pg.image.load("res/LongAlley.png").convert_alpha(),
    "BehindHouse": pg.image.load("res/BehindHouse.png").convert_alpha(),
    "LefterTop": pg.image.load("res/LefterTop.png").convert_alpha(),
    "Arcade": pg.image.load("res/Arcade.png").convert_alpha(),
    "FarWall": pg.image.load("res/FarWall.png").convert_alpha(),
    "neighborhood1": pg.image.load("res/neighborhood1.png").convert_alpha(),
    "intersection2": pg.image.load("res/intersection2.png").convert_alpha(),
    "LCPE": pg.image.load('res/LCPE.png').convert_alpha(),
    "DatCorner": pg.image.load('res/DatCorner.png').convert_alpha(),
    "DatCornerR": pg.image.load('res/DatCornerR.png').convert_alpha(),
    "DatCornerRB": pg.image.load('res/DatCornerRB.png').convert_alpha(),
    "Arcade1": pg.image.load('res/Arcade1.png').convert_alpha(),
    "ppu": pg.image.load('res/ping_pong_you.png').convert_alpha(),
    "pph": pg.image.load('res/ping_pong_him.png').convert_alpha()
}

font = pg.font.Font(None, 72)
pg.mixer.init()
errortext = font.render("BG not found :(", True, (0, 0, 0))
mmmfont = pgft.Font(None, 36)

mmbuttons = [pg.Rect(300, 150*x+75, 200, 75) for x in range(4)]
mmbuttonstext = ["Start", "Load", "QUIT", "Delete"]
savefile = None
def def_dia():
    return {'on': False,
            'inoptions': False,
            'text': [],
            'your_options': [],
            'responses': [],
            'diaID': 0,
            'processID': 0,
            'JSR': False,
            'font': None,
            'name': None}
dialogue = def_dia()
mmmfont_read = -1500
filerects0 = [pg.Rect(200+150*x, 50, 100, 50) for x in range(3)]
filerects1 = [pg.Rect(200+150*x, 500, 100, 50) for x in range(3)]
filerects = filerects0 + filerects1
slick = False
default = {
    "loc": "start",
    "mus": 'home',
    'blowhornblew': 0,
    "atebanana": False,
    'touched_money': False,
    "poster": False,
    "sat_on_couch_count": 0,
    "6Chips": False,
    "Ping-Pong_high_score": 0,
    "legend": False
}

mbuttons = [pg.Rect(300, 150*x+37.5, 200, 75) for x in range(4)]
mbuttonstext = ["Back", "Save", "Main Menu", "Quit"]
mm = True
m = False
need_error = False
frames = [pg.image.load(f'res/frames/{x}.png') for x in range(10)]
def animate(frame):
    frame += 1
    if frame == 10:
        frame = 0
    return frames[frame]
strongest = frames[9]
saved = pg.mixer.Sound('res/sound/saved.mp3')
bye = pg.mixer.Sound('res/sound/bye.mp3')
deleto = False
BOOK = [["Page 1", "I am about to go to job interview.",
         "I want the position called 'CEO'. Have no idea what it is but sounds cool",
         "I really hope I get the position. I mean it's not like I have anything better to do!"],
         ["Page 2", "I got accepted as the CEO! I start work next monday",
          "That means I have a whole 2 days to do absolutely nothing!"],
          ["Page 3", "So apparently I have to build houses.", "I managed to create my first house today!",
           "It digs into the place right below the entrance to this world.",
           "I made sure that if anyone were to come to this world there would be a room for them!",
           "And if someone new were to come here I would just build another room for them!"],
           ["Page 4", "After years of working I built the entire map!",
            "I made sure to put all the important stuff like houses, a dummy, etc.",
            "You can't forget the learning center! How will the people leave this world if they can't defend themsleves?",
            "She always protects the Tower of Separation so I don't expect anyone to leave anytime soon.",
            "It's actually weird. Why doesn't she want to leave? She would put her life on the line to keep people away from there!"]]
TEXT = ["Aaron's Job Profile", "Name: Aaron", "Age: 35", "Position: CEO",
        "Company Name: GCH (Good Construction of Houses)",
        "Became CEO: 17 years ago"]
cor1 = pg.mixer.Sound('res/sound/cor1.wav')
emergency = pg.mixer.Sound('res/sound/emergency.mp3')
savem = False
current = None
framei = 0
inspired = False
ribbit = pg.mixer.Sound('res/sound/frog.mp3')

def save(savefile, data=None):
    if data is None:
        try:
            with open(savefile, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            save(savefile, default)
            return default
    with open(savefile, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

playing = {
    'home': float('-inf'),
    '1': float('-inf'),
    '2': float('-inf'),
    '3': float('-inf'),
    '4': float('-inf'),
    '5': float('-inf'),
    '6': float('-inf'),
    '7': float('-inf'),
    'CoR1': float('-inf'),
    'Arcade': float('-inf'),
    'Ping-Pong': float('-inf'),
    "Space-Invaders": float('-inf')
}

musID = {
    'home': cor1,
    '1': pg.mixer.Sound("res/sound/1s_room.mp3"),
    '2': pg.mixer.Sound("res/sound/2s_room.mp3"),
    '3': pg.mixer.Sound("res/sound/3s_room.mp3"),
    '4': pg.mixer.Sound("res/sound/4s_room.mp3"),
    '5': pg.mixer.Sound("res/sound/5s_room.mp3"),
    '6': pg.mixer.Sound("res/sound/6s_room.mp3"),
    '7': pg.mixer.Sound("res/sound/7s_room.mp3"),
    'CoR1': pg.mixer.Sound("res/sound/outside.mp3"),
    'Arcade': pg.mixer.Sound("res/sound/arcade.mp3"),
    'Ping-Pong': pg.mixer.Sound('res/sound/PingPong.mp3'),
    "Space-Invaders": pg.mixer.Sound('res/sound/SpaceInvaders.mp3')
}

def setup_dialogue(text, diaID=0, your_options=[],
                   font=pgft.SysFont(None, 36), name=None):
    cd = def_dia()
    cd['on'] = True
    cd['font'] = font
    cd['text'] = text
    cd['name'] = name
    if not diaID:
        return cd
    cd['your_options'] = your_options
    cd['diaID'] = diaID
    return cd

def setup_game(g_type, g_id, objects={}, groups={}, g_vars={}, consts={}):
    return {
        "on": True,
        "objects": objects,
        "groups": groups,
        "vars": g_vars,
        "consts": consts,
        "ID": g_id,
        "type": g_type
    }

holding = False
def def_game():
    return {
        "on": False,
        "objects": {},
        "groups": {},
        "vars": {},
        "consts": {},
        "ID": 0,
        "type": None
    }
game = def_game()
frame = 0
run = True
while run:
    frame += 1
    framei += 1
    if framei == 30:
        framei = 0
    if framei % 3 == 0:
        strongest = animate(framei//3)
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
            bye.play()
            sleep(bye.get_length())
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and not mm and not dialogue['on'] and not game['on']:
                m = {True: False, False: True}[m]
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0] and not holding:
                clciked = True
    now = pg.time.get_ticks()
    if m:
        screen.fill((25, 150, 50))
        for i in range(len(mbuttonstext)):
            pg.draw.rect(screen, (255, 127, 0), mbuttons[i])
            mmmfont.render_to(screen, (310, 150*i+75), mbuttonstext[i], (255, 255, 255))
        mouse = pg.mouse.get_pos()
        for recti in range(len(mbuttons)):
            if mbuttons[recti].collidepoint(mouse) and clciked:
                if recti == 0:
                    m = False
                elif recti == 1:
                    save(savefile, current)
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
                    bye.play()
                    sleep(bye.get_length())
                    run = False
        clciked = False
    if mm:
        screen.fill((200, 200, 200))
        for i in range(len(mmbuttonstext)):
          pg.draw.rect(screen, (0, 0, 0), mmbuttons[i])
          mmmfont.render_to(screen, (350, 150*i+100), mmbuttonstext[i], (255, 255, 255))
        mouse = pg.mouse.get_pos()
        for recti in range(len(mmbuttons)):
            if mmbuttons[recti].collidepoint(mouse) and clciked and not savem and not deleto:
                clciked = False
                # if recti == 2 and now-lastm>200:
                if recti == 2:
                    bye.play()
                    sleep(bye.get_length())
                    run = False
                elif recti == 1:
                    savem = True
                elif recti == 0:
                    mmmfont_read = now
                    
                elif recti == 3:
                    deleto = True
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
                if os.path.exists(f'saves/data{i+1}.json'):
                    file = save(f"saves/data{i+1}.json")
                    if file.get("image", False):
                        image = pg.transform.scale(pg.image.load(file['image']), filerects[i].size)
                        screen.blit(image, filerects[i].topleft)
                    elif file.get("color", False):
                        pg.draw.rect(screen, file['color'], filerects[i])
                    else:
                        pg.draw.rect(screen, (0, 255, 0), filerects[i])
                else:
                    pg.draw.rect(screen, (0, 0, 0), filerects[i])
                c1, c2 = filerects[i].center
                mmmfont.render_to(screen, (c1-10, c2-15), str(i+1), (255, 255, 255))
            for rect in range(len(filerects)):
                if filerects[rect].collidepoint(mouse) and clciked:
                    savem = False
                    savefile = f'saves/data{rect+1}.json'
                    playing['home'] = float('-inf')
                    dialogue = def_dia()
                    current = save(savefile)
                    if current == {}:
                        save(savefile, default)
                        current = default
                    if os.path.exists(savefile) and os.path.getsize(savefile) == 0:
                        save(savefile, default)
                        current = default
                    mm = False
                    inspired = False
                    clciked = False
        if deleto:
            screen.fill((110, 20, 20))
            for i in range(len(filerects)):
                if os.path.exists(f'saves/data{i+1}.json'):
                    pg.draw.rect(screen, (0, 255, 0), filerects[i])
                else:
                    pg.draw.rect(screen, (0, 0, 0), filerects[i])
                c1, c2 = filerects[i].center
                mmmfont.render_to(screen, (c1-10, c2-15), str(i+1), (255, 255, 255))
            for rect in range(len(filerects)):
                if filerects[rect].collidepoint(mouse) and clciked:
                    clciked = False
                    savem = False
                    if os.path.exists(f'saves/data{rect+1}.json'):
                        os.remove(f'saves/data{rect+1}.json')
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
        elif current['loc'] in ["intersection1", "Arcade"]:
            current['mus'] = 'CoR1'
        elif current['loc'] == "Arcade1" and not game['on']:
            current['mus'] = 'Arcade'
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
                musID[current['mus']].play()
                playing[current['mus']] = now
        if current['loc'] in interactions and not dialogue['on'] and not game['on']:
            for ntc, interaction in interactions[current['loc']]:
                if ntc.collidepoint(mouse) and clciked:
                    if interaction == 'blowhorn':
                        current['blowhornblew'] = current.get('blowhornblew', 0) + 1
                        emergency.play()
                        playing['home'] = now+emergency.get_length()*1000-musID[current['mus']].get_length()*1000
                        cor1.stop()
                    elif interaction == 'talk_to_him':
                        current['loc'] = 'his_place'
                        dialogue['on'] = True
                        dialogue['font'] = pgft.SysFont("Papyrus", 36)
                        dialogue['text'] = ['Hey there! I am the strongest one here!',
                                                            "...",
                                                            "I can't find anything interesting in you.",
                                                            "Leave",
                                                            None]
                        dialogue['your_options'] = [None, None, None, None, ['Yes', 'No']]
                        dialogue['diaID'] = 1
                        dialogue['processID'] = 0
                        dialogue['JSR'] = False
                        dialogue['inoptions'] = False
                        dialogue['name'] = "???"
                        save(savefile, current)
                    elif interaction == 'eat_banana' and not current['atebanana']:
                        current['atebanana'] = True
                        dialogue['on'] = True
                        dialogue['font'] = pgft.SysFont('Cooper Black', 36)
                        dialogue['processID'] = 0
                        dialogue['text'] = ['You ate the banana',
                                                            'You feel full.']
                    elif interaction == 'leave':
                        current['loc'] = 'intersection1'
                    elif interaction == 'view_hubert':
                        ribbit.play()
                        musID[current['mus']].stop()
                        playing[current['mus']] = now-musID[current['mus']].get_length()*1000+ribbit.get_length()*1000
                    elif interaction == 'steal_money':
                        dialogue['on'] = True
                        dialogue['font'] = pgft.SysFont('Cooper Black', 36)
                        dialogue['processID'] = 0
                        dialogue['diaID'] = 2
                        dialogue['text'] = [
                            'Take the money?', None
                        ]
                        dialogue['your_options'] = [None, ["*Take*", "*Leave*"]]
                    elif interaction == 'view_him':
                        dialogue['on'] = True
                        dialogue['font'] = pgft.SysFont("Papyrus", 36)
                        dialogue['processID'] = 0
                        dialogue['text'] = [
                            "What a beautiful masterpiece!"
                        ]
                    elif interaction == 'read_book':
                        dialogue['on'] = True
                        dialogue['font'] = pgft.SysFont(None, 36)
                        dialogue['diaID'] = 3
                        dialogue['text'] = ["Read the book?", None]
                        dialogue['processID'] = 0
                        dialogue['your_options'] = [None, ["Yes", "No"]]
                        for page in BOOK:
                            for paragraph in page:
                                dialogue['text'].append(paragraph)
                                dialogue['your_options'].append(None)
                            dialogue['text'].append(None)
                            dialogue['your_options'].append([
                                "Proceed",
                                "Close Book"
                            ])
                        dialogue['your_options'][-1][0] = "Close Book"
                    elif interaction == 'read_note':
                        dialogue['on'] = True
                        dialogue['font'] = pgft.SysFont(None, 24)
                        dialogue['text'] = TEXT
                    elif interaction == '2VIhotel':
                        dialogue = setup_dialogue([
                            "It's a poster that says 'hotel'",
                            "The one who put it up is planning to build a hotel!",
                            'Why?',
                            "I don't know. Ask her."],
                            font=pgft.SysFont('Cooper Black', 24))
                    elif interaction == '2VIarcade':
                        dialogue = setup_dialogue([
                            "The one who put up this poster wants to build an arcade!",
                            "The way it's drawn is weird... Once someone enters the arcade they change way.",
                            "Just ask the person who put it up for further details. I'm just a poster, I don't know everything!"
                        ], font=pgft.SysFont('Cooper Black', 24))
                    elif interaction == '2VIzoo':
                        dialogue = setup_dialogue([
                            "A zoo! The person who put me up wants to make a zoo!",
                            "I really wish I could go to zoos but I'm just a poster who's being hung for eternity...",
                            "You're not bound by any glue or frame so explore the world to your fullest desires!"
                        ], font=pgft.SysFont('Cooper Black', 36))
                        inspired = True
                    elif interaction == '2VIrmaze':
                        dialogue = setup_dialogue([
                            "A rotating maze huh? It looks cool doesn't it!",
                            "So I guess every few moments your position and the maze changes.",
                            "It will be hard to get past that! Wish you good luck!",
                            "Actually, the poster close to me might know how to get past!"
                        ], font=pgft.SysFont("Cooper Black", 36))
                    elif interaction == '2VIguardpos' and not current['poster']:
                        if not inspired:
                            dialogue = setup_dialogue(
                                ["This is a position for guards. So they line up in some position",
                                "She sure seems to want to protect something.",
                                "What if I told you I can help you if you help me?",
                                "Take me with you to see the world. A poster has no legs but you do!",
                                None], -1, [None, None, None, None,
                                            ['Take It', "Refusal"]], pgft.SysFont("Comic Sans", 36), "Poster"
                            )
                        else:
                            dialogue = setup_dialogue([
                                "'You are not bound by any glue or frame so explore the world to your fullest desires'",
                                "We posters aren't free to roam wherever we want. BUT YOU ARE",
                                "Ever since my very production that was my dream.",
                                "I hold knowledge you would risk your life for. TAKE. ME. WITH. YOU",
                                None
                            ], -1, [None, None, None, None,
                                    ["Take", "Refusal"]], pgft.SysFont("Chiller", 64), "Poster")
                    elif interaction == '2VIlandmine':
                        dialogue = setup_dialogue([
                            'It is a landmine. I have no idea how you are supposed to go past.',
                            "Good luck, I guess..."
                        ], font=pgft.SysFont('Cooper Black', 36))
                    elif interaction == '3TV':
                        dialogue = setup_dialogue([
                            "It's a TV!", "... ... ...",
                            "It doesn't work. Of course."
                        ], font=pgft.SysFont("Eras Medium ITC", 32))
                    elif interaction == '3Couch':
                        dialogue = setup_dialogue([
                            "What a wonderful couch!", "It feels very nice.",
                            "You sat on the couch.", "Nice."
                        ], font=pgft.SysFont("Eras Medium ITC", 28))
                        current['sat_on_couch_count'] += 1
                    elif interaction == "3Candles":
                        dialogue = setup_dialogue([
                            "The candles are very warm.",
                            "The room feels very nice because of that."
                        ], font=pgft.SysFont("Eras Medium ITC", 28))
                    elif interaction == '3Chandelier':
                        dialogue = setup_dialogue([
                            "The chandelier feels nice.",
                            "Thank the chandelier for giving you light."
                        ], font=pgft.SysFont("Eras Medium ITC", 36))
                    elif interaction == '3':
                        dialogue = setup_dialogue([
                            "This is a real masterpiece.",
                            "I wonder who it is though.",
                            "Don't worry you'll meet him soon enough!"
                        ], font=pgft.SysFont("Eras Medium ITC", 36))
                    elif interaction == '3Mattress':
                        dialogue = setup_dialogue([
                            "A super comfy mattress!"
                        ], font=pgft.SysFont("Eras Medium ITC", 36))
                    elif interaction == '4HA':
                        dialogue = setup_dialogue([
                            "It's a picture of a human with a bright aura around him.",
                            "In this world every human has an aura which is their spiritual power/soul.",
                            "You use it when you engage in battle and don't punch others but fight with spiritual power.",
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4Fatass':
                        dialogue = setup_dialogue([
                            "When I was in the house I found some guy who calls himself 'the strongest'",
                            "The weird thing about him is his soul flashes 10 different colors.",
                            "A soul can only flash a single color. The color's meaning is something I still don't understand",
                            "So is it that he's a weirdo or he has 10 souls? I don't know, tbh."
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '410':
                        dialogue = setup_dialogue([
                            "So I suppose that the weirdo actually has 10 souls. But how did he obtain? I didn't even knew that was possible!",
                            "My best guess is that he killed some people. This means 13 people have ever come down here.",
                            "But only 3 people are here right now, so does everyone who comes here gets eaten by him? Sure hope not..."
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4Dead':
                        dialogue = setup_dialogue([
                            "I learned that when a person dies here sometimes they can leave their soul behind."
                            "Sometimes however, their soul dies as well. Even rarer, sometimes the body dies but the soul doesn't.",
                            "This means if you die you can have a chance of becoming a ghost. I'm not sure of there are ghosts around here...",
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4Eat':
                        dialogue = setup_dialogue([
                            "When a person dies and leave their soul behind, someone else may try to consume it.",
                            "I'm not sure how a soul is consumed though.",
                            "This is probably the way that weirdo got the 10 souls. His name is Hubert btw"
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4ToS':
                        dialogue = setup_dialogue([
                            "This world is actually super weird. Apparently there is a tower called the Tower of Separation.",
                            "Hubert claimed it's the only way to leave this world. At the edge of this world is a wall.",
                            "Even Hubert said he doesn't know what's past the wall!"
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4Exit':
                        dialogue = setup_dialogue([
                            "In the Tower of Separation is a platform which is supposed to make you leave this world.",
                            "Hubert said that I can leave if I wanted to.",
                            "I'm not planning on leaving this world anytime soon. Tha platform itself seems weird!",
                            "On it is something supposed to resemble the sun."
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4NoExit':
                        dialogue = setup_dialogue([
                            "I wonder what will happen when I leave this world.",
                            "Hubert says nothing. Hubert stopped smiling.",
                            "He's weird. But I'm not sure if that platform is safe at all.",
                            "Maybe that is the way he kills others.",
                            "I know if I dare challenge him I will have no chance at winning.",
                            "The best thing I can do is to stop anyone from leaving."
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '4LongText':
                        dialogue = setup_dialogue([
                            "Short summary, I think Hubert kills people for their souls.",
                            "He guides them to the Tower of Separation and waits for them to 'exit the world'"
                        ], font=pgft.SysFont("Baskerville Old Face", 36))
                    elif interaction == '5HUBERT':
                        dialogue = setup_dialogue([
                            "It's hubert. The painting is colorful."
                        ])
                    elif interaction == "5L":
                        dialogue = setup_dialogue([
                            "Paintings."
                        ])
                    elif interaction == '5R':
                        dialogue = setup_dialogue(["These paintings don't look detailed."])
                    elif interaction == "Lay's Chips #6" and not current['6Chips']:
                        dialogue = setup_dialogue([
                            "It's a bag that says Lay'd.", "Eat them?", None,
                        ],
                            4, [None, None, ["Eat", "Refusal"]], pgft.SysFont("Cooper Black", 36)
                        )
                    elif interaction == '6SpiderWeb':
                        dialogue = setup_dialogue([
                            "It's a spider web.", "Someone doesn't clean their room"
                        ], font=pgft.SysFont("Cooper Black", 36))
                    elif interaction == '7':
                        dialogue = setup_dialogue(["Empty"])
                    elif interaction == 'HELP!':
                        dialogue = setup_dialogue(["There's a wall far away"],
                                                  font=pgft.SysFont("Cooper Black", 36))
                    elif interaction == 'Arcade':
                        current['loc'] = 'Arcade1'
                    elif interaction == "1's_house":
                        print("Yo this is unfinished.")
                        ## Unfinished
                    elif interaction == "Dummy!":
                        print("This dummy ain't completed.")
                        ## Unfinished
                    elif interaction == "BrickWall":
                        dialogue = setup_dialogue(["It's a brick wall!"])
                    elif interaction == 'ArcadeGame1':
                        current['mus'] = "Ping-Pong"
                        game['on'] = True
                        game["type"] = "ArcadeGame"
                        game['objects'] = {
                            "ball": pg.Rect(388, 288, 24, 24),
                            "player": pg.Rect(30, 225, 15, 150),
                            "clanker": pg.Rect(755, 250, 45, 100)
                        }
                        game["consts"] = {"player_speed": 12, "frame": frame, "clanker_speed": 3}
                        minb, maxb = 5, 5
                        game["vars"] = {"dx": None, "dy": None,
                                        "pscore": 0, "cscore": 0,
                                        "on": False}
                        game["ID"] = 1
                    elif interaction == "ArcadeGame2":
                        game = setup_game("ArcadeGame", 2,
                                          {"player": Player("res/space_invaders_you.png"), "laser": Laser()},
                                          {"meteor": pg.sprite.Group(), "buff": pg.sprite.Group()},
                                          {"meteors_killed": 0, "start": False, "mst": 0, "bst": 0, "sas": 0, "pp": None},
                                          {"meteor_st": 250, "buff_st": 2500})
                        mx, my = 3, 10
                        current['mus'] = 'Space-Invaders'
                        survived = False
                    clciked = False
        if current['loc'] in ['kitchen', 'his_place']:
            if current['loc'] == 'kitchen':
                screen.blit(strongest, (107, 360))
            else:
                screen.blit(strongest, (300, 200))
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
                tall_boi = dialogue['font'].get_rect('()').height
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
        keys = pg.key.get_pressed()
        if game['on']:
            if game['ID'] == 0:
                game = def_game()
            elif game['type'] == 'ArcadeGame':
                pg.draw.rect(screen, (0, 0, 0), pg.Rect(5, 5, 790, 590))
                if game['ID'] == 1:
                    if game['vars']['on']:
                        pg.draw.ellipse(screen, (255, 255, 255), game['objects']['ball'])
                        pg.draw.rect(screen, (255, 255, 0), game["objects"]['player'])
                        screen.blit(images['ppu'], game['objects']['player'].topleft)
                        ball = game['objects']['ball']
                        # pg.draw.rect(screen, (255, 10, 10), game['objects']['clanker'])
                        screen.blit(images['pph'], game['objects']['clanker'].topleft)
                        mmmfont.render_to(screen, (10, 10), str(game['vars']['pscore']), (255, 255, 255))
                        mmmfont.render_to(screen, (773, 10), str(game['vars']['cscore']), (255, 255, 255))
                        if not game["vars"]['dx']:
                            dx = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                            dy = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                            game['vars']['dx'], game["vars"]["dy"] = dx, dy
                        if keys[pg.K_UP] or keys[pg.K_w]:
                            game['objects']['player'].y -= game['consts']['player_speed']
                        if keys[pg.K_DOWN] or keys[pg.K_s]:
                            game["objects"]['player'].y += game['consts']['player_speed']
                        if game["objects"]['player'].top < 5:
                            game["objects"]['player'].top = 5
                        if game['objects']['player'].bottom > 595:
                            game["objects"]['player'].bottom = 595
                        ball.x += game['vars']['dx']
                        ball.y += game['vars']['dy']
                        if ball.top < 5 or ball.bottom > 595:
                            game['vars']['dy'] *= -1
                        if ball.left < 5 and game['vars']['dx'] < 0:
                            game['vars']['cscore'] += 1
                            ball = pg.Rect(388, 288, 24, 24)
                            dx = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                            dy = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                            game['vars']['dx'], game['vars']['dy'] = dx, dy
                        if ball.right > 795:
                            game['vars']['pscore'] += 1
                            ball = pg.Rect(388, 288, 24, 24)
                            dx = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                            dy = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                            game['vars']['dx'], game['vars']['dy'] = dx, dy
                        balle = copy.copy(game['objects']['ball'])
                        dx, dy = copy.copy(game['vars']['dx']), copy.copy(game['vars']['dy'])
                        while balle.right < 755:
                            balle.x += dx
                            balle.y += dy
                            if (balle.top < 5 and dy < 0) or (balle.bottom > 595 and dy > 0):
                                dy = -dy
                            if balle.left < 45 and dx < 0:
                                dx = -dx
                        collided = False
                        # if not game['objects']['clanker'].colliderect(ball):
                        if game['objects']['clanker'].center[1] > balle.center[1]:
                            game['objects']['clanker'].y -= game['consts']['clanker_speed']
                        if game['objects']['clanker'].center[1] < balle.center[1]:
                            game['objects']['clanker'].y += game['consts']['clanker_speed']
                        protective_layer = pg.Rect(15, game['objects']['player'].top, 15, 150)
                        protective_layer2 = pg.Rect(5, protective_layer.top, 10, 150)
                        # pg.draw.rect(screen, (127, 0, 255), protective_layer)
                        # pg.draw.rect(screen, (127, 127, 255), protective_layer2)
                        if (ball.colliderect(game['objects']['player'])
                            or ball.colliderect(
                                protective_layer)
                                or ball.colliderect(protective_layer2)) and game['vars']['dx'] < 0:
                            if game['objects']['ball'].top+12 > game[
                                'objects']['player'].top and ball.bottom < game['objects']['player'].bottom+12:
                                game['vars']['dx'] *= -1
                                collided = True
                        if ball.colliderect(game['objects']['clanker']) and game['vars']['dx'] > 0:
                            # if game['objects']['ball'].top+12 > game['objects']['clanker'].top and game[
                            #     "objects"
                            # ]['ball'].bottom < game['objects']['clanker'].bottom+12:
                            game['vars']['dx'] *= -1
                            collided = True
                        if game['vars']['pscore'] >= 10 or game['vars']['cscore'] >= 10:
                            current["Ping-Pong_high_score"] = max(current["Ping-Pong_high_score"], game['vars']['pscore'])
                            game['on'] = False
                        if keys[pg.K_ESCAPE]:
                            game['on'] = False
                        if collided:
                            game['vars']['dx'] += (game['vars']['dx']/abs(game['vars']['dx'])) * random.randint(0, 1)
                            game['vars']['dy'] += (game['vars']['dy']/abs(game['vars']['dy'])) * random.randint(0, 1)
                    else:
                        mmmfont.render_to(screen, (10, 10), "ESC means exit. Get to 10 points. Click to start", (255, 255, 255))
                        mmmfont.render_to(screen, (10, 60), "You lose if the computer gets to 10 points.", (255, 255, 255))
                        if clciked:
                            game['vars']['on'] = True
                elif game['ID'] == 2:
                    if game['vars']['start']:
                        if not survived:
                            spcttd = 1
                            game['vars']['sas'] += 1
                            game['groups']['meteor'].update()
                            game['groups']['buff'].update()
                            game['objects']['player'].move()
                            game['objects']['laser'].move()
                            game['objects']['player'].draw(screen)
                            game['objects']['laser'].draw(screen)
                            mmmfont.render_to(screen, (790-mmmfont.get_rect(str(game[
                                'objects']['player'].hp)).width, 10),
                                str(game['objects']['player'].hp), (255, 255, 255))
                            mmmfont.render_to(screen, (10, 10), str(game['vars']['meteors_killed']).zfill(3), (255, 255, 255))
                            game['groups']['buff'].draw(screen)
                            game['groups']['meteor'].draw(screen)
                            player = game['objects']['player']
                            buffs = game['groups']['buff']
                            meteors = game['groups']['meteor']
                            laser = game['objects']['laser']
                            if game['vars']['meteors_killed'] == 10:
                                player.speed = 6
                                mx, my = 5, 12
                                spcttd = 1.1
                                game['consts']['meteor_st'] = 245
                                game['consts']['buff_st'] = 2550
                                
                            if game['vars']['meteors_killed'] == 20:
                                player.speed = 7
                                mx, my = 6, 15
                                spcttd = 1.25
                                game['consts']['meteor_st'] = 215
                                game['consts']['buff_st'] = 2600
                            if game['vars']['meteors_killed'] == 40:
                                player.speed = 8
                                mx, my = 10, 16
                                spcttd = 1.5
                                game['consts']['meteor_st'] = 180
                                game['consts']['buff_st'] = 2700
                            if game['vars']['meteors_killed'] == 60:
                                player.speed = 10
                                spcttd = 2
                                mx, my = 15, 20
                                game['consts']['meteor_st'] = 150
                                game['consts']['buff_st'] = 3000
                            if game['vars']['meteors_killed'] == 80:
                                player.speed = 12
                                spcttd = 2.5
                                mx, my = 20, 40
                                game['consts']['meteor_st'] = 75
                                game['consts']['buff_st'] = 3500
                            if game['vars']['meteors_killed'] == 115:
                                player.speed = 14
                                spcttd = 3
                                mx, my = 30, 40
                                game['consts']['meteor_st'] = 65
                                game['consts']['buff_st'] = 3600
                            if game['vars']['meteors_killed'] == 150:
                                player.speed = 15
                                spcttd = 3.25
                                mx, my = 40, 45
                                game['consts']['meteor_st'] = 60
                                game['consts']['buff_st'] = 3750
                            if game['vars']['meteors_killed'] == 200:
                                player.speed = 17.5
                                spcttd = 3.5
                                mx, my = 45, 50
                                game['consts']['meteor_st'] = 55
                                game['consts']['buff_st'] = 3800
                            if game['vars']['meteors_killed'] == 300:
                                player.speed = 18
                                spcttd = 4
                                mx, my = 50, 60
                                game['consts']['meteor_st'] = 50
                                game['consts']['buff_st'] = 4000
                            if game['vars']['meteors_killed'] == 500:
                                player.speed = 20
                                spcttd = 5
                                mx, my = 55, 75
                                game['consts']['meteor_st'] = 40
                                game['consts']['buff_st'] = 4500
                            if game['vars']['meteors_killed'] == 750:
                                player.speed = 25
                                spcttd = 7.5
                                mx, my = 80, 100
                                game['consts']['meteor_st'] = 30
                                game['consts']['buff_st'] = 5000
                            if game['vars']['meteors_killed'] == 950:
                                player.speed = 6
                                spcttd = 8
                                mx, my = 5, 10
                                game['consts']['meteor_st'] = 250
                                game['consts']['buff_st'] = 250

                            if abs((game['vars']['sas']-435)//spcttd) < 5:
                                ppy = random.randint(15, 585)
                                ppx = random.randint(15, 785)
                                pos = random.choice(["x", "y"])
                                if pos == "x":
                                    sarect = pg.Rect(5, ppy-20, 790, 40)
                                else:
                                    sarect = pg.Rect(ppx-20, 5, 40, 590)
                                pg.draw.rect(screen, (255, 0, 0), sarect)
                            elif game['vars']['sas'] >= 450//spcttd and sarect is not None:
                                game['vars']['sas'] = 0
                                if player.rect.colliderect(sarect):
                                    for _ in range(75):
                                        if player.damage():
                                            game['on'] = False
                                    if game['on']:
                                        survived = True
                                        ssa = False
                                        spcframe = now
                                        mmmfont.render_to(screen, (10, 100), "You survived attack!")
                                    else:
                                        screen.fill((255, 255, 0))
                                        pg.display.flip()
                            elif game['vars']['sas'] < 432//spcttd:
                                sarect = None
                                player.boost = 1.5
                            if sarect:
                                pg.draw.rect(screen, (255, 0, 0), sarect)
                                player.boost = 2
                            if now - game['vars']['mst'] >= game['consts']['meteor_st']:
                                mimages = ["res/space_invaders_meteor.png", "res/space_invaders_meteor2.png", "res/space_invaders_meteor3.png"]
                                abc = Meteor(random.choice(mimages), mx, my)
                                if now - player.useless['trees'] <= 5000:
                                    abc.speedx /= 2
                                    abc.speedy /= 2
                                game['vars']['mst'] = now
                                meteors.add(abc)
                            if now - player.useless['trees'] >= 5000:
                                player.useless['trees'] = float('inf')
                                for meteor in meteors:
                                    meteor.speedx *= 2
                                    meteor.speedy *= 2
                            if now - game['vars']['bst'] >= game['consts']['buff_st']:
                                bt = random.choice([("medkit", "res/space_invaders_medkit.png"),
                                                    ("lightning", "res/space_invaders_lightning.png"),
                                                    ("time", "res/space_invaders_clock.png")])
                                game['vars']['bst'] = now
                                buffs.add(Buff(bt))
                            ml = pg.sprite.spritecollideany(laser, meteors)
                            if ml:
                                ml.kill()
                                game['vars']['meteors_killed'] += 1
                                laser.delete()
                            mp = pg.sprite.spritecollideany(player, meteors)
                            if mp:
                                mp.kill()
                                if player.damage():
                                    game['on'] = False
                                    screen.fill((255, 0, 0))
                                    pg.display.flip()
                            bp = pg.sprite.spritecollideany(player, buffs)
                            if bp:
                                bp.kill()
                                if bp.type == "medkit":
                                    player.hp += 1
                                elif bp.type == "lightning":
                                    player.useless['glue'] = now
                                    laser.lightning()
                                elif bp.type == "time":
                                    player.useless["trees"] = now
                                    for meteor in meteors:
                                        meteor.speedx /= 2
                                        meteor.speedy /= 2
                            if now - player.useless['glue'] >= 5000:
                                player.useless['glue'] = float('inf')
                                laser.unlightning()
                            if clciked or keys[pg.K_RETURN] or keys[pg.K_z]:
                                laser.create("res/space_invaders_laser.png", player.rect.center)
                            if pg.key.get_pressed()[pg.K_ESCAPE]:
                                game['on'] = False
                            if game['vars']['meteors_killed'] >= 1000:
                                survived = True
                                spcframe = now
                                ssa = True
                        else:
                            if now - spcframe > 2000:
                                survived = False
                                game['on'] = False
                            else:
                                if not ssa:
                                    mmmfont.render_to(screen, (10, 100), "You survived the special attack!", (255, 0, 0))
                                else:
                                    mmmfont.render_to(screen, (10, 100), "YOU'RE A LEGEND!!! Save right now!", (255, 255, 0))
                                    current['legend'] = True

                    else:
                        mmmfont.render_to(screen, (15, 15), "Destroy 1000 meteors or survive a special", (255, 255, 255))
                        mmmfont.render_to(screen, (15, 65), "attack. You would need 75 HP for that!", (255, 255, 255))
                        mmmfont.render_to(screen, (15, 115), "Click to start.", (255, 255, 255))
                        mmmfont.render_to(screen, (15, 165), "Click to shoot, Z or Enter to keep shooting.", (255, 255, 255))
                        if clciked:
                            game['vars']['start'] = True
                        
                        
    holding = pg.mouse.get_pressed()[0]
    pg.display.flip()
    clock.tick(FPS)