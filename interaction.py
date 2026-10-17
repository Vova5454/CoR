import pygame as pg
import pygame.freetype as pgft
import random
from sprites import Laser, Player
from consts import TEXT, BOOK, file_thing
from func import save, setup_dialogue, setup_game


pgft.init()
pg.mixer.init()

emergency = pg.mixer.Sound(file_thing('res/sound/emergency.mp3'))
ribbit = pg.mixer.Sound(file_thing('res/sound/frog.mp3'))

def process_interactions(interaction, current, sfx, now, musID, playing, savefile, frame,
    FPS, game, dialogue, inspired, samp):
    if interaction == 'blowhorn':
        current['blowhornblew'] = current.get('blowhornblew', 0) + 1
        emergency.set_volume(sfx)
        for _ in range(samp): emergency.play()
        playing['home'] = now+emergency.get_length()*1000-musID[current['mus']].get_length()*1000
        musID['home'].stop()
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
        ribbit.set_volume(sfx)
        for _ in range(samp): ribbit.play()
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
        setup_dialogue(dialogue, [
            "It's a poster that says 'hotel'",
            "The one who put it up is planning to build a hotel!",
            'Why?',
            "I don't know. Ask her."],
            font=pgft.SysFont('Cooper Black', 24))
    elif interaction == '2VIarcade':
        setup_dialogue(dialogue, [
            "The one who put up this poster wants to build an arcade!",
            "The way it's drawn is weird... Once someone enters the arcade they change way.",
            "Just ask the person who put it up for further details. I'm just a poster, I don't know everything!"
        ], font=pgft.SysFont('Cooper Black', 24))
    elif interaction == '2VIzoo':
        setup_dialogue(dialogue, [
            "A zoo! The person who put me up wants to make a zoo!",
            "I really wish I could go to zoos but I'm just a poster who's being hung for eternity...",
            "You're not bound by any glue or frame so explore the world to your fullest desires!"
        ], font=pgft.SysFont('Cooper Black', 36))
        inspired.append(0)
    elif interaction == '2VIrmaze':
        setup_dialogue(dialogue, [
            "A rotating maze huh? It looks cool doesn't it!",
            "So I guess every few moments your position and the maze changes.",
            "It will be hard to get past that! Wish you good luck!",
            "Actually, the poster close to me might know how to get past!"
        ], font=pgft.SysFont("Cooper Black", 36))
    elif interaction == '2VIguardpos' and not current['poster']:
        if not inspired:
            setup_dialogue(dialogue,
                ["This is a position for guards. So they line up in some position",
                "She sure seems to want to protect something.",
                "What if I told you I can help you if you help me?",
                "Take me with you to see the world. A poster has no legs but you do!",
                None], -1, [None, None, None, None,
                            ['Take It', "Refusal"]], pgft.SysFont("Comic Sans", 36), "Poster"
            )
        else:
            setup_dialogue(dialogue, [
                "'You are not bound by any glue or frame so explore the world to your fullest desires'",
                "We posters aren't free to roam wherever we want. BUT YOU ARE",
                "Ever since my very production that was my dream.",
                "I hold knowledge you would risk your life for. TAKE. ME. WITH. YOU",
                None
            ], -1, [None, None, None, None,
                    ["Take", "Refusal"]], pgft.SysFont("Chiller", 64), "Poster")
    elif interaction == '2VIlandmine':
        setup_dialogue(dialogue, [
            'It is a landmine. I have no idea how you are supposed to go past.',
            "Good luck, I guess..."
        ], font=pgft.SysFont('Cooper Black', 36))
    elif interaction == '3TV':
        setup_dialogue(dialogue, [
            "It's a TV!", "... ... ...",
            "It doesn't work. Of course."
        ], font=pgft.SysFont("Eras Medium ITC", 32))
    elif interaction == '3Couch':
        setup_dialogue(dialogue, [
            "What a wonderful couch!", "It feels very nice.",
            "You sat on the couch.", "Nice."
        ], font=pgft.SysFont("Eras Medium ITC", 28))
        current['sat_on_couch_count'] += 1
    elif interaction == "3Candles":
        setup_dialogue(dialogue, [
            "The candles are very warm.",
            "The room feels very nice because of that."
        ], font=pgft.SysFont("Eras Medium ITC", 28))
    elif interaction == '3Chandelier':
        setup_dialogue(dialogue, [
            "The chandelier feels nice.",
            "Thank the chandelier for giving you light."
        ], font=pgft.SysFont("Eras Medium ITC", 36))
    elif interaction == '3':
        setup_dialogue(dialogue, [
            "This is a real masterpiece.",
            "I wonder who it is though.",
            "Don't worry you'll meet him soon enough!"
        ], font=pgft.SysFont("Eras Medium ITC", 36))
    elif interaction == '3Mattress':
        setup_dialogue(dialogue, [
            "A super comfy mattress!"
        ], font=pgft.SysFont("Eras Medium ITC", 36))
    elif interaction == '4HA':
        setup_dialogue(dialogue, [
            "It's a picture of a human with a bright aura around him.",
            "In this world every human has an aura which is their spiritual power/soul.",
            "You use it when you engage in battle and don't punch others but fight with spiritual power.",
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4Fatass':
        setup_dialogue(dialogue, [
            "When I was in the house I found some guy who calls himself 'the strongest'",
            "The weird thing about him is his soul flashes 10 different colors.",
            "A soul can only flash a single color. The color's meaning is something I still don't understand",
            "So is it that he's a weirdo or he has 10 souls? I don't know, tbh."
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '410':
        setup_dialogue(dialogue, [
            "So I suppose that the weirdo actually has 10 souls. But how did he obtain? I didn't even knew that was possible!",
            "My best guess is that he killed some people. This means 13 people have ever come down here.",
            "But only 3 people are here right now, so does everyone who comes here gets eaten by him? Sure hope not..."
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4Dead':
        setup_dialogue(dialogue, [
            "I learned that when a person dies here sometimes they can leave their soul behind."
            "Sometimes however, their soul dies as well. Even rarer, sometimes the body dies but the soul doesn't.",
            "This means if you die you can have a chance of becoming a ghost. I'm not sure of there are ghosts around here...",
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4Eat':
        setup_dialogue(dialogue, [
            "When a person dies and leave their soul behind, someone else may try to consume it.",
            "I'm not sure how a soul is consumed though.",
            "This is probably the way that weirdo got the 10 souls. His name is Hubert btw"
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4ToS':
        setup_dialogue(dialogue, [
            "This world is actually super weird. Apparently there is a tower called the Tower of Separation.",
            "Hubert claimed it's the only way to leave this world. At the edge of this world is a wall.",
            "Even Hubert said he doesn't know what's past the wall!"
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4Exit':
        setup_dialogue(dialogue, [
            "In the Tower of Separation is a platform which is supposed to make you leave this world.",
            "Hubert said that I can leave if I wanted to.",
            "I'm not planning on leaving this world anytime soon. Tha platform itself seems weird!",
            "On it is something supposed to resemble the sun."
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4NoExit':
        setup_dialogue(dialogue, [
            "I wonder what will happen when I leave this world.",
            "Hubert says nothing. Hubert stopped smiling.",
            "He's weird. But I'm not sure if that platform is safe at all.",
            "Maybe that is the way he kills others.",
            "I know if I dare challenge him I will have no chance at winning.",
            "The best thing I can do is to stop anyone from leaving."
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '4LongText':
        setup_dialogue(dialogue, [
            "Short summary, I think Hubert kills people for their souls.",
            "He guides them to the Tower of Separation and waits for them to 'exit the world'"
        ], font=pgft.SysFont("Baskerville Old Face", 36))
    elif interaction == '5HUBERT':
        setup_dialogue(dialogue, [
            "It's Hubert. The painting is colorful."
        ])
    elif interaction == "5L":
        setup_dialogue(dialogue, [
            "Paintings."
        ])
    elif interaction == '5R':
        setup_dialogue(dialogue, ["These paintings don't look detailed."])
    elif interaction == "Lay's Chips #6" and not current['6Chips']:
        setup_dialogue(dialogue, [
            "It's a bag that says Lay'd.", "Eat them?", None,
        ],
            4, [None, None, ["Eat", "Refusal"]], pgft.SysFont("Cooper Black", 36)
        )
    elif interaction == '6SpiderWeb':
        setup_dialogue(dialogue, [
            "It's a spider web.", "Someone doesn't clean their room"
        ], font=pgft.SysFont("Cooper Black", 36))
    elif interaction == '7':
        setup_dialogue(dialogue, ["Empty"])
    elif interaction == 'HELP!':
        setup_dialogue(dialogue, ["There's a wall far away"],
                                    font=pgft.SysFont("Cooper Black", 36))
    elif interaction == 'Arcade':
        current['loc'] = 'Arcade1'
    elif interaction == "1's_house":
        print("Yo this is unfinished.")
        ## Unfinished
    elif interaction == "Dummy!":
        setup_game(game, "Dummy!", -1,
                            {"you": pg.Rect(380, 280, 40, 40)},
                            {"enemy": pg.sprite.Group()},
                            {"read": False, "on": False, 'mso': None},
                            {"player_speed": 12})
    elif interaction == "BrickWall":
        setup_dialogue(dialogue, ["It's a brick wall!"])
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
        game["vars"] = {"dx": None, "dy": None,
                        "pscore": 0, "cscore": 0,
                        "on": False}
        game["ID"] = 1
    elif interaction == "ArcadeGame2":
        setup_game(game, "ArcadeGame", 2,
                            {"player": Player("res/space_invaders_you.png"), "laser": Laser()},
                            {"meteor": pg.sprite.Group(), "buff": pg.sprite.Group()},
                            {"meteors_killed": 0, "start": False, "mst": 0, "bst": 0,
                             "sas": 0, "pp": None, 'mx': 3, 'my': 10, 'survived': False},
                            {"meteor_st": 250, "buff_st": 2500})  
        current['mus'] = 'Space-Invaders'
    elif interaction == "ArcadeGame3":
        dx, dy = random.choice([1, -1]), random.choice([1, -1])
        setup_game(game, "ArcadeGame", 3,
                            {"player": pg.Rect(30, 225, 15, 150), "ball": pg.Rect(388, 288, 24, 24)},
                            {},
                            {"hits": 0, "dx": 5*dx, "dy": 5*dy, "lives": 3, "on": False,
                             'spcat': False},
                            {"player_speed": 9})
        current['mus'] = "PingPongWV"
    elif interaction == "ArcadeGame4":
        spcd = {"a": pg.K_a,"b": pg.K_b,"c": pg.K_c,"d": pg.K_d,"e": pg.K_e,
                "f": pg.K_f,"g": pg.K_g,"h": pg.K_h,"i": pg.K_i,"j": pg.K_j,
                "k": pg.K_k,"l": pg.K_l,"m": pg.K_m,"n": pg.K_n,"o": pg.K_o,
                "p": pg.K_p,"q": pg.K_q,"r": pg.K_r,"s": pg.K_s,"t": pg.K_t,
                "u": pg.K_u,"v": pg.K_v,"w": pg.K_w,"x": pg.K_x,"y": pg.K_y,
                "z": pg.K_z}
        setup_game(game, "ArcadeGame", 4, {}, {},
            {"typed": 0, "on": False, "word": "", 'w': {}},
            {'spcd': spcd})
    elif interaction == "Dumpster":
        if not current['got_key']:
            setup_dialogue(dialogue, ["There's a small key in the dumpster", "Take it?", None], 5,
                                    [None, None, ["Take", "Leave"]], pgft.SysFont(None, 24))
        else:
            setup_dialogue(dialogue, ["Dumpster"])
    elif interaction == "CasinoSlot":
        setup_game(game, "CasinoGame", 2, {}, {},
            {"slots": [None, None, None], "playing": False,
                "rolling": False, "bet": 1,
                "last_got_roll": float('-inf'),
                "typing": False, "finished": float('inf'),
                "text": [float('-inf'), "Message Here"],
                "effect": [False, "None"]},
                {"def": FPS, "FPS": 166})
    elif interaction == "Blackjack":
        deck = list(range(52))
        random.shuffle(deck)
        setup_game(game, "CasinoGame", 3, {"deck": deck}, {},
            {"YC": [], "HC": [], "read": False, "bet": 0,
                "lmm": float('-inf'), "text": [float('-inf'), "Message"],
                "playing": False, "end": False})
    elif interaction == "chips":
        setup_dialogue(dialogue, [
        "Since there is no way to obtain Casino Chips yet I shall give them out",
        "Do you want some Casino Chips?", None], 6, [None, None, ["Yes", "No"]],
        name="Chip Dealer") # TEMPE