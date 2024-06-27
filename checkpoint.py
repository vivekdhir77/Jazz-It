import json
from pydub import AudioSegment
import io
import librosa
import numpy as np
import random
import soundfile as sf

json_path = "./Data/JSON/"
song_path = "./Data/Songs/"
OUTPUT_PATH = "./Output2/"
fileName = "DraftPunk"
fileNo = ""
f = open(json_path+fileName+".json")
Chords_Bars = json.loads(f.read())

chord_progression = ["G", "D", "A#", "C#", "G", "D", "F#", "G"]

sample = []
for chord in chord_progression:
    if chord in Chords_Bars.keys():
        sample.append(random.choice(Chords_Bars[chord]))
    else:
        pass
print(sample)
def create_new_song(file_path, sample_bars):
    y, sr = librosa.load(file_path)
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames') # BPM 
    
    
    beat_times = librosa.frames_to_time(beat_frames, sr=sr) # Converting beat frames to time
    
   
    bar_duration = 4 * (beat_times[1] - beat_times[0]) # 4 beats per bar
    
    # Creating a new audio array
    new_song = np.array([])
    
    for bar in sample_bars:
        start_time = (bar - 1) * bar_duration
        end_time = bar * bar_duration
        
        start_sample = int(start_time * sr) # Converting time to samples
        end_sample = int(end_time * sr)
        
        # Extracting the bar from the original song
        bar_audio = y[start_sample:end_sample]
        new_song = np.concatenate((new_song, bar_audio))
    
    return new_song, sr

new_song, sr = create_new_song(song_path+f"{fileName}.mp3", sample)
byte_stream = io.BytesIO() # this will have it in wav format
sf.write(byte_stream, new_song, sr, format='wav')
byte_stream.seek(0)


audio_segment = AudioSegment.from_wav(byte_stream)# Creating an AudioSegment from the bytes object


audio_segment.export(OUTPUT_PATH+f"{fileName}{fileNo}.mp3", format="mp3") # Exporting as MP3

print(f"New song created and saved as '{fileName}.mp3'")