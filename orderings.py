__author__ = 'Mitchell Eithun'
from random import shuffle


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    return ('Railroad', 'Orange', 'Light Blue', 'Pink', 'Brown', 'Utility', 'Dark Blue', 'Red', 'Green', 'Yellow')


def best_ordering_archive():
    other_groups = ["Pink", "Red",
                    "Yellow", "Green",
                    "Dark Blue", "Utility", "Brown"]
    shuffle(other_groups)

    return tuple(["Railroad", "Light Blue", "Orange"] + other_groups)
