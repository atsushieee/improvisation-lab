# Improvisation Lab

A Python package for generating musical improvisation melodies based on music theory principles. The package specializes in creating natural-sounding melodic phrases that follow chord progressions while respecting musical rules, with real-time pitch detection for practice feedback.

TODO
![Improvisation Lab Demo](./docs/assets/demo.gif)

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
1. Run the script to start the melody generation and playback:

```bash
make run
```

2. Follow the displayed melody phrases
3. Sing along with the notes shown on screen
4. Get real-time feedback on your pitch accuracy

### Configuration

The application can be customized through a `config.yml` file in the root directory. 
The following options are available:

#### Audio Settings
- `sample_rate`: Audio sampling rate (default: 44100 Hz)
- `buffer_duration`: Duration of audio processing buffer (default: 0.2 seconds)
- `note_duration`: How long to display each note during practice (default: 3 seconds)

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
<div align="center">
  <video width="600" height="150" controls>
    <source src="https://github.com/user-attachments/assets/5512acca-320d-461d-ab03-d595c01ada8c" type="video/mp4">
  </video>
</div>

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
