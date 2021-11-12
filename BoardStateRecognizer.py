# format :
"""
board_pair:flush_draw:straight_draw
"""
class BoardStateRecognizer(object):

    @staticmethod
    def hash_board(com_hand):
        ret_hash = "";
        com_hand = com_hand;
        if not com_hand:
            return;
        else:
            ret_hash = str(BoardStateRecognizer.find_board_pair(com_hand))+":"+\
                       str(BoardStateRecognizer.find_straight_draws(com_hand))+":"+\
                       str(BoardStateRecognizer.find_flush_draws(com_hand));

        # call all functions and make formatted string
        # check if it is in dic
        # if not in dic : find most similar existing case for default vals

        return ret_hash;

    @staticmethod
    def find_board_pair(com_hand):
        temp = com_hand[0].val;
        for card in com_hand[1:]:
            if temp == card.val:
                return temp;
        return 0;

    @staticmethod
    def find_flush_draws(com_hand): #returns the number of flush draws
        temp_arr = [0, 0, 0, 0];
        for card in com_hand:
            temp_suit = card.suit;
            if      temp_suit == "Clubs":       temp_arr[0] += 1;
            elif    temp_suit == "Diamonds":    temp_arr[1] += 1;
            elif    temp_suit == "Hearts":      temp_arr[2] += 1;
            else:                               temp_arr[3] += 1;
        ret = 0;

        for num in temp_arr:
            if num > 1:
                ret += 1;
        return ret;

    @staticmethod
    def find_straight_draws(com_hand):
        ret = 0;
        val_arr = [];
        for card in com_hand:
            val_arr.append(card.val);

        for i in range(1,11):
            count = 0;
            for j in range(i,i+5):
                if j in val_arr:
                    count += 1;
            if count >= 3:
                ret += 1;
        return ret;



def test():

    import BotHoldem;
    import Deck;
    deck = Deck.Deck();
    #bot = BotHoldem.BotHoldem(1, 200);

    for i in range(20):
        deck.shuffle();
        temp_hand = [deck.deal_one(), deck.deal_one(), deck.deal_one()];
        for card in temp_hand:
            print(card,end=" ");
        print();
        print(BoardStateRecognizer.hash_board(temp_hand));
        print();
    # board_pair:flush_draw:straight_draw
test();


