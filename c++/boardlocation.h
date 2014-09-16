/*
 * =====================================================================================
 *
 *       Filename:  boardlocation.h
 *
 *    Description:  Header file for the boardlocation class
 *
 *        Version:  1.0
 *        Created:  Sep 4, 2014 2:53:15 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */
#pragma once
#ifndef BOARDLOCATION_H_
#define BOARDLOCATION_H_

#include<string>
#include<vector>

/**
 * A class meant to represent a location in a Monopoly gameboard.
 */
class BoardLocation
{
	int id;
	std::string name;
	int price = 0;
	std::vector<int> rents;
	int houseCost = 0;
	std::string group = "none";
	int buildings = 0;
	int visits = 0;
	bool mortgaged = false;

public:
	BoardLocation(int id, std::string name);
	BoardLocation(int id, std::string name, int price, std::string group);
	BoardLocation(int id, std::string name, int price, std::string group, std::vector<int> rents, int houseCost);

	// Getters and Setters
	int getID();
	std::string* getName();
	int getPrice();
	int getRents(int position);
	int getHouseCost();
	std::string* getGroup();
	int getBuildings();
	int getVisits();
	bool isMortgaged();
    void setMortgaged(bool val);

	// Instance methods
	void flipMortgaged();
	void incrementVisits();
	void changeBuildings(int);
};


#endif /* BOARDLOCATION_H_ */
