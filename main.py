from pychord import Chord
from pychord.utils import val_to_note, note_to_val, transpose_note
from data_util import SCALE_PALLETTE_VAL_DICT, MATCHES_DICT

print('')
print('')
print('SOLOAPE')
print('Программа для ЭВМ, версия 0.02')
print('Помогает обыгрывать аккорды since 2023.')
print('')
print('Введите аккорд, чтобы понять, какими нотами его можно обыграть.')
print('')
print('Какой аккорд хотите обыграть?')
user_chord_input = Chord(input('Ваш ответ: '))  # input chord

def get_scales_for_chord(user_chord_quality: Chord) -> list:
    """Получить список ладов, которыми обыгрывается аккорд."""
    return MATCHES_DICT[str(user_chord_quality.quality)]

suggested_scales = get_scales_for_chord(user_chord_input)

print('')
print('Вот какие лады можно использовать:')
for scale in suggested_scales:
    print(scale)
print('')

print('Какой лад будете использовать?')
user_scale_input = (input('Ваш ответ: '))  # choose scale

def scale_to_notes(scale: str) -> list:
    scale_values = SCALE_PALLETTE_VAL_DICT.get(scale)
    # Превращаем список values в список нот
    scale_notes = []
    for val in scale_values:
        scale_notes.append(val_to_note(val))
    # Транспонируем ноты по root аккорда
    scale_transposed_values = []
    for value in scale_notes:
        transpose_index = note_to_val(user_chord_input.root)
        transponded_note = transpose_note(value, transpose_index)
        scale_transposed_values.append(transponded_note)
    return scale_transposed_values

print('')
print('Играйте эти ноты:')
print(*scale_to_notes(user_scale_input))
print('Не благодарите!')
print('')
print('')
