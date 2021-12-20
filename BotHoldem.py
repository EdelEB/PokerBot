
from Player import Player;
from HoldemRecognizer import BoardDraws;
from HoldemRecognizer import HandRanker;
from HoldemRecognizer import HandDraws;
from random import randint;
import os;

class BotHoldem(Player):
    def __init__(self, id_num, stack, brain):
        super().__init__(f"Bot {id_num}", stack);
        self.is_bot = True;
        self.brain = brain; # BotBrain object
        self.id_num = id_num;

        # used to store states that are waiting for results
        self.pending = []; # [key,move] elements

        self.__always_call = False; # used for training

    def adjust_brain(self, winner): # Win/True || Loss/False
        won = False;
        if self == winner: won = True;
        self.brain.adjust_weights(won, self.pending);


    # key format:
    # <action> <hand rank> <# straight draws>:<# flush draws>:<# overs> <# straight draws>:<# flush draws>:<board paired?>
    def make_key(self, game, curr_bet):
        hand_rank = HandRanker(self.hand, game.com_hand);
        hand_draws = HandDraws(self.hand, game.com_hand);
        board_draws = BoardDraws(game.com_hand);

        if not curr_bet:
            bet = "0";
        elif game.pot // 2 > curr_bet:
            bet = "<";
        elif game.pot > curr_bet:
            bet = "|";
        else:
            bet = ">";

        return f"{bet} {hand_rank[0]} {hand_draws} {board_draws}";

    def request_move(self, game, curr_bet):
        key = self.make_key(game, curr_bet);
        if not game.com_hand:
            move = self.request_move_preflop(game, curr_bet);
        else:
            if key not in self.brain.dic:
                self.brain.dic[key] = [250, 500];
            tup = self.brain.dic[key];

            # ensures bot does not fold to no bet
            if curr_bet == self.money_out or curr_bet == 0:
                if int(tup[0]) > 599:
                    rand = 599;
                else:
                    rand = randint(int(tup[0]), 600);
            else:
                rand = randint(0, 600);

            if self.__always_call:
                print(f"{self.name} checked/called {curr_bet} raise");
                move = 'c';
                self.call(curr_bet, game);
            elif rand < int(tup[0]):      #fold
                print(f"{self.name} folded to {curr_bet} raise");
                move = 'f';
                self.fold(game);
            elif rand < int(tup[1]):    #call
                print(f"{self.name} checked/called {curr_bet} raise");
                move = 'c';
                self.call(curr_bet, game);
            else:
                move = 'r';
            self.pending.append([key, move]);

        if move == 'r':
            self.bet(game.pot, game);
            return self.money_out;
        return curr_bet;

    def request_move_preflop(self, game, curr_bet):
        if self.hand[0].val == self.hand[1].val or\
        self.hand[0].val > 10 and self.hand[0].val > 10:
            pass;
        elif self.hand[0].suit != self.hand[1].suit or\
        self.hand[0].val - self.hand[1].val > 2 or\
        self.hand[0].val < 5 and self.hand[1].val < 5:
            # if self.money_out == curr_bet: # handles big blind option
            #     print(f"Bot {self.name} checked its option");
            #     self.call(curr_bet, game);
            #     return 'c';
            print(f"{self.name} folded to {curr_bet} preflop");
            self.fold(game);
            return 'f';

        key = self.make_key(game, curr_bet);
        rand = randint(0, 600);

        if key not in self.brain.dic:
            self.brain.dic[key] = [100, 400];

        tup = self.brain.dic[key];

        if rand < int(tup[0]):
            print(f"{self.name} folded to {curr_bet} preflop");
            self.fold(game);
            move = 'f';  # fold
        elif rand < int(tup[1]):
            print(f"{self.name} checked/called {curr_bet} raise");
            self.call(curr_bet, game);
            move = 'c';  # call
        else:
            move = 'r'; # raise

        self.pending.append([key, move]);
        return move;

def test():
    bot = BotHoldem(1, 100);

#test();