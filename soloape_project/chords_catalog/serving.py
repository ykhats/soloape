from urllib.parse import quote, unquote

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


def get_quality_list(default_qualities_pychord):
    """Get list of qualities and encoded versions from DEFAULT_QUALITIES const in pychord"""
    return [q[0] for q in default_qualities_pychord]

def encode_qualities_for_url(quality_list: list) -> list:
    """Resolve issue with special characters used in qualities, like '#', '(' and ')' """
    return [quote(q) for q in quality_list]

def decode_qualities_for_url(quality_list: list) -> list:
    """Resolve issue with special characters used in qualities, like '#', '(' and ')' """
    return [unquote(q) for q in quality_list]


# Получаем данные про выбранный аккорд и его шкалы

# Получаем ноты из аккорда 
def get_chord_notes():
    # pychord?
    ...

# Получаем индексы из нот аккорда
def get_chord_indexes():
    # pychord?
    ...

# Получаем список подходящих шкал из quality аккорда
def get_scales_for_chord():
    ...

# Получаем ноты из индексов шкалы


# Test

from pychord import Chord

selected_chord = Chord('Am7')

def get_scales_for_chord(user_chord_quality: Chord) -> list:
    """Получить список ладов, которыми обыгрывается аккорд."""
    return MATCHES_DICT[str(user_chord_quality.quality)]