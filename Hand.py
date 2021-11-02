#!/usr/bin/env python

from Card import Card

class Hand (object):

    action = {
        HIT: 1,
        STAND: 2,
        SPLIT: 4,
        DOUBLE: 8,
        SURRENDER: 16
    }

    def __init__(self):
        self.cards = []
        self.initial_eval = True
        return

    def __str__(self):
        return(self.cards)

    def addCard(self, card):
        assert(isinstance(card, Card))
        self.cards.append(card)

    def evaluate(self, upcard):
        if self.initial_eval:
            # splits?
            if self.cards[0].value == self.cards[1].value:
                # potential split
                pass