import random

song = {}

song["fn"] = "spamton_neo_mix_ex_wip.ogg" # BIG SHOT
song["ff"] = "ogg"

song["bpm"] = 140 # beat per minute

def new_order(tick):
    ord = [random.choice([1, 2, 3, 4, 0]) for _ in range(4)]
    return ord, True

song["new_order"] = new_order
