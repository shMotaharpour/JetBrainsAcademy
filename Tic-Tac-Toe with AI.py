from random import choice
from typing import List, Optional, Tuple, Union

memory = {}


def game_drawer(in_tup: Union[tuple, list]):
    print('-' * 9)
    for i in range(3):
        print('|', *in_tup[3 * i: 3 * i + 3], '|')
    print('-' * 9)


possible_modes = ((0, 1, 2,), (3, 4, 5,), (6, 7, 8,),
                  (0, 3, 6,), (1, 4, 7), (2, 5, 8,),
                  (0, 4, 8), (2, 4, 6))


def state_analyser(in_tup: Union[List, Tuple]) -> Optional[str]:
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


def get_coordinate(in_list: list) -> Tuple[int, int]:
    raw_in: List[str] = input('Enter the coordinates:').split()
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


def user_move(in_tup: list, ch: str):
    in_coord = get_coordinate(in_tup)
    in_tup[in_coord[0] * 3 + in_coord[1]] = ch


def play_game(mode_x, mode_o):
    game_raw = list('_' * 9)
    game_drawer(game_raw)
    moves_type = {'user': user_move, 'easy': ai_easy_move, 'medium': ai_medium_move, 'hard': ai_hard_move}
    _player = {'X': moves_type[mode_x], 'O': moves_type[mode_o]}
    state = do_game(_player, game_raw)
    print(state)


def do_game(_player, game_raw):
    game = True
    while game:
        for mod in ['X', 'O']:
            _player[mod](game_raw, mod)
            game_drawer(game_raw)
            state = state_analyser(game_raw)
            if state is not None:
                game = False
                break
    return state


def ai_easy_move(in_list: list, ch: str):
    print('Making move level "easy"')
    ff = [n for n, ch in enumerate(in_list) if ch == '_']
    in_list[choice(ff)] = ch


def ai_medium_move(in_list: list, ch: str):
    print('Making move level "medium"')
    i_o = ai_think_medium(in_list, ch)
    if i_o != -1:
        in_list[i_o] = ch
    else:
        ff = [n for n, ch in enumerate(in_list) if ch == '_']
        in_list[choice(ff)] = ch


def ai_think_medium(in_list: list, ch: str):
    i_ = -1
    ans = -1
    ch_o = {'X': 'O', 'O': 'X'}[ch]
    for mode in possible_modes:
        n_ch = 0
        n_o_ch = 0
        for i in mode:
            n_ch += in_list[i] == ch
            n_o_ch += in_list[i] == ch_o
            if in_list[i] == '_':
                i_ = i
        if n_ch == 2 and i_ != -1:
            ans = i_
            break
        elif n_o_ch == 2 and i_ != -1:
            ans = i_
    return ans


def ai_hard_move(in_list: list, ch: str):
    print('Making move level "hard"')
    in_list.
    commands = memory.get(ch, None)
    if commands is None:
        memory[ch] = {}
        ai_think_hard(in_list, ch, memory[ch])
        commands: dict = memory[ch]
    form = ''.join(in_list)
    state = commands.get(form, -1)
    if state == -1:
        state = ai_think_medium(in_list, ch)
    in_list[state] = ch


def ai_think_hard(in_list: list, ch: str, ch_memory: dict):
    form = ''.join(in_list)
    ff = [n for n, ch in enumerate(in_list) if ch == '_']
    scores = {}
    op_ch = {'X': 'O', 'O': 'X'}[ch]
    for i_ch in ff:
        in_list_c = in_list.copy()
        in_list_c[i_ch] = ch
        first_move = state_analyser(in_list_c)
        if first_move is not None:
            if ch in first_move:
                ch_memory[form] = i_ch
                return 1
            elif first_move == 'Draw':
                return 0
            else:
                raise KeyError
        else:
            ff2 = [n for n, ch in enumerate(in_list_c) if ch == '_']
            for i_op in ff2:
                in_list_c2 = in_list_c.copy()
                in_list_c2[i_op] = op_ch
                second_move = state_analyser(in_list_c2)
                if second_move is not None:
                    if op_ch in second_move:
                        scores[i_ch] = -1
                        break
                    elif second_move == 'Draw':
                        scores[i_ch] = 0
                    else:
                        raise KeyError
                else:
                    scores[i_ch] = min(scores.get(i_ch, 10), ai_think_hard(in_list_c2, ch, ch_memory))
                if scores[i_ch] == -1:
                    break
    if scores:
        ch_memory[form] = max(scores, key=scores.get)
        return max(scores.values())
    raise KeyError


def menu():
    com_set = {'user', 'easy', 'medium', 'hard'}
    while True:
        command = input('Input command: ')
        if command == 'exit':
            break
        command = command.split()
        if len(command) != 3:
            print('Bad parameters!')
        else:
            if command[0] != 'start' or (command[1] not in com_set) or (command[2] not in com_set):
                print('Bad parameters!')
            else:
                play_game(command[1], command[2])


if __name__ == '__main__':
    menu()
    # cht = 'O'
    # in_listt = list('XXO_O_X__')
    # memory[cht] = {}
    # ai_think_hard(in_listt, cht, memory[cht])
    # ans = memory[cht][''.join(in_listt)]
    # print(ans)
