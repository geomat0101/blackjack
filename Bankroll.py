#!/usr/bin/env python

class Bankroll (object):

    def __init__(self, cash=1000):
        self.cash = cash
        return


    def __str__(self):
        return("Cash: %0.2f" % self.cash)


    def bet (self, hand):
        wager = self.getNextBet()
        hand.bet = wager
        assert(self.cash > wager)
        self.cash -= wager


    def blackjack (self, hand):
        # pays original bet plus 3:2
        self.cash += (hand.bet * 2.5)


    def double (self, hand):
        assert(self.cash > hand.bet)
        self.cash -= hand.bet
        hand.bet *= 2


    def getNextBet (self):
        return 25


    def lose (self, hand):
        # already deducted from cash when bet was made
        pass


    def push (self, hand):
        # pays final bet back
        self.cash += hand.bet


    def split (self, orig_hand, new_hand):
        assert(self.cash > orig_hand.bet)
        self.cash -= orig_hand.bet
        new_hand.bet = orig_hand.bet


    def win (self, hand):
        # pays final bet back plus 1:1
        self.cash += hand.bet * 2


if (__name__ == '__main__'):
    pass
