import pydub
import random
import math
import sys

BEATS = [32,16,8,4,2,1]

def get_random_beat_pattern(beats=BEATS[0]):
    ret = list(range(beats))
    random.shuffle(ret)
    return ret

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

def russian_roulette():
    return random.randint(1, 6) == 4
def chaos(seg):
    if russian_roulette():
        return seg.reverse()
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
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"], beats=beats))

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
            new_aud = new_aud.append((tot % (beats / 4) == 0 and chaos(part) or part), crossfade=0)
        pat = get_random_beat_pattern(beats=beats)

    new_aud = chaos(new_aud)

    return new_aud
def shuffle_beats(songdata):
    songseg = get_song_seg(songdata)
    dir = 0
    beats = BEATS[dir]
    while beats > 1:
        songseg = _shuffle_beats(songdata, songseg, beats=beats)
        dir = dir + 1
        beats = BEATS[dir]
    return songseg

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + songdata["fn"]
    out.export(fn, format=songdata["ff"])
    return fn
