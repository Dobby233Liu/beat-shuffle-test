import random

song = {}

song["fn"] = "spamton_neo_mix_ex_wip.ogg" # BIG SHOT
song["ff"] = "ogg"

song["bpm"] = 140 # beat per minute

choices = [1, 2, 3, 4, 0]
ord = [1, 2, 3, 4]
tick = 0
def new_order():
    tick = tick + 1
    if tick % 2 == 0:
        ord = [random.choice(choices) for _ in range(4)]
    return ord, True

song["new_order"] = new_order
