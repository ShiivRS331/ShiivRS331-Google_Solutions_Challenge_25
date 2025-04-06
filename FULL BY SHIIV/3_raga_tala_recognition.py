import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
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

def create_raga_tala_model(sequence_length, num_notes, num_ragas, num_talas):
    inputs = layers.Input(shape=(sequence_length, num_notes))
    x = layers.MultiHeadAttention(num_heads=8, key_dim=64)(inputs, inputs)
    x = layers.LayerNormalization(epsilon=1e-6)(x + inputs)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.GlobalAveragePooling1D()(x)
    raga_output = layers.Dense(num_ragas, activation='softmax', name='raga_output')(x)
    tala_output = layers.Dense(num_talas, activation='softmax', name='tala_output')(x)
    model = tf.keras.Model(inputs=inputs, outputs=[raga_output, tala_output])
    model.compile(optimizer='adam',
                  loss={'raga_output': 'categorical_crossentropy',
                        'tala_output': 'categorical_crossentropy'},
                  metrics={'raga_output': 'accuracy',
                           'tala_output': 'accuracy'})
    return model

def generate_random_dataset(num_samples, sequence_length, num_notes, num_ragas, num_talas):
    """Generates a random dataset for testing."""
    note_sequences = []
    raga_labels = []
    tala_labels = []

    for _ in range(num_samples):
        note_sequence = [random.randint(0, num_notes - 1) for _ in range(sequence_length)]
        raga_label = random.randint(0, num_ragas - 1)
        tala_label = random.randint(0, num_talas - 1)
        note_sequences.append(note_sequence)
        raga_labels.append(raga_label)
        tala_labels.append(tala_label)

    return note_sequences, raga_labels, tala_labels

def prepare_sequence_data(note_sequences, raga_labels, tala_labels, num_notes, num_ragas, num_talas):
    """Prepares batch data for training."""
    sequences_one_hot = []
    raga_one_hots = []
    tala_one_hots = []

    for note_sequence, raga_label, tala_label in zip(note_sequences, raga_labels, tala_labels):
        sequence_length = len(note_sequence)
        note_sequence_one_hot = np.zeros((sequence_length, num_notes))
        for i, note_index in enumerate(note_sequence):
            note_sequence_one_hot[i, note_index] = 1
        raga_one_hot = np.zeros(num_ragas)
        raga_one_hot[raga_label] = 1
        tala_one_hot = np.zeros(num_talas)
        tala_one_hot[tala_label] = 1

        sequences_one_hot.append(note_sequence_one_hot)
        raga_one_hots.append(raga_one_hot)
        tala_one_hots.append(tala_one_hot)

    return np.array(sequences_one_hot), np.array(raga_one_hots), np.array(tala_one_hots)

# Example Usage
num_notes = 12
num_ragas = 10
num_talas = 5
sequence_length = 10 #Example sequence length.
num_samples = 1000 #number of training examples.

# Generate Random Dataset
note_sequences, raga_labels, tala_labels = generate_random_dataset(num_samples, sequence_length, num_notes, num_ragas, num_talas)

# Prepare Data
sequences_one_hot, raga_one_hots, tala_one_hots = prepare_sequence_data(note_sequences, raga_labels, tala_labels, num_notes, num_ragas, num_talas)

# Create Model
model = create_raga_tala_model(sequence_length, num_notes, num_ragas, num_talas)

# Training Loop
model.fit(sequences_one_hot, {'raga_output': raga_one_hots, 'tala_output': tala_one_hots}, epochs=20, validation_split=0.2, batch_size=32)

# Evaluation
loss, raga_loss, tala_loss, raga_accuracy, tala_accuracy = model.evaluate(sequences_one_hot, {'raga_output': raga_one_hots, 'tala_output': tala_one_hots})
print(f"Raga Accuracy: {raga_accuracy}, Tala Accuracy: {tala_accuracy}")

# Prediction
predictions = model.predict(sequences_one_hot[:5])  # Predict on the first 5 samples
print("Predictions (Raga, Tala):", predictions)

#example of how to access the raga and tala prediction separately.
raga_predictions = predictions[0] #ragas
tala_predictions = predictions[1] #talas

print("Raga Predictions:", raga_predictions)
print("Tala Predictions:", tala_predictions)