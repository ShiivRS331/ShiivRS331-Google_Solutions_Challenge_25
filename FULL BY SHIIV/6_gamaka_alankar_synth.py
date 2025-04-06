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

def process_prompt_gamaka_alankar(prompt):
    prompt = prompt.lower()
    gamaka = "default"
    alankar = "default"
    if "andolan" in prompt:
        gamaka = "andolan"
    if "meend" in prompt:
        gamaka = "meend"
    if "sargam" in prompt:
        alankar = "sargam"
    if "alankar" in prompt and "simple" in prompt:
        alankar = "simple"

    return {"gamaka": gamaka, "alankar": alankar}

def transformer_audio_gamaka_alankar(audio, prompt_data):
    if prompt_data["gamaka"] == "andolan":
        pitch_shift = random.uniform(-0.5, 0.5)
        modified_audio = librosa.effects.pitch_shift(audio, sr=44100, n_steps=pitch_shift)
        return modified_audio
    elif prompt_data["gamaka"] == "meend":
        pitch_shift = random.uniform(-0.3, 0.3)
        modified_audio = librosa.effects.pitch_shift(audio, sr=44100, n_steps=pitch_shift)
        return modified_audio
    return audio

def transformer_symbolic_gamaka_alankar(music_sequence, prompt_data):
    modified_sequence = music_sequence.copy()
    if prompt_data["alankar"] == "sargam":
        sargam_pattern = ["note_C4_0.5", "note_D4_0.5", "note_E4_0.5", "note_F4_0.5", "note_G4_0.5", "note_A4_0.5", "note_B4_0.5", "note_C5_0.5"]
        modified_sequence.extend(sargam_pattern)
    elif prompt_data['alankar'] == 'simple':
        simple_pattern = ["note_C4_0.5", "note_D4_0.5", "note_E4_0.5"]
        modified_sequence.extend(simple_pattern)
    return modified_sequence

def latent_diffusion_gamaka_alankar(music_output):
    duration = 5
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), False)
    freq = 440
    audio = np.sin(2 * np.pi * freq * t)
    return audio

def music_sequence_to_midi(music_output, output_file):
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
            pass

    mf = music21.midi.translate.streamToMidiFile(score)
    mf.open(output_file, 'wb')
    mf.write()
    mf.close()

def modify_music_gamaka_alankar(music_input, input_type, prompt_data):
    if input_type == "audio":
        modified_music = transformer_audio_gamaka_alankar(music_input, prompt_data)
        return modified_music, "audio"
    elif input_type == "symbolic":
        modified_music = transformer_symbolic_gamaka_alankar(music_input, prompt_data)
        return modified_music, "symbolic"
    else:
        raise ValueError("Invalid input type")

def synthesize_audio_gamaka_alankar(modified_music, modified_type):
    if modified_type == "audio":
        return modified_music
    elif modified_type == "symbolic":
        return latent_diffusion_gamaka_alankar(modified_music)
    else:
        raise ValueError("Invalid modified type")
# Example usage
try:
    input_file = "C:\\Users\\rsshi\\OneDrive\\Desktop\\GDSC'25\\kal.mp3"
    music_input, sr, input_type = load_music_input(input_file)
    prompt = "Add an andolan gamaka and a sargam alankar"
    prompt_data = process_prompt_gamaka_alankar(prompt)
    modified_music, modified_type = modify_music_gamaka_alankar(music_input, input_type, prompt_data)
    synthesized_audio = synthesize_audio_gamaka_alankar(modified_music, modified_type)
    output_music(synthesized_audio, "audio", "output_gamaka_alankar.wav", sr)
    print("Gamaka and Alankar Synthesis Implemented")
except Exception as e:
    print(f"An error occurred: {e}")