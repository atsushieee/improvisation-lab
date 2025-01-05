# Improvisation Lab

A Python package for practicing musical improvisation through exercises. This package allows users to generate and practice melodic phrases based on music theory principles, offering real-time pitch detection for immediate feedback. Whether you're following chord progressions or practicing intervals, Improvisation Lab helps you improve your musical skills while adhering to musical rules.

## Try it out! 🚀
<a href="https://huggingface.co/spaces/atsushieee/improvisation-lab" target="_blank">
    <img src="https://img.shields.io/badge/🤗_Demo-Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face Spaces" />
</a>

Watch the demo in action:

### Interval Practice: Demo

https://github.com/user-attachments/assets/6a475cf0-9a82-4103-8316-7d4485b07c2e

### Piece Practice: Demo

https://github.com/user-attachments/assets/fa6e11d6-7b88-4b77-aa6e-a67c0927353d

Experience Improvisation Lab directly in your browser! Our interactive demo lets you:

- Generate melodic phrases based on chord progressions or intervals
- Practice your pitch accuracy in real-time
- Get instant visual guidance for hitting the right notes

### Web Interface Features
- **Tab Switching**: Easily switch between Interval Practice and Piece Practice using tabs in the web interface. This allows you to seamlessly transition between different practice modes without leaving the page.

### Note
The demo runs on Hugging Face Spaces' free tier, which means:
- Performance might vary depending on server availability
- If you encounter any issues, try refreshing the page or coming back later
- For consistent performance, consider running the package locally


## Features

- Web-based and direct microphone input support
- Real-time pitch detection with FCPE (Fast Context-aware Pitch Estimation)
- Provides real-time feedback on pitch accuracy

### Interval Practice: Features
- Focuses on practicing musical intervals.
- Users can select the interval and direction (up or down) to practice.

### Piece Practice: Features
- Allows users to select a song and practice its chord progressions.
- Generate melodic phrases based on scales and chord progressions.
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

3. Run the script to start the melody generation and playback (default is web interface):

- Access the web interface at [http://127.0.0.1:7860/](http://127.0.0.1:7860/).

```bash
make run
```

- To run the console interface, use:

```bash
poetry run python main.py --app_type console
```

4. Follow the displayed melody phrases and sing along with real-time feedback

### Configuration

The application can be customized through `config.yml` with the following options:

#### Common Audio Settings
- `sample_rate`: Audio sampling rate (default: 44100 Hz)
- `buffer_duration`: Duration of audio processing buffer (default: 0.2 seconds)
- `note_duration`: How long to display each note during practice (default: 3 seconds)
- `pitch_detector`: Configuration for the pitch detection algorithm
  - `hop_length`: Hop length for the pitch detection algorithm (default: 512)
  - `threshold`: Threshold for the pitch detection algorithm (default: 0.006)
  - `f0_min`: Minimum frequency for the pitch detection algorithm (default: 80 Hz)
  - `f0_max`: Maximum frequency for the pitch detection algorithm (default: 880 Hz)
  - `device`: Device to use for the pitch detection algorithm (default: "cpu")

#### Interval Practice Settings
- `interval`: The interval to practice
  - Example: For a minor second descending interval, the interval value is -1
- `num_problems`: The number of problems to practice

#### Piece Practice Settings
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

### Interval Practice: Melody Generation
The interval practice focuses on improving interval recognition and singing accuracy:
1. Users select the interval and direction (up or down) to practice.
2. The application generates a series of problems based on the selected interval.
3. Real-time feedback is provided to help users match the target interval.
4. The practice session can be customized with the number of problems and note duration.

### Piece Practice: Melody Generation
The melody generation follows these principles:
1. Notes are selected based on their relationship to the current chord and scale.
2. Chord tones have more freedom in movement.
3. Non-chord tones are restricted to moving to adjacent scale notes.
4. Phrases are connected naturally by considering the previous note.
5. All generated notes stay within the specified scale.

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
