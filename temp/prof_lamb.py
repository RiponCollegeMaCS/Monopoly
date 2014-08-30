# # # # # # # # # # # # # # # #
# Monopoly Simulator          #
# Created by Mitchell Eithun  #
# July 2014                   #
# # # # # # # # # # # # # # # #

# Import various commands.
from random import shuffle, randint, choice  # The randint, shuffle and choice functions.
from decimal import *  # The Decimal module for better rounding.
from statistics import mean  # The mean function.
import csv  # The csv module to output results.
import time  # Timer function

# Adjust the rounding scheme.
getcontext().rounding = ROUND_HALF_UP

# Timer.
timeList = []
def timer():
    timeList.append(time.time())
    if len(timeList) % 2 == 0:
        print('Time elapsed: ' + str(round(timeList[-1] - timeList[-2], 4)) + ' seconds.')
        timeList.pop()
        timeList.pop()


# Define the Player class.
class Player:
    def __init__(self, number, strategy):
        self.number = number
        self.position = 0  # The player starts on "Go".
        self.money = 1500  # The player starts with $1,500.
        self.chance_card = False  # The player has no "Get Out of Jail Free" cards.
        self.community_chest_card = False  # The player has no "Get Out of Jail Free" cards.
        self.in_jail = False  # The player is not in jail.
        self.buying_threshold = strategy[0]  # The player's primary strategy parameter.
        self.development_threshold = strategy[1]
        self.jail_time = 3  # = strategy[2]
        self.jail_counter = 0  # The "turns in jail" counter.
        self.card_rent = False
        self.monopolies = []  # A list of the player's monopolies.


# Define the Board_Location class.
class BoardLocation:
    def __init__(self, name, price=0, group="none", rents=(0, 0, 0, 0, 0, 0), house_cost=0):
        self.name = name  # The name of the board location.
        self.price = price  # How much it costs to buy the property.
        self.rents = rents  # The various rents.
        self.house_cost = house_cost  # How much it costs for a house.
        self.group = group  # Which group the property belongs to.
        self.buildings = 0  # The property starts with development.
        self.owner = 0  # The property is initially unowned.
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
        self.houses = 32  # House supply.
        self.hotels = 12  # Hotel supply.
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
            self.community_chest_cards.remove(1)  # Remove the card from the list
        elif card == 2:  # PAY SCHOOL TAX OF $150
            self.change_money(player, -150)
        elif card == 3:  # COLLECT $50 FROM EVERY PLAYER
            for individual in self.players:  # For each player...
                self.change_money(individual, -50)  # Take away $50.
                self.change_money(player, 50)  # Give the $50 to the player.
        elif card == 4:  # XMAS FUND MATURES / COLLECT $100
            self.change_money(player, 100)
        elif card == 5:  # INCOME TAX REFUND / COLLECT $20
            self.change_money(player, 20)
        elif card == 6:  # YOU INHERIT $100
            self.change_money(player, 100)
        elif card == 7:  # YOU HAVE WON SECOND PRIZE IN A BEAUTY CONTEST / COLLECT $10
            self.change_money(player, 10)
        elif card == 8:  # BANK ERROR IN YOUR FAVOR / COLLECT $200
            self.change_money(player, 200)
        elif card == 9:  # RECEIVE FOR SERVICES $25
            self.change_money(player, 25)
        elif card == 10:  # ADVANCE TO GO (COLLECT $200)
            self.move_to(player, 0)  # Player moves to Go.
        elif card == 11:  # YOU ARE ASSESSED FOR STREET REPAIRS
            house_counter = 0
            hotel_counter = 0
            for board_space in self.board:  # Cycle through all board spaces.
                if board_space.owner == player.number:  # If the player owns the property...
                    if board_space.buildings == 5:
                        hotel_counter += 1  # Add hotels.
                    else:
                        house_counter += board_space.buildings  # Add houses.
            house_repairs = 40 * house_counter  # $40 PER HOUSE
            hotel_repairs = 115 * hotel_counter  # $115 PER HOTEL
            self.change_money(player, house_repairs + hotel_repairs)
        elif card == 12:  # LIFE INSURANCE MATURES / COLLECT $100
            self.change_money(player, 100)
        elif card == 13:  # DOCTOR'S FEE / PAY $50
            self.change_money(player, 50)
        elif card == 14:  # FROM SALE OF STOCK / YOU GET $45
            self.change_money(player, 45)
        elif card == 15:  # PAY HOSPITAL $100
            self.change_money(player, 100)
        elif card == 16:  # GO TO JAIL
            self.go_to_jail(player)  # Send player to jail.

        self.community_chest_index = (self.community_chest_index + 1) % len(
            self.community_chest_cards)  # Increase index.

    # Defines the actions of the Chance cards.
    def chance(self, player):
        card = self.chance_cards[self.chance_index]
        if card == 1:  # GET OUT OF JAIL FREE
            player.chance_card = True  # Give the card to the player.
            self.chance_cards.remove(1)  # Remove the card from the list
        elif card == 2:  # GO DIRECTLY TO JAIL
            self.go_to_jail(player)  # Send player to jail.
        elif card == 3:  # YOUR BUILDING LOAN MATURES / COLLECT $150
            self.change_money(player, 150)
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
            player.card_rent = True
            self.board_action(player, self.board[player.position])
        elif card == 6:  # ADVANCE TO GO (COLLECT $200)
            self.move_to(player, 0)  # Player moves to Go.
        elif card == 7:  # ADVANCE TO ILLINOIS AVE.
            self.move_to(player, 24)
            self.board_action(player, self.board[player.position])
        elif card == 8:  # MAKE GENERAL REPAIRS ON ALL YOUR PROPERTY
            house_counter = 0
            hotel_counter = 0
            for board_space in self.board:  # Cycle through all board spaces.
                if board_space.owner == player.number:  # If the player owns the property...
                    if board_space.buildings == 5:
                        hotel_counter += 1  # Add hotels.
                    else:
                        house_counter += board_space.buildings  # Add houses.
            house_repairs = 45 * house_counter  # $45 PER HOUSE
            hotel_repairs = 100 * hotel_counter  # $100 PER HOTEL
            self.change_money(player, house_repairs + hotel_repairs)
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
            player.card_rent = True
            self.board_action(player, self.board[player.position])
        elif card == 12:  # PAY POOR TAX OF $15
            self.change_money(player, -15)
        elif card == 13:  # TAKE A RIDE ON THE READING RAILROAD
            self.move_to(player, 5)
            self.board_action(player, self.board[player.position])
        elif card == 14:  # ADVANCE TOKEN TO BOARD WALK [sic.]
            self.move_to(player, 39)
            self.board_action(player, self.board[player.position])
        elif card == 15:  # PAY EACH PLAYER $50
            for individual in self.players:  # For each player...
                self.change_money(individual, 50)  # Add $50.
                self.change_money(player, -50)  # Take $50 from the player.
        elif card == 16:  # BANK PAYS YOU DIVIDEND OF $50
            self.change_money(player, 50)

        self.chance_index = (self.chance_index + 1) % len(self.chance_cards)  # Increase index.

    # Moves a player ahead.
    def move_ahead(self, player, number_of_spaces):
        new_position = (player.position + number_of_spaces) % 40
        if new_position < player.position:  # Does the player pass Go?
            self.change_money(player, 200)  # The player collects $200 for passing Go.
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Moves a player to a specific spot.
    def move_to(self, player, new_position):
        if new_position < player.position:  # Does the player pass Go?
            self.change_money(player, 200)  # The player collects $200 for passing Go.
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Sends a player to jail.
    def go_to_jail(self, player):
        player.position = 10  # Move player.
        self.board[10].visits += 1  # Increase hit counter.
        player.in_jail = True  # Set the player's Jail status to true.

    # Has a player buy a property.
    def buy_property(self, player, board_space):
        board_space.owner = player.number  # Change property status.
        self.change_money(player, -board_space.price)  # Pay the money for the property.
        if self.monopoly_status(player, board_space):
            player.monopolies.append(board_space.group)

    # The player passed through pays rent to the player who owns the property.
    def pay_rent(self, player, diceroll):
        # Find the property.
        current_property = self.board[player.position]

        # Find the owner of the property.
        owner = self.players[current_property.owner - 1]

        # Rent for Railroads.
        if current_property.group == "Railroad":
            railroad_counter = 0
            for railroad_number in range(5, 40, 10):
                if self.board[railroad_number].owner == owner.number:
                    railroad_counter += 1  # Count the number of RRs.
            rent = 25 * railroad_counter  # The rent is $25 times the number of RRs.
            if player.card_rent:  # Rent is double for the railroad cards.
                rent *= 2

        # Rent for Utilities.
        elif current_property.group == "Utility":
            if self.board[12].owner == owner.number == self.board[28].owner:
                rent = diceroll * 10  # If the player owns both utilities, pay 10 times the dice.
            else:
                if player.card_rent:
                    rent = diceroll * 10
                else:
                    rent = diceroll * 4  # If the player owns one utility, pay 4 times the dice.


        # Rent for color-group properties.
        else:
            if current_property.buildings == 5:  # Check to see if there is a hotel.
                rent = current_property.rents[5]  # Pay the 5th rent for a hotel.
            elif current_property.buildings > 0 and current_property.buildings < 5:  # The property has houses.
                rent = current_property.rents[current_property.buildings]
            else:
                if current_property.group in owner.monopolies:  # If the player has a monopoly...
                    rent = current_property.rents[0] * 2  # Rent is doubled.
                else:
                    rent = current_property.rents[0]


        # Pay the rent.
        self.change_money(player, -rent)  # The player pays rent.
        self.change_money(owner, rent)  # The property owner receives rent.

    # Sell back one house or hotel on a property or sell all buildings back.
    def sell_building(self, player, property, building):
        if building == "house":
            property.buildings -= 1
            self.houses += 1
            player.money += property.house_cost / 2
        elif building == "hotel":
            property.buildings -= 1
            self.hotels += 1
            self.houses -= 4
            player.money += property.house_cost / 2
        elif building == "all":
            if property.buildings == 5:
                property.buildings = 0
                self.hotels += 1
                player.money += (property.house_cost / 2) * 5
            else:
                self.houses += property.buildings
                player.money += (property.house_cost / 2) * property.buildings
                property.buildings = 0

    # Changes a player's money total. Sells buildings and then mortgages properties to make funds.
    def change_money(self, player, increment):
        player.money += increment  # Change the player's money.

        # The player's money total is negative.
        if player.money <= 0:
            keep_selling = True
            # Sell houses and hotels to make funds.
            while keep_selling:
                keep_selling = False
                if player.monopolies:
                    for board_space in self.board:
                        if board_space.buildings > 0:  # It has buildings.
                            if board_space.group in player.monopolies:  # It's in the player's monopoly.
                                if self.even_selling_test(board_space):  # Building "evenly".
                                    keep_selling = True
                                    if board_space.buildings == 5:  # It's a hotel.
                                        if self.houses >= 4:  # Hotel - > 4 Houses
                                            self.sell_building(player, board_space, "hotel")
                                        else:  # Not enough houses to break hotel.
                                            for board_space2 in self.board:
                                                if board_space2.group == board_space.group:
                                                    self.sell_building(player, board_space2, "all")
                                    else:  # It's a house.
                                        self.sell_building(player, board_space, "house")
                                    if player.money > 0:  # The player is out of the hole.
                                        return  # Exit
            # Mortgage properties.
            for board_space in self.board:  # Cycle through all board spaces.
                if board_space.owner == player.number and board_space.buildings == 0:
                    mortgage_value = board_space.price / 2
                    player.money += mortgage_value  # Gain the mortgage value.
                    board_space.owner *= -1  # Mortgage property.
                    if board_space.group in player.monopolies:  # Update monopoly status.
                        player.monopolies.remove(board_space.group)
                    if player.money > 0:  # The player is out of the hole.
                        return  # Exit function.

    # Decides if the player is building evenly or not.
    def even_selling_test(self, property):
        test_result = True
        for board_space in self.board:
            if board_space.group == property.group:
                if board_space.buildings - property.buildings > 0:
                    test_result = False
        return test_result

    # Decides if the player is building evenly or not.
    def even_building_test(self, property):
        test_result = True
        for board_space in self.board:
            if board_space.group == property.group:
                if property.buildings - board_space.buildings > 0:
                    test_result = False
        return test_result

    # Un-mortgage and then buy houses/hotels.
    def develop_properties(self, player):
        # First, un-mortgage properties, if possible
        for board_space in self.board:  # Cycle through all board spaces.
            if board_space.owner == -player.number:
                unmortgage_price = int(round(Decimal(str(1.1 * (board_space.price / 2))), 0))
                if player.money - unmortgage_price >= player.buying_threshold:
                    player.money -= unmortgage_price  # Pay un-mortgage price.
                    board_space.owner *= -1  # Un-mortgage property.
                    if self.monopoly_status(player, board_space):
                        player.monopolies.append(board_space.group)
                else:
                    return  # Exit if the player doesn't have enough money to continue.

        # Then, build houses and hotels, if possible.
        if player.monopolies:
            keep_building = True  # Initial condition.
            while keep_building:
                keep_building = False  # Don't keep building unless something is bought.
                for board_space in self.board:
                    if board_space.group in player.monopolies:  # It's in a monopoly.
                        if player.money - board_space.house_cost >= player.development_threshold:  # Strategy param.
                            if self.even_building_test(board_space):  # Building "evenly".
                                if board_space.buildings < 4:  # Ready for a house.
                                    building_supply = self.houses
                                    building = "house"
                                elif board_space.buildings == 4:  # Ready for a hotel.
                                    building_supply = self.hotels
                                    building = "hotel"
                                else:
                                    building_supply = 0
                                if building_supply > 0:  # There's a building available.
                                    if building == "house":
                                        self.houses -= 1  # Take 1 house.
                                    elif building == "hotel":
                                        self.hotels -= 1  # Take 1 hotel.
                                        self.houses += 4  # Put back 4 houses.
                                    player.money -= board_space.house_cost  # Pay building cost.
                                    board_space.buildings += 1  # Add building to property.
                                    keep_building = True

    # Determines if the player owns all of the properties in the the given property's group.
    def monopoly_status(self, player, current_property):
        # Find the name of the property's group.
        group = current_property.group

        if group in ["", "Railroad", "Utility"]:
            return False  # The property is not in a color group.

        # Count how many properties in the group that player owns.
        property_counter = 0
        for board_space in self.board:  # Cycle through all board spaces.
            if board_space.group == group and board_space.owner == player.number:
                property_counter += 1

        if property_counter == 3:
            return True  # The property is in a monopoly and a group of three.
        elif property_counter == 2 and group in ["Dark Blue", "Brown"]:
            return True  # The property is in a monopoly and a group of two.
        else:
            return False  # The player doesn't have a monopoly.

    # Decide what the player should do on a given board space.
    def board_action(self, player, board_space, diceroll=0):
        if board_space.name in ["Go", "Just Visiting / In Jail", "Free Parking"]:
            pass  # Nothing happens.

        elif board_space.name == "Income Tax":
            liquid_property = 0  # The liquidated property wealth of the player.
            for board_space in self.board:  # Cycle through all board spaces.
                if board_space.owner == player.number:  # If the player owns the property...
                    liquid_property += board_space.price  # Add the price of the property.

            liquid_buildings = 0  # The cost of all buildings the player owns.
            for board_space in self.board:  # Cycle through all board spaces.
                if board_space.owner == player.number:  # If the player owns the property...
                    liquid_buildings += board_space.buildings * board_space.house_cost  # Add the price of the buildings.

            all_assets = player.money + liquid_property + liquid_buildings
            # The pays either $200 or 10% of all assets.
            self.change_money(player, -min(200, int(round(Decimal(str(0.1 * all_assets)), 0))))

        elif board_space.name == "Chance":
            self.chance(player)  # Draw card and make action.

        elif board_space.name == "Community Chest":
            self.community_chest(player)  # Draw card and make action.

        elif board_space.name == "Go to Jail":
            self.go_to_jail(player)  # The player goes to jail.

        elif board_space.name == "Luxury Tax":
            self.change_money(player, -75)  # The player pays $75.

        else:  # The player landed on a property.
            if board_space.owner == player.number:
                pass  # The player owns the property. Nothing happens.
            elif board_space.owner < 0:
                pass  # The property is mortgaged. Nothing happens.
            elif board_space.owner == 0:  # The property is unowned.
                if player.money - board_space.price >= player.buying_threshold:
                    self.buy_property(player, board_space)  # The player buys the property.
                else:
                    pass  # The property is auctioned.
            else:  # C The property is owned by another player.
                self.pay_rent(player, diceroll)  # The player pays the owner rent.

        # Reset this variable.
        player.card_rent = False

    # An individual player takes a turn.
    def take_turn(self, player):
        self.turn_counter += 1  # Increase turn counter
        self.doubles_counter = 0  # Reset doubles counter.

        # Check to see if properties can be un-mortgaged or houses and hotel and can be purchased.
        self.develop_properties(player)

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
                        self.chance_cards.append(1)  # Add the card back into the list.
                    elif player.community_chest_card:
                        player.community_chest_card = False  # The player uses his Community Chest GOOJF card.
                        self.community_chest_cards.append(1)  # Add the card back into the list.
                    else:
                        self.change_money(player, -50)  # The player pats $50 to get out.
                else:
                    self.move_again = False  # The player can not move around the board.
        else:  # The player is not in jail.
            self.move_again = True  # The player can roll and move.

        # The main loop.
        while self.move_again and player.money > 0:
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
            self.board_action(player, board_space, die1 + die2)

            # If a card or board space brought the player to jail, end the function.
            if player.in_jail:
                return

    # Provides the current status of the game, "live" or "done".
    def update_status(self):
        for single_player in self.players:
            if single_player.money <= 0:
                self.game_status = "done"
                if single_player.number == 1:
                    self.result = -1
                elif single_player.number == 2:
                    self.result = 1

        if self.turn_counter == 1000:
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
        return self.result


# main
from statistics import stdev
def main():
    success_list = []
    for j in range(1):
        rand_params = [randint(1, 500), randint(1, 500)]
        fixed_params = [1,1]
        results_list = []
        for i in range(100):
            player0 = Player(1, fixed_params)
            opponent = Player(2, [randint(1, 500), randint(1, 500)])
            current_game = Game([player0, opponent])
            results_list.append(current_game.play())
        success_list.append(mean(results_list))
    print(success_list)
    #print("Standard Deviation = " + str(stdev(success_list)))

timer()
main()
timer()
