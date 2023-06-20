from pychord import Chord
from pychord.utils import val_to_note, note_to_val, transpose_note
from data_util import SCALE_PALLETTE_VAL_DICT, MATCHES_DICT

user_chord_input = Chord('Am7')
user_scale_input = 'dorian'

def scale_to_notes(scale: str) -> list:
    scale_values = SCALE_PALLETTE_VAL_DICT.get(scale)
    # Превращаем список values в список нот
    scale_notes = []
    for val in scale_values:
        scale_notes.append(val_to_note(val))
    # Транспонируем values по root аккорда
    scale_transposed_values = []
    for value in scale_notes:
        transpose_index = note_to_val(user_chord_input.root)
        transponded_note = transpose_note(value, transpose_index)
        scale_transposed_values.append(transponded_note)
    return scale_transposed_values

    #     transpose_index: int = note_to_val(user_chord_input.root)  # value от root
    #     transposed_value = value + transpose_index
    #     transposed_value %= 12
    #     scale_transposed_values.append(transposed_value)
    # scale_transposed_values = scale_transposed_values.sort()

    # Транспонируем ноты по ключу из аккорда
    # for note in scale_values:
    #     scale_notes.append(transpose_note(note, note_to_val(user_chord_input.root())))
    # return scale_notes

print(*scale_to_notes(user_scale_input))