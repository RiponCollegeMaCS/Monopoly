/*
 * =====================================================================================
 *
 *       Filename:  player.cpp
 *
 *    Description:  Represent a player in a game of Monopoly
 *
 *        Version:  1.0
 *        Created:  9/2/2014 12:29:43 AM
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

class Player
{
    int number;

    // Strategy params
    int buyingThreshold = 100;
    int buildingThreshold = 5;
    int jailTime = 3;
    bool smartJailStrategy = false;
    int completeMonopoly = 0;
    int[] groupPreferences = new int[2];
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
    std::vector<std::string> monopolies; // implementation of these has to be checked for efficiency
    int auctionBid = 0;
    bool passedGo = false;
    std::vector<std::string> inventory;
    bool bidIncludesMortgages = false;

    public:
        Player(int num, int gp[], int buy_thresh=100, int build_thresh=5, int jt=3, bool sjs=false, int cm=0, int dt=0)
	{
		number = num;
		buyingThreshold = buy_thresh;
		buildingThreshold = build_thresh;
		jailTime = jt;
		smartJailStrategy = sjs;
		completeMonopoly = cm;
		developmentThreshold = dt;
	}
        void reset_values()
	{
		successIndicator = 0;
		position = 0;
		money = 1500;
		chanceCard = false;
		communityChestCard = false;
		inJail = false;
		jailCounter = 0;
		cardRent = false;
		monopolies = std::vector<std::string>; // check syntax
		auctionBid = 0;
		passedGo = false;
		inventory = std::vector<std::string>;
		bidIncludesMortgages = false;
	}

	// Getters and setters
	int getBuyingThreshold() { return buyingThreshold; }
	int getBuildingThreshold() { return buildingThreshold; }
	int getJailTime() { return jailTime; }
	bool isSmartJailStrategy() { return smartJailStrategy; }
	int getCompleteMonopoly() { return completeMonopoly; }
	int* getGroupPreferences() { return &groupPreferences; }
	int getDevelopmentThreshold() { return developmentThreshold; }

};
