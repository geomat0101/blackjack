#!/usr/bin/env python

from blackjack.Bankroll import MDGBankroll as Bankroll
from blackjack.Hand import Hand
from blackjack.Shoe import Shoe


# ref: https://healy.econ.ohio-state.edu/blackjack/table/dealing.html

class BlackJack ():

    def __init__(self, num_players=1, num_decks=1):
        self.num_players = num_players
        self.num_decks = num_decks
        self.interactive = set()

        self.shoe = self.getShoe()
        self.player_hands = []

        self.dealer_hand = None
        self.dealer_hand_value = 0
        self.dealer_busted = False

        self.bankrolls = []
        for player in range(self.num_players):
            self.bankrolls.append(Bankroll())
            self.interactive.add(player)
            
        # see self.play() from here
        return


    def compare_single_hand (self, hand):
        hand_value = 0
        if hand.soft_score:
            hand_value = hand.soft_score
        else:
            hand_value = hand.combined_value
        
        hand.final_value = hand_value
        
        if hand.verdict:
            return

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
    

    def update_bankroll (self, hand, bankroll):
        verdict_handlers = {
            'BLACKJACK':    bankroll.blackjack,
            'WIN':          bankroll.win,
            'PUSH':         bankroll.push,
            'LOSE':         bankroll.lose
        }
        verdict_handlers[hand.getVerdict()](hand)


    def compare_hands (self):
        # compare player hands vs dealer and pay out winnings
        for hand in self.player_hands:
            self.compare_single_hand(hand)
        
        for hand in self.player_hands:
            self.update_bankroll(hand, self.bankrolls[hand.player])
            message = "%9s - Player %d: %s -- %d -- %s" % (hand.v_map[hand.verdict], hand.player, ', '.join([str(x) for x in hand.cards]), hand.final_value, self.bankrolls[hand.player])
            print(message)


    def print_help_bet (self):
        print('''
    ?:  Print this message
    A:  Automate Decisions
    ### 0 < x <= bank:  Place a bet

    [ENTER] alone will place the suggested bet in [brackets]
''')
    

    def prompt_bet (self, hand, bankroll):
        valid_input = False
        wager = bankroll.getNextBet(hand)
        while not valid_input:
            print("\n'?' for Help\nPlayer %d -- Bank: $%0.2f" % (hand.player, bankroll.cash))
            user_input = input("Player Bet [%d]: " % wager).strip()
            if not user_input:
                return(wager)
            try:
                user_input = int(user_input)
                if user_input > 0 and user_input <= bankroll.cash:
                    return(user_input)
            except:
                user_input = user_input.upper()
                if user_input[0] == '?':
                    self.print_help_bet()
                elif user_input[0] == 'A':
                    self.interactive.remove(hand.player)
                    return(wager)
                else:
                    print("ERR: You did it wrong.  Enter a valid bet (0 < x <= bank)")


    def deal (self):
        if len(self.shoe.discards) > (3 * len(self.shoe.cards)):
            # passed 75% shoe penetration; time to reshuffle
            print("Re-Shuffling . . .")
            self.shoe = self.getShoe()

        # new set of hands
        self.player_hands = []  
        for player in range(self.num_players):
            hand = Hand(player=player)
            wager = None
            if hand.player in self.interactive:
                wager = self.prompt_bet(hand, self.bankrolls[player])
            self.bankrolls[player].bet(hand, wager=wager)
            self.player_hands.append(hand)
            print("Player %d: Bet $%0.2f" % (hand.player, hand.bet))
        
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

        # dealer blackjack?
        dealer_blackjack = False
        if upcard.value >= 10:
            print("Checking for dealer BlackJack")

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
    

    def hand_value_suffix (self, hand):
            if hand.soft_score and hand.soft_score > hand.combined_value:
                return("%d / %d" % (hand.combined_value, hand.soft_score))
            else:
                return(str(hand.combined_value))


    def hit (self, *args, **kwargs):
        hand = args[0]
        hand.addCard(self.shoe.nextCard())


    def split (self, *args, **kwargs):
        hand = args[0]
        upcard = args[1]
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
        print("Next split hand (player %d): %s -- %s" % (hand.player, ', '.join([str(x) for x in hand.cards]), self.hand_value_suffix(hand)))


    def double (self, *args, **kwargs):
        # Doubles are a single hit with a forced-stand after the hit
        # give it one card, check it for a bust, and end the turn
        hand = args[0]
        self.bankrolls[hand.player].double(hand)
        card = self.shoe.nextCard()
        hand.addCard(card)
    

    def print_help_actions (self):
        print('''
    ?:  Print this message
    H:  Hit
    S:  Stand
    D:  Double
    /:  Split
    A:  Automate Decisions
    *:  Display Recommendation

    [ENTER] alone will execute the "correct" action
''')


    def prompt_action(self, hand, upcard, suggestion):
        act_name = suggestion
        valid_input = False
        while not valid_input:
            print("%s -- %s" % (', '.join([str(x) for x in hand.cards]), self.hand_value_suffix(hand)))
            print("Dealer Showing: %s" % (str(upcard)))
            print("[?HSD/A*]")
            user_input = input('? ').strip().upper()
            if not user_input:
                return(act_name)

            if user_input[0] == '?':
                self.print_help_actions()
            elif user_input[0] == 'H':
                act_name = 'HIT'
                valid_input = True
            elif user_input[0] == 'S':
                act_name = 'STAND'
                valid_input = True
            elif user_input[0] == 'D':
                if len(hand.cards) > 2:
                    print("ERR: Can only DOUBLE on first hand action")
                else:
                    act_name = 'DOUBLE'
                    valid_input = True
            elif user_input[0] == '/':
                if len(hand.cards) > 2:
                    print("ERR: Can only SPLIT on first hand action")
                elif hand.cards[0].ranknum != hand.cards[1].ranknum:
                    print("ERR: Can only SPLIT cards with the same value")
                else:
                    act_name = 'SPLIT'
                    valid_input = True
            elif user_input[0] == 'A':
                print("INFO: Player %d decisions are now automated" % hand.player)
                self.interactive.remove(hand.player)
                valid_input = True
            elif user_input[0] == '*':
                print("You should %s\n" % act_name)

        return(act_name)
    

    def process_next_turn_iteration (self, hand, upcard):
        # handler method, continue_turn value
        action_handler = {
            'HIT':      (self.hit, True),
            'STAND':    (None, False),
            'SPLIT':    (self.split, True),
            'DOUBLE':   (self.double, False),
            'BUSTED':   (None, False)
        }

        act_name = hand.a_map[hand.evaluate(upcard)]
        if hand.player in self.interactive and act_name != 'BUSTED':
            act_name = self.prompt_action(hand, upcard, act_name)
        (handler, continue_turn) = action_handler[act_name]

        if handler:
            handler(hand, upcard)

        message = ""
        if act_name == 'HIT':
            message = "Hit: " + str(hand.cards[-1]) + " -- "
        elif act_name == 'STAND':
            message = "Stand -- "
        elif act_name == 'SPLIT':
            pass
        elif act_name == 'DOUBLE':
            message = "Double: " + str(hand.cards[-1]) + " -- "
            if hand.combined_value > 21:
                message = "Player Busted: Lose -- "
                hand.setVerdict('LOSE')
        elif act_name == 'BUSTED':
            message = "Player Busted: Lose -- "
            hand.setVerdict('LOSE')
        else:
            raise("Unimplemented player action: " + str(act_name))

        if message:
            message += self.hand_value_suffix(hand)
            print(message)
        
        return(continue_turn)


    def process_single_hand (self, hand, upcard):
        message = "\n\nProcessing hand for player %d: %s -- " % (hand.player, ', '.join([str(x) for x in hand.cards]))
        message += self.hand_value_suffix(hand)
        print(message)
        # blackjack?
        if sum([x.value for x in hand.cards]) == 21:
            # player blackjack
            print("Player BlackJack -- Win")
            hand.setVerdict('BLACKJACK')
            return
            
        while self.process_next_turn_iteration(hand, upcard):
            pass



if (__name__ == '__main__'):
    print(BlackJack(num_players=10, num_decks=8).play())
