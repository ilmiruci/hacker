import json
import os

from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent.parent

FILE_NAMES: dict[int, str] = {
    4: "four_letter_words.txt",
    5: "five_letter_words.txt",
}

print(BASE_DIR)

file_name = "config.json"
file_path: str = os.path.join(BASE_DIR, file_name)

print(file_path)

# TODO: Написать функцию read_config
# TODO: обработать возможные ошибки
with open(file_path, mode="r", encoding="UTF-8") as file:
    context: dict = json.load(file)

# CONFIG = read_config(
CONFIG = context

attempts = CONFIG.get("very_easy", {}).get("attempts", 4)
length_of_password = CONFIG.get("very_easy", {}).get("length_of_password", 4)
print(f"Количество попыток {attempts}")
print(f"Длина пароля {length_of_password}")

words_filename = os.path.join(
    BASE_DIR,
    'words',
    FILE_NAMES.get(length_of_password)
)
