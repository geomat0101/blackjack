#!/usr/bin/env python

import random
from Card import Card

class SingleDeck (object):

    def __init__(self):
        self.shuffled = False
        self.cards = []
        self.discards = []
        for suit in Card.suits:
            for value in range(1, 14):
                c = Card(suit, value)
                self.cards.append(c)
    
    def __str__ (self):
        message = "SingleDeck: " + str(len(self.cards)) + " cards; "
        if not self.shuffled:
            message += "NOT "
        message += "shuffled"
        return(message)

    def shuffle (self):
        random.shuffle(self.cards)
        self.shuffled = True
    
    def nextCard (self):
        if not self.cards:
            return

        c = self.cards.pop()
        self.discards.append(c)
        return(c)

if (__name__ == '__main__'):
    d = SingleDeck()
    print(d)
    d.shuffle()
    print(d)
    print(d.nextCard())
    print(d)
    while True:
        c = d.nextCard()
        if not c:
            break
        print(c)
    print(d)
    
