from pydub import AudioSegment
import io
import librosa
import numpy as np
import random
import json

def analyze_song(file_path):
    y, sr = librosa.load(file_path)
    
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)# Fining out beats per minute
    bpm = round(float(tempo)) 
    
    
    print("y: ", y)
    y_harmonic = librosa.effects.harmonic(y)# Extracting harmonic content
    print("y: ", y_harmonic)

    
    
    print("sr: ", sr)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)# Compute chroma features
    print("chroma: ", chroma)
    
    # Estimate beat frames
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    print("beat_frame: ", beat_frames)
    
    # Define chord templates
    major_template = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
    minor_template = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0])
    
    # Calculating chords for each bar
    chords = []
    for i in range(0, len(beat_frames) - 4, 4):
        bar_chroma = np.mean(chroma[:, beat_frames[i]:beat_frames[i+4]], axis=1)
        
        
        bar_chroma = bar_chroma / np.sum(bar_chroma)# Normalization of the chroma vector
        
       
        correlations = [] # Calculate correlation with major and minor templates
        for j in range(12):
            major_corr = np.correlate(bar_chroma, np.roll(major_template, j))
            minor_corr = np.correlate(bar_chroma, np.roll(minor_template, j))
            correlations.append((major_corr[0], 'major'))
            correlations.append((minor_corr[0], 'minor'))
        
        # Find the best match
        best_match = max(correlations, key=lambda x: x[0])
        chord_index = correlations.index(best_match) // 2
        chord_type = best_match[1]
        
        chord_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][chord_index]
        if chord_type == 'minor':
            chord_name += 'm'
        
        chords.append(chord_name)
    
    return bpm, chords

SongName ="DraftPunk"

song_path = "./Data/Songs/"
data_path = "./Data/JSON/"
bpm, chords = analyze_song(song_path+f"{SongName}.mp3")
print(f"BPM: {bpm}")
print("Chords for each bar:")
Chords_Bars = {}
for i, chord in enumerate(chords):
    print(f"Bar {i+1}: {chord}", end =", ")
    try:
        Chords_Bars[chord].append(i+1)
    except:
        Chords_Bars[chord] = [i+1]

def save_dict_to_json(dictionary, filename):
    with open(filename, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)

save_dict_to_json(Chords_Bars, data_path+f'{SongName}.json')
