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

#include<iostream>
#include<string>
#include<vector>
#include<algorithm>

#include "player.h"
#include "boardlocation.h"
#include "game.h"

class Game
{
	const int BOARD_SIZE = 40;
	const int NUMBER_OF_CARDS = 16;

	bool gameStatus = true;
	int numberOfPlayers;
	BoardLocation board[];
	Player players[];
	int turnCounter = 0;
	int doublesCounter = 0;
	int houses = 32;
	int hotels = 12;
	int result = 99; // What does this do?
	int diceRoll = 0;
	bool auctionsEnabled = false;
	bool firstBuilding = false;
	int cutoff = 300;

	// House rules flags
	bool freeParkingPool = false;
	int moneyInFP = 0;
	bool doubleOnGo = false;
	bool noRentInJail = false;
	bool tripToStart = false;
	bool snakeEyesBonus = false;

	// Card decks
	int[] chanceCards = int[16];
	int[] communityChestCards = int[16];
	int chanceIndex = 0;
	int communityChestIndex = 0;

	void createCards()
	{
		for (int i = 0; i < NUMBER_OF_CARDS; i++)
		{
			chanceCards[i] = i + 1;
			communityChestCards[i] = i + 1;
		}

		std::random_shuffle(&chanceCards[0], &chanceCards[15]);
		std::random_shuffle(&communityChestCards[0], &communityChestCards[15]);
	}

	void create_board()
	{
		board = malloc(sizeof(BoardLocation)*41); // no idea

		board[0] = new BoardLocation(0, "Go");
		board[1] = new BoardLocation(1, "Mediterranean Ave.", 60, "Brown", (2, 10, 30, 90, 160, 250), 50);
	}

	public:
		Game(Player* listOfPlayers, bool auct, bool fpp, bool dog, bool nrij, bool tts, bool seb, int co)
		{
			players = listOfPlayers; // correct pointer syntax?
			auctionsEnabled = auctionsEnabled && auct;
			freeParkingPool = freeParkingPool && fpp;
			doubleOnGo = doubleOnGo && dog;
			noRentInJail = noRentInJail && nrij;
			tripToStart = tripToStart && tts;
			snakeEyesBonus = snakeEyesBonus && seb;
			if (co != NULL)
				cutoff = co; // maybe?
		}
};
