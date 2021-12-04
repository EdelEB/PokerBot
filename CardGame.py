
from Player import Player;
from Deck import Deck;

class Game:
    def __init__(self, player_count, hand_size, big_blind, limit):
        if player_count < 2: print("Error 2 players needed"); return;
        self.deck = Deck();

        self.player_count = player_count
        self.players = {}; # player data
        for i in range(1, int(player_count)+1):
            self.players[i] = Player(i, big_blind * 100);
        self.dealer = self.button = 1;

        self.hand_size = int(hand_size);
        self.big_blind = int(big_blind);
        self.limit = limit;
        self.pot = 0;
        self.com_hand = [];

        self.hand_ended = False;

    def setup_hand(self):
        self.deck.shuffle();

        for pos in self.players:
            if self.players[pos].stack == 0:
                self.players[pos].fold();
            else:
                self.players[pos].unfold();

        self.dealer = self.next_player(self.dealer);
        self.button = self.dealer;

    def betting_preflop(self):

        ########## Initializes small and big blinds ####################################################################

        cp = self.next_player(self.dealer);             # current player = small blind

        self.players[cp].bet(self.big_blind // 2);      # small blind

        cp = self.next_player(cp);                      # current player = big blind

        self.players[cp].bet(self.big_blind);           # big blind

        curr_bet = self.big_blind;

        ################################################################################################################

        bb = cp; # save big blind position to end betting
        while True:
            cp = self.next_player(cp);

            # ends loop but makes sure big blind has option to raise
            if curr_bet == self.players[cp].money_out and not (curr_bet == self.big_blind and cp == bb):
                for p in self.players:
                    self.players[p].confirm_bet(self);            # adjust pot, stack size, and money_out
                break;

            curr_bet = self.get_move(cp, curr_bet);

    def betting(self):
        cp = self.button;  # current player with action
        curr_bet = 0;

        while True:
            cp = self.next_player(cp);

            if self.players[cp].money_out == curr_bet and curr_bet > 0:
                for p in self.players:
                    self.players[p].confirm_bet(self);          # adjust pot, stack size, and money_out
                break;

            curr_bet = self.get_move(cp, curr_bet);

            if curr_bet == 0 and cp == self.button:         # checked through
                break;

    def get_move(self, cp, curr_bet):

        bet = self.players[cp].request_move(self, curr_bet);

        if bet == 'f':  # fold
            if self.players_in() == 1:
                self.end_hand();
            elif cp == self.button:
                self.shift_button();

        elif bet == 'c':  # call
            pass
        else:  # raise
            return curr_bet + int(bet);

        return curr_bet;

    def deal_hands(self):
        cp = self.next_player(self.dealer);

        for i in range(self.hand_size):
            for j in range(self.players_in()):
                c = self.deck.deal_one();
                self.players[cp].hand.append(c);
                cp = self.next_player(cp);

    def clear_com(self):
        self.com_hand = []; # clear community hand

    def deal_com(self, num):
        for i in range(num):
            self.com_hand.append(self.deck.deal_one());

    def display_runout(self):
        if len(self.com_hand) == 0:
            print("|| Preflop ||");
            return;

        print('|| Runout: ',end='');
        for card in self.com_hand:
            print(card, ' ', end='');
        print(' ||');

    def display_hands(self):
        for p in self.players:
            print(f"Player {self.players[p]}: ", end='');
            self.players[p].display_hand();

    def end_hand(self):
        self.clear_com();
        self.hand_ended = True;
        print("HAND ENDED")             #FIXME
        pass;

    def next_player(self, pos): # return next player in hand (not folded)
        while True:
            pos = self.next_pos(pos);
            if self.players[pos].status:
                return pos;

    def next_pos(self, pos): # returns next position in players array
        pos += 1;
        if pos > len(self.players):
            return 1;
        return pos;

    def players_in(self):
        count = 0;
        for pos in self.players:
            if self.players[pos].status:
                count += 1;
        return count;

    def shift_button(self):
        while not self.players[self.button].status:
            self.button -= 1;
            if self.button < 1:
                self.button = len(self.players);

    def showdown(self):
        pass;