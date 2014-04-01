#!python
# -*- encoding: utf-8 -*-

# Y_makeTeamData1.py

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
This module's 'MakeTeamdata1 method creates the team's starting data1 sheet.
The data1 sheet holds information for all of the team's actual decisions,
as well as the selected language and current round.
'''

import csv
import os, sys
import X_utilities

def MakeTeamData1():
    '''Creates the starting .csv file that will keep track of all
    the team's decisions throughout the game. The sheet includes 
    values for all of the decision points that are pre-decided for 
    the teams.'''
    
    # Try to create the teamData1.csv file in the My Documents dir
    md = os.path.expanduser('~/My Documents')
    try:
        os.mkdir(os.path.join(md, 'Novus Data'))
    except WindowsError, e:
        pass
    path = os.path.join(md, 'Novus Data', 'teamData1.csv')
        
    makeFile = True
    if __name__ == '__main__' and os.path.isfile(path):
        accept = ('Y', 'y')
        print "'teamData1.csv' already exists!"
        print "Do you want to replace the existing file? (y / n)"
        input = raw_input("> ")
        if input in accept:
            makeFile = True
        else:
            makeFile = False
            
    if makeFile:
        file = open(path, 'wb')
        writer = csv.writer(file, dialect='excel')
        
        table = [
                 ('Year', 1),                                                   
                 ('Language', 'English'),                                                                  
                 # Manufacturing Machinery
                 ('Machine 1 Purchased, Type', 0, 0, 0),                       
                 ('Machine 2 Purchased, Type', 0, 0, 0),                       
                 ('Machine 3 Purchased, Type', 0, 0, 0),                      
                 ('Machine 4 Purchased, Type', 0, 0, 0),                       
                 ('Machine 5 Purchased, Type', 0, 0, 0),                       
                 # Packaging Machinery
                 ('Kegging Machine', 0, 0),                                        
                 ('Bottling Machine', 0, 0),                                       
                 ('Canning Machine', 0, 0),                                        
                 # Finished Goods Storage Space
                 ('Finished Goods Storage', 0, 0),                               
                 # Year 1 Debt and Euity
                 ('Year 1 Debt, Rate, Payback', 0, 0, 0),                       
                 ('Year 1 Equity, Shares', 0, 0),                               
                 # Year 4 Debt
                 ('Year 4 Debt, Rate, Payback', 0, 0, 0),                       
                 # Short Term Borrowing
                 ('Short Term Borrowing Draw', 0, 0, 0, 0, 0, 0),               
                 ('Short Term Borrowing Rate', 0, 0, 0, 0, 0, 0),               
                 # Production
                 ('Machine 1 Cycles Run', 0, 0, 0, 0, 0, 0),                    
                 ('Machine 2 Cycles Run', 0, 0, 0, 0, 0, 0),                    
                 ('Machine 3 Cycles Run', 0, 0, 0, 0, 0, 0),                    
                 ('Machine 4 Cycles Run', 0, 0, 0, 0, 0, 0),                    
                 ('Machine 5 Cycles Run', 0, 0, 0, 0, 0, 0),                    
                 # Human Resources
                 ('CEOs', 1, 1, 1, 1, 1, 1),                                    
                 ('CFO/Accountants', 0, 0, 0, 0, 0, 0),                         
                 ('Managers', 0, 0, 0, 0, 0, 0),                                
                 ('Asst. Managers', 0, 0, 0, 0, 0, 0),                          
                 ('Head of Marketings', 0, 0, 0, 0, 0, 0),                      
                 ('Sales Reps', 0, 0, 0, 0, 0, 0),                              
                 ('Customer Service Specs.', 0, 0, 0, 0, 0, 0),                 
                 ('Quality Ctrl. Specs.', 0, 0, 0, 0, 0, 0),                    
                 ('Brewers', 0, 0, 0, 0, 0, 0),  
                 ('Packagers', 0, 0, 0, 0, 0, 0),                               
                 ('Drivers', 0, 0, 0, 0, 0, 0),                                 
                 ('Cleaners', 0, 0, 0, 0, 0, 0),                                
                 # Pricing
                 ('Ale - Keg ASP', 0.00, 55.51, 59.00, 0.00, 0.00, 0.00),       
                 ('Ale - Bottle ASP', 0.00, 0.48, 0.51, 0.00, 0.00, 0.00),      
                 ('Ale - Can ASP', 0.00, 0.42, 0.45, 0.00, 0.00, 0.00),         
                 ('Lager - Keg ASP', 0.00, 70.97, 75.43, 0.00, 0.00, 0.00),     
                 ('Lager - Bottle ASP', 0.00, 0.63, 0.66, 0.00, 0.00, 0.00),    
                 ('Lager - Can ASP', 0.00, 0.54, 0.58, 0.00, 0.00, 0.00),       
                 # Segment Production
                 ('Ale - Keg Prod.', 0, 0, 0, 0, 0, 0),       
                 ('Ale - Bottle Prod.', 0, 0, 0, 0, 0, 0),    
                 ('Ale - Can Prod.', 0, 0, 0, 0, 0, 0),       
                 ('Lager - Keg Prod.', 0, 0, 0, 0, 0, 0),       
                 ('Lager - Bottle Prod.', 0, 0, 0, 0, 0, 0),  
                 ('Lager - Can Prod.', 0, 0, 0, 0, 0, 0),     
                 # Quality of Ingredients
                 ('Ale Quality', 2, 2, 2, 2, 2, 2),                           
                 ('Lager Quality', 2, 3, 3, 2, 2, 2),                           
                 # Other Spending
                 ('Marketing', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),             
                 ('Product Development', 0.25, 0.00, 0.00, 0.00, 0.00, 0.00),   
                 ('Promotional Activity', 0.50, 0.00, 0.00, 0.00, 0.00, 0.00),   
                 ('Community Development', 0.50, 0.00, 0.00, 0.00, 0.00, 0.00),
                 # Part II: Historical Records
                 ('Revenue - AK', 0, 0, 0, 0, 0, 0),
                 ('Revenue - AB', 0, 0, 0, 0, 0, 0),
                 ('Revenue - AC', 0, 0, 0, 0, 0, 0),
                 ('Revenue - LK', 0, 0, 0, 0, 0, 0),
                 ('Revenue - LB', 0, 0, 0, 0, 0, 0),
                 ('Revenue - LC', 0, 0, 0, 0, 0, 0),
                 ('Cash', 0, 0, 0, 0, 0, 0),
                 ('Short Term Investments', 0, 0, 0, 0, 0, 0),
                 ('Accounts Receivable', 0, 0, 0, 0, 0, 0),
                 ('Inventory', 0, 0, 0, 0, 0, 0),
                 ('Gross PPE', 0, 0, 0, 0, 0, 0),
                 ('Accumulated Depreciation', 0, 0, 0, 0, 0, 0),
                 ('Accounts Payable', 0, 0, 0, 0, 0, 0),
                 ('Short Term Borrowing', 0, 0, 0, 0, 0, 0),
                 ('Line of Credit', 0, 0, 0, 0, 0, 0),
                 ('Current Portion of LTD', 0, 0, 0, 0, 0, 0),
                 ('Long Term Debt', 0, 0, 0, 0, 0, 0),
                 ('Retained Earnings', 0, 0, 0, 0, 0, 0),
                 ('Ending Cash Balance', 0, 0, 0, 0, 0, 0),
                 ('Managerial Effectiveness Score',  0, 0, 0, 0, 0, 0) 
                 ]
        for line in table:
            writer.writerow(line)
        
        file.close()
                 
if __name__ == '__main__':
    MakeTeamData1()
                 
            
            
    
    