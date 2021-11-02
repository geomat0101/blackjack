#!/usr/bin/env python

class Card (object):

    ranks = [   '',
                'Ace',
                'Two',
                'Three',
                'Four',
                'Five',
                'Six',
                'Seven',
                'Eight',
                'Nine',
                'Ten',
                'Jack',
                'Queen',
                'King'
                ]
    
    suits = ['SPADES', 'CLUBS', 'HEARTS', 'DIAMONDS']

    def __init__(self, suit, value):
        assert(type(value) == type(1))
        assert(value > 0)
        assert(value < 14)
        assert(suit.upper() in self.suits)
        self.suit = suit.lower().capitalize()
        self.value = value
    
    def __str__(self):
        return(self.ranks[self.value] + ' of ' + self.suit)


if (__name__ == '__main__'):
    print(Card('sPaDeS', 1))
