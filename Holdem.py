
import CardGame;

class Holdem(CardGame.Game):
    def __init__(self, people, big_blind, bots):
        super().__init__(people, 2, big_blind, None, bots); # no limit

    def play_hand(self):
        self.setup_hand();

        self.deal_hands();          # deals players' hole cards
        print("######################################################################################################");
        self.print_runout();
        print("######################################################################################################");
        self.betting_preflop();     # pre flop betting
        if self.hand_ended: return;

        self.deal_com(3);           # flop
        print("######################################################################################################");
        self.print_runout();
        print("######################################################################################################");
        self.betting();             # flop betting
        if self.hand_ended: return;

        self.deal_com(1);           # turn
        print("######################################################################################################");
        self.print_runout();
        print("######################################################################################################");
        self.betting();             # turn betting
        if self.hand_ended: return;

        self.deal_com(1);           # river
        print("######################################################################################################");
        self.print_runout();
        print("######################################################################################################");
        self.betting();             # river betting

        self.end_hand();

def test():
    mygame = Holdem(0 ,2, 3); # (people, big blind, bots)

    for i in range(1000):
        print(f"################################################################################### {i} >>>>>>>>>>>>>");
        mygame.reset_stacks();
        mygame.play_hand();

test();
