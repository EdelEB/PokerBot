
import CardGame;

class Holdem(CardGame.Game):
    def __init__(self, people, big_blind, bot):
        super().__init__(people, 2, big_blind, None, bot); # no limit

    def play_hand(self):
        self.setup_hand();
        self.deal_hands();

        self.print_runout();

        self.betting_preflop();     # pre flop betting
        if self.hand_ended: return;
        self.deal_com(3);           # flop

        self.print_runout();

        self.betting();             # flop betting
        if self.hand_ended: return;
        self.deal_com(1);           # turn

        self.print_runout();

        self.betting();             # turn betting
        if self.hand_ended: return;
        self.deal_com(1);           # river

        self.betting();             # river betting
        if self.hand_ended: return;
        self.end_hand();

def test():
    mygame = Holdem( 0 ,2, 2);

    mygame.play_hand();

test();
