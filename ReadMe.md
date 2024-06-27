## Song Sampler

          conda version : 24.4.0
    conda-build version : not installed
         python version : 3.12.3.final.0
                 solver : libmamba (default)
       virtual packages : __archspec=1=cannonlake
                          __conda=24.4.0=0
                          __osx=10.16=0
                          __unix=0=0

This code is designed to generate a sample given song and predefined chord progression. Below is an explanation of the code, its functionality, and the libraries used.

## Code Functionality

### 1. Importing Libraries
The following libraries are used in the code:
- `pydub`: For handling audio file operations.
- `io`: For handling file input and output.
- `librosa`: For music and audio analysis.
- `numpy`: For numerical operations.
- `random`: For random sampling.
- `json`: For handling JSON data.

### 2. Defining the `analyze_song` Function
The `analyze_song` function is the core of the code, performing the following tasks:
- **Loading the Audio File**: Uses `librosa.load` to load the audio file from the given file path.
- **Estimating BPM**: Uses `librosa.beat.beat_track` to estimate the beats per minute (BPM) of the song.
- **Extracting Harmonic Content**: Uses `librosa.effects.harmonic` to isolate the harmonic content from the audio signal.
- **Computing Chroma Features**: Uses `librosa.feature.chroma_cqt` to compute chroma features, which represent the harmonic content.
- **Estimating Beat Frames**: Uses `librosa.beat.beat_track` to identify the beat frames in the song.
- **Identifying Chords**: Attempts to identify the chords for each bar by correlating chroma features with predefined chord templates.

### 3. Analyzing the Song
The code uses an example file path `./song.mp3` to analyze a song:
- **Printing BPM and Chords**: It prints the estimated BPM and the chords identified for each bar.

### 4. Creating a Dictionary of Chords and Bars
The code creates a dictionary `Chords_Bars` that maps each chord to the bars where it appears in the song.

### 5. Predefined Chord Progression
A predefined chord progression `["C", "Am", "F", "G"]` is used to sample bars from the analyzed song.

### 6. Suggesting a New Song
Based on the sampled bars, the code suggests creating a new song using the bars that match the predefined chord progression.
