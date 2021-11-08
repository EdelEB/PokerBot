
import Player;
import Deck;
import sll;

class Game:
    def __init__(self, player_count, hand_size, big_blind, limit):
        if player_count < 2: print("Error 2 players needed"); return;
        self.deck = Deck();

        self.positions = sll.SLL();
        self.players = {}; # player data
        for i in range(int(player_count)):
            self.positions.add(i);
            self.players[i] = Player(i, big_blind * 100);
        self.positions.tie();
        self.dealer = self.positions.head;

        self.hand_size = int(hand_size);
        self.big_blind = int(big_blind);
        self.limit = limit;
        self.pot = 0;
        self.com_hand = [];

    def setup_hand(self):
        self.dealer = self.dealer.next;
        self.deck.shuffle();
        for player in self.players:
            if self.players[player].stack == 0: self.players[player].status  = False;
            else: self.players[player].status = True;

    def betting_preflop(self):
        cp = self.dealer.next; # current player with action
        curr_bet = self.big_blind;

        self.players[cp.val].money_out = self.big_blind // 2; # small blind
        cp = cp.next;
        self.players[cp.val].money_out = self.big_blind; # big blind
        bb = cp.val; # big blind name
        while True:
            cp = cp.next;
            while not self.players[cp.val].status: cp = cp.next;

            if self.players[cp.val].money_out == curr_bet and cp.val != bb:
                for p in self.players:
                    self.pot += self.players[p].money_out;
                    self.players[p].bet(); # adjust stack size and money_out
                break;

            print();
            self.players[cp.val].display_hand();
            print("Pot:", str(self.pot), ", Bet:", str(curr_bet), "Committed:", str(self.players[cp.val].money_out),
                  "Stack:", str(self.players[cp.val].stack));
            bet = int(input("Player " + str(cp.val) + "'s bet (0=call, -1=fold): "));

            if bet == -1:
                self.players[cp.val].bet();
                self.players[cp.val].status = False;
            elif bet == 0 or bet < curr_bet: # call
                if curr_bet > self.players[cp.val].stack:
                    self.players[cp.val].money_out = self.players[cp.val].stack; # all-in to call
                else:
                    self.players[cp.val].money_out = curr_bet;
            else:
                curr_bet = bet;
                self.players[cp.val].money_out = bet;

    def betting(self):
        cp = self.dealer;  # current player with action

        curr_bet = 0;
        bet_made = False;
        while True:
            cp = cp.next;
            while not self.players[cp.val].status: cp = cp.next;

            if self.players[cp.val].money_out and bet_made:
                for p in self.players:
                    self.pot += self.players[p].money_out;
                    self.players[p].bet();  # adjust stack size and money_out
                break;

            print();
            self.display_runout();
            self.players[cp.val].display_hand();
            print("Pot:",str(self.pot),", Bet:",str(curr_bet),"Committed:",str(self.players[cp.val].money_out),"Stack:",str(self.players[cp.val].stack));
            bet = int(input("Player " + str(cp.val) + "'s bet (0=call, -1=fold): "));

            if bet == -1:
                self.players[cp.val].bet();
                self.players[cp.val].status = False;
            elif bet == 0 or bet < curr_bet:  # call
                if curr_bet > self.players[cp.val].stack:
                    self.players[cp.val].money_out = self.players[cp.val].stack;  # all-in to call
                else:
                    self.players[cp.val].money_out = curr_bet;
            else:
                curr_bet = bet;
                self.players[cp.val].money_out = bet;
                bet_made = True;

    def deal_hands(self):
        cp = self.dealer; # current player ; its a computer so dealing to the left of the dealer is dumb
        for h in self.deck.deal_table(len(self.players), self.hand_size):
            self.players[cp.val].hand = h;
            cp = cp.next;

    def clear_comm(self): self.com_hand = []; # clear community hand

    def deal_comm(self, num):
        for i in range(num):
            self.com_hand.append(self.deck.deal_one());

    def display_runout(self):
        print('Runout: ',end='');
        for card in self.com_hand:
            print(card, ' ', end='');
        print();

    def display_hands(self):
        for p in self.players:
            print("Player",self.players[p],': ', end='');
            self.players[p].display_hand();


