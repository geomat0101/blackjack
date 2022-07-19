from blackjack.Card import Card
from blackjack.Hand import Hand
# from blackjack.Shoe import Shoe
import pytest


def test_Hand_init ():
    h = Hand(player='foo')
    assert(len(h.cards) == 0)
    assert(h.initial_eval)
    assert(h.player == 'foo')
    assert(h.verdict == None)
    assert(h.bet == 0)


@pytest.mark.parametrize("card1,card2,card3,exp_combined,exp_soft",
        [
            (Card('spades',10), Card('spades', 10), None, 20, None),
            (Card('spades',1), Card('spades', 10), None, 11, 21),
            (Card('spades',10), Card('spades', 10), Card('spades', 1), 21, 21),
        ])
def test_Hand_addCard (card1, card2, card3, exp_combined, exp_soft):
    h = Hand()
    h.addCard(card1)
    assert(h.cards[-1] == card1)
    h.addCard(card2)
    assert(h.cards[-1] == card2)
    if card3:
        h.addCard(card3)
        assert(h.cards[-1] == card3)
    assert(h.combined_value == exp_combined)
    assert(h.soft_score == exp_soft)