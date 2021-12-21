import pandas as pd
import io
import argparse

outputs = io.StringIO()


class Cards:
    columns = ['definition', 'wrong']

    def __init__(self):
        self.number = 1
        self.data = pd.DataFrame(columns=Cards.columns)

    def card_add(self):
        term = input2(f'The term for card #{self.number}:')
        while term in self.data.index:
            term = input2(f'The term "{term}" already exists. Try again:')
        definition = input2(f'The definition for card #{self.number}:')
        while any(self.data['definition'] == definition):
            definition = input2(f'The definition "{definition}" already exists. Try again:')
        self.data = self.data.append(pd.DataFrame({'definition': definition, 'wrong': 0}, index=[term]))
        self.number += 1
        print2(f'The pair ("{term}":"{definition}") has been added\n')

    def remove(self):
        term = input2('Which card?')
        if term in self.data.index:
            self.data.drop(term, inplace=True)
            print2('The card has been removed.\n')
            self.number -= 1
        else:
            print2(f'Can\'t remove "{term}": there is no such card.\n')

    def ask(self):
        from random import choices
        number_of_q = input2('How many times to ask?')
        questions = choices(self.data.index, k=int(number_of_q))
        for term in questions:
            definition = self.data.loc[term].definition
            answer = input2(f'Print the definition of "{term}":')
            if answer == definition:
                print2('Correct!\n')
            else:
                self.data.loc[term].wrong += 1
                if any(self.data.definition == answer):
                    new_term = self.data[self.data.definition == answer].index[0]
                    print2(
                            f'Wrong. The right answer is "{definition}", but your definition is correct for "'
                            f'{new_term}".\n')
                else:
                    print2(f'Wrong. The right answer is "{definition}".\n')

    def card_import(self, name: str = None):
        from pathlib import Path
        if not name:
            name = input2('File name:')
        link = Path(name)
        try:
            self.data = pd.read_csv(link, header=None, index_col=0, names=Cards.columns)
            print2(f'{self.data.shape[0]} cards have been loaded.\n')
        except IOError:
            print2('File not found.\n')

    def card_export(self, name: str = None):
        from pathlib import Path
        if not name:
            name = input2('File name:')
        link = Path(name)
        self.data.to_csv(link, header=False)
        print2(f'{self.data.shape[0]} cards have been saved.')

    def hardest(self):
        max_err = self.data.wrong.max()
        max_list = self.data[self.data.wrong == max_err].index
        if len(max_list) == 0 or max_err == 0:
            print2('There are no cards with errors.\n')
        elif len(max_list) == 1:
            print2(f'The hardest card is "{max_list[0]}". You have {max_err} errors answering it\n')
        else:
            str_list = '", "'.join(max_list)
            print2(f'The hardest card are "{str_list}". You have {max_err} errors answering them\n')

    def reset(self):
        for i in self.data.index:
            self.data.loc[i, 'wrong'] = 0
        print2('Card statistics have been reset.')


def print2(txt):
    for screen in [None, outputs]:
        print(txt, file=screen)


def input2(txt=""):
    print2(txt)
    param = input()
    outputs.write(param)
    return param


def save_log():
    from pathlib import Path
    name = input2('File name:')
    link = Path(name)
    with open(link, 'w') as f:
        f.write(outputs.getvalue())
    print2('The log has been saved.')


def com_line(obj: Cards):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--import_from', help='import file')
    parser.add_argument('--export_to', help='export file')
    args = parser.parse_args()
    import_from = args.import_from
    export_to = args.export_to
    if import_from:
        obj.card_import(import_from)
    menu()
    if export_to:
        obj.card_export(export_to)
    print2('Bye bye!')
    outputs.close()


def menu():
    commands = {'add'         : card_box.card_add, 'remove': card_box.remove, 'import': card_box.card_import,
                'export'      : card_box.card_export, 'ask': card_box.ask, 'log': save_log,
                'hardest card': card_box.hardest, 'reset stats': card_box.reset}
    while True:
        command = input2('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        if command == 'exit':
            break
        elif command in commands:
            commands[command]()


if __name__ == '__main__':
    card_box = Cards()
    com_line(card_box)
