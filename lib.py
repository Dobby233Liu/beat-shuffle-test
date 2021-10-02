import pydub
import math

BEATS = 4
CF_AMOUNT = 10

def get_song_seg(songdata):
    r = pydub.AudioSegment.from_file(songdata["fn"], songdata["ff"])
    if r.channels == 1:
        r = pydub.AudioSegment.from_mono_audiosegments(r, r)
    return r

def s_to_ms(n, rounding=math.floor):
    # As for now this seems to be a good choice.
    # I'm battling this $4!7 during testing BIG SHOT
    return rounding(n * 1000)

def each_beat_takes_seconds(bpm):
    return 60 / bpm

def arrange_like(origin, example):
    assert(len(origin) == len(example))

    ret = []
    for i in example:
        ap = None
        if i <= 0 or i > len(origin):
            ap = pydub.AudioSegment.empty()
        else:
            ap = origin[i - 1]
        ret.append(ap)

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
    supposed_len = len(buf)
 
    pat = [1, 4, 3, 2]
    if "new_order" in songdata:
        pat = songdata["new_order"]
    assert(len(pat) == beats)
    slice_portion = s_to_ms(each_beat_takes_seconds(songdata["bpm"]))
    if "beat_delay" in songdata:
        slice_portion = slice_portion + s_to_ms(songdata["beat_delay"])
    cf_amount = CF_AMOUNT
    if "crossfade" in songdata:
        cf_amount = songdata["crossfade"]

    while len(buf) > 0:
        segs = []
        for beat in range(beats):
            seg = buf[:slice_portion]
            buf = buf[slice_portion:]
            seg = normalize(seg)
            segs.append(seg)
        segs = arrange_like(segs, pat)
        for part in segs:
            crossfade = cf_amount
            if (len(new_aud) < crossfade) or (len(part) < crossfade):
                crossfade = 0
            new_aud = new_aud.append(part, crossfade=crossfade)

    if _temp_endbuf is not None:
        crossfade = cf_amount
        if len(new_aud) < crossfade:
            crossfade = 0
        new_aud = new_aud.append(_temp_endbuf, crossfade=crossfade)

    assert((cf_amount != 0) or (len(new_aud) == supposed_len))
    new_aud = normalize(new_aud)

    return new_aud

def shuffle_beats(songdata):
    songseg = get_song_seg(songdata)
    songseg = _shuffle_beats(songdata, songseg, beats=songdata.get("beats", BEATS))
    return songseg

def shuffle_beats_and_export(songdata):
    out = shuffle_beats(songdata)
    fn = "shuffled_" + songdata["fn"]
    out.export(fn, format=songdata["ff"])
    return fn
