#!/usr/bin/env python

from blackjack.Blackjack import BlackJack

if (__name__ == '__main__'):
    print(BlackJack(num_players=4, num_decks=8).play())
