#!/usr/bin/env python

class Bankroll ():

    def __init__(self, cash=1000):
        self.cash = cash
        self.low_cash = cash
        self.high_cash = cash
        self.won_last_hand = False
        return


    def __str__(self):
        return("Cash: %0.2f - %0.2f - %0.2f" % (self.low_cash, self.cash, self.high_cash))


    def adjust_cash (self, amount):
        assert((self.cash + amount) > 0)
        self.cash += int(amount)
        if self.cash < self.low_cash:
            self.low_cash = self.cash
        if self.cash > self.high_cash:
            self.high_cash = self.cash


    def bet (self, hand):
        wager = self.getNextBet()
        hand.bet = wager
        self.adjust_cash(-1 * wager)


    def blackjack (self, hand):
        # pays original bet plus 3:2
        self.adjust_cash(hand.bet * 2.5)
        self.won_last_hand = True


    def double (self, hand):
        self.adjust_cash(-1 * hand.bet)
        hand.bet *= 2


    def getNextBet (self):
        return 100


    def lose (self, hand):
        # already deducted from cash when bet was made
        self.won_last_hand = False


    def push (self, hand):
        # pays final bet back
        self.adjust_cash(hand.bet)
        self.won_last_hand = False


    def split (self, orig_hand, new_hand):
        self.adjust_cash(-1 * orig_hand.bet)
        new_hand.bet = orig_hand.bet


    def win (self, hand):
        # pays final bet back plus 1:1
        self.adjust_cash(hand.bet * 2)
        self.won_last_hand = True


class MDGBankroll (Bankroll):

    def __init__ (self, cash=1000):
        Bankroll.__init__(self, cash=cash)

        print("MDGBankroll loaded")
        self.mark = False
        return


    def getNextBet (self):
        if not self.mark:
            if self.won_last_hand:
                self.mark = True
            return 25
        
        # mark is on
        if self.won_last_hand:
            # keep it rolling
            return 25
        
        # mark is on and lost one; go big one round
        self.mark = False
        print("BETTING 50")
        return 50


if (__name__ == '__main__'):
    pass
