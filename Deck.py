import random;
import Card;

class Deck:
    def __init__(self):
        self.pile = [];
        self.top = 0;
        for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
            for val in range(2, 15):
                self.pile.append(Card(suit, val));

    def shuffle(self):
        for i in range(1000):
            rand1 = random.randint(0,51);
            rand2 = random.randint(0,51);
            while rand1 == rand2:
                rand2 = random.randint(0,51);
            self.pile[rand1], self.pile[rand2] = self.pile[rand2], self.pile[rand1];
        self.top = 0;

    def discard(self):
        self.top += 1;
        if self.top == 52: print("Reached end of deck. Reshuffling..."); self.shuffle();

    def deal_one(self):
        temp = self.pile[self.top];
        self.top += 1;
        if self.top == 52: print("Reached end of deck. Reshuffling..."); self.shuffle();
        return temp;

    def deal_table(self, positions, hand):
        if positions * hand > 52:
            print("More than 52 cards are needed for that many positions/hand sizes.")
            return [];

        hands_arr = []; #array of (arrays of Cards) ; initializes all hands
        for i in range(positions):
            hands_arr.append([]);

        for i in range(hand): # populates hands with cards
            for j in range(positions):
                hands_arr[j].append(self.deal_one());
        return hands_arr;

    def __str__(self):
        for card in self.pile:
            print(card, end='|');