import random
import sys
import logging

from utils.hack_utils import (get_difficulty_level, get_max_tries, askForPlayerGuess, getComputerMemoryString, getWords,
                              numMatchingLetters, )
from utils.config import configure_logging

def main():
    print('''Мини-игра "h@ck3r"
Найдите пароль в памяти компьютера. Вам даются подсказки после
каждой попытки. Например, если секретный пароль – MONITOR, а игрок
угадал CONTAIN, ему будет дана подсказка, что 2 из 7 букв правильные,
потому что и MONITOR, и CONTAIN содержат буквы O и N на 2-й и 3-й позициях.
У вас есть четыре попытки.\n''')
    input('Нажмите Enter, чтобы начать...')

    difficulty_level = get_difficulty_level()
    gameWords = getWords()

    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print()
    print(computerMemory)
    max_tries = get_max_tries(difficulty_level)
    for triesRemaining in range(max_tries, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('Д О С Т У П   Р А З Р Е Ш Е Н')
            logger.info("Пароль угадан")
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print('Доступ запрещен ({}/7 правильных)'.format(numMatches))
    print('Попытки закончились. Секретный пароль был {}.'.format(secretPassword))


# Если программа запущена (а не импортирована), запускаем игру:
if __name__ == '__main__':
    logger = logging.getLogger("__name__")
    configure_logging()

    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # При нажатии Ctrl-C завершаем программу.
