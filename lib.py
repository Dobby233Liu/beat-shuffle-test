import pydub
import random
import math
import sys

BEATS = [4]

def get_random_beat_pattern(beats=BEATS[0]):
    #r = list(range(beats))
    #random.shuffle(r)
    #return r
    r = [1,4,3,2]
    r = [i - 1 for i in r]
    return r

def get_song_seg(songdata):
    return pydub.AudioSegment.from_file(songdata["fn"], songdata["ff"])

def s_to_ms(n):
    return math.floor(n * 1000)

def each_beat_takes_seconds(bpm, beats=BEATS[0]):
    return round(60 / bpm / (beats / 4) * 1000) / 1000

def arrange_like(origin, example):
    assert(len(origin) == len(example))

    ret = []
    for i in example:
        ret.append(origin[i])

    return ret

def russian_roulette(s=None):
    return False
def chaos(seg):
    return seg

def _shuffle_beats(songdata, songseg, beats=BEATS[0]):
    buf = songseg
    new_aud = pydub.AudioSegment.empty()

    if "start" in songdata:
        buf = buf[s_to_ms(songdata["start"]):]
    if "end" in songdata:
        buf = buf[:-s_to_ms(songdata["end"])]
    supposed_len = len(buf)
 
    pat = get_random_beat_pattern(beats=beats)
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"], beats=beats)) - 1

    tot = 0
    while len(buf) > 0:
        tot = tot + 1
        segs = []
        for beat in range(beats):
            cutoff = slicing_portion
            seg = buf[:cutoff]
            buf = buf[cutoff:]
            segs.append(seg)
        segs = arrange_like(segs, pat)
        for part in segs:
            new_aud = new_aud.append(part, crossfade=5)
        pat = get_random_beat_pattern(beats=beats)

    return new_aud

def shuffle_beats(songdata):
    songseg = get_song_seg(songdata)
    songseg = _shuffle_beats(songdata, songseg, beats=BEATS[0])
    return songseg

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + songdata["fn"]
    out.export(fn, format=songdata["ff"])
    return fn
