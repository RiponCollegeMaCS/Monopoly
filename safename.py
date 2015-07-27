__author__ = 'Mitchell Eithun'
# Convert a team name to a safer alternative.
def safe_name(name):
    new_name = ""
    for character in name:
        if character == "&":
            new_name += "and"
        elif character == "'" or character == "`":
            new_name += ""
        elif character == "_" or character == " ":
            new_name += ""
        else:
            new_name += character
    return new_name
