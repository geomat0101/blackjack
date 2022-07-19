import pytest
from blackjack.Card import Card


@pytest.mark.parametrize("suit,ranknum", 
        [   ('spades', 'x'), 
            ('clubs', 0), 
            ('hearts', 14),
            ('cups', 1)
        ])
def test_Card_init_input (suit, ranknum):
    with pytest.raises(AssertionError):
        Card(suit, ranknum)


@pytest.mark.parametrize("ranknum,expected,label",
        [
            (1, 11, "Ace"), (2, 2, "Two"), (3, 3, "Three"),
            (4, 4, "Four"), (5, 5, "Five"), (6, 6, "Six"),
            (7, 7, "Seven"), (8, 8, "Eight"), (9, 9, "Nine"), 
            (10, 10, "Ten"), (11, 10, "Jack"),
            (12, 10, "Queen"), (13, 10, "King")
        ])
def test_Card_init (ranknum, expected, label):
    c = Card('diamonds', ranknum)
    assert(c.value == expected)
    assert(str(c) == "%s of Diamonds" % label)