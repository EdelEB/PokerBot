
from Deck import Deck;
from HoldemRecognizer import HandRanker;
from Player import Player;
from BotHoldem import BotHoldem;

import logging
logging.basicConfig(level=logging.DEBUG)


class Game:
    def __init__(self, people, hand_size, big_blind, limit, bot):
        self.deck = Deck();
        self.STACK_SIZE = big_blind*1000;
        self.player_count = people + bot;
        if self.player_count < 2:
            print("Error 2 player minimum");
            self.end_game();
            return;
        self.players = []; # player data
        for i in range(self.player_count):
            if bot:
                self.players.append(BotHoldem(i, self.STACK_SIZE));
                bot -= 1;
            else:
                self.players.append(Player(i, self.STACK_SIZE));
        self.dealer = self.button = self.players[0];

        self.HAND_SIZE = int(hand_size);
        self.BIG_BLIND = int(big_blind);
        self.LIMIT = limit;
        self.pot = 0;
        self.com_hand = [];

        self.hand_ended = False;

    def __del__(self):
        print("GAME ENDED");

    def betting_preflop(self):

        ########## Initializes blinds ##################################################################################

        cp = self.next_player(self.dealer);             # current player = small blind

        cp.bet(self.BIG_BLIND // 2, self);              # small blind

        cp = self.next_player(cp);                      # current player = big blind

        curr_bet = cp.bet(self.BIG_BLIND, self);        # big blind

        ################################################################################################################

        bb = cp; # save big blind position to end betting

        while True:
            if self.hand_ended: return;
            cp = self.next_player(cp);

            if curr_bet == cp.get_money_out():
                # this gives big blind option to raise if checks around to them
                if cp == bb and curr_bet == self.BIG_BLIND:
                    curr_bet = cp.request_move(self, curr_bet);
                    continue;
                else:
                    self.collect_bets();
                    return;

            curr_bet = cp.request_move(self, curr_bet);

    def betting(self):
        if not self.dealer.in_hand:
            cp = self.next_player(self.dealer);
        else:
            cp = self.dealer;  # current player with action (this will be incremented immediately)
        button = cp;
        curr_bet = 0;

        while True:
            cp = self.next_player(cp);

            if cp == button and curr_bet == 0:
                curr_bet = cp.request_move(self, curr_bet);
                if not curr_bet:
                    self.collect_bets();
                    return;
                continue;

            if cp.money_out == curr_bet and curr_bet > 0:
                self.collect_bets();
                return;

            curr_bet = cp.request_move(self, curr_bet);

            if self.hand_ended: return;             #FIXME IDK if this is necessary

    def clear_com(self):
        self.com_hand = []; # clear community hand

    def collect_bets(self):
        for p in self.players:
            p.clear_money_out();

    def deal_hands(self):
        cp = self.next_player(self.dealer);

        for i in range(self.HAND_SIZE):
            for j in range(self.players_in()):
                c = self.deck.deal_one();
                cp.hand.append(c);
                cp = self.next_player(cp);

    def deal_com(self, num):
        for i in range(num):
            self.com_hand.append(self.deck.deal_one());

    def end_game(self):
        del self;

    def end_hand(self):
        self.collect_bets();
        winner = Player("PLACEHOLDER",0 );
        if self.players_in() == 1:
            for p in self.players:
                if p.in_hand:
                    winner = p;
            print(f"|| Winner ||\nPlayer {winner.name} Won without showdown");
        elif self.players_in():
            winner = self.showdown();
            print(f"|| Winner ||\nPlayer {winner.name} Won with {HandRanker(winner.hand, self.com_hand)}");
        else:   # 0 players in
            print("Error no players in")

        winner.stack += self.pot;

        for p in self.players:
            if p.is_bot:
                p.adjustWeights(winner);
            p.discard_hand();

        print("HAND ENDED");
        self.hand_ended = True;
        self.pot = 0;

    def next_player(self, curr): # return next player in hand (not folded)

        pos = self.players.index(curr);

        for count in range(self.player_count):
            pos += 1;
            if pos >= self.player_count: pos = 0;

            if self.players[pos].in_hand:
                if self.players[pos] is curr:
                    self.end_hand()
                    return curr;
                return self.players[pos]; # this is what I want to hit every time

        logging.debug("No players in hand??");
        self.end_hand();
        return curr;

    def players_in(self):
        count = 0;
        for p in self.players:
            if p.in_hand:
                count += 1;
        return count;

    def print_runout(self):
        if not self.com_hand:
            print("|| Preflop ||");
            return;

        print('|| Runout: ',end='');
        for card in self.com_hand:
            print(card, ' ', end='');
        print(' ||');

    def print_hands(self):
        for p in self.players:
            print(f"Player {p}: ", end='');
            p.print_hand();

    def reset_stacks(self):
        for p in self.players:
            p.stack = self.STACK_SIZE;

    def setup_hand(self):
        self.hand_ended = False;
        self.clear_com();
        self.deck.shuffle();

        for p in self.players:
            if p.stack <= 0:
                p.fold(self);
            else:
                p.unfold();

        self.dealer = self.next_player(self.dealer);
        self.button = self.dealer;

    def showdown(self):
        finals = [];
        for p in self.players:
            if p.in_hand:
                finals.append((p, HandRanker(p.hand, self.com_hand)));

        print("\n|| Showdown ||");

        winner = finals[0];
        for tup in finals:
            print(f"Player {tup[0].name} : {tup[1]}")
            if tup[1] > winner[1]:
                winner = tup;
        return winner[0];