# format :
"""
board_pair:flush_draw:straight_draw
"""
class BoardStateRecognizer(object):

    com_hand = []; # com_hand = array of cards

    def hash_board(self, com_hand):
        ret_hash = "";
        com_hand = self.com_hand;
        if not com_hand:
            return;
        else:
            ret_hash = self.find_board_pair()+":"+self.find_straight_draws()+":"+self.find_flush_draws();

        # call all functions and make formatted string
        # check if it is in dic
        # if not in dic : find most similar existing case for default vals

        return ret_hash;

    def find_board_pair(self):
        temp = self.com_hand[0].val;
        for card in self.com_hand[1:]:
            if temp == self.com_hand.val:
                return temp;
        return 0;

    def find_flush_draws(self): #returns the number of flush draws
        temp_arr = [0, 0, 0, 0];
        for card in self.com_hand:
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

    def find_straight_draws(self):
        ret = 0;
        val_arr = [];
        for card in self.com_hand:
            val_arr.append(card.val);

        for i in range(1,11):
            count = 0;
            for j in range(i,i+5):
                if j in val_arr:
                    count += 1;
            if count >= 3:
                ret += 1;

        return ret;





