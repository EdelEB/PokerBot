
class Player:
    def __init__(self, name, stack):
        self.name = name;
        self.hand = [];
        self.stack = stack;
        self.money_out = 0;
        self.status = False; # True : in hand, False : sitting out

    def bet(self):
        self.stack -= self.money_out;
        self.money_out = 0;

    def discard_hand(self):
        self.hand = [];

    def display_hand(self):
        print("Hand: ", end='');
        for card in self.hand:
            print(card,' ', end='');
        print();
