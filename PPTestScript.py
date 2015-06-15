# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 10:39:02 2015

@author: mckenzielamb
"""
from multiprocessing import *
import monopoly
from timer import *

def PlaySimpleSet(games_in_a_set=1000):
    counter = 0
    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=500)
        player2 = monopoly.Player(2, buying_threshold=500)
        game0 = monopoly.Game([player1, player2], cutoff=1000, new_trading=True)
        results = game0.play()

        # Store length.
        if results['winner'] == 1:
            counter += 1
    return counter / games_in_a_set
    


def PlaySet(results_q, games_in_a_set=1000):
    counter = 0
    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=500)
        player2 = monopoly.Player(2, buying_threshold=500)
        game0 = monopoly.Game([player1, player2], cutoff=1000, new_trading=True)
        results = game0.play()

        # Store length.
        if results['winner'] == 1:
            counter += 1
    results_q.put(counter / games_in_a_set)


def PlaySetParallel(number_of_games=1000, procs=4, static_opponent=False):
    results_q = Queue()  # Queue for results.
    proc_list = [Process(target=PlaySet, args=(results_q, number_of_games // procs))
                 for i in
                 range(procs)]  # List of processes.
    for proc in proc_list:  # Start all processes.
        proc.start()
    for proc in proc_list:  # Wait for all processes to finish.
        proc.join()
    results_list = []

    # Gather the results from each process in a list of counts.
    while results_q.empty() == False:
        results_list.append(results_q.get())
    # Success rate = total count / total number of games
    success_rate = float(sum(results_list)) / float(number_of_games)
    return 100 * success_rate

def PlayGame(game_number):
    player1 = monopoly.Player(1, buying_threshold=500)
    player2 = monopoly.Player(2, buying_threshold=500)
    game0 = monopoly.Game([player1, player2], cutoff=1000, new_trading=True)
    return game0.play()['winner']

def PlaySetParallel2(number_of_games=1000, procs=4, static_opponent=False):
    pool = Pool(processes=procs)
    results_list = pool.map(PlayGame, range(number_of_games))
    #print(results_list[0:10])
    
def TimeTest():
    timer()
    print(PlaySimpleSet(100))
    timer()