"""
# Import csv commands.
#import csv
board_spaces=['']
with open('board_data.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for col in row:
            board_spaces.append(Board_Location(row))

print(board_spaces[40].name)
"""

"""
class Property(Board_Location):
    def __init__(self, cost, rent, house_cost, color_group):
        self.rent = rent # How much it costs to buy the property.
        self.house_cost = house_cost # How much it costs for a house.
        self.color_group = color_group # Which group the property belongs to.
        self.houses = 0 # The property starts with no houses.
        self.hotels = 0 # The property starts with no hotels.
        self.owner = 0 # The property is unowned.
"""