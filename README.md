# Improvisation Lab

A Python package for generating musical improvisation melodies based on music theory principles. The package specializes in creating natural-sounding melodic phrases that follow chord progressions while respecting musical rules.

## Features

- Generate melodic phrases based on scales and chord progressions
- Support for multiple scale types (major, natural minor, harmonic minor)
- Support for various chord types (maj7, min7, dom7, dim7, etc.)
- Intelligent note selection based on chord tones and scale degrees
- Natural phrase connections and melodic movement
- Music theory-based approach to improvisation

## Installation
```bash
make install
```

## Quick Start
```bash
make run
```

## How It Works

The melody generation follows these principles:
1. Notes are selected based on their relationship to the current chord and scale
2. Chord tones have more freedom in movement
3. Non-chord tones are restricted to moving to adjacent scale notes
4. Phrases are connected naturally by considering the previous note
5. All generated notes stay within the specified scale

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
