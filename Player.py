
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
        num -= self.money_out;
        if num > self.stack:
            self.bet(self.stack);
        else:
            self.bet(num);

    def confirm_bet(self):
        self.money_out = 0;

    def discard_hand(self):
        self.hand = [];

    def display_hand(self):
        print("Hand: ", end='');
        for card in self.hand:
            print(card,' ', end='');
        print();

    def fold(self):
        self.status = False;

    def unfold(self):
        self.status = True;