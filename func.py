import os
import sys
import json
import pygame.freetype as pgft
from consts import save_folder


pgft.init()

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
    "legend": False,
    "inventory": [],
    "got_key": False,
    "CasinoChips": 0
}

def save(savefile, data=None):
    path = os.path.join(save_folder, savefile)
    if data is None:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def file_thing(path):
    clean_path = path.replace("\\", "/")
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, clean_path)

if not os.path.exists(os.path.join(save_folder, "settings.json")):
    save("settings.json", {"sfx": 0.5, "mus": 0.5, "samp": 1})
    settings = {"sfx": 0.5, "mus": 0.5, "samp": 1}
else:
    settings = save("settings.json")
    if settings.get('sfx', []) == []: settings['sfx'] = 0.5
    if settings.get('mus', []) == []: settings['mus'] = 0.5
    if settings.get('samp', []) == []: settings['samp'] = 1
    save('settings.json', settings)

sfx = settings['sfx']
mus = settings['mus']
samp = settings['samp']

def cv(v):
    if v > 255: return 255
    if v < 0: return 0
    return v

def animate(frames, frame):
    frame += 1
    if frame == len(frames):
        frame = 0
    return frames[frame]

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

def setup_dialogue(self, text, diaID=0, your_options=[],
                   font=pgft.SysFont(None, 36), name=None):
    self['on'] = True
    self['font'] = font
    self['text'] = text
    self['name'] = name
    if not diaID:
        return
    self['your_options'] = your_options
    self['diaID'] = diaID

def fill_out_six_files(six_files):
    for i in range(256):
        for j in range(6):
            if os.path.exists(os.path.join(save_folder, f"data{j+1+6*i}.json")):
                six_files[i][j] = save(f"data{j+1+6*i}.json")
            else:
                six_files[i][j] = {}

def setup_game(game, g_type, g_id, objects={}, groups={}, g_vars={}, consts={}):
    game['on'] = True
    game['objects'] = objects
    game['groups'] = groups
    game['vars'] = g_vars
    game['consts'] = consts
    game['ID'] = g_id
    game['type'] = g_type

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