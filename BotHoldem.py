
from Player import Player;
from CardGame import Game;
#import WeightStorage as ws;
from WeightStorage import *;
from random import randint;

class BotHoldem():

    def __init__(self, id_num, stack):
        super().__init__("Bot"+str(id_num), stack)
        self.id_num = id_num;
        self.dic = WeightStorage.retrieve(id_num);

    def getAction(self, state):
        # state is a hash of the current board/hand state
        # this will return 0:call -1:fold num>0:raise

        if state in self.dic:
            temp = self.dic[state];
            rand = randint(0,600);
            if rand < temp[0]: return -1; # fold
            elif rand < temp[1]: return 0; # call
            else: return 10; # raise to ??


