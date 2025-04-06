import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def audio_preprocessing(audio_file):
    """
    Performs audio preprocessing using STFT and CQT.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        tuple: (spectrogram, cqt_representation, sample_rate)
    """

    # 1. Load Audio Data
    y, sr = librosa.load(audio_file)

    # 2. STFT
    stft = librosa.stft(y)
    spectrogram = np.abs(stft)  # Magnitude spectrogram

    # 3. CQT
    cqt = librosa.cqt(y, sr=sr)
    cqt_representation = np.abs(cqt)

    return spectrogram, cqt_representation, sr

# Example usage
audio_file = "C:\\Users\\rsshi\OneDrive\Desktop\GDSC'25\kal.mp3" # Replace with your audio file
spectrogram, cqt_representation, sample_rate = audio_preprocessing(audio_file)

# Visualization (Optional)
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
librosa.display.specshow(librosa.amplitude_to_db(spectrogram, ref=np.max), sr=sample_rate, x_axis='time', y_axis='log')
plt.title('Spectrogram')

plt.subplot(1, 2, 2)
librosa.display.specshow(librosa.amplitude_to_db(cqt_representation, ref=np.max), sr=sample_rate, x_axis='time', y_axis='cqt_note')
plt.title('CQT Representation')

plt.tight_layout()
plt.show()

print("Audio Preprocessing Done")