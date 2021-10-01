import pydub
import random
import math
import sys

BEATS = 4

def get_random_beat_pattern(beats=BEATS):
    #r = list(range(beats))
    #random.shuffle(r)
    #return r
    r = [1,4,3,2]
    r = [i - 1 for i in r]
    return r

def get_song_seg(songdata):
    r = pydub.AudioSegment.from_file(songdata["fn"], songdata["ff"])
    if r.channels == 1:
        r = pydub.AudioSegment.from_mono_audiosegments(r, r)
    return r

def s_to_ms(n):
    return math.floor(n * 1000)

def each_beat_takes_seconds(bpm, beats=BEATS):
    return round(60 / bpm / (beats / 4) * 1000) / 1000

def arrange_like(origin, example):
    assert(len(origin) == len(example))

    ret = []
    for i in example:
        ret.append(origin[i])

    return ret

def normalize(seg):
    return seg.normalize().remove_dc_offset()

def _shuffle_beats(songdata, songseg, beats=BEATS):
    buf = songseg
    new_aud = pydub.AudioSegment.empty()

    if "start" in songdata:
        buf = buf[s_to_ms(songdata["start"]):]
    if "end" in songdata:
        buf = buf[:-s_to_ms(songdata["end"])]
    supposed_len = len(buf)
 
    pat = get_random_beat_pattern(beats=beats)
    slicing_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"], beats=beats))# - 1

    while len(buf) > 0:
        segs = []
        for beat in range(beats):
            cutoff = slicing_portion
            seg = buf[:cutoff]
            buf = buf[cutoff:]
            seg = normalize(seg)
            _mseg = seg.split_to_mono()
            segs.append([seg, _mseg[0].max_dBFS, _mseg[1].max_dBFS])
        _old_segs = segs
        segs = arrange_like(segs, pat)
        for part in range(len(segs)):
            real_part = segs[part][0].apply_gain_stereo(-_old_segs[part][1], -_old_segs[part][2])
            new_aud = new_aud.append(real_part, crossfade=((len(new_aud) == 0 or len(part) == 0) and 0 or 5))

    return normalize(new_aud)

def shuffle_beats(songdata):
    songseg = get_song_seg(songdata)
    songseg = _shuffle_beats(songdata, songseg, beats=BEATS)
    return songseg

def shuffle_beats_and_export(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + songdata["fn"]
    out.export(fn, format=songdata["ff"])
    return fn
