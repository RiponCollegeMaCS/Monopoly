/*
 * =====================================================================================
 *
 *       Filename:  game.cpp
 *
 *    Description:  Does magic to play a game of Monopoly
 *
 *        Version:  1.0
 *        Created:  09/02/2014 13:53:59
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */

#include "game.h"
#include "player.h"
#include "boardlocation.h"

#include<iostream>
#include<string>
#include<vector>
#include<algorithm>

Game::Game(std::vector<Player> players, bool auct, bool fpp, bool dog, bool nrij, bool tts, bool seb, int cutoff=300)
{
	Game::players = players;
	Game::numberOfPlayers = (sizeof(Game::players)/sizeof(Game::players[0]));
	Game::auctionsEnabled = Game::auctionsEnabled && auct;
	Game::freeParkingPool = Game::freeParkingPool && fpp;
	Game::doubleOnGo = Game::doubleOnGo && dog;
	Game::noRentInJail = Game::noRentInJail && nrij;
	Game::tripToStart = Game::tripToStart && tts;
	Game::snakeEyesBonus = Game::snakeEyesBonus && seb;
	Game::cutoff = cutoff;
}

void Game::createCards()
	{
		for (int i = 0; i < NUMBER_OF_CARDS; i++)
		{
			chanceCards[i] = i + 1;
			communityChestCards[i] = i + 1;
		}

		std::random_shuffle(&chanceCards[0], &chanceCards[15]);
		std::random_shuffle(&communityChestCards[0], &communityChestCards[15]);
	}

void Game::createBoard()
	{

		board.push_back(BoardLocation(0, "Go"));
		board.push_back(BoardLocation(1, "Mediterranean Ave.", 60, "Brown", std::vector<int> {2, 10, 30, 90, 160, 250} , 50));
		board.push_back(BoardLocation(2, "Community Chest"));
		board.push_back(BoardLocation(3, "Baltic Ave.", 60, "Brown", std::vector<int> {4, 20, 60, 180, 320, 450}, 50));
		board.push_back(BoardLocation(4, "Income Tax"));
		board.push_back(BoardLocation(5, "Reading Railroad", 200, "Railroad"));
		board.push_back(BoardLocation(6, "Oriental Ave.", 100, "Light Blue", std::vector<int> {6, 30, 90, 270, 400, 550}, 50));
		board.push_back(BoardLocation(7, "Chance"));
		board.push_back(BoardLocation(9, "Vermont Ave.", 100, "Light Blue", std::vector<int> {6, 30, 90, 270, 400, 550}, 50));
		board.push_back(BoardLocation(10, "Connecticut Ave.", 120, "Light Blue", std::vector<int> {8, 40, 100, 300, 450, 600}, 50));
		board.push_back(BoardLocation(11, "Just Visiting / In Jail"));
		board.push_back(BoardLocation(12, "St. Charles Place", 140, "Pink", std::vector<int> {10, 50, 150, 450, 625, 750}, 100));
		board.push_back(BoardLocation(13, "Electric Company", 150, "Utility"));
		board.push_back(BoardLocation(14, "States Ave.", 140, "Pink", std::vector<int> {10, 50, 150, 450, 625, 750}, 100));
		board.push_back(BoardLocation(15, "Virginia Ave.", 160, "Pink", std::vector<int> {12, 60, 180, 500, 700, 900}, 100));
		board.push_back(BoardLocation(16, "Pennsylvania Railroad", 200, "Railroad"));
		board.push_back(BoardLocation(17, "St. James Place", 180, "Orange", std::vector<int> {14, 70, 200, 550, 750, 950}, 100));
		board.push_back(BoardLocation(18, "Community Chest"));
		board.push_back(BoardLocation(19, "Tennessee Ave.", 180, "Orange", std::vector<int> {14, 70, 200, 550, 750, 950}, 100));
		board.push_back(BoardLocation(20, "New York Ave.", 200, "Orange", std::vector<int> {16, 80, 220, 600, 800, 1000}, 100));
		board.push_back(BoardLocation(21, "Free Parking"));
		board.push_back(BoardLocation(22, "Kentucky Ave.", 220, "Red", std::vector<int> {18, 90, 250, 700, 875, 1050}, 150));
		board.push_back(BoardLocation(23, "Chance"));
		board.push_back(BoardLocation(24, "Indiana Ave.", 220, "Red", std::vector<int> {18, 90, 250, 700, 875, 1050}, 150));
		board.push_back(BoardLocation(25, "Illinois Ave.", 240, "Red", std::vector<int> {20, 100, 300, 750, 925, 1100}, 150));
		board.push_back(BoardLocation(26, "B. & O. Railroad", 200, "Railroad"));
		board.push_back(BoardLocation(27, "Atlantic Ave.", 260, "Yellow", std::vector<int> {22, 110, 330, 800, 975, 1150}, 150));
		board.push_back(BoardLocation(28, "Ventnor Ave.", 260, "Yellow", std::vector<int> {22, 110, 330, 800, 975, 1150}, 150));
		board.push_back(BoardLocation(29, "Water Works", 150, "Utility"));
		board.push_back(BoardLocation(30, "Marvin Gardens", 280, "Yellow", std::vector<int> {24, 120, 360, 850, 1025, 1200}, 150));
		board.push_back(BoardLocation(31, "Go to Jail"));
		board.push_back(BoardLocation(32, "Pacific Ave.", 300, "Green", std::vector<int> {26, 130, 390, 900, 1100, 1275}, 200));
		board.push_back(BoardLocation(33, "North Carolina Ave.", 300, "Green", std::vector<int> {26, 130, 390, 900, 1100, 1275}, 200));
		board.push_back(BoardLocation(34, "Community Chest"));
		board.push_back(BoardLocation(35, "Pennsylvania Ave.", 320, "Green", std::vector<int> {28, 150, 450, 1000, 1200, 1400}, 200));
		board.push_back(BoardLocation(36, "Short Line Railroad", 200, "Railroad"));
		board.push_back(BoardLocation(37, "Chance"));
		board.push_back(BoardLocation(38, "Park Place", 350, "Dark Blue", std::vector<int> {35, 175, 500, 1100, 1300, 1500}, 200));
		board.push_back(BoardLocation(39, "Luxury Tax"));
		board.push_back(BoardLocation(40, "Boardwalk", 400, "Dark Blue", std::vector<int> {50, 200, 600, 1400, 1700, 2000}, 200));

		unownedProperties.swap(board); // double check
	}

void Game::communityChest(Player* player)
{
	int card = communityChestCards[communityChestIndex];
}
