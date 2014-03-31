blackjack
=========

A blackjack simulator for simulating games between a player and a dealer.

Run `python blackjack.py` to simulate games. Round outcomes get logged in `log.txt`. The format for each line is: player's card (`H` represents "hard" as opposed to "soft"), dealer's card, move (`0` is a "hit"), outcome (`0` is a "win").

Run `python calculate_odds.py` to parse through `log.txt` and calculate odds of winning for a given scenario (player card and dealer card) with a given move (hit or stay). 
