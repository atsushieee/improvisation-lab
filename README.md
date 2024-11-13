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
