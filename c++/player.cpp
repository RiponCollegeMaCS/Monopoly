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

#include<iostream>

class Player
{
    int number;
    int buying_threshold = 100;
    int building_threshold = 5;
    int jail_time = 3;
    bool smart_jail_strategy = false;
    int complete_monopoly = 0;
    int[] group_preferences = new int[2];
    int development_threshold = 0;

    public:
        Player(int num, int buy_thresh, int build_thresh, int jt, bool sjs, int cm, int dt)
	{
		number = num;
		if (buy_thresh != NULL)
			building_threshold = buy_thresh;
		if (build_thresh != NULL)
			building_threshold = build_thresh;
		if (jt != NULL)
			jail_time = jt;
		if (sjs != NULL)
			smart_jail_strategy = sjs;
		if (cm != NULL)
			complete_monopoly = cm;
		if (dt != NULL)
			development_threshold = dt;
	}
        void reset_values()
	{

	}
};
