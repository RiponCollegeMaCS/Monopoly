//
//  success.h
//  Monopoly
//
//  Created by Braxton Schafer on 9/21/14.
//  Copyright (c) 2014 Braxton Schafer. All rights reserved.
//

#ifndef Monopoly_success_h
#define Monopoly_success_h

#include <unordered_map>
#include <string>
#include "player.h"


const int NUMBER_OF_GAMES = 100;
const int NUMBER_OF_TURNS = 1000;


Player* generateRandomPlayer(int number);
int sumArray(int results[], int numberResults);
void playSet(Player* basePlayer, int numberOfGames, Player* staticOpponent, int results[]);
float successIndicator(Player* basePlayer, int numberOfGames, int procs, Player* staticOpponent);
void shortBruteForce(int numberOfGames);

#endif
