import random

song = {}

song["fn"] = "spamton_neo_mix_ex_wip.ogg" # BIG SHOT
song["ff"] = "ogg"

song["bpm"] = 140 * 2 # beat per minute
song["beats"] = 4 * 2 # fake beat number to split more segments

# Spamton had a stroke
def new_order(tick):
    return [random.randint(0, 8) for i in range(8)], True
song["new_order"] = new_order
song["crossfade"] = 5
