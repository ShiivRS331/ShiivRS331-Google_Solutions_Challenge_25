import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import librosa
import music21
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

def load_music_input(input_file):
    if input_file.lower().endswith(('.wav', '.mp3')):
        audio, sr = librosa.load(input_file)
        return audio, sr, "audio"
    elif input_file.lower().endswith(('.mid', '.midi', '.xml', '.musicxml')):
        score = music21.converter.parse(input_file)
        music_sequence = music21_to_sequence(score)
        return music_sequence, None, "symbolic"
    else:
        raise ValueError("Unsupported input file format")

def music21_to_sequence(score):
    """Converts a music21 score to a sequence of musical events."""
    sequence = []
    for element in score.recurse():
        if isinstance(element, music21.note.Note):
            sequence.append(f"note_{element.nameWithOctave}_{element.duration.quarterLength}")
        elif isinstance(element, music21.note.Rest):
            sequence.append(f"rest_{element.duration.quarterLength}")
        elif isinstance(element, music21.tempo.MetronomeMark):
            sequence.append(f"tempo_{element.number}")
        elif isinstance(element, music21.stream.Measure):
            sequence.append("measure_start")
    return sequence

def process_prompt(prompt):
    """Processes a text prompt to extract modification instructions."""
    prompt = prompt.lower()
    if "add taan" in prompt:
        gamaka = "slide" if "slide" in prompt else "default"
        return {"modification_type": "add_taan", "gamaka": gamaka}
    else:
        return {"modification_type": "default", "gamaka": "default"}

def transformer_audio_modification(audio, prompt_data):
    """Placeholder: Implement Transformer-based audio modification."""
    # This is a placeholder. A real implementation would involve a trained Transformer model.
    # For now, we'll add a simple pitch shift as an example.
    if prompt_data["modification_type"] == "add_taan":
        pitch_shift = random.uniform(-2, 2)  # Random pitch shift
        modified_audio = librosa.effects.pitch_shift(audio, sr=44100, n_steps=pitch_shift)
        return modified_audio
    return audio

def transformer_symbolic_modification(music_sequence, prompt_data):
    """Placeholder: Implement Transformer-based symbolic music modification."""
    # This is a placeholder. A real implementation would involve a trained Transformer model.
    modified_sequence = music_sequence.copy()
    if prompt_data["modification_type"] == "add_taan":
        # Example: Add a simple taan-like pattern
        taan_pattern = ["note_C4_0.5", "note_D4_0.5", "note_E4_0.5", "note_F4_0.5"]
        modified_sequence.extend(taan_pattern)
    return modified_sequence

def latent_diffusion_audio_generation(music_output):
    """Placeholder: Implement Latent Diffusion Model for audio generation."""
    # This is a placeholder. A real implementation would involve a trained Latent Diffusion Model.
    # For now, we'll return a sine wave as an example.
    duration = 5  # seconds
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), False)
    freq = 440  # Hz
    audio = np.sin(2 * np.pi * freq * t)
    return audio

def music_sequence_to_midi(music_output, output_file):
    """Converts a music sequence to a MIDI file."""
    score = music21.stream.Stream()
    offset = 0
    for event in music_output:
        if event.startswith("note_"):
            parts = event.split("_")
            note_name = parts[1]
            duration = float(parts[2])
            note = music21.note.Note(note_name, quarterLength=duration)
            note.offset = offset
            score.append(note)
            offset += duration
        elif event.startswith("rest_"):
            duration = float(event.split("_")[1])
            rest = music21.note.Rest(quarterLength=duration)
            rest.offset = offset
            score.append(rest)
            offset += duration
        elif event.startswith("tempo_"):
            tempo = music21.tempo.MetronomeMark(number=float(event.split("_")[1]))
            score.append(tempo)
        elif event == "measure_start":
            pass #measure start is ignored.

    mf = music21.midi.translate.streamToMidiFile(score)
    mf.open(output_file, 'wb')
    mf.write()
    mf.close()

def modify_music(music_input, input_type, prompt_data):
    if input_type == "audio":
        modified_music = transformer_audio_modification(music_input, prompt_data)
        return modified_music, "audio"
    elif input_type == "symbolic":
        modified_music = transformer_symbolic_modification(music_input, prompt_data)
        return modified_music, "symbolic"
    else:
        raise ValueError("Invalid input type")

def synthesize_audio(modified_music, modified_type):
    if modified_type == "audio":
        return modified_music
    elif modified_type == "symbolic":
        return latent_diffusion_audio_generation(modified_music)
    else:
        raise ValueError("Invalid modified type")

# Example usage
try:
    input_file = "C:\\Users\\rsshi\\OneDrive\\Desktop\\GDSC'25\\kal.mp3" # or "input.mid"
    music_input, sr, input_type = load_music_input(input_file)
    prompt = "Add a taan with a slide gamaka"
    prompt_data = process_prompt(prompt)
    modified_music, modified_type = modify_music(music_input, input_type, prompt_data)
    synthesized_audio = synthesize_audio(modified_music, modified_type)
    output_music(synthesized_audio, "audio", "output.wav", sr)
    print("Music Synthesis and Modification Implemented")
except Exception as e:
    print(f"An error occurred: {e}")