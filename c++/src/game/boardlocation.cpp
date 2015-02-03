/*
 * =====================================================================================
 *
 *       Filename:  boardlocation.cpp
 *
 *    Description:  Represent a location on a monopoly gameboard.
 *
 *        Version:  1.0
 *        Created:  09/02/2014 12:19:05
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */

#include "game/boardlocation.h"

#include<vector>

/**
 * Basic BoardLocation constructor for non-properties
 *
 * Needed for creation of some of the "non-property" spaces.
 *
 * @param id Numerical id of the location, where 0 is Go and 40 is Boardwalk
 * @param name Friendly name of the location
 */
BoardLocation::BoardLocation(int id, std::string name)
{
	BoardLocation::id = id;
	BoardLocation::name = name;


}

/**
 * More detailed BoardLocation constructor for railroads, etc
 *
 * This is what some properties such as railroads use.
 *
 * @param id Numerical id of the location, where 0 is Go and 40 is Boardwalk
 * @param name Friendly name of the location
 * @param price Integer price of the property
 * @param group Color group the property belongs to, e.g. "Red"
 */
BoardLocation::BoardLocation(int id, std::string name, int price, std::string group)
{
	BoardLocation::id = id;
	BoardLocation::name = name;
	BoardLocation::price = price;
	BoardLocation::group = group;
}

/**
 * Most detailed BoardLocation constructor for properties
 *
 * This is what most properties use as it fills in most information.
 *
 * @param id Numerical id of the location, where 0 is Go and 40 is Boardwalk
 * @param name Friendly name of the location
 * @param price Integer price of the property
 * @param group Color group the property belongs to, e.g. "Red"
 * @param rents List of the 6 rents on property (singleton, monopoly, 1-4 houses, hotel)
 * @param houseCost The cost to buy/build one house on the property
 */
BoardLocation::BoardLocation(int id, std::string name, int price, std::string group, std::vector<int> rents, int houseCost)
{
	BoardLocation::id = id;
	BoardLocation::name = name;
	BoardLocation::price = price;
	BoardLocation::group = group;
	BoardLocation::rents = rents;
	BoardLocation::houseCost=houseCost;
}

// Getters and Setters
/**
 * Gets the space ID (0..40) of the location
 * @return numerical positional identifier
 */
int BoardLocation::getID()
{
	return (id);
}

/**
 * Gets the friendly name of the property
 * @return pointer to a string containing the name
 */
std::string* BoardLocation::getName()
{
	return (&name);
}

/**
 * Gets the purchase price of the property, as displayed on the card
 * @return price of property
 */
int BoardLocation::getPrice()
{
	return (price);
}

/**
 * Gets the rent for a specific case
 * @param position the rent to get, where 0 is a singleton and 5 is a hotel
 * @return the rent in Monopoly dollars
 */
int BoardLocation::getRents(int position)
{
	return (rents[position]);
}

/**
 * Gets the cost to buy/build a house
 * @return the cost in Monopoly dollars
 */
int BoardLocation::getHouseCost()
{
	return (houseCost);
}

/**
 * Gets the color group the property belongs to, e.g. "Red"
 * @return a pointer to the color group
 */
std::string* BoardLocation::getGroup()
{
	return (&group);
}

/**
 * Gets the number of buildings on the property
 *
 * 0: no buildings
 * 1-4: that many houses
 * 5: a hotel
 * @return the number of buildings on the property
 */
int BoardLocation::getBuildings()
{
	return (buildings);
}

/**
 * Gets the number of times the property has been visited
 * @return the counter of times a player has landed on property
 */
int BoardLocation::getVisits()
{
	return (visits);
}

/**
 * Is this property currently mortgaged (i.e. out of play)?
 * @return true if mortgaged, else false
 */
bool BoardLocation::isMortgaged()
{
	return (mortgaged);
}

/**
 * Set the mortgaged value of the property
 * @param val true if mortgaged, else false
 */
void BoardLocation::setMortgaged(bool val)
{
	mortgaged = val;
}

int BoardLocation::getUnmortgagePrice()
{
	return BoardLocation::price * 1.1; // pay price + 10%
}

// Instance methods
void BoardLocation::mortgage()
{
    mortgaged = true;
}

void BoardLocation::unmortgage()
{
    mortgaged = false;
}
/**
 * Increments the visit counter of the space
 *
 * When a player lands on a space, it needs to be incremented by one.
 * This is more convenient and accurate than a pure setter.
 */
void BoardLocation::incrementVisits()
{
	visits++;
}

/**
 * Changes the number of buildings on the property by a given quantity
 *
 * Increases or decreases the buildings by the count.  Doesn't do
 * any sanity checking.
 * @param delta the change in buildings
 */
void BoardLocation::changeBuildings(int delta) { buildings += delta; }
