import random
hangmans = ['''

  +---+
  |   |
      |
      |
      |
      |
=========''','''

  +---+
  |   |
  O   |
      |
      |
      |
=========''','''

  +---+
  |   |
  O   |
  |   |
      |
      |
=========''','''

  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''','''

  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''','''

  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''','''

  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']


def userchoice():  # выбор одной из трех категорий
    while True:
        print('Choice one theme:\n1 - cities\n2 - birds\n3 - colors')
        choice = input()
        if choice == '1':
            return 'cities'
        elif choice == '2':
            return 'birds'
        elif choice == '3':
            return 'colors'


def randomword(theme):  # программа выбирает рандомное слово из категории
    with open(theme + '.txt', encoding='utf-8') as f:
        words = f.read().split('\n')
    return random.choice(words)


def display(pict, missedlett, correctlett,secretword):
    print(pict[len(missedlett)])
    print()
    print('Осталось попыток:', 6-len(missedlett))
    print('Неправильные буквы:', end=' ')
    for letter in missedlett:
        print(letter, end=' ')
    print()

    blanks = '_'*len(secretword)

    for i in  range(len(secretword)):  # меняет _ на буквы
        if secretword[i] in correctlett:
            blanks = blanks[:i] + secretword[i] + blanks[i+1:]

    for letter in blanks:
        print(letter, end=' ')
    print()


def getletter(lettersguessed):  # проверяет ввод
    while True:
        print('Введите букву')
        letter = input()
        letter = letter.lower()
        if len(letter) != 1:
            print('Попробуйте снова')
        elif letter in lettersguessed:
            print ('Вы уже пробовали эту букву. Выберите другую')
        elif letter not in 'ёйцукенгшщзхъфывапролджэячсмитьбю':
            print('Пожалуйста, введите букву кириллицы')
        else:
            return letter


def onemoregame():
    print('Хотите попробовать еще раз? ("Да" или "Нет")')
    return input().lower().startswith('д')


def main():
    missedletters = ''
    correctletters = ''
    progword = randomword(userchoice())
    thend = False
    while True:
        display(hangmans, missedletters, correctletters, progword)
        lett = getletter(missedletters + correctletters)
        if lett in progword:  # проверка условия выиграша
            correctletters = correctletters + lett
            foundall = True
            for i in range(len(progword)):
                if progword[i] not in correctletters:
                    foundall = False
                    break
            if foundall:
                print('Превосходно! Было загадано слово "' + progword + '"! Вы победили!')
                thend = True
        else:  # проверка условия проигрыша
            missedletters = missedletters + lett
            if len(missedletters) == len(hangmans) - 1:
                display(hangmans, missedletters, correctletters, progword)
                print('У вас не осталось попыток!\nЗагаданное слово:"' + progword + '"')
                thend = True
        if thend:  # еще одна игра
            if onemoregame():
                missedletters = ''
                correctletters = ''
                thend = False
                progword = randomword(userchoice())
            else:
                break

if __name__ == '__main__':
    main()