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

#include "game/player.h"
#include "game/boardlocation.h"
#include "game/game.h"

#include <iostream>
#include <vector>
#include <unordered_set>

Player::Player(int num, std::unordered_set<std::string*> groupPreferences, int buy_thresh=100, int build_thresh=5, int jt=3, bool sjs=false, int cm=0, int dt=0, int mab=0)
{
	number = num;
	buyingThreshold = buy_thresh;
	buildingThreshold = build_thresh;
	jailTime = jt;
	smartJailStrategy = sjs;
	completeMonopoly = cm;
	developmentThreshold = dt;
    maxAuctionBid = mab;
	Player::groupPreferences = groupPreferences;
}

Player::Player(const int* parameters)
{
	Player::number = parameters[0];
	Player::buyingThreshold = parameters[1];
	Player::buildingThreshold = parameters[2];
	Player::jailTime = parameters[3];
	Player::smartJailStrategy = parameters[4];
	Player::completeMonopoly = parameters[5];
	Player::developmentThreshold = parameters[6];
    Player::maxAuctionBid = parameters[7];
	Player::groupPreferences = std::unordered_set<std::string*>();
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

void Player::appendToMonopolies(std::string* group)
{
    monopolies.insert(group); // TODO: check
}

bool Player::isInMonopolies(std::string* group)
{
    if (monopolies.find(group) != monopolies.end())
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
		Player::takeChanceCard();
		game->addChanceCardToDeck();
	}
	else if (Player::hasCommunityChestCard())
	{
		Player::takeCommunityChestCard();
		game->addCommunityChestCardToDeck();
	}
	else
	{
		game->exchangeMoney(this, 50);
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
		if (boardSpace->isMortgaged() && Player::isInMonopolies(boardSpace->getGroup()))
		{
			int unmortgagePrice = boardSpace->getUnmortgagePrice();

			if (Player::money - unmortgagePrice >= Player::buyingThreshold)
			{
				Player::money -= unmortgagePrice;
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

            for (auto boardSpace : Player::inventory)
			{
				if (Player::isInMonopolies(boardSpace->getGroup()))
				{
					if (Player::evenBuildingTest(boardSpace))
					{
						if (boardSpace->getBuildings() < buildingThreshold)
						{
							int availableCash;

							if (boardSpace->isMortgaged())
							{
								std::cerr << "error 10"  << boardSpace->getName() << __LINE__ << std::endl;
							}

                            // Calculate current cash available
							if (1 == Player::developmentThreshold)
							{
								availableCash = Player::money - 1;
							}
							else if (2 == Player::developmentThreshold)
							{
							    // Find available mortgage value
								int availableMortgageValue = 0;
								for (auto property : Player::inventory)
								{
									if (!Player::isInMonopolies(property->getGroup()) && !property->isMortgaged())
									{
										availableMortgageValue += property->getPrice() / 2;
									}
								}
								availableCash = availableMortgageValue + Player::money - 1;
							}
							else
							{
								availableCash = Player::money - Player::buyingThreshold;
							}

							// The player can afford it.
							if (availableCash - boardSpace->getHouseCost() >= 0)
							{
								int buildingSupply = 0;
								std::string building;
								if (boardSpace->getBuildings() < 4) // Ready for a house
								{
									buildingSupply = game->getAvailableHouses();
									building = "house";
								}
								else if (boardSpace->getBuildings() == 4) // Ready for a hotel
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
									Player::money -= boardSpace->getHouseCost();

									if (Player::developmentThreshold != 2 && Player::money < 0)
									{
										std::cerr << "error 9" << Player::money << __LINE__ <<  std::endl;
									}

									// Mortgage properties to pay for building
									if (2 == Player::developmentThreshold)
									{
										for (auto cProperty : Player::inventory)
										{
											if (money > 0)
											{
												break; // deviation alert!
											}
											else
											{
												if (!Player::isInMonopolies(cProperty->getGroup()) && !cProperty->isMortgaged())
												{
													cProperty->mortgage();
													money += cProperty->getPrice() / 2;
												}
											}
										}
									}

									keepBuilding = true; // Allow the player to build again
									game->hasFirstBuilding(); // Buildings have been built.
								}
							}
						}
					}
				}
			}
		}
	}

	for (auto boardSpace : Player::inventory)
	{
		if (boardSpace->isMortgaged())
		{
			int unmortgagePrice = game->unmortgagePrice(boardSpace);

			if (Player::money - unmortgagePrice >= Player::buyingThreshold)
			{
				Player::money -= unmortgagePrice;
				boardSpace->unmortgage();
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
		game->changeHouses(-4);
		Player::money += property->getHouseCost() / 2;
	}

	else if ("all" == building)
	{
		if (5 == property->getBuildings())
		{
			property->changeBuildings(-5);
			game->changeHotels(1);
			Player::money += (property->getHouseCost() / 2) * 5;
		}

		else
		{
			game->changeHouses(property->getBuildings());
			Player::money += (property->getHouseCost() / 2) * property->getBuildings();
			property->changeBuildings(-property->getBuildings());
		}
	}
}

void Player::makeFunds(Game* game)
{
	// Mortgage properties if they are not in a monopoly

	for (auto boardSpace : Player::inventory)
	{
		if (!Player::isInMonopolies(boardSpace->getGroup()) && !boardSpace->isMortgaged())
		{
			int mortgageValue = boardSpace->getPrice() / 2;
			Player::money += mortgageValue;
			boardSpace->mortgage();
			if (Player::money > 0)
			{
				return;
			}
		}
	}

	// Sell houses and hotels

	if (Player::monopolies.size() > 0)
	{
		bool keepSelling = true;

		while (keepSelling)
		{
			keepSelling = false;

			for (auto boardSpace : Player::inventory)
			{
				// It has buildings and we are selling evenly
				if (boardSpace->getBuildings() > 0 && Player::evenSellingTest(boardSpace))
				{
					keepSelling = true;
					if (5 == boardSpace->getBuildings())
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
			if (!isInMonopolies(boardSpace->getGroup()))
			{
				std::cerr << "eee error" << __LINE__ << std::endl;
			}
			Player::money += boardSpace->getPrice() / 2;
			boardSpace->mortgage();
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
		if (boardSpace->getGroup() == property->getGroup() && boardSpace->getBuildings() - property->getBuildings() > 0)
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
		if (boardSpace->getGroup() == property->getGroup() && property->getBuildings() - boardSpace->getBuildings() > 0)
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
		if (0 == property->getBuildings() && !property->isMortgaged() && !Player::isInMonopolies(property->getGroup()))
		{
			available += property->getPrice() / 2;
		}
	}

	return (available);
}

//void Player::makeBid(BoardLocation* property, Game* game)
//{
//	Player::bidIncludesMortgages = false;
//
//    std::vector<BoardLocation*> additional = {property};
//
//	if (isInGroupPreferences(*property->getGroup()))
//	{
//		Player::auctionBid = Player::money - 1;
//	}
//
//	else if (1 == Player::completeMonopoly && game->monopolyStatus(this, property, &additional))
//	{
//		Player::auctionBid = Player::money - 1;
//	}
//
//	else if (2 == Player::completeMonopoly && game->monopolyStatus(this, property, &additional))
//	{
//		Player::bidIncludesMortgages = true;
//
//		int available = Player::findAvailableMortgageValue();
//
//		Player::auctionBid = Player::money + available - 1;
//	}
//
//	else
//	{
//		Player::auctionBid = Player::money - Player::buyingThreshold;
//	}
//}
//
//void Player::makeAuctionFunds(BoardLocation* property, Game* game, int winningBid)
//{
//	// Special buying procedure if the player wants to mortgage properties.
//	if (Player::bidIncludesMortgages)
//	{
//		Player::money -= winningBid;
//
//		// Make up the funds
//		for (auto property : Player::inventory)
//		{
//			if (money > 0)
//			{
//				break; // deviation alert
//			}
//
//			if (0 == property->getBuildings() && !property->isMortgaged() && !isInMonopolies(property->getGroup()))
//			{
//				property->mortgage();
//				Player::money = property->getPrice() / 2;
//			}
//		}
//
//		Player::money += winningBid;
//	}
//}

int Player::getMaxAuctionBid()
{
    return Player::maxAuctionBid > Player::money ? Player::money - 1 : Player::maxAuctionBid;
}

bool Player::unownedPropertyAction(Game* game, BoardLocation* property)
{
    std::vector<BoardLocation*> additional = {property};
	// The player has enough money to buy the property
	if (Player::money - property->getPrice() >= Player::buyingThreshold)
	{
		game->buyProperty(this, property);
		return true;
	}

	// The player has a preference for the group and will pay any money they have
	if (Player::isInGroupPreferences(*property->getGroup()) && Player::money - property->getPrice() > 0)
	{
		game->buyProperty(this, property);
		return true;
	}

	// The player will gain a monopoly, they want to complete the group, they have the money
	if (1 == Player::completeMonopoly && Player::money - property->getPrice() > 0 && game->monopolyStatus(this, property, &additional))
	{
		game->buyProperty(this, property);
		return true;
	}

	// The player will mortgage other properties to buy it if it completes a group
	if (2 == Player::completeMonopoly && game->monopolyStatus(this, property, &additional))
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
				if (0 == cProperty->getBuildings() && !cProperty->isMortgaged() && !Player::isInMonopolies(cProperty->getGroup()))
				{
					cProperty->mortgage();
					Player::money += cProperty->getPrice() / 2;
				}
			}

			game->removeFromUnownedProperties(property);
			Player::inventory.insert(property);
			Player::monopolies.insert(property->getGroup());
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

bool Player::completesMonopoly(BoardLocation *property)
{
    int count = 0;
    for (auto aProperty : Player::inventory)
    {
        if (aProperty->getGroup() == property->getGroup())
        {
            count++;
        }
    }
    if (BoardLocation::getGroupSize(property->getGroup()) == count)
    {
        return true;
    }

    return false;
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
void Player::giveCommunityChestCard() { communityChestCard = true; }
void Player::takeCommunityChestCard() { communityChestCard = false; }
bool Player::hasCommunityChestCard() { return (communityChestCard); }
void Player::giveChanceCard() { chanceCard = true; }
void Player::takeChanceCard() { chanceCard = false; }
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
bool Player::getCardRent() { return (cardRent); }
void Player::setCardRent(bool rent) { cardRent = rent; }
int Player::getJailCounter() { return (jailCounter); }
void Player::setJailCounter(int count) { jailCounter = count; }
void Player::incrementJailCounter() { jailCounter++; }

void Player::endGame()
{
	Player::moveAgain = false;
}

int* Player::getInfo()
{
    int* info = new int[6];

    info[0] = Player::buyingThreshold;
    info[1] = Player::buildingThreshold;
    info[2] = Player::jailTime;
    info[3] = Player::smartJailStrategy;
    info[4] = Player::completeMonopoly;
    info[5] = Player::developmentThreshold;
    info[6] = Player::maxAuctionBid;

    return info;
}

