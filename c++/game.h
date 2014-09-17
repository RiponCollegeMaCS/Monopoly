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

struct endReport
{
    int result;
    int turnCounter;
    std::unordered_set<std::string*> player0Monopolies;
    std::unordered_set<std::string*> player1Monopolies;
    int player0Money;
    int player1Money;
};

class Game
{
	const int BOARD_SIZE = 40;
	const int NUMBER_OF_CARDS = 16;

	bool gameStatus = true;
	int numberOfPlayers;
    BoardLocation* board[40];
	std::vector<Player*> players;
	int turnCounter = 0;
	int doublesCounter = 0;
	int result = 99;
	int diceRoll = 0;
	bool auctionsEnabled = false;
	bool firstBuilding = false;
	int cutoff = 300;

	bool moveAgain = false;

	// House rules flags
	bool freeParkingPool = false;
	bool doubleOnGo = false;
	bool noRentInJail = false;
	bool tripToStart = false;
	bool snakeEyesBonus = false;

	// Card decks
	int chanceCards[16];
	int communityChestCards[16];
	int chanceIndex = 0;
	int communityChestIndex = 0;
	int chanceJailIndex = -1;
	int communityChestJailIndex = -1;

	std::unordered_set<BoardLocation*> unownedProperties;

	// Miscellaneous
	int moneyInFP = 0;
    int houses = 32;
    int hotels = 12;

	void createCards();
	void createBoard();

public:
	Game(std::vector<Player*> players, int cutoff);
	Game(std::vector<Player*> players, bool auct, bool fpp, bool dog, bool nrij, bool tts, bool seb, int cutoff);
    ~Game();

	void communityChest(Player* player);
	void chance(Player* player);
	void moveAhead(Player* player, int numberOfSpaces);
	void moveTo(Player* player, int location);
	void payOutOfJail(Player* player);
	void goToJail(Player* player);
    void buyProperty(Player* player, BoardLocation* boardSpace, int customPrice);
    Player* propertyOwner(BoardLocation* property);
    void payRent(Player* player);
    int unmortgagePrice(BoardLocation* property);
    void sellBuilding(Player* player, BoardLocation* property, std::string building);
    void changeMoney(Player* player, int amount);
    bool evenSellingTest(BoardLocation* property, Player* player);
    bool evenBuildingTest(BoardLocation* property, Player* player);
    bool mortgageCheck(BoardLocation* property, Player* player);
    void developProperties(Player* player);
    bool monopolyStatus(Player* player, BoardLocation* boardSpace);
    int findAvailableMortgageValue(Player* player);
    void auction(BoardLocation* boardSpace);
    int totalAssets(Player* player);
    void propertyAction(Player* player, BoardLocation* boardSpace);
	void boardAction(Player* player, BoardLocation* boardLocation);
    void takeTurn(Player* player);
    void updateStatus();
    endReport play();
    int rollDie();
    int chooseRandomPlayer();
};



#endif /* GAME_H_ */
