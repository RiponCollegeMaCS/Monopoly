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
#include "game.h"
#include "player.h"

void pyMain()
{
	std::unordered_set<std::string*> noPrefs;
	Player goodPlayer1(1, noPrefs, 100, 5, 0, true, 1, 1);
	Player grandma(2, noPrefs, 1000, 5, 3, false, 0, 0);

	int numberOfGames = 1000;
	int resultsList[1000];


	for (int i = 0; i< numberOfGames; i++)
	{
		goodPlayer1.reset_values();
		grandma.reset_values();
		std::vector<Player*> players = {&goodPlayer1, &grandma};
		Game gameObject(players, 1000);
		resultsList[i] = gameObject.play().result;
	}

	std::cout << (std::count(resultsList, resultsList + 1000, 1) * 100 / 1000) << "%" << std::endl;
}

int main()
{
	pyMain();
	return (0);
}
