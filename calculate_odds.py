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
        f.close()

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

                table[hand][dealer][0] = round(float(hit_num_win)/max(float(hit_num_total), 1), 2)
                table[hand][dealer][1] = round(float(stay_num_win)/max(float(stay_num_total), 1), 2)

        print table
        return table

    @staticmethod
    def format_table(table):
        table = sorted([i for i in table.iteritems()])
        for player_hand, dealer_hands in table:
            line = [player_hand]
            dhands_sorted = sorted([int(hand) for hand in dealer_hands.iterkeys()])
            for hand in dhands_sorted:
                hand = str(hand)
                _hit, _stay = dealer_hands[hand]
                hit = round(float(_hit), 2)
                stay = round(float(_stay), 2)
                # line.append(str(hit) + " " + str(stay))

                if hit >= stay:
                    line.append(hand + " H")
                else:
                    line.append(hand + " S")

            print "\t".join(line) + "\n"

if __name__ == "__main__":
    Parser.parse()
    table = Parser.write_table()
    Parser.format_table(table)
