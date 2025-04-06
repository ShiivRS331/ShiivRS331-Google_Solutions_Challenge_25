import librosa
import music21
import numpy as np
import random

def augment_audio(audio, sr, pitch_shift_range=2, time_stretch_range=0.2, noise_level=0.01):
    """Augments audio data."""
    # Pitch shift
    pitch_shift = random.uniform(-pitch_shift_range, pitch_shift_range)
    augmented_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_shift)

    # Time stretch
    time_stretch = random.uniform(1 - time_stretch_range, 1 + time_stretch_range)
    augmented_audio = librosa.effects.time_stretch(augmented_audio, rate=time_stretch)

    # Add noise
    noise = np.random.normal(0, noise_level, len(augmented_audio))
    augmented_audio += noise

    return augmented_audio

def augment_music_sheet(score, pitch_shift_range=2, time_stretch_range=0.2):
    """Augments music sheet data."""
    augmented_score = score.clone()  # Create a copy

    # Pitch Augmentation
    interval = music21.interval.ChromaticInterval(random.randint(-pitch_shift_range, pitch_shift_range))
    for note in augmented_score.recurse().notes:
        note.transpose(interval, inPlace=True)

    # Rhythm Augmentation
    for note in augmented_score.recurse().notes:
        if random.random() < 0.2:  # 20% chance to change duration
            durations = [0.25, 0.5, 1.0, 2.0]  # Example durations
            note.duration.quarterLength = random.choice(durations)

    # Add grace notes
    for note in augmented_score.recurse().notes:
        if random.random() < 0.1:  # 10% chance to add grace note
            grace = music21.note.GraceNote("C4", quarterLength=0.1)
            augmented_score.insert(note.offset, grace)

    # Articulation changes
    for note in augmented_score.recurse().notes:
        if random.random() < 0.15:
            if random.random() < 0.5:
                note.articulations.append(music21.articulations.Staccato())
            else:
                note.articulations.append(music21.articulations.Tenuto())

    # Dynamic changes
    for element in augmented_score.recurse().getElementsByClass('Dynamic'):
        if random.random() < 0.2:
            dynamics = ['ff', 'f', 'mf', 'mp', 'p', 'pp']
            element.value = random.choice(dynamics)

    return augmented_score

# --- Example Usage ---

audio, sr = librosa.load("input.wav")  # REPLACE WITH YOUR AUDIO FILE
augmented_audio = augment_audio(audio, sr)
librosa.output.write_wav("augmented_audio.wav", augmented_audio, sr)

score = music21.converter.parse("input.xml")  # REPLACE WITH YOUR MUSICXML FILE
augmented_score = augment_music_sheet(score)
augmented_score.write("musicxml", "augmented_score.xml")

print("Data Augmentation Implemented")