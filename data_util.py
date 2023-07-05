import csv

# Формируем словарь названий ладов и values нот внутри них
SCALE_PALLETTE_VAL_DICT = dict()  # DELAULT_SCALES_DICT

with open("scales_data.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        key = row[0]
        value = [int(x) for x in row[1].split()]
        SCALE_PALLETTE_VAL_DICT[key] = value
file.close()

# Формируем словарь соответствий quality и названий ладов
MATCHES_DICT = dict()

with open("matches_data.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        key = row[0]
        value = row[1:]
        value = [v for v in value if v]  # Remove empty strings
        if value:
            MATCHES_DICT[key] = value
file.close()
