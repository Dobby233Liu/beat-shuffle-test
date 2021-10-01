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
    return round(n * 1000)

def each_beat_takes_seconds(bpm):
    return 60 / bpm

def arrange_like(origin, example):
    assert(len(origin) == len(example))

    ret = []
    for i in example:
        ret.append(origin[i])

    return ret

def shuffle_beats(songdata):
    buf = get_song_seg(songdata)
    new_aud = pydub.AudioSegment.empty()

    pat = get_random_beat_pattern()
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"]))
    print(pat)
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
            if cutoff > (len(buf)-1):
                cutoff = (len(buf)-1)
                print(str(beat) + ": " + "REMAINDER FAILSAFE")
            seg = buf[:cutoff]
            buf = buf[cutoff:]
            seg = seg.apply_gain(-seg.max_dBFS).remove_dc_offset()
            segs.append(seg)
        segs = arrange_like(segs, pat)
        for part in segs:
            new_aud = new_aud.append(part, crossfade=0)

    new_aud = new_aud.apply_gain(-new_aud.max_dBFS).remove_dc_offset()
    assert(len(new_aud) == supposed_len)

    return new_aud, [i + 1 for i in pat]

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + ''.join([str(i) for i in out[1]]) + "_" + songdata["fn"]
    out[0].export(fn, format=songdata["ff"])
    return fn
