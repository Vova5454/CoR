import pygame as pg
import pygame.freetype as pgft
from func import def_game
import random
from consts import minb, maxb
import copy
from sprites import Meteor, Buff, DummySprite
from func import file_thing, save, cv


pgft.init()

mmmfont = pgft.Font(None, 36)
spcdfont = pgft.SysFont("Comic Sans", 48)
casino_font = pgft.SysFont("Bell MT", 24)
medium_casino_font = pgft.SysFont("Bell MT", 18)
tiny_casino_font = pgft.SysFont("Bell MT", 6)

plus = pg.image.load(file_thing("res/dummy_plus.png"))
minus = pg.image.load(file_thing("res/dummy_minus.png"))
blackjack_deck = [pg.image.load(file_thing(f'res/Casino/Blackjack/{x}.png')) for x in range(52)]
blackjack_deck.append(pg.image.load(file_thing('res/Casino/Blackjack/empty.png')))
casino_slots = [pg.image.load(file_thing(f'res/Casino/SlotMachine/{x}.png')) for x in range(20)]
dsvcs = [pg.image.load(file_thing(f'res/Casino/SlotMachine/V/{x}.png')) for x in range(20)]
explore = pg.image.load(file_thing("res/map_explore_sign.png"))
left = pg.image.load(file_thing("res/dummy_left.png"))
right = pg.image.load(file_thing("res/dummy_right.png"))

pg.mixer.init()

sprite_hit = pg.mixer.Sound(file_thing('res/sound/hit.mp3'))

def process_game(game, screen, images, clciked, now, current, frame, sfx, mouse, pressing,
    savefile, fps):
    keys = pg.key.get_pressed()
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
                    ball.x = 388
                    ball.y = 288
                    dx = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                    dy = random.choice([random.randint(minb, maxb), -random.randint(minb, maxb)])
                    game['vars']['dx'], game['vars']['dy'] = dx, dy
                if ball.right > 795:
                    game['vars']['pscore'] += 1
                    ball.x = 388
                    ball.y = 288
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
                if game['objects']['clanker'].center[1] > balle.center[1]:
                    game['objects']['clanker'].y -= game['consts']['clanker_speed']
                if game['objects']['clanker'].center[1] < balle.center[1]:
                    game['objects']['clanker'].y += game['consts']['clanker_speed']
                protective_layer = pg.Rect(15, game['objects']['player'].top, 15, 150)
                protective_layer2 = pg.Rect(5, protective_layer.top, 10, 150)
                if (ball.colliderect(game['objects']['player'])
                    or ball.colliderect(
                        protective_layer)
                        or ball.colliderect(protective_layer2)) and game['vars']['dx'] < 0:
                    if game['objects']['ball'].top+12 > game[
                        'objects']['player'].top and ball.bottom < game['objects']['player'].bottom+12:
                        game['vars']['dx'] *= -1
                        collided = True
                if ball.colliderect(game['objects']['clanker']) and game['vars']['dx'] > 0:
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
                if not game['vars']['survived']:
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
                        game['vars']['mx'], game['vars']['my'] = 5, 12
                        spcttd = 1.1
                        game['consts']['meteor_st'] = 245
                        game['consts']['buff_st'] = 2550
                        
                    if game['vars']['meteors_killed'] == 20:
                        player.speed = 7
                        game['vars']['mx'], game['vars']['my'] = 6, 15
                        spcttd = 1.25
                        game['consts']['meteor_st'] = 215
                        game['consts']['buff_st'] = 2600
                    if game['vars']['meteors_killed'] == 40:
                        player.speed = 8
                        game['vars']['mx'], game['vars']['my'] = 10, 16
                        spcttd = 1.5
                        game['consts']['meteor_st'] = 180
                        game['consts']['buff_st'] = 2700
                    if game['vars']['meteors_killed'] == 60:
                        player.speed = 10
                        spcttd = 2
                        game['vars']['mx'], game['vars']['my'] = 15, 20
                        game['consts']['meteor_st'] = 150
                        game['consts']['buff_st'] = 3000
                    if game['vars']['meteors_killed'] == 80:
                        player.speed = 12
                        spcttd = 2.5
                        game['vars']['mx'], game['vars']['my'] = 20, 40
                        game['consts']['meteor_st'] = 75
                        game['consts']['buff_st'] = 3500
                    if game['vars']['meteors_killed'] == 115:
                        player.speed = 14
                        spcttd = 3
                        game['vars']['mx'], game['vars']['my'] = 30, 40
                        game['consts']['meteor_st'] = 65
                        game['consts']['buff_st'] = 3600
                    if game['vars']['meteors_killed'] == 150:
                        player.speed = 15
                        spcttd = 3.25
                        game['vars']['mx'], game['vars']['my'] = 40, 45
                        game['consts']['meteor_st'] = 60
                        game['consts']['buff_st'] = 3750
                    if game['vars']['meteors_killed'] == 200:
                        player.speed = 17.5
                        spcttd = 3.5
                        game['vars']['mx'], game['vars']['my'] = 45, 50
                        game['consts']['meteor_st'] = 55
                        game['consts']['buff_st'] = 3800
                    if game['vars']['meteors_killed'] == 300:
                        player.speed = 18
                        spcttd = 4
                        game['vars']['mx'], game['vars']['my'] = 50, 60
                        game['consts']['meteor_st'] = 50
                        game['consts']['buff_st'] = 4000
                    if game['vars']['meteors_killed'] == 500:
                        player.speed = 20
                        spcttd = 5
                        game['vars']['mx'], game['vars']['my'] = 55, 75
                        game['consts']['meteor_st'] = 40
                        game['consts']['buff_st'] = 4500
                    if game['vars']['meteors_killed'] == 750:
                        player.speed = 25
                        spcttd = 7.5
                        game['vars']['mx'], game['vars']['my'] = 80, 100
                        game['consts']['meteor_st'] = 30
                        game['consts']['buff_st'] = 5000
                    if game['vars']['meteors_killed'] == 950:
                        player.speed = 6
                        spcttd = 8
                        game['vars']['mx'], game['vars']['my'] = 5, 10
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
                    elif game['vars']['sas'] >= 450//spcttd+5 and sarect is not None:
                        game['vars']['sas'] = 0
                        if player.rect.colliderect(sarect):
                            for _ in range(75):
                                if player.damage():
                                    game['on'] = False
                            if game['on']:
                                game['vars']['survived'] = True
                                ssa = False
                                spcframe = now
                                mmmfont.render_to(screen, (10, 100), "You survived attack!")
                            else:
                                screen.fill((255, 255, 0))
                    elif game['vars']['sas'] < 432//spcttd:
                        sarect = None
                        player.boost = 1.5
                    if sarect:
                        pg.draw.rect(screen, (255, 0, 0), sarect)
                        player.boost = 2
                    if now - game['vars']['mst'] >= game['consts']['meteor_st']:
                        mimages = ["res/space_invaders_meteor.png", "res/space_invaders_meteor2.png", "res/space_invaders_meteor3.png"]
                        abc = Meteor(random.choice(mimages), game['vars']['mx'], game['vars']['my'])
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
                        game['vars']['survived'] = True
                        spcframe = now
                        ssa = True
                else:
                    if now - spcframe > 2000:
                        game['vars']['survived'] = False
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
        elif game['ID'] == 3:
            if game['vars']['on']:
                if keys[pg.K_ESCAPE]:
                    game['on'] = False
                if not game['vars']['spcat']:
                    player = game['objects']['player']
                    ball = game['objects']['ball']
                    ps = game['consts']['player_speed']
                    if keys[pg.K_w]: player.y -= ps
                    if keys[pg.K_s]: player.y += ps
                    if keys[pg.K_e]: player.y -= ps/2
                    if keys[pg.K_d]: player.y += ps/2
                    if keys[pg.K_r]: player.y -= ps/4
                    if keys[pg.K_f]: player.y += ps/4
                    if keys[pg.K_t]: player.y -= ps/8
                    if keys[pg.K_g]: player.y += ps/8
                    if player.top < 5: player.top = 5
                    if player.bottom > 595: player.bottom = 595
                    ball.x += game['vars']['dx']
                    ball.y += game['vars']['dy']
                    if game['vars']['hits'] == 10:
                        game['consts']['player_speed'] = 10
                    if game['vars']['hits'] == 20:
                        game['consts']['player_speed'] = 15
                    if game['vars']['hits'] == 30:
                        game['consts']['player_speed'] = 20
                    if game['vars']['hits'] == 40:
                        game['consts']['player_speed'] = 25
                    if game['vars']['hits'] == 50:
                        game['consts']['player_speed'] = 30
                    if game['vars']['hits'] == 60:
                        game['consts']['player_speed'] = 35
                    if game['vars']['hits'] == 70:
                        game['consts']['player_speed'] = 40
                    if game['vars']['hits'] == 80:
                        game['consts']['player_speed'] = 45
                    if game['vars']['hits'] == 90:
                        game['consts']['player_speed'] = 50
                    pg.draw.rect(screen, (0, 255, 0), player)
                    pg.draw.ellipse(screen, (255, 0, 255), ball)
                    mmmfont.render_to(screen, (15, 15), str(game['vars']['hits']), (255, 255, 255))
                    mmmfont.render_to(screen, (765, 15), str(game['vars']['lives']), (255, 255, 255))
                    hit = False
                    if ball.top <= 5:
                        ball.top = 5
                        game['vars']['dy'] *= -1
                        hit = True
                    if ball.bottom >= 595:
                        ball.bottom = 595
                        game['vars']['dy'] *= -1
                        hit = True
                    if ball.right > 795:
                        ball.right = 795
                        hit = True
                        game['vars']['dx'] *= -1
                    if ball.left <= 45 and player.top < ball.centery and player.bottom > ball.centery and game[
                        'vars']['dx'] < 0:
                        game['vars']['dx'] *= -1
                        game['vars']['hits'] += 1
                        hit = True
                        ball.left = 45
                    if hit:
                        game['vars']['dx'] += abs(game['vars']['dx'])/game['vars']['dx']*(random.randint(0, 15)//15)
                        game['vars']['dy'] += abs(game['vars']['dy'])/game['vars']['dy']*(random.randint(0, 15)//15)
                    if ball.left <= 0:
                        ball.x = 388
                        ball.y = 288
                        game['vars']['lives'] -= 1
                        if game['vars']['lives'] == 0:
                            game['on'] = False
                            screen.fill((255, 0, 0))
                        game['vars']['dx'] = 5 * random.choice([1, -1])
                        game['vars']['dy'] = 5 * random.choice([1, -1])
                    if game['vars']['hits'] == 100:
                        game['vars']['spcat'] = now
                else:
                    if now - game['vars']['spcat'] > 2000:
                        game['on'] = False
                    mmmfont.render_to(screen, (15, 15), "Congrats! You survived!", (255, 255, 127))

            else:
                mmmfont.render_to(screen, (15, 15), "You need to parry the ball 100 times to win.", (255, 255, 255))
                mmmfont.render_to(screen, (15, 65), "You have 3 lives. Click to start.", (255, 255, 255))
                if clciked:
                    game['vars']['on'] = True
        elif game['ID'] == 4:
            if game['vars']['on']:
                if keys[pg.K_ESCAPE]:
                    game['on'] = False
                if len(game['vars']['word']) < 25:
                    for _ in range(25-len(game['vars']['word'])):
                        alphabet = 'abcdefghijklmnopqrstuvwxyz'
                        game['vars']['word'] += alphabet[random.randint(0, 25)]
                pressed = []
                for string, pgm in game['vars']['spcd'].items():
                    if keys[pgm]:
                        if game['vars']['w'][string] is None:
                            game['vars']['w'][string] = frame
                            pressed.append(string)
                        if game['vars']['w'][string] - frame >= 6:
                            pressed.append(string)
                    else:
                        game['vars']['w'][string] = None
                for typed in pressed:
                    if typed == game['vars']['word'][0]:
                        game['vars']['word'] = game['vars']['word'][1:]
                        game['vars']['typed'] += 1
                    else:
                        game['vars']['typed'] -= 5
                spcdfont.render_to(screen, (15, 115),
                    str(round(game['vars']['typed']/(now-game[
                    'vars']['on'])*1000, 2)), (255, 255, 255))
                spcdfont.render_to(screen, (15, 15), game['vars']['word'],
                                    (255, 255, 255))

                
            else:
                mmmfont.render_to(screen, (15, 15),
                    "Type, correct letter gives +1. -5 if not.", (255, 255, 255))
                if clciked:
                    game['vars']['on'] = now
    elif game['type'] == "Dummy!":
        screen.fill((0, 0, 0))
        fontf = pgft.SysFont("Comic Sans", 36)
        enemy = game['groups']['enemy']
        player = game['objects']['you']
        if game['vars']['read']:
            if game['vars']['on']:
                game['groups']['enemy'].draw(screen)
                game['groups']['enemy'].update()
                pg.draw.rect(screen, (127, 127, 127), player)
                pc = [sprite for sprite in enemy if
                        sprite.rect.colliderect(player)]
                if pc:
                    pc[0].kill()
                    sprite_hit.set_volume(sfx)
                    sprite_hit.play()
                if not game['groups']['enemy']:
                    game['vars']['on'] = False
                if keys[pg.K_w]:
                    player.y -= game['consts']['player_speed']
                if keys[pg.K_a]:
                    player.x -= game['consts']['player_speed']
                if keys[pg.K_s]:
                    player.y += game['consts']['player_speed']
                if keys[pg.K_d]:
                    player.x += game['consts']['player_speed']
                if player.left < 0: player.left = 0
                if player.right > 800: player.right = 800
                if player.bottom > 600: player.bottom = 600
                if player.top < 0: player.top = 0

            else:
                fontf.render_to(screen, (790-fontf.get_rect(str(len(enemy))).width, 10), str(len(enemy)), (255, 255, 255))
                rae = pg.Rect(750, 50, 40, 40)
                sgb = pg.Rect(375, 275, 50, 50)
                etsotp = pg.Rect(10, 10, 150, 50)
                trfie = pg.Rect(10, 550, 40, 40)
                add = pg.Rect(350, 250, 100, 100)
                arfae = pg.Rect(375, 20, 50, 50)
                back = pg.Rect(0, 0, 75, 75)
                x = pg.Rect(100, 10, 100, 50)
                y = pg.Rect(210, 10, 100, 50)
                wi = pg.Rect(320, 10, 100, 50)
                he = pg.Rect(430, 10, 100, 50)
                dxr = pg.Rect(540, 10, 100, 50)
                dyr = pg.Rect(650, 10, 100, 50)
                rfew = pg.Rect(450, 325, 150, 50)
                rfeh = pg.Rect(450, 425, 150, 50)
                aeb = [x, y, wi, he, dxr, dyr]
                if game['vars']['mso'] is None:
                    fontf.render_to(screen, (750, 90), "del", (255, 255, 255))
                    pg.draw.rect(screen, (255, 0, 0), rae)
                    pg.draw.rect(screen, (220, 230, 240), trfie)
                    pg.draw.rect(screen, (127, 255, 127), arfae)
                    pg.draw.rect(screen, (255, 255, 255), sgb)
                    pg.draw.rect(screen, (72, 72, 72), etsotp)
                    screen.blit(plus, (10, 10))
                    fontf.render_to(screen, (10, 525), "Inspect Enemies", (255, 255, 255))
                    fontf.render_to(screen, (65, 15), str(game['consts']['player_speed']), (255, 255, 255))
                    screen.blit(minus, (110, 10))
                    fontf.render_to(screen, (375, 75), "Add enemy", (255, 255, 0))
                    fontf.render_to(screen, (335, 225), "START", (255, 255, 255))
                    if rae.collidepoint(mouse) and clciked:
                        game['groups']['enemy'] = pg.sprite.Group()
                    if sgb.collidepoint(mouse) and clciked:
                        game['vars']['on'] = True
                    if pg.Rect(10, 10, 50, 50).collidepoint(mouse) and clciked:
                        game['consts']['player_speed'] += 1
                    if pg.Rect(110, 10, 50, 50).collidepoint(mouse) and clciked:
                        game['consts']['player_speed'] -= 1
                    if arfae.collidepoint(mouse) and clciked:
                        ae = [0, 0, 0, 0, 5, 5]
                        game['vars']['mso'] = "add_enemy"
                        wyt = None
                    pg.draw.rect(screen, (196, 196, 196), rfew)
                    pg.draw.rect(screen, (196, 196, 196), rfeh)
                    screen.blit(plus, (450, 325))
                    screen.blit(plus, (450, 425))
                    screen.blit(minus, (550, 325))
                    screen.blit(minus, (550, 425))
                    screen.blit(explore, (100, 400))
                    exr = pg.Rect(100, 400, 50, 50)
                    fontf.render_to(screen, (500, 335), str(player.width))
                    fontf.render_to(screen, (500, 435), str(player.height))
                    if pg.Rect(450, 325, 50, 50).collidepoint(mouse) and clciked:
                        player.width += 1
                    if pg.Rect(450, 425, 50, 50).collidepoint(mouse) and clciked:
                        player.height += 1
                    if pg.Rect(550, 325, 50, 50).collidepoint(mouse) and clciked:
                        player.width -= 1
                    if pg.Rect(550, 425, 50, 50).collidepoint(mouse) and clciked:
                        player.height -= 1
                    if trfie.collidepoint(mouse) and clciked and len(enemy):
                        game['vars']['mso'] = "inspect_enemy"
                        enemies_but_list = [rect for rect in enemy]
                        index_for_enemies = 0
                    if exr.collidepoint(mouse) and clciked:
                        game['vars']['mso'] = "map_explore"
                        moved_x = 0
                        moved_y = 0
                elif game['vars']['mso'] == "add_enemy":
                    pg.draw.rect(screen, (255, 255, 255), add)
                    pg.draw.rect(screen, (127, 127, 127), x)
                    fontf.render_to(screen, (110, 20), str(ae[0]), (255, 255, 255))
                    pg.draw.rect(screen, (127, 127, 127), y)
                    fontf.render_to(screen, (220, 20), str(ae[1]), (255, 255, 255))
                    pg.draw.rect(screen, (127, 127, 127), wi)
                    fontf.render_to(screen, (330, 20), str(ae[2]), (255, 255, 255))
                    pg.draw.rect(screen, (127, 127, 127), he)
                    fontf.render_to(screen, (440, 20), str(ae[3]), (255, 255, 255))
                    pg.draw.rect(screen, (127, 127, 127), dxr)
                    fontf.render_to(screen, (550, 20), str(ae[4]), (255, 255, 255))
                    pg.draw.rect(screen, (127, 127, 127), dyr)
                    fontf.render_to(screen, (660, 20), str(ae[5]), (255, 255, 255))
                    pg.draw.rect(screen, (255, 127, 63), back)
                    fontf.render_to(screen, (350, 200), "Add", (0, 255, 255))
                    fontf.render_to(screen, (10, 55), "Back", (142, 45, 66))
                    if add.collidepoint(mouse) and clciked:
                        de = DummySprite((ae[2], ae[3]), (ae[0], ae[1]), ae[4], ae[5])
                        enemy.add(de)
                    if back.collidepoint(mouse) and clciked:
                        game['vars']['mso'] = None
                    cotbfae = False
                    isfto = 0
                    for ia in aeb:
                        if ia.collidepoint(mouse) and clciked:
                            wyt = isfto
                            cotbfae = True
                        isfto += 1
                    if not cotbfae and clciked:
                        ia = None
                    iadd = {
                        0: 0,
                        1: 1,
                        2: 2,
                        3: 3,
                        4: 4,
                        5: 5
                    }
                    ia = wyt
                    if ia or ia == 0:
                        if 1 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 1
                        if 2 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 2
                        if 3 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 3
                        if 4 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 4
                        if 5 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 5
                        if 6 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 6
                        if 7 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 7
                        if 8 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 8
                        if 9 in pressing:
                                ae[iadd[ia]] *= 10
                                ae[iadd[ia]] += 9
                        if 0 in pressing:
                                ae[iadd[ia]] *= 10
                        if '-' in pressing:
                                ae[iadd[ia]] *= -1
                        if 'backspace' in pressing:
                                ae[iadd[ia]] = 0
                elif game['vars']['mso'] == "inspect_enemy":
                    pg.draw.rect(screen, (127, 0, 0), pg.Rect(0, 0, 150, 50))
                    fontf.render_to(screen, (10, 10), "Back", (255, 255, 255))
                    if pg.Rect(0, 0, 150, 50).collidepoint(mouse) and clciked:
                        game['vars']['mso'] = None
                    screen.blit(left, (325, 450))
                    screen.blit(right, (425, 450))
                    fontf.render_to(screen, (380, 460), str(index_for_enemies), (255, 255, 255))
                    if pg.Rect(325, 450, 50, 50).collidepoint(mouse) and clciked:
                        index_for_enemies -= 1
                    if pg.Rect(425, 450, 50, 50).collidepoint(mouse) and clciked:
                        index_for_enemies += 1
                    index_for_enemies %= len(enemies_but_list)
                    specific_enemy = enemies_but_list[index_for_enemies]
                    fontf.render_to(screen, (300, 100), f'X: {str(specific_enemy.rect.x)}', (255, 255, 255))
                    fontf.render_to(screen, (300, 150), f'Y: {str(specific_enemy.rect.y)}', (255, 255, 255))
                    fontf.render_to(screen, (300, 200), f'Width: {str(specific_enemy.rect.width)}', (255, 255, 255))
                    fontf.render_to(screen, (300, 250), f'Height: {str(specific_enemy.rect.height)}', (255, 255, 255))
                    fontf.render_to(screen, (300, 300), f'DX: {str(specific_enemy.dx)}', (255, 255, 255))
                    fontf.render_to(screen, (300, 350), f'DY: {str(specific_enemy.dy)}', (255, 255, 255))
                elif game['vars']['mso'] == "map_explore":
                    game['groups']['enemy'].draw(screen)
                    fontf.render_to(screen, (10, 10), f'{moved_x}, {moved_y}', (255, 255, 255))
                    screen.blit(explore, (100, 400))
                    if exr.collidepoint(mouse) and clciked:
                        game['vars']['mso'] = None
                    new_movement_x = 0
                    new_movement_y = 0
                    if keys[pg.K_w]:
                        new_movement_y += game['consts']['player_speed']
                    if keys[pg.K_a]:
                        new_movement_x += game['consts']['player_speed']
                    if keys[pg.K_s]:
                        new_movement_y -= game['consts']['player_speed']
                    if keys[pg.K_d]:
                        new_movement_x -= game['consts']['player_speed']
                    moved_x += new_movement_x
                    moved_y += new_movement_y
                    for obj in enemy:
                        obj.rect.x += new_movement_x
                        obj.rect.y += new_movement_y
                    if game['vars']['mso'] is None:
                        for obj in enemy:
                            obj.rect.x -= moved_x
                            obj.rect.y -= moved_y
        else:
            fontf.render_to(screen, (10, 10), "You can simulate attack patterns with this", (255, 255, 255))
            fontf.render_to(screen, (10, 60), "dummy. You can add rects which will attack", (255, 255, 255))
            fontf.render_to(screen, (10, 110), "and play a noise if you hit them. You can't", (255, 255, 255))
            fontf.render_to(screen, (10, 160), "delete a single object, has to be all of them.", (255, 255, 255))
            fontf.render_to(screen, (10, 210), "You can customize the speed of yourself and", (255, 255, 255))
            fontf.render_to(screen, (10, 260), "the objects. Click to start. ESC to exit.", (255, 255, 255))
            if clciked:
                game['vars']['read'] = True
        if keys[pg.K_ESCAPE]:
            game['on'] = False
    elif game['type'] == "CasinoGame":
        if game['ID'] == 1:
            if game['vars']['start']:
                if not game['vars']['betting_on']:
                    if not game['vars']['ISTM']:
                        casino_font.render_to(screen, (610, 50),
                            f'Bet: {game['vars']['bet']}', (0, 0, 0))
                        pg.draw.rect(screen, (255, 0, 0), pg.Rect(35, 50, 150, 50))
                        casino_font.render_to(screen, (45, 60), "RED", (0, 255, 255))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(35, 150, 150, 50))
                        casino_font.render_to(screen, (45, 160), "BLACK", (255, 255, 255))
                        pg.draw.rect(screen, (0, 255, 0), pg.Rect(35, 250, 150, 50))
                        casino_font.render_to(screen, (45, 260), "GREEN", (255, 0, 255))
                        pg.draw.rect(screen, (63, 63, 196), pg.Rect(35, 350, 150, 50))
                        casino_font.render_to(screen, (45, 360), "CUSTOM", (127, 127, 196))
                        if pg.Rect(35, 350, 150, 50).collidepoint(mouse) and clciked:
                            game['vars']['ISTM'] = True
                        if pg.Rect(35, 50, 150, 50).collidepoint(mouse) and clciked:
                            game['vars']['betting_on'] = 'RED'
                        if pg.Rect(35, 150, 150, 50).collidepoint(mouse) and clciked:
                            game['vars']['betting_on'] = 'BLACK'
                        if pg.Rect(35, 250, 150, 50).collidepoint(mouse) and clciked:
                            game['vars']['betting_on'] = 'GREEN'
                    else:
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(35, 50, 25, 25))
                        medium_casino_font.render_to(screen, (35, 50),
                        "37", (255, 255, 255))
                        for simfcro in range(37):
                            if simfcro < 18:
                                if not game['vars']['toast'][simfcro]:
                                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(35,
                                    50+simfcro*25, 25, 25))
                                else:
                                    pg.draw.rect(screen, (196, 196, 196), pg.Rect(35,
                                    50+simfcro*25, 25, 25))              
                                medium_casino_font.render_to(screen, (37,
                                52+simfcro*25), f"{simfcro+1}", (255, 255, 255))
                            elif simfcro < 36:
                                if not game['vars']['toast'][simfcro]:
                                    pg.draw.rect(screen, (255, 0, 0), pg.Rect(85,
                                    50+simfcro%18*25, 25, 25))
                                else:
                                    pg.draw.rect(screen, (255, 196, 196), pg.Rect(85,
                                    50+simfcro%18*25, 25, 25))              
                                medium_casino_font.render_to(screen, (87,
                                52+simfcro%18*25), f"{simfcro+1}", (255, 255, 255))
                            else:
                                if game['vars']['toast'][36]:
                                    pg.draw.rect(screen, (196, 255, 196),
                                    pg.Rect(135, 50, 25, 25))
                                    medium_casino_font.render_to(screen, (137, 52),
                                    "37", (255, 255, 255))
                                else:
                                    pg.draw.rect(screen, (0, 255, 0),
                                    pg.Rect(135, 50, 25, 25))
                                    medium_casino_font.render_to(screen, (137, 52),
                                    "37", (255, 255, 255))
                            if pg.Rect(35+simfcro//18*50, 50+(simfcro%18)*25, 25, 25).collidepoint(
                                mouse) and clciked:
                                game['vars']['toast'][simfcro] ={
                                True: False, False: True}[game['vars']['toast'][simfcro]]
                        casino_font.render_to(screen, (50, 20), "Each Slot costs your bet.")
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(600, 100, 150, 50))
                        casino_font.render_to(screen, (610, 110), "START", (255, 255, 255))
                        if pg.Rect(600, 100, 150, 50).collidepoint(mouse) and clciked:
                            if len([0 for x in game['vars']['toast'] if x])*game[
                                'vars']['bet'] <= current['CasinoChips']:
                                game['vars']['betting_on'] = 'TOAST'
                            else:
                                game['vars']['text'] = [now, "You're too broke!"]
                    game['vars']['starttime'] = now
                    fps = game['consts']['FPS']
                else:
                    if now - game['vars']['starttime'] < 1000:
                        temp = pg.Rect(0, 0, 24, 24)
                        while ((400-temp.centerx)**2 + (300-temp.centery)**2)**0.5 > game['consts']['dist']:
                            temp.center = (random.randint(0, 800), random.randint(0, 600))
                        game['objects']['ball'] = temp
                        game['vars']['got'] = random.randint(0, 36)
                    else:
                        fps = game['consts']['def']
                        if game['vars']['got'] == 0:
                            gott = 'GREEN'
                        elif game['vars']['got'] % 2:
                            gott = 'RED'
                        else:
                            gott = 'BLACK'
                        if game['vars']['betting_on'] != 'TOAST':
                            if gott != game['vars']['betting_on']:
                                current['CasinoChips'] -= game['vars']['bet']
                                game['vars']['text'] = [now, f"{gott}... You lose ${game['vars']['bet']}"]
                            else:
                                if gott == 'GREEN':
                                    current['CasinoChips'] += 35*game['vars']['bet']
                                    game['vars']['text'] = [now, f"{gott}! You won ${35*game['vars']['bet']}"]
                                else:
                                    current['CasinoChips'] += game['vars']['bet']
                                    game['vars']['text'] = [now, f"{gott}! You won ${game['vars']['bet']}"]
                        else:
                            temp = len([0 for x in game['vars']['toast'] if x])
                            temp_cost = temp*game['vars']['bet']
                            current['CasinoChips'] -= temp_cost
                            temp_hit = False
                            if game['vars']['toast'][game['vars']['got']]:
                                current['CasinoChips'] += 36*game['vars']['bet']
                                temp_hit = True
                            temp_won = (36-temp)*game['vars']['bet']
                            if temp == 37:
                                game['vars']['text'] = [now,
                                f"{game['vars']['got']+1}. You lost ${game['vars']['bet']}."]
                            elif temp == 36 and temp_hit:
                                game['vars']['text'] = [
                                now, f"{game['vars']['got']+1}. Well you didn't get anything."]
                            elif temp == 36 and not temp_hit:
                                game['vars']['text'] = [
                                now, f"{game['vars']['got']+1}. You lost ${temp_cost}..."]
                            elif temp_hit:
                                game['vars']['text'] = [
                                now, f"{game['vars']['got']+1}. You won ${temp_won}!"]
                            else:
                                game['vars']['text'] = [
                                now, f"{game['vars']['got']+1}. You lost ${temp_cost}..."]
                        game['vars']['ISTM'] = False
                        save(savefile, current)
                        game['vars']['start'] = False
                        
            else:
                casino_font.render_to(screen, (610, 50),
                    f'Chips: {str(current['CasinoChips'])}')
                pg.draw.rect(screen, (20, 50, 50), pg.Rect(600, 400, 150, 50))
                casino_font.render_to(screen, (610, 410), "exit", (127, 255, 255))
                if pg.Rect(600, 400, 150, 50).collidepoint(mouse) and clciked:
                    game['on'] = False
                    current['loc'] = "CasinoEntrance"
                pg.draw.rect(screen, (127, 127, 196), pg.Rect(600, 100, 150, 50))
                casino_font.render_to(screen, (610, 110), str(game['vars']['bet']))
                if pg.Rect(600, 100, 150, 50).collidepoint(mouse) and clciked:
                    if game['vars']['bet'] < 0:
                        game['vars']['text'] = [now, "Should be positive."]
                    elif game['vars']['bet'] > current['CasinoChips']:
                        game['vars']['text'] = [now, "You're too broke!"]
                    else:
                        game['vars']['start'] = True
                        game['vars']['betting_on'] = False
                game['vars']['bet'] = str(game['vars']['bet'])
                if 'backspace' in pressing: game['vars']['bet'] = '0'
                if 0 in pressing: game['vars']['bet'] += '0'
                if 1 in pressing: game['vars']['bet'] += '1'
                if 2 in pressing: game['vars']['bet'] += '2'
                if 3 in pressing: game['vars']['bet'] += '3'
                if 4 in pressing: game['vars']['bet'] += '4'
                if 5 in pressing: game['vars']['bet'] += '5'
                if 6 in pressing: game['vars']['bet'] += '6'
                if 7 in pressing: game['vars']['bet'] += '7'
                if 8 in pressing: game['vars']['bet'] += '8'
                if 9 in pressing: game['vars']['bet'] += '9'
                game['vars']['bet'] = int(game['vars']['bet'])
            if now - game['vars']['text'][0] < 1500:
                casino_font.render_to(screen, (200, 50), 
                game['vars']['text'][1], (0, 0, 0))
            pg.draw.ellipse(screen, (255, 255, 255), game['objects']['ball'])
        elif game['ID'] == 2:
            fps = game['consts']['FPS']
            screen.blit(images['CSM'], (0, 0))
            if not game['vars']['rolling']:
                if None in game['vars']['slots']:
                    pg.draw.rect(screen, (196, 196, 196), pg.Rect(760, 580, 30, 10))
                    screen.blit(images['Casino/SlotMachine/empty'], (180, 150))
                    screen.blit(images['Casino/SlotMachine/empty'], (330, 150))
                    screen.blit(images['Casino/SlotMachine/empty'], (480, 150))
                    tiny_casino_font.render_to(screen, (762, 582), "EXIT", (255, 255, 255))
                    pg.draw.rect(screen, (255, 255, 255), pg.Rect(300, 45, 200, 50))
                    casino_font.render_to(screen, (370, 62), "Start!", (0, 0, 0))
                    if len(str(game['vars']['bet'])) > 13:
                        casino_font.render_to(screen, (10, 45),
                        f'{str(game['vars']['bet'])[:12]}...')
                    else:
                        casino_font.render_to(screen, (10, 45),
                                            str(game['vars']['bet'])[:13])
                    casino_font.render_to(screen, (10, 10), "Bet:")
                    if pg.Rect(760, 580, 30, 10).collidepoint(mouse) and clciked:
                        fps = game['consts']['def']
                        game['on'] = False
                    if (pg.Rect(300, 45, 200, 50).collidepoint(
                        mouse) and clciked) or (' ' in pressing):
                        if game['vars']['bet'] <= current['CasinoChips']:
                            game['vars']['rolling'] = True
                        else:
                            game['vars']['text'] = [now+1000, "Insufficient Funds"]
                    pg.draw.rect(screen, (120, 120, 120), pg.Rect(10, 500, 120, 50))
                    casino_font.render_to(screen, (20, 510), "TYPING", (255, 255, 255))
                    if clciked:
                        if pg.Rect(10, 500, 120, 50).collidepoint(mouse):
                            game['vars']['typing'] = True
                        else:
                            game['vars']['typing'] = False
                    if game['vars']['typing']:
                        for pressed in pressing:
                            if pressed == 'backspace':
                                game['vars']['bet'] //= 10
                                if not game['vars']['bet']:
                                    game['vars']['bet'] = 1
                            elif pressed == '-':
                                continue
                            elif pressed == 'CAPSLOCK':
                                game['vars']['bet'] = 1
                            elif pressed == ' ':
                                continue
                            else:
                                game['vars']['bet'] *= 10
                                game['vars']['bet'] += pressed
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(10, 150, 120, 50))
                    casino_font.render_to(screen, (55, 165), "x2", (255, 255, 255))
                    if pg.Rect(10, 150, 120, 50).collidepoint(mouse) and clciked:
                        game['vars']['bet'] *= 2
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(10, 250, 120, 50))
                    casino_font.render_to(screen, (55, 265), "x5", (255, 255, 255))
                    if pg.Rect(10, 250, 120, 50).collidepoint(mouse) and clciked:
                        game['vars']['bet'] *= 5
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(10, 350, 120, 50))
                    casino_font.render_to(screen, (50, 365), "x10", (255, 255, 255))
                    if pg.Rect(10, 350, 120, 50).collidepoint(mouse) and clciked:
                        game['vars']['bet'] *= 10
                    if now - game['vars']['finished'] > 500:
                        game['vars']['effect'] = [False, "None"]
                else:
                    if now - game['vars']['finished'] > 250:
                        game['vars']['slots'] = [None, None, None]
                    if game['vars']['unfinished']:
                        game['vars']['unfinished'] = False
                        if len(set(game['vars']['slots'])) == 3:
                            current['CasinoChips'] -= game['vars']['bet']
                            game['vars']['text'] = [now+1000, f"You lost ${game['vars']['bet']}"]
                        elif len(set(game['vars']['slots'])) == 1:
                            for slot in game['vars']['slots']:
                                actm = slot
                            if actm == 19:
                                current['CasinoChips'] += 5000*game['vars']['bet']
                                game['vars']['text'] = [now+2500,
                                f"YOU HIT THE JACKPOT! {5000*game['vars']['bet']}"]
                                game['vars']['effect'] = [True, "JACKPOT"]
                            elif actm in [15, 16, 17, 18]:
                                current['CasinoChips'] += 99*game['vars']['bet']
                                game['vars']['text'] = [now+2000,
                                    f"You won ${100*game['vars']['bet']}!"]
                                game['vars']['effect'] = [True, "TRIPLE B"]
                            else:
                                mystery_mult = random.uniform(9, 19)
                                current['CasinoChips'] += int(game['vars'][
                                'bet']*mystery_mult)
                                game['vars']['text'] = [now+1500,
                                f"You won ${int((mystery_mult+1)*game['vars']['bet'])}"]
                                game['vars']['effect'] = [True, "Triple"]
                            
                        else:
                            if game['vars']['slots'][0] == game['vars']['slots'][1]:
                                actm = game['vars']['slots'][0]
                                proceed = True
                            else:
                                actm = 20
                                proceed = False
                            if actm == 19:
                                current['CasinoChips'] += game['vars']['bet']*4
                                game['vars']['text'] = [now+1200,
                                    f"You won ${game['vars']['bet']*5}!"]
                                game['vars']['effect'] = [True, "Double F"]
                            elif proceed:
                                mystery_mult = random.uniform(0, 1)
                                current['CasinoChips'] += int(game[
                                'vars']['bet']*mystery_mult)
                                game['vars']['text'] = [now+1050,
                                    f"You won ${int(game['vars']['bet']*(mystery_mult+1))}!"]
                                int(game['vars']['bet']*(mystery_mult+1))
                                game['vars']['effect'] = [True, "small"]
                            else:
                                myst_mult = random.uniform(0, 0.5)
                                current['CasinoChips'] += int(game['vars'][
                                    'bet']*myst_mult)
                                game['vars']['text'] = [now+750,
                                    f"You won ${int(myst_mult*game['vars']['bet'])}!"]
                                game['vars']['effect'] = [True, "bruh"]
                        save(savefile, current)
            else:
                if game['vars']['slots'][0] or game['vars']['slots'][0] == 0:
                    screen.blit(casino_slots[game['vars']['slots'][0]], (180, 150))
                    game['vars']['effect'] = [False, "None"]
                else:
                    screen.blit(dsvcs[now%20], (180, 150))
                if game['vars']['slots'][1] or game['vars']['slots'][1] == 0:
                    screen.blit(casino_slots[game['vars']['slots'][1]], (330, 150))
                else:
                    screen.blit(dsvcs[(now+3)%20], (330, 150))
                if game['vars']['slots'][2] or game['vars']['slots'][2] == 0:
                    screen.blit(casino_slots[game['vars']['slots'][2]], (480, 150))
                else:
                    screen.blit(dsvcs[(now+7)%20], (480, 150))
                if not None in game['vars']['slots'] and now > game[
                    'vars']['last_got_roll']:
                    game['vars']['rolling'] = False
                    game['vars']['finished'] = now
                    game['vars']['unfinished'] = True
                else:
                    if ' ' in pressing:
                        spci = 0
                        for slot in game['vars']['slots']:
                            if slot is None:
                                game['vars']['slots'][spci] = now%20
                                game['vars']['last_got_roll'] = now+500
                                break
                            spci += 1
            if now < game['vars']['text'][0]:
                casino_font.render_to(screen, (200, 50), game['vars']['text'][1])
            if game['vars']['effect'][0]:
                if game['vars']['effect'][1] == "JACKPOT":
                    if frame%2:
                        screen.fill((255, 0, 0))
                    else:
                        screen.fill((255, 255, 0))
                elif game['vars']['effect'][1] == "TRIPLE B":
                    tripleb_surface = pg.Surface((800, 600), pg.SRCALPHA)
                    if frame%3:
                        tripleb_surface.fill((255, 0, 0, 85))
                    else:
                        tripleb_surface.fill((255, 255, 0, 85))
                    screen.blit(tripleb_surface, (0, 0))
                elif game['vars']['effect'][1] == "Triple":
                    triple_surface = pg.Surface((800, 600), pg.SRCALPHA)
                    triple_surface.fill((cv(random.randint(0, 255)),
                                            cv(random.randint(0, 255)),
                                            cv(random.randint(0, 255)),
                                            cv(random.randint(0, 96))))
                    screen.blit(triple_surface, (0, 0))
                elif game['vars']['effect'][1] == "Double F":
                    doublef_surface = pg.Surface((800, 600), pg.SRCALPHA)
                    doublef_surface.fill((255, 255, 0, cv((now-game['vars']['finished'])//2)))
                    screen.blit(doublef_surface, (0, 0))
                elif game['vars']['effect'][1] == "small":
                    small_surface = pg.Surface((800, 600), pg.SRCALPHA)
                    small_surface.fill((255, 255, 0, cv((now-game['vars']['finished'])//10)))
                    screen.blit(small_surface, (0, 0))
                elif game['vars']['effect'][1] == "bruh":
                    bruh_surface = pg.Surface((800, 600), pg.SRCALPHA)
                    bruh_surface.fill((0, 0, 0, cv((now-game['vars']['finished'])/3)))
                    screen.blit(bruh_surface, (0, 0))
        elif game['ID'] == 3:
            if game['vars']['read']:
                screen.fill((255, 255, 255))
                if game['vars']['playing']:
                    if not game['vars']['YC']:
                        game['vars']['YC'] = [game['objects']['deck'].pop(),
                                                game['objects']['deck'].pop()]
                        game['vars']['HC'] = [game['objects']['deck'].pop(),
                                                game['objects']['deck'].pop()]
                    if len(game['vars']['YC']) == 2:
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(407, 335, 160, 260))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(233, 335, 160, 260))
                        screen.blit(blackjack_deck[game['vars']['YC'][0]], (412, 340))
                        screen.blit(blackjack_deck[game['vars']['YC'][1]], (238, 340))
                    else:
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(320, 335, 160, 260))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(145, 335, 160, 260))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(495, 335, 160, 260))
                        screen.blit(blackjack_deck[game['vars']['YC'][0]], (325, 340))
                        screen.blit(blackjack_deck[game['vars']['YC'][1]], (150, 340))
                        screen.blit(blackjack_deck[game['vars']['YC'][2]], (500, 340))
                    if len(game['vars']['HC']) == 2:
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(407, 5, 160, 260))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(233, 5, 160, 260))
                        screen.blit(blackjack_deck[game['vars']['HC'][0]], (412, 10))
                        if game['vars']['lmm'] == float('-inf'):
                            screen.blit(blackjack_deck[52], (238, 10))
                        else:
                            screen.blit(blackjack_deck[game['vars']['HC'][1]], (238, 10))
                    else:
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(320, 5, 160, 260))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(145, 5, 160, 260))
                        pg.draw.rect(screen, (0, 0, 0), pg.Rect(495, 5, 160, 260))
                        screen.blit(blackjack_deck[game['vars']['HC'][0]], (325, 10))
                        screen.blit(blackjack_deck[game['vars']['HC'][1]], (150, 10))
                        screen.blit(blackjack_deck[game['vars']['HC'][2]], (500, 10))
                    if not game['vars']['end']:
                        if (len(game['vars']['YC']), len(game['vars']['HC'])) == (2, 2):
                            if game['vars']['lmm'] == float('-inf'):
                                pg.draw.rect(screen, (0, 0, 0), pg.Rect(200, 275, 150, 50))
                                pg.draw.rect(screen, (0, 0, 0), pg.Rect(450, 275, 150, 50))
                                casino_font.render_to(screen, (205, 280), "DRAW", (255, 255, 255))
                                casino_font.render_to(screen, (455, 280), "DON'T", (255, 255, 255))
                                if pg.Rect(200, 275, 150, 50).collidepoint(mouse) and clciked:
                                    game['vars']['YC'].append(game['objects']['deck'].pop())
                                    game['vars']['lmm'] = now
                                if pg.Rect(450, 275, 150, 50).collidepoint(mouse) and clciked:
                                    game['vars']['lmm'] = now
                            else:
                                if now - game['vars']['lmm'] >= 500:
                                    thysum = 0
                                    for card in game['vars']['HC']:
                                        if card % 13 < 10:
                                            thysum += card%13 + 1
                                        else:
                                            thysum += 10
                                    if 0 in game['vars']['HC']: thysum += 10
                                    elif 13 in game['vars']['HC']: thysum += 10
                                    elif 26 in game['vars']['HC']: thysum += 10
                                    elif 39 in game['vars']['HC']: thysum += 10
                                    if thysum <= 16:
                                        game['vars']['HC'].append(game['objects']['deck'].pop())
                                    game['vars']['end'] = True
                                    game['vars']['lmm'] = now
                        if (len(game['vars']['YC']), len(game['vars']['HC'])) == (3, 2):
                            if now - game['vars']['lmm'] >= 500:
                                thysum = 0
                                thyace = False
                                for card in game['vars']['HC']:
                                    if card % 13 < 10:
                                        thysum += card%13 + 1
                                        if card%13 == 0:
                                            thyace = True
                                    else:
                                        thysum += 10
                                if thyace: thysum += 10
                                if thysum <= 16:
                                    game['vars']['HC'].append(game['objects']['deck'].pop())
                                game['vars']['end'] = True
                                game['vars']['lmm'] = now
                    else:
                        your_sum = 0
                        your_aces = 0
                        their_sum = 0
                        their_aces = 0
                        for card in game['vars']['YC']:
                            if card%13 < 10:
                                your_sum += card%13 + 1
                                if card%13 == 0: your_aces += 1
                            else:
                                your_sum += 10
                        if your_aces: your_sum += 10
                        if your_sum > 21 and your_aces: your_sum -= 10
                        for card in game['vars']['HC']:
                            if card%13 < 10:
                                their_sum += card%13+1
                                if card%13 == 0: their_aces += 1
                            else:
                                their_sum += 10
                        if their_aces: their_sum += 10
                        if their_sum > 21 and their_aces: their_sum -= 10
                        casino_font.render_to(screen, (10, 10), str(their_sum))
                        casino_font.render_to(screen, (770, 575), str(your_sum))
                        if now - game['vars']['lmm'] > 1750:
                            self_sum = 0
                            self_aces = 0
                            his_sum = 0
                            his_aces = 0
                            for card in game['vars']['YC']:
                                if card%13 < 10 and card%13:
                                    self_sum += card%13+1
                                else:
                                    if card%13:
                                        self_sum += 10
                                    else:
                                        self_aces += 1
                                        self_sum += 1
                            if self_aces and 21-self_sum>=10: self_sum += 10
                            for card in game['vars']['HC']:
                                if card%13 < 10 and card%13:
                                    his_sum += card%13+1
                                else:
                                    if card%13:
                                        his_sum += 10
                                    else:
                                        his_aces += 1
                                        his_sum += 1
                            if his_aces and 21-his_sum>=10: his_sum += 10
                            if self_sum > 21 and his_sum > 21:
                                current['CasinoChips'] -= game['vars']['bet']
                                game['vars']['text'] = [now+1500,
                                f"Technically you went over 21 first... -${game['vars']['bet']}"]
                            elif self_sum > 21:
                                current['CasinoChips'] -= game['vars']['bet']
                                game['vars']['text'] = [now+1000,
                                f"You went over 21... -${game['vars']['bet']}"]
                            elif 21-self_sum < abs(21-his_sum):
                                if self_sum == 21 and len(game['vars']['YC']) == 2:
                                    temp = int(1.5*game['vars']['bet'])
                                    current['CasinoChips'] += temp
                                    game['vars']['text'] = [now+2000,
                                    f"1.5x bonus! First 2 cards are 21! +${temp}"]
                                else:
                                    current['CasinoChips'] += game['vars']['bet']
                                    game['vars']['text'] = [now+1200,
                                    f"You're closer to 21! +${game['vars']['bet']}"]
                            elif his_sum > 21:
                                current['CasinoChips'] += game['vars']['bet']
                                game['vars']['text'] = [now+1750,
                                f"You won! Dealer went over 21. +${game['vars']['bet']}"]
                            elif 21-self_sum == 21-his_sum:
                                game['vars']['text'] = [now+1000, "Tie!"]
                            else:
                                current['CasinoChips'] -= game['vars']['bet']
                                game['vars']['text'] = [now+1000,
                                f"The dealer was closer to 21... -${game['vars']['bet']}"]
                            game['vars']['YC'] = []
                            game['vars']['HC'] = []
                            game['vars']['playing'] = False
                            game['vars']['lmm'] = float('-inf')
                            game['vars']['end'] = False
                            deck = list(range(52))
                            random.shuffle(deck)
                            game['objects']['deck'] = deck
                            save(savefile, current)
                
                else:
                    pg.draw.rect(screen, (127, 127, 127), pg.Rect(10, 10, 150, 50))
                    pg.draw.rect(screen, (0, 0, 0), pg.Rect(10, 70, 150, 50))
                    casino_font.render_to(screen, (20, 80), "EXIT", (255, 255, 255))
                    casino_font.render_to(screen, (15, 15), str(game['vars']['bet']),
                        (255, 255, 255))
                    casino_font.render_to(screen, (170, 10), str(current['CasinoChips']))
                    if pg.Rect(10, 10, 150, 50).collidepoint(mouse) and clciked:
                        if game['vars']['bet'] <= current['CasinoChips']:
                            game['vars']['playing'] = True
                        else:
                            game['vars']['text'] = [now+1000, "You're too broke."]
                    if pg.Rect(10, 70, 150, 50).collidepoint(mouse) and clciked:
                        game['on'] = False
                    for key in pressing:
                        if key in ['CAPSLOCK', ' ', '-']: continue
                        if key == 'backspace':
                            game['vars']['bet'] = 0
                        else:
                            game['vars']['bet'] *= 10
                            game['vars']['bet'] += key
                if now < game['vars']['text'][0]:
                    casino_font.render_to(screen, (10, 280), game['vars']['text'][1])
            else:
                screen.fill((0, 0, 0))
                casino_font.render_to(screen, (10, 10), "In this game you need for the sum of the value of your card to be as", (255, 255, 255))
                casino_font.render_to(screen, (10, 60), "close to 21 without going over. If you go over 21 you lose, same", (255, 255, 255))
                casino_font.render_to(screen, (10, 110), "applies for the dealer. If you both go over 21, you lose. Cards 2-10", (255, 255, 255))
                casino_font.render_to(screen, (10, 160), "are worth their value. Jack, Queen and King are worth 10. Aces can", (255, 255, 255))
                casino_font.render_to(screen, (10, 210), "be worth 1 or 11 depending on what benefits the player more", (255, 255, 255))
                casino_font.render_to(screen, (10, 260), "Click to start. Click ESC to exit and type to choose bet.", (255, 255, 255))
                if clciked:
                    game['vars']['read'] = True
    elif game['type'] == "TEMPE":
        screen.fill((0, 0, 0))
        casino_font.render_to(screen, (10, 10), str(game['objects']['WTR']), (255, 255, 255))
        for key in pressing:
            if key in ['CAPSLOCK', '-', ' ']: continue
            if key == 'backspace':
                game['objects']['WTR'] = 0
            else:
                game['objects']['WTR'] *= 10
                game['objects']['WTR'] += key
        casino_font.render_to(screen, (10, 60),
            f"Your Casino Chips: ${current['CasinoChips']}", (255, 255, 255))
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(10, 110, 150, 50))
        casino_font.render_to(screen, (20, 120), "Recieve")
        if pg.Rect(10, 110, 150, 50).collidepoint(mouse) and clciked:
            current['CasinoChips'] += game['objects']['WTR']
        if keys[pg.K_ESCAPE]: game['on'] = False
        casino_font.render_to(screen, (10, 250), "ESC to exit", (255, 255, 255))
    return fps