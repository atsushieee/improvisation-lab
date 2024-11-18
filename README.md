# Improvisation Lab

A Python package for generating musical improvisation melodies based on music theory principles. The package specializes in creating natural-sounding melodic phrases that follow chord progressions while respecting musical rules, with real-time pitch detection for practice feedback.

Improvisation Lab Demo

https://github.com/user-attachments/assets/a4207f7e-166c-4f50-9c19-5bf5269fd04e


## Features

- Generate melodic phrases based on scales and chord progressions
- Support for multiple scale types:
  - Major
  - Natural minor
  - Harmonic minor
  - Diminished
- Support for various chord types:
  - Major 7th (maj7)
  - Minor 7th (min7)
  - Dominant 7th (dom7)
  - Half-diminished (min7b5)
  - Diminished 7th (dim7)
- Intelligent note selection based on:
  - Chord tones vs non-chord tones
  - Scale degrees
  - Previous note context
- Real-time pitch detection with FCPE (Fast Context-aware Pitch Estimation)
- Web-based and direct microphone input support

## Prerequisites

- Python 3.11 or higher
- A working microphone
- [Poetry](https://python-poetry.org/) for dependency management

## Installation
```bash
make install
```

## Quick Start
1. Create your configuration file:

```bash
cp config.yml.example config.yml
```

2.  (Optional) Edit `config.yml` to customize settings like audio parameters and song selection

3. Run the script to start the melody generation and playback:

```bash
make run
```

4. Follow the displayed melody phrases and sing along with real-time feedback

### Configuration

The application can be customized through `config.yml` with the following options:

#### Audio Settings
- `sample_rate`: Audio sampling rate (default: 44100 Hz)
- `buffer_duration`: Duration of audio processing buffer (default: 0.2 seconds)
- `note_duration`: How long to display each note during practice (default: 3 seconds)
- `pitch_detector`: Configuration for the pitch detection algorithm
  - `hop_length`: Hop length for the pitch detection algorithm (default: 512)
  - `threshold`: Threshold for the pitch detection algorithm (default: 0.006)
  - `f0_min`: Minimum frequency for the pitch detection algorithm (default: 80 Hz)
  - `f0_max`: Maximum frequency for the pitch detection algorithm (default: 880 Hz)
  - `device`: Device to use for the pitch detection algorithm (default: "cpu")

#### Song Selection
- `selected_song`: Name of the song to practice
- `chord_progressions`: Dictionary of songs and their progressions
  - Format: `[scale_root, scale_type, chord_root, chord_type, duration]`
  - Example:
    ```yaml
    fly_me_to_the_moon:
      - ["A", "natural_minor", "A", "min7", 4]
      - ["A", "natural_minor", "D", "min7", 4]
      - ["C", "major", "G", "dom7", 4]
    ```


## How It Works

### Melody Generation
The melody generation follows these principles:
1. Notes are selected based on their relationship to the current chord and scale
2. Chord tones have more freedom in movement
3. Non-chord tones are restricted to moving to adjacent scale notes
4. Phrases are connected naturally by considering the previous note
5. All generated notes stay within the specified scale

### Real-time Feedback
Pitch Detection Demo:

https://github.com/user-attachments/assets/fd9e6e3f-85f1-42be-a6c8-b757da478854

The application provides real-time feedback by:
1. Capturing audio from your microphone
2. Detecting the pitch using FCPE (Fast Context-aware Pitch Estimation)
3. Converting the frequency to the nearest musical note
4. Displaying both the target note and your sung note in real-time

## Development
### Running Lint
```bash
make lint
```

### Running Format
```bash
make format
```

### Running Tests
```bash
make test
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
