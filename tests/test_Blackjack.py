from blackjack.Bankroll import Bankroll
from blackjack.Blackjack import BlackJack
from blackjack.Card import Card
from blackjack.Hand import Hand
from blackjack.Shoe import Shoe
import pytest


# helper methods
def aceFactory (*args, **kwargs):
    return(Card('spades',1))


def calledIt (self, *args, **kwargs):
    if 'pytest' not in dir(self):
        self.pytest = {}
    self.pytest['calledIt'] = True


# tests
def test_Blackjack_init ():
    b = BlackJack()
    assert(b.num_players == b.num_decks == 1)


'''
            self.deal()
            self.process_player_hands()
            self.dealer_hand_value = 0
            self.dealer_busted = False
            while self.dealer_hand_value < 17:
                self.process_dealer_hand()
            self.compare_hands()
'''

def test_Blackjack_deal ():
    b = BlackJack()
    b.deal()
    assert(len(b.player_hands) == 1)
    assert(b.dealer_hand)
    assert(len(b.player_hands[0].cards) == 2)
    assert(len(b.dealer_hand.cards) == 2)


@pytest.mark.parametrize("downcard,upcard,card1,card2,exp_verdict",
        [
            (Card('spades',10),Card('spades',1),Card('spades',10),Card('spades',1),'PUSH'),
            (Card('spades',10),Card('spades',1),Card('spades',10),Card('spades',10),'LOSE')
        ])
def test_Blackjack_process_player_hands (downcard, upcard, card1, card2, exp_verdict):
    b = BlackJack()
    b.deal()
    b.dealer_hand.cards = [downcard, upcard]
    b.player_hands[0].cards = [card1,card2]
    b.process_player_hands()
    assert(b.player_hands[0].getVerdict() == exp_verdict)


@pytest.mark.parametrize("card1,card2,upcard,exp_verdict",
        [
            (Card('spades',10),Card('spades',1),Card('spades',6),'BLACKJACK')
        ])
def test_Blackjack_process_single_hand (card1, card2, upcard, exp_verdict):
    hand = Hand(player=0)
    hand.addCard(card1)
    hand.addCard(card2)
    b = BlackJack()
    b.process_single_hand(hand, upcard)
    assert(hand.getVerdict() == exp_verdict)


def test_Blackjack_hit ():
    b = BlackJack()
    hand = Hand()
    card = b.shoe.cards[0]
    b.hit(hand)
    assert(hand.cards[-1] == card)


def test_Blackjack_split (monkeypatch):
    # after the split, a new hand should be prepended to the hands list and already
    # evaluated with a verdict on it.  The original hand is given a new card and is
    # reset for initial evaluation by the caller (process_single_hand)
    b = BlackJack()
    hand = Hand(player=0)
    hand.addCard(Card('spades',10))
    hand.addCard(Card('spades',10))
    b.player_hands.append(hand)
    upcard = Card('spades',1)
    monkeypatch.setattr(Shoe, "nextCard", aceFactory) # splitting 10s and drawing Aces
    assert(b.shoe.nextCard().ranknum == 1)
    monkeypatch.setattr(Bankroll, "split", calledIt)
    b.split(hand,upcard)
    assert(b.bankrolls[hand.player].pytest['calledIt'])
    assert(len(b.player_hands) == 2)
    assert(b.player_hands[-1] == hand)
    assert(b.player_hands[-1].initial_eval)
    assert(b.player_hands[0].getVerdict() == 'BLACKJACK')


def test_Blackjack_double (monkeypatch):
    b = BlackJack()
    hand = Hand(player=0)
    monkeypatch.setattr(Bankroll, "double", calledIt)
    b.double(hand)
    assert(b.bankrolls[hand.player].pytest['calledIt'])


@pytest.mark.parametrize("card1,card2,card3,exp_dhv",
        [
            (Card('spades',1),Card('spades',9),None,20),
            (Card('spades',10),Card('spades',10),None,20),
            (Card('spades',10),Card('spades',6),None,16),
            (Card('spades',10),Card('spades',10),Card('spades',10),30)
        ])
def test_Blackjack_process_dealer_hand (monkeypatch, card1, card2, card3, exp_dhv):
    hand = Hand()
    hand.addCard(card1)
    hand.addCard(card2)
    if card3:
        hand.addCard(card3)
    b = BlackJack()
    b.dealer_hand = hand
    b.process_dealer_hand()
    assert(b.dealer_hand_value == exp_dhv)
    if exp_dhv < 17:
        assert(len(hand.cards) == 3)
    if exp_dhv > 21:
        assert(b.dealer_busted)


@pytest.mark.parametrize("card1,card2,card3,dealer_busted,dhv,exp_verdict",
        [
            (Card('spades', 10), Card('spades', 10), None, True, 30, 'WIN'),
            (Card('spades', 10), Card('spades', 10), Card('spades', 10), False, 20, 'LOSE'),
            (Card('spades', 10), Card('spades', 10), None, False, 19, 'WIN'),
            (Card('spades', 10), Card('spades', 10), None, False, 20, 'PUSH'),
            (Card('spades', 10), Card('spades', 9), None, False, 20, 'LOSE')
        ])
def test_Blackjack_compare_single_hand (card1, card2, card3, dealer_busted, dhv, exp_verdict):
    hand = Hand(player=0)
    hand.addCard(card1)
    hand.addCard(card2)
    if card3:
        hand.addCard(card3)
    b = BlackJack()
    b.dealer_busted = dealer_busted
    b.dealer_hand_value = dhv
    b.compare_single_hand(hand)
    assert(hand.getVerdict() == exp_verdict)

