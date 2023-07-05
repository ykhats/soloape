from django.shortcuts import render

# Should have been in serving.py, but faced problems with import
from urllib.parse import quote, unquote

from pychord import Chord

from pychord.utils import val_to_note, note_to_val, transpose_note

from pychord.constants.qualities import DEFAULT_QUALITIES


# Roots in tonal order. Felt cute, might change later
ROOT_LIST = [
    'Ab',
    'A',
    'A#',
    'Bb',
    'B',
    'Cb',
    'C',
    'C#',
    'Db',
    'D',
    'D#',
    'Eb',
    'E',
    'F',
    'F#',
    'Gb',
    'G',
    'G#',
]

# scale_name:values for key of C — formed with function in data_util.py from scales_data.csv
# Source update is needed
DEFAULT_SCALES_DICT = {'lydian': [0, 2, 4, 6, 7, 9, 11],
                  'major': [0, 2, 4, 5, 7, 9, 11], 
                  'mixolydian': [0, 2, 4, 5, 7, 9, 10], 
                  'dorian': [0, 2, 3, 5, 7, 9, 10], 
                  'aeolian': [0, 2, 3, 5, 7, 8, 10], 
                  'phrygian': [0, 1, 3, 5, 7, 8, 10], 
                  'locrian': [0, 1, 3, 5, 6, 8, 10], 
                  'melodic minor': [0, 2, 3, 5, 7, 9, 11], 
                  'melodic minor second mode': [0, 1, 3, 5, 7, 9, 10], 
                  'lydian augmented': [0, 2, 4, 6, 8, 9, 11], 
                  'lydian dominant': [0, 2, 4, 6, 7, 9, 10], 
                  'melodic minor fifth mode': [0, 2, 4, 5, 7, 8, 10], 
                  'locrian #2': [0, 2, 3, 5, 6, 8, 10], 
                  'locrian major': [0, 2, 4, 5, 6, 8, 10], 
                  'altered': [0, 1, 3, 4, 6, 8, 10], 
                  'major pentatonic': [0, 2, 4, 7, 9], 
                  'lydian pentatonic': [0, 4, 6, 7, 11], 
                  'mixolydian pentatonic': [0, 4, 5, 7, 10], 
                  'locrian pentatonic': [0, 3, 5, 6, 10], 
                  'minor pentatonic': [0, 3, 5, 7, 10], 
                  'minor six pentatonic': [0, 3, 5, 7, 9], 
                  'minor hexatonic': [0, 2, 3, 5, 7, 11], 
                  'flat three pentatonic': [0, 2, 3, 7, 9], 
                  'flat six pentatonic': [0, 2, 4, 7, 8], 
                  'major flat two pentatonic': [0, 1, 4, 7, 9], 
                  'whole tone pentatonic': [0, 4, 6, 8, 10], 
                  'ionian pentatonic': [0, 4, 5, 7, 11], 
                  'lydian #5 pentatonic': [0, 4, 6, 8, 11], 
                  'lydian dominant pentatonic': [0, 4, 6, 7, 10], 
                  'minor #7 pentatonic': [0, 3, 5, 7, 11], 
                  'super locrian pentatonic': [0, 3, 4, 6, 10], 
                  'in-sen': [0, 1, 5, 7, 10], 
                  'iwato': [0, 1, 5, 6, 10], 
                  'hirajoshi': [0, 2, 3, 7, 8], 
                  'kumoijoshi': [0, 1, 5, 7, 8], 
                  'pelog': [0, 1, 3, 7, 8], 
                  'vietnamese 1': [0, 3, 5, 7, 8], 
                  'vietnamese 2': [0, 3, 5, 7, 10], 
                  'prometheus': [0, 2, 4, 6, 9, 10], 
                  'prometheus neopolitan': [0, 1, 4, 6, 9, 10], 
                  'ritusen': [0, 2, 5, 7, 9], 
                  'scriabin': [0, 1, 4, 7, 9], 
                  'piongio': [0, 2, 5, 7, 9, 10], 
                  'major blues': [0, 2, 3, 4, 7, 9], 
                  'minor blues': [0, 3, 5, 6, 7, 10], 
                  'composite blues': [0, 2, 3, 4, 5, 6, 7, 9, 10], 
                  'augmented': [0, 3, 4, 7, 8, 11],
                  'augmented heptatonic': [0, 3, 4, 5, 7, 8, 11], 
                  'dorian #4': [0, 2, 3, 6, 7, 9, 10], 
                  'lydian diminished': [0, 2, 3, 6, 7, 9, 11], 
                  'whole tone': [0, 2, 4, 6, 8, 10], 
                  'leading whole tone': [0, 2, 4, 6, 8, 10, 11], 
                  'harmonic minor': [0, 2, 3, 5, 7, 8, 11], 
                  'lydian minor': [0, 2, 4, 6, 7, 8, 10], 
                  'neopolitan': [0, 1, 3, 5, 7, 8, 11], 
                  'neopolitan minor': [0, 1, 3, 5, 7, 8, 10], 
                  'neopolitan major': [0, 1, 3, 5, 7, 9, 11], 
                  'neopolitan major pentatonic': [0, 4, 5, 6, 10], 
                  'romanian minor': [0, 2, 3, 6, 7, 9, 10], 
                  'double harmonic lydian': [0, 1, 4, 6, 7, 8, 11], 
                  'diminished': [0, 2, 3, 5, 6, 8, 9, 11], 
                  'harmonic major': [0, 2, 4, 5, 7, 8, 11], 
                  'double harmonic major': [0, 1, 4, 5, 7, 8, 11], 
                  'egyptian': [0, 2, 5, 7, 10], 
                  'hungarian minor': [0, 2, 3, 6, 7, 8, 11], 
                  'hungarian major': [0, 3, 4, 6, 7, 9, 10], 
                  'oriental': [0, 1, 4, 5, 6, 9, 10], 
                  'spanish': [0, 1, 4, 5, 7, 8, 10], 
                  'spanish heptatonic': [0, 1, 3, 4, 5, 7, 8, 10], 
                  'flamenco': [0, 1, 3, 4, 6, 7, 10], 
                  'balinese': [0, 1, 3, 5, 7, 8, 11], 
                  'todi raga': [0, 1, 3, 6, 7, 8, 11], 
                  'malkos raga': [0, 3, 5, 8, 10], 
                  'kafi raga': [0, 3, 4, 5, 7, 9, 10, 11], 
                  'purvi raga': [0, 1, 4, 5, 6, 7, 8, 11], 
                  'persian': [0, 1, 4, 5, 6, 8, 11], 
                  'bebop': [0, 2, 4, 5, 7, 9, 10, 11], 
                  'bebop dominant': [0, 2, 4, 5, 7, 9, 10, 11], 
                  'bebop minor': [0, 2, 3, 4, 5, 7, 9, 10], 
                  'bebop major': [0, 2, 4, 5, 7, 8, 9, 11], 
                  'bebop locrian': [0, 1, 3, 5, 6, 7, 8, 10], 
                  'minor bebop': [0, 2, 3, 5, 7, 8, 10, 11], 
                  'mystery #1': [0, 1, 4, 6, 8, 10], 
                  'enigmatic': [0, 1, 4, 6, 8, 10, 11], 
                  'minor six diminished': [0, 2, 3, 5, 7, 8, 9, 11], 
                  'ionian augmented': [0, 2, 4, 5, 8, 9, 11], 
                  'lydian #9': [0, 1, 4, 6, 7, 9, 11], 
                  'ichikosucho': [0, 2, 4, 5, 6, 7, 9, 11], 
                  'six tone symmetric': [0, 1, 4, 5, 8, 9], 
                  'Diminished Half-Whole': [0, 1, 3, 4, 6, 7, 9, 10], 
                  'Hindu': [0, 2, 4, 5, 7, 8, 10]
                  }

# quality:scale_names — formed with function in data_util.py from matches_data.csv
# Source update is needed (both for quality list and matches lists) 
QUALITY_TO_SCALES_MATCHES_DICT = {
    "major": [
        "major",
        "major pentatonic",
        "minor blues",
        "bebop major",
        "mixolydian",
        "lydian",
        "mixolydian pentatonic",
    ],
    "minor": [
        "dorian",
        "aeolian",
        "minor pentatonic",
        "phrygian",
        "minor blues",
        "melodic minor",
        "harmonic minor",
        "bebop minor",
    ],
    "∆": ["major", "major pentatonic", "bebop major", "lydian"],
    "∆#4": ["lydian", "major pentatonic"],
    "∆#4#5": ["lydian augmented", "lydian #5 pentatonic"],
    "∆#5#4": ["lydian augmented", "lydian #5 pentatonic"],
    "∆+4": ["lydian", "major pentatonic"],
    "∆+4+5": ["lydian augmented", "lydian #5 pentatonic"],
    "∆+5+4": ["lydian augmented", "lydian #5 pentatonic"],
    "∆13": ["major", "major pentatonic", "bebop major", "lydian"],
    "∆7": ["major", "major pentatonic", "bebop major", "lydian"],
    "∆7#11": ["lydian", "major pentatonic"],
    "∆7#4": ["lydian", "major pentatonic"],
    "∆7#4#5": ["lydian augmented", "lydian #5 pentatonic"],
    "∆7#5": ["lydian augmented"],
    "∆7#5#4": ["lydian augmented", "lydian #5 pentatonic"],
    "∆7+4": ["lydian", "major pentatonic"],
    "∆7+4+5": ["lydian augmented", "lydian #5 pentatonic"],
    "∆7add2": ["major", "major pentatonic", "bebop major", "lydian"],
    "∆7add4": ["major", "major pentatonic"],
    "∆7add6": ["major", "major pentatonic"],
    "∆7b6": ["harmonic minor"],
    "∆9": ["major", "major pentatonic", "bebop major", "lydian"],
    "∆9#11": ["lydian", "major pentatonic"],
    "∆b6": ["harmonic minor"],
    "+": ["altered", "whole tone"],
    "+11": ["ionian augmented", "bebop major", "six tone symmetric"],
    "+13": ["lydian augmented"],
    "+7": ["whole tone", "altered"],
    "+9": ["whole tone"],
    "+M11": ["harmonic major", "double harmonic major"],
    "+M13": ["lydian augmented"],
    "+M9": ["lydian augmented", "lydian #5 pentatonic"],
    "+maj7": ["lydian augmented", "lydian #5 pentatonic"],
    "−": [
        "dorian",
        "aeolian",
        "minor pentatonic",
        "phrygian",
        "minor blues",
        "melodic minor",
        "harmonic minor",
        "bebop minor",
    ],
    "−#5": ["harmonic minor", "aeolian"],
    "−∆": ["melodic minor", "harmonic minor"],
    "−∆7": ["melodic minor", "harmonic minor"],
    "−∆7add2": ["melodic minor", "harmonic minor"],
    "−∆7add4": ["melodic minor", "harmonic minor"],
    "−∆7add6": ["melodic minor"],
    "−∆9": ["melodic minor", "harmonic minor"],
    "−11": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "−13": ["dorian"],
    "−6": ["dorian", "bebop minor", "melodic minor"],
    "−6/9": ["dorian", "bebop minor"],
    "−7": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "phrygian",
    ],
    "−7add2": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "−7add4": ["mixolydian", "bebop dominant"],
    "−7add6": ["dorian", "bebop minor", "melodic minor"],
    "−7b5": ["locrian", "locrian #2"],
    "−7dim5": ["locrian", "locrian #2"],
    "−7o5": ["locrian", "locrian #2"],
    "−9": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "−add2": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "melodic minor",
        "harmonic minor",
    ],
    "−add4": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "−add6": ["dorian", "bebop minor", "melodic minor"],
    "−add9": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "melodic minor",
        "harmonic minor",
    ],
    "−b6": ["aeolian", "minor pentatonic", "harmonic minor"],
    "−b6b9": ["phrygian"],
    "−b9b6": ["phrygian"],
    "−maj7": ["melodic minor", "harmonic minor"],
    "ø": ["locrian", "locrian #2"],
    "ø7": ["locrian", "locrian #2"],
    "ø9": ["locrian #2"],
    "ø9#2": ["locrian #3"],
    "ø9+2": ["locrian #2"],
    "ø11": ["locrian"],
    "øb9": ["altered", "Diminished Half-Whole"],
    "o": ["diminished"],
    "o∆7": ["diminished"],
    "o7": ["diminished"],
    "o9": ["diminished"],
    "o11": ["locrian #2"],
    "oM7": ["diminished"],
    "omaj7": ["diminished"],
    "2": [
        "major",
        "major pentatonic",
        "minor blues",
        "mixolydian",
        "lydian dominant",
        "lydian",
        "aeolian",
        "minor pentatonic",
        "dorian",
        "melodic minor",
        "harmonic minor",
        "bebop major",
        "bebop minor",
        "bebop dominant",
    ],
    "2sus": [
        "major",
        "major pentatonic",
        "minor blues",
        "mixolydian",
        "lydian dominant",
        "lydian",
        "aeolian",
        "minor pentatonic",
        "dorian",
        "melodic minor",
        "harmonic minor",
        "bebop major",
        "bebop minor",
        "bebop dominant",
    ],
    "4sus": ["mixolydian", "bebop dominant"],
    "5": [
        "major",
        "major pentatonic",
        "minor blues",
        "mixolydian",
        "lydian dominant",
        "lydian",
        "aeolian",
        "minor pentatonic",
        "dorian",
        "melodic minor",
        "harmonic minor",
        "bebop major",
        "bebop minor",
        "bebop dominant",
    ],
    "6": ["major", "minor blues", "major pentatonic", "bebop major", "lydian"],
    "6/9": ["major", "minor blues", "major pentatonic", "bebop major", "lydian"],
    "7": [
        "mixolydian",
        "bebop dominant",
        "lydian dominant",
        "flamenco",
        "Diminished Half-Whole",
        "whole tone",
        "altered",
        "spanish",
        "major pentatonic",
        "minor blues",
    ],
    "7#11": ["lydian dominant", "major pentatonic", "minor blues"],
    "7#11#9": ["altered", "Diminished Half-Whole"],
    "7#4": ["lydian dominant", "lydian dominant pentatonic"],
    "7#5": ["whole tone", "altered", "whole tone pentatonic"],
    "7#5#9": ["altered"],
    "7#9": ["altered", "Diminished Half-Whole"],
    "7#9#11": ["altered", "Diminished Half-Whole"],
    "7#9#5": ["altered"],
    "7#9b5": ["altered", "Diminished Half-Whole"],
    "7#9b9": ["altered", "Diminished Half-Whole"],
    "7+": ["whole tone", "altered"],
    "7+11": ["lydian dominant", "major pentatonic", "minor blues"],
    "7+11+9": ["altered", "Diminished Half-Whole"],
    "7+4": ["lydian dominant", "lydian dominant pentatonic"],
    "7+5": ["whole tone", "altered", "whole tone pentatonic"],
    "7+5+9": ["altered"],
    "7+9": ["altered", "Diminished Half-Whole"],
    "7+9+11": ["altered", "Diminished Half-Whole"],
    "7+9+5": ["altered"],
    "7+9b5": ["altered", "Diminished Half-Whole"],
    "7+9b9": ["altered", "Diminished Half-Whole"],
    "7add2": ["mixolydian", "major pentatonic", "lydian dominant", "bebop dominant"],
    "7add4": ["mixolydian", "bebop dominant"],
    "7add6": ["mixolydian", "major pentatonic", "lydian dominant", "bebop dominant"],
    "7alt": ["altered"],
    "7aug": ["whole tone", "altered"],
    "7b13": ["spanish", "altered"],
    "7b13b9": ["spanish", "altered"],
    "7b13sus": ["spanish"],
    "7b13sus4": ["spanish"],
    "7b5": [
        "lydian dominant",
        "whole tone",
        "whole tone pentatonic",
        "altered",
        "Diminished Half-Whole",
    ],
    "7b6": ["Hindu"],
    "7b9": ["spanish", "altered", "Diminished Half-Whole"],
    "7b9#11": ["altered", "Diminished Half-Whole"],
    "7b9#5": ["altered"],
    "7b9#9": ["altered", "Diminished Half-Whole"],
    "7b9+11": ["altered", "Diminished Half-Whole"],
    "7b9+5": ["altered"],
    "7b9+9": ["altered", "Diminished Half-Whole"],
    "7b9b13": ["spanish", "altered"],
    "7b9b5": ["altered", "Diminished Half-Whole"],
    "7b9sus": ["spanish", "phrygian"],
    "7b9sus4": ["spanish", "phrygian"],
    "7sus": ["mixolydian", "bebop dominant"],
    "7sus4": ["mixolydian", "bebop dominant"],
    "7sus4add3": ["mixolydian", "bebop dominant"],
    "7susadd3": ["mixolydian", "bebop dominant"],
    "9": [
        "mixolydian",
        "bebop dominant",
        "lydian dominant",
        "lydian dominant pentatonic",
        "whole tone",
        "whole tone pentatonic",
        "major pentatonic",
        "minor blues",
    ],
    "9#11": ["lydian dominant"],
    "9#5": ["whole tone"],
    "9+": ["whole tone"],
    "9+11": ["lydian dominant"],
    "9+5": ["whole tone"],
    "9aug": ["whole tone"],
    "9b5": ["lydian dominant", "whole tone"],
    "9sus": ["mixolydian", "bebop dominant"],
    "9sus4": ["mixolydian", "bebop dominant"],
    "11": ["mixolydian", "bebop dominant"],
    "11#5": ["ionian augmented", "bebop major", "six tone symmetric"],
    "13": [
        "mixolydian",
        "bebop minor",
        "lydian dominant",
        "major pentatonic",
        "minor blues",
    ],
    "13#11": ["lydian dominant", "major pentatonic", "minor blues"],
    "13#5": ["lydian augmented"],
    "13#9": ["Diminished Half-Whole"],
    "13+11": ["lydian dominant", "major pentatonic", "minor blues"],
    "13+9": ["Diminished Half-Whole"],
    "13b9": ["Diminished Half-Whole"],
    "13sus": ["mixolydian", "bebop dominant"],
    "13sus4": ["mixolydian", "bebop dominant"],
    "add2": [
        "major",
        "mixolydian",
        "major pentatonic",
        "lydian dominant",
        "bebop dominant",
    ],
    "add4": ["major", "mixolydian", "major pentatonic", "bebop dominant"],
    "add6": ["major", "minor blues", "major pentatonic", "bebop major", "lydian"],
    "add9": [
        "major",
        "mixolydian",
        "lydian",
        "major pentatonic",
        "minor blues",
        "bebop major",
    ],
    "aug": ["altered", "whole tone"],
    "aug11": ["ionian augmented", "bebop major", "six tone symmetric"],
    "aug13": ["lydian augmented"],
    "aug7": ["whole tone", "altered"],
    "aug9": ["whole tone"],
    "augmaj11": ["harmonic major", "double harmonic major"],
    "augmaj13": ["lydian augmented"],
    "augmaj7": ["lydian augmented", "lydian #5 pentatonic"],
    "augmaj9": ["lydian augmented", "lydian #5 pentatonic"],
    "dim": ["diminished"],
    "dim11": ["locrian #3"],
    "dim7": ["diminished"],
    "dim9": ["diminished"],
    "m": [
        "dorian",
        "aeolian",
        "minor pentatonic",
        "phrygian",
        "minor blues",
        "melodic minor",
        "harmonic minor",
        "bebop minor",
    ],
    "m7": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "phrygian",
    ],
    "M#5": ["altered", "whole tone"],
    "m#5": ["harmonic minor", "aeolian"],
    "m∆": ["melodic minor", "harmonic minor"],
    "m∆7": ["melodic minor", "harmonic minor"],
    "m∆9": ["melodic minor", "harmonic minor"],
    "M+5": ["altered", "whole tone"],
    "m11": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "M11": ["major"],
    "M13": ["major", "major pentatonic", "bebop major", "lydian"],
    "m13": ["dorian"],
    "m6": ["dorian", "bebop minor", "melodic minor"],
    "m6/9": ["dorian", "bebop minor"],
    "M7#11": ["lydian", "major pentatonic"],
    "M7#4": ["lydian", "major pentatonic"],
    "m7b5": ["locrian", "locrian #4"],
    "m7dim5": ["locrian", "locrian #2"],
    "m7o5": ["locrian", "locrian #2"],
    "M9": ["major", "major pentatonic", "bebop major", "lydian"],
    "m9": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "madd9": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "melodic minor",
        "harmonic minor",
    ],
    "maj": [
        "major",
        "major pentatonic",
        "minor blues",
        "bebop major",
        "mixolydian",
        "lydian",
        "mixolydian pentatonic",
    ],
    "maj11": ["major"],
    "maj11#5": ["harmonic major", "double harmonic major"],
    "maj11+5": ["harmonic major", "double harmonic major"],
    "maj13": ["major", "major pentatonic", "bebop major", "lydian"],
    "maj7": ["major", "major pentatonic", "bebop major", "lydian"],
    "maj7#11": ["lydian", "major pentatonic"],
    "maj7#4": ["lydian", "major pentatonic"],
    "maj7#5": ["lydian augmented"],
    "maj7+": ["lydian augmented", "lydian #5 pentatonic"],
    "maj7aug": ["lydian augmented", "lydian #5 pentatonic"],
    "maj9": ["major", "major pentatonic", "bebop major", "lydian"],
    "maj9#11": ["lydian", "major pentatonic"],
    "mb5": ["diminished"],
    "mb6": ["aeolian", "minor pentatonic", "harmonic minor"],
    "mb6b9": ["phrygian"],
    "mb9b6": ["phrygian"],
    "mi": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "phrygian",
    ],
    "mi#5": ["harmonic minor", "aeolian"],
    "mi∆": ["melodic minor", "harmonic minor"],
    "mi∆7": ["melodic minor", "harmonic minor"],
    "mi∆9": ["melodic minor", "harmonic minor"],
    "mi11": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "mi13": ["dorian"],
    "mi6": ["dorian", "bebop minor", "melodic minor"],
    "mi6/9": ["dorian", "bebop minor"],
    "mi7b5": ["locrian", "locrian #5"],
    "mi9": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "mib6": ["aeolian", "minor pentatonic", "harmonic minor"],
    "mib6b9": ["phrygian"],
    "mib9b6": ["phrygian"],
    "min": [
        "dorian",
        "aeolian",
        "minor pentatonic",
        "phrygian",
        "minor blues",
        "melodic minor",
        "harmonic minor",
        "bebop minor",
    ],
    "min#5": ["harmonic minor", "aeolian"],
    "min∆": ["melodic minor", "harmonic minor"],
    "min∆7": ["melodic minor", "harmonic minor"],
    "min∆9": ["melodic minor", "harmonic minor"],
    "min11": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "min13": ["dorian"],
    "min6": ["dorian", "bebop minor", "melodic minor"],
    "min6/9": ["dorian", "bebop minor"],
    "min7": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "phrygian",
    ],
    "min7b5": ["locrian", "locrian #3"],
    "min7dim5": ["locrian", "locrian #2"],
    "min7o5": ["locrian", "locrian #2"],
    "min9": ["dorian", "minor pentatonic", "minor blues", "bebop minor", "aeolian"],
    "minadd9": [
        "dorian",
        "minor pentatonic",
        "minor blues",
        "bebop minor",
        "aeolian",
        "melodic minor",
        "harmonic minor",
    ],
    "minb5": ["diminished"],
    "minb6": ["aeolian", "minor pentatonic", "harmonic minor"],
    "minb6b9": ["phrygian"],
    "minb9b6": ["phrygian"],
    "minM7": ["melodic minor", "harmonic minor"],
    "minM9": ["melodic minor", "harmonic minor"],
    "minmaj7": ["melodic minor", "harmonic minor"],
    "minmaj9": ["melodic minor", "harmonic minor"],
    "mino5": ["diminished"],
    "mo5": ["diminished"],
    "sus": ["mixolydian", "bebop dominant"],
    "sus2": [
        "major",
        "major pentatonic",
        "minor blues",
        "mixolydian",
        "lydian dominant",
        "lydian",
        "aeolian",
        "minor pentatonic",
        "dorian",
        "melodic minor",
        "harmonic minor",
        "bebop major",
        "bebop minor",
        "bebop dominant",
    ],
    "sus4": ["mixolydian", "bebop dominant"],
}


# chord_list serving functions 

def get_quality_list(default_qualities_pychord):
    """Get list of qualities from DEFAULT_QUALITIES const in pychord."""
    quality_list = [q[0] for q in default_qualities_pychord]
    return quality_list


def encode_list_for_url(list_to_code: list) -> list:
    """Resolve issue with special characters used in qualities, like '#', '(' and ')'."""
    quality_to_quote_dict = [
        {'title': q, 'quote': quote(q)} for q in list_to_code]
    return quality_to_quote_dict


# Render VIEW function
def chords_list(request):
    template = 'chords_catalog/list.html'
    root_list = ROOT_LIST
    quality_list = get_quality_list(DEFAULT_QUALITIES)
    context = {
        'root_list': encode_list_for_url(root_list),
        'quality_list': encode_list_for_url(quality_list),
    }
    return render(request, template, context)


# chord_detail serving functions 

def get_chord_scales(user_chord: Chord) -> list:
    """Get list of scales that can be played over given chord."""
    chord_scales = QUALITY_TO_SCALES_MATCHES_DICT[str(user_chord.quality)]
    return chord_scales


def get_scale_notes(scale: str, key: str  = 'C') -> list:
    """
    Get list of notes from scale name and key note:
    >>>get_scale_notes('dorian', 'A')
    ['A', 'B', 'C', 'D', 'E', 'F#', 'G']
    """
    scale_default_values = DEFAULT_SCALES_DICT.get(scale)
    # Превращаем список values в список нот
    scale_notes = []
    for val in scale_default_values:
        scale_notes.append(val_to_note(val))
    # Транспонируем ноты по root аккорда
    scale_transposed_notes = []
    for value in scale_notes:
        transpose_index = note_to_val(key)
        transposed_note = transpose_note(value, transpose_index, key)
        scale_transposed_notes.append(transposed_note)
    return scale_transposed_notes 


def get_scale_values(scale: str, key: str  = 'C') -> list:
    """
    Get list of values from scale name and key note:
    >>>get_scale_values('dorian', 'A')
    [9, 11, 0, 2, 4, 6, 7]
    """
    scale_transposed_notes = get_scale_notes(scale, key)
    scale_transposed_values = []
    for note in scale_transposed_notes:
        scale_transposed_values.append(note_to_val(note))
    return scale_transposed_values  


def get_scale_values_from_notes(scale_transposed_notes: list) -> list:
    """
    Get list of values from list of notes:
    >>>get_scale_values_from_notes(['A', 'B', 'C', 'D', 'E', 'F#', 'G'])
    [9, 11, 0, 2, 4, 6, 7]
    """
    scale_transposed_values = []
    for note in scale_transposed_notes:
        scale_transposed_values.append(note_to_val(note))
    return scale_transposed_values  # [9, 11, 0, 2, 4, 6, 7] for 'A dorian'


def get_scale_info(scale: str, key: str ='C') -> dict:
    """
    Collect a dictionary of info for a given scale and root
    """
    scale_info = {}
    scale_info['scale_name'] = f'{key} {scale}'
    scale_info['scale_quality'] = {scale}
    scale_info['scale_key'] = {key}
    scale_notes = get_scale_notes(scale, key)
    scale_info['scale_notes'] = scale_notes
    scale_info['scale_values'] = get_scale_values_from_notes(scale_notes)
    return scale_info


def chord_detail(request, chord_name):
    template = 'chords_catalog/detail.html'
    
    # Chord info prepare
    chord_name = unquote(chord_name)
    selected_chord = Chord(chord_name)
    chord_root = selected_chord.root
    chord_quality = selected_chord.quality
    chord_notes = selected_chord.components(visible=True)
    chord_values = selected_chord.components(visible=False)
    chord_scales_list = get_chord_scales(selected_chord)

    # Scale info prepare
    chord_scales = []
    for scale in chord_scales_list:
        chord_scales.append(get_scale_info(scale, chord_root))

    context = {
        # Chord info
        'chord_name': chord_name,
        'selected_chord': selected_chord,
        'chord_root': chord_root,
        'chord_quality': chord_quality,
        'chord_notes': chord_notes,
        'chord_values': chord_values,
        'chord_scales': chord_scales,
        # Scales info 
        'chord_scales': chord_scales,  # List of dictionaries
    }
    return render(request, template, context)




#teststuff


# chord_name = 'Am9'
# selected_chord = Chord(chord_name)
# chord_root = selected_chord.root
# chord_quality = selected_chord.quality
# chord_notes = selected_chord.components(visible=True)
# chord_values = selected_chord.components(visible=False)
# chord_scales_list = get_chord_scales(selected_chord)











# get_scale_info(chord_scales[0], chord_root)


# print('Какой лад будете использовать?')
# user_scale_input = (input('Ваш ответ: '))  # choose scale

# scale_notes = get_scale_notes('dorian', 'A')

# print(scale_notes)

# print(get_scale_values_from_notes(scale_notes))




# def scale_to_notes(scale: str, key: str  = 'C') -> list:
#     scale_values = DEFAULT_SCALES_DICT.get(scale)
#     # Превращаем список values в список нот
#     scale_notes = []
#     for val in scale_values:
#         scale_notes.append(val_to_note(val))
#     # Транспонируем ноты по root аккорда
#     scale_transposed_values = []
#     for value in scale_notes:
#         transpose_index = note_to_val(key)
#         transponded_note = transpose_note(value, transpose_index, key)
#         scale_transposed_values.append(transponded_note)
#     return scale_transposed_values