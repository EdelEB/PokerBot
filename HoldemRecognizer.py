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

    if not hole: return [0];

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
        if two_tup[1] == three[1]:
            return [7, three[1], two_tup[2]];
        #two_tup.pop(two_tup.index(three[1]));
        else:
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
            ret = [2, x]
            if temp:
                for i in range(len(temp)):
                    ret.append(temp[i]);
            return ret;
    return False;

########################################################################################################################

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

def BoardDraws(com_hand):
    ret = "";
    if com_hand:
        ret = f"{board_draw_straight(com_hand)}:{board_draw_flush(com_hand)}:{board_draw_pair(com_hand)}";
    return ret;

def board_draw_pair(com_hand):
    temp = [card.val for card in com_hand];
    for val in temp:
        if subset([val, val], temp):
            return True;
    return False;

def board_draw_flush(com_hand):
    dic = {
        'C' : 0,
        'D' : 0,
        'H' : 0,
        'S' : 0
    };
    for card in com_hand:
        dic[card.suit] += 1;

    if ret := [key for key in dic if dic[key] > 1]:
        return ret;

    return False;

def board_draw_straight(com_hand):
    vals = [card.val for card in com_hand];
    draws = 0;

    for i in range(14, 4, -1):
        sub = [i,i-1,i-2,i-3,i-4];
        count = 0;
        for val in vals:
            if val in sub:
                count+=1;
        if count > 2:
            draws+=1;
    return draws;

def HandDraws(hole, com_hand):
    ret = "";
    if hole:
        ret = f"{hand_draw_straight(hole, com_hand)}:{hand_draw_flush(hole, com_hand)}:{hand_draw_overs(hole, com_hand)}";
    return ret;

def hand_draw_overs(hole, com_hand):
    holes = [card.val for card in hole];
    coms = [card.val for card in com_hand];
    count = 0;

    for h in holes:
        for c in coms:
            if h < c:
                count -= 1;
                break
        count += 1;
    return count;

def hand_draw_flush(hole, com_hand):
    dic = {
        'C' : 0,
        'D' : 0,
        'H' : 0,
        'S' : 0
    };
    for card in hole+com_hand:
        dic[card.suit] += 1;

    if ret := [key for key in dic if dic[key] > 3]:
        return ret;

    return False;

def hand_draw_straight(hole, com_hand):
    vals = [card.val for card in hole+com_hand];
    draws = 0;

    for i in range(14, 4, -1):
        sub = [i,i-1,i-2,i-3,i-4];
        count = 0;
        for val in vals:
            if val in sub:
                count+=1;
        if count > 3:
            draws+=1;
    return draws;


def test():

    from BotHoldem import BotHoldem as BotH;
    from Deck import Deck;
    d = Deck();
    #bot = BotH(1, 200);

    for i in range(20):
        d.shuffle();
        com = [d.deal_one(), d.deal_one(), d.deal_one(), d.deal_one(), d.deal_one()];
        hole = [d.deal_one(), d.deal_one()]
        # for card in (hole+com):
        #     print(card, end=" ");
        #print();
        #print(HandRecognizer(hole, com));
        com2 = [d.deal_one(), d.deal_one(), d.deal_one()];
        for card in com2: print(card, end=" ");
        print();
        print("straights: ",board_draw_straight(com2));
        print(board_draw_flush(com2));
        print(board_draw_pair(com2));
        print();

    # sub = [1, 5];
    # arr = [1, 3, 2, 2, 3, 5, 6];
    # print(arr)
    # print(check_four(arr));
    # print(check_straight(arr))
    # print(check_two_pair(arr))
    # print(arr);
    # board_pair:flush_draw:straight_draw
#test();


