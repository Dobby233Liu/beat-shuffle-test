import pydub
import random

def get_random_beat_pattern():
    return random.shuffle([1,2,3,4])

def get_song_seg(songdata):
    return AudioSegment.from_file(songdata["fn"], songdata["ff"])
