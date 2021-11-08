
class Card:
    def __init__(self, suit, val):
        self.suit = suit;
        self.val = val;
        self.img = None;

    def trans_val(self, val): # translate value
        if 1 < val < 11: return val;
        switch = { 11 : 'J', 12 : 'Q', 13 : 'K', 14 : 'A'}
        if val in switch: return switch[val];
        else: return None;

    def flip(self):
        pass;

    def __str__(self):
        return str(self.trans_val(self.val)) + self.suit[0].lower();
