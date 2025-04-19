import json
import os
import random
import string
import logging

from .constants import *
from .config import *

logger = logging.getLogger(__name__)

def get_words_file_path(file_name):
    """Получает полный путь до файла со словами (пароли)"""
    words_file_name = f"{file_name}.txt"
    words_file_path = os.path.join(BASE_DIR, "utils", words_file_name)
    # logger.debug("Получили полный путь до файла с паролями")
    return words_file_path


def read_config() -> dict:  # Что возвращает?
    """Открывает файл конфига и возвращает конфиг в виде словаря"""
    config_file_name = "config.json"
    config_file_path = os.path.join(BASE_DIR, "utils", config_file_name)
    with open(config_file_path, mode="r", encoding="UTF-8") as config_file:
        context: dict = json.load(config_file)
    # logger.debug("Открыт файл конфига config.json")
    return context


CONFIG = read_config()


def get_words() -> list[str]:
    """Открывает файл и возвращает список со словами"""
    with open(
        get_words_file_path("seven_letter_words"), mode="r", encoding="UTF-8"
    ) as wordListFile:
        WORDS = wordListFile.readlines()
    for i in range(len(WORDS)):
        WORDS[i] = WORDS[i].strip().upper()
    # logger.debug("Открыт файл seven_letter_words и присвоен содержимое(список слов) переменной WORD")
    return WORDS


def get_difficulty_level() -> str:
    """Выбор уровня сложности игры"""
    difficulty_level: int = 0
    level = ""

    while difficulty_level < 1 or difficulty_level > 5:
        difficulty_level: int = int(
            input(
                "Уровень сложности (1-5, 1 - самый легкий, "
                "5 - самый сложный)> "
            )
        )

    match difficulty_level:
        case 1:
            level = "very_easy"
        case 2:
            level = "easy"
        case 3:
            level = "medium"
        case 4:
            level = "hard"
        case 5:
            level = "very hard"

    logger.info("Выбран уровень %s", level)
    return level


def get_max_tries(difficulty_level) -> int:
    """Выбор максимального количества попыток для угадывания пароля"""
    attempts = CONFIG.get(difficulty_level, {}).get("attempts", 4)
    logger.debug("Переменной attempts задано максимальное количество попыток %s", attempts)
    return attempts


def getWords() -> list:
    """Возвращает список из 12 слов, которые могут быть паролем.

    Секретный пароль будет первым словом в списке.
    Чтобы игра была честной, мы стараемся включить слова с разным
    количеством совпадающих букв с секретным словом."""
    secretPassword: str = random.choice(get_words())
    # logger.debug("Выбран секретный пароль %s", secretPassword)
    words: list[str] = [secretPassword]

    while len(words) < 3:
        randomWord: str = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)
    logger.debug("В randomWord добавлено 2 слова")

    for i in range(500):
        if len(words) == 5:
            break  # Нашли 5 слов, выходим из цикла.

        randomWord: str = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)
    logger.debug("В randomWord добавлено 3 слова")

    for i in range(500):
        if len(words) == 12:
            break

        randomWord: str = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)
    logger.debug("В randomWord добавлено 7 слов")

    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)

    assert len(words) == 12
    return words


def getOneWordExcept(blocklist=None) -> str:
    """Возвращает случайное слово из WORDS, которого нет в blocklist."""
    if blocklist == None:
        blocklist = []

    while True:
        randomWord = random.choice(get_words())
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2) -> int:
    """Возвращает количество совпадающих букв в этих двух словах."""
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    # logger.info("Попытка угадать пароль")
    # logger.info("Совпадающих букв %S", matches)
    return matches


def getComputerMemoryString(words) -> str:
    """Возвращает строку, представляющую "память компьютера"."""

    # Выбираем по одной строке на каждое слово. Всего 16 строк,
    # но они разделены на две половины.
    linesWithWords: int = random.sample(range(16 * 2), len(words))
    # Начальный адрес памяти (это тоже косметика).
    memoryAddress: int = 16 * random.randint(0, 4000)

    # Создаем строку "памяти компьютера".
    computerMemory: list[str] = (
        []
    )  # Будет содержать 16 строк, по одной на каждую линию.
    nextWord: int = 0  # Индекс слова в words, которое нужно вставить в строку.
    for lineNum in range(16):  # "Память компьютера" имеет 16 строк.
        # Создаем половину строки из случайных символов:
        leftHalf: str = ""
        rightHalf: str = ""
        for j in range(16):  # Каждая половина строки содержит 16 символов.
            leftHalf += random.choice(GARBAGE_CHARS)
            rightHalf += random.choice(GARBAGE_CHARS)

        # Вставляем слово из списка words:
        if lineNum in linesWithWords:
            # Находим случайное место в половине строки для вставки слова:
            insertionIndex = random.randint(0, 9)
            # Вставляем слово:
            leftHalf = (
                leftHalf[:insertionIndex]
                + words[nextWord]
                + leftHalf[insertionIndex + 7 :]
            )
            nextWord += 1  # Переходим к следующему слову.
        if lineNum + 16 in linesWithWords:
            # Находим случайное место в половине строки для вставки слова:
            insertionIndex = random.randint(0, 9)
            # Вставляем слово:
            rightHalf = (
                rightHalf[:insertionIndex]
                + words[nextWord]
                + rightHalf[insertionIndex + 7 :]
            )
            nextWord += 1  # Переходим к следующему слову.

        computerMemory.append(
            "0x"
            + hex(memoryAddress)[2:].zfill(4)
            + "  "
            + leftHalf
            + "    "
            + "0x"
            + hex(memoryAddress + (16 * 16))[2:].zfill(4)
            + "  "
            + rightHalf
        )

        memoryAddress += 16  # Переход от, например, 0xe680 к 0xe690.

    # Каждая строка в списке computerMemory объединяется в одну большую строку:
    return "\n".join(computerMemory)


def is_valid_password(guess_answer) -> bool:
    """Валидация пароля на содержание латинских букв"""
    for ch in guess_answer:
        if ch.upper() in string.ascii_uppercase:
            return True
        else:
            return False


def askForPlayerGuess(words, tries):
    """Позволяет игроку ввести предположение пароля."""
    while True:
        print("\nВведите пароль: (осталось {} попыток)".format(tries))
        guess = input("> ").upper()

        while not is_valid_password(guess):
            print("Пароль должен содержать буквы только латинского алфавита")
            guess = input("> ").upper()

        if guess in words:
            return guess
        print("Это не одно из возможных паролей, перечисленных выше.")
        print('Попробуйте ввести "{}" или "{}".'.format(words[0], words[1]))
