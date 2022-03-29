#!/usr/bin/env python

from Bankroll import MDGBankroll as Bankroll
from Hand import Hand
from Shoe import Shoe


# ref: https://healy.econ.ohio-state.edu/blackjack/table/dealing.html

class BlackJack (object):

    def __init__(self, num_players=1, num_decks=1):
        self.num_players = num_players
        self.num_decks = num_decks

        self.shoe = self.getShoe()
        self.player_hands = []

        self.dealer_hand = None
        self.dealer_hand_value = 0
        self.dealer_busted = False

        self.bankrolls = []
        for player in range(self.num_players):
            self.bankrolls.append(Bankroll())
            
        # see self.play() from here
        return
    

    def compare_hands (self):
        # compare player hands vs dealer and pay out winnings
        for hand in self.player_hands:
            hand_value = 0
            if hand.soft_score:
                hand_value = hand.soft_score
            else:
                hand_value = hand.combined_value
            
            hand.final_value = hand_value
            
            if hand.verdict:
                continue
    
            if self.dealer_busted:
                if hand_value <= 21:
                    hand.setVerdict('WIN')
            elif hand_value > 21:
                hand.setVerdict('LOSE')
            elif hand_value > self.dealer_hand_value:
                hand.setVerdict('WIN')
            elif hand_value == self.dealer_hand_value:
                hand.setVerdict('PUSH')
            else:
                hand.setVerdict('LOSE')

        v_map = {v: k for k, v in Hand.verdicts.iteritems()}

        for hand in self.player_hands:
            if hand.verdict == Hand.verdicts['BLACKJACK']:
                self.bankrolls[hand.player].blackjack(hand)
            elif hand.verdict == Hand.verdicts['WIN']:
                self.bankrolls[hand.player].win(hand)
            elif hand.verdict == Hand.verdicts['PUSH']:
                self.bankrolls[hand.player].push(hand)
            else:
                self.bankrolls[hand.player].lose(hand)

            message = "%9s - Player %d: %s -- %d -- %s" % (v_map[hand.verdict], hand.player, ', '.join([str(x) for x in hand.cards]), hand.final_value, self.bankrolls[hand.player])
            print(message)


    def deal (self):
        if len(self.shoe.discards) > (3 * len(self.shoe.cards)):
            # passed 75% shoe penetration; time to reshuffle
            print("Re-Shuffling . . .")
            self.shoe = self.getShoe()

        # new set of hands
        self.player_hands = []  
        for player in range(self.num_players):
            hand = Hand(player=player)
            self.bankrolls[player].bet(hand)
            self.player_hands.append(hand)
        
        self.dealer_hand = Hand()

        # first round of player cards
        for hand in self.player_hands:
            hand.addCard(self.shoe.nextCard())
        
        # dealer down-card
        downcard = self.shoe.nextCard()
        self.dealer_hand.addCard(downcard)

        # second round of player cards
        for hand in self.player_hands:
            hand.addCard(self.shoe.nextCard())

        # dealer up-card
        upcard = self.shoe.nextCard()
        self.dealer_hand.addCard(upcard)

        print("All cards dealt: Dealer showing " + str(upcard))


    def getShoe (self, burn_top_card=True):
        shoe = Shoe(self.num_decks)
        shoe.shuffle()
        if burn_top_card:
            shoe.nextCard()
        print(str(shoe))
        return(shoe)


    def play (self):
        # main game loop
        game_round = 1
        while True:
            print("*** Round %d ***" % game_round)
            self.deal()
            self.process_player_hands()

            self.dealer_hand_value = 0
            self.dealer_busted = False
            while self.dealer_hand_value < 17:
                self.process_dealer_hand()
            print(str(self.shoe))
            
            self.compare_hands()
            game_round += 1


    def process_dealer_hand (self):
        hand = self.dealer_hand
        message = "Dealer Hand: %s -- " % ', '.join([str(x) for x in hand.cards])
        if hand.soft_score:
            message += "%d / %d" % (hand.combined_value, hand.soft_score)
            self.dealer_hand_value = hand.soft_score
        else:
            message += "%d" % hand.combined_value
            self.dealer_hand_value = hand.combined_value

        print(message)

        if self.dealer_hand_value < 17:
            card = self.shoe.nextCard()
            print("Dealer Hits: %s" % card)
            hand.addCard(card)
        elif self.dealer_hand_value > 21:
            print("Dealer Busts")
            self.dealer_busted = True
        else:
            print("Dealer Stands")


    def process_player_hands (self):
        downcard = self.dealer_hand.cards[0]
        upcard = self.dealer_hand.cards[1]

        print("Checking for dealer BlackJack")

        # dealer blackjack?
        dealer_blackjack = False
        if upcard.value == 11:          # Ace showing
            # UNIMPLEMENTED: Insurance bets
            if downcard.value == 10:    # 10 under
                dealer_blackjack = True
        elif upcard.value == 10:        # 10 showing
            if downcard.value == 11:    # Ace under
                dealer_blackjack = True
        
        if dealer_blackjack:
            for hand in self.player_hands:
                if sum([x.value for x in hand.cards]) == 21:
                    # blackjack push
                    message = "Dealer BlackJack: Player %d pushed -- " % hand.player
                    hand.setVerdict('PUSH')
                else:
                    # player hand lost to dealer blackjack
                    message = "Dealer BlackJack: Player %d lost -- " % hand.player
                    hand.setVerdict('LOSE')
                message += ', '.join([str(x) for x in hand.cards])
                print(message)
        else:
            # process player hands
            for hand in self.player_hands:
                self.process_single_hand(hand, upcard)
            

    def process_single_hand (self, hand, upcard):
        print("Processing hand for player %d: %s" % (hand.player, ', '.join([str(x) for x in hand.cards])))
        # blackjack?
        if sum([x.value for x in hand.cards]) == 21:
            # player blackjack
            print("Player BlackJack -- Win")
            hand.setVerdict('BLACKJACK')
            return
            
        player_turn_in_progress = True
        while player_turn_in_progress:
            player_action = hand.evaluate(upcard)
            message = ""
            if player_action == Hand.action['HIT']:
                card = self.shoe.nextCard()
                message = "Hit: " + str(card) + " -- "
                hand.addCard(card)
            elif player_action == Hand.action['STAND']:
                message = "Stand -- "
                player_turn_in_progress = False
            elif player_action == Hand.action['SPLIT']:
                print("Player Splits the hand")
                
                # create a second hand and move one of the existing cards to it from the other hand
                # stick it on the front of the hands list
                split_hand = Hand(player=hand.player)
                self.bankrolls[hand.player].split(hand, split_hand)
                split_hand.addCard(hand.cards.pop())
                self.player_hands = [split_hand] + self.player_hands

                # deal the second card on it and process it immediately via recursion
                split_hand.addCard(self.shoe.nextCard())
                self.process_single_hand(split_hand, upcard)

                # deal a second card on the original hand and let it get processed again via
                # iterating in this while loop.  Reset initial_eval so it gets the first-time
                # eval treatment again in case we happen to deal out a split-after-split scenario
                hand.addCard(self.shoe.nextCard())
                hand.initial_eval = True
                print("Next split hand (player %d): %s" % (hand.player, ', '.join([str(x) for x in hand.cards])))
            elif player_action == Hand.action['DOUBLE']:
                # Doubles are a single hit with a forced-stand after the hit
                # give it one card, check it for a bust, and end the turn
                self.bankrolls[hand.player].double(hand)
                card = self.shoe.nextCard()
                message = "Double: " + str(card) + " -- "
                hand.addCard(card)
                if hand.combined_value > 21:
                    message = "Player Busted: Lose -- "
                    hand.setVerdict('LOSE')
                player_turn_in_progress = False
            elif player_action == Hand.action['BUSTED']:
                message = "Player Busted: Lose -- "
                hand.setVerdict('LOSE')
                player_turn_in_progress = False
            else:
                raise("Unimplemented player action: " + str(player_action))

            if message:
                if hand.soft_score:
                    message += "%d / %d" % (hand.combined_value, hand.soft_score)
                else:
                    message += str(hand.combined_value)
                print(message)



if (__name__ == '__main__'):
    print(BlackJack(num_players=10, num_decks=8).play())
