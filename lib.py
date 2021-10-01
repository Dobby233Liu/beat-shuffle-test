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
    origin_aud = get_song_seg(songdata)
    new_aud = pydub.AudioSegment.empty()

    pat = get_random_beat_pattern()
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"]))
    print(pat)
    print(slicing_portion)

    #if len(origin_aud) % slicing_portion != 0: # add padding
    #    origin_aud = origin_aud + pydub.AudioSegment.silent(duration=(slicing_portion - (len(origin_aud) % slicing_portion)))

    supposed_len = len(origin_aud)
    seek = 0
    if "start" in songdata:
        seek = s_to_ms(songdata["start"])
        supposed_len = supposed_len - seek
    if "end" in songdata:
        supposed_len = supposed_len - s_to_ms(songdata["end"])

    while len(new_aud) < supposed_len:
        segs = []
        for beat in range(BEATS):
            start_seek = seek
            seek = seek + slicing_portion
            if (seek - start_seek) == 0:
                print(str(beat) + ": " + "appending nothing")
                segs.append(pydub.AudioSegment.empty())
                continue
            if seek > supposed_len - 1:
                seek = supposed_len - 1
                print(str(beat) + ": " + "REMAINDER FAILSAFE, seek set to %d" % seek)
            assert(not (seek < 0 or seek < start_seek))
            seg = origin_aud[start_seek:seek]
            seg = seg.apply_gain(-seg.max_dBFS).remove_dc_offset()
            segs.append(seg)
            print(str(beat) + ": " + "%d:%d" % (start_seek, seek))
        segs = arrange_like(segs, pat)
        for part in segs:
            new_aud = new_aud.append(part, crossfade=0)

    new_aud = new_aud.apply_gain(-new_aud.max_dBFS).remove_dc_offset()

    return new_aud, [i + 1 for i in pat]

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + ''.join([str(i) for i in out[1]]) + "_" + songdata["fn"]
    out[0].export(fn, format=songdata["ff"])
    return fn
