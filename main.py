"""Main module to demonstrate melody generation with chord progression."""

from improvisation_lab.domain.music_theory import ChordTone
from improvisation_lab.domain.melody_jam import MelodyGenerator


def main():
    """Generate melody phrases over Fly Me to the Moon chord progression."""
    melody_generator = MelodyGenerator()
    
    # Generate phrases based on the first 8 bars of "Fly Me to the Moon"
    progression = [
        # (scale_root, scale_type, chord_root, chord_type, length)
        ('A', 'natural_minor', 'A', 'min7', 8),
        ('A', 'natural_minor', 'D', 'min7', 8),
        ('C', 'major', 'G', 'dom7', 8),
        ('C', 'major', 'C', 'maj7', 4),
        ('F', 'major', 'C', 'dom7', 4),
        ('C', 'major', 'F', 'maj7', 8),
        ('A', 'natural_minor', 'B', 'min7(b5)', 8),
        ('A', 'harmonic_minor', 'E', 'dom7', 8),
        ('A', 'natural_minor', 'A', 'min7', 4),
        ('D', 'harmonic_minor', 'A', 'dom7', 4),
    ]

    # Keep track of the last note from previous phrase for natural connections
    prev_note = None
    prev_note_was_chord_tone = False
    
    print("Generating melody for Fly Me to the Moon:")
    print("-" * 50)

    for i, (scale_root, scale_type, chord_root, chord_type, length) in enumerate(progression, 1):
        phrase = melody_generator.generate_phrase(
            scale_root=scale_root,
            scale_type=scale_type,
            chord_root=chord_root,
            chord_type=chord_type,
            prev_note=prev_note,
            prev_note_was_chord_tone=prev_note_was_chord_tone,
            length=length
        )
        
        # Update information for the next phrase
        prev_note = phrase[-1]
        prev_note_was_chord_tone = melody_generator.is_chord_tone(
            prev_note,
            ChordTone.get_chord_tones(chord_root, chord_type)
        )
        
        # Display the generated phrase
        chord_name = f"{chord_root}{chord_type}"
        print(f"Phrase {i} ({chord_name}, {scale_root} {scale_type}):")
        print(" -> ".join(phrase))
        print()


if __name__ == "__main__":
    main()
