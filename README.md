# Improvisation Lab

A Python package for generating musical improvisation melodies based on music theory principles. The package specializes in creating natural-sounding melodic phrases that follow chord progressions while respecting musical rules, with real-time pitch detection for practice feedback.

Improvisation Lab Demo

https://github.com/user-attachments/assets/cca490ec-0c81-4128-9dc6-337ea472f014

## Features

- Generate melodic phrases based on scales and chord progressions
- Support for multiple scale types (major, natural minor, harmonic minor)
- Support for various chord types (maj7, min7, dom7, dim7, etc.)
- Intelligent note selection based on chord tones and scale degrees
- Natural phrase connections and melodic movement
- Real-time pitch detection for practice feedback
- Music theory-based approach to improvisation

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

4. Follow the displayed melody phrases
5. Sing along with the notes shown on screen
6. Get real-time feedback on your pitch accuracy

### Configuration

The application can be customized through a `config.yml` file in the root directory. 
The following options are available:

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
- `chord_progressions`: Dictionary of available songs and their chord progressions
  - Each progression is defined as: `[scale_root, scale_type, chord_root, chord_type, duration]`
  - Supported scale types: major, natural_minor, harmonic_minor
  - Supported chord types: maj7, min7, dom7, min7(b5)

### Custom Songs

You can add your own songs by adding new entries to the `chord_progressions` section:


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
