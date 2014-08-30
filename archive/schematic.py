#Monopoly Schematic

class Player:
    def __init__(self, initial_money, strategy_params):
        self.money = initial_money
        self.goojf = 0
        self.threshold = strategy_params[0]
        self.param2 = strategy_params[1]
        self.param3 = strategy_params[2]


class BoardLocation:
    def __init__(self, name, rent):
        self.name = name
        self.rent = rent



class Game:
    def CreateBoard(self):
        self.board = [] #list of board locations.
        self.board.append(BoardLocation("Park Place",35))
        self.board.append(BoardLocation("Boardwalk", 50))

    def CreatePlayerList(self, player_strategy_list):
        self.player_list = [Player(500,player_strategy_list[i]) for i in range(len(player_strategy_list))] #list of player objects

    def PlayGame(self):
        print("Playing Game . . .")

    def __init__(self, player_strategy_list):
        self.CreateBoard()
        self.CreatePlayerList(player_strategy_list)

##player1 = Player(100,(200,0.5,1))
##print("player1.threshold = " + str(player1.threshold))

game1 = Game([(200,0.5,1),(300,0.75,2)])
print("player1.threshold = " + str(game1.player_list[0].threshold))
game1.player_list[0].threshold = 700
print("player1.threshold = " + str(game1.player_list[0].threshold))
print("player2.threshold = " + str(game1.player_list[1].threshold))
print("player2.param2 = " + str(game1.player_list[1].param2))
print("game1.boardlocation2.name = " + str(game1.board[1].name))
