/*
 * =====================================================================================
 *
 *       Filename:  game.cpp
 *
 *    Description:  Does magic to play a game of Monopoly
 *
 *        Version:  1.0
 *        Created:  09/02/2014 13:53:59
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */

#include "game.h"
#include "player.h"
#include "boardlocation.h"

#include<iostream>
#include<string>
#include<vector>
#include<algorithm>
#include<cstdlib>
#include<ctime>
#include<cmath>
#include<functional>

Game::Game(std::vector<Player*> players, int cutoff)
{
	Game::players = players;
	Game::numberOfPlayers = (int) (players.size());
	Game::cutoff = cutoff;
}

Game::Game(std::vector<Player*> players, bool auct, bool fpp, bool dog, bool nrij, bool tts, bool seb, int cutoff=300)
{
	Game::players = players;
	Game::numberOfPlayers = (sizeof(Game::players)/sizeof(Game::players[0]));
	Game::auctionsEnabled = Game::auctionsEnabled && auct;
	Game::freeParkingPool = Game::freeParkingPool && fpp;
	Game::doubleOnGo = Game::doubleOnGo && dog;
	Game::noRentInJail = Game::noRentInJail && nrij;
	Game::tripToStart = Game::tripToStart && tts;
	Game::snakeEyesBonus = Game::snakeEyesBonus && seb;
	Game::cutoff = cutoff;
}

Game::~Game()
{
    for (int i = 0; i < 40; i++)
    {
        delete board[i];
    }
}

void Game::createCards()
	{
		for (int i = 0; i < NUMBER_OF_CARDS; i++)
		{
			chanceCards[i] = i + 1;
			communityChestCards[i] = i + 1;
		}

		std::random_shuffle(&chanceCards[0], &chanceCards[15]);
		std::random_shuffle(&communityChestCards[0], &communityChestCards[15]);
	}

void Game::createBoard()
	{
		board[0] = (new BoardLocation(0, "Go"));
		board[1] = (new BoardLocation(1, "Mediterranean Ave.", 60, "Brown", std::vector<int> {2, 10, 30, 90, 160, 250} , 50));
		board[2] = (new BoardLocation(2, "Community Chest"));
		board[3] = (new BoardLocation(3, "Baltic Ave.", 60, "Brown", std::vector<int> {4, 20, 60, 180, 320, 450}, 50));
		board[4] = (new BoardLocation(4, "Income Tax"));
		board[5] = (new BoardLocation(5, "Reading Railroad", 200, "Railroad"));
		board[6] = (new BoardLocation(6, "Oriental Ave.", 100, "Light Blue", std::vector<int> {6, 30, 90, 270, 400, 550}, 50));
		board[7] = (new BoardLocation(7, "Chance"));
		board[8] = (new BoardLocation(8, "Vermont Ave.", 100, "Light Blue", std::vector<int> {6, 30, 90, 270, 400, 550}, 50));
		board[9] = (new BoardLocation(9, "Connecticut Ave.", 120, "Light Blue", std::vector<int> {8, 40, 100, 300, 450, 600}, 50));
		board[10] = (new BoardLocation(10, "Just Visiting / In Jail"));
		board[11] = (new BoardLocation(11, "St. Charles Place", 140, "Pink", std::vector<int> {10, 50, 150, 450, 625, 750}, 100));
		board[12] = (new BoardLocation(12, "Electric Company", 150, "Utility"));
		board[13] = (new BoardLocation(13, "States Ave.", 140, "Pink", std::vector<int> {10, 50, 150, 450, 625, 750}, 100));
		board[14] = (new BoardLocation(14, "Virginia Ave.", 160, "Pink", std::vector<int> {12, 60, 180, 500, 700, 900}, 100));
		board[15] = (new BoardLocation(15, "Pennsylvania Railroad", 200, "Railroad"));
		board[16] = (new BoardLocation(16, "St. James Place", 180, "Orange", std::vector<int> {14, 70, 200, 550, 750, 950}, 100));
		board[17] = (new BoardLocation(17, "Community Chest"));
		board[18] = (new BoardLocation(18, "Tennessee Ave.", 180, "Orange", std::vector<int> {14, 70, 200, 550, 750, 950}, 100));
		board[19] = (new BoardLocation(19, "New York Ave.", 200, "Orange", std::vector<int> {16, 80, 220, 600, 800, 1000}, 100));
		board[20] = (new BoardLocation(20, "Free Parking"));
		board[21] = (new BoardLocation(21, "Kentucky Ave.", 220, "Red", std::vector<int> {18, 90, 250, 700, 875, 1050}, 150));
		board[22] = (new BoardLocation(22, "Chance"));
		board[23] = (new BoardLocation(23, "Indiana Ave.", 220, "Red", std::vector<int> {18, 90, 250, 700, 875, 1050}, 150));
		board[24] = (new BoardLocation(24, "Illinois Ave.", 240, "Red", std::vector<int> {20, 100, 300, 750, 925, 1100}, 150));
		board[25] = (new BoardLocation(25, "B. & O. Railroad", 200, "Railroad"));
		board[26] = (new BoardLocation(26, "Atlantic Ave.", 260, "Yellow", std::vector<int> {22, 110, 330, 800, 975, 1150}, 150));
		board[27] = (new BoardLocation(27, "Ventnor Ave.", 260, "Yellow", std::vector<int> {22, 110, 330, 800, 975, 1150}, 150));
		board[28] = (new BoardLocation(28, "Water Works", 150, "Utility"));
		board[29] = (new BoardLocation(29, "Marvin Gardens", 280, "Yellow", std::vector<int> {24, 120, 360, 850, 1025, 1200}, 150));
		board[30] = (new BoardLocation(30, "Go to Jail"));
		board[31] = (new BoardLocation(31, "Pacific Ave.", 300, "Green", std::vector<int> {26, 130, 390, 900, 1100, 1275}, 200));
		board[32] = (new BoardLocation(32, "North Carolina Ave.", 300, "Green", std::vector<int> {26, 130, 390, 900, 1100, 1275}, 200));
		board[33] = (new BoardLocation(33, "Community Chest"));
		board[34] = (new BoardLocation(34, "Pennsylvania Ave.", 320, "Green", std::vector<int> {28, 150, 450, 1000, 1200, 1400}, 200));
		board[35] = (new BoardLocation(35, "Short Line Railroad", 200, "Railroad"));
		board[36] = (new BoardLocation(36, "Chance"));
		board[37] = (new BoardLocation(37, "Park Place", 350, "Dark Blue", std::vector<int> {35, 175, 500, 1100, 1300, 1500}, 200));
		board[38] = (new BoardLocation(38, "Luxury Tax"));
		board[39] = (new BoardLocation(39, "Boardwalk", 400, "Dark Blue", std::vector<int> {50, 200, 600, 1400, 1700, 2000}, 200));

        std::copy(board, board + 40, std::inserter(unownedProperties, unownedProperties.end())); // doublecheck
	}

void Game::communityChest(Player* player)
{
	int card = communityChestCards[communityChestIndex];

	switch (card)
	{
	case 0: // The card's been 'removed'.
		communityChestIndex++;
		Game::communityChest(player);
		break;
	case 1: // Get out of jail free
		player->flipCommunityChestCard();
		communityChestCards[communityChestIndex] = 0;
		communityChestJailIndex = communityChestIndex;
		break;
	case 2: // Pay school fees of $50 [2008 update]
		Game::changeMoney(player, -50);
		moneyInFP += 50;
		break;
	case 3: // It is your birthday \ Collect $10 from every player [2008 update]
            for (auto i : players)
		{
			Game::changeMoney(i, -10);
			Game::changeMoney(player, 10);
		}
		break;
	case 4: // Xmas fund matures / Collect $100
		Game::changeMoney(player, 100);
		break;
	case 5: // Income tax refund/ Collect $20
		Game::changeMoney(player, 20);
		break;
	case 6: // You inherit $100
		Game::changeMoney(player, 100);
		break;
	case 7: // You have won second prize in a beauty concert / Collect $10
		Game::changeMoney(player, 10);
		break;
	case 8: // Bank error in your favor / collect $200
		Game::changeMoney(player, 200);
		break;
	case 9: // Receive $25 \ Consultancy fee [2008 update - wording change]
		Game::changeMoney(player, 25);
		break;
	case 10: // Advance to go (collect $200)
		Game::moveTo(player, 0); // Player moves to Go.
		break;
	case 11: // You are assessed for street repairs
        {
		int houses = 0, hotels = 0;

		if (player->getMonopolies()->empty())
		{
            for (auto i : *player->getInventory())
			{
				if (5 == i->getBuildings())
                {
					hotels++;
                }
				else
                {
					houses += i->getBuildings();
                }
			}
			int houseRepairs = 40 * houses;
			int hotelRepairs = 115 * hotels;

			Game::changeMoney(player, (houseRepairs + hotelRepairs));
			moneyInFP += houseRepairs + hotelRepairs;
		}
            
        break;
        }
	case 12: // Life insurance matures / Collect $100
		Game::changeMoney(player, 100);
		break;
	case 13: // Doctor's fee / Pay $50
		Game::changeMoney(player, -50);
		moneyInFP += 50;
		break;
	case 14: // From sale of stock / You get $50 [2008 update]
		Game::changeMoney(player, 50);
		break;
	case 15: // Pay hospital $100
		Game::changeMoney(player, -100);
		moneyInFP += 100;
		break;
	case 16:
		Game::goToJail(player);
		break;
	}

	communityChestIndex = (communityChestIndex + 1) % NUMBER_OF_CARDS;
}

void Game::chance(Player* player)
{
	int card = chanceCards[chanceIndex];

	switch (card)
	{
	case 0: // The card's been 'removed'.
		chanceIndex++;
		Game::chance(player);
		break;
	case 1: // Get out of jail free
		player->flipChanceCard();
		chanceCards[chanceIndex] = 0;
		chanceJailIndex = chanceIndex;
		break;
	case 2: // Go directly to jail
		Game::goToJail(player);
		break;
	case 3: // Your building loan matures / Collect $150
		Game::changeMoney(player, 150);
		break;
	case 4: // Go back 3 spaces
		player->changePosition(-3);
		board[player->getPosition()]->incrementVisits(); // Increase hit counter
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 5:
	case 11: // Advance token to the nearest railroad
		if (player->getPosition() <= 7)
			Game::moveTo(player, 15);
		else if (player->getPosition() <= 22)
			Game::moveTo(player, 25);
		else if (player->getPosition() <= 36)
			Game::moveTo(player, 5);
		player->setCardRent(true);
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 6: // Advance to Go (Collect $200)
		Game::moveTo(player, 0);
		break;
	case 7: // Advance to Illinois Ave.
		Game::moveTo(player, 24);
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 8: // Make general repairs on all your property.
        {
		int houses = 0, hotels = 0;

		if (player->getMonopolies()->empty())
		{
            for (auto i : *player->getInventory())
			{
				if (5 == i->getBuildings())
					hotels++;
				else
					houses += i->getBuildings();
			}
			int houseRepairs = 45 * houses;
			int hotelRepairs = 100 * hotels;

			Game::changeMoney(player, (houseRepairs + hotelRepairs));
			moneyInFP += houseRepairs + hotelRepairs;
		}
		break;
        }
	case 9: // Advance to St. Charles Place
		Game::moveTo(player, 11);
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 10: // Advance token to nearest utility
		if (player->getPosition() <= 7)
			Game::moveTo(player, 12);
		else if (player->getPosition() <= 22)
			Game::moveTo(player, 28);
		else if (player->getPosition() <= 36)
			Game::moveTo(player, 12);
		player->setCardRent(true);
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 12: // Pay poor tax of $15
		Game::changeMoney(player, -15);
		moneyInFP += 15;
		break;
	case 13: // Take a ride on the Reading Railroad
		Game::moveTo(player, 5);
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 14: // Advance token to Board Walk [sic]
		Game::moveTo(player, 39);
		Game::boardAction(player, board[player->getPosition()]);
		break;
	case 15: // Pay each player $50
            for (auto i : players)
		{
			Game::changeMoney(i, 50);
			Game::changeMoney(player, -50);
		}
		break;
	case 16: // Bank pays you divident of $50
		Game::changeMoney(player, 50);
		break;
	}
	chanceIndex = (chanceIndex + 1) % NUMBER_OF_CARDS;
}

void Game::moveAhead(Player* player, int numberOfSpaces)
{
	int newPosition = (player->getPosition() + numberOfSpaces) % 40;

	if (newPosition < player->getPosition()) // Does the player pass Go?
	{
		Game::changeMoney(player, 200);
		player->passGo();
	}
	player->setPosition(newPosition);
	board[newPosition]->incrementVisits();
//	std::cout << "Hello" << std::endl;
}

void Game::moveTo(Player* player, int newPosition)
{
	if (newPosition < player->getPosition()) // Does the player pass Go?
	{
		Game::changeMoney(player, 200);
		player->passGo();
	}
	player->setPosition(newPosition);
	board[newPosition]->incrementVisits();
}

void Game::payOutOfJail(Player* player)
{
	if (player->hasChanceCard())
	{
		player->flipChanceCard();
		chanceCards[chanceJailIndex] = 1;
	}
	else if (player->hasCommunityChestCard())
	{
		player->flipCommunityChestCard();
		communityChestCards[communityChestJailIndex] = 1;
	}
	else
	{
		Game::changeMoney(player, -50);
	}
}

void Game::goToJail(Player* player)
{
	player->setPosition(10);
	board[10]->incrementVisits();
	moveAgain = false;
    player->setInJail(true);

	if (player->hasSmartJailStrategy() && firstBuilding)
	{
		player->setJailTime(3);
	}
	else
	{
		player->setJailTime(player->getInitJailTime());
	}
}

void Game::buyProperty(Player* player, BoardLocation* boardSpace, int customPrice=0)
{
	if (customPrice)
	{
		Game::changeMoney(player, -customPrice);
	}
	else
	{
		Game::changeMoney(player, -boardSpace->getPrice());
	}

	unownedProperties.erase(boardSpace);
	player->appendToInventory(boardSpace);

	if (monopolyStatus(player, boardSpace))
	{
		player->appendToMonopolies(*boardSpace->getGroup());
	}
}

Player* Game::propertyOwner(BoardLocation* property)
{
    for (auto i : players)
	{
        if (i->isInInventory(property))
		{
			return (i);
		}
	}
    return (NULL);
}

void Game::payRent(Player* player)
{
	BoardLocation* currentProperty = board[player->getPosition()];
	Player* owner = Game::propertyOwner(currentProperty);
    if (owner == NULL)
    {
        return;
    }

	int rent = 0;

	if (noRentInJail && owner->isInJail())
		return;

	if (*currentProperty->getGroup() == "Railroad")
	{
		int railroadCounter = 0;
        for (auto i : *owner->getInventory())
		{
			if (*i->getGroup() == "Railroad")
			{
				railroadCounter++;
			}
		}

		rent = 25 * std::pow(2.0, railroadCounter - 1);

		if (player->getCardRent())
		{
			rent *= 2;
		}
	}
	else if (*currentProperty->getGroup() == "Utility")
	{
        diceRoll = Game::rollDie(); // TODO: Check this
		int utilityCounter = 0;
        for (auto i : *owner->getInventory())
		{
			if (*i->getGroup() == "Utility")
                utilityCounter++;
		}

		if (utilityCounter == 2 || player->getCardRent())
		{
			rent = diceRoll * 10;
		}
		else
		{
			rent = diceRoll * 4;
		}
	}
	else // for color group properties
	{
		if (currentProperty->getBuildings() == 5) // Hotel?
		{
			rent = currentProperty->getRents(5);
		}
		else if (0 < currentProperty->getBuildings() && currentProperty->getBuildings() < 5)
		{
			rent = currentProperty->getRents(currentProperty->getBuildings());
		}
		else
		{
            if (owner->isInMonopolies(*currentProperty->getGroup()))
            {
                rent = currentProperty->getRents(0) * 2;
                
                /*// If a property in the monopoly is mortgaged, redefine the rent.
                 for (auto i : *owner->getInventory())
                 {
                 if (i->getGroup() == currentProperty->getGroup() && i->isMortgaged())
                 {
                 rent = currentProperty->getRents(0);
                 }*/
            }
            else // The player does not have a monopoly
            {
                rent = currentProperty->getRents(0);
            }
        }
    }


    // Let's pay this rent!
    Game::changeMoney(player, -rent);
    Game::changeMoney(owner, rent);
}

int Game::unmortgagePrice(BoardLocation* property)
{
    return ((int) 1.1 * (property->getPrice() / 2)); // TODO: Check rounding
}

void Game::sellBuilding(Player* player, BoardLocation* property, std::string building)
{
    if (building == "house")
    {
        property->changeBuildings(-1);
        houses += 1;
        player->addMoney(property->getHouseCost() / 2); // Better than setting the member variable?
    }
    else if (building == "hotel")
    {
        property->changeBuildings(-1);
        hotels += 1;
        houses -= 4;
        player->addMoney((property->getHouseCost() / 2) * 5);
    }
    else if (building == "all")
    {
        if (property->getBuildings() == 5)
        {
            property->changeBuildings(-5);
            hotels++;
            player->addMoney((property->getHouseCost() / 2 * property->getBuildings()));
            property->changeBuildings(-property->getBuildings());
        }
    }
}

void Game::changeMoney(Player* player, int amount)
{
    player->addMoney(amount);
    
    if (player->getMoney() <= 0)
    {
        // Mortgage properties if they're not in a monopoly.
        for (auto boardSpace : *player->getInventory())
        {
            if (!player->isInMonopolies(*boardSpace->getGroup()) && !boardSpace->isMortgaged())
            {
                int mortgageValue = boardSpace->getPrice() / 2;
                player->addMoney(mortgageValue);
                boardSpace->setMortgaged(true);
                if (player->getMoney() > 0)
                    return;
            }
        }
        
        // Sell houses and hotels.
        
        if (!player->getMonopolies()->empty()) // verify
        {
            bool keepSelling = true;
            
            while (keepSelling)
            {
                keepSelling = false;
                
                for (auto boardSpace : *player->getInventory())
                {
                    if (boardSpace->getBuildings() > 0 && Game::evenSellingTest(boardSpace, player))
                    {
                        keepSelling = true;
                        if (boardSpace->getBuildings() == 5)
                        {
                            if (houses >= 4)
                            {
                                Game::sellBuilding(player, boardSpace, "hotel");
                            }
                            else // Not enough houses to break hotel.
                            {
                                for (auto i : *player->getInventory())
                                {
                                    if (i->getGroup() == boardSpace->getGroup())
                                    {
                                        Game::sellBuilding(player, i, "all");
                                    }
                                }
                            }
                        }
                        else // It's a house
                        {
                            Game::sellBuilding(player, boardSpace, "house");
                        }
                        if (player->getMoney() > 0)
                            return;
                    }
                }
            }
            for (auto boardSpace : *player->getInventory())
            {
                if (!boardSpace->isMortgaged())
                {
                    if (player->isInMonopolies(*boardSpace->getGroup()))
                    {
                        //throw 2; // ???
                    }
                    
                    int mortgageValue = boardSpace->getPrice() / 2;
                    player->addMoney(mortgageValue);
                    boardSpace->setMortgaged(true);
                    
                    if (player->getMoney() > 0)
                    {
                        return;
                    }
                }
            }
        }
    }
}

bool Game::evenSellingTest(BoardLocation* property, Player* player)
{
    bool testResult = true;
    for (auto boardSpace : *player->getInventory())
    {
        if (boardSpace->getGroup() == property->getGroup() && boardSpace->getBuildings() - property->getBuildings() > 0)
    
            testResult = false;
    }
    return (testResult);
}

bool Game::evenBuildingTest(BoardLocation* property, Player* player)
{
    bool testResult = true;
    for (auto boardSpace : *player->getInventory())
    {
        if (boardSpace->getGroup() == property->getGroup() && property->getBuildings() - boardSpace->getBuildings() > 0)
        {
            testResult = false;
        }
    }
    return (testResult);
}

bool Game::mortgageCheck(BoardLocation* property, Player* player)
{
    bool testResult = true;
    for (auto aProperty : *player->getInventory())
    {
        if (aProperty->getBuildings() > 0 && aProperty->getGroup() == property->getGroup())
        {
            testResult = false;
        }
    }
    
    return (testResult);
}

void Game::developProperties(Player* player)
{
    // Unmortgage proprties in monopolies, if possible.
    for (auto boardSpace : *player->getInventory())
    {
        if (boardSpace->isMortgaged() && player->isInMonopolies(*boardSpace->getGroup()))
        {
            int unmortgagePrice = Game::unmortgagePrice(boardSpace);
            if (player->getMoney() - unmortgagePrice >= player->getBuyingThreshold())
            {
                player->addMoney(-unmortgagePrice);
                boardSpace->setMortgaged(false);
            }
            else
                return;
        }
    }
    
    // Buy buildings
    if (!player->getMonopolies()->empty())
    {
        bool keepBuilding = true;
        while (keepBuilding)
        {
            keepBuilding = false;
            for (auto boardSpace : *player->getInventory())
            {
                if (player->isInInventory(boardSpace))
                {
                    if (Game::evenBuildingTest(boardSpace, player))
                    {
                        if (boardSpace->getBuildings() < player->getBuildingThreshold())
                        {
                            if (boardSpace->isMortgaged());
                                //throw 2;
                            
                            int availableCash = 0, availableMorgageValue = 0;
                            // Calculate current cash available
                            if (player->getDevelopmentThreshold() == 1)
                                availableCash += player->getMoney() - 1;
                            else if (player->getDevelopmentThreshold() == 2)
                            {
                                for (auto property : *player->getInventory())
                                {
                                    if (!player->isInMonopolies(*property->getGroup()) && !property->isMortgaged())
                                    
                                        availableMorgageValue += property->getPrice() / 2;
                                    
                                    availableCash = availableMorgageValue + player->getMoney();
                                }
                            }
                            else
                            {
                                availableCash = player->getMoney() - player->getBuyingThreshold();
                            }
                            
                            if (availableCash - boardSpace->getHouseCost() >= 0) // The player can afford it.
                            {
                                int buildingSupply = 0;
                                std::string building;
                                if (boardSpace->getBuildings() < 4)
                                {
                                    buildingSupply = houses;
                                    building = "house";
                                }
                                else if (boardSpace->getBuildings() == 4)
                                {
                                    buildingSupply = hotels;
                                    building = "hotel";
                                }
                                
                                // Check if there's a building available.
                                if (buildingSupply > 0)
                                {
                                    if (building == "house")
                                        houses--;
                                    else if (building == "hotel")
                                    {
                                        hotels--;
                                        houses += 4;
                                    }
                                    
                                    boardSpace->changeBuildings(1);
                                    player->addMoney(-boardSpace->getHouseCost());
                                    
                                    if (player->getDevelopmentThreshold() != 2 && player->getMoney() < 0);
                                        
                                        //throw 20;
                                    
                                    if (player->getDevelopmentThreshold() == 2)
                                    {
                                        for (auto cProperty : *player->getInventory()) // !!!DEVIATION ALERT!!!
                                        {
                                            if (player->getMoney() <= 0)
                                            {
                                                break;
                                            }
                                            
                                            
                                            if (!player->isInMonopolies(*cProperty->getGroup()) && !cProperty->isMortgaged())
                                            {
                                                if (Game::mortgageCheck(cProperty, player))
                                                {
                                                    cProperty->setMortgaged(true);
                                                    player->addMoney(cProperty->getPrice());
                                                }
                                            }
                                        }
                                    }
                                    
                                    keepBuilding = true;
                                    firstBuilding = true; // Buildings have been built.
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    // Unmortgage singleton properties
    for (auto boardSpace : *player->getInventory())
    {
        if (boardSpace->isMortgaged())
        {
            int unmortgagedPrice = Game::unmortgagePrice(boardSpace);
            if (player->getMoney() - unmortgagedPrice >= player->getBuyingThreshold())
            {
                player->addMoney(-unmortgagedPrice);
                boardSpace->setMortgaged(false);
            }
            else
                return;
        }
    }
}

// Doesn't edeal with additional properties...yet.
bool Game::monopolyStatus(Player* player, BoardLocation* boardSpace)
{
    std::string group = *boardSpace->getGroup();
    
    if (group == "" || group == "Railroad" || group == "Utility")
    {
        return (false);
    }
    
    int propertyCounter = 0;
    
    for (auto property : *player->getInventory())
    {
        if (*property->getGroup() == group)
        {
            propertyCounter++;
        }
    }
    
    if (propertyCounter == 3 && (group == "Light Blue" || group == "Pink" || group == "Orange" || group == "Red" || group == "Yellow" || group == "Green"))
    {
        return (true);
    }
    else if (propertyCounter == 2 && (group == "Dark Blue" || group == "Brown"))
    {
        return (true);
    }
    return (false);
}

int Game::findAvailableMortgageValue(Player* player)
{
    int available = 0;
    bool addMyValue;
    for (auto property : *player->getInventory())
    {
        if (property->getBuildings() == 0 && !property->isMortgaged() && !player->isInMonopolies(*property->getGroup()))
        {
            addMyValue = true;
            
            /*if (player->isInMonopolies(*property->getGroup()))
            {
                for (auto aProperty : *player->getInventory())
                {
                    if (aProperty->getBuildings() > 0 && aProperty->getGroup() == property->getGroup())
                    {
                        addMyValue = false;
                    }
                }
            }*/
            
            if (addMyValue)
            {
                available += property->getPrice() / 2;
            }
        }
    }
    
    return (available);
}

void Game::auction(BoardLocation* boardSpace)
{
    int winningBid = 0;
    Player* winningPlayer = NULL;
    
    for (auto player : players)
    {
        player->setBidIncludesMortgages(false);
        
        if (player->isInGroupPreferences(*boardSpace->getGroup()))
        {
            player->setAuctionBid(player->getMoney() - 1);
        }
        
        else if (1 == player->getCompleteMonopoly() && Game::monopolyStatus(player, boardSpace))
        {
            player->setAuctionBid(player->getMoney() - 1);
        }
        
        else if (2 == player->getCompleteMonopoly() && Game::monopolyStatus(player, boardSpace))
        {
            player->setBidIncludesMortgages(true);
            int availableMortgageValue = Game::findAvailableMortgageValue(player);
            player->setAuctionBid(player->getMoney() + availableMortgageValue - 1);
        }
        
        else
        {
            player->setAuctionBid(player->getMoney() - player->getBuyingThreshold());
        }
    }
    
    Player* player1 = players[0];
    Player* player2 = players[1];
    
    if (player1->getAuctionBid() < 1 && player2->getAuctionBid() < 1)
        return;
    
    else if (player1->getAuctionBid() > 0 && player2->getAuctionBid() < 1)
    {
        winningBid = 1;
        winningPlayer = player1;
    }
    
    else if (player1->getAuctionBid() < 1 && player2->getAuctionBid() > 0)
    {
        winningBid = 1;
        winningPlayer = player2;
    }
    
    else if (player1->getAuctionBid() == player2->getAuctionBid())
    {
        winningPlayer = player1->getNumber() == 0 ? player1 : player2;
        winningBid = winningPlayer->getAuctionBid();
    }
    
    else if (player1->getAuctionBid() > player2->getAuctionBid())
    {
        winningBid = player2->getAuctionBid() + 1;
        winningPlayer = player1;
    }
    
    else if (player2->getAuctionBid() > player1->getAuctionBid())
    {
        winningBid = player1->getAuctionBid() + 1;
        winningPlayer = player2;
    }
    
    else
    {
        //throw 20;
        return;
    }
    
    // Special buying procedure if the player wants to include mortgages.
    if (winningPlayer->getBidIncludesMortgages())
    {
        winningPlayer->addMoney(-winningBid);
        
        // Make up the funds...
        
        for (auto property : *winningPlayer->getInventory()) // !!!DEVIATION ALERT!!!
        {
            if (winningPlayer->getMoney() <= 0)
            {
                break;
            }
            
            if (property->getBuildings() == 0 && !property->isMortgaged() && !winningPlayer->isInMonopolies(*property->getGroup()))
            {
                if (Game::mortgageCheck(property, winningPlayer))
                {
                    property->setMortgaged(true);
                    winningPlayer->addMoney(property->getPrice() / 2);
                }
            }
            
        }
        
        unownedProperties.erase(boardSpace); // Pointer?
        
        winningPlayer->appendToInventory(boardSpace);
        winningPlayer->appendToMonopolies(*boardSpace->getGroup());
    }
    
    else
    {
        Game::buyProperty(winningPlayer, boardSpace, winningBid);
    }
}

int Game::totalAssets(Player* player)
{
    int liquidProperty = 0; // Liquidated property wealth of player
    for (auto boardSpace : *player->getInventory())
    {
        liquidProperty += boardSpace->getPrice();
    }
    
    int liquidBuildings = 0; // Cost of all buildings player owns
    for (auto boardSpace : *player->getInventory())
    {
        liquidBuildings += boardSpace->getBuildings() * boardSpace->getHouseCost();
    }
    
    return (player->getMoney() + liquidBuildings + liquidProperty);
}

void Game::propertyAction(Player* player, BoardLocation* boardSpace)
{
    if (player->isInInventory(boardSpace)) // Player owns property, nothing happens.
    {
        ; // do nothing, TODO: rewrite
    }
    else if (boardSpace->isMortgaged()) // Property is mortgaged, nothing happens.
    {
        ; // do nothing
    }
    
    else if (std::find(unownedProperties.begin(), unownedProperties.end(), boardSpace) != unownedProperties.end())
    {
        if (tripToStart && !player->hasPassedGo())
        {
            ; // do nothing
        }
        else
        {
            if (player->getMoney() - boardSpace->getPrice() >= player->getBuyingThreshold())
            {
                Game::buyProperty(player, boardSpace);
            }
            
            else if (player->isInGroupPreferences(*boardSpace->getGroup()) && boardSpace->getPrice() > 0)
            {
                Game::buyProperty(player, boardSpace);
            }
            
            else if (player->getCompleteMonopoly() == 1 && player->getMoney() - boardSpace->getPrice() > 0 && Game::monopolyStatus(player, boardSpace))
            {
                Game::buyProperty(player, boardSpace);
            }
            
            else if (player->getCompleteMonopoly() == 2 && Game::monopolyStatus(player, boardSpace))
            {
                if ((player->getMoney() + Game::findAvailableMortgageValue(player)) - boardSpace->getPrice() > 0)
                {
                    player->addMoney(-boardSpace->getPrice());
                    
                    
                    for (auto cProperty : *player->getInventory()) // !!!DEVIATION ALERT!!!
                    {
                        if (player->getMoney() <= 0)
                        {
                            break;
                        }
                        if (cProperty->getBuildings() == 0 && !cProperty->isMortgaged() && !player->isInMonopolies(*cProperty->getGroup()))
                        {
                            if (Game::mortgageCheck(cProperty, player))
                            {
                                cProperty->setMortgaged(true);
                                player->addMoney(cProperty->getPrice() / 2);
                            }
                        }
                    }
                    
                    unownedProperties.erase(boardSpace);
                    player->appendToMonopolies(*boardSpace->getGroup());
                }
            }
            
            else // Player can't buy it or decides not to.
            {
                if (auctionsEnabled)
                {
                    Game::auction(boardSpace);
                }
            }
        }
    }
    
    else // Property is owned by another player.
    {
        Game::payRent(player);
    }
}

void Game::boardAction(Player* player, BoardLocation* boardSpace)
{
    if (*boardSpace->getName() == "Go" || *boardSpace->getName() == "Just Visiting / In Jail")
    {
        ; // do nothing - TODO: restructure
    }
    
    else if (*boardSpace->getName() == "Go")
    {
        if (doubleOnGo)
        {
            Game::changeMoney(player, 200);
        }
    }
    
    else if (*boardSpace->getName() == "Income Tax")
    {
        Game::changeMoney(player, -200);
        
        if (freeParkingPool)
        {
            moneyInFP += 200;
        }
    }
    
    else if (*boardSpace->getName() == "Free Parking")
    {
        if (freeParkingPool)
        {
            Game::changeMoney(player, moneyInFP);
            moneyInFP = 0;
        }
    }
    
    else if (*boardSpace->getName() == "Chance")
    {
        Game::chance(player);
    }
    
    else if (*boardSpace->getName() == "Community Chest")
    {
        Game::communityChest(player);
    }
    
    else if (*boardSpace->getName() == "Go to Jail")
    {
        Game::goToJail(player);
    }
    
    else if (*boardSpace->getName() == "Luxury Tax")
    {
        Game::changeMoney(player, -100);
        
        if (freeParkingPool)
        {
            moneyInFP += 100;
        }
    }
    
    else
    {
        propertyAction(player, boardSpace);
    }
    
    player->setCardRent(false);
}

void Game::takeTurn(Player* player)
{
    turnCounter++;
    doublesCounter = 0;
    
    int die1 = Game::rollDie();
    int die2 = Game::rollDie();
    diceRoll = die1 + die2;
    
    if (snakeEyesBonus && die1 == 1 && die2 == 1)
    {
        Game::changeMoney(player, 500);
    }
    
    if (player->isInJail())
    {
        player->incrementJailCounter();
        
        if (player->getJailCounter() - 1 == player->getJailTime() || (die1 != die2 && player->getJailCounter() == 3))
        {
            player->setJailCounter(0);
            moveAgain = true;
            Game::payOutOfJail(player);
        }
        
        else if (die1 == die2)
        {
            player->setJailCounter(0);
            moveAgain = true;
        }
        
        else
        {
            moveAgain = false;
        }
    }
    
    else
    {
        moveAgain = true;
    }
    
    while (moveAgain && player->getMoney() > 0)
    {
        if (doublesCounter > 0)
        {
            die1 = Game::rollDie();
            die2 = Game::rollDie();
            diceRoll = die1 + die2;
            
            if (snakeEyesBonus && die1 == 1 && die2 == 1)
            {
                Game::changeMoney(player, 500);
            }
        }
        
        if (die1 == die2 && !player->isInJail())
        {
            doublesCounter++;
            if (doublesCounter == 3)
            {
                Game::goToJail(player);
                return;
            }
            
            else
            {
                moveAgain = true;
            }
        }
        
        else
        {
            player->setInJail(false);
            moveAgain = false;
        }
        
        Game::moveAhead(player, diceRoll);
        BoardLocation* boardSpace = board[player->getPosition()];
        
        Game::boardAction(player, boardSpace);
        
        if (player->isInJail())
        {
            return;
        }
    }
}

void Game::updateStatus()
{
    for (auto player : players)
    {
        if (player->getMoney() <= 0)
        {
            gameStatus = false; // TODO: Should be bool or string?
            if (player->getNumber() == 1)
            {
                result = 2;
            }
            else if (player->getNumber() == 2)
            {
                result = 1;
            }
        }
    }
    
    if (turnCounter == cutoff)
    {
        gameStatus = false;
        result = 0;
    }
}

endReport Game::play()
{
    int playingOrder[2];
    playingOrder[0] = Game::chooseRandomPlayer();
    playingOrder[1] = playingOrder[0] == 0 ? 1 : 0;
    
    int currentPlayerIndex = 0;
    
    Game::createBoard();
    
    while (gameStatus)
    {
        if (0 == currentPlayerIndex)
        {
            Game::developProperties(players[0]);
            Game::developProperties(players[1]);
        }
        else
        {
            Game::developProperties(players[1]);
            Game::developProperties(players[0]);
        }
        
        Game::takeTurn(players[playingOrder[currentPlayerIndex]]);
        
        currentPlayerIndex = (currentPlayerIndex + 1) % numberOfPlayers;
        
        Game::updateStatus();
    }
    
    endReport report;
    report.result = result;
    report.turnCounter = turnCounter;
    report.player0Monopolies = *players[0]->getMonopolies();
    report.player1Monopolies = *players[1]->getMonopolies();
    report.player0Money = players[0]->getMoney();
    report.player1Money = players[1]->getMoney();
    
    return (report); // Check for efficiency.
}

int Game::rollDie()
{
	std::srand((int) std::time(NULL) + rand());
	return (std::rand() % 6 + 1);
}

int Game::chooseRandomPlayer()
{
	std::srand((int) std::time(NULL) + rand());
	return (std::rand() % 1 + 1);
}
