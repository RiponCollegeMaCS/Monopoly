# # # # # # # # # # # # # # # #
# Monopoly Simulator          #
# Created by Mitchell Eithun  #
# July 2014 - July 2015       #
# # # # # # # # # # # # # # # #

from random import randint, shuffle, choice  # For random game elements.
from decimal import getcontext, ROUND_HALF_UP  # The Decimal module for better rounding.
from imageExport import exportBoard  # Used to create images of the board


getcontext().rounding = ROUND_HALF_UP  # Adjust the rounding scheme.


# Define the Player class.
class Player:
    __slots__ = ['number', 'development_threshold', 'init_jail_time', 'jail_time',
                 'smart_jail_strategy', 'complete_monopoly', 'buying_threshold', 'property_values',
                 'group_ordering', 'group_ranking', 'group_values', 'group_inv', 'inventory', 'monopolies',
                 'mortgaged_properties', 'position', 'money', 'jail_counter', 'chance_card',
                 'community_chest_card', 'in_jail', 'card_rent', 'passed_go',
                 'mortgage_auctioned_property', 'auction_bid', 'bid_includes_mortgages', 'trade_pairs', 'rent_power']

    def __init__(self,
                 number,
                 buying_threshold=500,
                 jail_time=3,
                 smart_jail_strategy=False,
                 complete_monopoly=0,
                 development_threshold=0,
                 group_ordering=("Brown", "Light Blue", "Pink", "Orange",
                                 "Red", "Yellow", "Green", "Dark Blue", "Utility", "Railroad"),
                 group_values=None,
                 property_values=[0] * 40
    ):

        self.number = number  # A player's id number.

        # Strategy parameters.
        self.development_threshold = development_threshold
        self.init_jail_time = jail_time
        self.jail_time = jail_time
        self.smart_jail_strategy = smart_jail_strategy
        self.complete_monopoly = complete_monopoly
        self.buying_threshold = buying_threshold
        self.property_values = property_values

        self.rent_power = 0

        # Property rankings.
        self.group_values = group_values

        if self.group_values:
            self.group_ordering = sorted(group_values, key=group_values.get, reverse=True)
        else:
            self.group_ordering = group_ordering
            self.group_ranking = {"Brown": 0, "Light Blue": 0, "Pink": 0, "Orange": 0,
                                  "Red": 0, "Yellow": 0, "Green": 0, "Dark Blue": 0,
                                  "Utility": 0, "Railroad": 0}
            for index in range(len(self.group_ordering)):
                self.group_ranking[self.group_ordering[index]] = index

        self.group_inv = {"Brown": [], "Light Blue": [], "Pink": [], "Orange": [],
                          "Red": [], "Yellow": [], "Green": [], "Dark Blue": [],
                          "Utility": [], "Railroad": []}  # Inventory dictionary organized by group
        self.trade_pairs = {"Brown": [], "Light Blue": [], "Pink": [], "Orange": [],
                            "Red": [], "Yellow": [], "Green": [], "Dark Blue": [],
                            "Utility": [], "Railroad": []}

        # Sets of properties.
        self.inventory = set()  # A set of the player's properties.
        self.monopolies = set()
        self.mortgaged_properties = set()

        # Misc.
        self.position = 0  # The player starts on "Go".
        self.money = 1500  # The player starts with $1,500.
        self.jail_counter = 0  # The "turns in jail" counter.

        # Flags
        self.chance_card = False  # The player has no "Get Out of Jail Free" cards.
        self.community_chest_card = False  # The player has no "Get Out of Jail Free" cards.
        self.in_jail = False  # The player is not in jail.
        self.card_rent = False
        self.passed_go = False  # Used for a house rule.

        # For auctions
        self.mortgage_auctioned_property = False
        self.auction_bid = 0

        # For house rules.
        self.bid_includes_mortgages = False

    # Add a group to the list of monopolies, checking that it is a valid color group.
    def add_monopoly(self, group):
        if group != "Railroad" and group != "Utility":
            self.monopolies.add(group)
        return

    # Used in analysis to add railroad and utility monopolies to player's lists of monopolies.
    def add_railroads_and_utilities(self):
        railroad_counter = self.group_inv['Railroad']
        utility_counter = self.group_inv["Utility"]

        if railroad_counter == 4:
            self.monopolies.add("Railroad")

        if utility_counter == 2:
            self.monopolies.add("Utility")

    # Unmortgage properties in monopolies if possible, in accordance with buying threshold.
    def unmortgage_monopolied_properties(self, game_info):
        # Look at properties in complete monopolies.
        for board_space in set(self.mortgaged_properties):
            if board_space.group in self.monopolies:
                # See if we can afford to unmortgage it.
                if self.money - board_space.unmortgage_price >= self.get_buying_threshold(game_info):
                    self.money -= board_space.unmortgage_price  # Pay un-mortgage price.
                    board_space.unmortgage(game_info)  # Un-mortgage property.


    # Attempt to develop properties in monopolies.
    def buy_buildings(self, game_info):
        # Main loop.
        for group in self.monopolies:  # Cycle through player's monopolies.
            keep_building = True
            while keep_building:
                # Don't keep building unless something is bought.
                keep_building = False
                for board_space in self.group_inv[group]:
                    if board_space.buildings < 5 and not board_space.mortgaged:  # Check we can actually build.

                        # Calculate current cash available.
                        if self.development_threshold == 1:
                            # The player will use all but $1 to buy.
                            available_cash = self.money - 1
                        elif self.development_threshold == 2:
                            available_cash = self.find_available_mortgage_value() + self.money - 1
                        else:
                            available_cash = self.money - self.get_buying_threshold(game_info)

                        # The player can afford it.
                        if available_cash - board_space.house_cost >= 0:

                            # Check if there is a building available.
                            building_supply = 0
                            if board_space.buildings < 4:  # Ready for a house.
                                building_supply = game_info.houses  # The number of houses available
                                building = "house"
                            elif board_space.buildings == 4:  # Ready for a hotel.
                                building_supply = game_info.hotels  # The number of hotels available
                                building = "hotel"

                            if building_supply > 0:
                                if self.even_building_test(board_space):  # Building "evenly".
                                    self.rent_power -= board_space.rents[board_space.buildings]
                                    # Build!
                                    if building == "house":
                                        game_info.houses -= 1  # Take 1 house.
                                    elif building == "hotel":
                                        game_info.hotels -= 1  # Take 1 hotel.
                                        game_info.houses += 4  # Put back 4 houses.

                                    board_space.buildings += 1  # Add building to property.
                                    self.money -= board_space.house_cost  # Pay building cost.

                                    self.rent_power += board_space.rents[board_space.buildings]

                                    # Mortgage properties to pay for building.
                                    if self.development_threshold == 2:
                                        for c_property in set(self.inventory - self.mortgaged_properties):
                                            if c_property.group not in self.monopolies:
                                                c_property.mortgage(game_info)
                                                self.money += c_property.mortgage_value
                                            if self.money > 0:
                                                break

                                    keep_building = True  # Allow the player to build again.
                                    game_info.first_building = True  # Buildings have been built.

        if game_info.hotel_upgrade or game_info.building_sellback:
            # # Buy hotels if we have exhausted houses # #
            if game_info.houses == 0 and game_info.hotels > 0:
                for group in self.monopolies:
                    house_disparity = 0
                    properties_in_group = 0
                    house_cost = 0
                    houses_found = 0
                    for board_space in self.group_inv[group]:
                        properties_in_group += 1
                        house_cost = board_space.house_cost
                        house_disparity += 5 - board_space.buildings
                        houses_found += board_space.buildings

                    # There are houses to build.
                    if house_disparity > 0:
                        # Check if there are enough hotels available.
                        if game_info.hotels >= properties_in_group:

                            # Calculate current cash available.
                            if self.development_threshold == 1:
                                # The player will use all but $1 to buy.
                                available_cash = self.money - 1
                            elif self.development_threshold == 2:
                                available_cash = self.find_available_mortgage_value() + self.money - 1
                            else:
                                available_cash = self.money - self.get_buying_threshold(game_info)

                            house_costs = []
                            for prop in self.inventory:
                                if prop.group != group:
                                    if prop.buildings != 5:
                                        for house in range(prop.buildings):
                                            house_costs.append(prop.house_cost)

                            keep_going = True
                            if len(house_costs) < house_disparity and game_info.building_sellback:  # TODO
                                keep_going = False

                            if keep_going:
                                house_costs.sort()
                                total_house_costs = 0
                                for i in range(house_disparity):
                                    total_house_costs += house_costs[i] / 2

                                # Check if we can afford it.
                                if available_cash - (house_disparity * house_cost) - total_house_costs >= 0:

                                    # Build!
                                    for prop in self.group_inv[group]:
                                        prop.buildings = 5
                                        game_info.hotels -= 1
                                        game_info.houses += houses_found

                                    # Pay for it.
                                    self.money -= (house_cost * house_disparity) + total_house_costs

                                    # Mortgage properties to pay for buildings.
                                    if self.development_threshold == 2:
                                        for c_property in set(self.inventory - self.mortgaged_properties):
                                            if c_property.group not in self.monopolies:
                                                c_property.mortgage(game_info)
                                                self.money += c_property.mortgage_value
                                            if self.money > 0:
                                                break

    # # Un-mortgage singleton properties. # #
    def unmortgage_properties(self, game_info):
        for board_space in set(self.mortgaged_properties):
            if self.money - board_space.unmortgage_price >= self.get_buying_threshold(game_info):
                self.money -= board_space.unmortgage_price  # Pay un-mortgage price.
                board_space.unmortgage(game_info)  # Un-mortgage property.


    # Called between turns.
    def between_turns(self, game_info):
        # Un-mortgage properties in monopolies, if possible.
        self.unmortgage_monopolied_properties(game_info)

        # Attempt to buy buildings.
        self.buy_buildings(game_info)

        # Unmortgage properties.
        self.unmortgage_properties(game_info)


    # Determines how a player gets out of jail: use a GOOJF or pay $50.
    def pay_out_of_jail(self, game_info):
        if self.chance_card:
            self.chance_card = False  # The player uses his Chance GOOJF card.
            game_info.chance_cards.append(1)  # Add the card back into the list.
        elif self.community_chest_card:
            self.community_chest_card = False  # The player uses his Community Chest GOOJF card.
            game_info.community_chest_cards.append(1)  # Add the card back into the list.
        else:
            # The player pays $50 to get out.
            game_info.exchange_money(amount=50, giver=self, receiver=game_info.bank, summary="Paying out of Jail.")


    # Sell back one house or hotel on a property or sell all buildings back.
    def sell_building(self, property, building, game_info):
        # Sell one house on the property.
        if building == "house":
            self.rent_power -= property.rents[property.buildings]
            property.buildings -= 1
            game_info.houses += 1
            self.rent_power += property.rents[property.buildings]

            self.money += property.house_cost / 2

        # Downgrade from a hotel to 4 houses.
        elif building == "hotel":
            self.rent_power -= property.rents[property.buildings]
            property.buildings -= 1
            game_info.hotels += 1
            game_info.houses -= 4
            self.rent_power += property.rents[property.buildings]

            self.money += property.house_cost / 2

        # Sell all buildings on the property.
        elif building == "all":  # The property has a hotel.
            self.rent_power -= property.rents[property.buildings]
            if property.buildings == 5:
                property.buildings = 0
                game_info.hotels += 1
                self.money += (property.house_cost / 2) * 5
            else:  # The property has houses.
                game_info.houses += property.buildings
                self.money += (property.house_cost / 2) * property.buildings
                property.buildings = 0

            self.rent_power += property.rents[property.buildings]

    # Decides how player's make funds if they are in the hole.
    def make_funds(self, game_info):
        # # Mortgage properties if they are not in a monopoly. # #
        for board_space in set(self.inventory - self.mortgaged_properties):  # Cycle through the player's properties.
            if board_space.group not in self.monopolies:
                mortgage_value = board_space.mortgage_value  # Find the mortgage value.
                self.money += mortgage_value  # Gain the mortgage value.
                board_space.mortgage(game_info)  # Mortgage property.
                if self.money > 0:  # Check if the player is out of the hole.
                    return  # Exit function.

        # # Sell houses and hotels. # #

        # Check if the player has any monopolies
        if self.monopolies:

            # Initial condition.
            keep_selling = True

            while keep_selling:
                keep_selling = False
                for board_space in self.inventory:
                    # It has buildings and we are selling "evenly".
                    if board_space.buildings > 0 and self.even_selling_test(board_space):
                        keep_selling = True  # We should check again.
                        if board_space.buildings == 5:  # It's a hotel.
                            if game_info.houses >= 4:  # Check if there are 4 houses to replace the hotel.
                                self.sell_building(board_space, "hotel", game_info)  # Hotel - > 4 Houses
                            else:  # Not enough houses to break hotel.
                                for board_space2 in self.group_inv[
                                    board_space.group]:  # Sell back all buildings in GROUP.
                                    self.sell_building(board_space2, "all", game_info)
                        else:  # It's a house.
                            self.sell_building(board_space, "house", game_info)
                        if self.money > 0:  # The player is out of the hole.
                            return  # Exit

        # # Mortgage properties in monopolies. # #
        for board_space in set(self.inventory - self.mortgaged_properties):  # Cycle through all board spaces.
            mortgage_value = board_space.mortgage_value  # Find the mortgage value.
            self.money += mortgage_value  # Gain the mortgage value.
            board_space.mortgage(game_info)  # Mortgage property.
            if self.money > 0:  # Check if the player is out of the hole.
                return  # Exit function.

    # Allows the player to decide upon a jail strategy as soon as they are sent there.
    def set_jail_strategy(self, game_info):
        if self.smart_jail_strategy and game_info.first_building:
            self.jail_time = 3
        else:
            self.jail_time = self.init_jail_time

    # Decides if the player is selling evenly or not.
    def even_selling_test(self, property):
        for board_space in self.group_inv[property.group]:
            if board_space.buildings - property.buildings > 0:
                return False
        return True

    # Decides if the player is building evenly or not.
    def even_building_test(self, property):
        for board_space in self.group_inv[property.group]:
            if property.buildings - board_space.buildings > 0:
                return False
        return True

    # Calculate how much money a player has available to mortgage
    def find_available_mortgage_value(self):
        available_mortgage_value = 0
        for property in set(self.inventory - self.mortgaged_properties):
            if property.buildings == 0 and property.group not in self.monopolies:
                # Add mortgage value.
                available_mortgage_value += property.mortgage_value
        return available_mortgage_value

    # Decides how players make auction bids.
    def make_bid(self, property, game_info):
        # Reset these variables.
        self.bid_includes_mortgages = False
        self.mortgage_auctioned_property = False

        # If the player will complete their group and wants to.
        if self.complete_monopoly == 1 and \
                game_info.monopoly_status(player=self, current_property=property, add_me=1):
            self.auction_bid = self.money - 1

        # If the player wants to mortgage properties.
        elif self.complete_monopoly == 2 and \
                game_info.monopoly_status(player=self, current_property=property, add_me=1):
            self.bid_includes_mortgages = True
            # Find all the money the player can use by mortgaging other properties.
            available_mortgage_value = self.find_available_mortgage_value()
            self.auction_bid = self.money + available_mortgage_value - 1
        else:
            self.auction_bid = self.money - self.get_buying_threshold(game_info)

        # The bid should be at least the mortgage value of the property.
        if self.auction_bid < property.mortgage_value:
            self.auction_bid = property.mortgage_value
            self.mortgage_auctioned_property = True

    # Allows a player to gather the funds needed to complete an auction.
    def make_auction_funds(self, game_info, winning_bid, property):
        # If the bid with intentions to mortgage it.
        if self.mortgage_auctioned_property:
            property.mortgage(game_info)
            self.money += property.mortgage_value

        # Special buying procedure if the player wants to mortgage properties.
        if self.bid_includes_mortgages:
            self.money -= winning_bid  # Pay for property temporarily.

            # Make up the funds.
            for c_property in set(self.inventory - self.mortgaged_properties):
                if c_property.buildings == 0 and c_property.group not in self.monopolies:
                    c_property.mortgage(game_info)
                    self.money += c_property.mortgage_value
                if self.money > 0:
                    break

            self.money += winning_bid  # Pay money back.

    # Decides what the player does when he lands on an unowned property.
    def unowned_property_action(self, game_info, property):
        property_price = property.price
        # The player has enough money to buy the property.
        if self.money - property_price >= self.get_buying_threshold(game_info):
            game_info.buy_property(self, property)
            return True

        # The player will gain a monopoly, they want to complete the group, they have the money.
        if self.complete_monopoly == 1 and self.money - property_price > 0 and \
                game_info.monopoly_status(self, property, add_me=1):
            game_info.buy_property(self, property)
            return True

        # The player will mortgage other properties to buy it if it completes a group.
        if self.complete_monopoly == 2 and \
                game_info.monopoly_status(self, property, add_me=1):
            # Find all the money the player can use by mortgaging other properties.
            available_mortgage_value = self.find_available_mortgage_value()

            # If the player can mortgage to buy, they will.
            if (self.money + available_mortgage_value) - property.price > 0:
                self.money += -property.price  # Pay for property.

                # Make up the funds.
                for c_property in set(self.inventory - self.mortgaged_properties):
                    if c_property.buildings == 0 and c_property.group not in self.monopolies:
                        c_property.mortgage(game_info)
                        self.money += c_property.mortgage_value
                    if self.money > 0:
                        break

                game_info.update_inventories(player_from="Bank", player_to=self, prop=property)
                return True

        return False

    # Allow the player to make a decision about getting out of jail.
    def jail_decision(self, game_info):
        if self.jail_counter - 1 == self.jail_time:
            return True
        else:
            return False

    def highest_possible_rent(self, game_info):
        highest_possible_rent = 0
        for player in game_info.active_players:
            if player != self:
                for property in player.inventory:
                    temp = game_info.calculate_rent(owner=player, property=property)
                    if temp > highest_possible_rent:
                        highest_possible_rent = temp
        return highest_possible_rent

    # Return buying threshold at current point in game
    def get_buying_threshold(self, game_info):
        total_rent = game_info.other_player(self).rent_power
        return self.buying_threshold * total_rent


# Define the MoneyPool class.
class MoneyPool:
    def __init__(self, money):
        self.money = money


# Define the BoardLocation class.
class BoardLocation:
    __slots__ = ['id', 'name', 'price', 'group', 'rents', 'house_cost', 'unmortgage_price', 'mortgage_value',
                 'buildings', 'visits', 'mortgaged', 'owner', 'is_property']

    def __init__(self, id, name, price=0, group=None, rents=(0, 0, 0, 0, 0, 0), house_cost=0, unmortgage_price=0,
                 mortgage_value=0, is_property=True):
        self.id = id
        self.name = name  # The name of the board location.
        self.price = price  # How much it costs to buy the property.
        self.rents = rents  # The various rents.
        self.house_cost = house_cost  # How much it costs for a house.
        self.group = group  # Which group the property belongs to.
        self.buildings = 0  # The property starts with no development.
        self.visits = 0  # Hit counter.
        self.mortgaged = False
        self.owner = None
        self.unmortgage_price = unmortgage_price
        self.mortgage_value = mortgage_value
        self.is_property = is_property

    def unmortgage(self, game_info):
        self.mortgaged = False
        self.owner.mortgaged_properties.remove(self)
        self.owner.rent_power += game_info.calculate_rent(self)

    def mortgage(self, game_info):
        self.mortgaged = True
        if self.owner:
            self.owner.mortgaged_properties.add(self)
            self.owner.rent_power -= game_info.calculate_rent(self)


# Define the Game class.
class Game:
    __slots__ = ['auctions_enabled', 'trading_enabled', 'hotel_upgrade', 'building_sellback',
                 'free_parking_pool', 'double_on_go', 'no_rent_in_jail', 'trip_to_start', 'snake_eyes_bonus', 'cutoff',
                 'group_counts', 'inactive_players', 'active_players', 'num_active_players', 'turn_counter',
                 'doubles_counter', 'houses', 'hotels', 'winner', 'dice_roll', 'first_building', 'loss_reason',
                 'starting_player', 'trade_count', 'bank', 'free_parking', 'trade_pairs', 'player1', 'player2',
                 'chance_cards', 'community_chest_cards', 'chance_index', 'community_chest_index', 'board',
                 'development_order', 'move_again', 'board_groups', 'p1_trade_pairs', 'p2_trade_pairs',
                 'image_exporting', 'trades']

    def __init__(self, list_of_players=None, auctions_enabled=True, trading_enabled=False,
                 hotel_upgrade=False, building_sellback=False, image_exporting=False,
                 free_parking_pool=False, double_on_go=False, no_rent_in_jail=False, trip_to_start=False,
                 snake_eyes_bonus=False, cutoff=1000):

        # Rule changes.
        self.auctions_enabled = auctions_enabled  # A toggle to disable auctions.
        self.trading_enabled = trading_enabled
        self.hotel_upgrade = hotel_upgrade
        self.building_sellback = building_sellback
        self.image_exporting = image_exporting
        self.trades = []

        # Attributes for house rules.
        self.free_parking_pool = free_parking_pool
        self.double_on_go = double_on_go
        self.no_rent_in_jail = no_rent_in_jail
        self.trip_to_start = trip_to_start
        self.snake_eyes_bonus = snake_eyes_bonus

        # Misc.
        self.cutoff = cutoff
        self.group_counts = {"Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3,
                             "Red": 3, "Yellow": 3, "Green": 3, "Dark Blue": 2,
                             "Utility": 2, "Railroad": 4}
        self.create_board()

        # Add new players and reset values.
        if list_of_players:
            self.new_players(list_of_players)

    def new_players(self, list_of_players):
        # Player lists.
        self.inactive_players = []  # An empty list to store losing players.
        self.active_players = list_of_players  # Create  a list of players.
        self.num_active_players = len(list_of_players)

        # Create game elements.
        self.create_cards()  # Shuffle both card decks.

        # Reset board
        for space in self.board:
            space.mortgaged = False
            space.buildings = 0
            space.owner = None

        # Misc.
        self.turn_counter = 0  # Reset turn counter.
        self.doubles_counter = 0  # Reset doubles counter.
        self.houses = 32  # House supply.
        self.hotels = 12  # Hotel supply.
        self.winner = -1  # Ending game data.
        self.first_building = False  # Records whether a building has been bought for smart_jail_strategy
        self.loss_reason = []  # To store how a player lost the game.
        self.starting_player = 0  # Store which player started.
        self.trade_count = 0

        # Money pools.
        self.bank = MoneyPool(12500)  # Create the bank.
        self.free_parking = MoneyPool(0)  # Create the Free Parking pool.


    # Create list of numbers to represent Chance and Community Chest cards.
    def create_cards(self):
        # Create cards.
        self.chance_cards = [i for i in range(1, 16 + 1)]
        self.community_chest_cards = [i for i in range(1, 16 + 1)]

        # Shuffle cards.
        shuffle(self.chance_cards)
        shuffle(self.community_chest_cards)

        # Reset index.
        self.chance_index = 0
        self.community_chest_index = 0

    # Creates a BoardLocation object for each space on the board.
    def create_board(self):
        # "Name", Price, "Group", (Rents), House Cost, Unmortgage Price, Mortgage Value
        self.board = [
            BoardLocation(0, "Go", is_property=False),
            BoardLocation(1, "Mediterranean Ave.", 60, "Brown", (2, 10, 30, 90, 160, 250), 50, 33, 0),
            BoardLocation(2, "Community Chest", is_property=False),
            BoardLocation(3, "Baltic Ave.", 60, "Brown", (4, 20, 60, 180, 320, 450), 50, 33, 30),
            BoardLocation(4, "Income Tax", is_property=False),
            BoardLocation(5, "Reading Railroad", 200, "Railroad", (), 0, 110, 100),
            BoardLocation(6, "Oriental Ave.", 100, "Light Blue", (6, 30, 90, 270, 400, 550), 50, 55, 50),
            BoardLocation(7, "Chance", is_property=False),
            BoardLocation(8, "Vermont Ave.", 100, "Light Blue", (6, 30, 90, 270, 400, 550), 50, 55, 50),
            BoardLocation(9, "Connecticut Ave.", 120, "Light Blue", (8, 40, 100, 300, 450, 600), 50, 66, 60),
            BoardLocation(10, "Just Visiting / In Jail", is_property=False),
            BoardLocation(11, "St. Charles Place", 140, "Pink", (10, 50, 150, 450, 625, 750), 100, 77, 70),
            BoardLocation(12, "Electric Company", 150, "Utility", (), 0, 83, 75),
            BoardLocation(13, "States Ave.", 140, "Pink", (10, 50, 150, 450, 625, 750), 100, 77, 70),
            BoardLocation(14, "Virginia Ave.", 160, "Pink", (12, 60, 180, 500, 700, 900), 100, 88, 80),
            BoardLocation(15, "Pennsylvania Railroad", 200, "Railroad", (), 0, 110, 100),
            BoardLocation(16, "St. James Place", 180, "Orange", (14, 70, 200, 550, 750, 950), 100, 99, 90),
            BoardLocation(17, "Community Chest", is_property=False),
            BoardLocation(18, "Tennessee Ave.", 180, "Orange", (14, 70, 200, 550, 750, 950), 100, 99, 90),
            BoardLocation(19, "New York Ave.", 200, "Orange", (16, 80, 220, 600, 800, 1000), 100, 110, 100),
            BoardLocation(20, "Free Parking", is_property=False),
            BoardLocation(21, "Kentucky Ave.", 220, "Red", (18, 90, 250, 700, 875, 1050), 150, 121, 110),
            BoardLocation(22, "Chance", is_property=False),
            BoardLocation(23, "Indiana Ave.", 220, "Red", (18, 90, 250, 700, 875, 1050), 150, 121, 110),
            BoardLocation(24, "Illinois Ave.", 240, "Red", (20, 100, 300, 750, 925, 1100), 150, 132, 120),
            BoardLocation(25, "B. & O. Railroad", 200, "Railroad", (), 0, 110, 100),
            BoardLocation(26, "Atlantic Ave.", 260, "Yellow", (22, 110, 330, 800, 975, 1150), 150, 143, 130),
            BoardLocation(27, "Ventnor Ave.", 260, "Yellow", (22, 110, 330, 800, 975, 1150), 150, 143, 130),
            BoardLocation(28, "Water Works", 150, "Utility", (), 0, 83, 75),
            BoardLocation(29, "Marvin Gardens", 280, "Yellow", (24, 120, 360, 850, 1025, 1200), 150, 154, 140),
            BoardLocation(30, "Go to Jail", is_property=False),
            BoardLocation(31, "Pacific Ave.", 300, "Green", (26, 130, 390, 900, 1100, 1275), 200, 165, 150),
            BoardLocation(32, "North Carolina Ave.", 300, "Green", (26, 130, 390, 900, 1100, 1275), 200, 165, 150),
            BoardLocation(33, "Community Chest", is_property=False),
            BoardLocation(34, "Pennsylvania Ave.", 320, "Green", (28, 150, 450, 1000, 1200, 1400), 200, 176, 160),
            BoardLocation(35, "Short Line Railroad", 200, "Railroad", (), 0, 110, 100),
            BoardLocation(36, "Chance", is_property=False),
            BoardLocation(37, "Park Place", 350, "Dark Blue", (35, 175, 500, 1100, 1300, 1500), 200, 193, 175),
            BoardLocation(38, "Luxury Tax", is_property=False),
            BoardLocation(39, "Boardwalk", 400, "Dark Blue", (50, 200, 600, 1400, 1700, 2000), 200, 220, 200),
        ]

        # Create a dictionary to quickly find properties in a certain group.
        self.board_groups = {"Brown": [], "Light Blue": [], "Pink": [], "Orange": [],
                             "Red": [], "Yellow": [], "Green": [], "Dark Blue": [],
                             "Utility": [], "Railroad": []}

        for space in self.board:
            if space.is_property:
                self.board_groups[space.group].append(space)


    # Defines the actions of the Community Chest cards.
    def community_chest(self, player):
        card = self.community_chest_cards[self.community_chest_index]
        if card == 1:  # GET OUT OF JAIL FREE
            player.community_chest_card = True  # Give the card to the player.
            self.community_chest_cards.remove(1)  # Remove the card from the list
        elif card == 2:  # PAY SCHOOL FEES OF $50 [UPDATED IN 2008]
            self.exchange_money(amount=50, giver=player, receiver=self.free_parking, summary="Community Chest.")
        elif card == 3:  # IT IS YOUR BIRTHDAY. / COLLECT $10 / FROM EVERY PLAYER [UPDATED IN 2008]
            for individual in self.active_players:  # For each player...
                self.exchange_money(amount=10, giver=individual, receiver=player, summary="Community Chest.")
        elif card == 4:  # XMAS FUND MATURES / COLLECT $100
            self.exchange_money(amount=100, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 5:  # INCOME TAX REFUND / COLLECT $20
            self.exchange_money(amount=20, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 6:  # YOU INHERIT $100
            self.exchange_money(amount=100, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 7:  # YOU HAVE WON SECOND PRIZE IN A BEAUTY CONTEST / COLLECT $10
            self.exchange_money(amount=10, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 8:  # BANK ERROR IN YOUR FAVOR / COLLECT $200
            self.exchange_money(amount=200, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 9:  # RECEIVE $25 / CONSULTANCY FEE [WORDING UPDATED IN 2008]
            self.exchange_money(amount=25, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 10:  # ADVANCE TO GO (COLLECT $200)
            self.move_to(player, 0)  # Player moves to Go.
        elif card == 11:  # YOU ARE ASSESSED FOR STREET REPAIRS
            if player.monopolies:
                house_counter = 0
                hotel_counter = 0
                for board_space in player.inventory:  # Cycle through all board spaces.
                    if board_space.buildings == 5:
                        hotel_counter += 1  # Add hotels.
                    else:
                        house_counter += board_space.buildings  # Add houses.
                house_repairs = 40 * house_counter  # $40 PER HOUSE
                hotel_repairs = 115 * hotel_counter  # $115 PER HOTEL
                self.exchange_money(amount=house_repairs + hotel_repairs, giver=player, receiver=self.free_parking,
                                    summary="Community Chest.")
        elif card == 12:  # LIFE INSURANCE MATURES / COLLECT $100
            self.exchange_money(amount=100, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 13:  # DOCTOR'S FEE / PAY $50
            self.exchange_money(amount=50, giver=player, receiver=self.free_parking, summary="Community Chest.")
        elif card == 14:  # FROM SALE OF STOCK / YOU GET $50 [UPDATED IN 2008]
            self.exchange_money(amount=50, giver=self.bank, receiver=player, summary="Community Chest.")
        elif card == 15:  # PAY HOSPITAL $100
            self.exchange_money(amount=100, giver=player, receiver=self.free_parking, summary="Community Chest.")
        elif card == 16:  # GO TO JAIL
            self.go_to_jail(player)  # Send player to jail.

        if card == 1 and self.community_chest_index == 15:  # GOOJF card was at the end.
            self.community_chest_index = 0  # Restart deck.
        elif card == 1:  # GOOJF card was somewhere else.
            pass  # Do not change index.
        else:
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
            self.exchange_money(amount=150, giver=self.bank, receiver=player, summary="Chance.")
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
            if player.monopolies:
                house_counter = 0
                hotel_counter = 0
                for board_space in player.inventory:  # Cycle through all board spaces.
                    if board_space.buildings == 5:
                        hotel_counter += 1  # Add hotels.
                    else:
                        house_counter += board_space.buildings  # Add houses.
                house_repairs = 45 * house_counter  # $45 PER HOUSE
                hotel_repairs = 100 * hotel_counter  # $100 PER HOTEL
                self.exchange_money(amount=house_repairs + hotel_repairs, giver=player, receiver=self.free_parking,
                                    summary="Chance.")
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
            self.exchange_money(amount=15, giver=player, receiver=self.free_parking, summary="Chance.")
        elif card == 13:  # TAKE A RIDE ON THE READING RAILROAD
            self.move_to(player, 5)
            self.board_action(player, self.board[player.position])
        elif card == 14:  # ADVANCE TOKEN TO BOARD WALK [sic.]
            self.move_to(player, 39)
            self.board_action(player, self.board[player.position])
        elif card == 15:  # PAY EACH PLAYER $50
            for individual in self.active_players:  # For each player...
                self.exchange_money(amount=50, giver=player, receiver=individual, summary="Chance.")
        elif card == 16:  # BANK PAYS YOU DIVIDEND OF $50
            self.exchange_money(amount=50, giver=self.bank, receiver=player, summary="Chance.")

        if card == 1 and self.chance_index == 15:  # GOOJF card was at the end.
            self.chance_index = 0  # Restart deck.
        elif card == 1:  # GOOJF card was somewhere else.
            pass  # Do not change index.
        else:
            self.chance_index = (self.chance_index + 1) % len(self.chance_cards)  # Increase index.

    # Moves a player ahead.
    def move_ahead(self, player, number_of_spaces):
        new_position = (player.position + number_of_spaces) % 40
        if new_position < player.position:  # Does the player pass Go?
            # The player collects $200 for passing Go.
            self.exchange_money(amount=200, giver=self.bank, receiver=player, summary="$200 from Go.")
            player.passed_go = True
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Moves a player to a specific spot.(Used in cards.)
    def move_to(self, player, new_position):
        if new_position < player.position:  # Does the player pass Go?
            # The player collects $200 for passing Go.
            self.exchange_money(amount=200, giver=self.bank, receiver=player, summary="$200 from Go.")
            player.passed_go = True  # Parameter for house rule.
        player.position = new_position  # Update the player's position.
        self.board[new_position].visits += 1  # Increase hit counter.

    # Allows money to be exchanged between players or money pools.
    def exchange_money(self, giver, receiver, amount, summary):
        # Exchange the money.
        giver.money -= amount
        receiver.money += amount

        # If a player's money total went negative, allow them to make funds.
        for current_party in [receiver, giver]:
            if current_party.money <= 0 and isinstance(current_party, Player):
                current_party.make_funds(game_info=self)

                # Check if the player lost.
                if current_party.money <= 0:
                    # Kick the player out.
                    self.move_again = False  # Stop the player's current turn.
                    self.inactive_players.append(current_party)  # And the player to the inactive players list.
                    self.active_players.remove(current_party)  # Remove the player from the active player's list.
                    self.num_active_players -= 1

                    # Identify why the player lost.
                    if summary[0] == "Paying rent.":
                        property = summary[1]
                        self.loss_reason = property.group
                    else:
                        self.loss_reason = summary

                    # If there are still other players, give away the player's assets.
                    if len(self.active_players) > 1:
                        # Find other party.
                        parties = [receiver, giver]
                        parties.remove(current_party)
                        other_party = parties[0]

                        # Determine who the player lost to.
                        if other_party == self.bank:
                            # The player lost to the bank.
                            self.bank += current_party.money
                            # TODO Auction off all properties.
                        else:
                            # The player lost to another player.
                            other_party.money += current_party.money
                            list_length = len(current_party.inventory)
                            for i in range(list_length):
                                self.update_inventories(player_from=current_party, player_to=other_party,
                                                        prop=next(iter(current_party.inventory)))
                            # Transfer GOOJF cards
                            if current_party.chance_card:
                                other_party.chance_card = True
                            if current_party.community_chest_card:
                                other_party.community_chest_card = True

    def other_player(self, playerA):
        for playerB in self.active_players:
            if playerB != playerA:
                return playerB
        return None

    def new_trading(self, player1, property):
        g1to2 = property.group
        p1to2 = property

        # Find the other player.
        player2 = self.other_player(player1)

        # Find how highly the group is ranked.
        group_rank = player1.group_ranking[g1to2]

        # Look at groups that are ranked better that player 1 might want.
        for g2to1 in player1.group_ordering[:group_rank]:
            # See if Player 2 has properties in the group
            if player2.group_inv[g2to1]:
                # Check that Player 2 will accept the group.
                if player2.group_ranking[g2to1] > player2.group_ranking[g1to2]:
                    mono1 = (len(player1.group_inv[g2to1]) + 1 - self.group_counts[g2to1] == 0)
                    mono2 = (len(player2.group_inv[g1to2]) + 1 - self.group_counts[g1to2] == 0)

                    if (mono1 and mono2) or (not mono1 and not mono2):
                        # Grab the first property in that Player 2 owns in the group.
                        p2to1 = player2.group_inv[g2to1][0]
                        self.update_inventories(player_from=player1, player_to=player2, prop=p1to2)
                        self.update_inventories(player_from=player2, player_to=player1, prop=p2to1)

                        if player1.number == 1:
                            # print(g1to2, "<-->", g2to1)
                            self.trades.append([p1to2, p2to1])
                        else:
                            # print(g2to1, "<-->", g1to2)
                            self.trades.append([p2to1, p1to2])

                        return


    def cont_trading(self, playerA):
        # Find the other player
        playerB = self.other_player(playerA)
        # Find what player A would like to get rid of.
        for gAtoB in reversed(playerA.group_ordering):
            # See what Player A would accept.
            for gBtoA in playerA.group_ordering:
                # They won't trade within groups.
                if gAtoB != gBtoA:
                    # See if player A has something and doesn't have a monopoly.
                    if 0 < len(playerA.group_inv[gAtoB]) < self.group_counts[gAtoB]:
                        # See if player B can agree.
                        if 0 < len(playerB.group_inv[gBtoA]) < self.group_counts[gBtoA]:
                            mono1 = (len(playerA.group_inv[gBtoA]) + 1 - self.group_counts[gBtoA] == 0)
                            mono2 = (len(playerB.group_inv[gAtoB]) + 1 - self.group_counts[gAtoB] == 0)

                            if (mono1 and mono2) or (not mono1 and not mono2):
                                # See how much player B will contribute so the deal makes sense for him. (Signed)
                                money_available_for_playerB = max(playerB.money - playerB.get_buying_threshold(self), 0)
                                money_playerB_could_contribute = (playerB.group_values[gAtoB] - playerB.group_values[
                                    gBtoA]) / 2
                                deal_money = min(money_playerB_could_contribute, money_available_for_playerB)
                                print(deal_money)

                                # See if player A can afford the deal.
                                if deal_money + playerA.money - playerA.get_buying_threshold(self) > 0:
                                    benefitA = playerA.group_values[gBtoA] + 2 * deal_money - playerA.group_values[
                                        gAtoB]
                                    # See if player A gets a benefit out of this deal.
                                    if benefitA > 0:
                                        # Make the deal!
                                        for pAtoB in list(playerA.group_inv[gAtoB]):
                                            for pBtoA in list(playerB.group_inv[gBtoA]):
                                                self.update_inventories(player_from=playerA, player_to=playerB,
                                                                        prop=pAtoB)
                                                self.update_inventories(player_from=playerB, player_to=playerA,
                                                                        prop=pBtoA)
                                                self.exchange_money(giver=playerB, receiver=playerA, amount=deal_money,
                                                                    summary="Making a trade.")
                                                self.trade_count += 1
                                                if playerA.number == 1:
                                                    self.trades.append([pAtoB, pBtoA])
                                                else:
                                                    self.trades.append([pBtoA, pAtoB])
                                                return
                                                # print(gAtoB,gBtoA)


    # When a property is transferred from one player to another (including the Bank),
    # update player inventories (both list and dictionary forms) and monopoly lists.
    # Also update the list of unowned properties.
    def update_inventories(self, player_from, player_to, prop):
        if player_from == "Bank":
            # Update inventory, group_inv for player_to.
            player_to.group_inv[prop.group].append(prop)
            player_to.inventory.add(prop)

            # Update set of monopolies
            if len(player_to.group_inv[prop.group]) == self.group_counts[prop.group]:
                player_to.add_monopoly(prop.group)

            # Update property owner.
            prop.owner = player_to

            # Check if it was mortgaged in an auction.
            if prop.mortgaged:
                player_to.mortgaged_properties.add(prop)
            else:
                player_to.rent_power += self.calculate_rent(prop)

        else:
            # Update inventory, group_inv, for player_to.
            player_to.group_inv[prop.group].append(prop)
            player_to.inventory.add(prop)

            # Now remove from inventories.
            player_from.group_inv[prop.group].remove(prop)
            player_from.inventory.remove(prop)

            if len(player_to.group_inv[prop.group]) == self.group_counts[prop.group]:
                player_to.add_monopoly(prop.group)

            # Update property owner.
            prop.owner = player_to


            # Check if the property was mortgaged.
            if prop.mortgaged:
                player_to.mortgaged_properties.add(prop)
                player_from.mortgaged_properties.remove(prop)
            else:
                rent = self.calculate_rent(prop)
                player_from.rent_power -= rent
                player_to.rent_power += rent



    # Determines if the player owns all of the properties in the the given property's group.
    def monopoly_status(self, player, current_property, add_me=0):
        # Find the name of the property's group.
        group = current_property.group

        # There are no monopolies for board spaces, railroads or utilities.
        if group in ["", "Railroad", "Utility"]:
            return False  # The property is not in a color group.
        else:
            if len(player.group_inv[group]) + add_me - self.group_counts[group] == 0:
                return True

        return False

    # Determines if the player owns all of the properties in the the given property's group.
    def quick_monopoly_status(self, player, current_property, add_me=0):
        # Find the name of the property's group.
        group = current_property.group
        if len(player.group_inv[group]) + add_me - self.group_counts[group] == 0:
            return True

        return False

    # Sends a player to jail.
    def go_to_jail(self, player):
        player.position = 10  # Move player.
        self.board[10].visits += 1  # Increase hit counter for jail.
        self.move_again = False  # Prevent the player from moving again.
        player.in_jail = True  # Set the player's Jail status to true.
        player.set_jail_strategy(self)  # Allow the player to make strategy decisions.

    # Has a player buy a property.
    def buy_property(self, player, board_space, custom_price=False):
        # Allows a property to be bought at a custom price (used in auctions).
        if custom_price:
            self.exchange_money(amount=custom_price, giver=player, receiver=self.bank, summary="Buying property.")
        else:
            # Pay the money for the property.
            self.exchange_money(amount=board_space.price, giver=player, receiver=self.bank,
                                summary="Paying property at auction.")

        self.update_inventories(player_from="Bank", player_to=player, prop=board_space)

        if self.trading_enabled:
            self.new_trading(property=board_space, player1=player)
            pass

    # Determines the owner of a property.
    def property_owner(self, property):
        return property.owner

    # Determines the rent owed on a property.
    def calculate_rent(self, property):
        owner = property.owner
        # Rent for Railroads.
        if property.group == "Railroad":
            rent = 25 * pow(2, len(owner.group_inv["Railroad"]) - 1)  # The rent.

        # Rent for Utilities.
        elif property.group == "Utility":
            utility_counter = len(owner.group_inv["Utility"])
            if utility_counter == 2:
                rent = 70  # If the player owns both utilities, pay 10 times the dice.
            else:
                rent = 28  # If the player owns one utility, pay 4 times the dice.

        # Rent for color-group properties.
        else:
            if property.buildings == 5:  # Check to see if there is a hotel.
                rent = property.rents[5]  # Pay the 5th rent for a hotel.
            elif 0 < property.buildings < 5:  # The property has houses.
                rent = property.rents[property.buildings]
            else:
                if property.group in owner.monopolies:  # If the player has a monopoly...
                    rent = property.rents[0] * 2  # Rent is doubled.
                else:  # The player does not have a monopoly.
                    rent = property.rents[0]

        return rent

    def calculate_rent_proportion(self, property):
        # Rent for Railroads.
        if property.group == "Railroad":
            max_rent = 200
            rent = self.calculate_rent(property)  # 200
        # Rent for Utilities.
        elif property.group == "Utility":
            rent = 70
            max_rent = self.calculate_rent(property)  # 70

        # Rent for color-group properties.
        else:
            max_rent = property.rents[5]
            rent = self.calculate_rent(property)

        return rent / max_rent


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
            rent = 25 * pow(2, len(owner.group_inv['Railroad']) - 1)  # The rent.
            if player.card_rent:  # Rent is double for the railroad cards.
                rent *= 2

        # Rent for Utilities.
        elif current_property.group == "Utility":
            # Roll the dice.
            die1 = randint(1, 6)
            die2 = randint(1, 6)
            self.dice_roll = die1 + die2

            # Check for snakes eyes.
            if self.snake_eyes_bonus and die1 == 1 == die2:
                self.exchange_money(amount=500, giver=self.bank, receiver=player, summary="Snake eyes bonus.")

            utility_counter = owner.group_inv['Utility']
            if utility_counter == 2 or player.card_rent:
                rent = self.dice_roll * 10  # If the player owns both utilities, pay 10 times the dice.
            else:
                rent = self.dice_roll * 4  # If the player owns one utility, pay 4 times the dice.

        # Rent for color-group properties.
        else:
            if 0 < current_property.buildings <= 5:  # The property has houses or a hotel.
                rent = current_property.rents[current_property.buildings]
            else:
                if current_property.group in owner.monopolies:  # If the player has a monopoly...
                    rent = current_property.rents[0] * 2  # Rent is doubled.
                else:  # The player does not have a monopoly.
                    rent = current_property.rents[0]

        # Pay the rent.
        summary = ["Paying rent on", current_property]
        self.exchange_money(amount=rent, giver=player, receiver=owner, summary=summary)


    # Handles auctions when a property is not bought.
    def auction(self, board_space):
        # Each player makes a bid on the property.
        for current_player in self.active_players:
            current_player.make_bid(game_info=self, property=board_space)

        # The two-player case.
        player1 = self.active_players[0]
        player2 = self.active_players[1]

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

        # The bids tie. A random player buys the property.
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
            return

        winning_player.make_auction_funds(winning_bid=winning_bid, property=board_space, game_info=self)
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
        if board_space.mortgaged or board_space.owner == player:
            return  # The property is mortgaged or the player owns the property. Nothing happens.
        elif board_space.owner == None:  # The property is unowned.
            if self.trip_to_start and (not player.passed_go):
                return  # The player has to wait to pass Go to buy/auction a property.
            else:  # The player can buy it.
                if not player.unowned_property_action(game_info=self, property=board_space):
                    # The player can't buy it or decides not to.
                    if self.auctions_enabled:  # If auctions are enabled...
                        self.auction(board_space)  # The property is auctioned.
        else:  # The property is owned by another player.
            self.pay_rent(player)  # The player pays the owner rent.

    def board_action(self, player, board_space):
        if board_space.is_property:
            # The player landed on a property.
            self.property_action(player, board_space)

        elif board_space.name == "Chance":
            self.chance(player)  # Draw card and make action.

        elif board_space.name == "Community Chest":
            self.community_chest(player)  # Draw card and make action.

        elif board_space.name == "Go":
            # Give the player an extra $200 if the house rule is enabled.
            if self.double_on_go:
                self.exchange_money(amount=200, giver=self.bank, receiver=player,
                                    summary="Got extra $200 for landing on Go.")

        elif board_space.name == "Income Tax":
            # The player pays $200.  The '10% of all assets' option was removed in 2008.
            self.exchange_money(amount=200, giver=player, receiver=self.free_parking, summary="Income Tax.")

        elif board_space.name == "Free Parking":
            if self.free_parking_pool:  # Check to see if the Free Parking pool is enabled.
                # The player takes the money in Free Parking.
                self.exchange_money(amount=self.free_parking.money, giver=self.free_parking, receiver=player,
                                    summary="Received Free Parking pool.")

        elif board_space.name == "Go to Jail":
            self.go_to_jail(player)  # The player goes to jail.

        elif board_space.name == "Luxury Tax":
            # The player pays a $100 tax.
            self.exchange_money(amount=100, giver=player, receiver=self.free_parking, summary="Luxury Tax.")

        else:
            pass  # Nothing happens on Just Visiting.

        # Reset this variable.
        player.card_rent = False

    # An individual player takes a turn.
    def take_turn(self, player):
        self.turn_counter += 1  # Increase master turn counter
        self.doubles_counter = 0  # Reset doubles counter.

        # Track the player's money.
        # player.money_changes.append(player.money)

        # Is the player in jail?
        if player.in_jail:  # Player is in jail.
            player.jail_counter += 1  # Increase the jail turn counter
            if player.jail_decision(self):
                player.jail_counter = 0  # Reset the jail counter.
                player.pay_out_of_jail(game_info=self)  # Pay out using a card or $50.
            else:
                # Roll the dice.
                die1 = randint(1, 6)
                die2 = randint(1, 6)
                self.dice_roll = die1 + die2

                # Check for snake eyes.
                if self.snake_eyes_bonus and die1 == 1 == die2:
                    self.exchange_money(amount=500, giver=self.bank, receiver=player, summary="Snake eyes bonus.")

                # Make an action.
                if die1 == die2:  # The player rolled doubles.
                    player.jail_counter = 0  # Reset the jail counter.
                    self.move_again = True  # The player can move out of jail
                elif die1 != die2 and player.jail_counter == 3:
                    player.jail_counter = 0  # Reset the jail counter.
                    player.pay_out_of_jail(game_info=self)  # Pay out using a card or $50.
                else:  # The player didn't roll doubles.
                    return  # The player can not move around the board.

        if player.money > 0:  # If the player did not go broke coming out of jail!
            self.move_again = True  # Initial condition.

        # The main loop.
        while self.move_again:
            self.move_again = False

            # Roll the dice.
            die1 = randint(1, 6)
            die2 = randint(1, 6)
            self.dice_roll = die1 + die2

            # Check for snakes eyes.
            if self.snake_eyes_bonus and die1 == 1 == die2:
                self.exchange_money(amount=500, giver=self.bank, receiver=player, summary="Snake eyes bonus.")

            # Check for doubles.
            if player.in_jail:
                player.in_jail = False  # The player is no longer in jail, but can not move again regardless.
            elif die1 == die2:
                self.doubles_counter += 1  # Increase the doubles counter.
                if self.doubles_counter == 3:  # The players is speeding.
                    self.go_to_jail(player)
                    return  # The function ends.
                self.move_again = True  # The player can move again.

            self.move_ahead(player, self.dice_roll)  # Move the player
            board_space = self.board[player.position]  # Find the current board space.
            self.board_action(player, board_space)  # Make an action based on the current board space.

            # If a card or board space brought the player to jail, end the function.
            if player.in_jail:
                return


    # Plays a game object.
    def play(self):
        # Shuffle the players.
        shuffle(self.active_players)

        # Initial condition.
        current_player_index = 0

        # Store starting player for reference.
        self.starting_player = self.active_players[0].number

        # Game loop. Continue if there is more than 1 player and we haven't reached the cutoff.
        while self.num_active_players > 1 and self.turn_counter < self.cutoff:
            if self.image_exporting:
                if self.turn_counter % self.image_exporting == 0:
                    exportBoard(self)

            # Create list of players starting with the player who is going.
            self.development_order = []
            self.development_order.extend(self.active_players[current_player_index - 1:])
            self.development_order.extend(self.active_players[:current_player_index - 1])

            # Allow the player to develop and un-mortgage properties.
            for player in self.development_order:
                player.between_turns(game_info=self)
                # self.cont_trading(playerA=player)

            # Current player takes turn.
            self.take_turn(self.active_players[current_player_index])

            # Update current_player_index.
            current_player_index = (current_player_index + 1) % self.num_active_players

        # # # The game has ended # # #
        if self.image_exporting:
            self.active_players.extend(self.inactive_players)
            exportBoard(self)
            for player in self.inactive_players:
                self.active_players.remove(player)

        # Find all monopolies.
        all_monopolies = []
        for player in self.active_players:
            all_monopolies.extend(player.monopolies)
        for player in self.inactive_players:
            all_monopolies.extend(player.monopolies)

        # Identify the winner.
        if self.num_active_players == 1:
            self.winner = self.active_players[0].number
        else:  # It was tie.
            self.winner = 0
            self.loss_reason = "Tie"

        # Ending report.
        results = {'winner': self.winner,
                   'length': self.turn_counter,
                   'end behavior': self.loss_reason,
                   'monopolies': all_monopolies,
                   'started': self.starting_player,
                   'players': self.active_players,
                   'trade count': self.trade_count
        }
        return results

