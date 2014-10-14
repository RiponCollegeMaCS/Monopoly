from monopoly import *

for i in range(10):
    players = [Player(1), Player(2)]
    game1 = Game(players)
    print(game1.play())
