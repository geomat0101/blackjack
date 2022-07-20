from blackjack.SingleDeck import SingleDeck
from blackjack.Card import Card
from itertools import islice
import pytest

def test_SingleDeck_init ():
    d = SingleDeck()
    assert(not d.shuffled)
    assert(len(d.discards) == 0)
    assert(len(d.cards) == 52)


def test_SingleDeck_build_deck ():
    d = SingleDeck()
    i = 0
    for suit in Card.suits:
        label = suit.lower().capitalize()
        for rank in range(1, 14):
            card = d.cards[i]
            assert(card.ranknum == rank)
            assert(card.suit == label)
            i += 1


def test_SingleDeck_shuffle ():
    d = SingleDeck()
    assert(not d.shuffled)
    (a,b,c) = islice(d.cards, 0, 3)
    d.shuffle()
    assert(d.shuffled)
    (x,y,z) = islice(d.cards, 0, 3)
    assert(not (a==x and b==y and c==z)) # ~1:52**3 odds of false match


def test_SingleDeck_nextCard ():
    d = SingleDeck()
    a = d.cards[0]
    card = d.nextCard()
    assert(card.suit == Card.suits[0].lower().capitalize())
    assert(card.ranknum == 1)
    assert(a == d.discards[0])

    d.cards = []
    assert(d.nextCard() == None)

