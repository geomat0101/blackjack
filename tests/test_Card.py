import pytest
from blackjack.Card import Card

def test_Card ():
    assert(str(Card('sPaDeS', 1)) == 'Ace of Spades')