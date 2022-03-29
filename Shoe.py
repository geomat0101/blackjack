#!/usr/bin/env python

from SingleDeck import SingleDeck

class Shoe (SingleDeck):

    def __init__(self, num_decks=1):
        SingleDeck.__init__(self)
        self.num_decks = num_decks
        for i in range(num_decks-1):    # first one is free with the parent class init
            self.cards += self.build_deck()
    
    def __str__ (self):
        message = "Shoe - " + str(self.num_decks) + " decks: " + str(len(self.cards)) + " cards; "
        if not self.shuffled:
            message += "NOT "
        message += "shuffled"
        return(message)


if (__name__ == '__main__'):
    print(Shoe(1))
    d = Shoe(2)
    d.shuffle()
    print(d)
    while True:
        c = d.nextCard()
        if not c:
            break
        print(c)

