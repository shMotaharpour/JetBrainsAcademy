def analysis(text: str):
    return ''.join(ch for ch in text if ch in '01')


def get_sample(num: int) -> str:
    sample = ''
    print(f'Please give AI some data to learn...\nThe current data length is 0, {num} symbols left', end='')
    while len(sample) < num:
        sample += analysis(input('\nPrint a random string containing 0 or 1:\n'))
        if num - len(sample) > 0:
            print('Current data length is {}, {} symbols left'.format(len(sample), max(0, num - len(sample))))
    return sample


data_analysed = {'000': [0, 0, 0, ],
                 '001': [0, 0, 0, ],
                 '010': [0, 0, 0, ],
                 '011': [0, 0, 0, ],
                 '100': [0, 0, 0, ],
                 '101': [0, 0, 0, ],
                 '110': [0, 0, 0, ],
                 '111': [0, 0, 0, ]}


def data_analyser(dda, triads):
    for triad in triads:
        search_inx = 0
        while True:
            search_inx = dda.find(triad, search_inx) + 1
            check_inx = search_inx + 2
            if check_inx < 3 or check_inx >= len(dda):
                break
            next_bit = 0 if dda[check_inx] == '0' else 1
            triads[triad][next_bit] += 1
            triads[triad][2] += 1


def triads_print(dda):
    for tri in dda:
        print('{}: {},{}'.format(tri, dda[tri][0], dda[tri][1]))


def key_max(dic: dict):
    s = 0
    key_ = ''
    for key in dic:
        if dic[key][2] > s:
            s = dic[key][2]
            key_ = key
    return key_


def predictor(dic: dict, sample: str):
    predicted = key_max(dic)
    for inx in range(3, len(sample)):
        key = sample[inx - 3:inx]
        predicted += '0' if dic[key][0] >= dic[key][1] else '1'
    n_p = len(test_sample) - 3
    n_c = 0
    for bit in range(3, len(sample)):
        if predicted[bit] == sample[bit]:
            n_c += 1
    p_acc = round(n_c / n_p * 100, 2)
    data_analyser(sample, dic)
    return predicted, n_p, n_c, p_acc


data = get_sample(100)
print(f'Final data string:\n{data}')
data_analyser(data, data_analysed)
print('\nYou have $1000. Every time the system successfully predicts your next press, you lose $1.'
      '\nOtherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')
capital = 1000
while True:
    input_raw = input('\nPrint a random string containing 0 or 1:\n')
    if input_raw.lower() == 'enough':
        break
    test_sample = analysis(input_raw)
    if len(test_sample) > 3:
        predicted_sample, m, n, acc = predictor(data_analysed, test_sample)
        print('prediction:', predicted_sample, sep='\n')
        print(f'\nComputer guessed right {n} out of {m} symbols ({acc} %)')
        capital = capital - 2 * n + m
        print(f'Your capital is now ${capital}')
    if capital < 1:
        break
print('Game Over')
