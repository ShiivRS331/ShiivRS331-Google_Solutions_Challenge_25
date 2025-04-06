import librosa
import numpy as np
import pyaudio
import whisper  # OpenAI's Whisper for speech recognition
import noisereduce as nr  # For noise reduction

# Load Whisper model
whisper_model = whisper.load_model("base")  # You can use "small", "medium", or "large" for better accuracy

# Define the Indian scale ratios (relative to Sa) with microtones (shruti)
indian_scale_ratios = {
    'Sa': 1/1,
    'Re_komal': 16/15,  # Minor second
    'Re': 9/8,         # Major second
    'Ga_komal': 6/5,   # Minor third
    'Ga': 5/4,         # Major third
    'Ma': 4/3,         # Perfect fourth
    'Ma_tivra': 45/32, # Augmented fourth
    'Pa': 3/2,         # Perfect fifth
    'Dha_komal': 8/5,  # Minor sixth
    'Dha': 5/3,        # Major sixth
    'Ni_komal': 9/5,   # Minor seventh
    'Ni': 15/8,        # Major seventh
    'Sa_high': 2/1     # Octave
}

# Function to map frequency to the nearest Indian note
def map_to_indian_scale(freq, sa_freq):
    min_diff = float('inf')
    note = ''
    for key, ratio in indian_scale_ratios.items():
        expected_freq = sa_freq * ratio
        diff = abs(freq - expected_freq)
        if diff < min_diff:
            min_diff = diff
            note = key
    return note

# Real-time audio capture and processing
def real_time_processing():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=2048)  # Increase buffer size

    print("Sing now...")

    # Detect the Sa (tonic) frequency
    print("Please sing Sa (the tonic note) to set the base frequency...")
    sa_data = stream.read(2048)  # Increase buffer size for better pitch detection
    sa_audio = np.frombuffer(sa_data, dtype=np.int16)
    
    # Convert int16 audio to floating-point
    sa_audio = sa_audio.astype(np.float32) / 32768.0  # Normalize to [-1, 1]

    # Apply noise reduction
    sa_audio = nr.reduce_noise(y=sa_audio, sr=44100)

    # Detect pitch using librosa
    pitches, magnitudes = librosa.core.piptrack(y=sa_audio, sr=44100, n_fft=2048)  # Increase n_fft for better resolution
    max_index = np.argmax(magnitudes)
    sa_freq = pitches[max_index // magnitudes.shape[1], max_index % magnitudes.shape[1]]
    print(f"Detected Sa frequency: {sa_freq:.2f} Hz")

    while True:
        data = stream.read(2048)  # Increase buffer size for better pitch detection
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Convert int16 audio to floating-point
        audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize to [-1, 1]

        # Apply noise reduction
        audio_data = nr.reduce_noise(y=audio_data, sr=44100)

        # Save audio to a temporary file for Whisper
        import soundfile as sf
        sf.write("temp.wav", audio_data, 44100)

        # Convert audio to text (lyrics) using Whisper
        result = whisper_model.transcribe("temp.wav")
        text = result["text"]
        print(f"Lyrics: {text}")

        # Detect pitch
        pitches, magnitudes = librosa.core.piptrack(y=audio_data, sr=44100, n_fft=2048)
        max_index = np.argmax(magnitudes)
        pitch = pitches[max_index // magnitudes.shape[1], max_index % magnitudes.shape[1]]
        
        # Map pitch to Indian scale (relative to Sa)
        if pitch > 0:
            note = map_to_indian_scale(pitch, sa_freq)
            print(f"Note: {note}")

# Run the real-time processing
real_time_processing()