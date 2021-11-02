#!/usr/bin/env python

from Hand import Hand
from Shoe import Shoe


# ref: https://healy.econ.ohio-state.edu/blackjack/table/dealing.html

class BlackJack (object):

    def __init__(self, num_players=1, num_decks=1):
        self.num_players = num_players
        self.num_decks = num_decks
        self.shoe = self.getShoe()
        return


    def getShoe (self, burn_top_card=True):
        shoe = Shoe(self.num_decks)
        shoe.shuffle()
        if burn_top_card:
            shoe.nextCard()
        return(shoe)


    def deal (self):
        if len(self.shoe.discards) > (3 * len(self.shoe)):
            # passed 75% shoe penetration; time to reshuffle
            print("Re-Shuffling . . .")
            self.shoe = self.getShoe()

        player_hands = []
        for player in range(self.num_players):
            player_hands.append(Hand())
        
        dealer_hand = Hand()

        # first round of player cards
        for hand in player_hands:
            hand.addCard(self.shoe.nextCard())
        
        # dealer down-card
        downcard = self.shoe.nextCard()
        dealer_hand.addCard(downcard)

        # second round of player cards
        for hand in player_hands:
            hand.addCard(self.shoe.nextCard())

        # dealer up-card
        upcard = self.shoe.nextCard()
        dealer_hand.addCard(upcard)

        # dealer blackjack?
        # UNIMPLEMENTED: Insurance bets
        dealer_blackjack = False
        if upcard.value == 11:          # Ace showing
            if downcard.value == 10:    # 10 under
                dealer_blackjack = True
        elif upcard.value == 10:        # 10 showing
            if downcard.value == 11:    # Ace under
                dealer_blackjack = True
        
        # UNIMPLEMENTED: WIN/LOSS
        if dealer_blackjack:
            for hand in player_hands:
                if sum([x.value for x in hand.cards]) == 21:
                    # blackjack push
                    pass
                else:
                    # player hand lost to dealer blackjack
                    pass
            return
        

        # process player hands
        for hand in player_hands:
            # blackjack?
            if sum([x.value for x in hand.cards]) == 21:
                # player blackjack
                next
            
            # UNIMPLEMENTED: Surrender Hands
            player_action = hand.evaluate(upcard)

        
if (__name__ == '__main__'):
    print(BlackJack(num_players=1, num_decks=6).shoe)
