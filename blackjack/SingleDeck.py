#!/usr/bin/env python

from blackjack.Card import Card
from queue import deque
import random

class SingleDeck ():

    def __init__(self):
        self.shuffled = False
        self.discards = deque()
        self.cards = self.build_deck()

    def build_deck (self):
        deck = deque()
        for suit in Card.suits:
            for ranknum in range(1, 14):
                deck.append(Card(suit, ranknum))
        return(deck)
    
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

        c = self.cards.popleft()
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
    

