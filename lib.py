import pydub
import random
import math
import sys

BEATS = 4
CF_AMOUNT = 5

def get_random_beat_pattern(beats=BEATS):
    # r = list(range(beats))
    # random.shuffle(r)
    # return r
    r = [0, 3, 2, 1] # 1, 4, 3, 2
    return r

def get_song_seg(songdata):
    r = pydub.AudioSegment.from_file(songdata["fn"], songdata["ff"])
    if r.channels == 1:
        r = pydub.AudioSegment.from_mono_audiosegments(r, r)
    return r

def s_to_ms(n):
    return n * 1000

def each_beat_takes_seconds(bpm):
    return math.ceil(60 / bpm)

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
    _temp_endbuf = None
    new_aud = pydub.AudioSegment.empty()

    if "start" in songdata:
        new_aud.append(normalize(buf[:s_to_ms(songdata["start"])]), crossfade=0)
        buf = buf[s_to_ms(songdata["start"]):]
    if "end" in songdata:
        _temp_endbuf = normalize(buf[-s_to_ms(songdata["end"]):0])
        buf = buf[:-s_to_ms(songdata["end"])]
 
    pat = get_random_beat_pattern(beats=beats)
    assert(len(pat) == beats)
    slice_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"]))# - 1

    while len(buf) > 0:
        segs = []
        for beat in range(beats):
            seg = buf[:slice_portion]
            buf = buf[slice_portion:]
            seg = normalize(seg)
            _mseg = seg.split_to_mono()
            segs.append([seg, _mseg[0].max_dBFS, _mseg[1].max_dBFS])
        _old_segs = segs
        segs = arrange_like(segs, pat)
        for part in range(len(segs)):
            real_part = normalize(segs[part][0].apply_gain_stereo(-_old_segs[part][1], -_old_segs[part][2]))
            crossfade = CF_AMOUNT
            if (len(new_aud) < crossfade) or (len(real_part) < crossfade):
                crossfade = 0
            new_aud = new_aud.append(real_part, crossfade=crossfade)

    if _temp_endbuf is not None:
        crossfade = CF_AMOUNT
        if len(new_aud) < crossfade:
            crossfade = 0
        new_aud = new_aud.append(_temp_endbuf, crossfade=crossfade)

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
