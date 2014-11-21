/*
 * =====================================================================================
 *
 *       Filename:  csv.cpp
 *
 *    Description:  Writes out to CSV files
 *
 *        Version:  1.0
 *        Created:  Nov 15, 2014 7:40:44 PM
 *       Revision:  none
 *       Compiler:  clang
 *
 *         Author:  Braxton Schafer (bjs), braxton.schafer@gmail.com
 *   Organization:  Ripon College
 *
 * =====================================================================================
 */

#include <fstream>
#include <string>
#include "util/csv.h"

CSV::CSV(std::string filename)
{
    CSV::outfile.open(filename, std::ios::out | std::ios::app | std::ios::binary);
}

CSV::~CSV()
{
    CSV::outfile.close();
}

void CSV::writeline(int* player, float result)
{
    CSV::outfile << result << CSV::SEPARATOR;

    for (int i = 0; i < 6; i++)
    {
        if (i < 5)
            CSV::outfile << player[i] << CSV::SEPARATOR;
        else
            CSV::outfile << player[i];
    }

    CSV::outfile << CSV::TERMINATOR;

    CSV::outfile.flush();
    delete [] player;
}
