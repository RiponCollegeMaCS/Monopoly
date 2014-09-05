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

#include<vector>
#include<string>

class Player
{
	int number;

	// Strategy params
	    int buyingThreshold = 100;
	    int buildingThreshold = 5;
	    int jailTime = 3;
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
	    std::vector<std::string> monopolies; // implementation of these has to be checked for efficiency
	    int auctionBid = 0;
	    bool passedGo = false;
	    std::vector<std::string> inventory;
	    bool bidIncludesMortgages = false;

public:
    Player(int num, std::vector<int> groupPreferencers, int buy_thresh, int build_thresh, int jt, bool sjs, int cm, int dt);

    void reset_values();

    // Getters and setters
    int getBuyingThreshold();
    int getBuildingThreshold();
    int getJailTime();
    bool isSmartJailStrategy();
    int getCompleteMonopoly();
    std::vector<int> getGroupPreferences();
    int getDevelopmentThreshold();
    void giveCommunityChestCard();
};



#endif /* PLAYER_H_ */
