class CoffeeMachine:
    def __init__(self):
        self.coffee_machine_source = {'water': 400,
                                      'milk': 540,
                                      'coffee beans': 120,
                                      'disposable cups': 9,
                                      'money': 550}
        self.menu1 = {'buy': self.buy_set, 'fill': self.fill_set, 'take': self.take_set, 'remaining': self.source_print}

    resp = {'1': {'water': 250, 'milk': 00, 'coffee beans': 16, 'money': -4},  # espresso
            '2': {'water': 350, 'milk': 75, 'coffee beans': 20, 'money': -7},  # latte
            '3': {'water': 200, 'milk': 100, 'coffee beans': 12, 'money': -6}}  # cappuccino

    def take_input(self, mode):
        if mode == 'on':
            while True:
                ordered = input('Write action (buy, fill, take, remaining):\n').lower()
                if ordered in self.menu1:
                    self.menu1[ordered]()
                elif ordered == 'exit':
                    break
        elif mode == 'inp_source':
            return (int(input('Write how many ml of water you want to add:\n')),
                    int(input('Write how many ml of milk you want to add:\n')),
                    int(input('Write how many grams of coffee beans you want to add:\n')),
                    int(input('Write how many disposable coffee cups you want to add:\n')))
        elif mode == 'buy':
            return input(
                '\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\nelse back to previous menu\n')

    def buy_set(self):
        w2b = self.take_input('buy')
        if w2b in self.resp:
            if all([self.coffee_machine_source[key] >= self.resp[w2b][key] for key in self.resp[w2b]]) and \
                    self.coffee_machine_source['disposable cups']:
                for key in self.resp[w2b]:
                    self.coffee_machine_source[key] -= self.resp[w2b][key]
                self.coffee_machine_source['disposable cups'] -= 1
                print('I have enough resources, making you a coffee!')
            else:
                print('\nSorry, do some else\n')

    def fill_set(self):
        temp = self.take_input('inp_source')
        self.coffee_machine_source['water'] += temp[0]
        self.coffee_machine_source['milk'] += temp[1]
        self.coffee_machine_source['coffee beans'] += temp[2]
        self.coffee_machine_source['disposable cups'] += temp[3]

    def take_set(self):
        print("I gave you $%d" % self.coffee_machine_source['money'])
        self.coffee_machine_source['money'] = 0

    def source_print(self):
        print('\nThe coffee machine has:')
        print(*[str(self.coffee_machine_source[key]) + ' of ' + key for key in self.coffee_machine_source], sep='\n',
              end='\n\n')


amir_machine = CoffeeMachine()
amir_machine.take_input('on')
