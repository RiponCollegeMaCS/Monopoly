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

#include <algorithm>
#include <ctime>
#include <iostream>
#include <stdlib.h>
#include <unordered_set>
#include <vector>

#include "game/game.h"
#include "stats/success.h"

using namespace Monopoly;

std::string CRAPPY_MONOPOLY = "Brown";
std::unordered_set<std::string*> noPrefs;

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
		resultsList[i] = gameObject.play().winner;
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
		resultsList[i] = results.winner;

		if (0 == results.winner)
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



int main(int argc, char** argv)
{
	if (argc > 1)
	{
		if (argc == 8) // we have player options here
		{
			// Note that the first element in argv is
			// the program name (I think?)
			int params[7];
			for (int i = 0; i < 7; i++)
			{
				params[i] = std::atoi(argv[i+1]);
			}
			std::cout << successIndicator(params) << std::endl;
		}
	}
	else
	{
//		std::clock_t begin = std::clock();
//		pyMain();
//		monopolyTest();
		shortBruteForce(NUMBER_OF_GAMES/8);
//		std::clock_t end = clock();
//		double elapsedSecs = double(end - begin) / CLOCKS_PER_SEC;
//		std::cout << "Time elapsed: " << elapsedSecs << std::endl;
	}
	return (0);
}
