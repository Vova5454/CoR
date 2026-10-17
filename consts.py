import os


WIDTH = 800
HEIGHT = 600
FPS = 30
SAMP_CAP = 10
minb, maxb = 5, 5
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

def file_thing(v):
    return v

save_folder = os.environ.get("LOCALAPPDATA")
if not save_folder:
    save_folder = os.path.join(os.path.expanduser("~"), "AppData", "Local")
save_folder = os.path.join(save_folder, "CoR")
os.makedirs(save_folder, exist_ok=True)