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

#include "player.h"

#include<iostream>
#include<vector>

Player::Player(int num, std::vector<int> groupPreferences, int buy_thresh=100, int build_thresh=5, int jt=3, bool sjs=false, int cm=0, int dt=0)
{
	number = num;
	buyingThreshold = buy_thresh;
	buildingThreshold = build_thresh;
	jailTime = jt;
	smartJailStrategy = sjs;
	completeMonopoly = cm;
	developmentThreshold = dt;
	Player::groupPreferences = groupPreferences;
}

void Player::reset_values()
{
	successIndicator = 0;
	position = 0;
	money = 1500;
	chanceCard = false;
	communityChestCard = false;
	inJail = false;
	jailCounter = 0;
	cardRent = false;
	monopolies.clear();
	auctionBid = 0;
	passedGo = false;
	inventory.clear();
	bidIncludesMortgages = false;
}

// Getters and setters
int Player::getBuyingThreshold() { return (buyingThreshold); }
int Player::getBuildingThreshold() { return (buildingThreshold); }
int Player::getJailTime() { return (jailTime); }
bool Player::hasSmartJailStrategy() { return (smartJailStrategy); }
int Player::getCompleteMonopoly() { return (completeMonopoly); }
std::vector<int> Player::getGroupPreferences() { return (groupPreferences); }
int Player::getDevelopmentThreshold() { return (developmentThreshold); }
void Player::giveCommunityChestCard() { communityChestCard = true; }
