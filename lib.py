import pydub
import random
import sys

BEATS = 4

def get_random_beat_pattern():
    #ret = list(range(BEATS))
    #random.shuffle(ret)
    #return ret
    return [i - 1 for i in [1, 4, 3, 2]] # Guaranteed random with [[Hyperlink Blocked]]

def get_song_seg(songdata):
    return pydub.AudioSegment.from_file(songdata["fn"], songdata["ff"])

def s_to_ms(n):
    return n * 1000

def each_beat_takes_seconds(bpm):
    return 60 / bpm

def arrange_like(origin, example):
    if len(origin) != len(example):
        raise Exception("no")
    ret = []
    for i in example:
        ret.append(origin[i])
    return ret

def shuffle_beats(songdata):
    origin_aud = get_song_seg(songdata)
    new_aud = pydub.AudioSegment.empty()

    pat = get_random_beat_pattern()
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"]))
    #if len(origin_aud) % slicing_portion != 0: # add padding
    #    origin_aud = origin_aud + pydub.AudioSegment.silent(duration=(slicing_portion - (len(origin_aud) % slicing_portion)))
    rest_ms = len(origin_aud)
    seek = 0
    if songdata["start"] is not None:
        seek = s_to_ms(songdata["start"])

    while rest_ms > 0:
        segs = []
        for _ in range(BEATS):
            start_seek = seek
            seek = seek + slicing_portion
            if (seek - start_seek) > rest_ms:
                seek = rest_ms
                rest_ms = 0
            else:
                rest_ms = rest_ms - slicing_portion
            seg = origin_aud[start_seek:seek]
            seg = seg.apply_gain(-seg.max_dBFS)
            segs.append(seg)
        segs = arrange_like(segs, pat)
        for seg in segs:
            new_aud = new_aud + seg

    new_aud = new_aud.apply_gain(-new_aud.max_dBFS)

    return new_aud, [i + 1 for i in pat]

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + ''.join([str(i) for i in out[1]]) + "_" + songdata["fn"] + (songdata["ff"] != "ogg" and ".ogg" or "")
    out[0].export(fn, format="ogg")
    return fn
