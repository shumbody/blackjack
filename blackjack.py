import math
import random

class Card:
    card_types = {
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "Q": 10,
            "K": 10
    }
    def __init__(self, card_type):
        self.value = self.card_types[card_type]
        self.type = card_type

    def __str__(self):
        return self.type

class Deck:
    num_decks = 0
    card_count = {}
    cards_left = 0

    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards_left = 52*self.num_decks

        for k in Card.card_types.iterkeys():
            self.card_count[k] = 4*self.num_decks

    def deal_card(self):
        if self.is_empty():
            return None

        else:
            while True:
                index = self.random_index()
                card_type = [i for i in Card.card_types.iterkeys()][index]

                if (self.card_count[card_type] != 0):
                    self.card_count[card_type] -= 1
                    self.cards_left -= 1
                    break

            return Card(card_type)

    def get_cards_left(self):
        return self.cards_left

    def is_empty(self):
        return self.cards_left == 0

    def random_index(self):
        return int(math.floor(random.random()*len(Card.card_types)))

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
          self.add_card(card)

    def clear(self):
        self.cards = []

    def get_hand_value(self):
        hand_value = 0
        for card in self.cards:
            hand_value += card.value
        return hand_value

    def has_aces(self):
        for card in self.cards:
            if card.type == "A":
                return True
        return False

    def get_size(self):
        return len(self.cards)

    def to_string(self):
        out = ""
        for card in self.cards:
            out += card.to_string()
            out += "\n"
        return out

class Player:
    moves = {"HIT": 0, "STAY": 1}

    def __init__(self):
        self.hand = Hand()

    @staticmethod
    def move(player_move):
        return Player.moves[player_move]

    def clear_hand(self):
        self.hand.clear()

    def deal(self, inp):
        if isinstance(inp, list):
            self.hand.add_cards(inp)
        elif isinstance(inp, Card):
            self.hand.add_card(inp)

    def get_move(self):
        index = int(math.floor(random.random()*len(Player.moves)))
        return index

    def get_max_score(self):
        min_score = self.get_min_score()
        max_score = min_score + 10

        if self.hand.has_aces() and max_score <= 21:
            return max_score
        else:
            return min_score

    def get_min_score(self):
        return self.hand.get_hand_value()

    def has_aces(self):
        return self.hand.has_aces()

    def is_bust(self):
        score = self.get_max_score()
        return score > 21

    def print_hand(self):
        print [card.value for card in self.hand.cards]

class Dealer(Player):
    def __init__(self):
        Player.__init__(self)

    def get_move(self):
        if self.get_max_score() < 17:
            return Player.move("HIT")
        else:
            return Player.move("STAY")

class Logger:
    round_actions = []

    def __init__(self):
        return

    @staticmethod
    def clear():
        Logger.round_actions = []
        Logger.log = []

    @staticmethod
    def emit(max_score, min_score, dealer_card, move):
        if min_score != max_score:
            value = "S"
        else:
            value = "H"

        value += str(max_score)
        Logger.round_actions.append([value, dealer_card, move])

    @staticmethod
    def log_round(outcome):
        logfile = open('log.txt', 'a')
        for value, dealer_card, move in Logger.round_actions:
            log_line = ""
            log_line += str(value) + " "
            log_line += str(dealer_card) + " "
            log_line += str(move) + " "
            log_line += str(outcome) + "\n"
            logfile.write(log_line)
        Logger.round_actions = []
        logfile.close()

class Game:
    round_outcomes = {
        "WIN": 0,
        "LOSE": 1,
        "PUSH": 2
    }

    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()

        self.players = []
        self.players.append(self.player)
        self.players.append(self.dealer)

        self.deck = Deck(6)

    def deal_cards(self):
        for p in self.players:
            card1 = self.deck.deal_card()
            card2 = self.deck.deal_card()
            p.deal([card1, card2])

    def get_round_outcome(self):
        if self.player.is_bust():
            outcome = Game.round_outcomes["LOSE"]
        else:
            if self.dealer.is_bust():
                outcome = Game.round_outcomes["WIN"]
            else:
                player_score = self.player.get_max_score()
                dealer_score = self.dealer.get_max_score()

                if player_score > dealer_score:
                    outcome = Game.round_outcomes["WIN"]
                elif player_score < dealer_score:
                    outcome = Game.round_outcomes["LOSE"]
                else:
                    outcome = Game.round_outcomes["PUSH"]

        return outcome

    def is_game_over(self):
        return self.deck.get_cards_left() < 2*len(self.players)

    def play(self):
        while not self.is_game_over():
            self.deal_cards()

            for p in self.players:
                player_move = None
                while player_move != Player.move("STAY") and not p.is_bust():
                    player_move = p.get_move()

                    if not isinstance(p, Dealer):
                        max_score = p.get_max_score()
                        min_score = p.get_min_score()
                        dealer_card = self.dealer.hand.cards[0].value
                        Logger.emit(max_score, min_score, dealer_card, player_move)

                    if player_move == Player.move("HIT"):
                        dealt_card = self.deck.deal_card()
                        if dealt_card is not None:
                            p.deal(dealt_card)
                        else:
                            break

                # Player busts, end round early.
                if p.is_bust() and not isinstance(p, Dealer):
                    break

            outcome = self.get_round_outcome()
            if outcome is not Game.round_outcome("PUSH"):
                Logger.log_round(outcome)

            #Round over, clear hands
            for p in self.players:
                p.clear_hand()

    @staticmethod
    def round_outcome(outcome):
        return Game.round_outcomes[outcome]

if __name__ == "__main__":
    for i in range(10000):
        game = Game()
        game.play()

