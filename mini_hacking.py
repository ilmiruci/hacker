"""Мини-игра "h@ck3r" на взлом из "Fallout 3".
Найдите семибуквенное слово, которое является паролем, используя
подсказки после каждой попытки.
"""

# ПРИМЕЧАНИЕ: Для работы программы требуется файл seven_letter_words.txt.

import random, sys

# Установка констант:
# Символы для заполнения "памяти компьютера".
GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

# Загрузка списка WORDS из текстового файла с семибуквенными словами.
with open('seven_letter_words.txt') as wordListFile:
    WORDS = wordListFile.readlines()
for i in range(len(WORDS)):
    # Преобразуем каждое слово в верхний регистр и удаляем символ новой строки:
    WORDS[i] = WORDS[i].strip().upper()


def main():
    """Запуск одной игры "Взлом"."""
    print('''Мини-игра "h@ck3r"
Найдите пароль в памяти компьютера. Вам даются подсказки после
каждой попытки. Например, если секретный пароль – MONITOR, а игрок
угадал CONTAIN, ему будет дана подсказка, что 2 из 7 букв правильные,
потому что и MONITOR, и CONTAIN содержат буквы O и N на 2-й и 3-й позициях.
У вас есть четыре попытки.\n''')
    input('Нажмите Enter, чтобы начать...')

    gameWords = getWords()
    # "Память компьютера" – это просто косметика, но выглядит круто:
    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print()
    print(computerMemory)
    # Начинаем с 4 попыток, уменьшая их количество:
    for triesRemaining in range(4, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('Д О С Т У П   Р А З Р Е Ш Е Н')
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print('Доступ запрещен ({}/7 правильных)'.format(numMatches))
    print('Попытки закончились. Секретный пароль был {}.'.format(secretPassword))


def getWords():
    """Возвращает список из 12 слов, которые могут быть паролем.

    Секретный пароль будет первым словом в списке.
    Чтобы игра была честной, мы стараемся включить слова с разным
    количеством совпадающих букв с секретным словом."""
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    # Находим еще два слова; они не имеют совпадающих букв.
    # Используем "< 3", потому что секретный пароль уже в списке.
    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    # Находим два слова, которые имеют 3 совпадающие буквы
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(words) == 5:
            break  # Нашли 5 слов, выходим из цикла.

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    # Находим хотя бы семь слов, которые имеют хотя бы одну совпадающую букву
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(words) == 12:
            break  # Нашли 7 или более слов, выходим из цикла.

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    # Добавляем случайные слова, чтобы получить 12 слов в общей сложности.
    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)

    assert len(words) == 12
    return words


def getOneWordExcept(blocklist=None):
    """Возвращает случайное слово из WORDS, которого нет в blocklist."""
    if blocklist == None:
        blocklist = []

    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2):
    """Возвращает количество совпадающих букв в этих двух словах."""
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getComputerMemoryString(words):
    """Возвращает строку, представляющую "память компьютера"."""

    # Выбираем по одной строке на каждое слово. Всего 16 строк,
    # но они разделены на две половины.
    linesWithWords = random.sample(range(16 * 2), len(words))
    # Начальный адрес памяти (это тоже косметика).
    memoryAddress = 16 * random.randint(0, 4000)

    # Создаем строку "памяти компьютера".
    computerMemory = []  # Будет содержать 16 строк, по одной на каждую линию.
    nextWord = 0  # Индекс слова в words, которое нужно вставить в строку.
    for lineNum in range(16):  # "Память компьютера" имеет 16 строк.
        # Создаем половину строки из случайных символов:
        leftHalf = ''
        rightHalf = ''
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
        if guess in words:
            return guess
        print('Это не одно из возможных паролей, перечисленных выше.')
        print('Попробуйте ввести "{}" или "{}".'.format(words[0], words[1]))


# Если программа запущена (а не импортирована), запускаем игру:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # При нажатии Ctrl-C завершаем программу.
