#!python
# -*- encoding: utf-8 -*-

# X_utilities.py

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
This module contains all the utility functions used by the Novus Program.
'''

import os, sys
import string
import Q_data
import Y_makeTeamData1

def ImageFP(fileName):
    'Returns a filepath to the named file located in the "resources" directory.'
    if hasattr(sys, 'frozen'):
        path = os.path.join('resources', 'images', fileName)
    else:
        path = os.path.join('novus_pkg', 'resources', 'images', fileName)
    return path

#--------------------------------------------------------------------------
def ResourceFP(fileName):
    '''Returns the path of a file in the resources directory.'''
    if hasattr(sys, 'frozen'):
        path = os.path.join('resources', fileName)
    else:
        path = os.path.join('novus_pkg', 'resources', fileName)
    return path

#--------------------------------------------------------------------------
def yearDirFP(year=1):
    '''Returns a file path to the specified year's directory
    in the "resources" directory.'''
    data = Q_data.Data(None)
    langSwitch = data.GetData1()[1][1]
    
    yearSwitches = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5',
                        'Year 6']
    
    yearSwitch = yearSwitches[year-1]
    if hasattr(sys, 'frozen'):
        path = os.path.join('resources', langSwitch, yearSwitch)
    else:
        path = os.path.join('novus_pkg', 'resources', langSwitch, yearSwitch)
    return path

#--------------------------------------------------------------------------
def teamDataCheck():
    '''Checks that the teamData1.csv file exists in the My Documents 
    directory. If not, it creates the file.'''
    # Check that the file exists
    md = os.path.expanduser('~/')
    path = os.path.join(md, 'My Documents', 'Novus Data', 'teamData1.csv')
    if not os.path.isfile(path):
        Y_makeTeamData1.MakeTeamData1()
    
#--------------------------------------------------------------------------
def teamDataCheck2():
    '''Checks that the teamData1.csv file is complete.'''
    data = Q_data.Data(None)
    try:
        data.GetData1()
    except IndexError, e:
        Y_makeTeamData1.MakeTeamData1()
        
#--------------------------------------------------------------------------
def roundto(x, b):
    '''(int x, int b)
    Rounds x to the nearest b.'''
    z = x/b
    low = b * z
    high = b * (z+1)
    if high-x < x-low:
        return high
    else:
        return low

#--------------------------------------------------------------------------
def roundup(x):
    '''Rounds 'x', a float, up to the nearest integer.'''
    base = int(x)
    if x == base:
        return base
    else:
        return base + 1
    
#--------------------------------------------------------------------------

def ValidateLastFloat(input):
    '''Confirms that the last char of a unicode input can be converted 
    into a float.'''
    if len(input) == 0: return ''
    inputList = list(input)
    valid = string.digits + '.'
    if inputList[-1] not in valid and inputList[-1]!='.':
        del inputList[-1]
    
    return ''.join(inputList)
    
#--------------------------------------------------------------------------
def ValidateConvertFloat(input):
    '''Confirms that a unicode input can be converted into a floating 
    point number.'''
    if len(input) == 0: return True
    try:
        float(input)
        return True
    except ValueError:
        return False
    
#--------------------------------------------------------------------------
def ButtonTextWrapper(text):
    '''Takes a set of text to be written in 12, wx.SWISS, wx.BOLD
    and wraps the text accordingly.'''
    # Break the text apart
    word_list = text.split(' ')
    output = ''
    chars = 0
    for x in word_list:
        chars += len(x) + len(word_list[:word_list.index(x)+1])
        if chars >= 20:
            output += ' '.join(word_list[:word_list.index(x)])+'\n'
            word_list = word_list[word_list.index(x):]
            chars = 0
        if len(x) >= 20:
            output += ''.join(list(x)[:20]) + '\n'
            wordList = word_list[word_list.index(x)+1:]
            chars = 0
        if len(' '.join(word_list)) <= 20:
            output += ' '.join(word_list) + '\n'
            return output
    return output
    
        
            
        
                                  
    

        
        
        