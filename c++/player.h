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
#pragma once
#ifndef PLAYER_H_
#define PLAYER_H_

#include "boardlocation.h"
#include<vector>
#include<string>

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
	std::vector<int> groupPreferences;
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
	std::vector<std::string*> monopolies; // implementation of these has to be checked for efficiency
	int auctionBid = 0;
	bool passed_go = false;
	std::vector<BoardLocation*> inventory;
	bool bidIncludesMortgages = false;

public:
    Player(int num, std::vector<int> groupPreferencers, int buy_thresh, int build_thresh, int jt, bool sjs, int cm, int dt);

    void reset_values();
    void changePosition(int delta);
    void passedGo();
    void appendToInventory(BoardLocation* boardSpace);
    void appendToMonopolies(std::string group);

    // Getters and setters
    int getNumber();
    int getBuyingThreshold();
    int getBuildingThreshold();
    bool hasPassedGo();
    int getJailTime();
    void setJailTime(int jailTime);
    int getInitJailTime();
    bool hasSmartJailStrategy();
    int getCompleteMonopoly();
    std::vector<int> getGroupPreferences();
    int getDevelopmentThreshold();
    void flipCommunityChestCard();
    bool hasCommunityChestCard();
    void flipChanceCard();
    bool hasChanceCard();
    std::vector<std::string*> getMonopolies();
    std::vector<BoardLocation*> getInventory();
    int getPosition();
    void setPosition(int position);
    bool isInJail();
    void setInJail(bool jail);
    int getMoney();
    void setMoney(int newMoney);
    void addMoney(int add);
    bool getBidIncludesMortgages();
    void setBidIncludesMortgages(bool bid);
    int getAuctionBid();
    void setAuctionBid(int bid);
    void setCardRent(bool rent);
    int getJailCounter();
    void setJailCounter(int count);
    void incrementJailCounter();
};



#endif /* PLAYER_H_ */
