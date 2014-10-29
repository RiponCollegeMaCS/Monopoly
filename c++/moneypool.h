/*
 * moneypool.h
 *
 *  Created on: Oct 28, 2014
 *      Author: braxton
 */

#ifndef MONEYPOOL_H_
#define MONEYPOOL_H_

class MoneyPool
{
	int money = 0;

public:
	int getMoney();
	void setMoney(int newMoney);
	void addMoney(int add);

	char getType();
};



#endif /* MONEYPOOL_H_ */
