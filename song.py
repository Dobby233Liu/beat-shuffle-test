import random

song = {}

song["fn"] = "spamton_neo_mix_ex_wip.ogg" # BIG SHOT
song["ff"] = "ogg"

song["bpm"] = 140 # beat per minute

choices = [1, 2, 3, 4, 0]
def new_order():
    random.shuffle(choices)
    return choices[:4], True

song["new_order"] = new_order
