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
    return bpm / 60

def guess_bpm(seg):
    # reduce loudness of sounds over 120Hz (focus on bass drum, etc)
    seg = seg.low_pass_filter(120.0)

    # we'll call a beat: anything above average loudness
    beat_loudness = seg.dBFS 

    # the fastest tempo we'll allow is 240 bpm (60000ms / 240beats)
    minimum_silence = int(60000 / 240.0)

    nonsilent_times = pydub.silence.detect_nonsilent(seg, minimum_silence, beat_loudness)

    spaces_between_beats = []
    last_t = nonsilent_times[0][0]

    for peak_start, _ in nonsilent_times[1:]:
        spaces_between_beats.append(peak_start - last_t)
        last_t = peak_start

    # We'll base our guess on the median space between beats
    spaces_between_beats = sorted(spaces_between_beats)
    space = spaces_between_beats[len(spaces_between_beats) / 2]

    return 60000 / space

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
    slicing_portion = s_to_ms(each_beat_takes_seconds(guess_bpm(origin_aud)))
    if len(origin_aud) % slicing_portion != 0: # add padding
        origin_seg = origin_aud + pydub.AudioSegment.silent(duration=(slicing_portion - (len(origin_aud) % slicing_portion)))
    rest_ms = len(origin_aud)
    seek = 0

    while rest_ms > 0:
        segs = []
        for _ in range(BEATS):
            start_seek = seek
            seek = seek + slicing_portion
            rest_ms = rest_ms - slicing_portion
            segs.append(origin_seg[start_seek:seek])
        segs = arrange_like(segs, pat)
        for seg in segs:
            new_aud = new_aud + seg

    return new_aud, [i + 1 for i in pat]

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + ''.join([str(i) for i in out[1]]) + "_" + songdata["fn"] + (songdata["ff"] != "ogg" and ".ogg" or "")
    out[0].export(fn, format="ogg")
    return fn
