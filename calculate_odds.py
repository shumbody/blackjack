from blackjack import Player, Game

class Parser:
    freq = {}

    def __init__(self):
        return

    @staticmethod
    def parse():
        f = open("log.txt")
        line = f.readline()

        while line != "":
            hand, dealer, move, outcome = line.split(" ")
            key = hand, dealer
            move_key = int(float(move))
            outcome_key = int(float(outcome))

            if key not in Parser.freq:
                Parser.freq[key] = {
                    Player.move("HIT"): [0,0],
                    Player.move("STAY"): [0,0]
                    }

            if outcome_key == Game.round_outcome("WIN"):
                Parser.freq[key][move_key][0] += 1

            Parser.freq[key][move_key][1] += 1

            line = f.readline()

    @staticmethod
    def write_table():
        keys = Parser.freq.keys()
        table = {}

        if len(keys) != 0:
            for key in keys:
                hand, dealer = key

                if hand not in table:
                    table[hand] = {}

                # win % for hit, stay
                table[hand][dealer] = [0, 0]

                hit_num_win, hit_num_total = Parser.freq[key][Player.move("HIT")]
                stay_num_win, stay_num_total = Parser.freq[key][Player.move("STAY")]

                table[hand][dealer][0] = float(hit_num_win)/float(hit_num_total)
                table[hand][dealer][1] = float(stay_num_win)/float(stay_num_total)

        print table

if __name__ == "__main__":
    Parser.parse()
    Parser.write_table()
