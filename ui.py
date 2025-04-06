import numpy as np
import sounddevice as sd
import scipy.signal as signal
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time

# Define Indian musical notes and their frequencies (4th octave)
NOTES = {
    "S": 261.63,  # C4
    "r1": 277.18,  # C#4/Db4
    "r2": 293.66,  # D4
    "g1": 311.13,  # D#4/Eb4
    "g2": 329.63,  # E4
    "m1": 349.23,  # F4
    "m2": 369.99,  # F#4/Gb4
    "P": 392.00,  # G4
    "d1": 415.30,  # G#4/Ab4
    "d2": 440.00,  # A4
    "n1": 466.16,  # A#4/Bb4
    "n2": 493.88,  # B4
    "S'": 523.25, #C5
}

NOTE_NAMES = list(NOTES.keys())
NOTE_FREQS = list(NOTES.values())

def find_nearest_note(freq):
    """Find the nearest musical note to a given frequency."""
    if freq <= 0:
        return None
    distances = [abs(f - freq) for f in NOTE_FREQS]
    nearest_index = distances.index(min(distances))
    return NOTE_NAMES[nearest_index]

def detect_note(audio_data, sample_rate):
    """Detect the dominant frequency and corresponding note in audio data."""
    if len(audio_data) == 0:
        return None, None

    frequencies, magnitudes = signal.welch(audio_data, sample_rate, nperseg=1024)
    dominant_frequency = frequencies[np.argmax(magnitudes)]
    note = find_nearest_note(dominant_frequency)
    return dominant_frequency, note

def audio_callback(indata, frames, time, status):
    """Callback function for audio input."""
    global audio_data
    if status:
        print(status)
    audio_data = indata.flatten()

def update_graph():
    """Update the graph with new audio data and detected notes."""
    global audio_data, time_data, note_data, freq_data
    if len(audio_data) > 0:
        freq, note = detect_note(audio_data, sample_rate)
        if note:
            time_data.append(time.time() - start_time)
            note_data.append(note)
            freq_data.append(freq)
            ax.clear()
            ax.plot(time_data, [NOTE_FREQS[NOTE_NAMES.index(n)] if n else 0 for n in note_data], marker='o', linestyle='-')
            ax.set_yticks(NOTE_FREQS)
            ax.set_yticklabels(NOTE_NAMES)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Notes")
            canvas.draw()
            detected_label.config(text=f"Detected Note: {note}, Frequency: {freq:.2f} Hz")

    root.after(100, update_graph) #update every 100ms

# Initialize global variables
audio_data = np.array([])
time_data = []
note_data = []
freq_data = []
sample_rate = 44100
start_time = time.time()

# Create Tkinter window
root = tk.Tk()
root.title("Real-time Indian Note Detection")

# Create Matplotlib figure and canvas
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create label for detected note
detected_label = tk.Label(root, text="Detected Note: None")
detected_label.pack()

# Start audio stream in a separate thread
def start_audio_stream():
    """Starts the audio stream"""
    with sd.InputStream(callback=audio_callback, samplerate=sample_rate):
        while True:
            time.sleep(0.1)

audio_thread = threading.Thread(target=start_audio_stream)
audio_thread.daemon = True #close thread when main window closes.
audio_thread.start()

# Start updating the graph
update_graph()

# Start Tkinter event loop
root.mainloop()