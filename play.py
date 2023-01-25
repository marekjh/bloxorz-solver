import pyautogui
import json
from solve import solve
import time
import os

def main():
    key = {"U": "up", "D": "down", "R": "right", "L": "left"}
    time.sleep(2)
    for filename in os.listdir("levels"):
        for step in solve(get_level(filename)):
            pyautogui.press(key[step], interval=0.3)
        time.sleep(6)

def get_level(filename):
    with open(os.path.join("levels", filename)) as f:
        level = json.load(f)
        level["start"] = tuple(level["start"])
        level["objectives"] = {k: tuple(v) for k, v in level["objectives"].items()}
        level["bridges"] = {k: [tuple(e) for e in v] for k, v in level["bridges"].items()}
        level["map"] = [list(s) for s in level["map"]]
        return level
        
main()
    
