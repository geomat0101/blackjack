from blackjack.Shoe import Shoe
import pytest


def test_Shoe_init ():
    s = Shoe(num_decks=8)
    assert(s.num_decks == 8)
    assert(len(s.cards) == 8*52)

