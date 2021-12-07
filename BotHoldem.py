
from Player import Player;
from HoldemRecognizer import BoardDraws;
from HoldemRecognizer import HandRanker;
from HoldemRecognizer import HandDraws;
from random import randint;
import os;

class BotHoldem(Player):
    def __init__(self, id_num, stack):
        super().__init__(f"Bot {id_num}", stack);
        self.is_bot = True;
        self.wfile = f"bot{id_num}_weights.txt"; # personal bot weights
        #self.wfile = "uni_weights.txt"; # universal weights accumulated by all bots
        self.id_num = id_num;
        self.dic = {};
        self.retrieveWeights(id_num);

        # used to store states that are waiting for results
        self.pending = []; # [key,move] elements

    def __del__(self):
        self.storeWeights(self.dic, self.id_num);
        print(self.name, "data stored");

    def adjustWeights(self, winner): # Win/True || Loss/False
        for tup in self.pending:
            key = tup[0];
            move = tup[1];
            if self is winner:
                self.dic[key][0], self.dic[key][1] = int(self.dic[key][0])+2, int(self.dic[key][1])+2 ;
            else:
                if move == 'c' and int(self.dic[key][1]) - int(self.dic[key][0]) > 3:
                    self.dic[key][0], self.dic[key][1] = int(self.dic[key][0])+2, int(self.dic[key][1])-2;

                self.dic[key][0], self.dic[key][1] = int(self.dic[key][0]) + 2, int(self.dic[key][1]) + 2;
        self.pending = [];

    def makeKey(self, game, curr_bet):
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

        return f"{bet} {hand_rank} {hand_draws} {board_draws}";

    def request_move(self, game, curr_bet):
        if not game.com_hand:
            return self.request_move_preflop(game, curr_bet);

        key = self.makeKey(game, curr_bet);
        if key not in self.dic:
            self.dic[key] = [250, 500];

        tup = self.dic[key];
        if curr_bet == 0:
            rand = randint(tup[0], 600);
        else:
            rand = randint(0, 600);

        # There is definitely a better way to do this, but I can't worry about it right now. I know this code is
        # repetitive and disgusting. #FIXME
        if rand < int(tup[0]):
            self.fold(game);
            move = 'f';  # fold
        elif rand < int(tup[1]):
            self.call(curr_bet, game);
            move = 'c';  # call
        else:
            self.bet(game.pot, game);
            move = game.pot;  # raise to ??

        self.pending.append([key, move]);
        return move;


    def request_move_preflop(self, game, curr_bet):
        if self.hand[0].val == self.hand[1].val or\
        self.hand[0].val > 10 and self.hand[0].val > 10:
            pass;
        elif self.hand[0].suit != self.hand[1].suit or\
        self.hand[0].val - self.hand[1].val > 2 or\
        self.hand[0].val < 5 and self.hand[1].val < 5:
            # if self.money_out == curr_bet: # handles big blind option
            #     self.call(curr_bet, game);
            #     return 'c';
            self.fold(game);
            return 'f';

        key = self.makeKey(game, curr_bet);
        rand = randint(0, 600);

        if key not in self.dic:
            self.dic[key] = [100, 400];

        tup = self.dic[key];

        if rand < int(tup[0]):
            self.fold(game);
            move = 'f';  # fold
        elif rand < int(tup[1]):
            self.call(curr_bet, game);
            move = 'c';  # call
        else:
            self.bet(game.pot, game);
            move = game.pot;  # raise to ??

        self.pending.append([key, move]);
        return move;

    def storeWeights(self, dic, id_num):
        with open(self.wfile, 'w') as file:
            for key in dic:
                string = f"{key}--{dic[key][0]},{dic[key][1]}\n";
                file.write(string);
                file.truncate();

    def retrieveWeights(self, id_num):
        dic = {};

        with open(self.wfile, 'r') as file:
            for line in file:
                tup = line.strip().split("--"); # scenario:(fold_threshold,raise_threshold)
                dic[tup[0]] = tup[1].split(',');
        #file.close();
        #os.remove(self.wfile);
        self.dic = dic;

def test():
    bot = BotHoldem(1, 100);

#test();