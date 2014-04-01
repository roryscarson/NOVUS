#!python
# -*- encoding: utf-8 -*-

# Z_mrktInfo.py

# Greg Wilson & Austin Sherwindt, 2012
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
This module contains functions that return the information for the 
current year in the financial model.
'''

import X_utilities

def getPop(year):
    '''Returns the model's population for the year supplied in the 
    argument. [year - int]'''
    populations = [400000, 400000, 400000, 420000, 430500, 436958]
    return populations[year-1]
    
#--------------------------------------------------------------------------
def getPerCapConsumption(year):
    '''Returns the model's Per Capita Consumption for the year 
    supplied in the argument. [year - int]'''
    consumption = [80, 80, 82, 84, 84, 84]
    return consumption[year-1]
    
#--------------------------------------------------------------------------
def getPriceRange(year):
    '''Returns a list of tuples of the model's product's minimum 
    and maximum prices for the year supplied in the argument.
    [year - int]'''
    priceRanges = [
                   [(55.0, 80.0), (0.45, 0.70), (0.40, 0.60)],
                   [(55.0, 80.0), (0.45, 0.70), (0.40, 0.60)],
                   [(56.65, 82.40), (0.46, 0.72), (0.41, 0.62)],
                   [(58.35, 84.87), (0.48, 0.74), (0.42, 0.64)],
                   [(60.10, 87.42), (0.49, 0.76), (0.44, 0.66)],
                   [(61.90, 90.04), (0.51, 0.79), (0.45, 0.68)]
                   ]
    return priceRanges[year-1]

#--------------------------------------------------------------------------
def getMarketSegmentation(year):
    '''Returns a list of market shares for each of the model's 
    products (Ales, Lagers and Stouts) for the year supplied
    in the argument. [year - int]'''
    mrktSegs = [
                [0.90, 0.05, 0.05],
                [0.83, 0.10, 0.07],
                [0.67, 0.23, 0.10],
                [0.57, 0.34, 0.09],
                [0.49, 0.41, 0.10],
                [0.35, 0.52, 0.13]
                ]
    return mrktSegs[year-1]
    
#--------------------------------------------------------------------------
def GetMarketLiters(year):
    '''Returns the total Ale and Lager liters consumed in the market for
    the given year.'''
    mrkt = [(28800000, 1600000),
            (26560000, 3200000),
            (21976000, 7544000),
            (20109600, 11995200),
            (17719380, 14826420),
            (12846551, 19086304)]
    return mrkt[year-1]

#--------------------------------------------------------------------------
def getAvgLiterPrices(year):
    '''Returns a list of average liter prices - 
    [kegALP, bottleALP, canALP].'''
    prices = getPriceRange(year)
    kegVol = 64                 # Liters in a Keg
    bottleVol = 0.5             # Liters in a Bottle
    canVol = 1.0/3.0               # Liters in a can                 
    kegALP=(prices[0][0]/kegVol+prices[0][1]/kegVol)/2
    bottleALP=(prices[1][0]/bottleVol+prices[1][1]/bottleVol)/2
    canALP=(prices[2][0]/canVol+prices[2][1]/canVol)/2
    return [round(kegALP, 3), round(bottleALP, 3), round(canALP, 3)]
    
#--------------------------------------------------------------------------
def getAvgUnitPrices(year):
    '''Returns a list of average unit prices for the year -
    [kegAUP, bottle AUP, canAUP]'''
    prices = getPriceRange(year)
    kegAUP = (prices[0][0] + prices[0][1]) / 2
    bottleAUP = (prices[1][0] + prices[1][1]) / 2
    canAUP = (prices[2][0] + prices[2][1]) / 2
    return [kegAUP, bottleAUP, canAUP]

#--------------------------------------------------------------------------
def getCOGS(year, totalOutput):
    '''Returns a list of tuples - 
            [(Keg-Low, Keg-Med, Keg-High),
            (Bottle-Low, Bottle-Med, Bottle-High),
            (Can-Low, Cal-Med, Can-High)]
    of the COGS per product / quality based on the year and 
    total production output supplied.'''
    totalOutput = int(totalOutput)
    avgGM = 0.486535
    EoS = (totalOutput-1)/1000000 * 0.01
    if EoS > 0.06: EoS = 0.06

    kegMed = getAvgLiterPrices(year)[0]*(1-avgGM-0.05-EoS)
    bottleMed = getAvgLiterPrices(year)[1]*(1-avgGM-EoS)
    canMed = getAvgLiterPrices(year)[2]*(1-avgGM+0.02-EoS)
    return [(round(0.9*kegMed, 3), round(kegMed, 3), round(1.1*kegMed, 3)),
            (round(0.9*bottleMed, 3), round(bottleMed, 3), round(1.1*bottleMed, 3)),
            (round(0.9*canMed, 3), round(canMed, 3), round(1.1*canMed, 3))]
    
#--------------------------------------------------------------------------
def getHRCosts(year):
    '''Returns a list of total annual employee cost per person for each 
    position, which includes salary/wages and benefits/taxes, adjusted 
    for inflation.'''
    year1HRCosts = [80000,      # CEO
                    60000,      # CFO
                    50000,      # Manager
                    40000,      # Asst. Manager
                    60000,      # Head of Marketing
                    50000,      # Sales Reps
                    50000,      # Customer Service Specialist
                    25000,      # Quality Control Specialist
                    12000,      # Brewer
                    12000,      # Packager
                    24000,      # Driver
                    7500]       # Cleaner
    hrCosts = []
    for x in year1HRCosts:
        if year <=2:
            hrCosts.append(int(x*1.075))
        else:
            hrCosts.append(int((x*(1.03)**(year-2))*1.075))
    return hrCosts


#--------------------------------------------------------------------------
# BEST CASE INFO
#--------------------------------------------------------------------------
def BestOutput(year):
    '''Given a year, returns the Best Case Production Output for Ale and 
    Lager in total Liters as a list.'''
    bc = [[0, 0], [8, 2], [9, 7], [13, 15], [13, 23], [10, 36]]
    cycs = bc[year-1]
    return [cycs[0] * 100000, cycs[1] * 100000]
    
#--------------------------------------------------------------------------
def BestHR(fcastRev, totCycles):
    '''Returns the Best Case HR Decisions.'''
    # CFO ?
    cfoCt = 1 if fcastRev > 1500000 else 0
    # Head of Marketing ?
    headMktgCt = 1 if fcastRev > 1500000 else 0
    # Sales Representatives
    if fcastRev >= 3000000:
        salesRepCt = X_utilities.roundup(fcastRev / 3000000.0)
    else:
        salesRepCt = 0
    # Customer Service ?
    custServCt = 1 if fcastRev > 4500000 else 0
    # Drivers
    if totCycles > 0:
        driverCt = X_utilities.roundup((totCycles * 100000) / 1800000.0)
    else:
        driverCt = 0
    # Quality Control Specialist ?
    qualityCtrlCt = 1 if totCycles > 20 else 0
    # Brewers
    if totCycles > 20:
        brewerCt = X_utilities.roundup(totCycles / 20.0)
    else:
        brewerCt = 0
    # Packager ?
    packagerCt = 1 if totCycles > 1 else 0
    # Cleaners
    if totCycles / 30.0 > 1:
        cleanerCt = int(totCycles / 30.0)
    else:
        cleanerCt = 0
    
    workerCt = brewerCt + packagerCt + driverCt + cleanerCt
    # Managers 
    if workerCt > 0 and workerCt <= 5:
        managerCt = 1
    elif workerCt > 5:
        managerCt = 1 + int(workerCt / 5.0)
    else:
        managerCt = 0
    # Assistant Managers
    if workerCt > 10:
        asstManagerCt = X_utilities.roundup(workerCt / 10.0)
    else:
        asstManagerCt = 0
    
    return [1, cfoCt, managerCt, asstManagerCt, headMktgCt,
              salesRepCt, custServCt, qualityCtrlCt, brewerCt,
              packagerCt, driverCt, cleanerCt]
    
#--------------------------------------------------------------------------
def BestProduct(year):
    '''Returns the best posssible product decisions for the given year.'''
    y1 = [2, 2, 
          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
          47, 41, 12, 47, 45, 8]
    y2 = [2, 3, 
          55.51, 0.48, 0.42, 70.97, 0.63, 0.54,
          52, 41, 7, 53, 44, 3]
    y3 = [2, 3,
          59.0, 0.51, 0.45, 75.43, 0.66, 0.58,
          52, 33, 15, 54, 36, 10]
    y4 = [2, 3,
          61.69, 0.53, 0.46, 78.90, 0.69, 0.60,
          54, 29, 17, 58, 31, 11]
    y5 = [2, 3, 
          [[57.83, 0.46, 0.42, 71.43, 0.57, 0.51],
           [62.56, 0.52, 0.46, 77.27, 0.64, 0.57],
           [67.29, 0.58, 0.50, 83.12, 0.71, 0.62]],
          62, 17, 21, 68, 18, 14]
    y6 = [2, 3, 
          [[58.39, 0.47, 0.42, 73.57, 0.59, 0.53],
           [63.17, 0.52, 0.46, 79.59, 0.66, 0.58],
           [67.95, 0.58, 0.50, 85.61, 0.73, 0.64]],
          68, 7, 25, 76, 7, 17]
    bp = [y1, y2, y3, y4, y5, y6]
    return bp[year-1]

#--------------------------------------------------------------------------
def BestOther(year):
    '''Returns the best possible other spending decisions for the given 
    year.'''
    y1 = [0, 0, 0, 0]
    y2 = [1.25, 1.25, 1.25, 0.25]
    y3 = [1.25, 1.00, 1.25, 0.50]
    y4 = [1.25, 0.75, 1.25, 0.75]
    y5 = [1.00, 0.50, 1.00, 1.00]
    y6 = [1.00, 0.50, 0.75, 1.25]
    bo = [y1, y2, y3, y4, y5, y6]
    return bo[year-1]

#--------------------------------------------------------------------------
def GetBestRev(year):
    '''Returns the per product revenues for the best case scenario.'''
    y1 = [0, 0, 0, 0, 0, 0]
    y2 = [360796, 317842, 71051, 117526, 110114, 9778]
    y3 = [431385, 305604, 181877, 445502, 334832, 121128]
    y4 = [676631, 401759, 308079, 1072548, 643164, 296707]
    y5 = [787801, 230625, 375876, 2031095, 589802, 596399]
    y6 = [671173, 73074, 346094, 3659785, 369780, 1167535]
    bestRev = [y1, y2, y3, y4, y5, y6]
    return bestRev[year-1]
    
#--------------------------------------------------------------------------
def GetBestRatios(year):
    '''Gets the best case Key Financial Ratios (D/E, current, roa, 
    roe and Interest Coverage) from the best case scenario.'''
    best = [(0.690, 4.347, -0.225, 0.0, 0.0),
            (0.495, 2.357, -0.046, 0.073, 0.7),
            (0.204, 2.187, 1.127, 0.198, 13.9),
            (0.389, 2.081, 0.119, 0.224, 16.3),
            (0.204, 3.117, 0.236, 0.416, 49.8),
            (0.102, 3.918, 0.248, 0.396, 85.9)]
    return best[year-1]
    
#-------------------------------------------------------------------------
def GetBestAR(year):
    '''Returns the best case scenario AR as a share of total assets.'''
    ar = [0.0, 121497/1112686.0, 224053/1167204,
          418348/1746874.0, 567613/2287281.0, 773882/3116889.0]
    return ar[year-1]
    
#--------------------------------------------------------------------------
def GetBestInv(year):
    '''Returns the best case scenario inventory as a share of
    total assets.'''
    inv = [0.0, 25302/1112686.0, 44484/1167204.0, 79056/1746874.0,
           99084/2287281.0, 132927/3116889.0]
    return inv[year-1]

#--------------------------------------------------------------------------
# MODIFIER INFO
#--------------------------------------------------------------------------
def AllowOverProd(year):
    '''Given a year, returns the allowable over production as a percent
    over the best case scenario for that year.'''
    bc = [0.00, 0.06, 0.12, 0.18, 0.24, 0.30]
    return bc[year-1]
    
#--------------------------------------------------------------------------
def OutputMod(year):
    '''Returns the output modifier for the given year.'''
    mod = [0, -0.15, -0.18, -0.21, -0.25, -0.30]
    return mod[year-1]
    
#--------------------------------------------------------------------------
def ProductMod(year):
    '''Returns the product modifier for the given year.'''
    mod = [0, -0.25, -0.30, -0.35, -0.40, -0.45]
    return mod[year-1]
    
#--------------------------------------------------------------------------
def GenSalesMod(year):
    '''Returns the Gen. Sales modifier for the given year.'''
    mod = [0, -0.15, -0.18, -0.21, -0.25, -0.30]
    return mod[year-1]