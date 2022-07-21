from blackjack.Bankroll import Bankroll
from blackjack.Hand import Hand
import pytest


def test_Bankroll_init ():
    b = Bankroll()
    assert(b.cash == b.low_cash == b.high_cash == 1000)
    assert(not b.won_last_hand)


def test_Bankroll_adjust_cash ():
    b = Bankroll()
    with pytest.raises(AssertionError):
        b.adjust_cash(-1001)
    b.adjust_cash(-500)
    assert(b.cash == b.low_cash == 500)
    b.adjust_cash(1000)
    assert(b.cash == b.high_cash == 1500)


def test_Bankroll_bet ():
    b = Bankroll()
    h = Hand()
    b.bet(h)
    assert(h.bet == 100)
    assert(b.cash == 900)


def test_Bankroll_blackjack ():
    b = Bankroll()
    hand = Hand()
    b.bet(hand)
    b.blackjack(hand)
    assert(b.won_last_hand)
    assert(b.cash == 1150)


def test_Bankroll_double ():
    b = Bankroll()
    hand = Hand()
    b.bet(hand)
    b.double(hand)
    assert(b.cash == 800)
    assert(hand.bet == 200)


def test_Bankroll_getNextBet ():
    b = Bankroll()
    assert(b.getNextBet(None) == 100)


def test_Bankroll_lose ():
    b = Bankroll()
    hand = Hand()
    b.bet(hand)
    b.lose(hand)
    assert(not b.won_last_hand)


def test_Bankroll_push ():
    b = Bankroll()
    hand = Hand()
    b.bet(hand)
    b.push(hand)
    assert(b.cash == 1000)
    assert(not b.won_last_hand)


def test_Bankroll_split ():
    b = Bankroll()
    hand = Hand()
    hand2 = Hand()
    b.bet(hand)
    b.split(hand, hand2)
    assert(b.cash == 800)
    assert(hand2.bet == hand.bet)


def test_Bankroll_win ():
    b = Bankroll()
    hand = Hand()
    b.bet(hand)
    b.win(hand)
    assert(b.cash == 1100)
    assert(b.won_last_hand)
