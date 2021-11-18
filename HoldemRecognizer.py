
from Card import Card

def HandRecognizer(hole, board): # Card[] hole cards, Card[] community cards
    all_cards = hole + board;

    c,d,h,s = 0,0,0,0;      # helps check for flushes
    vals = [];              # helps check for straights
    for card in all_cards:

        match card.suit:
            case 'C':
                c += 1;
            case 'D':
                d += 1;
            case 'H':
                h += 1;
            case 'S':
                s += 1;

        if card.val == 14:  # for A's
            vals.append(1);
            vals.append(14);
        else:
            vals.append(card.val);

    vals = sorted(vals,key=None,reverse=True); # descending order
    check_sf(vals);
    check_four(vals);
    check_full(vals);
    check_flush([c, d, h, s]);
    check_straight(vals);
    check_three(vals);
    check_two_pair(vals);
    check_pair(vals);
    high = vals[0];

def check_sf(arr):
    pass;

def check_four(arr):
    for x in arr:
        if [x,x,x,x] in arr:
            return x;
    return False;

def check_full(arr):
    three = check_three(arr)
    two_tup = check_two_pair(arr)
    if three and two_tup:
        two_tup.pop(three);
        return [three, two_tup[0]];
    return False;

def check_three(arr):
    for x in arr:
        if [x,x,x] in arr:
            return x;
    return False;

def check_two_pair(arr):
    while 1 in arr: # removes extra Ace vals, 14 is in arr already
        arr.pop(1);

    ret = [];
    for x in arr:
        if len(ret)==2:
            break;
        if [x,x] in arr:
            ret.append(x)
            while x in arr:
                arr.pop(x);

    if not ret:
        return False;
    return ret;

def check_pair(arr):
    for x in arr:
        if [x,x] in arr:
            return x;
    return False;

def check_flush(arr):
    for x in arr:
        if x > 4:
            return True;
    return False;

def check_straight(arr):
    for i in range(1,10):
        if [i,i+1,i+2,i+3,i+4] in arr:
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
        print(DrawRecognizer.hash_board(temp_hand));
        print();
    # board_pair:flush_draw:straight_draw
test();


