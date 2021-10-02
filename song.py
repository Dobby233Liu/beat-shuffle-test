import random

song = {}

song["fn"] = "berdly_chase.ogg" # Smart Race
song["ff"] = "ogg"

song["bpm"] = 150 # beat per minute

def new_order(tick):
    ret = [1, 4, 3, 2]
    if tick % 9 > 4:
        ret = [3, 2, 1, 4]
    return ret, True
song["new_order"] = new_order
