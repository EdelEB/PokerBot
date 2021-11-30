
from Player import Player;
from CardGame import Game;
from random import randint;
import os;

class BotHoldem(Player):

    def __init__(self, id_num, stack):
        super().__init__(f"Bot {id_num}", stack);
        self.id_num = id_num;
        self.dic = self.retrieveWeights(id_num);
        self.pending = []; # used to store states that are waiting for results

    def adjustWeights(self, outcome): # Win/True || Loss/False
        for key in self.pending:
            if outcome:
                self.dic[key][0], self.dic[key][1] = int(self.dic[key][0])+2, int(self.dic[key][1])+2 ;
            else:
                self.dic[key][0], self.dic[key][1] = int(self.dic[key][0]) + 2, int(self.dic[key][1]) + 2;

    def getAction(self, state):
        # state is a hash of the current board/hand state
        # this will return 0:call -1:fold num>0:raise

        if state in self.dic:
            tup = self.dic[state];
            rand = randint(0,600);
            if rand < int(tup[0]): return -1; # fold
            elif rand < int(tup[1]): return 0; # call
            else: return 10; # raise to ??

    def executeTurn(self):
        pass

    def storeWeights(self, dic, id_num):
        file = open(f"bot{id_num}_weights.txt", 'w');

        for element in dic:
            string = f"{element}--{dic[element]}\n";
            file.write(string);
        file.close();

    def retrieveWeights(self, id_num):
        dic = {};
        file = open(f"bot{id_num}_weights.txt", 'r');
        for line in file:
            tup = line.strip().split("--"); # scenario:(fold_threshold,raise_threshold)
            dic[tup[0]] = tup[1];
        file.close();
        os.remove(f"bot{id_num}_weights.txt");
        return dic;


