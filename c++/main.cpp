/*
 * =====================================================================================
 *
 *       Filename:  main.cpp
 *
 *    Description:  Runs Monopoly simulations
 *
 *        Version:  1.0
 *        Created:  Sep 15, 2014 7:40:44 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */

#include<iostream>
#include<vector>
#include<algorithm>
#include<unordered_set>
#include<cstdlib>
#include<ctime>
#include "game.h"
#include "player.h"

const int NUMBER_OF_GAMES = 1000;
const int NUMBER_OF_TURNS = 1000;
std::string CRAPPY_MONOPOLY = "Brown";
std::unordered_set<std::string*> noPrefs;


Player* generateRandomPlayer(int number)
{
    std::srand((int) std::time(NULL) + rand());
    return new Player(number, noPrefs, std::rand() % 500 + 1, std::rand() % 6, std::rand() % 3, std::rand() % 1, std::rand() % 2, std::rand() % 2); // check all these
}

void pyMain()
{
	Player goodPlayer1(1, noPrefs, 100, 5, 0, true, 1, 1);
	Player grandma(2, noPrefs, 1000, 5, 3, false, 0, 0);

	int resultsList[NUMBER_OF_GAMES];


	for (int i = 0; i < NUMBER_OF_GAMES; i++)
	{
		goodPlayer1.resetValues();
		grandma.resetValues();
		std::vector<Player*> players = {&goodPlayer1, &grandma};
		Game gameObject(players, NUMBER_OF_TURNS);
		resultsList[i] = gameObject.play().result;
	}

	std::cout << (std::count(resultsList, resultsList + NUMBER_OF_GAMES, 1) * 100 / NUMBER_OF_GAMES) << "%" << std::endl;
}

void monopolyTest()
{
	Player player1(1, noPrefs, 1000, 5, 3, false, 0, 0);
	Player player2(2, noPrefs, 1000, 5, 3, false, 0, 0);

	int endedEarlyNoMonopolies = 0;
	int finishedGamesWithNoMonopolies = 0;

	int resultsList[NUMBER_OF_GAMES];

	for (int i = 0; i < NUMBER_OF_GAMES; i++)
	{
		player1.resetValues();
		player2.resetValues();
		std::vector<Player*> players = {&player1, &player2};
		Game gameObject(players, NUMBER_OF_TURNS);

		endReport results = gameObject.play();
		resultsList[i] = results.result;

		if (0 == results.result)
		{
			if ((results.player0Monopolies.empty() && results.player1Monopolies.empty()) || (results.player0Monopolies.find(&CRAPPY_MONOPOLY) != results.player0Monopolies.end() && results.player0Monopolies.size() == 1) || (results.player1Monopolies.find(&CRAPPY_MONOPOLY) != results.player1Monopolies.end() && results.player1Monopolies.size() == 1))
			{
				endedEarlyNoMonopolies++;
			}
			else
			{
//				std::cout << "Resultant monos: TBD" << std::endl;
			}
		}

		else
		{
			if ((results.player0Monopolies.empty() && results.player1Monopolies.empty()) || (results.player0Monopolies.find(&CRAPPY_MONOPOLY) != results.player0Monopolies.end() && results.player0Monopolies.size() == 1) || (results.player1Monopolies.find(&CRAPPY_MONOPOLY) != results.player1Monopolies.end() && results.player1Monopolies.size() == 1))
			{
				finishedGamesWithNoMonopolies++;
			}
		}
	}

	std::cout << "Ended early: " << std::count(resultsList, resultsList + NUMBER_OF_GAMES, 0) << std::endl;
	std::cout << "Ended early & no monos or just brown: " << endedEarlyNoMonopolies << std::endl;
	std::cout << "Finished games with no monos or just brown: " << finishedGamesWithNoMonopolies << std::endl;
}

void playSet(Player* basePlayer, int numberOfGames, Player* staticOpponent, int* results)
{
    if (staticOpponent != NULL)
    {
        for (int i = 0; i < numberOfGames; i++)
        {
            Player* player1 = basePlayer;
            player1->resetValues();
            
            Player* opponent = staticOpponent;
            opponent->resetValues();
            opponent->setNumber(2);
            
             // Let's play!
            std::vector<Player*> players = {player1, opponent};
            Game currentGame(players, NUMBER_OF_TURNS);
            results[i] = currentGame.play().result;
        }
    }
    
    else
    {
        for (int i = 0; i < numberOfGames; i++)
        {
            Player* player1 = basePlayer;
            player1->resetValues();
            
            Player* opponent = generateRandomPlayer(2);
            
            // Let's play!
            std::vector<Player*> players = {player1, opponent};
            Game currentGame(players, NUMBER_OF_TURNS);
            results[i] = currentGame.play().result;
            
            delete opponent;
        }
    }
}

int successIndicator(Player* basePlayer, int numberOfGames = 1000, int procs = 2, Player* staticOpponent = NULL)
{
    int results[numberOfGames];
    
    // Do processes later.
    playSet(basePlayer, numberOfGames, staticOpponent, results);
    
    return (int) std::count(results, results + numberOfGames, 1) / numberOfGames; // ?
}

void shortBruteForce(int numberOfGames=5000)
{
    std::unordered_set<std::string*> noPrefs;

    for (int jailtime = 0; jailtime < 4; jailtime++)
    {
        for (int smartJailStrategy = 0; smartJailStrategy < 2; smartJailStrategy++)
        {
            for (int completeMonopoly = 0; completeMonopoly < 3; completeMonopoly++)
            {
                for (int developmentThreshold = 0; developmentThreshold < 3; developmentThreshold++)
                {
                    Player player(1, noPrefs, 100, 5, jailtime, smartJailStrategy, completeMonopoly, developmentThreshold);
                    std::cout << successIndicator(&player, numberOfGames, 4) << std::endl;
                }
            }
        }
    }
}

int main()
{
	std::clock_t begin = std::clock();
	pyMain();
	monopolyTest();
//    shortBruteForce();
	std::clock_t end = clock();
	double elapsedSecs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "Time elapsed: " << elapsedSecs << std::endl;
	return (0);
}
