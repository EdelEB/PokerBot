import logging

from Card import Card
"""
format : 
    hand array format : 
        straight flush: 9 , top
        4 of a kind:    8 , 4card.val
        full house:     7 , 3card.val , 2card.val
        flush:          6 , top
        straight:       5 , top
        three of kind:  4 , 3card , high_card.val descending
        two pair:       3 , high_pair.val , low_pair.val, high_card.val
        pair:           2 , pair.val , 
        high:           1 , card.val's descending
"""

def HandRecognizer(hole, board): # Card[] hole cards, Card[] community cards

    if not hole: return;

    all_cards = hole + board;
    all_cards.sort(key=lambda temp: temp.val, reverse=True);

    vals = [];              # helps check for straights
    for card in all_cards:
        if card.val == 14:  # for A's
            vals.append(1);
            vals.append(14);
        else:
            vals.append(card.val);

    vals = sorted(vals,key=None,reverse=True); # descending order

    if  x := check_sf(all_cards, vals):
        return x;
    elif x := check_four(vals):
        return x;
    elif x := check_full(vals):
        return x;
    elif x := check_flush(all_cards):
        return x;
    elif x := check_straight(vals):
        return x;
    elif x := check_three(vals):
        return x;
    elif x := check_two_pair(vals):
        return x;
    elif check_pair(vals):
        return check_pair(vals);
    else:
        vals = vals[0:len(vals)-3];
        vals.insert(0,1);
        return vals;

# checks for straight flush
def check_sf(cards, vals):
    if (suit := flush_suit(cards)) and (svals := check_straight(vals)):
        count = 0;
        for card in cards:
            if card.val in svals and card.suit == suit:
                count+=1;
        return [9, svals[0]];
    return False;


# check for four of a kind
# returns [hand rank, val of card that there are four of] || False
def check_four(vals):
    for x in vals:
        if subset([x,x,x,x], vals):
            return [8, x];
    return False;

# checks for full house
# returns [hand rank, three card val, pair card val] || False
def check_full(vals):
    three = check_three(vals)
    two_tup = check_two_pair(vals)
    if three and two_tup:
        two_tup.pop(two_tup.index(three[1]));
        return [7, three[1], two_tup[1]];
    return False;

# if flush returns suit
def flush_suit(cards):
    dic = {
        'C' : 0,
        'D' : 0,
        'H' : 0,
        'S' : 0
    };
    for card in cards:
        dic[card.suit] += 1;

    for k in dic:
        if dic[k] > 4:
            return k;

    return False;

def check_flush(cards): # returns flush suit
    if suit := flush_suit(cards):
        ret = [6];
        for card in cards:
            if card.suit == suit and len(ret) < 6:
                ret.append(card.val);
        return ret;
    return False;

def check_straight(vals):
    for i in range(14, 4, -1):
        sub = [i,i-1,i-2,i-3,i-4];
        if subset(sub, vals):
            sub.insert(0,5);
            return sub;

# check if three of a kind
def check_three(vals):
    for x in vals:
        if subset([x,x,x], vals):
            temp = [y for y in vals if y != x];
            return [4, x, temp[0], temp[1]];
    return False;

def check_two_pair(vals):
    temp = [num for num in vals if num != 1]; # removes Ace 1's (14's are already in list)

    pairs = [];
    ret = [];

    for x in temp:
        if len(ret)>1:
            break;
        if x not in pairs and subset([x,x], temp):
            ret.append(x);
            pairs.append(x);

    if len(ret) > 1:
        ret.insert(0,3);
        ret.append(temp[0]);
        return ret;
    return False;

def check_pair(vals):
    temp = vals.copy();
    for x in temp:
        if subset([x,x], temp):
            temp = [y for y in temp if y != x];
            # temp.pop(temp.index(x));
            # temp.pop(temp.index(x));
            return [2, x, temp[0], temp[1], temp[2]];
    return False;

def subset(sub, full):
    temp = full.copy();
    for x in sub:
        if x in temp:
            temp.pop(temp.index(x));
        else:
            return False;
    return True;

# format :
"""
board_pair:flush_draw:straight_draw
"""
class DrawRecognizer(object):

    @staticmethod
    def hash_board(com_hand):
        ret_hash = "";
        com_hand = com_hand;
        if not com_hand:
            return;
        else:
            ret_hash = str(DrawRecognizer.find_board_pair(com_hand))+":"+\
                       str(DrawRecognizer.find_straight_draws(com_hand))+":"+\
                       str(DrawRecognizer.find_flush_draws(com_hand));

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

    from BotHoldem import BotHoldem as BotH;
    from Deck import Deck;
    d = Deck();
    #bot = BotH(1, 200);

    for i in range(20):
        d.shuffle();
        com = [d.deal_one(), d.deal_one(), d.deal_one(), d.deal_one(), d.deal_one()];
        hole = [d.deal_one(), d.deal_one()]
        for card in (hole+com):
            print(card, end=" ");
        print();
        print(HandRecognizer(hole, com));
        print();

    # sub = [1, 5];
    # arr = [1, 3, 2, 2, 3, 5, 6];
    # print(arr)
    # print(check_four(arr));
    # print(check_straight(arr))
    # print(check_two_pair(arr))
    # print(arr);
    # board_pair:flush_draw:straight_draw
test();


