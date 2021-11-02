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

    def __init__(self, suit, ranknum):
        assert(type(ranknum) == type(1))
        assert(ranknum > 0)
        assert(ranknum < 14)
        assert(suit.upper() in self.suits)
        self.suit = suit.lower().capitalize()
        self.ranknum = ranknum
        if ranknum > 9:
            self.value = 10
        elif ranknum == 1:
            self.value = 11
        else:
            self.value = ranknum
    
    def __str__(self):
        return(self.ranks[self.ranknum] + ' of ' + self.suit)


if (__name__ == '__main__'):
    print(Card('sPaDeS', 1))
