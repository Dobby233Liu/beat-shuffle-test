import pydub
import random
import math
import sys

BEATS = 128
assert(BEATS % 4 == 0)

def get_random_beat_pattern():
    ret = list(range(BEATS))
    random.shuffle(ret)
    return ret

def get_song_seg(songdata):
    return pydub.AudioSegment.from_file(songdata["fn"], songdata["ff"])

def s_to_ms(n):
    return math.floor(n * 1000)

def each_beat_takes_seconds(bpm):
    return round(60 / bpm / (BEATS / 4) * 1000) / 1000

def arrange_like(origin, example):
    assert(len(origin) == len(example))

    ret = []
    for i in example:
        ret.append(origin[i])

    return ret

def russian_roulette():
    return random.randint(1, 6) == 4
def chaos(seg):
    if russian_roulette():
        return seg.reverse()
    return seg

def shuffle_beats(songdata):
    buf = get_song_seg(songdata)
    new_aud = pydub.AudioSegment.empty()

    pat = get_random_beat_pattern()
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"]))
    print(slicing_portion)

    if "start" in songdata:
        buf = buf[s_to_ms(songdata["start"]):]
    if "end" in songdata:
        buf = buf[:-s_to_ms(songdata["end"])]
    supposed_len = len(buf)

    while len(buf) > 0:
        segs = []
        for beat in range(BEATS):
            cutoff = slicing_portion
            seg = buf[:cutoff]
            buf = buf[cutoff:]
            seg = chaos(seg.apply_gain(-seg.max_dBFS).remove_dc_offset())
            segs.append(seg)
        segs = arrange_like(segs, pat)
        for part in segs:
            new_aud = new_aud.append(chaos(part), crossfade=0)
        pat = get_random_beat_pattern()

    new_aud = chaos(new_aud.apply_gain(-new_aud.max_dBFS).remove_dc_offset())
    assert(len(new_aud) == supposed_len)

    return new_aud

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + songdata["fn"]
    out.export(fn, format=songdata["ff"])
    return fn
