//
//  success.cpp
//  Monopoly
//
//  Created by Braxton Schafer on 9/21/14.
//  Copyright (c) 2014 Braxton Schafer. All rights reserved.
//

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <functional>
#include <future>
#include "stats/success.h"
#include "game/player.h"
#include "game/game.h"
#include "util/csv.h"

std::unordered_set<std::string*> noGroupPrefs;

Player* generateRandomPlayer(int number)
{
    std::srand((int) std::time(NULL) + rand());
    return new Player(number, noGroupPrefs, std::rand() % 500 + 1, std::rand() % 6, std::rand() % 4, std::rand() % 2, std::rand() % 3, std::rand() % 3); // check all these
}

int sumArray(int results[], int numberResults)
{
    int sum = 0;
    for (int i = 0; i < numberResults; i++)
    {
        sum += results[i];
    }
    
    return (sum);
}

int playSet(const int* basePlayer, int numberOfGames)
{
    int num1won = 0;
    
//    if (staticOpponent != NULL)
//    {
//        for (int i = 0; i < numberOfGames; i++)
//        {
//            Player player1(basePlayer);
//
//            Player* opponent = staticOpponent;
//            opponent->resetValues();
//            opponent->setNumber(2);
//
//            // Let's play!
//            std::vector<Player*> players = {&player1, opponent};
//            Game currentGame(players, NUMBER_OF_TURNS);
//            int winner = currentGame.play().winner;
//            results[i] = winner;
//            if (1 == winner)
//            {
//                num1won++;
//            }
//        }
//    }
    
//    else
//    {

//    std::vector<std::future<Game>> futures;

    for (int i = 0; i < numberOfGames; i++)
        {
            Player player1(basePlayer);

            Player* opponent = generateRandomPlayer(2);

            // Let's play!
            std::vector<Player*> players = {&player1, opponent};
            Game currentGame(players, NUMBER_OF_TURNS);
//            futures.push_back(std::async(std::launch::async, &Game::play, &currentGame));
            int winner = currentGame.play().winner;
//            results[i] = winner;
            if (1 == winner)
            {
                num1won++;
            }
            
            delete opponent;
        }

//    for (auto &t : futures)
//    {
//        int winner = t.get().winner;
//
//        if (1 == winner)
//        {
//            num1won++;
//        }
//    }
//    }
    
    return (num1won);
}

float successIndicator(const int* basePlayer, int numberOfGames = 1000, int procs = 2, Player* staticOpponent = NULL)
{
    int results[numberOfGames];
    int success = 0;

    std::vector<std::future<int>> futures;

    for (int i = 0; i < procs; i++)
    {
        futures.push_back(std::async(&playSet, basePlayer, numberOfGames / procs));
    }

    for (auto &i : futures)
    {
        success += i.get();
    }
//    int success = playSet(basePlayer, numberOfGames, staticOpponent, results);

//        std::vector<std::thread> threads;
//
//        for (int i = 0; i < procs; i++)
//        {
//            threads.push_back(std::thread(playSet, std::ref(basePlayer), numberOfGames / 4, std::ref(staticOpponent), results));
//        }
//
//        for (auto i : threads)
//        {
//            i.join();
//        }
    
    return ((float) success / (float) numberOfGames);
}

void shortBruteForce(int numberOfGames=5000)
{
    std::unordered_set<std::string*> noGroupPrefs;
    CSV results("/Users/braxton/Development/git/monopoly/c++/src/success.csv");
    
    for (int jailtime = 0; jailtime < 4; jailtime++)
    {
        for (int smartJailStrategy = 0; smartJailStrategy < 2; smartJailStrategy++)
        {
            for (int completeMonopoly = 0; completeMonopoly < 3; completeMonopoly++)
            {
                for (int developmentThreshold = 0; developmentThreshold < 3; developmentThreshold++)
                {
//                    Player player(1, noGroupPrefs, 100, 5, jailtime, smartJailStrategy, completeMonopoly, developmentThreshold);
                    int params[7] = { 1, 100, 5, 0, 0, 0, 0 }; // send parameters to thread
                    float s = successIndicator(params, numberOfGames, 4);
//                    results.writeline(player.getInfo(), s);
                    std::cout << s << std::endl;
                };
            }
        }
    }
}
