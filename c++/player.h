/*
 * =====================================================================================
 *
 *       Filename:  player.h
 *
 *    Description:  Header file for a player class
 *
 *        Version:  1.0
 *        Created:  Sep 4, 2014 2:52:42 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */
#ifndef PLAYER_H_
#define PLAYER_H_

#include "boardlocation.h"
#include <vector>
#include <unordered_set>
#include <string>

class Player
{
	int number;

	// Strategy params
	int buyingThreshold = 100;
	int buildingThreshold = 5;
	int jailTime = 3;
	int initJailTime = 3; // ??????
	bool smartJailStrategy = false;
	int completeMonopoly = 0;
    std::unordered_set<std::string*> groupPreferences;
	int developmentThreshold = 0;

	// Parameters
	int successIndicator = 0;
	int position = 0;
	int money = 1500;
	bool chanceCard = false;
	bool communityChestCard = false;
	bool inJail = false;
	int jailCounter = 0;
	bool cardRent = false;
	std::unordered_set<std::string*> monopolies;
	int auctionBid = 0;
	bool passedGo = false;
	std::unordered_set<BoardLocation*> inventory;
	bool bidIncludesMortgages = false;

public:
    Player(int num, std::unordered_set<std::string*> groupPreferences, int buy_thresh, int build_thresh, int jt, bool sjs, int cm, int dt);

    void resetValues();
    void changePosition(int delta);
    void passGo();
    void appendToInventory(BoardLocation* boardSpace);
    bool isInInventory(BoardLocation* boardSpace);
    void appendToMonopolies(std::string group);
    bool isInMonopolies(std::string group); // pointer?
    bool isInGroupPreferences(std::string group);

    // Strategy methods
    void payOutOfJail(Game* game);
    bool buyProperty(BoardLocation* property, int customPrice);
    void developProperties(); // I wish I didn't have to access so much info internal to Game
    int findAvailableMortgageValue();
    int getTotalAssets();


    // Getters and setters
    int getNumber();
    void setNumber(int num);
    int getBuyingThreshold();
    int getBuildingThreshold();
    bool hasPassedGo();
    int getJailTime();
    void setJailTime(int jailtime);
    int getInitJailTime();
    bool hasSmartJailStrategy();
    int getCompleteMonopoly();
    std::unordered_set<std::string*>* getGroupPreferences();
    int getDevelopmentThreshold();
    void flipCommunityChestCard();
    bool hasCommunityChestCard();
    void flipChanceCard();
    bool hasChanceCard();
    std::unordered_set<std::string*>* getMonopolies();
    std::unordered_set<BoardLocation*>* getInventory();
    int getPosition();
    void setPosition(int pos);
    bool isInJail();
    void setInJail(bool jail);
    int getMoney();
    void setMoney(int newMoney);
    void addMoney(int add);
    bool getBidIncludesMortgages();
    void setBidIncludesMortgages(bool bid);
    int getAuctionBid();
    void setAuctionBid(int bid);
    bool getCardRent();
    void setCardRent(bool rent);
    int getJailCounter();
    void setJailCounter(int count);
    void incrementJailCounter();
};



#endif /* PLAYER_H_ */
