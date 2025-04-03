import random, string

# Установка констант:
# Символы для заполнения "памяти компьютера".
# TODO: Вынести в файл констант
# from core.constants import GARBAGE_CHARS
GARBAGE_CHARS: str = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

# TODO: Название файла
# Загрузка списка WORDS из текстового файла с семибуквенными словами.
with open('seven_letter_words.txt') as wordListFile:
    WORDS = wordListFile.readlines()
for i in range(len(WORDS)):
    # Преобразуем каждое слово в верхний регистр и удаляем символ новой строки:
    WORDS[i] = WORDS[i].strip().upper()

def get_difficulty_level() -> str:
    difficulty_level = str(input("Уровень сложности (1-4, 1 - самый сложный, 4 - самый легкий)> "))
    return difficulty_level

def get_max_tries(difficulty_level) -> int:
    match difficulty_level:
        case "1":
            return 4
        case "2":
            return 5
        case "3":
            return 6
        case "4":
            return 7
        # TODO: значение по умолчанию

def getWords() -> list:
    """Возвращает список из 12 слов, которые могут быть паролем.

    Секретный пароль будет первым словом в списке.
    Чтобы игра была честной, мы стараемся включить слова с разным
    количеством совпадающих букв с секретным словом."""
    secretPassword: str = random.choice(WORDS)
    words: list[str] = [secretPassword]

    # Находим еще два слова; они не имеют совпадающих букв.
    # Используем "< 3", потому что секретный пароль уже в списке.
    while len(words) < 3:
        randomWord: str = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    # Находим два слова, которые имеют 3 совпадающие буквы
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(words) == 5:
            break  # Нашли 5 слов, выходим из цикла.

        randomWord: str = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    # Находим хотя бы семь слов, которые имеют хотя бы одну совпадающую букву
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(words) == 12:
            break  # Нашли 7 или более слов, выходим из цикла.

        randomWord: str = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    # Добавляем случайные слова, чтобы получить 12 слов в общей сложности.
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
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2) -> int:
    """Возвращает количество совпадающих букв в этих двух словах."""
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getComputerMemoryString(words) -> str:
    """Возвращает строку, представляющую "память компьютера"."""

    # Выбираем по одной строке на каждое слово. Всего 16 строк,
    # но они разделены на две половины.
    linesWithWords: str = random.sample(range(16 * 2), len(words))
    # Начальный адрес памяти (это тоже косметика).
    memoryAddress: int = 16 * random.randint(0, 4000)

    # Создаем строку "памяти компьютера".
    computerMemory: list[str] = []  # Будет содержать 16 строк, по одной на каждую линию.
    nextWord: int = 0  # Индекс слова в words, которое нужно вставить в строку.
    for lineNum in range(16):  # "Память компьютера" имеет 16 строк.
        # Создаем половину строки из случайных символов:
        leftHalf: str = ''
        rightHalf: str = ''
        for j in range(16):  # Каждая половина строки содержит 16 символов.
            leftHalf += random.choice(GARBAGE_CHARS)
            rightHalf += random.choice(GARBAGE_CHARS)

        # Вставляем слово из списка words:
        if lineNum in linesWithWords:
            # Находим случайное место в половине строки для вставки слова:
            insertionIndex = random.randint(0, 9)
            # Вставляем слово:
            leftHalf = (leftHalf[:insertionIndex] + words[nextWord]
                        + leftHalf[insertionIndex + 7:])
            nextWord += 1  # Переходим к следующему слову.
        if lineNum + 16 in linesWithWords:
            # Находим случайное место в половине строки для вставки слова:
            insertionIndex = random.randint(0, 9)
            # Вставляем слово:
            rightHalf = (rightHalf[:insertionIndex] + words[nextWord]
                         + rightHalf[insertionIndex + 7:])
            nextWord += 1  # Переходим к следующему слову.

            """
            0x13d0;SPECIES?_<*:^/:0x14d0>?(MEXICAN/*=!|;
            0x13e0]@|@}>_^{]|$^=(.0x14e0>}$/-)/}@[~,|)*+
            """

        computerMemory.append('0x' + hex(memoryAddress)[2:].zfill(4)
                              + '  ' + leftHalf + '    '
                              + '0x' + hex(memoryAddress + (16 * 16))[2:].zfill(4)
                              + '  ' + rightHalf)

        memoryAddress += 16  # Переход от, например, 0xe680 к 0xe690.

    # Каждая строка в списке computerMemory объединяется в одну большую строку:
    return '\n'.join(computerMemory)


def askForPlayerGuess(words, tries):
    """Позволяет игроку ввести предположение пароля."""
    while True:
        print('\nВведите пароль: (осталось {} попыток)'.format(tries))
        guess = input('> ').upper()

        # TODO: Изменить логику: Лучше проверить символы
        #  введенного пароля, что содержат только латинские буквы.
        # is_valid_password(guess)
        # while not is_valid_password(guess):
        #     print("Пароль не должен содержать цифры")
        #     guess = input('> ').upper()

        for ch in string.digits:
            while ch in guess:
                print("Пароль не должен содержать цифры")
                guess = input('> ').upper()

        if guess in words:
            return guess
        print('Это не одно из возможных паролей, перечисленных выше.')
        print('Попробуйте ввести "{}" или "{}".'.format(words[0], words[1]))
