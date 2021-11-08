
import Player;
import CardGame;
import WeightStorage as ws;
import random;

class BotHoldem(Player.Player):
    id_num = None;
    dic = None;
    def __init__(self, id_num, stack):
        super().__init__("Bot"+id_num, stack)
        self.id_num = id_num;
        self.dic = ws.WeightStorage.retrieve(id_num);

    def getAction(self, state):
        # state is a hash of the current board/hand state
        # this will return 0:call -1:fold num>0:raise

        if state in self.dic:
            temp = self.dic[state];
            rand = random.random(600);
            if rand < temp[0]: return -1; # fold
            elif rand < temp[1]: return 0; # call
            else: return 10; # raise to ??


