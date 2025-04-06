import numpy as np
import sounddevice as sd
import soundfile as sf
import scipy.signal as signal
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

# Define Indian musical notes and their frequencies
NOTES = {
    "2": {"S": 65.41, "r1": 69.30, "r2": 73.42, "g1": 77.78, "g2": 82.41,
          "m1": 87.31, "m2": 92.50, "P": 98.00, "d1": 103.83, "d2": 110.00,
          "n1": 116.54, "n2": 123.47, "S'": 130.81},
    "3": {"S": 130.81, "r1": 138.59, "r2": 146.83, "g1": 155.56, "g2": 164.81,
          "m1": 174.61, "m2": 185.00, "P": 196.00, "d1": 207.65, "d2": 220.00,
          "n1": 233.08, "n2": 246.94, "S'": 261.63},
    "4": {"S": 261.63, "r1": 277.18, "r2": 293.66, "g1": 311.13, "g2": 329.63,
          "m1": 349.23, "m2": 369.99, "P": 392.00, "d1": 415.30, "d2": 440.00,
          "n1": 466.16, "n2": 493.88, "S'": 523.25},
    "5": {"S": 523.25, "r1": 554.37, "r2": 587.33, "g1": 622.25, "g2": 659.25,
          "m1": 698.46, "m2": 739.99, "P": 783.99, "d1": 830.61, "d2": 880.00,
          "n1": 932.33, "n2": 987.77, "S'": 1046.50},
    "6": {"S": 1046.50, "r1": 1108.73, "r2": 1174.66, "g1": 1244.51, "g2": 1318.51,
          "m1": 1396.91, "m2": 1479.98, "P": 1567.98, "d1": 1661.22, "d2": 1760.00,
          "n1": 1864.66, "n2": 1975.53, "S'": 2093.00}
}

ALL_NOTES = [f"{note} ({octave})" for octave in NOTES for note in NOTES[octave]]
ALL_FREQS = [freq for octave in NOTES.values() for freq in octave.values()]

# Load the audio file
filename = "C:\\Users\\rsshi\\OneDrive\\Desktop\\GDSC'25\\circleoflife.wav"
audio_data, sample_rate = sf.read(filename, dtype="float32")
duration = len(audio_data) / sample_rate

# Plot setup
fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot([], [], marker="o", linestyle="-")
ax.set_yticks(ALL_FREQS)
ax.set_yticklabels(ALL_NOTES)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Notes")
ax.set_xlim(0, 5)

# Variables for tracking time & detected notes
time_data, freq_data, note_data, octave_data = [], [], [], []
start_time = None
prev_note, prev_octave = None, None

# Find the nearest note for a given frequency
def find_nearest_note(freq): ...

# Extract dominant note
def detect_note(audio_chunk):
    if len(audio_chunk) < 16:
        return None, None, None
    frequencies, magnitudes = signal.welch(audio_chunk, sample_rate, nperseg=min(1024, len(audio_chunk)))
    if len(magnitudes) == 0 or len(frequencies) == 0:
        return None, None, None
    dominant_index = np.argmax(magnitudes)
    if dominant_index >= len(frequencies):
        return None, None, None
    dominant_freq = frequencies[dominant_index]
    note, octave = find_nearest_note(dominant_freq)
    if note is None or octave is None:
        return None, None, None
    return dominant_freq, note, octave

# Animation update function
def update(frame):
    global time_data, freq_data, note_data, octave_data, start_time, prev_note, prev_octave
    if start_time is None:
        return
    elapsed_time = time.time() - start_time
    index = int(elapsed_time * sample_rate / 1024)
    if index < len(audio_data) // 1024:
        chunk = audio_data[index * 1024:(index + 1) * 1024]
        freq, note, octave = detect_note(chunk)
        if note and (note != prev_note or octave != prev_octave):
            time_data.append(elapsed_time)
            freq_data.append(freq)
            note_data.append(note)
            octave_data.append(octave)
            prev_note, prev_octave = note, octave
            line.set_data(time_data, [NOTES[o][n] for n, o in zip(note_data, octave_data) if o and n])
            ax.set_xlim(max(0, elapsed_time - 5), elapsed_time + 1)
            ax.set_ylim(min(ALL_FREQS), max(ALL_FREQS))
            plt.title(f"Current Note: {note} ({octave}), Frequency: {freq:.2f} Hz")

# Play audio and animate graph together
def play_audio():
    global start_time
    start_time = time.time()
    ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
    audio_thread = threading.Thread(target=lambda: sd.play(audio_data, sample_rate))
    audio_thread.start()
    plt.draw()
    plt.pause(0.1)
    plt.show()

# Start the visualization
play_audio()
