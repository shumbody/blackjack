import math
import random

class Card:
  card_types = {
            "ACE": 1,
            "TWO": 2,
            "THREE": 3,
             "FOUR":4,
            "FIVE": 5,
            "SIX": 6,
            "SEVEN": 7,
            "EIGHT": 8,
            "NINE": 9,
            "TEN": 10
  }
  def __init__(self, card_type):
            self.name = self._get_string_from_type(card_type)
            self.value = self._get_value_from_type(card_type)
            self.type = card_type

  def to_string(self):
      return self.name

  @staticmethod
  def type(str_value):
      return Card.card_types[str_value]

  def _get_string_from_type(self, card_type):
            if card_type == self.card_types["ACE"]:
                return "Ace"
            elif card_type == self.card_types["TWO"]:
                return "Two"
            elif card_type == self.card_types["THREE"]:
                return "Three"
            elif card_type == self.card_types["FOUR"]:
                return "Four"
            elif card_type == self.card_types["FIVE"]:
                return "Five"
            elif card_type == self.card_types["SIX"]:
                return "Six"
            elif card_type == self.card_types["SEVEN"]:
                return "Seven"
            elif card_type == self.card_types["EIGHT"]:
                return "Eight"
            elif card_type == self.card_types["NINE"]:
                return "Nine"
            elif card_type == self.card_types["TEN"]:
                return "Ten"

  def _get_value_from_type(self, card_type):
            if card_type == self.card_types["ACE"]:
                return 1
            elif card_type == self.card_types["TWO"]:
                return 2
            elif card_type == self.card_types["THREE"]:
                return 3
            elif card_type == self.card_types["FOUR"]:
                return 4
            elif card_type == self.card_types["FIVE"]:
                return 5
            elif card_type == self.card_types["SIX"]:
                return 6
            elif card_type == self.card_types["SEVEN"]:
                return 7
            elif card_type == self.card_types["EIGHT"]:
                return 8
            elif card_type == self.card_types["NINE"]:
                return 9
            elif card_type == self.card_types["TEN"]:
                return 10

class Deck:
    num_decks = 0
    card_count = {}
    cards_left = 0
    card_types = [
        Card.type("TWO"),
        Card.type("THREE"),
        Card.type("FOUR"),
        Card.type("FIVE"),
        Card.type("SIX"),
        Card.type("SEVEN"),
        Card.type("EIGHT"),
        Card.type("NINE"),
        Card.type("TEN"),
        Card.type("ACE")
    ]

    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.shuffle(num_decks)

    def deal_card(self):
        if self.is_empty():
            return None

        else:
            while True:
                index = self.random_index()
                card_type = self.card_types[index]

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
        return int(math.floor(random.random()*len(self.card_types)))

    def shuffle(self, mult):
        self.card_count = {
            Card.type("TWO"): 4*mult,
            Card.type("THREE"): 4*mult,
            Card.type("FOUR"): 4*mult,
            Card.type("FIVE"): 4*mult,
            Card.type("SIX"): 4*mult,
            Card.type("SEVEN"): 4*mult,
            Card.type("EIGHT"): 4*mult,
            Card.type("NINE"): 4*mult,
            Card.type("TEN"): 16*mult,
            Card.type("ACE"): 4*mult
        }
        self.cards_left = 52*mult

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
            if card.type == Card.type("ACE"):
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
        "LOSE": 1
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
        elif self.dealer.is_bust():
            outcome = Game.round_outcomes["WIN"]
        else:
            player_score = self.player.get_max_score()
            dealer_score = self.player.get_max_score()

            if player_score > dealer_score:
                outcome = Game.round_outcomes["WIN"]
            else:
                outcome = Game.round_outcomes["LOSE"]

        return outcome

    def is_game_over(self):
        return self.deck.get_cards_left() < 2*len(self.players)

    def play(self):
        round_num = 1
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
                        p.deal(self.deck.deal_card())

            outcome = self.get_round_outcome()
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

