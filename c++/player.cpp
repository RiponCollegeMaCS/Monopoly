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
#include "boardlocation.h"
#include "game.h"

#include<iostream>
#include<vector>

Player::Player(int num, std::unordered_set<std::string*> groupPreferences, int buy_thresh=100, int build_thresh=5, int jt=3, bool sjs=false, int cm=0, int dt=0)
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

void Player::resetValues()
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
    inventory.insert(boardSpace);
}

bool Player::isInInventory(BoardLocation* boardSpace)
{
    if (inventory.find(boardSpace) != inventory.end()) // ...what if it's not the same pointer? TODO: check
    {
        return (true);
    }
    
    return (false);
}

void Player::appendToMonopolies(BoardLocation* boardSpace)
{
    monopolies.insert(boardSpace); // TODO: check
}

bool Player::isInMonopolies(BoardLocation* boardSpace)
{
    if (monopolies.find(boardSpace) != monopolies.end())
    {
        return (true);
    }
    
    return (false);
}

bool Player::isInGroupPreferences(std::string group)
{
    if (groupPreferences.find(&group) != groupPreferences.end())
    {
        return (true);
    }
    
    return (false);
}

// Strategy methods
void Player::payOutOfJail(Game* game)
{
	if (Player::hasChanceCard())
	{
		Player::flipChanceCard();
		game->addChanceCardToDeck();
	}
	else if (Player::hasCommunityChestCard())
	{
		Player::flipCommunityChestCard();
		game->addCommunityChestCardToDeck();
	}
	else
	{
		game->exchangeMoney(this, -50);
	}
}

bool Player::buyProperty(BoardLocation* property, int customPrice=0)
{
	if (customPrice)
	{
		return true;
	}
	return false;
}

void Player::developProperties(Game* game)
{
	// First, unmortgage if we can
	for (auto boardSpace : inventory)
	{
		if (boardSpace->isMortgaged && Player::isInMonopolies(boardSpace))
		{
			int unmortgagePrice = boardSpace->getUnmortgagePrice();

			if (money - unmortgagePrice >= buyingThreshold)
			{
				money -= unmortgagePrice;
				boardSpace->setMortgaged(false);
			}
			else
			{
				return;
			}
		}
	}

	// Buy buildings
	if (monopolies.size() != 0)
	{
		bool keepBuilding = true;
		while (keepBuilding)
		{
			keepBuilding = false;

			for (auto boardSpace : monopolies)
			{
				if (Player::isInMonopolies(boardSpace))
				{
					if (Player::evenBuildingTest(boardSpace))
					{
						if (boardSpace->exchangeMoney() < buildingThreshold)
						{
							int availableCash;

							if (boardSpace->isMortgaged())
							{
								throw 2;
							}

							if (1 == developmentThreshold)
							{
								availableCash = money - 1;
							}
							else if (2 == developmentThreshold)
							{
								int availableMortgageValue = 0;
								for (auto property : inventory)
								{
									if (!Player::isInMonopolies(property) && !property->isMortgaged())
									{
										availableMortgageValue += property->getPrice() / 2;
									}
								}
								availableCash = availableMortgageValue + money - 1;
							}
							else
							{
								availableCash = money - buyingThreshold;
							}

							// The player can afford it.
							if (availableCash - boardSpace->getHouseCost() >= 0)
							{
								int buildingSupply = 0;
								std::string building;
								if (boardSpace->exchangeMoney < 4)
								{
									buildingSupply = game->getAvailableHouses();
									building = "house";
								}
								else if (boardSpace->exchangeMoney == 4)
								{
									buildingSupply = game->getAvailableHotels();
									building = "hotel";
								}

								// Check if there is a building available
								if (buildingSupply > 0)
								{
									if ("house" == building)
									{
										game->changeHouses(-1);
									}
									else if ("hotel" == building)
									{
										game->changeHotels(-1);
										game->changeHouses(4);
									}

									boardSpace->changeBuildings(1);
									money -= boardSpace->getHouseCost();

									if (developmentThreshold != 2 && money < 0)
									{
										throw 2;
									}

									// Mortgage properties to pay for building
									if (2 == developmentThreshold)
									{
										for (auto cProperty : inventory)
										{
											if (money > 0)
											{
												break; // deviation alert!
											}
											else
											{
												if (!Player::isInMonopolies(cProperty) && !cProperty->isMortgaged())
												{
													cProperty->flipMortgaged();
													money += cProperty->getPrice() / 2;
												}
											}
										}
									}

									keepBuilding = true; // Allow the player to build again
									game->firstBuilding(); // Buildings have been built.
								}
							}
						}
					}
				}
			}
		}
	}

	for (auto boardSpace : inventory)
	{
		if (boardSpace->isMortgaged())
		{
			int unmortgagePrice = game->unmortgagePrice(boardSpace);

			if (money - unmortgagePrice >= buyingThreshold)
			{
				money -= unmortgagePrice;
				boardSpace->flipMortgaged();
			}
			else
			{
				return;
			}
		}
	}
}

void Player::sellBuilding(BoardLocation* property, std::string building, Game* game)
{
	// Sell one house on the property
	if ("house" == building)
	{
		property->changeBuildings(-1);
		game->changeHouses(1);
		Player::money += property->getHouseCost() / 2;
	}

	// Downgrade from hotel to 4 houses
	else if ("hotel" == building)
	{
		property->changeBuildings(-1);
		game->changeHotels(1);
		game->changeHouses(4);
		Player::money += property->getHouseCost() / 2;
	}

	else if ("all" == building)
	{
		if (5 == property->exchangeMoney())
		{
			property->changeBuildings(-5);
			game->changeHotels(1);
			Player::money += (property->getHouseCost() / 2) * 5;
		}

		else
		{
			game->changeHouses(property->exchangeMoney());
			Player::money += (property->getHouseCost() / 2) * property->exchangeMoney();
			property->changeBuildings(-property->exchangeMoney());
		}
	}
}

void Player::makeFunds(Game* game)
{
	// Mortgage properties if they are not in a monopoly

	for (auto boardSpace : Player::inventory)
	{
		if (!Player::isInMonopolies(boardSpace) && !boardSpace->isMortgaged())
		{
			int mortgageValue = boardSpace->getPrice / 2;
			Player::money += mortgageValue;
			boardSpace->flipMortgaged();
			if (Player::money > 0)
			{
				return;
			}
		}
	}

	// Sell houses and hotels

	if (Player::monopolies.size() != 0)
	{
		bool keepSelling = true;

		while (keepSelling)
		{
			keepSelling = false;

			for (auto boardSpace : Player::inventory)
			{
				// It has buildings and we are selling evenly
				if (boardSpace->exchangeMoney() > 0 && Player::evenSellingTest(boardSpace))
				{
					keepSelling = true;
					if (5 == boardSpace->exchangeMoney())
					{
						if (game->getAvailableHouses() >= 4)
						{
							Player::sellBuilding(boardSpace, "hotel", game);
						}
						else
						{
							for (auto relativeSpace : Player::inventory)
							{
								if (relativeSpace->getGroup() == boardSpace->getGroup())
								{
									Player::sellBuilding(relativeSpace, "all", game);
								}
							}
						}
					}
					else // It's a house!
					{
						Player::sellBuilding(boardSpace, "house", game);
					}

					if (Player::money > 0)
					{
						return;
					}
				}
			}
		}
	}

	 // Mortgage properties in monopolies

	for (auto boardSpace : Player::inventory)
	{
		if (!boardSpace->isMortgaged())
		{
			if (isInMonopolies(boardSpace))
			{
				throw 2;
			}
			Player::money += boardSpace->getPrice() / 2;
			boardSpace->flipMortgaged();
			if (Player::money > 0)
				return;
		}
	}
}

void Player::setJailStrategy(Game* game)
{
	if (Player::smartJailStrategy && game->hasFirstBuilding())
	{
		Player::jailTime = 3;
	}
	else
	{
		Player::jailTime = Player::initJailTime;
	}
}

bool Player::evenSellingTest(BoardLocation* property)
{
	for (auto boardSpace : Player::inventory)
	{
		if (boardSpace->getGroup() == property->getGroup() && boardSpace->exchangeMoney() - property->exchangeMoney() > 0)
		{
			return (false);
		}
	}

	return (true);
}

bool Player::evenBuildingTest(BoardLocation* property)
{
	for (auto boardSpace : Player::inventory)
	{
		if (boardSpace->getGroup() == property->getGroup() && property->exchangeMoney() - boardSpace->exchangeMoney() > 0)
		{
			return (false);
		}
	}

	return (true);
}

int Player::findAvailableMortgageValue()
{
	int available = 0;

	for (auto property : Player::inventory)
	{
		if (0 == property->exchangeMoney() && !property->isMortgaged() && !Player::isInMonopolies(property))
		{
			available += property->getPrice() / 2;
		}
	}

	return (available);
}

void Player::makeBid(BoardLocation* property, Game* game)
{
	Player::bidIncludesMortgages = false;

	if (isInGroupPreferences(*property->getGroup()))
	{
		Player::auctionBid = Player::money - 1;
	}

	else if (1 == Player::completeMonopoly && game->monopolyStatus(this, property))
	{
		Player::auctionBid = Player::money - 1;
	}

	else if (2 == Player::completeMonopoly && game->monopolyStatus(this, property))
	{
		Player::bidIncludesMortgages = true;

		int available = Player::findAvailableMortgageValue();

		Player::auctionBid = Player::money + available - 1;
	}

	else
	{
		Player::auctionBid = Player::money - Player::buyingThreshold;
	}
}

void Player::makeAuctionFunds(BoardLocation* property, Game* game, int winningBid)
{
	// Special buying procedure if the player wants to mortgage properties.
	if (Player::bidIncludesMortgages)
	{
		Player::money -= winningBid;

		// Make up the funds
		for (auto property : Player::inventory)
		{
			if (money > 0)
			{
				break; // deviation alert
			}

			if (0 == property->exchangeMoney() && !property->isMortgaged() && !isInMonopolies(property))
			{
				property->flipMortgaged();
				Player::money = property->getPrice / 2;
			}
		}

		Player::money += winningBid;
	}
}

bool Player::unownedPropertyAction(Game* game, BoardLocation* property)
{
	// The player has enough money to buy the property
	if (Player::money - property->getPrice() >= Player::buyingThreshold)
	{
		game->buyProperty(this, property);
		return true;
	}

	// The player has a preference for the group and will pay any money they have
	if (Player::isInGroupPreferences(*property->getGroup()) && Player::money - property->getPrice > 0)
	{
		game->buyProperty(this, property);
		return true;
	}

	// The player will gain a monopoly, they want to complete the group, they have the money
	if (1 == Player::completeMonopoly && Player::money - property->getPrice() > 0 && game->monopolyStatus(this, property))
	{
		game->buyProperty(this, property);
		return true;
	}

	// The player will mortgage other properties to buy it if it completes a group
	if (2 == Player::completeMonopoly && game->monopolyStatus, this, property)
	{
		if ((Player::money + Player::findAvailableMortgageValue()) - property->getPrice() > 0)
		{
			Player::money -= property->getPrice();

			for (auto cProperty : Player::inventory) // deviation alert
			{
				if (Player::money > 0)
				{
					break;
				}
				if (0 == cProperty->exchangeMoney && !cProperty->isMortgaged() && !Player::isInMonopolies(cProperty))
				{
					cProperty->flipMortgaged();
					Player::money += cProperty->getPrice() / 2;
				}
			}

			game->removeFromUnownedProperties(property);
			Player::inventory.insert(property);
			Player::monopolies.insert(property);
			return true;
		}
	}

	return false;
}

bool Player::jailDecision(Game* game)
{
	if (Player::jailCounter - 1 == Player::jailTime)
	{
		return (true);
	}

	return (false);
}

// Getters and setters
int Player::getNumber() { return (number); }
void Player::setNumber(int num) { number = num; }
int Player::getBuyingThreshold() { return (buyingThreshold); }
int Player::getBuildingThreshold() { return (buildingThreshold); }
bool Player::hasPassedGo() { return (passedGo); }
int Player::getJailTime() { return (jailTime); }
void Player::setJailTime(int jailtime) { jailTime = jailtime; }
int Player::getInitJailTime() { return (initJailTime); }
bool Player::hasSmartJailStrategy() { return (smartJailStrategy); }
int Player::getCompleteMonopoly() { return (completeMonopoly); }
std::unordered_set<std::string*>* Player::getGroupPreferences() { return (&groupPreferences); }
int Player::getDevelopmentThreshold() { return (developmentThreshold); }
void Player::flipCommunityChestCard() { communityChestCard = !communityChestCard; }
bool Player::hasCommunityChestCard() { return (communityChestCard); }
void Player::flipChanceCard() { chanceCard = !chanceCard; }
bool Player::hasChanceCard() { return (chanceCard); }
std::unordered_set<std::string*>* Player::getMonopolies() { return (&monopolies); }
std::unordered_set<BoardLocation*>* Player::getInventory() { return (&inventory); }
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

char Player::getType() { return 'p'; }

