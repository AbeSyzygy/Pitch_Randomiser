import numpy as np
import sounddevice as sd
import random
import keyboard

from note_to_freq import note_to_freq
# Add the complete note_to_freq dictionary here

def get_notes_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if ":1" in line]

def get_next_note():
    global last_note
    while True:
        next_note = random.choice(notes)
        if next_note != last_note:
            break
    last_note = next_note
    return next_note

def play_tone(note, duration_ms):
    frequency = note_to_freq[note.split(':')[0]]
    sample_rate = 44100
    duration_s = duration_ms / 1000
    num_samples = int(sample_rate * duration_s)
    t = np.linspace(0, duration_s, num_samples, False)

    # Generate sine wave
    samples = (np.sin(frequency * 2 * np.pi * t) * 32767).astype(np.int16)

    # Play the audio
    with sd.OutputStream(samplerate=sample_rate, channels=1, dtype='int16'):
        sd.play(samples, blocking=True)

notes = get_notes_from_file("notes.txt")
last_note = None

# Main loop
interval_ms = int(input("Enter the interval duration in milliseconds: "))
try:
    while True:
        note = get_next_note()
        play_tone(note, interval_ms)
        if keyboard.is_pressed('q'):
            print("Program terminated.")
            break
except KeyboardInterrupt:
    print("Program terminated.")
