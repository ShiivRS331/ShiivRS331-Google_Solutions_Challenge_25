
import asyncio
import numpy as np
import sounddevice as sd
import scipy.signal as signal
from matplotlib.figure import Figure
import matplotlib.backends.backend_agg as agg
import time
import json
import base64
import io
import traceback
import websockets

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
    if len(audio_data) == 0:
        return None, None, None
    try:
        frequencies, magnitudes = signal.welch(audio_data, sample_rate, nperseg=1024)
        dominant_frequency = frequencies[np.argmax(magnitudes)]
        note, octave = find_nearest_note(dominant_frequency)
        return dominant_frequency, note, octave
    except Exception as e:
        print(f"Error in detect_note: {e}")
        traceback.print_exc()
        return None, None, None

def audio_callback(indata, frames, time, status):
    global audio_data
    if status:
        print(f"Error in audio_callback: {status}")
    audio_data = indata.flatten()

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

async def update_graph(websocket):
    if len(audio_data) > 0:
        dominant_frequency, note, octave = detect_note(audio_data, sample_rate)
        if dominant_frequency is not None:
            freq_data.append(dominant_frequency)
            note_data.append(note)
            octave_data.append(octave)
            time_data.append(time.time() - start_time)

            ax.clear()
            ax.plot(time_data, freq_data)
            ax.set_title(f"Note: {note} ({octave}), Freq: {dominant_frequency:.2f} Hz")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Frequency (Hz)")

            canvas = agg.FigureCanvasAgg(fig)
            buffer = io.BytesIO()
            canvas.print_png(buffer)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()

            data = {
                'note': note,
                'octave': octave,
                'frequency': dominant_frequency,
                'image': image_base64,
            }
            try:
                await websocket.send(json.dumps(data))
            except Exception as e:
                print(f"Error sending data: {e}")
                traceback.print_exc()
    await asyncio.sleep(0.1)

async def audio_stream(websocket):
    print("Audio stream started.")
    try:
        with sd.InputStream(callback=audio_callback, samplerate=sample_rate):
            while True:
                await update_graph(websocket)
    except Exception as e:
        print(f"Error in start_audio_stream: {e}")
        traceback.print_exc()

async def handler(websocket, path):
    print(f"Client connected. Websocket: {websocket}, Path: {path}")
    await audio_stream(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 65431) as server: #Corrected Port
        print("WebSocket server started at ws://0.0.0.0:65431")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
