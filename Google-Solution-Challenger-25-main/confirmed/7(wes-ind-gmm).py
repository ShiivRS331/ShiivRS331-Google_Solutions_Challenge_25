import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

# Load Audio (First 30 Seconds)
audio_path = r"C:\Users\drivi\Downloads\kal.mp3"  # Replace with your song
y, sr = librosa.load(audio_path, sr=16000, duration=30)

# Autocorrelation-Based Pitch Detection
def autocorrelation_pitch_detection(signal, sr, frame_length=1024, hop_length=256):
    pitches = []
    for i in range(0, len(signal) - frame_length, hop_length):
        frame = signal[i:i + frame_length]
        frame -= np.mean(frame)
        frame *= np.hanning(len(frame))
        autocorr = np.correlate(frame, frame, mode='full')[len(frame) - 1:]
        autocorr /= np.max(autocorr)
        peaks = np.where((autocorr[:-1] < autocorr[1:]) & (autocorr[1:] > autocorr[2:]))[0]
        if len(peaks) > 0:
            lag = peaks[0]
            pitch = sr / lag
            pitches.append(pitch)
        else:
            pitches.append(np.nan)
    return np.array(pitches)

pitches = autocorrelation_pitch_detection(y, sr)
filtered_pitches = pitches[~np.isnan(pitches)]
shruti_freq = np.median(filtered_pitches) if len(filtered_pitches) > 0 else 208

# Apply GMM for Clustering
valid_pitches = filtered_pitches.reshape(-1, 1)
gmm = GaussianMixture(n_components=12, random_state=42)
gmm.fit(valid_pitches)
cluster_labels = gmm.predict(valid_pitches)
cluster_means = gmm.means_.flatten()
pitch_clusters = [cluster_means[label] for label in cluster_labels]

# Hindustani Swaras Mapping
svara_ratios = {
    "S": 1, "R1": 16/15, "R2": 9/8, "R3": 6/5,
    "G1": 9/8, "G2": 6/5, "G3": 5/4,
    "M1": 4/3, "M2": 17/12,
    "P": 3/2,
    "D1": 8/5, "D2": 5/3, "D3": 9/5,
    "N1": 5/3, "N2": 9/5, "N3": 15/8,
    "S'": 2
}

svara_frequencies = {s: shruti_freq * r for s, r in svara_ratios.items()}
def map_pitch_to_swara(frequency):
    if np.isnan(frequency) or frequency <= 0:
        return None
    return min(svara_frequencies, key=lambda s: abs(svara_frequencies[s] - frequency))

clustered_swaras = [map_pitch_to_swara(f) for f in pitch_clusters]

# Visualization
plt.figure(figsize=(12, 6))
plt.scatter(range(len(cluster_labels)), cluster_labels, c=cluster_labels, cmap='viridis', label="GMM Clusters")
plt.xlabel("Time Frames")
plt.ylabel("Cluster ID")
plt.title("GMM Clustered Notes Over Time (Mapped to Hindustani Scale)")
plt.colorbar(label="Cluster ID")
plt.legend()
plt.show()