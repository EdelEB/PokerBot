
import CardGame;

class Holdem(CardGame.Game):
    def __init__(self, player_count, big_blind):
        super().__init__(player_count, 2, big_blind, None); # no limit

    def play_hand(self):
        self.setup_hand();
        self.deal_hands();

        self.betting_preflop();     # pre flop betting

        self.deal_com(3);           # flop

        self.betting();             # flop betting

        self.deal_com(1);           # turn

        self.betting();             # turn betting

        self.deal_com(1);           # river

        self.betting();             # river betting

        self.showdown();

def test():
    mygame = Holdem(5,2);

    mygame.play_hand();

test();
