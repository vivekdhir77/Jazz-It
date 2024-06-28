# from pydub import AudioSegment
import io
import librosa
import numpy as np
import random
import json

def analyze_song(file_path):
    y, sr = librosa.load(file_path)
    
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = round(float(tempo))
    
    y_harmonic = librosa.effects.harmonic(y)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
    
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    
    major_template = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
    minor_template = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0])
    
    chords = []
    for i in range(0, len(beat_frames) - 2, 2):  # Changed from 4 to 2 for half bars
        half_bar_chroma = np.mean(chroma[:, beat_frames[i]:beat_frames[i+2]], axis=1)
        
        half_bar_chroma = half_bar_chroma / np.sum(half_bar_chroma)
        
        correlations = []
        for j in range(12):
            major_corr = np.correlate(half_bar_chroma, np.roll(major_template, j))
            minor_corr = np.correlate(half_bar_chroma, np.roll(minor_template, j))
            correlations.append((major_corr[0], 'major'))
            correlations.append((minor_corr[0], 'minor'))
        
        best_match = max(correlations, key=lambda x: x[0])
        chord_index = correlations.index(best_match) // 2
        chord_type = best_match[1]
        
        chord_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][chord_index]
        if chord_type == 'minor':
            chord_name += 'm'
        
        chords.append(chord_name)
    
    return bpm, chords

SongName ="beat2"

song_path = "./Data/Songs/"
data_path = "./Data/JSON/"
fileNo = ""
bpm, chords = analyze_song(song_path+f"{SongName}.mp3")
print(f"BPM: {bpm}")
print("Chords for each half bar:")
Chords_Half_Bars = {}
for i, chord in enumerate(chords):
    half_bar_number = i + 1
    bar_number = (i // 2) + 1
    half_bar_position = 'first half' if i % 2 == 0 else 'second half'
    
    print(f"Bar {bar_number} ({half_bar_position}): {chord}", end=", ")
    
    try:
        Chords_Half_Bars[chord].append(half_bar_number)
    except KeyError:
        Chords_Half_Bars[chord] = [half_bar_number]

print("\n\nChords and their occurrences (by half bar numbers):")
for chord, occurrences in Chords_Half_Bars.items():
    print(f"{chord}: {occurrences}")

def save_dict_to_json(dictionary, filename):
    with open(filename, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)

save_dict_to_json(Chords_Half_Bars, data_path+f'{SongName}{fileNo}.json')
