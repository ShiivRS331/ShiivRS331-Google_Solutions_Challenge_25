import numpy as np
import sounddevice as sd
import scipy.signal as signal
from matplotlib.figure import Figure
import matplotlib.backends.backend_agg as agg
import threading
import time
import json
import socket
import base64
import io
import traceback  # Import traceback for detailed error logging

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
    """
    Finds the nearest Indian musical note to a given frequency.

    Args:
        freq (float): The frequency to find the nearest note for.

    Returns:
        tuple: (nearest_note, nearest_octave).  Returns (None, None) if freq <= 0.
    """
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
    """
    Detects the dominant note and frequency from audio data.

    Args:
        audio_data (numpy.ndarray): The audio data.
        sample_rate (int): The sample rate of the audio data.

    Returns:
        tuple: (dominant_frequency, note, octave). Returns (None, None, None) if audio_data is empty.
    """
    if len(audio_data) == 0:
        return None, None, None

    try:
        frequencies, magnitudes = signal.welch(audio_data, sample_rate, nperseg=1024)
        dominant_frequency = frequencies[np.argmax(magnitudes)]
        note, octave = find_nearest_note(dominant_frequency)
        return dominant_frequency, note, octave
    except Exception as e:
        print(f"Error in detect_note: {e}")
        traceback.print_exc()  # Print the full traceback
        return None, None, None

def audio_callback(indata, frames, time, status):
    """
    Callback function for the sounddevice InputStream.  Processes incoming audio data.

    Args:
        indata (numpy.ndarray): The audio data.
        frames (int): The number of frames.
        time (CPointer):  Time information (not used here).
        status (int):  Status flags (checks for errors).
    """
    global audio_data
    if status:
        print(f"Error in audio_callback: {status}")  # Print the error status
    audio_data = indata.flatten()

# Socket setup
HOST = '127.0.0.1'  # Changed to a constant
PORT = 65432  # Changed to a constant
BUFFER_SIZE = 1024 * 1024  # Added a buffer size

# Initialize global variables
audio_data = np.array([])
time_data = []
note_data = []
freq_data = []
octave_data = []
sample_rate = 44100
start_time = time.time()
x_offset = 0

fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

def update_graph(conn):
    """
    Updates the graph with the latest audio data and sends it to the client.

    Args:
        conn (socket.socket): The socket connection to the client.
    """
    global audio_data, time_data, note_data, freq_data, octave_data, x_offset

    if len(audio_data) > 0:
        freq, note, octave = detect_note(audio_data, sample_rate)
        if note:
            current_time = time.time() - start_time
            time_data.append(current_time)
            note_data.append(note)
            freq_data.append(freq)
            octave_data.append(octave)

            ax.clear()
            ax.plot([t - x_offset for t in time_data], [NOTES[o][n] if o and n else 0 for n, o in zip(note_data, octave_data)], marker='o', linestyle='-')
            ax.set_yticks(ALL_FREQS)
            ax.set_yticklabels(ALL_NOTES)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Notes")
            ax.set_xlim(max(0, current_time - 5), current_time + 1)
            if octave:
                y_min = NOTES[octave]["S"] - 50
                y_max = NOTES[octave]["S'"] + 50
                ax.set_ylim(y_min, y_max)
            ax.text(0.05, 0.95, f"Note: {note} ({octave})\nFrequency: {freq:.2f} Hz", transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

            # Save the graph as a base64 encoded image
            buffer = io.BytesIO()
            try:
                agg.FigureCanvasAgg(fig)
                fig.savefig(buffer, format='png')  # Or 'jpeg'
                image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            except Exception as e:
                print(f"Error saving graph: {e}")
                traceback.print_exc()
                return

            # Send data through the socket
            data = {
                'note': note,
                'octave': octave,
                'frequency': freq,
                'image': image_base64
            }
            try:
                json_data = json.dumps(data).encode('utf-8')
                conn.sendall(json_data)
            except Exception as e:
                print(f"Error sending data: {e}")
                traceback.print_exc()
                return  # Exit the function if there's an error
    time.sleep(0.1)

def start_audio_stream():
    """Starts the audio input stream and continuously processes audio data."""
    try:
        with sd.InputStream(callback=audio_callback, samplerate=sample_rate):
            while True:
                # Pass the connection to the update_graph function
                update_graph(conn)
    except Exception as e:
        print(f"Error in start_audio_stream: {e}")
        traceback.print_exc()  # Print the full traceback
        # Consider adding a return here, or some other error handling

# Socket server setup
s = None
conn = None # Declare conn
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print(f"Socket bound to {HOST}:{PORT}")
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    # Move the audio thread start into the 'with conn' block
    with conn:
        audio_thread = threading.Thread(target=start_audio_stream)
        audio_thread.daemon = True
        audio_thread.start()
        # Keep the main thread alive to prevent the program from exiting.
        while True:
            time.sleep(1)

except Exception as e:
    print(f"Error setting up socket server: {e}")
    traceback.print_exc()
finally:
    if s:
        s.close()
        print("Socket closed")
