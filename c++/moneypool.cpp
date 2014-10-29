/*
 * =====================================================================================
 *
 *       Filename:  moneypool.cpp
 *
 *    Description:  Represent money in a game of Monopoly
 *
 *        Version:  1.0
 *        Created:  10/28/2014 7:49:16 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */

#include "moneypool.h"

class MoneyPool
{
	int money = 0;

public:
	int getMoney() { return money; }
	void setMoney(int newMoney) { money += newMoney; }
	void addMoney(int add) { money += add; }

	char getType() { return 'm'; }
};
