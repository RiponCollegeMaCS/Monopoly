# # # # # # # # # # # # # # # #
# Monopoly Simulator          #
# [NO MONEY!]                 #
# Created by Mitchell Eithun  #
# July 2014                   #
# # # # # # # # # # # # # # # #

# Import various commands.
from random import shuffle, randint  # The randint, shuffle functions.


# Define the Player class.
class Player:
    def __init__(self, number, jail_time=3):
        self.number = number
        self.position = 0  # The player starts on "Go".
        self.chance_card = False  # The player has no "Get Out of Jail Free" cards.
        self.community_chest_card = False  # The player has no "Get Out of Jail Free" cards.
        self.in_jail = False  # The player is not in jail.
        self.jail_time = jail_time
        self.jail_counter = 0  # The "turns in jail" counter.


# Define the Board_Location class.
class BoardLocation:
    def __init__(self, name, price=0, group="none", rents=(0, 0, 0, 0, 0, 0), house_cost=0):
        self.name = name
        self.visits = 0  # Hit counter.


# Define the Game class.
class Game:
    def __init__(self, list_of_players):
        self.create_board()  # Set-up the board.
        self.create_cards()  # Shuffle both card decks.
        self.number_of_players = len(list_of_players)
        self.players = list_of_players  # Create  a list of players.
        self.turn_counter = 0  # Reset turn counter.
        self.doubles_counter = 0  # Reset doubles counter.
        self.result = None

    def create_cards(self):
        self.chance_cards = [i for i in range(1, 17)]  # Create cards.
        self.community_chest_cards = [i for i in range(1, 17)]  # Create cards.
        shuffle(self.chance_cards)  # Shuffle cards.
        shuffle(self.community_chest_cards)  # Shuffle cards.
        self.chance_index = 0  # Reset index.
        self.community_chest_index = 0  # Reset index.

    # Creates a BoardLocation object for each space on the board.
    def create_board(self):
        self.board = []  # List of board locations.
        # "Name", Price, "Group", (Rents), House Cost
        self.board.append(BoardLocation("Go"))
        self.board.append(BoardLocation("Mediterranean Avenue", 60, "Brown", (2, 10, 30, 90, 160, 250), 50))
        self.board.append(BoardLocation("Community Chest"))
        self.board.append(BoardLocation("Baltic Avenue", 60, "Brown", (4, 20, 60, 180, 320, 450), 50))
        self.board.append(BoardLocation("Income Tax"))
        self.board.append(BoardLocation("Reading Railroad", 200, "Railroad"))
        self.board.append(BoardLocation("Oriental Avenue", 100, "Light Blue", (6, 30, 90, 270, 400, 550), 50))
        self.board.append(BoardLocation("Chance"))
        self.board.append(BoardLocation("Vermont Avenue", 100, "Light Blue", (6, 30, 90, 270, 400, 550), 50))
        self.board.append(BoardLocation("Connecticut Avenue", 120, "Light Blue", (8, 40, 100, 300, 450, 600), 50))
        self.board.append(BoardLocation("Just Visiting / In Jail"))
        self.board.append(BoardLocation("St. Charles Place", 140, "Purple", (10, 50, 150, 450, 625, 750), 100))
        self.board.append(BoardLocation("Electric Company", 150))
        self.board.append(BoardLocation("States Avenue", 140, "Purple", (10, 50, 150, 450, 625, 750), 100))
        self.board.append(BoardLocation("Virginia Avenue", 160, "Purple", (12, 60, 180, 500, 700, 900), 100))
        self.board.append(BoardLocation("Pennsylvania Railroad", 200))
        self.board.append(BoardLocation("St. James Place", 180, "Orange", (14, 70, 200, 550, 750, 950), 100))
        self.board.append(BoardLocation("Community Chest"))
        self.board.append(BoardLocation("Tennessee Avenue", 180, "Orange", (14, 70, 200, 550, 750, 950), 100))
        self.board.append(BoardLocation("New York Avenue", 200, "Orange", (16, 80, 220, 600, 800, 1000), 100))
        self.board.append(BoardLocation("Free Parking"))
        self.board.append(BoardLocation("Kentucky Avenue", 220, "Red", (18, 90, 250, 700, 875, 1050), 150))
        self.board.append(BoardLocation("Chance"))
        self.board.append(BoardLocation("Indiana Avenue", 220, "Red", (18, 90, 250, 700, 875, 1050), 150))
        self.board.append(BoardLocation("Illinois Avenue", 240, "Red", (20, 100, 300, 750, 925, 1100), 150))
        self.board.append(BoardLocation("B. & O. Railroad", 200, "Railroad"))
        self.board.append(BoardLocation("Atlantic Avenue", 260, "Yellow", (22, 110, 330, 800, 975, 1150), 150))
        self.board.append(BoardLocation("Ventnor Avenue", 260, "Yellow", (22, 110, 330, 800, 975, 1150), 150))
        self.board.append(BoardLocation("Water Works", 150, "Utility"))
        self.board.append(BoardLocation("Marvin Gardens", 280, "Yellow", (24, 120, 360, 850, 1025, 1200), 150))
        self.board.append(BoardLocation("Go to Jail"))
        self.board.append(BoardLocation("Pacific Avenue", 300, "Green", (26, 130, 390, 900, 1100, 1275), 200))
        self.board.append(BoardLocation("North Carolina Avenue", 300, "Green", (26, 130, 390, 900, 1100, 1275), 200))
        self.board.append(BoardLocation("Community Chest"))
        self.board.append(BoardLocation("Pennsylvania Avenue", 320, "Green", (28, 150, 450, 1000, 1200, 1400), 200))
        self.board.append(BoardLocation("Short Line Railroad", 200, "Railroad"))
        self.board.append(BoardLocation("Chance"))
        self.board.append(BoardLocation("Park Place", 350, "Dark Blue", (35, 175, 500, 1100, 1300, 1500), 200))
        self.board.append(BoardLocation("Luxury Tax"))
        self.board.append(BoardLocation("Boardwalk", 400, "Dark Blue", (50, 200, 600, 1400, 1700, 2000), 200))

    # Defines the actions of the Community Chest cards.
    def community_chest(self, player):
        card = self.community_chest_cards[self.community_chest_index]
        if card == 1:  # GET OUT OF JAIL FREE
            player.community_chest_card = True  # Give the card to the player.
            #self.community_chest_cards.remove(1)  # Remove the card from the list
        elif card == 10:  # ADVANCE TO GO (COLLECT $200)
            self.move_to(player, 0)  # Player moves to Go.
        elif card == 16:  # GO TO JAIL
            self.go_to_jail(player)  # Send player to jail.

        self.community_chest_index = (self.community_chest_index + 1) % len(
            self.community_chest_cards)  # Increase index.

    # Defines the actions of the Chance cards.
    def chance(self, player):
        card = self.chance_cards[self.chance_index]
        if card == 1:  # GET OUT OF JAIL FREE
            player.chance_card = True  # Give the card to the player.
            #self.chance_cards.remove(1)  # Remove the card from the list
        elif card == 2:  # GO DIRECTLY TO JAIL
            self.go_to_jail(player)  # Send player to jail.
        elif card == 4:  # GO BACK 3 SPACES
            player.position -= 3  # Move player.
            self.board[player.position].visits += 1  # Increase hit counter.
            self.board_action(player, self.board[player.position])
        elif card == 5 or card == 11:  # ADVANCE TOKEN TO THE NEAREST RAILROAD
            if player.position == 7:
                self.move_to(player, 15)
            elif player.position == 22:
                self.move_to(player, 25)
            elif player.position == 36:
                self.move_to(player, 5)
            self.board_action(player, self.board[player.position])
        elif card == 6:  # ADVANCE TO GO (COLLECT $200)
            self.move_to(player, 0)  # Player moves to Go.
        elif card == 7:  # ADVANCE TO ILLINOIS AVE.
            self.move_to(player, 24)
            self.board_action(player, self.board[player.position])
        elif card == 9:  # ADVANCE TO ST. CHARLES PLACE
            self.move_to(player, 11)
            self.board_action(player, self.board[player.position])
        elif card == 10:  # ADVANCE TOKEN TO NEAREST UTILITY
            if player.position == 7:
                self.move_to(player, 12)
            elif player.position == 22:
                self.move_to(player, 28)
            elif player.position == 36:
                self.move_to(player, 12)
            self.board_action(player, self.board[player.position])
        elif card == 13:  # TAKE A RIDE ON THE READING RAILROAD
            self.move_to(player, 5)
            self.board_action(player, self.board[player.position])
        elif card == 14:  # ADVANCE TOKEN TO BOARD WALK [sic.]
            self.move_to(player, 39)
            self.board_action(player, self.board[player.position])

        self.chance_index = (self.chance_index + 1) % len(self.chance_cards)  # Increase index.

    # Moves a player ahead.
    def move_ahead(self, player, number_of_spaces):
        new_position = (player.position + number_of_spaces) % 40
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Moves a player to a specific spot.
    def move_to(self, player, new_position):
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Sends a player to jail.
    def go_to_jail(self, player):
        player.position = 10  # Move player.
        self.board[10].visits += 1  # Increase hit counter.
        player.in_jail = True  # Set the player's Jail status to true.


    # Decide what the player should do on a given board space.
    def board_action(self, player, board_space):
        if board_space.name == "Chance":
            self.chance(player)  # Draw card and make action.

        elif board_space.name == "Community Chest":
            self.community_chest(player)  # Draw card and make action.

        elif board_space.name == "Go to Jail":
            self.go_to_jail(player)  # The player goes to jail.

        else:  # The player landed on something else..
            pass


    # An individual player takes a turn.
    def take_turn(self, player):
        self.turn_counter += 1  # Increase turn counter
        self.doubles_counter = 0  # Reset doubles counter.

        # Roll the dice.
        die1 = randint(1, 6)
        die2 = randint(1, 6)

        # Is the player in jail?
        if player.in_jail:  # Player is in jail.
            player.jail_counter += 1  # Increase the jail turn counter.
            if die1 == die2:  # The player rolled doubles.
                player.jail_counter = 0  # Reset the jail counter.
                self.move_again = True  # The player can move out of jail
            else:  # The player didn't roll doubles.
                if player.jail_counter == player.jail_time:  # The player used their attempts.
                    player.jail_counter = 0  # Reset the jail counter.
                    self.move_again = True  # The player can move.
                    if player.chance_card:
                        player.chance_card = False  # The player uses his Chance GOOJF card.
                        #self.chance_cards.append(1)  # Add the card back into the list.
                    elif player.community_chest_card:
                        player.community_chest_card = False  # The player uses his Community Chest GOOJF card.
                        #self.community_chest_cards.append(1)  # Add the card back into the list.
                    else:
                        pass  # The player pats $50 to get out.
                else:
                    self.move_again = False  # The player can not move around the board.
        else:  # The player is not in jail.
            self.move_again = True  # The player can roll and move.

        # The main loop.
        while self.move_again:
            # Roll again for doubles.
            if self.doubles_counter > 0:
                die1 = randint(1, 6)
                die2 = randint(1, 6)

            # Check for doubles.
            if die1 == die2 and player.in_jail == False:
                self.doubles_counter += 1  # Increase the doubles counter.
                if self.doubles_counter == 3:  # The players is speeding.
                    self.go_to_jail(player)
                    return  # The function ends.
                else:  # The player is not speeding.
                    self.move_again = True  # The player rolled doubles.
            else:
                player.in_jail = False  # The player is no longer in jail.
                self.move_again = False  # The player did not roll doubles.

            # Move the player
            self.move_ahead(player, die1 + die2)

            # Find the current board space.
            board_space = self.board[player.position]

            # Make an action based on the current board space.
            self.board_action(player, board_space)

            # If a card or board space brought the player to jail, end the function.
            if player.in_jail:
                return

    # Provides the current status of the game, "live" or "done".
    def update_status(self):
        if self.turn_counter == 10000000:
            self.game_status = "done"
            self.result = 0

    # Plays a game object.
    def play(self):
        # Shuffle the players.
        playing_order = [player_number for player_number in range(1, self.number_of_players + 1)]
        shuffle(playing_order)

        # Initial conditions.
        self.game_status = "live"
        current_player_index = 0

        # Game loop.
        while self.game_status == "live":
            self.take_turn(self.players[playing_order[current_player_index] - 1])  # Current player takes turn.
            current_player_index = (current_player_index + 1) % (self.number_of_players)  # Update current_player_index.
            self.update_status()  # Update game status.

        # Ending report.
        hits = []
        for board_space in self.board:
            hits.append(board_space.visits)

        return hits


# main
def main():
    game1 = Game([Player(number=1, jail_time=3), Player(number=2, jail_time=3)])
    results = game1.play()
    print(results)


main()
