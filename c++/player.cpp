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

void Player::changePosition(int delta)
{
    position += delta;
}

void Player::passGo()
{
    passedGo = true;
}

void Player::appendToInventory(BoardLocation* boardSpace)
{
    inventory.push_back(boardSpace);
}

void Player::appendToMonopolies(std::string group)
{
    monopolies.push_back(&group); // TODO: check
}

// Getters and setters
int Player::getNumber() { return (number); }
int Player::getBuyingThreshold() { return (buyingThreshold); }
int Player::getBuildingThreshold() { return (buildingThreshold); }
bool Player::hasPassedGo() { return (passedGo); }
int Player::getJailTime() { return (jailTime); }
void Player::setJailTime(int jailtime) { jailTime = jailtime; }
int Player::getInitJailTime() { return (initJailTime); }
bool Player::hasSmartJailStrategy() { return (smartJailStrategy); }
int Player::getCompleteMonopoly() { return (completeMonopoly); }
std::vector<int> Player::getGroupPreferences() { return (groupPreferences); }
int Player::getDevelopmentThreshold() { return (developmentThreshold); }
void Player::flipCommunityChestCard() { communityChestCard = !communityChestCard; }
bool Player::hasCommunityChestCard() { return (communityChestCard); }
void Player::flipChanceCard() { chanceCard = !chanceCard; }
bool Player::hasChanceCard() { return (chanceCard); }
std::vector<std::string*> Player::getMonopolies() { return (monopolies); }
std::vector<BoardLocation*> Player::getInventory() { return (inventory); }
int Player::getPosition() { return (position); }
void Player::setPosition(int pos) { position = pos; }
bool Player::isInJail() { return (inJail); }
void Player::setInJail(bool jail) { inJail = jail; }
int Player::getMoney() { return (money); }
void Player::setMoney(int newMoney) { money = newMoney; }
void Player::addMoney(int add) { money += add; }
bool Player::getBidIncludesMortgages() { return (bidIncludesMortgages); }
void Player::setBidIncludesMortgages(bool bid) { bidIncludesMortgages = bid; }
int Player::getAuctionBid() { return (auctionBid); }
void Player::setAuctionBid(int bid) { auctionBid = bid; }
bool Player::getCardRent() { return (cardRent); }
void Player::setCardRent(bool rent) { cardRent = rent; }
int Player::getJailCounter() { return (jailCounter); }
void Player::setJailCounter(int count) { jailCounter = count; }
void Player::incrementJailCounter() { jailCounter++; }

