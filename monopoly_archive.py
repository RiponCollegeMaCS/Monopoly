# # # # # # # # # # # # # # # #
# Monopoly Simulator          #
# Created by Mitchell Eithun  #
# July/August 2014            #
# # # # # # # # # # # # # # # #

# Import various commands.
from random import *  # The randint, shuffle and choice functions.
from decimal import *  # The Decimal module for better rounding.

# Adjust the rounding scheme.
getcontext().rounding = ROUND_HALF_UP

# Define the Player class.
class Player:
    def __init__(self, number, buying_threshold=100, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                 complete_monopoly=0, group_preferences=(), development_threshold=0):
        self.number = number
        self.reset_values()

        # Strategy parameters.
        self.group_preferences = group_preferences
        self.development_threshold = development_threshold
        self.init_jail_time = jail_time
        self.jail_time = jail_time
        self.smart_jail_strategy = smart_jail_strategy
        self.building_threshold = building_threshold
        self.complete_monopoly = complete_monopoly
        self.buying_threshold = buying_threshold

    # Reset a player's parameters so the same player can play in a series of games.
    def reset_values(self):
        self.success_indicator = 0
        self.position = 0  # The player starts on "Go".
        self.money = 1500  # The player starts with $1,500.
        self.chance_card = False  # The player has no "Get Out of Jail Free" cards.
        self.community_chest_card = False  # The player has no "Get Out of Jail Free" cards.
        self.in_jail = False  # The player is not in jail.
        self.jail_counter = 0  # The "turns in jail" counter.
        self.card_rent = False
        self.monopolies = []  # A list of the player's monopolies.
        self.auction_bid = 0
        self.passed_go = False
        self.inventory = []  # A list of the player's properties.
        self.bid_includes_mortgages = False


# Define the Board_Location class.
class BoardLocation:
    def __init__(self, id, name, price=0, group="none", rents=(0, 0, 0, 0, 0, 0), house_cost=0):
        self.id = id
        self.name = name  # The name of the board location.
        self.price = price  # How much it costs to buy the property.
        self.rents = rents  # The various rents.
        self.house_cost = house_cost  # How much it costs for a house.
        self.group = group  # Which group the property belongs to.
        self.buildings = 0  # The property starts with development.
        self.visits = 0  # Hit counter.
        self.mortgaged = False


# Define the Game class.
class Game:
    def __init__(self, list_of_players, auctions_enabled=True, free_parking_pool=False,
                 double_on_go=False, no_rent_in_jail=False, trip_to_start=False, snake_eyes_bonus=False, cutoff=300):
        self.game_status = "live"  # Current status of the game.
        self.create_board()  # Set-up the board.
        self.create_cards()  # Shuffle both card decks.
        self.number_of_players = len(list_of_players)  # The number of players.
        self.players = list_of_players  # Create  a list of players.
        self.turn_counter = 0  # Reset turn counter.
        self.doubles_counter = 0  # Reset doubles counter.
        self.houses = 32  # House supply.
        self.hotels = 12  # Hotel supply.
        self.result = 99  # Ending game data
        self.dice_roll = 0  # The current dice roll can be accessible everywhere.
        self.auctions_enabled = auctions_enabled  # A toggle to disable auctions.
        self.first_building = False  # Records whether a building has been bought for smart_jail_strategy
        self.cutoff = cutoff  # Determines when a game should be terminated.

        # Attributes for house rules.
        self.free_parking_pool = free_parking_pool
        self.money_in_fp = 0
        self.double_on_go = double_on_go
        self.no_rent_in_jail = no_rent_in_jail
        self.trip_to_start = trip_to_start
        self.snake_eyes_bonus = snake_eyes_bonus

    # Create list of numbers to represent Chance and Community Chest cards.
    def create_cards(self):
        self.chance_cards = [i for i in range(1, 16 + 1)]  # Create cards.
        self.community_chest_cards = [i for i in range(1, 16 + 1)]  # Create cards.
        shuffle(self.chance_cards)  # Shuffle cards.
        shuffle(self.community_chest_cards)  # Shuffle cards.
        self.chance_index = 0  # Reset index.
        self.community_chest_index = 0  # Reset index.

    # Creates a BoardLocation object for each space on the board.
    def create_board(self):
        self.board = []  # List of board locations.
        # "Name", Price, "Group", (Rents), House Cost
        self.board.append(BoardLocation(0, "Go"))
        self.board.append(BoardLocation(1, "Mediterranean Ave.", 60, "Brown", (2, 10, 30, 90, 160, 250), 50))
        self.board.append(BoardLocation(2, "Community Chest"))
        self.board.append(BoardLocation(3, "Baltic Ave.", 60, "Brown", (4, 20, 60, 180, 320, 450), 50))
        self.board.append(BoardLocation(4, "Income Tax"))
        self.board.append(BoardLocation(5, "Reading Railroad", 200, "Railroad"))
        self.board.append(BoardLocation(6, "Oriental Ave.", 100, "Light Blue", (6, 30, 90, 270, 400, 550), 50))
        self.board.append(BoardLocation(7, "Chance"))
        self.board.append(BoardLocation(9, "Vermont Ave.", 100, "Light Blue", (6, 30, 90, 270, 400, 550), 50))
        self.board.append(BoardLocation(10, "Connecticut Ave.", 120, "Light Blue", (8, 40, 100, 300, 450, 600), 50))
        self.board.append(BoardLocation(11, "Just Visiting / In Jail"))
        self.board.append(BoardLocation(12, "St. Charles Place", 140, "Pink", (10, 50, 150, 450, 625, 750), 100))
        self.board.append(BoardLocation(13, "Electric Company", 150, "Utility"))
        self.board.append(BoardLocation(14, "States Ave.", 140, "Pink", (10, 50, 150, 450, 625, 750), 100))
        self.board.append(BoardLocation(15, "Virginia Ave.", 160, "Pink", (12, 60, 180, 500, 700, 900), 100))
        self.board.append(BoardLocation(16, "Pennsylvania Railroad", 200, "Railroad"))
        self.board.append(BoardLocation(17, "St. James Place", 180, "Orange", (14, 70, 200, 550, 750, 950), 100))
        self.board.append(BoardLocation(18, "Community Chest"))
        self.board.append(BoardLocation(19, "Tennessee Ave.", 180, "Orange", (14, 70, 200, 550, 750, 950), 100))
        self.board.append(BoardLocation(20, "New York Ave.", 200, "Orange", (16, 80, 220, 600, 800, 1000), 100))
        self.board.append(BoardLocation(21, "Free Parking"))
        self.board.append(BoardLocation(22, "Kentucky Ave.", 220, "Red", (18, 90, 250, 700, 875, 1050), 150))
        self.board.append(BoardLocation(23, "Chance"))
        self.board.append(BoardLocation(24, "Indiana Ave.", 220, "Red", (18, 90, 250, 700, 875, 1050), 150))
        self.board.append(BoardLocation(25, "Illinois Ave.", 240, "Red", (20, 100, 300, 750, 925, 1100), 150))
        self.board.append(BoardLocation(26, "B. & O. Railroad", 200, "Railroad"))
        self.board.append(BoardLocation(27, "Atlantic Ave.", 260, "Yellow", (22, 110, 330, 800, 975, 1150), 150))
        self.board.append(BoardLocation(28, "Ventnor Ave.", 260, "Yellow", (22, 110, 330, 800, 975, 1150), 150))
        self.board.append(BoardLocation(29, "Water Works", 150, "Utility"))
        self.board.append(BoardLocation(30, "Marvin Gardens", 280, "Yellow", (24, 120, 360, 850, 1025, 1200), 150))
        self.board.append(BoardLocation(31, "Go to Jail"))
        self.board.append(BoardLocation(32, "Pacific Ave.", 300, "Green", (26, 130, 390, 900, 1100, 1275), 200))
        self.board.append(BoardLocation(33, "North Carolina Ave.", 300, "Green", (26, 130, 390, 900, 1100, 1275), 200))
        self.board.append(BoardLocation(34, "Community Chest"))
        self.board.append(BoardLocation(35, "Pennsylvania Ave.", 320, "Green", (28, 150, 450, 1000, 1200, 1400), 200))
        self.board.append(BoardLocation(36, "Short Line Railroad", 200, "Railroad"))
        self.board.append(BoardLocation(37, "Chance"))
        self.board.append(BoardLocation(38, "Park Place", 350, "Dark Blue", (35, 175, 500, 1100, 1300, 1500), 200))
        self.board.append(BoardLocation(39, "Luxury Tax"))
        self.board.append(BoardLocation(40, "Boardwalk", 400, "Dark Blue", (50, 200, 600, 1400, 1700, 2000), 200))

        # Copy the board to create a linked list of unowned properties.
        self.unowned_properties = []
        self.unowned_properties.extend(self.board)

    # Defines the actions of the Community Chest cards.
    def community_chest(self, player):
        card = self.community_chest_cards[self.community_chest_index]
        if card == 1:  # GET OUT OF JAIL FREE
            player.community_chest_card = True  # Give the card to the player.
            self.community_chest_cards.remove(1)  # Remove the card from the list
        elif card == 2:  # PAY SCHOOL FEES OF $50 [UPDATED IN 2008]
            self.change_money(player, -50)
            self.money_in_fp += 50  # The pool gains the card fee.
        elif card == 3:  # IT IS YOUR BIRTHDAY. / COLLECT $10 / FROM EVERY PLAYER [UPDATED IN 2008]
            for individual in self.players:  # For each player...
                self.change_money(individual, -10)  # Take away $50.
                self.change_money(player, 10)  # Give the $50 to the player.
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
        elif card == 9:  # RECEIVE $25 / CONSULTANCY FEE [WORDING UPDATED IN 2008]
            self.change_money(player, 25)
        elif card == 10:  # ADVANCE TO GO (COLLECT $200)
            self.move_to(player, 0)  # Player moves to Go.
        elif card == 11:  # YOU ARE ASSESSED FOR STREET REPAIRS
            house_counter = 0
            hotel_counter = 0
            if player.monopolies:
                for board_space in player.inventory:  # Cycle through all board spaces.
                    if board_space.buildings == 5:
                        hotel_counter += 1  # Add hotels.
                    else:
                        house_counter += board_space.buildings  # Add houses.
                house_repairs = 40 * house_counter  # $40 PER HOUSE
                hotel_repairs = 115 * hotel_counter  # $115 PER HOTEL
                self.change_money(player, house_repairs + hotel_repairs)
                self.money_in_fp += house_repairs + hotel_repairs  # The pool gains the card fee.
        elif card == 12:  # LIFE INSURANCE MATURES / COLLECT $100
            self.change_money(player, 100)
        elif card == 13:  # DOCTOR'S FEE / PAY $50
            self.change_money(player, -50)
            self.money_in_fp += 50  # The pool gains the card fee.
        elif card == 14:  # FROM SALE OF STOCK / YOU GET $50 [UPDATED IN 2008]
            self.change_money(player, 50)
        elif card == 15:  # PAY HOSPITAL $100
            self.change_money(player, -100)
            self.money_in_fp += 100  # The pool gains the card fee.
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
            if player.monopolies:
                for board_space in player.inventory:  # Cycle through all board spaces.
                    if board_space.buildings == 5:
                        hotel_counter += 1  # Add hotels.
                    else:
                        house_counter += board_space.buildings  # Add houses.
            house_repairs = 45 * house_counter  # $45 PER HOUSE
            hotel_repairs = 100 * hotel_counter  # $100 PER HOTEL
            self.change_money(player, house_repairs + hotel_repairs)
            self.money_in_fp += house_repairs + hotel_repairs  # The pool gains the card fee.
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
            self.money_in_fp += 15  # The pool gains the card fee.
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
            player.passed_go = True
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Moves a player to a specific spot.(Used in cards.)
    def move_to(self, player, new_position):
        if new_position < player.position:  # Does the player pass Go?
            self.change_money(player, 200)  # The player collects $200 for passing Go.
            player.passed_go = True  # Parameter for house rule.
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Determines how a player gets out of jail: use a GOOJF or pay $50.
    def pay_out_of_jail(self, player):
        if player.chance_card:
            player.chance_card = False  # The player uses his Chance GOOJF card.
            self.chance_cards.append(1)  # Add the card back into the list.
        elif player.community_chest_card:
            player.community_chest_card = False  # The player uses his Community Chest GOOJF card.
            self.community_chest_cards.append(1)  # Add the card back into the list.
        else:
            self.change_money(player, -50)  # The player pats $50 to get out.

    # Sends a player to jail.
    def go_to_jail(self, player):
        player.position = 10  # Move player.
        self.board[10].visits += 1  # Increase hit counter.
        self.move_again = False  # Prevent the player from moving again.
        player.in_jail = True  # Set the player's Jail status to true.
        if player.smart_jail_strategy and self.first_building:
            player.jail_time = 3
        else:
            player.jail_time = player.init_jail_time

    # Has a player buy a property.
    def buy_property(self, player, board_space, custom_price=False):
        # Allows a property to buy at a custom price (used in auctions).
        if custom_price:
            self.change_money(player, -custom_price)  # Pay the money for the property.
        else:
            self.change_money(player, -board_space.price)  # Pay the money for the property.

        self.unowned_properties.remove(board_space)  # Remove the property from the list of unowned properties.
        player.inventory.append(board_space)  # Give it to the player for now.

        # If the player has a completed a monopoly, add it to the player's list of monopolies.
        if self.monopoly_status(player, board_space):
            player.monopolies.append(board_space.group)

    # Determine the owner of a property.
    def property_owner(self, property):
        for current_player in self.players:
            if property in current_player.inventory:
                return current_player

    # The player passed through pays rent to the player who owns the property the original player sits on..
    def pay_rent(self, player):
        # Find the property.
        current_property = self.board[player.position]

        # Find the owner of the property.
        owner = self.property_owner(current_property)

        # Exit if the owner is in jail and the "no rent in jail" house rule is in effect.
        if self.no_rent_in_jail and owner.in_jail:
            return

        # Rent for Railroads.
        if current_property.group == "Railroad":
            railroad_counter = 0
            for property in owner.inventory:
                if property.group == "Railroad":
                    railroad_counter += 1
            rent = 25 * pow(2, railroad_counter - 1)  # The rent.
            if player.card_rent:  # Rent is double for the railroad cards.
                rent *= 2

        # Rent for Utilities.
        elif current_property.group == "Utility":
            self.dice_roll = randint(1, 6) + randint(1, 6)  # Roll again.
            utility_counter = 0
            for property in owner.inventory:
                if property.group == "Utility":
                    utility_counter += 1
            if utility_counter == 2 or player.card_rent:
                rent = self.dice_roll * 10  # If the player owns both utilities, pay 10 times the dice.
            else:
                rent = self.dice_roll * 4  # If the player owns one utility, pay 4 times the dice.
        # Rent for color-group properties.
        else:
            if current_property.buildings == 5:  # Check to see if there is a hotel.
                rent = current_property.rents[5]  # Pay the 5th rent for a hotel.
            elif 0 < current_property.buildings < 5:  # The property has houses.
                rent = current_property.rents[current_property.buildings]
            else:
                if current_property.group in owner.monopolies:  # If the player has a monopoly...
                    rent = current_property.rents[0] * 2  # Rent is doubled.
                    '''# If a property in the monopoly is mortgaged, redefine the rent.
                    for group_property in owner.inventory:
                        if group_property.group == current_property.group and group_property.mortgaged:
                            rent = current_property.rents[0]'''
                else:  # The player does not have a monopoly.
                    rent = current_property.rents[0]

        # Pay the rent.
        self.change_money(player, -rent)  # The player pays rent.
        self.change_money(owner, rent)  # The property owner receives rent.

    # Calculate the cost to unmortgage a given property.
    def unmortgage_price(self, property):
        return int(round(Decimal(str(1.1 * (property.price / 2))), 0))

    # Sell back one house or hotel on a property or sell all buildings back.
    def sell_building(self, player, property, building):

        # Sell one house on the property.
        if building == "house":
            property.buildings -= 1
            self.houses += 1
            player.money += property.house_cost / 2

        # Downgrade from a hotel to 4 houses.
        elif building == "hotel":
            property.buildings -= 1
            self.hotels += 1
            self.houses -= 4
            player.money += property.house_cost / 2

        # Sell all buildings on the property.
        elif building == "all":
            if property.buildings == 5:
                property.buildings = 0
                self.hotels += 1
                player.money += (property.house_cost / 2) * 5
            else:
                self.houses += property.buildings
                player.money += (property.house_cost / 2) * property.buildings
                property.buildings = 0

    # Changes a player's money total; sells buildings and mortgages properties if necessary.
    def change_money(self, player, increment):

        # Change the player's money.
        player.money += increment

        # The player's money total is negative.
        if player.money <= 0:

            # # Mortgage properties if they are not in a monopoly. # #

            for board_space in player.inventory:  # Cycle through the player's properties.
                if (board_space.group not in player.monopolies) and (not board_space.mortgaged):
                    mortgage_value = board_space.price / 2  # Find the mortgage value.
                    player.money += mortgage_value  # Gain the mortgage value.
                    board_space.mortgaged = True  # Mortgage property.
                    if player.money > 0:  # Check if the player is out of the hole.
                        return  # Exit function.

            # # Sell houses and hotels. # #

            # Check if the player has any monopolies
            if player.monopolies:

                # Initial condition.
                keep_selling = True

                while keep_selling:
                    keep_selling = False
                    for board_space in player.inventory:
                        # It has buildings and we are selling "evenly".
                        if board_space.buildings > 0 and self.even_selling_test(board_space, player):
                            keep_selling = True  # We should check again.
                            if board_space.buildings == 5:  # It's a hotel.
                                if self.houses >= 4:  # Check if there are 4 houses to replace the hotel.
                                    self.sell_building(player, board_space, "hotel")  # Hotel - > 4 Houses
                                else:  # Not enough houses to break hotel.
                                    for board_space2 in player.inventory:
                                        if board_space2.group == board_space.group:
                                            self.sell_building(player, board_space2, "all")
                            else:  # It's a house.
                                self.sell_building(player, board_space, "house")
                            if player.money > 0:  # The player is out of the hole.
                                return  # Exit

            # # Mortgage properties in monopolies. # #

            for board_space in player.inventory:  # Cycle through all board spaces.
                if not board_space.mortgaged:
                    if board_space.group not in player.monopolies:
                        print('eee error')
                    mortgage_value = board_space.price / 2  # Find the mortgage value.
                    player.money += mortgage_value  # Gain the mortgage value.
                    board_space.mortgaged = True  # Mortgage property.
                    if player.money > 0:  # Check if the player is out of the hole.
                        return  # Exit function.

    # Decides if the player is selling evenly or not.
    def even_selling_test(self, property, player):
        test_result = True
        for board_space in player.inventory:
            if board_space.group == property.group and board_space.buildings - property.buildings > 0:
                test_result = False
        return test_result

    # Decides if the player is building evenly or not.
    def even_building_test(self, property, player):
        test_result = True
        for board_space in player.inventory:
            if board_space.group == property.group and property.buildings - board_space.buildings > 0:
                test_result = False
        return test_result


    # Check that a property in the same group does not have buildings.
    def mortgage_check(self, property, player):
        test_result = True
        for a_property in player.inventory:
            if a_property.buildings > 0 and a_property.group == property.group:
                test_result = False
        return test_result

    # Un-mortgage and then buy houses/hotels.
    def develop_properties(self, player):

        # # Un-mortgage properties in monopolies, if possible. # #
        for board_space in player.inventory:
            if (board_space.mortgaged) and (board_space.group in player.monopolies):
                unmortgage_price = self.unmortgage_price(board_space)
                if player.money - unmortgage_price >= player.buying_threshold:
                    player.money -= unmortgage_price  # Pay un-mortgage price.
                    board_space.mortgaged = False  # Un-mortgage property.
                else:
                    return
        # TODO Bug

        # # Buy buildings. # #
        if player.monopolies:
            keep_building = True  # Initial condition.
            while keep_building:
                keep_building = False  # Don't keep building unless something is bought.
                for board_space in player.inventory:  # Cycle through player inventory.
                    if board_space.group in player.monopolies:  # and not board_space.mortgaged:  # It's in a monopoly.
                        if self.even_building_test(board_space, player):  # Building "evenly".
                            if board_space.buildings < player.building_threshold:  # Check player's building limit.
                                if board_space.mortgaged:
                                    print('error 10', board_space.name)

                                # Calculate current cash available.
                                if player.development_threshold == 1:
                                    available_cash = player.money - 1
                                elif player.development_threshold == 2:
                                    # Find available mortgage value.
                                    available_mortgage_value = 0
                                    for property in player.inventory:
                                        if (property.group not in player.monopolies) and (not property.mortgaged):
                                            available_mortgage_value += property.price / 2
                                    available_cash = available_mortgage_value + player.money - 1
                                else:
                                    available_cash = player.money - player.buying_threshold

                                # The player can afford it.
                                if available_cash - board_space.house_cost >= 0:
                                    building_supply = 0
                                    if board_space.buildings < 4:  # Ready for a house.
                                        building_supply = self.houses
                                        building = "house"
                                    elif board_space.buildings == 4:  # Ready for a hotel.
                                        building_supply = self.hotels
                                        building = "hotel"

                                    # Check if there is a building available.
                                    if building_supply > 0:
                                        if building == "house":
                                            self.houses -= 1  # Take 1 house.
                                        elif building == "hotel":
                                            self.hotels -= 1  # Take 1 hotel.
                                            self.houses += 4  # Put back 4 houses.

                                        board_space.buildings += 1  # Add building to property.
                                        player.money -= board_space.house_cost  # Pay building cost.

                                        if player.development_threshold != 2 and player.money < 0:
                                            print("error 9", player.money)

                                        # Mortgage properties to pay for building.
                                        if player.development_threshold == 2:
                                            property_index = 0
                                            while player.money <= 0:
                                                c_property = player.inventory[property_index]
                                                if c_property.group not in player.monopolies and not c_property.mortgaged:
                                                    mortgage_me = self.mortgage_check(c_property, player)
                                                    if mortgage_me:
                                                        c_property.mortgaged = True
                                                        player.money += c_property.price / 2
                                                property_index += 1

                                        keep_building = True  # Allow the player to build again.
                                        self.first_building = True  # Buildings have been built.

        # # Un-mortgage singleton properties. # #
        for board_space in player.inventory:
            if board_space.mortgaged:
                unmortgage_price = self.unmortgage_price(board_space)
                if player.money - unmortgage_price >= player.buying_threshold:
                    player.money -= unmortgage_price  # Pay un-mortgage price.
                    board_space.mortgaged = False  # Un-mortgage property.
                else:
                    return  # Exit if the player doesn't have enough money to continue.

    # Determines if the player owns all of the properties in the the given property's group.
    def monopoly_status(self, player, current_property, additional_properties=()):
        # Find the name of the property's group.
        group = current_property.group

        # There are no monopolies for board spaces, railroads or utilities.
        if group in ["", "Railroad", "Utility"]:
            return False  # The property is not in a color group.

        # Count how many properties in the group that player owns.
        property_counter = 0  # Initialize counter.

        # Check all of the player's properties.
        for property in player.inventory:
            if property.group == group:
                property_counter += 1

        # Check additional properties.
        if additional_properties:
            for property in additional_properties:
                if property.group == group:
                    property_counter += 1

        # Return result.
        if property_counter == 3 and group in ["Light Blue", "Pink", "Orange", "Red", "Yellow", "Green"]:
            return True  # The property is in a monopoly and a group of three.
        elif property_counter == 2 and group in ["Dark Blue", "Brown"]:
            return True  # The property is in a monopoly and a group of two.
        else:
            return False  # The player doesn't have a monopoly.

    # Calculate how much money a player has available to mortgage
    def find_avaliable_mortgage_value(self, player):
        available_mortgage_value = 0
        for property in player.inventory:
            if property.buildings == 0 and not property.mortgaged and property.group not in player.monopolies:
                add_my_value = True

                '''# Check that another property in the group does not have a building.
                if property.group in player.monopolies:
                    for a_property in player.inventory:
                        if a_property.buildings > 0 and a_property.group == property.group:
                            add_my_value = False'''

                # Add mortgage value.
                if add_my_value:
                    available_mortgage_value += property.price / 2
        return available_mortgage_value

    # Handles auctions when a property is not bought.
    def auction(self, board_space):
        # Eah player makes a bid on the property.
        for current_player in self.players:
            current_player.bid_includes_mortgages = False  # Reset this variable.

            # If the player has a preference for the group.
            if board_space.group in current_player.group_preferences:
                current_player.auction_bid = current_player.money - 1

            # If the player will complete their group and wants to.
            elif current_player.complete_monopoly == 1 and \
                    self.monopoly_status(current_player, board_space, additional_properties=[board_space]):
                current_player.auction_bid = current_player.money - 1

            # If the player wants to mortgage properties.
            elif current_player.complete_monopoly == 2 and \
                    self.monopoly_status(current_player, board_space, additional_properties=[board_space]):
                current_player.bid_includes_mortgages = True
                # Find all the money the player can use by mortgaging other properties.
                available_mortgage_value = self.find_avaliable_mortgage_value(current_player)
                current_player.auction_bid = current_player.money + available_mortgage_value - 1
            else:
                current_player.auction_bid = current_player.money - current_player.buying_threshold

        # The two-player case.
        player1 = self.players[0]
        player2 = self.players[1]

        # The property is not bought.
        if player1.auction_bid < 1 and player2.auction_bid < 1:
            return  # Exit function.

        # Player 1 buys it at $1
        elif player1.auction_bid > 0 and player2.auction_bid < 1:
            winning_bid = 1
            winning_player = player1

        # Player 2 buys it at $1
        elif player1.auction_bid < 1 and player2.auction_bid > 0:
            winning_bid = 1
            winning_player = player2

        # A random player buys the property.
        elif player1.auction_bid == player2.auction_bid:
            random_player = choice([player1, player2])
            winning_bid = random_player.auction_bid
            winning_player = random_player

        # Player 1 has a higher bid.
        elif player1.auction_bid > player2.auction_bid:
            winning_bid = player2.auction_bid + 1
            winning_player = player1

        # Player 2 has a higher bid.
        elif player2.auction_bid > player1.auction_bid:
            winning_bid = player1.auction_bid + 1
            winning_player = player2
        else:
            winning_player = Player(3)
            print('error 8')
            return

        # Special buying procedure if the player wants to mortgage properties.
        if winning_player.bid_includes_mortgages:
            winning_player.money += -winning_bid  # Pay for property.

            # Make up the funds.
            property_index = 0
            while winning_player.money <= 0:
                c_property = winning_player.inventory[property_index]
                if c_property.buildings == 0 and not c_property.mortgaged and c_property.group not in winning_player.monopolies:
                    mortgage_me = self.mortgage_check(c_property, winning_player)

                    # Mortgage the property.
                    if mortgage_me:
                        c_property.mortgaged = True
                        winning_player.money += c_property.price / 2
                property_index += 1

            self.unowned_properties.remove(board_space)  # Remove property from unowned properties list.
            winning_player.inventory.append(board_space)  # Add the property to the player's inventory.
            winning_player.monopolies.append(board_space.group)  # Add the group to the player's list of monopolies.

        else:
            self.buy_property(winning_player, board_space, custom_price=winning_bid)


    # Find the liquid wealth of all of the player's properties.
    def total_assets(self, player):
        liquid_property = 0  # The liquidated property wealth of the player.
        for board_space in player.inventory:
            liquid_property += board_space.price

        liquid_buildings = 0  # The cost of all buildings the player owns.
        for board_space in player.inventory:
            liquid_buildings += board_space.buildings * board_space.house_cost  # Add the price of the buildings.

        all_assets = player.money + liquid_property + liquid_buildings
        return all_assets

    # Decides what a player does on a property,
    def property_action(self, player, board_space):
        if board_space in player.inventory:
            pass  # The player owns the property. Nothing happens.
        elif board_space.mortgaged:
            pass  # The property is mortgaged. Nothing happens.
        elif board_space in self.unowned_properties:  # The property is unowned.
            if self.trip_to_start and (not player.passed_go):
                pass  # The player has to wait to pass Go to buy/auction a property.
            else:  # The player can buy it.
                # The player has enough money to buy the property.
                if player.money - board_space.price >= player.buying_threshold:
                    self.buy_property(player, board_space)

                # The player has a preference for the group and will pay any money they have.
                elif board_space.group in player.group_preferences and player.money - board_space.price > 0:
                    self.buy_property(player, board_space)

                # The player will gain a monopoly, they want to complete the group, they have the money.
                elif player.complete_monopoly == 1 and player.money - board_space.price > 0 and \
                        self.monopoly_status(player, board_space, additional_properties=[board_space]):
                    self.buy_property(player, board_space)

                # The player will mortgage other properties to buy it if it completes a group.
                elif player.complete_monopoly == 2 and \
                        self.monopoly_status(player, board_space, additional_properties=[board_space]):
                    # Find all the money the player can use by mortgaging other properties.
                    available_mortgage_value = self.find_avaliable_mortgage_value(player)

                    # If the player can mortgage to buy, they will.
                    if (player.money + available_mortgage_value) - board_space.price > 0:
                        player.money += -board_space.price  # Pay for property.

                        # Make up the funds.
                        property_index = 0
                        while player.money <= 0:
                            c_property = player.inventory[property_index]
                            if c_property.buildings == 0 and not c_property.mortgaged and c_property.group not in player.monopolies:
                                mortgage_me = self.mortgage_check(c_property, player)
                                if mortgage_me:
                                    c_property.mortgaged = True
                                    player.money += c_property.price / 2
                            property_index += 1

                        self.unowned_properties.remove(board_space)  # Remove property from unowned properties list.
                        player.inventory.append(board_space)
                        player.monopolies.append(board_space.group)  # Add the group to the player's list of monopolies.

                # The player can't buy it or decides not to.
                else:
                    if self.auctions_enabled:  # If auctions are enabled...
                        self.auction(board_space)  # The property is auctioned.
        else:  # The property is owned by another player.
            self.pay_rent(player)  # The player pays the owner rent.

    # Decide what the player should do on a given board space.
    def board_action(self, player, board_space):
        if board_space.name in ["Go", "Just Visiting / In Jail"]:
            pass  # Nothing happens on Go or Just Visiting.

        elif board_space.name == "Go":
            # Give the player an extra $200 if the house rule is enabled.
            if self.double_on_go:
                self.change_money(player, 200)

        elif board_space.name == "Income Tax":
            # The player pays $200.  The '10% of all assets' option was removed in 2008.
            self.change_money(player, -200)

            # Check to see if the Free Parking pool is enabled.
            if self.free_parking_pool:
                self.money_in_fp += 200  # The pool gains the tax.

        elif board_space.name == "Free Parking":
            if self.free_parking_pool:  # Check to see if the Free Parking pool is enabled.
                self.change_money(player, self.money_in_fp)  # The player takes the money in Free Parking.
                self.money_in_fp = 0  # The pool is reset to $0.

        elif board_space.name == "Chance":
            self.chance(player)  # Draw card and make action.

        elif board_space.name == "Community Chest":
            self.community_chest(player)  # Draw card and make action.

        elif board_space.name == "Go to Jail":
            self.go_to_jail(player)  # The player goes to jail.

        elif board_space.name == "Luxury Tax":
            self.change_money(player, -100)  # The player pays a $100 tax.

            if self.free_parking_pool:  # Check to see if the Free Parking pool is enabled.
                self.money_in_fp += 100  # The pool gains the tax.

        else:  # The player landed on a property.
            self.property_action(player, board_space)

        # Reset this variable.
        player.card_rent = False

    # An individual player takes a turn.
    def take_turn(self, player):
        self.turn_counter += 1  # Increase turn counter
        self.doubles_counter = 0  # Reset doubles counter.

        # Roll the dice.
        die1 = randint(1, 6)
        die2 = randint(1, 6)
        self.dice_roll = die1 + die2

        # Check for snake eyes.
        if self.snake_eyes_bonus and die1 == 1 == die2:
            self.change_money(player, 500)

        # Is the player in jail?
        if player.in_jail:  # Player is in jail.
            player.jail_counter += 1  # Increase the jail turn counter
            # The player wants to move or they have to.
            if (player.jail_counter - 1 == player.jail_time) or (die1 != die2 and player.jail_counter == 3):
                player.jail_counter = 0  # Reset the jail counter.
                self.move_again = True  # The player can move.
                self.pay_out_of_jail(player)  # Pay out using a card or $50.
            elif die1 == die2:  # The player rolled doubles.
                player.jail_counter = 0  # Reset the jail counter.
                self.move_again = True  # The player can move out of jail
            else:  # The player didn't roll doubles.
                self.move_again = False  # The player can not move around the board.
        else:  # The player is not in jail.
            self.move_again = True  # The player can roll and move.

        # The main loop.
        while self.move_again and player.money > 0:
            # Roll again for doubles.
            if self.doubles_counter > 0:
                die1 = randint(1, 6)
                die2 = randint(1, 6)
                self.dice_roll = die1 + die2

                # Check for snakes eyes.
                if self.snake_eyes_bonus and die1 == 1 == die2:
                    self.change_money(player, 500)

            # Check for doubles.
            if (die1 == die2) and (not player.in_jail):
                self.doubles_counter += 1  # Increase the doubles counter.
                if self.doubles_counter == 3:  # The players is speeding.
                    self.go_to_jail(player)
                    return  # The function ends.
                else:  # The player is not speeding.
                    self.move_again = True  # The player rolled doubles.
            else:
                player.in_jail = False  # The player is no longer in jail.
                self.move_again = False  # The player did not roll doubles.

            self.move_ahead(player, self.dice_roll)  # Move the player
            board_space = self.board[player.position]  # Find the current board space.
            self.board_action(player, board_space)  # Make an action based on the current board space.

            # If a card or board space brought the player to jail, end the function.
            if player.in_jail:
                return

    # Provides the current status of the game, "live" or "done".
    def update_status(self):
        for single_player in self.players:
            if single_player.money <= 0:
                self.game_status = "done"
                if single_player.number == 1:
                    self.result = 2
                elif single_player.number == 2:
                    self.result = 1

        # End the game at the designated cutoff.
        if self.turn_counter == self.cutoff:
            self.game_status = "done"
            self.result = 0

            '''player1_assets = self.total_assets(self.players[0])
            player2_assets = self.total_assets(self.players[1])
            if player1_assets > player2_assets:
                self.result = 1
            elif player1_assets < player2_assets:
                self.result = 2
            else:
                self.result = choice([1, 2])'''


    # Plays a game object.
    def play(self):
        # Shuffle the players.
        playing_order = [player_number for player_number in range(1, self.number_of_players + 1)]
        shuffle(playing_order)

        # Initial conditions.
        current_player_index = 0

        # Game loop.
        while self.game_status == "live":
            # Check to see if properties can be un-mortgaged or houses and hotel and can be purchased.
            if current_player_index == 0:
                self.develop_properties(self.players[0])
                self.develop_properties(self.players[1])
            else:
                self.develop_properties(self.players[1])
                self.develop_properties(self.players[0])

            self.take_turn(self.players[playing_order[current_player_index] - 1])  # Current player takes turn.
            current_player_index = (current_player_index + 1) % self.number_of_players  # Update current_player_index.
            self.update_status()  # Update game status.

        # Ending report.
        return [self.result, self.turn_counter, self.players[0].monopolies, self.players[1].monopolies,
                self.players[0].money, self.players[1].money]