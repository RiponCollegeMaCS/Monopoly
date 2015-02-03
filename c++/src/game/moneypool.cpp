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

#include "game/moneypool.h"

MoneyPool::MoneyPool()
{
    MoneyPool::money = 0;
}

MoneyPool::MoneyPool(int start)
{
    MoneyPool::money = start;
}

int MoneyPool::getMoney() { return money; }
void MoneyPool::setMoney(int newMoney) { money += newMoney; }
void MoneyPool::addMoney(int add) { money += add; }
char MoneyPool::getType() { return 'm'; }
