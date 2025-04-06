import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import librosa
import numpy as np
import os
import random

# GPU verification and memory management
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)
else:
    print("No GPU detected, using CPU.")

def audio_preprocessing(audio_file):
    y, sr = librosa.load(audio_file)
    stft = librosa.stft(y)
    spectrogram = np.abs(stft)
    return spectrogram, sr

def create_note_detection_model(input_shape, num_notes, num_octaves):
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_notes, activation='softmax', name='note_output'),
        layers.Dense(num_octaves, activation='softmax', name='octave_output'),
        layers.Dense(1, name='frequency_output')
    ])
    model.compile(optimizer='adam',
                  loss={'note_output': 'categorical_crossentropy',
                        'octave_output': 'categorical_crossentropy',
                        'frequency_output': 'mse'},
                  metrics={'note_output': 'accuracy',
                           'octave_output': 'accuracy',
                           'frequency_output': 'mae'})
    return model

def generate_random_dataset(num_samples, num_notes, num_octaves, sample_rate=44100, duration=1.0):
    """Generates a random dataset for testing."""
    audio_files = []
    note_labels = []
    octave_labels = []
    frequency_labels = []

    for _ in range(num_samples):
        # Create a simple sine wave audio file
        freq = random.uniform(100, 1000)  # Random frequency
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(2 * np.pi * freq * t)
        audio_file = f"temp_audio_{random.randint(1000, 9999)}.wav"
        librosa.output.write_wav(audio_file, audio, sample_rate)
        audio_files.append(audio_file)

        # Random labels
        note_label = random.randint(0, num_notes - 1)
        octave_label = random.randint(0, num_octaves - 1)
        frequency_label = freq

        note_labels.append(note_label)
        octave_labels.append(octave_label)
        frequency_labels.append(frequency_label)

    return audio_files, note_labels, octave_labels, frequency_labels

def prepare_batch_data(audio_files, note_labels, octave_labels, frequency_labels, num_notes, num_octaves):
    spectrograms = []
    note_one_hots = []
    octave_one_hots = []
    frequency_labels_list = []

    for audio_file, note_label, octave_label, frequency_label in zip(audio_files, note_labels, octave_labels, frequency_labels):
        spectrogram, _ = audio_preprocessing(audio_file)
        spectrogram = np.expand_dims(spectrogram, axis=-1)
        spectrograms.append(spectrogram)

        note_one_hot = np.zeros(num_notes)
        note_one_hot[note_label] = 1
        note_one_hots.append(note_one_hot)

        octave_one_hot = np.zeros(num_octaves)
        octave_one_hot[octave_label] = 1
        octave_one_hots.append(octave_one_hot)

        frequency_labels_list.append(frequency_label)

    return np.array(spectrograms), np.array(note_one_hots), np.array(octave_one_hots), np.array(frequency_labels_list)

# Example Usage
num_notes = 12
num_octaves = 5
num_samples = 100
batch_size = 32
epochs = 20

# Generate Random Dataset
audio_files, note_labels, octave_labels, frequency_labels = generate_random_dataset(num_samples, num_notes, num_octaves)

# Prepare Data
spectrograms, note_one_hots, octave_one_hots, frequency_labels_array = prepare_batch_data(audio_files, note_labels, octave_labels, frequency_labels, num_notes, num_octaves)

input_shape = spectrograms.shape[1:]

# Create Model
model = create_note_detection_model(input_shape, num_notes, num_octaves)

# Training Loop
model.fit(spectrograms, {'note_output': note_one_hots, 'octave_output': octave_one_hots, 'frequency_output': frequency_labels_array}, epochs=epochs, validation_split=0.2, batch_size=batch_size)

# Evaluation
loss, note_loss, octave_loss, frequency_loss, note_accuracy, octave_accuracy, frequency_mae = model.evaluate(spectrograms, {'note_output': note_one_hots, 'octave_output': octave_one_hots, 'frequency_output': frequency_labels_array})
print(f"Note Accuracy: {note_accuracy}, Octave Accuracy: {octave_accuracy}, Frequency MAE: {frequency_mae}")

# Prediction
predictions = model.predict(spectrograms[:5])
print("Predictions:", predictions)

# Clean up temp files
for file in audio_files:
    os.remove(file)