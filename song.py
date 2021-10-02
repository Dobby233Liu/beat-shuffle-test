import random

song = {}

song["fn"] = "spamton_neo_mix_ex_wip.ogg" # BIG SHOT
song["ff"] = "ogg"

song["bpm"] = 140 # beat per minute

order = [1, 2, 3, 4]
def new_order():
    random.shuffle(order)
    return order, True

song["new_order"] = new_order
