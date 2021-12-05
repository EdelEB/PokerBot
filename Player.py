import logging
#logging.basicConfig(level=logging.DEBUG)

class Player:
    def __init__(self, name, stack):
        self.name = name;
        self.hand = [];
        self.stack = stack;
        self.money_out = 0;
        self.status = False; # True : in hand, False : sitting out

    def bet(self, num):
        if num > self.stack: # cannot bet more than stack
            num = self.stack;
        self.stack -= num;
        self.money_out += num;
        return num;

    def call(self, num):
        self.bet(num);

    def confirm_bet(self, game):
        game.pot += self.money_out;
        self.money_out = 0;

    def discard_hand(self):
        self.hand = [];

    def print_hand(self):
        print("|| Hand: ", end='');
        for card in self.hand:
            print(card,' ', end='');
        print(" ||");

    def fold(self):
        self.status = False;

    def request_move(self, game, curr_bet):
        print();
        game.print_runout();
        self.print_hand();
        print(f"|| Pot:{game.pot} || Bet:{curr_bet} || Comitted:{self.money_out} ||\n|| Player {self.name}'s Stack:{self.stack} ||");
        bet = input(f"|| c=call/check || f=fold || raise:  ");  # gets bet input

        if bet == 'f':
            self.fold();
        elif bet == 'c':
            self.call(curr_bet);
        elif bet == 'end':
            game.end_game();
        else:
            try:
                bet = int(bet);
            except:
                raise Exception("Error Invalid Input: ", bet);

            if bet > self.stack:  # cannot bet more than stack
                bet = self.stack;

            self.bet(curr_bet + bet - self.money_out );

        return bet


    def unfold(self):
        self.status = True;