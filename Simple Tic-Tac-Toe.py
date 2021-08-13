from typing import Tuple, List


def game_drawer(in_tup: tuple):
    print('-' * 9)
    for i in range(3):
        print('|', *in_tup[3 * i: 3 * i + 3], '|')
    print('-' * 9)


possible_modes = ((0, 1, 2,), (3, 4, 5,), (6, 7, 8,),
                  (0, 3, 6,), (1, 4, 7), (2, 5, 8,),
                  (0, 4, 8), (2, 4, 6))


def state_analyser(in_tup: tuple) -> str:
    """

    :type in_tup: 9 members of input
    """
    if abs(in_tup.count('X') - in_tup.count('O')) > 1:
        return 'Impossible'
    check_mode = []
    for mode in possible_modes:
        check_mode.append(set(map(in_tup.__getitem__, mode)))
    if {'X'} in check_mode and {'O'} not in check_mode:
        return 'X wins'
    if {'O'} in check_mode and {'X'} not in check_mode:
        return 'O wins'
    if {'X'} in check_mode and {'O'} in check_mode:
        return 'Impossible'
    if in_tup.count('X') + in_tup.count('O') == 9:
        return "Draw"
    return None


def get_coordinate(in_list: list) -> tuple[int, int]:
    raw_in: list[str] = input('Enter the coordinates:').split()
    if all(ch.isdigit() for ch in raw_in):
        if raw_in[0] in '123' and raw_in[1] in '123':
            new: tuple = tuple(int(ch) - 1 for ch in raw_in)
            point = new[0] * 3 + new[1]
            if in_list[point] == '_':
                return new
            print('This cell is occupied! Choose another one!')
            return get_coordinate(in_list)

        else:
            print('Coordinates should be from 1 to 3!')
            return get_coordinate(in_list)
    else:
        print('You should enter numbers!')
        return get_coordinate(in_list)


def make_move(in_coord: tuple, in_tup: list, ch: str):
    in_tup[in_coord[0] * 3 + in_coord[1]] = ch


game_raw = list('_' * 9)
game_drawer(game_raw)
while True:
    make_move(get_coordinate(game_raw), game_raw, 'X')
    game_drawer(game_raw)
    state = state_analyser(game_raw)
    if state is not None:
        print(state)
        break
    make_move(get_coordinate(game_raw), game_raw, 'O')
    game_drawer(game_raw)
    state = state_analyser(game_raw)
    if state is not None:
        print(state)
        break
