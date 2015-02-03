/*
 * =====================================================================================
 *
 *       Filename:  csv.h
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

#ifndef __MONOPOLY_CSV_H
#define __MONOPOLY_CSV_H

#include <string>
#include <fstream>

class CSV
{
    const char SEPARATOR = ',';
    const char TERMINATOR = '\n';

    std::ofstream outfile;

public:
    CSV(std::string filename);
    ~CSV();

    void writeline(int* player, float result);

};

#endif /* __MONOPOLY_CSV_H */