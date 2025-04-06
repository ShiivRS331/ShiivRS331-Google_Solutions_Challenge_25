import numpy as np
import scipy.signal as signal
import librosa

# Define Indian musical notes and their frequencies (octaves 2-6)
NOTES = {
    "2": {
        "S": 65.41, "r1": 69.30, "r2": 73.42, "g1": 77.78, "g2": 82.41,
        "m1": 87.31, "m2": 92.50, "P": 98.00, "d1": 103.83, "d2": 110.00,
        "n1": 116.54, "n2": 123.47, "S'": 130.81
    },
    "3": {
        "S": 130.81, "r1": 138.59, "r2": 146.83, "g1": 155.56, "g2": 164.81,
        "m1": 174.61, "m2": 185.00, "P": 196.00, "d1": 207.65, "d2": 220.00,
        "n1": 233.08, "n2": 246.94, "S'": 261.63
    },
    "4": {
        "S": 261.63, "r1": 277.18, "r2": 293.66, "g1": 311.13, "g2": 329.63,
        "m1": 349.23, "m2": 369.99, "P": 392.00, "d1": 415.30, "d2": 440.00,
        "n1": 466.16, "n2": 493.88, "S'": 523.25
    },
    "5": {
        "S": 523.25, "r1": 554.37, "r2": 587.33, "g1": 622.25, "g2": 659.25,
        "m1": 698.46, "m2": 739.99, "P": 783.99, "d1": 830.61, "d2": 880.00,
        "n1": 932.33, "n2": 987.77, "S'": 1046.50
    },
    "6": {
        "S": 1046.50, "r1": 1108.73, "r2": 1174.66, "g1": 1244.51, "g2": 1318.51,
        "m1": 1396.91, "m2": 1479.98, "P": 1567.98, "d1": 1661.22, "d2": 1760.00,
        "n1": 1864.66, "n2": 1975.53, "S'": 2093.00
    }
}

def find_nearest_note(freq):
    """Find the nearest musical note and octave to a given frequency."""
    if freq <= 0:
        return None, None

    min_dist = float('inf')
    nearest_note = None
    nearest_octave = None

    for octave, notes in NOTES.items():
        for note, note_freq in notes.items():
            dist = abs(freq - note_freq)
            if dist < min_dist:
                min_dist = dist
                nearest_note = note
                nearest_octave = octave
    return nearest_note, nearest_octave

def detect_note(audio_data, sample_rate):
    """Detect the dominant frequency and corresponding note in audio data."""
    if len(audio_data) < 256:
        return None, None, None

    frequencies, magnitudes = signal.welch(audio_data, sample_rate, nperseg=512)
    window_size = 3
    magnitudes_smooth = np.convolve(magnitudes, np.ones(window_size) / window_size, mode='same')
    dominant_frequency = frequencies[np.argmax(magnitudes_smooth)]

    note, octave = find_nearest_note(dominant_frequency)
    return dominant_frequency, note, octave

def process_audio_file(audio_file):
    y, sr = librosa.load(audio_file)
    note_data_file = []
    octave_data_file = []
    freq_data_file = []
    time_step = 0.05
    for i in range(0, len(y), int(sr * time_step)):
        audio_segment = y[i:i + int(sr * time_step)]
        if len(audio_segment) > int(sr * time_step * .75):
            freq, note, octave = detect_note(audio_segment, sr)
            if note:
                note_data_file.append(note)
                octave_data_file.append(octave)
                freq_data_file.append(freq)
    return note_data_file, octave_data_file, freq_data_file

# Load audio file and extract notes
audio_file_path = "C:\\Users\\rsshi\\OneDrive\\Desktop\\GDSC'25\\kal.mp3"
note_data_file, octave_data_file, freq_data_file = process_audio_file(audio_file_path)

# Create an array of notes and frequencies for the full song, grouped into rows of 7
full_song_notes_array = []
for i in range(0, len(note_data_file), 7):
    row = []
    for j in range(i, min(i + 7, len(note_data_file))):
        if note_data_file[j] and octave_data_file[j]:
            row.append(f"{note_data_file[j]} ({octave_data_file[j]}) - {freq_data_file[j]:.2f} Hz")
        else:
            row.append(None) # or some other placeholder for no note detected
    full_song_notes_array.append(row)

# Print the array of notes and frequencies
print("Notes and Frequencies in kal.mp3 (grouped by 7):")
for row in full_song_notes_array:
    print(row)