from PIL import ImageFont, Image, ImageDraw, ImageEnhance

# Colors on the board.
colors = {
    'Brown': (153, 102, 51),
    'Light Blue': (197, 216, 241),
    'Pink': (214, 0, 147),
    'Orange': (247, 150, 70),
    'Red': (192, 0, 0),
    'Yellow': (255, 255, 0),
    'Green': (0, 176, 80),
    'Dark Blue': (0, 112, 192),
    'Board': (198, 239, 206),
    'Gray': (225, 225, 225),
    'Border': (0, 0, 0)
}


# Use the pseudo-monopoly font.
def font(size=10):
    return ImageFont.truetype("C:/Windows/Fonts/Kabel-Heavy.ttf", int(size))


# Find the side of the board a property is on.
def find_side(num):
    if 0 <= num < 10:
        return 0
    elif 10 <= num < 20:
        return 1
    elif 20 <= num < 30:
        return 2
    else:
        return 3


# Return the color for that player.
def player_color(num):
    num = int(num)
    if num == 1:
        return 'Blue'
    elif num == 2:
        return 'Red'
    else:
        return colors['Board']


# Draw a skinny board space.
def draw_space(size, space, game):
    # Find dimensions of space.
    size = int(size)
    width = size
    height = size * 2
    white_height = int(0.8 * height)  # The open green part of the space.
    strip_height = height - white_height  # The colored strip

    # Create base image
    if space.group == "Railroad":
        board_space = Image.open("images/src/railroad.png").resize((width, height), Image.ANTIALIAS)
    elif space.name == "Electric Company":
        board_space = Image.open("images/src/company.png").resize((width, height), Image.ANTIALIAS)
    elif space.name == "Water Works":
        board_space = Image.open("images/src/waterworks.png").resize((width, height), Image.ANTIALIAS)
    else:
        board_space = Image.new("RGBA", (width, height))

    # See if the property is owned
    player_num = False  # "Ø"
    if space.owner != None:
        player_num = str(space.owner.number)


    # Convert to draw.
    draw = ImageDraw.Draw(board_space)

    # Draw regions.
    if space.group in ["Railroad", "Utility"]:
        for i in range(round(size / 65)):
            # Draw border.
            draw.rectangle(xy=(i, i, width - 1 - i, height - 1 - i), outline=colors['Border'])
    else:
        # For all other properties.
        for i in range(round(size / 65)):
            draw.rectangle(xy=(i, white_height + i, width - 1 - i, height - 1 - i), fill=colors[space.group],
                           outline=colors['Border'])
            draw.rectangle(xy=(i, i, width - 1 - i, white_height - 1 - i), fill=colors['Board'],
                           outline=colors['Border'])

    # Store how many buildings we have.
    buildings = space.buildings

    # The property has a hotel.
    if buildings == 5:
        # Open hotel image and resize accordingly.
        hotel_raw = Image.open("images/src/hotel3.png")
        hotel = hotel_raw.resize((int(width / 4), int(strip_height)), Image.ANTIALIAS)
        hotel = hotel.rotate(angle=180)

        # Add hotel image to property.
        offset = int((width - (width / 4)) / 2)
        board_space.paste(hotel, (offset, int(white_height)), mask=hotel)

    # The property has a house.
    elif 1 <= buildings <= 4:
        # Open house image and resize accordingly.
        house_raw = Image.open("images/src/house3.png")
        house = house_raw.resize((int(width / 4), int(strip_height)), Image.ANTIALIAS)
        house = house.rotate(angle=180)

        # Add houses to property.
        offset = int((width - (buildings * (width / 4))) / 2)
        for i in range(buildings):
            board_space.paste(house, (offset + int(width / 4) * i, int(white_height)), mask=house)

    # Add player token.
    for player in game.active_players:
        if player.position == space.id:
            draw.ellipse((width / 3, 0, width / 3 + width / 3, width / 3),
                         fill=player_color(player.number),
                         outline=colors['Border']
            )

    # Find the side of the board the property is on.
    side = find_side(space.id)

    # Rotate the image to the correct orientation.
    board_space = board_space.rotate(angle=(4 - side) * 90)

    # The procedure to add the owner to the property.
    if player_num:
        # Load font.
        myfont = font(size * 0.8)

        # Convert to draw.
        draw = ImageDraw.Draw(board_space)

        # See where to place text.
        tsize = draw.textsize(player_num, myfont)

        if side == 0:
            center_coordinates = ((width - tsize[0]) / 2, (white_height - tsize[1]) / 2)
        elif side == 1:
            center_coordinates = (strip_height + (white_height - tsize[0]) / 2, (width - tsize[1]) / 2)
        elif side == 2:
            center_coordinates = ((width - tsize[0]) / 2, strip_height + (white_height - tsize[1]) / 2)
        else:
            center_coordinates = ((white_height - tsize[0]) / 2, (width - tsize[1]) / 2)

        for i in range(1, 3):
            draw.text((center_coordinates[0] + i, center_coordinates[1] + i), text=player_num, fill='Black',
                      font=myfont)

        draw.text(center_coordinates, text=player_num, fill=player_color(player_num), font=myfont)

        # Darken the entire image if the property is mortgaged.
        if space.mortgaged:
            board_space = ImageEnhance.Brightness(board_space).enhance(0.7)
            # draw.text(center_coordinates, text="x", fill=colors['Border'], font=myfont)


    # Return result.
    return board_space


# Create a blank tile for spaces that are not properties.
def blank_space(size, space, game):
    # Figure dimensions
    size = int(size)
    width = size
    height = size * 2
    side = find_side(space.id)

    if space.name == "Chance":
        board_space = Image.open("images/src/chance1.png").resize((size, 2 * size), Image.ANTIALIAS)
    elif space.name == "Community Chest":
        board_space = Image.open("images/src/communitychest.png").resize((size, 2 * size), Image.ANTIALIAS)
    elif space.name == "Luxury Tax":
        board_space = Image.open("images/src/luxurytax.png").resize((size, 2 * size), Image.ANTIALIAS)
    else:  # Create image.
        board_space = Image.open("images/src/incometax.png").resize((size, 2 * size), Image.ANTIALIAS)
        # board_space = Image.new("RGBA", (width, height))

    # Convert to draw.
    draw = ImageDraw.Draw(board_space)

    # Draw border and region
    for i in range(round(size / 65)):
        draw.rectangle(xy=(i, i, width - i - 1, height - i - 1), outline=colors['Border'])

    # Add player token.
    for player in game.active_players:
        if player.position == space.id:
            draw.ellipse((width / 3, 0, width / 3 + width / 3, width / 3),
                         fill=player_color(player.number),
                         outline=colors['Border']
            )



    # Rotate the image to the correct orientation.
    board_space = board_space.rotate(angle=(4 - side) * 90)

    return board_space


# Create a graphical representation of the board.
def exportBoard(game,size = 80):
    # The number of pixels alon the short side of a property


    # Calculate image dimension
    board_size = 13 * size

    # Create image.
    board = Image.new("RGBA", (board_size, board_size), color=colors['Board'])

    # Load corner images.
    go = Image.open("images/src/go.png").resize((2 * size, 2 * size), Image.ANTIALIAS)
    go_to_jail = Image.open("images/src/gotojail.png").resize((2 * size, 2 * size), Image.ANTIALIAS)
    free_parking = Image.open("images/src/freeparking.png").resize((2 * size, 2 * size), Image.ANTIALIAS)
    jail = Image.open("images/src/jail.png").resize((2 * size, 2 * size), Image.ANTIALIAS)

    # Place corner images.
    board.paste(go, (0, 0))
    board.paste(jail, (11 * size, 0))
    board.paste(free_parking, (11 * size, 11 * size))
    board.paste(go_to_jail, (0, 11 * size))



    # A place to store property sub-images
    board_space_images = []

    # Create all of skinny board spaces.
    for square in game.board:
        if square.is_property:
            space = draw_space(size, square, game)
        else:
            space = blank_space(size, square, game)

        # space.save("images/src/" + str(square.id) + ".png")
        board_space_images.append(space)


    # Place properties.
    # Side 0
    for i in range(1, 10):
        board.paste(board_space_images[i], (size * 2 + (i - 1) * size, 0))

    # Side 1
    for i in range(11, 20):
        board.paste(board_space_images[i], (11 * size, size * 2 + (i - 11) * size))

    # Side 2
    for i in range(21, 30):
        board.paste(board_space_images[50 - i], (size * 2 + (i - 21) * size, 11 * size))

    # Side 3
    for i in range(31, 40):
        board.paste(board_space_images[70 - i], (0, size * 2 + (i - 31) * size))

    draw = ImageDraw.Draw(board)


    # Add tokens to 4 corners.
    for player in game.active_players:
        # Go
        if player.position == 0:
            draw.ellipse((size / 3, 0, size / 3 + size / 3, size / 3),
                         fill=player_color(player.number),
                         outline=colors['Border'])
        # Jail
        elif player.position == 10:
            if not player.in_jail:
                draw.ellipse((size / 3 + (11 * size), 0, size / 3 + size / 3 + (11 * size), size / 3),
                             fill=player_color(player.number),
                             outline=colors['Border'])
            else:
                draw.ellipse((size / 3 + (11 * size), size, size / 3 + size / 3 + (11 * size), size / 3 + size),
                             fill=player_color(player.number),
                             outline=colors['Border'])

        # Free Parking
        elif player.position == 20:
            draw.ellipse(
                (size / 3 + (12 * size), 0 + (12 * size), size / 3 + size / 3 + (12 * size), size / 3 + (12 * size)),
                fill=player_color(player.number),
                outline=colors['Border'])

    # Enhance corner outlines.
    for i in range(round(size / 65)):
        draw.rectangle(xy=(i, i, 2 * size - i - 1, 2 * size - i - 1), outline=colors['Border'])
        draw.rectangle(xy=(11 * size + i, i, 11 * size + 2 * size - i - 1, 2 * size - i - 1), outline=colors['Border'])
        draw.rectangle(xy=(11 * size + i, 11 * size + i, 11 * size + 2 * size - i - 1, 11 * size + 2 * size - i - 1),
                       outline=colors['Border'])
        draw.rectangle(xy=(i, 11 * size + i, 2 * size - i - 1, 11 * size + 2 * size - i - 1), outline=colors['Border'])
        draw.rectangle(xy=(size * 2 + i, size * 2 + i, 11 * size - i - 1, 11 * size - i - 1),
                       outline=colors['Border'])  # Inner box

    # Enhance border.
    for i in range(round(size / 65), 2 * round(size / 65)):
        draw.rectangle(xy=(i, i, board_size - i - 1, board_size - i - 1), outline=colors['Border'])

    # Print turn counter.
    draw.text((3 * size, 3 * size), text=str(game.turn_counter), fill='Black', font=font(size=size))

    # Money amounts



    myfont = font(size=size / 1.5)
    for player in game.active_players:
        money_string = "$" + str(player.money)
        tsize = draw.textsize(money_string, myfont)

        draw.text((9 * size + (size - tsize[0]), (2 + player.number) * size), text=money_string,
                  fill=player_color(player.number), font=myfont)

    offset = 0
    myfont = font(size=size / 2)
    draw.text((3 * size, 4.5 * size), text="Trades", fill=colors['Border'], font=myfont)

    myfont = ImageFont.truetype("C:/Windows/Fonts/Kabel Regular.ttf", int(size / 3))
    for trade_pair in game.trades:
        #text = trade_pair[0].name + " <-> " + trade_pair[1].name
        #draw.text((3 * size, (5 + offset) * size), text=text, fill='Black', font=myfont)

        draw.text((3 * size, (5 + offset) * size), text=trade_pair[0].name, fill=player_color(1), font=myfont)
        draw.text((7 * size, (5 + offset) * size), text=trade_pair[1].name, fill=player_color(2), font=myfont)

        offset += (1 / 2)

    '''
    if game.active_players[0].number == 1:
        player1 = game.active_players[0]
        player2 = game.active_players[1]
    else:
        player1 = game.active_players[1]
        player2 = game.active_players[0]
    scalar = 3000  # player1.money + player2.money
    max_height = 9 * size
    # Player 1 money bar
    height2 = max_height * (player1.money / scalar)
    draw.rectangle(xy=(8 * size, int(size + ((size * 10) - height2)), 9 * size, 11 * size), outline='Black',
                   fill='Blue')
    thresh_height2 = max_height * (player1.buying_threshold / scalar)

    # Player 2 money bar
    height1 = max_height * (player2.money / scalar)
    draw.rectangle(xy=(9 * size, int(size + ((size * 10) - height1)), 10 * size, 11 * size), outline='Black',
                   fill='Red')
    thresh_height1 = max_height * (player2.buying_threshold / scalar)

    # Buying threshold.
    for i in range(2 * round(size / 65)):
        draw.line(
            (8 * size, int(size + ((size * 10) - thresh_height2)) + i, 9 * size,
             int(size + ((size * 10) - thresh_height2)) + i),
            fill='Black')

        draw.line(
            (9 * size, int(size + ((size * 10) - thresh_height1)) + i, 10 * size,
             int(size + ((size * 10) - thresh_height1)) + i),
            fill='Black')
        '''


    # Save image to file
    board.save("images/board" + str(game.turn_counter).zfill(4) + ".png")
    print("Exported board at", game.turn_counter, "turns")


    #################################################################

    '''# The property has a special symbol
    elif space.group in ['Railroad', "Utility"]:
        # Load the correct symbol
        if space.name == "Electric Company":
            icon_raw = Image.open("images/src/electric.png")
        elif space.name == "Water Works":
            icon_raw = Image.open("images/src/water.png")
        else:  # Railroad
            icon_raw = Image.open("images/src/train.png")

            # Process the symbol
        icon_raw = icon_raw.convert("RGBA")  # Convert the symbol to RGBA
        icon = icon_raw.resize((int(strip_height * 2), int(strip_height * 1.8)), Image.ANTIALIAS)  # Resize the symbol
        icon = icon.rotate(angle=180)  # Rotate the symbol

        # Position the symbol on the property.
        board_space.paste(icon, (int(height / 20), int(white_height / 1.4)), icon)


        # Create the colored overlays
        red = Image.new('RGB', board_space.size, color)


        # create a mask using RGBA to define an alpha channel to make the overlay transparent
        mask = Image.new('RGBA', board_space.size, (0, 0, 0, 150))

        board_space = Image.composite(board_space, red, mask).convert('RGB')'''
