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

#include "boardlocation.h"

#include<vector>

BoardLocation::BoardLocation(int id, std::string name)
{
	BoardLocation::id = id;
	BoardLocation::name = name;
}

BoardLocation::BoardLocation(int id, std::string name, int price, std::string group)
{
	BoardLocation::id = id;
	BoardLocation::name = name;
	BoardLocation::price = price;
	BoardLocation::group = group;
}

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
int BoardLocation::getID() { return (id); }
std::string* BoardLocation::getName() { return (&name); }
int BoardLocation::getPrice() { return (price); }
int BoardLocation::getRents(int position) { return (rents[position]); }
int BoardLocation::getHouseCost() { return (houseCost); }
std::string* BoardLocation::getGroup() { return (&group); }
int BoardLocation::getBuildings() { return (buildings); }
int BoardLocation::getVisits() { return (visits); }
bool BoardLocation::isMortgaged() { return (mortgaged); }
void BoardLocation::setMortgaged(bool val) { mortgaged = val; }

// Instance methods
void BoardLocation::flipMortgaged() { mortgaged = !mortgaged; }
void BoardLocation::incrementVisits() { visits++; }
void BoardLocation::changeBuildings(int delta) { buildings += delta; }
