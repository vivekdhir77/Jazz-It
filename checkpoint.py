import json
from pydub import AudioSegment
import io
import librosa
import numpy as np
import random
import soundfile as sf

json_path = "./Data/JSON/"
song_path = "./Data/Songs/"
OUTPUT_PATH = "./Outputs/"
fileName = "More"
fileNo = "1"
f = open(json_path+fileName+".json")
Chords_Half_Bars = json.loads(f.read())

chord_progression = ['C', 'C', 'C']

sample = []
for chord in chord_progression:
    if chord in Chords_Half_Bars.keys():
        sample.append(random.choice(Chords_Half_Bars[chord]))
    else:
        pass
print(sample)

def create_new_song(file_path, sample_half_bars):
    y, sr = librosa.load(file_path)
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    half_bar_duration = 2 * (beat_times[1] - beat_times[0])  # 2 beats per half-bar
    
    new_song = np.array([])
    
    for half_bar in sample_half_bars:
        start_time = (half_bar - 1) * half_bar_duration
        end_time = half_bar * half_bar_duration
        
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        
        half_bar_audio = y[start_sample:end_sample]
        new_song = np.concatenate((new_song, half_bar_audio))
        # new_song = np.tile(new_song, 2)
    return new_song, sr

new_song, sr = create_new_song(song_path+f"{fileName}.mp3", sample)
byte_stream = io.BytesIO()
sf.write(byte_stream, new_song, sr, format='wav')
byte_stream.seek(0)

audio_segment = AudioSegment.from_wav(byte_stream)

audio_segment.export(OUTPUT_PATH+f"{fileName}{fileNo}.mp3", format="mp3")

print(f"New song created and saved as '{fileName}{fileNo}.mp3'")