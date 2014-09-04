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

#include<iostream>
#include<std::string>

class BoardLocation
{
	int id;
	std::string name;
	int price;
	int[] rents;
	int houseCost;
	std::string group;
	int buildings;
	int visits;
	bool mortgaged;

	public:
		BoardLocation(int ID, std::string* n, int p=0, std::string* g="none", int[] r=[0, 0, 0, 0, 0, 0], int hc=0)
		{
			id = ID;
			name = *n;
			price = p;
			rents = r;
			houseCost = hc;
			group = *g;
			buildings = 0;
			visits = 0;
			mortgaged = false;

		}
		
		// Getters and Setters
		int getID() { return id; }
		std::string* getName() { return &name; }
		int getPrice() { return price; }
		int* getRents() { return &rents; }
		int getHouseCost() { return houseCost; }
		std::string* getGroup() { return &group; }
		int getBuildings() { return buildings; }
		int getVisits() { return visits; }
		bool isMortgaged() { return mortgaged; }

		// Instance methods
		void flipMortgaged() { mortgaged = !mortgaged; }
		void incrementVisits() { visits++; }
		void changeBuildings(int delta) { buildings += delta; }
};
