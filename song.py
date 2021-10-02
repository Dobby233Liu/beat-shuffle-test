import random
from tqdm.auto import tqdm

song = {}

song["fn"] = "spamton_neo_mix_ex_wip.ogg" # BIG SHOT
song["ff"] = "ogg"

song["bpm"] = 140 # beat per minute

def new_order(tick):
    ord = [1, 2, 3, 4]
    start = (tick % (len(ord) + 1))
    ord = ord[start:-start]
    tqdm.write("start:%d ord:%s" % (start, str(ord)))
    random.shuffle(ord)
    return ord, True

song["new_order"] = new_order
