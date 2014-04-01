#!python
# -*- encoding: utf-8 -*-

# X_export.py

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
This class contains tools to get the current results from years played
in the game, and export them as an Excel spreadsheet
'''

from pyExcelerator import *
import datetime
import os
import string

def Export(incStmt, balSheet, cfStmt, fr, bsc=None, year=1):
    '''Export(list - Income Statement, list - Balance Sheet,
                list - Statement of Cash Flows, list - Financial Ratios,
                list - Balanced Score Card)
    
    Takes lists of all of the financial reports and exports them to a
    workbook with a dateTime stamp filename.'''
    wb = Workbook()
    UnicodeUtils.DEFAULT_ENCODING = 'utf8'
    
    # Formats -------------------------------------------------------------
    fmt = "$#,##0_);[Red]($#,##0)"
    style1 = XFStyle()
    style1.num_format_str = fmt
    
    # Create the Income Statement Sheet -----------------------------------
    # Get IS name 
    is_lbl = incStmt[0][0]
    try:
        is_tabName = string.upper(is_lbl[:3])
    except IndexError:
        is_tabName = is_lbl
        
    isSheet = wb.add_sheet(is_tabName)
    isSheet.write(0, 0, is_lbl)
    
    row = 2
    incStmt.insert(43, [])
    for x in incStmt:
        col = 0
        for y in x:
            if row == 2 and col == 0:
                pass
            else:
                isSheet.write(row, col, y)
            col += 1
        row += 1
        
    # Set Column Width
    isSheet.col(0).width=0x0d00*3
    for i in range(1, 7):
        isSheet.col(i).width=0x0d00*1.25
    
    # Create the Balance Sheet --------------------------------------------
    bs_lbl = balSheet[0][0]
    try:
        bs_tabName = string.upper(bs_lbl[:3])
    except IndexError:
        bs_tabName = bs_lbl
        
    bsSheet = wb.add_sheet(bs_tabName)
    bsSheet.write(0, 0, bs_lbl)
    
    row = 2
    for x in balSheet:
        col = 0
        for y in x:
            if row == 2 and col == 0:
                pass
            else:
                bsSheet.write(row, col, y)
            col += 1
        row += 1
    bsSheet.col(0).width=0x0d00*3
    
    # Set Column Width
    bsSheet.col(0).width=0x0d00*3
    for i in range(1, 7):
        bsSheet.col(i).width=0x0d00*1.25
        
    # Create the Statement of Cash Flows ----------------------------------
    cf_lbl = cfStmt[0][0]
    try:
        cf_tabName = string.upper(cf_lbl[:3])
    except IndexError:
        cf_tabName = cf_lbl
    
    cfSheet = wb.add_sheet(cf_tabName)
    cfSheet.write(0, 0, cf_lbl)
    row = 2
    for x in cfStmt:
        col = 0
        for y in x:
            if row == 2 and col == 0:
                pass
            else:
                cfSheet.write(row, col, y)
            col += 1
        row += 1
    cfSheet.col(0).width=0x0d00*3
    
    # Set Column Width
    cfSheet.col(0).width=0x0d00*3
    for i in range(1, 7):
        cfSheet.col(i).width=0x0d00*1.25
    
    # Create the Financial Ratio sheet ------------------------------------
    fr_lbl = fr[0][0]
    try:
        fr_tabName = string.upper(fr_lbl[:3])
    except IndexError:
        fr_tabName = fr_lbl
    
    frSheet = wb.add_sheet(fr_tabName)
    frSheet.write(0, 0, fr_lbl)
    row = 2
    for x in fr:
        col = 0
        for y in x:
            if row == 2 and col == 0:
                pass
            else:
                frSheet.write(row, col, y)
            col += 1
        row += 1
    frSheet.col(0).width=0x0d00*3
    
    # Set Column Width
    frSheet.col(0).width=0x0d00*3
    for i in range(1, 7):
        frSheet.col(i).width=0x0d00*1.25
        
    # Create the Balanced Score Card --------------------------------------
    if bsc:
        bsc_lbl = bsc[0][0]
        try:
            bsc_tabName = string.upper(bsc_lbl[:3])
        except IndexError:
            bsc_tabName = bsc_lbl
        
        bscSheet = wb.add_sheet('BSC')
        bscSheet.write(0, 0, 'Balanced Score Card')
        row = 2
        for x in bsc:
            col = 0
            for y in x:
                if row == 2 and col == 0:
                    pass
                else:
                    bscSheet.write(row, col, y)
                col += 1
            row += 1
        bscSheet.col(0).width=0x0d00*3
        
        # Set Column Width
        bscSheet.col(0).width=0x0d00*3
        for i in range(1, 7):
            bscSheet.col(i).width=0x0d00*1.25
        
    # Save the workbook ---------------------------------------------------
    if bsc:    
        path = GetFileName1()
    else:
        path = GetFileName2(year)
        
    wb.save(path)

#--------------------------------------------------------------------------
def GetFileName1():
    '''Returns the appropriate file path and name to the
    "NOVUS Data" directory.'''
    p = os.path.abspath(os.path.expanduser('~/'))
    
    # Generate time stamped filename
    dt = datetime.datetime
    fName = dt.isoformat(dt.now())
    a = fName.split('T')[0]
    fName = 'NOVUS ' + a + '.xls'
    
    p = os.path.join(p, 'My Documents', 'Novus Data', fName)
    return p

#--------------------------------------------------------------------------
def GetFileName2(year):
    '''Returns the name of the file that corresponds to the year supplied
    in the argument. This is used for creating the file names for exporting
    forecast vs actual results.'''
    p = os.path.abspath(os.path.expanduser('~/My Documents'))
    
    # Check to see if the "Forecast" directory exists
    fcastDir_path = os.path.join(p, 'Novus Data', 'Forecasts')
    
    # Make sure the directory exists
    if not os.path.isdir(fcastDir_path):
        os.mkdir(fcastDir_path)
        
    # If Year 1, remove all old forecast files
    if year == 1:
        files = os.listdir(fcastDir_path)
        for x in files:
            os.remove(os.path.join(fcastDir_path, x))
        
    return os.path.join(fcastDir_path, 'Round_'+str(year)+'.xls')
    
#--------------------------------------------------------------------------
def MakeArray(rowSt, rowEnd):
    '''Takes a starting and ending row number. Returns a list of columnar
    arrays for columns B through F between the provided rows.'''
    col = ['B', 'C', 'D', 'E', 'F', 'G']
    out = []
    for x in col:
        out.append(x+str(rowSt)+':'+x+str(rowEnd))
    return out
    
