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
#include "../game/player.h"


const int NUMBER_OF_GAMES = 1000;
const int NUMBER_OF_TURNS = 1000;


Player* generateRandomPlayer(int number);
int sumArray(int results[], int numberResults);
int playSet(const int* basePlayer, int numberOfGames);
float successIndicator(const int* basePlayer, int numberOfGames, int procs, Player* staticOpponent);
void shortBruteForce(int numberOfGames);

#endif
