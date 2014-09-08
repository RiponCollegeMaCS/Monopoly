/*
 * =====================================================================================
 *
 *       Filename:  game.h
 *
 *    Description:  Header file for a game class
 *
 *        Version:  1.0
 *        Created:  Sep 4, 2014 3:01:49 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */
#pragma once
#ifndef GAME_H_
#define GAME_H_

#include "boardlocation.h"
#include "player.h"

#include<string>
#include<vector>

class Game
{
	const int BOARD_SIZE = 40;
	const int NUMBER_OF_CARDS = 16;
	const int HOUSES = 32;
	const int HOTELS = 12;

	bool gameStatus = true;
	int numberOfPlayers;
	std::vector<BoardLocation> board;
	std::vector<Player> players;
	int turnCounter = 0;
	int doublesCounter = 0;
	int result = 99;
	int diceRoll = 0;
	bool auctionsEnabled = false;
	bool firstBuilding = false;
	int cutoff = 300;

	// House rules flags
	bool freeParkingPool = false;
	int moneyInFP = false;
	bool doubleOnGo = false;
	bool noRentInJail = false;
	bool tripToStart = false;
	bool snakeEyesBonus = false;

	// Card decks
	int chanceCards[16];
	int communityChestCards[16];
	int chanceIndex = 0;
	int communityChestIndex = 0;

	std::vector<BoardLocation> unownedProperties;

	// Miscellaneous
	int moneyInFP = 0;

	void createCards();
	void createBoard();

public:
	Game(std::vector<Player> players, bool auct, bool fpp, bool dog, bool nrij, bool tts, bool seb, int cutoff);

	void communityChest(Player* player);
	void chance(Player* player);
	void changeMoney(Player* player, int amount);
	void moveTo(Player* player, int location);
	void goToJail(Player* player);
	void boardAction(Player* player, BoardLocation* boardLocation);

};



#endif /* GAME_H_ */
