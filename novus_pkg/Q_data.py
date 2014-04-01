#!python
# -*- encoding: utf-8 -*-

# Q_data.py

# Greg Wilson, 2012
# gwilson.sq1@gmail.com
# This software is part of the Public Domain.

#    This file is part of the NOVUS Entrepreneurship Training Program.

#    NOVUS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    NOVUS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with NOVUS.  If not, see <http://www.gnu.org/licenses/>.

'''
This module contains the data class. This class uses the
'teamData1.py' to keep track of the team's decisions and
basic program configuration specifications.
'''

import csv
import os
import wx
import X_utilities
import Y_makeTeamData1
from Q_language import GetPhrase

class Data(wx.Object):
    '''This class is used to manage the team's decisions
    for the game, as well as basic configuration specifications.'''
    def __init__(self, parent, *args, **kwargs):
        
        X_utilities.teamDataCheck()
        md = os.path.expanduser('~/')
        self.data1FP = os.path.join(md, 'My Documents', 'Novus Data', 'teamData1.csv')
    
    #----------------------------------------------------------------------
    def GetData1(self):
        '''Reads the team data 1 file and returns a formatted 
        table.'''
        X_utilities.teamDataCheck()
        file = open(self.data1FP, 'rb')
        reader = csv.reader(file, dialect='excel')
        table = []
        for row in reader:
            table.append(row)
        file.close()
        
        # Format Output
        table[0][1] = int(table[0][1])
        # Man. / Pack. Equipment and FG Storage Years 1-3
        table[2][1] = int(table[2][1])
        table[3][1] = int(table[3][1])
        table[4][1] = int(table[4][1])
        table[5][1] = int(table[5][1])
        table[6][1] = int(table[6][1])
        
        table[7][1] = int(table[7][1])
        table[8][1] = int(table[8][1])
        table[9][1] = int(table[9][1])
        
        table[10][1] = int(table[10][1])
        # Man. / Pack. Equipment and FG Storage Years 4 - 6
        table[2][2] = int(table[2][2])
        table[3][2] = int(table[3][2])
        table[4][2] = int(table[4][2])
        table[5][2] = int(table[5][2])
        table[6][2] = int(table[6][2])
        
        table[7][2] = int(table[7][2])
        table[8][2] = int(table[8][2])
        table[9][2] = int(table[9][2])
        
        table[10][1] = int(table[10][1])
        table[10][2] = int(table[10][2])
        
        table[2][3] = int(table[2][3])
        table[3][3] = int(table[3][3])
        table[4][3] = int(table[4][3])
        table[5][3] = int(table[5][3])
        table[6][3] = int(table[6][3])
        
        # Long Term Debt Amt, Rate, Payback Period - Year 1
        table[11][1] = int(table[11][1])
        table[11][2] = float(table[11][2])
        table[11][3] = int(table[11][3])
        # Equity Amount and Shares
        table[12][1] = int(table[12][1])
        table[12][2] = int(table[12][2])
        # Long Term Debt Amt, Rate, Payback Period - Year 1
        table[13][1] = int(table[13][1])
        table[13][2] = float(table[13][2])
        table[13][3] = int(table[13][3])
        
        # Six Years - All Integers
        intRows = (14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                   27, 28, 29, 30, 31, 32, 39, 40, 41, 42, 43, 44, 45, 46)
        
        for row in intRows:
            for i in range(1, 7):
                table[row][i] = int(table[row][i])
    
        # Six Years - All Float
        floatRows = (15, 33, 34, 35, 36, 37, 38, 47, 48, 49, 50)
        
        for row in floatRows:
            for i in range(1, 7):
                table[row][i] = round(float(table[row][i]), 3)
                
        # All Historical Performace Info Formatted as Integers
        for row in range(51, 71):
            for col in range(1, 7):
                table[row][col] = int(table[row][col])
        
        return table
    
    #----------------------------------------------------------------------
    def CombineData1(self, decList, year):
        '''This function gets the team's historical decision list stored 
        in the "teamData1.csv" file, and combines it with the team's 
        current decisions for the round.'''
        combTable = self.GetData1()
        # Add Manufacturing / Packaging Equipment / FG Storage Decisions
        if year == 1:
            for row in range(2, 11):
                combTable[row][1] = decList[row][1]
                if decList[row][1] and row < 7:
                    combTable[row][3] = decList[row][3]
        if year == 4:
            for row in range(2, 11):
                combTable[row][2] = decList[row][2]
                if decList[row][2] and row < 7:
                    combTable[row][3] = decList[row][3]
                
        # Add Year 1 Debt, Year 1 Equity, and Year 4 Debt
        if year == 1:
            combTable[11][1] = decList[11][1]
            combTable[11][2] = decList[11][2]
            combTable[11][3] = decList[11][3]
            combTable[12][1] = decList[12][1]
            combTable[12][2] = decList[12][2]
        if year == 4:
            combTable[13][1] = decList[13][1]
            combTable[13][2] = decList[13][2]
            combTable[13][3] = decList[13][3]
        
        # Add the rest of the current decisions in the correct year colummns
        for row in range(14, 51):
            combTable[row][year] = decList[row][year]
        
        return combTable
    
    #----------------------------------------------------------------------
    def WriteData1(self, decInfo):
        '''Writes the combined decision table to the "teamData1.csv"
        file.'''
        
        file = open(self.data1FP, 'wb')
        writer = csv.writer(file, dialect='excel')
        for row in decInfo:
            writer.writerow(row)
        file.close()
        
    #----------------------------------------------------------------------
    def ChangeLanguage(self, lang):
        '''Changes the program's languages to the specified string. This
        will correlate with one of the langauge directories in the 
        resources directory.'''
        table = self.GetData1()
        table[1][1] = lang
        
        self.WriteData1(table)
    