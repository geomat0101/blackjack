from blackjack.Card import Card
from blackjack.Hand import Hand
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


@pytest.mark.parametrize("card1,card2,card3,upcard,exp_action",
        [
            (Card('spades',4), Card('spades',5), None, Card('spades',6), 'DOUBLE'),
            (Card('spades',4), Card('spades',5), None, Card('spades',7), 'HIT'),
            (Card('spades',4), Card('spades',6), None, Card('spades',9), 'DOUBLE'),
            (Card('spades',4), Card('spades',6), None, Card('spades',10), 'HIT'),
            (Card('spades',5), Card('spades',6), None, Card('spades',10), 'DOUBLE'),
            (Card('spades',5), Card('spades',6), None, Card('spades',1), 'HIT'),
            (Card('spades',10), Card('spades',10), Card('spades',10), Card('spades',1), 'BUSTED'),
            (Card('spades',2), Card('spades',3), Card('spades',1), Card('spades',6), 'HIT'),
            (Card('spades',10), Card('spades',7), None, Card('spades',1), 'STAND'),
            (Card('spades',10), Card('spades',6), None, Card('spades',6), 'STAND'),
            (Card('spades',10), Card('spades',6), None, Card('spades',7), 'HIT'),
            (Card('spades',10), Card('spades',2), None, Card('spades',3), 'HIT'),
            (Card('spades',10), Card('spades',2), None, Card('spades',4), 'STAND'),
            (Card('spades',10), Card('spades',2), None, Card('spades',5), 'STAND'),
            (Card('spades',10), Card('spades',2), None, Card('spades',6), 'STAND'),
            (Card('spades',10), Card('spades',2), None, Card('spades',7), 'HIT'),
            (Card('spades',2), Card('spades',3), None, Card('spades',1), 'HIT'),
            (Card('spades',2), Card('spades',4), None, Card('spades',1), 'HIT'),
            (Card('spades',4), Card('spades',3), None, Card('spades',1), 'HIT'),
            (Card('spades',5), Card('spades',3), None, Card('spades',1), 'HIT')
        ])
def test_Hand_evaluate (card1, card2, card3, upcard, exp_action):
    h = Hand()
    h.addCard(card1)
    h.addCard(card2)
    action = h.evaluate(upcard)
    assert(not h.initial_eval)
    if card3:
        h.addCard(card3)
        action = h.evaluate(upcard)
    assert(h.a_map[action] == exp_action)


@pytest.mark.parametrize("split_value,upcard_value,exp_action",
        [
            (8,11,'SPLIT'),
            (11,11,'SPLIT'),
            (10,11,'STAND'),
            (9,6,'SPLIT'),
            (9,7,'STAND'),
            (9,9,'SPLIT'),
            (9,10,'STAND'),
            (9,11,'STAND'),
            (7,7,'SPLIT'),
            (7,8,'HIT'),
            (6,2,'HIT'),
            (6,3,'SPLIT'),
            (6,4,'SPLIT'),
            (6,5,'SPLIT'),
            (6,6,'SPLIT'),
            (6,7,'HIT'),
            (5,9,'DOUBLE'),
            (5,10,'HIT'),
            (4,2,'HIT'),
            (4,11,'HIT'),
            (3,3,'HIT'),
            (3,4,'SPLIT'),
            (3,5,'SPLIT'),
            (3,6,'SPLIT'),
            (3,7,'SPLIT'),
            (3,8,'HIT'),
            (2,3,'HIT'),
            (2,4,'SPLIT'),
            (2,5,'SPLIT'),
            (2,6,'SPLIT'),
            (2,7,'SPLIT'),
            (2,8,'HIT')
        ])
def test_Hand_evaluate_split (split_value, upcard_value, exp_action):
    h = Hand()
    action = h.evaluate_split(split_value, upcard_value)
    assert(h.a_map[action] == exp_action)


@pytest.mark.parametrize("offcard_value,upcard_value,exp_action",
        [
            (2,4,'HIT'),
            (2,5,'DOUBLE'),
            (2,6,'DOUBLE'),
            (2,7,'HIT'),
            (3,4,'HIT'),
            (3,5,'DOUBLE'),
            (3,6,'DOUBLE'),
            (3,7,'HIT'),
            (4,3,'HIT'),
            (4,4,'DOUBLE'),
            (4,5,'DOUBLE'),
            (4,6,'DOUBLE'),
            (4,7,'HIT'),
            (5,3,'HIT'),
            (5,4,'DOUBLE'),
            (5,5,'DOUBLE'),
            (5,6,'DOUBLE'),
            (5,7,'HIT'),
            (6,2,'HIT'),
            (6,3,'DOUBLE'),
            (6,4,'DOUBLE'),
            (6,5,'DOUBLE'),
            (6,6,'DOUBLE'),
            (6,7,'HIT'),
            (7,2,'STAND'),
            (7,3,'DOUBLE'),
            (7,4,'DOUBLE'),
            (7,5,'DOUBLE'),
            (7,6,'DOUBLE'),
            (7,7,'STAND'),
            (7,8,'STAND'),
            (7,9,'HIT'),
            (7,10,'HIT'),
            (7,11,'HIT'),
            (8,11,'STAND'),
            (9,11,'STAND'),
            (10,11,'STAND')
        ])
def test_Hand_evaluate_soft_hand (offcard_value, upcard_value, exp_action):
    h = Hand()
    action = h.evaluate_soft_hand(offcard_value, upcard_value)
    assert(h.a_map[action] == exp_action)

