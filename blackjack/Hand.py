#!/usr/bin/env python

from blackjack.Card import Card

class Hand ():

    action = {
        'HIT': 1,
        'STAND': 2,
        'SPLIT': 4,
        'DOUBLE': 8,
        'SURRENDER': 16,
        'BUSTED': 32
    }

    verdicts = {
        'WIN': 1,
        'LOSE': 2,
        'PUSH': 4,
        'BLACKJACK': 8
    }


    def __init__(self, player=None):
        self.cards = []
        self.initial_eval = True
        self.player = player
        self.verdict = None
        self.bet = 0
        return


    def __str__(self):
        return(self.cards)


    def addCard(self, card):
        assert(isinstance(card, Card))
        self.cards.append(card)
        self.combined_value = sum([x.value for x in self.cards])

        # Soft hand?
        self.soft_score = None
        ace_count = len([x for x in self.cards if x.value == 11])
        if ace_count:
            self.combined_value = self.combined_value - (10 * ace_count)  # count aces as 1 to start instead of 11
            if self.combined_value <= 11:
                self.soft_score = self.combined_value + 10
            else:
                self.soft_score = self.combined_value
        

    def evaluate(self, upcard):
        if self.initial_eval:
            self.initial_eval = False
            card1 = self.cards[0]
            card2 = self.cards[1]
            # splits?
            if card1.value == card2.value:
                # potential split
                if card1.value in [8, 11]:
                    # always split pairs of Aces and Eights
                    return(self.action['SPLIT'])
                elif card1.value == 10:
                    # always stand on Tens
                    return(self.action['STAND'])
                elif card1.value == 9:
                    # stand if dealer is showing 7, 10, or A; else split
                    if upcard.value in [7,10,11]:
                        return(self.action['STAND'])
                    else:
                        return(self.action['SPLIT'])
                elif card1.value == 7:
                    # split if dealer is showing 7 or lower; else hit
                    if upcard.value <= 7:
                        return(self.action['SPLIT'])
                    else:
                        return(self.action['HIT'])
                elif card1.value == 6:
                    # split if dealer is showing 3-6; else hit
                    if upcard.value in [3, 4, 5, 6]:
                        return(self.action['SPLIT'])
                    else:
                        return(self.action['HIT'])
                elif card1.value == 5:
                    # double if dealer is showing < 10; else hit
                    if upcard.value < 10:
                        return(self.action['DOUBLE'])
                    else:
                        return(self.action['HIT'])
                elif card1.value == 4:
                    # always hit 4s
                    return(self.action['HIT'])
                else:
                    # split if dealer is showing 4-7; else hit
                    if upcard.value in [4,5,6,7]:
                        return(self.action['SPLIT'])
                    else:
                        return(self.action['HIT'])

            # not a split
            # got any aces?
            ace_offcard = None
            if card1.value == 11:
                ace_offcard = card2
            if card2.value == 11:
                ace_offcard = card1

            if ace_offcard:
                return(self.evaluate_soft_hand(ace_offcard.value, upcard.value))

            # No splits or Aces
            # check for double down opportunities
            if self.combined_value == 9:
                # Double if dealer is showing less than 7; else hit
                if upcard.value < 7:
                    return self.action['DOUBLE']
                else:
                    return self.action['HIT']
            elif self.combined_value == 10:
                # Double if dealer is showing less than 10; else hit
                if upcard.value < 10:
                    return self.action['DOUBLE']
                else:
                    return self.action['HIT']
            elif self.combined_value == 11:
                # Double if dealer is showing anything except Ace; else hit
                if upcard.value < 11:
                    return self.action['DOUBLE']
                else:
                    return self.action['HIT']
            
            # end of initial eval
            # no more splits or double downs after initial cards are dealt

        # busted?
        if self.combined_value > 21:
            return(self.action['BUSTED'])
        
        # Soft hand?
        ace_count = len([x for x in self.cards if x.value == 11])
        if ace_count:
            if self.soft_score > self.combined_value:
                ace_result = self.evaluate_soft_hand(self.soft_score-11, upcard.value)
                if ace_result == self.action['DOUBLE']:
                    # can't double after the initial hand
                    ace_result = self.action['HIT']
                return(ace_result)
        

        # if we are down here, then it's not a blackjack or split or double or a soft hand
        if self.combined_value >= 17:
            return(self.action['STAND'])
        elif self.combined_value >= 13:
            if upcard.value < 7:
                return(self.action['STAND'])
            else:
                return(self.action['HIT'])
        elif self.combined_value == 12:
            if upcard.value in [4,5,6]:
                return(self.action['STAND'])
            else:
                return(self.action['HIT'])
        else:
            return(self.action['HIT'])
            

    def evaluate_soft_hand (self, offcard_value, upcard_value):
        if offcard_value in [2,3]:
            # Double if dealer is showing 5-6; else hit
            if upcard_value in [5,6]:
                return self.action['DOUBLE']
            else:
                return self.action['HIT']
        elif offcard_value in [4,5]:
            # Double if dealer is showing 4-6; else hit
            if upcard_value in [4,5,6]:
                return self.action['DOUBLE']
            else:
                return self.action['HIT']
        elif offcard_value == 6:
            # Double if dealer is showing 3-6; else hit
            if upcard_value in [3,4,5,6]:
                return self.action['DOUBLE']
            else:
                return self.action['HIT']
        elif offcard_value == 7:
            # Double if dealer is showing 3-6
            # Stand if dealer is showing 2,7,8; else hit
            if upcard_value in [3,4,5,6]:                        
                return self.action['DOUBLE']
            elif upcard_value in [2,7,8]:
                return self.action['STAND']
            else:
                return self.action['HIT']
        else:
            return self.action['STAND']


    def setVerdict (self, verdict):
        verdict = verdict.upper()
        assert(verdict in self.verdicts.keys())
        assert(self.verdict is None)
        self.verdict = Hand.verdicts[verdict]









