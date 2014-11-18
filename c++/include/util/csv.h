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

#include <iostream>
#include <string>
#include <vector>

class CSV
{
    const char SEPARATOR = ',';
    const char TERMINATOR = '\n';

    std::string filename;

public:
    CSV(std::string filename, int columns);
    ~CSV();

    writeLine()

};

#endif /* __MONOPOLY_CSV_H */