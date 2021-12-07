import logging
#logging.basicConfig(level=logging.DEBUG)

class Player:
    def __init__(self, name, stack):
        self.is_bot = False;
        self.name = name;
        self.hand = [];
        self.stack = stack;
        self.money_out = 0;
        self.in_hand = False;

    def bet(self, num, game):
        if num > self.stack: # cannot bet more than stack
            num = self.stack;
        self.stack -= num;
        self.money_out += num;
        game.pot += num;
        return self.money_out;

    def call(self, num, game):
        num -= self.money_out;
        self.bet(num, game);

    def clear_money_out(self):
        self.money_out = 0;

    def discard_hand(self):
        self.hand = [];

    def fold(self):
        self.in_hand = False;

    def get_money_out(self):
        return self.money_out;

    def print_hand(self):
        print("|| Hand: ", end='');
        for card in self.hand:
            print(card,' ', end='');
        print(" ||");

    def request_move(self, game, curr_bet):
        print();
        game.print_runout();
        self.print_hand();
        print(f"|| Pot:{game.pot} || Bet:{curr_bet} || Comitted:{self.money_out} ||\n|| Player {self.name}'s Stack:{self.stack} ||");
        bet = input(f"|| c=call/check || f=fold || raise:  ");  # gets bet input

        if bet == 'f':
            self.fold();
            print(f"Player {self.name} folded to {curr_bet} raise");
        elif bet == 'c':
            self.call(curr_bet, game);
            print(f"Player {self.name} checked/called {curr_bet} raise");
        elif bet == 'end':
            print(f"Player {self.name} Requested to End Game");
            game.end_game();
        else:
            try:
                bet = int(bet);
            except:
                raise Exception("Error Invalid Input: ", bet);

            self.bet(bet, game);    #FIXME I think something is wrong with what happens when the stack is too small
            return self.money_out;

        return curr_bet;

    def unfold(self):
        self.in_hand = True;