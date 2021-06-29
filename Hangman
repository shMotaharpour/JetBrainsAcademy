import random
import re
words = ['python', 'java', 'kotlin', 'javascript']

def game():
    word = random.choice(words)
    res = ['-'] * len(word)
    word_set = set(word)
    used_set = set()
    life = 8
    while life and len(word_set):
        print('\n', *res, sep='')
        ch = input('Input a letter:')
        if len(ch) != 1:
            print('You should input a single letter')
            continue
        if re.match('[^a-z]', ch):
            print('Please enter a lowercase English letter')
            continue
        if ch in word_set:
            word_set.remove(ch)
            used_set.add(ch)
            for e, m in enumerate(word):
                if m == ch:
                    res[e] = ch
        elif ch in used_set:
            print("You've already guessed this letter")
        else:
            life -= 1
            used_set.add(ch)
            print("That letter doesn't appear in the word")
    if life:
        print(r'You guessed the word {word}!', 'You survived!\n', sep='\n')
    else:
        print("You lost!\n")

print('H A N G M A N')
while True:
    com = input('Type "play" to play the game, "exit" to quit:')
    if com == 'exit':
        break
    elif com == 'play':
        game()
