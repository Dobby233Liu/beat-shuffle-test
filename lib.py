import pydub
import random
import math
import sys

BEATS = [32,16,8,4,2,1]

def get_random_beat_pattern(beats=BEATS[0]):
    r = list(range(beats))
    random.shuffle(r)
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

def russian_roulette(s=6):
    return random.randint(1, s) == (s / 2 + 1 * 2)
def chaos(seg):
    if russian_roulette(6):
        seg = seg.reverse()
    if russian_roulette(8):
        samples = seg.get_array_of_samples()
        r = random.randrange(0, len(samples), 2)
        samples[r] = random.randint(0,127)
        samples[r + 1] = random.randint(0,127)
        seg = seg._spawn(samples)
    if russian_roulette(12):
        samples = seg.get_array_of_samples()
        r = random.randrange(0, len(samples), 2)
        samples.pop(r)
        samples.pop(r)
        seg = seg._spawn(samples)
    if russian_roulette(24):
        seg = seg.compress_dynamic_range(random.uniform(-10, -2), random.uniform(1, 4))
    if russian_roulette(28):
        seg = seg.low_pass_filter(random.randint(8, 20))
    if russian_roulette(30):
        seg = seg.high_pass_filter(random.randint(8, 20))
    if russian_roulette(32):
        seg = seg.pan(random.uniform(-1, 1))
    if russian_roulette(34):
        seg = seg.apply_gain(random.uniform(-2, 8))
    if russian_roulette(36):
        seg = seg.apply_gain_stereo(random.uniform(-2, 8), random.uniform(-2, 8))
    if russian_roulette(100):
        samples = seg.get_array_of_samples()
        random.shuffle(samples)
        seg = seg._spawn(samples)
    return seg.normalize()

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
    for beats in BEATS:
        songseg = _shuffle_beats(songdata, songseg, beats=beats)
    return songseg

def make_lemonade(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + songdata["fn"]
    out.export(fn, format=songdata["ff"])
    return fn
