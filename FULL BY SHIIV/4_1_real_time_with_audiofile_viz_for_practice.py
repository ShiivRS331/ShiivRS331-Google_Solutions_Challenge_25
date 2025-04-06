import numpy as np
import sounddevice as sd
import scipy.signal as signal
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
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

OCTAVES = ["2", "3", "4", "5", "6"]
ALL_NOTES = []
ALL_FREQS = []
for octave in OCTAVES:
    for note_name, freq in NOTES[octave].items():
        ALL_NOTES.append(f"{note_name} ({octave})")
        ALL_FREQS.append(freq)

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

def audio_callback(indata, frames, time, status):
    global audio_data
    if status:
        print(status)
    audio_data = indata.flatten()

def process_audio_file(audio_file):
    y, sr = librosa.load(audio_file)
    time_data_file = []
    note_data_file = []
    freq_data_file = []
    octave_data_file = []
    time_step = 0.05 # Increased time_step
    for i in range(0, len(y), int(sr * time_step)):
        audio_segment = y[i:i + int(sr * time_step)]
        if len(audio_segment) > int(sr * time_step * .75):
            freq, note, octave = detect_note(audio_segment, sr)
            if note:
                time_data_file.append(i / sr)
                note_data_file.append(note)
                freq_data_file.append(freq)
                octave_data_file.append(octave)
        else:
            print(f"Audio segment too short: {len(audio_segment)}") # Added error message
    return time_data_file, note_data_file, freq_data_file, octave_data_file, sr

def update_graph():
    global audio_data, time_data, note_data, freq_data, octave_data, x_offset, audio_file_data, start_time, audio_file_sr

    freq, note, octave = None, None, None
    if len(audio_data) > 0:
        freq, note, octave = detect_note(audio_data, sample_rate)
        if note:
            current_time = time.time() - start_time
            time_data.append(current_time)
            note_data.append(note)
            freq_data.append(freq)
            octave_data.append(octave)

    fig.clf() # Clear the figure.

    ax1 = fig.add_subplot(211) # real time plot
    ax2 = fig.add_subplot(212) # audio file plot

    # Plot real-time data
    ax1.plot([t - x_offset for t in time_data], [NOTES[o][n] if o and n else 0 for n, o in zip(note_data, octave_data)], marker='o', linestyle='-', color='blue', label='Real-time')
    ax1.set_yticks(ALL_FREQS)
    ax1.set_yticklabels(ALL_NOTES)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Notes")
    ax1.legend()
    if note and octave:
        ax1.text(0.05, 0.95, f"Note: {note} ({octave})\nFrequency: {freq:.2f} Hz", transform=ax1.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        y_min = NOTES[octave]["S"] - 50
        y_max = NOTES[octave]["S'"] + 50
        ax1.set_ylim(y_min, y_max)

    # Plot audio file data
    if audio_file_data:
        time_data_file, note_data_file_file, freq_data_file_file, octave_data_file_file, audio_file_sr_file = audio_file_data

        print("Audio File Time Data:", time_data_file)
        print("Audio File Note Data:", note_data_file_file)

        # Filter the time data
        filtered_time_data_file = []
        if len(time_data_file) > 0:
            filtered_time_data_file.append(time_data_file[0])
            for i in range(1, len(time_data_file)):
                if time_data_file[i] - time_data_file[i-1] < 10: # Adjust the threshold as needed
                    filtered_time_data_file.append(time_data_file[i])

        audio_duration = librosa.get_duration(path="C:\\Users\\rsshi\\OneDrive\\Desktop\\GDSC'25\\kal.mp3") # Fixed FutureWarning
        scaled_time_data_file = []
        if len(filtered_time_data_file) > 0:
            audio_time_scale = audio_duration / filtered_time_data_file[-1] if filtered_time_data_file[-1] > 0 else 1
            scaled_time_data_file = [t * audio_time_scale for t in filtered_time_data_file]

            # Adjust scaled_time_data_file to match real time
            current_real_time = time.time() - start_time
            max_audio_time = scaled_time_data_file[-1] if scaled_time_data_file else 0

            if max_audio_time > 0:
                plot_indices = [i for i, t in enumerate(scaled_time_data_file) if t <= current_real_time]
                plot_time = [scaled_time_data_file[i] for i in plot_indices]
                plot_notes = [NOTES[o][n] if o and n else 0 for i, (n, o) in enumerate(zip(note_data_file_file, octave_data_file_file)) if i in plot_indices]

                ax2.plot(plot_time, plot_notes, marker='.', linestyle='-', color='red', label='Audio File')
                ax2.set_yticks(ALL_FREQS)
                ax2.set_yticklabels(ALL_NOTES)
                ax2.set_xlabel("Time (s)")
                ax2.set_ylabel("Notes")
                ax2.legend()

                # Dynamic y-axis for audio file plot
                if plot_indices: # Check if there are any plotted points
                    # Get the note and octave corresponding to the last plotted time
                    last_index = plot_indices[-1]
                    last_note = note_data_file_file[last_index]
                    last_octave = octave_data_file_file[last_index]
                    last_freq = freq_data_file_file[last_index] # Added frequency

                    if last_note and last_octave:
                        y_min = NOTES[last_octave]["S"] - 50
                        y_max = NOTES[last_octave]["S'"] + 50
                        ax2.set_ylim(y_min, y_max)
                        print(f"Audio File Y-Axis: {y_min}, {y_max}") # Debug print
                        ax2.text(0.05, 0.95, f"Note: {last_note} ({last_octave})\nFrequency: {last_freq:.2f} Hz", transform=ax2.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')) # Added text for audio file

    canvas.draw()
    root.after(100, update_graph)

# --- (Rest of your Tkinter and audio stream code) ---

audio_data = np.array([])
time_data = []
note_data = []
freq_data = []
octave_data = []
sample_rate = 44100
start_time = time.time()
x_offset = 0
audio_file_data = None
audio_file_sr = None

root = tk.Tk()
root.title("Vocal Training App")
fig = Figure(figsize=(12, 12)) # increased figure size
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Load audio file directly in the code:
audio_file_path = "C:\\Users\\rsshi\\OneDrive\\Desktop\\GDSC'25\\kal.mp3" # Replace with your file path
audio_file_data = process_audio_file(audio_file_path)

def start_audio_stream():
    with sd.InputStream(callback=audio_callback, samplerate=sample_rate):
        while True:
            time.sleep(0.1)

audio_thread = threading.Thread(target=start_audio_stream)
audio_thread.daemon = True
audio_thread.start()

update_graph()

root.mainloop()

print("Real-Time Vocal Training Visualization Implemented")