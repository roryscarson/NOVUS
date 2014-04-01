#!python
# -*- encoding: utf-8 -*-

# Z_gameIO.py

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
This module contains functions that process the decision information into
financial results. 
'''

import math
import wx
import X_utilities
import Z_mrktInfo
import Q_data

daysOfFG = 17.105
kegVol = 64
bottleVol = 1.0/2.0
canVol = 1.0/3.0

def GetFinanceOutput(decInfo, year, ale_lbl, lager_lbl, mod=False):
    '''Calculates the Per Product and Total Revenues, and COGS.'''
    #----------------------------------------------------------------------
    #   PART I - INCOME STATEMENT 1
    #----------------------------------------------------------------------
    # GET BASIC PRODUCTION INFORMATION ------------------------------------
    #   Part 1.1 - Find the type of each purchased machine (1=Ale, 2=Lager, 0=None)
    mTypes = GetManMachTypes(decInfo, ale_lbl, lager_lbl)
    
    #   Part 1.2 - Find the number of Cycles run on each machine
    mCycles = GetManMachCycles(decInfo, year)
    
    #   Part 1.3 - Find the total Ale / Lager Production
    aleVol, lagerVol = GetProdVol(mTypes, mCycles)
    
    soldAle, soldLager = aleVol, lagerVol
    plannedAle, plannedLager = aleVol, lagerVol
    
    aleCycs = aleVol / 100000
    lagerCycs = lagerVol / 100000
    
    #   Part 1.4 - Get Packaging Settings and Unit Output
    soldVol = GetProdLiters(decInfo, year, aleVol, lagerVol)
    prodUnits = GetProdUnits(decInfo, year, aleVol, lagerVol)
    
    # GET REVENUE, COGS, INV SPOIL / OVERPROD EXP / ADJ COGS --------------
    #   Part 1.5 - Get the Per-Product Revenue and Total Revenue
    prodRev = GetProdRev(decInfo, year, prodUnits)
    totalRev = 0
    for x in prodRev:
        totalRev += x
    fcastTotRev = totalRev
    
    #======================================================================
    # IF mod: APPLY SCORES AND MODS TO OUTPUT / SALES
    if mod:
        # OUTPUT
        prodAleVol1, prodLagerVol1 = GetAllowedProd(year, aleVol, lagerVol)
        outputScore = OutputScore(decInfo, year, fcastTotRev, aleCycs+lagerCycs)
        prodAleVol2, prodLagerVol2 = OutputAdjust(decInfo, year, outputScore, prodAleVol1, prodLagerVol1)
        realProdVol = GetProdLiters(decInfo, year, prodAleVol2, prodLagerVol2)
        
        aleVol, lagerVol = prodAleVol2, prodLagerVol2
        
        # SALES
        # 1) Get Starting Sales Volume
        soldAleVol1, soldLagerVol1 = GetStartSalesVol(year, prodAleVol2, prodLagerVol2)
        soldProdVol1 = GetProdLiters(decInfo, year, soldAleVol1, soldLagerVol1)
        prodScore = ProductScores(decInfo, year) 
        salesAdj1 =  SalesAdjust1(year, soldProdVol1, prodScore)
        genSalesScore =  GenSalesScore(decInfo, year, fcastTotRev, aleCycs+lagerCycs)
        salesAdj2 = SalesAdjust2(year, soldProdVol1, genSalesScore)
        soldVol = GetSalesVol(decInfo, year, soldProdVol1, salesAdj1, salesAdj2)[0]
        soldUnits = GetSalesVol(decInfo, year, soldProdVol1, salesAdj1, salesAdj2)[1]
        soldAle = soldVol[0] + soldVol[1] + soldVol[2]
        soldLager = soldVol[3] + soldVol[4] + soldVol[5]
        prodRev = GetProdRev(decInfo, year, soldUnits)
        totalRev = 0
        for x in prodRev:
            totalRev += x
        
#        print
#        print 50 * '+'
#        print 'SCORING CHECK'
#        print 50 * '+'
#        print
#        print 'Allowed Ale Prod. 1     >', prodAleVol1
#        print 'Allowed Lager Prod. 1   >', prodLagerVol1
#        print 'Output Score            >', outputScore
#        print 'Allowed Ale Prod. 2     >', prodAleVol2
#        print 'Allowed Lager Prod. 2   >', prodLagerVol2
#        print 25 * '-'
#        print 'Start Sales Vol - Ale   >', soldAleVol1
#        print 'Start Sales Vol - Lager >', soldLagerVol1
#        print 'Start Sales (L)         >', soldProdVol1
#        print 25 * '-'
#        print 'Product Score           >', prodScore
#        print 'Sales Vol. Adj. 1       >', salesAdj1
#        print 'General Sales Score     >', genSalesScore
#        print 'Sales Vol. Adj. 2       >', salesAdj2
#        print 25 * '-'
#        print 'Ale Sales (L)           >', soldAle
#        print 'Lager Sales (L)         >', soldLager
#        print 'Final Sales - Liters    >', soldVol
#        print 'Final Sales - Units     >', soldUnits
#        print 'Total Revenue           >', totalRev
        
    #======================================================================

    #   Part 1.6 - Get the per product and total COGS
     
    prodCOGS = GetCOGS(decInfo, year, aleVol+lagerVol, soldVol)

    totalCOGS = 0
    for x in prodCOGS:
        totalCOGS += x
    
    #   Part 1.7 - Set the OverProduction Expense to 0 and Find Inventory
    overProdExp = 0
    
    #======================================================================
    # IF mod: GET ACTUAL OVERPRODUCTION COST
    if mod:
        overProdExp = GetOverProdCost(decInfo, year, realProdVol, soldVol)
    #======================================================================
    
    invSpoil = GetInvSpoil(decInfo, year, totalCOGS, overProdExp)
    
    #   Part 1.8 - Get the invSpoil + OverProdExp per Product and
    #    add it to COGS to get the ajdusted COGS
    prodShares = GetProdShares(decInfo, year, aleVol, lagerVol)
    adjProdCOGS = []
    totalAdjCOGS = 0
    for share, cogs in zip(prodShares, prodCOGS):
        adjProdCOGS.append(cogs + int((overProdExp + invSpoil) * share))
        totalAdjCOGS += cogs + int((overProdExp + invSpoil) * share)
    
    # GOSS INCOME / MARGIN ------------------------------------------------
    
    #   Part 1.9 - Get the Gross Income / Margin
    prodGrossIncome = GetGrossIncome(prodRev, adjProdCOGS)
    totalGI = 0
    for x in prodGrossIncome:
        totalGI += x
    
    prodGrossMargin = GetGrossMargin(prodGrossIncome, prodRev)
    
    # OPERATIONAL EXPENSES ------------------------------------------------
    #    Part 1.10 - Get Operating Expenses
    totalOpExp = 0
    
    #   Part 1.11 - Get HR Costs
    hrExp = GetHRExp(decInfo, year)
    totalOpExp += hrExp
    
    #   Part 1.12 - Get Rent Expense
    rentExp = GetRentExp(decInfo, year, ale_lbl, lager_lbl)
    totalOpExp += rentExp
    
    #   Part 1.13 - Utilities Expense
    totCycs = aleVol/100000.0 + lagerVol/100000.0
    utilExp = GetUtilExp(year, totCycs)
    if mod:
        utilExp = GetUtilExpMod(year, prodAleVol2+prodLagerVol2, plannedAle+plannedLager)
    totalOpExp += utilExp
    
    #   Part 1.14 - Get Gas Expense
    gasExp = GetGasExp(totCycs)
    if mod and fcastTotRev != 0:
        pfGasExp = GetGasExp(int((plannedAle+plannedLager)/100000.0))
        gasExp = float(totalRev)/float(fcastTotRev) * pfGasExp
    totalOpExp += gasExp
    
    #   Part 1.15 - Marketing, Prod. Dev., and Other Exp
    mrktExp, prDvExp, othrExp = GetOtherExp(decInfo, year, fcastTotRev)
    totalOpExp += mrktExp
    totalOpExp += prDvExp
    totalOpExp += othrExp
    
    opExp = [hrExp, rentExp, utilExp, gasExp, mrktExp, prDvExp, othrExp]
    
    # EDBITDA, DEP/AMORT., EBIT, INTEREST EXP -----------------------------
    
    #   Part 1.16 - EBITDA
    ebitda = totalGI - totalOpExp
    
    #   Part 1.17 - depreciation & EBIT
    depr = GetDepr(decInfo, year, ale_lbl, lager_lbl)
    ebit = ebitda - depr
    
    #   Part 1.18 - STB & LTD Interest Expense
    ltdIE = GetLTDIntExp(decInfo, year)
    stbIE = GetSTBIntExp(decInfo, year)
    ebt = ebit - (ltdIE + stbIE)
    
    #   Part 1.19 - Taxes and Net Income
    taxes = 0.30 * ebt if ebt > 0 else 0
    
    netIncome = ebt - taxes
    
    #    Part 1.20 - Shares Outstanding
    sharesOut = GetSharesOut(decInfo, year)
    
    #----------------------------------------------------------------------
    #   PART II - BALANCE SHEET PART 1
    #----------------------------------------------------------------------

    # CURRENT ASSETS ------------------------------------------------------
    cash = 50000
    ar = GetAR(totalRev)
    inv = GetInventory(decInfo, year, totalCOGS, overProdExp)
    
    # ASSETS --------------------------------------------------------------
    grossPPE = GetGrossPPE(decInfo, year, ale_lbl, lager_lbl)
    accumDep = GetAccumDep(decInfo, year, ale_lbl, lager_lbl)
    netPPE = grossPPE - accumDep
    
    assets = cash + ar + inv + netPPE
    
    # LIABILITIES ---------------------------------------------------------
    ap = GetAP(totalCOGS, overProdExp)
    stb = GetSTB(decInfo, year)
    cLTD = GetCurrentLTD(decInfo, year)
    ltd = GetLTD(decInfo, year)
              
    liabilities = ap + stb + cLTD + ltd
    
    # EQUITY --------------------------------------------------------------
    cs = GetCS(decInfo, year)
    capSurplus = GetCapSurplus(decInfo, year)
    re = GetRE(year, netIncome)
    equity = cs + capSurplus + re
    
    #======================================================================
    # BALANCE SHEET PLUG
    #----------------------------------------------------------------------
    y1LTD = ltd+cLTD if year == 1 else 0
    
    plug = BSPlug(year, ebit, ltdIE, stbIE, assets, liabilities, cs+capSurplus, netIncome, y1LTD)
    
    plug = int(X_utilities.roundto(plug, 1))
    
    if (liabilities + equity) - assets < 0:
        loc = plug
        sti = 0
    else:
        loc = 0
        sti = plug
    
    # Update Income Statement after EBIT
    locIE = int(X_utilities.roundto(GetLoCIntExp(year, loc), 1))
    intExp = ltdIE + stbIE + locIE
    intInc = GetIntInc(year, sti, cs+capSurplus, y1LTD)
    ebt = ebit + intInc - intExp
    taxes = 0 if ebt < 0 else ebt * 0.30
    netIncome= int(ebt - taxes)
    
    # Update Balance Sheet
    re = GetRE(year, netIncome)
    
    #======================================================================
    # REVISED INCOME STATEMENT
    #----------------------------------------------------------------------
    ISout = []
    ISout.append(prodRev)
    ISout.append(prodCOGS)
    ISout.append(overProdExp)
    ISout.append(invSpoil)
    ISout.append(adjProdCOGS)
    ISout.append(prodGrossIncome)
    ISout.append(prodGrossMargin)
    ISout.append(opExp)
    ISout.append(depr)
    ISout.append(intInc)
    ISout.append(intExp)
    ISout.append(sharesOut)
    
    #======================================================================
    # REVISED BALANCE SHEET
    #----------------------------------------------------------------------
    BSout = []
    BSout.append([cash, sti, ar, inv])
    BSout.append([grossPPE, accumDep, netPPE])
    BSout.append([ap, stb, loc, cLTD])
    BSout.append(ltd)
    BSout.append([cs, capSurplus, int(re)])
    BSout.append(sharesOut)
                 
    #======================================================================
    # STATEMENT OF CASH FLOWS
    #----------------------------------------------------------------------
    CFout = []
    data = Q_data.Data(None)
    perfHist = data.GetData1()
    
    # Operating Activities
    if year == 1:
        chRec = -1 * ar
        chInv = -1 * inv
        chPay = ap
    else:
        chRec = perfHist[59][year-1] - ar
        chInv = perfHist[60][year-1] - inv
        chPay = ap - perfHist[63][year-1]
    CFout.append([netIncome, depr, chRec, chInv, chPay])
    
    # Investing Activities
    ppeSched = GetPPESched(decInfo, year, ale_lbl, lager_lbl)
    CFout.append([-1*ppeSched[2][year-1], 
                  -1*ppeSched[1][year-1],
                  -1*ppeSched[0][year-1]])
    
    # Financing Activities
    if year == 1:
        chSTB = stb
        chLoC = loc
        incLTD = decInfo[11][1]
        decLTD = 0
        incEq = decInfo[12][1]
    else:
        chSTB = stb - perfHist[64][year - 1]
        chLoC = loc - perfHist[65][year - 1]
        incLTD = decInfo[13][1] if year == 4 else 0
        decLTD = -1 * perfHist[66][year - 1]
        incEq = 0
    divPaid = 0
    CFout.append([chSTB, chLoC, incLTD, decLTD, incEq, divPaid])
    
    # Add in Beginning Cash Balance
    if year == 1:
        CFout.append(0)
    else:
        begCB = perfHist[69][year-1]
        CFout.append(begCB)
    
    #======================================================================
    # FINANCIAL RATIOS
    #----------------------------------------------------------------------
    FRout = []
    # Y2Y growth
    if year < 3:
        y2y = 0
    else:
        lastTotRev = 0
        for x in perfHist[51:57]:
            lastTotRev += x[year-1]
        try:
            y2y = ((totalRev - lastTotRev)/float(lastTotRev))*100.0
        except ZeroDivisionError:
            y2y = 0
    FRout.append(y2y)
    
    # Gross Margin 
    try:
        gm = (totalGI / float(totalRev))*100.0
    except ZeroDivisionError:
        gm = 0
    FRout.append(gm)
    
    # SG&A 
    try:
        sgaOfRev = (totalOpExp / float(totalRev)) * 100.0
    except ZeroDivisionError:
        sgaOfRev = 0
    FRout.append(sgaOfRev)
    
    # EBITDA Margin
    try:
        ebitdaMargin = (ebitda / float(totalRev)) * 100.0
    except ZeroDivisionError:
        ebitdaMargin = 0
    FRout.append(ebitdaMargin)    
        
    # EBIT Margin
    try:
        ebitMargin = (ebit / float(totalRev)) * 100.0
    except ZeroDivisionError:
        ebitMargin = 0
    FRout.append(ebitMargin)    
        
    # Tax Rate...
    taxRate = 0 if netIncome < 0 else 0.30
    FRout.append(taxRate)
    
    # Net Profit Margin...
    try:
        netPM = (netIncome / float(totalRev)) * 100.0
    except ZeroDivisionError:
        netPM = 0
    FRout.append(netPM)    
        
    # Current Ratio
    try:
        currentRatio = (cash + sti + ar + inv) / float(ap + stb + loc + cLTD)
    except ZeroDivisionError:
        currentRatio = 0
    FRout.append(currentRatio)    
        
    # Quick Ratio
    try:
        quickRatio = (cash + ar) / float(ap + stb + loc + cLTD)
    except ZeroDivisionError:
        quickRatio = 0
    FRout.append(quickRatio)    
        
    # Cash Ratio
    try:
        cashRatio = cash / float(ap + stb + loc + cLTD)
    except ZeroDivisionError:
        cashRatio = 0
    FRout.append(cashRatio)    
    
    # Days Inventory Outstanding:
    if year == 1:
        daysInvOut = 0
    else:
        try:
            daysInvOut = ((perfHist[60][year-1]+inv)/2.0)/(totalCOGS/365.0)
        except ZeroDivisionError:
            daysInvOut = 0
    FRout.append(daysInvOut)
    
    # Days Sales Outstanding
    if year == 1:
        daysSalesOut = 0
    else:
        try:
            daysSalesOut = ((perfHist[59][year - 1]+ar)/2.0)/(totalRev/365.0)
        except ZeroDivisionError:
            daysSalesOut = 0
    FRout.append(daysSalesOut)        
            
    # Days Payables Outstanding
    if year == 1:
        daysPayOut = 0
    else:
        try:
            daysPayOut = ((perfHist[63][year - 1] + ap)/2.0)/(totalCOGS/365.0)
        except ZeroDivisionError:
            daysPayOut = 0
    FRout.append(daysPayOut)
    
    # Cash Conversion Cycle
    ccc = daysInvOut + daysSalesOut - daysPayOut
    FRout.append(ccc)
    
    # ROA
    try:
        roa = netIncome / float(cash + ar + sti + inv + netPPE)
    except ZeroDivisionError:
        roa = 0
    FRout.append(roa)
    
    # ROE
    if year == 1:
        lastEq = 0
    else:
        lastEq = perfHist[68][year - 1] + cs + capSurplus
    newEq = re + cs + capSurplus
    try:
        roe = netIncome / float(((lastEq + newEq)) / 2.0)
    except ZeroDivisionError:
        roe = 0
    FRout.append(roe)
    
    # ROI
    if year == 1:
        lastAssets = 0
    else:
        lastAssets = perfHist[57][year-1]+perfHist[58][year-1]+\
            perfHist[59][year-1]+perfHist[60][year-1]+\
                (perfHist[61][year-1]-perfHist[62][year-1])
    newAssets = cash + sti + ar + inv + netPPE
    try:
        roi = netIncome / ((lastAssets + newAssets)/2.0)
    except ZeroDivisionError:
        roi = 0
    FRout.append(roi)
    
    # Est. Interest Rate
    if year == 1:
        try:
            estIR = intExp / (((loc + cLTD + ltd)+(cLTD+ltd))/2.0)
        except ZeroDivisionError:
            estIR = 0
    else:
        oldDebt = perfHist[65][year-1]+perfHist[66][year-1]+perfHist[67][year-1]
        newDebt = loc + cLTD + ltd
        try:
            estIR = intExp / ((oldDebt + newDebt)/2.0) 
        except ZeroDivisionError:
            estIR = 0
    FRout.append(estIR* 100.0)
    
    # Debt / Equity
    try:
        dTOe = float(cLTD + ltd) / float(cs + capSurplus + re)
    except ZeroDivisionError:
        dTOe = 0
    FRout.append(dTOe)
    
    # EBITDA / Interest Expense
    try:
        ebitdaToIntExp = ebitda / float(intExp)
    except ZeroDivisionError:
        ebitdaToIntExp = 0
    FRout.append(ebitdaToIntExp)
    
    #======================================================================
    # Return all this financial stuff
    #----------------------------------------------------------------------
    return [ISout, BSout, CFout,FRout]
    
#==========================================================================
# GENERAL INFORMATION
#--------------------------------------------------------------------------
def GetManMachTypes(decInfo, ale_lbl, lager_lbl):
    '''Find the type of each purchased machine (1=Ale, 2=Lager, 0=None)'''
    mTypes = []
    for x in decInfo[2:7]:
        if x[3] == 1:
            mTypes.append(1)
        elif x[3] == 2:
            mTypes.append(2)
        else:
            mTypes.append(0)
    return mTypes

#--------------------------------------------------------------------------
def GetManMachCycles(decInfo, year):
    '''Finds the number of cycles run on each machine.'''
    cycles = []
    for x in decInfo[16:21]:
        cycles.append(x[year])
    return cycles

#--------------------------------------------------------------------------
def GetProdVol(mTypes, cycles):
    '''Takes a list of the five machine types, and a list of the number
    of cycles done by each machine. Returns a list of 
    [aleVolume, lagerVolumne].'''
    aleVol, lagerVol = 0, 0
    for mType, cyc in zip(mTypes, cycles):
        if mType == 1:
            aleVol += cyc * 100000
        elif mType == 2:
            lagerVol += cyc * 100000
    return [aleVol, lagerVol]
    
#--------------------------------------------------------------------------
def GetProdUnits(decInfo, year, aleVol, lagerVol):
    '''Finds the production units for each product and returns them
    as a list. [ak, ab, ac, lk, lb, lc]'''
    packList = []
    for x in decInfo[39:45]:
        packList.append(x[year])
    ak = int(aleVol * (packList[0] / 100.0) / kegVol)
    ab = int(aleVol * (packList[1] / 100.0) / bottleVol)
    ac = int(aleVol * (packList[2] / 100.0) / canVol)
    lk = int(lagerVol * (packList[3] / 100.0) / kegVol)
    lb = int(lagerVol * (packList[4] / 100.0) / bottleVol)
    lc = int(lagerVol * (packList[5] / 100.0) / canVol)
    return [ak, ab, ac, lk, lb, lc]
    
#--------------------------------------------------------------------------
def GetProdShares(decInfo, year, aleVol, lagerVol):
    '''Returns the percent of total volume production assigned to
    each product.'''
    totalVol = aleVol + lagerVol
    if totalVol == 0:
        return [0, 0, 0, 0, 0, 0]
    packList = []
    for x in decInfo[39:45]:
        packList.append(x[year])
    
    ak = round(aleVol * (packList[0] / 100.0) / totalVol, 4)
    ab = round(aleVol * (packList[1] / 100.0) / totalVol, 4)
    ac = round(aleVol * (packList[2] / 100.0) / totalVol, 4)
    lk = round(lagerVol * (packList[3] / 100.0) / totalVol, 4)
    lb = round(lagerVol * (packList[4] / 100.0) / totalVol, 4)
    lc = round(lagerVol * (packList[5] / 100.0) / totalVol, 4)
    return [ak, ab, ac, lk, lb, lc]
    
#--------------------------------------------------------------------------
def GetProdLiters(decInfo, year, aleVol, lagerVol):
    '''Finds the production Liters for each product and returns them
    as a list. [ak, ab, ac, lk, lb, lc]'''
    packList = []
    for x in decInfo[39:45]:
        packList.append(x[year])
    ak = int(aleVol * (packList[0] / 100.0))
    ab = int(aleVol * (packList[1] / 100.0))
    ac = int(aleVol * (packList[2] / 100.0))
    lk = int(lagerVol * (packList[3] / 100.0))
    lb = int(lagerVol * (packList[4] / 100.0))
    lc = int(lagerVol * (packList[5] / 100.0))
    return [ak, ab, ac, lk, lb, lc]
    
#--------------------------------------------------------------------------
def GetAllowedProd(year, aleVol, lagerVol):
    '''GetAllowedProd(int year, int aleProd, int lagerProd)
    If the team produces over the allowed limit, then this returns
    the maximum allowed production. Otherwise, it returns the team's 
    starting value.'''
    bestOutput = Z_mrktInfo.BestOutput(year)
    allowable = Z_mrktInfo.AllowOverProd(year)
    maxAle = bestOutput[0] * (1 + allowable)
    maxLager = bestOutput[1] * (1 + allowable)
    
    if aleVol > maxAle: aleVol = maxAle
    if lagerVol > maxLager: lagerVol = maxLager
    
    return [aleVol, lagerVol]
    
#--------------------------------------------------------------------------
def GetStartSalesVol(year, aleVol, lagerVol):
    '''Returns the starting sales volume. If the production is greater than
    the best case, than the starting sales volume is equal to the 
    best case. Otherwise, the starting sales volume is equal to the 
    production volume.'''
    bestAle, bestLager = Z_mrktInfo.BestOutput(year)
    aleSalesVol = bestAle if aleVol > bestAle else aleVol
    lagerSalesVol = bestLager if lagerVol > bestLager else lagerVol
    
    return [aleSalesVol, lagerSalesVol]

#--------------------------------------------------------------------------
def GetProdHistory(decInfo, year):
    '''Get Production History from year 1 up to the current year. This
    returns the total liters of production for each year.'''
    data = Q_data.Data(None)
    decHist = data.GetData1()
              
    # Get Information from the past years
    prodHist = []
    for x in range(1,7):
        totalProd = 0
        for y in decHist[16:21]:
            totalProd += y[x] * 100000
        prodHist.append(totalProd)
        
    # Insert Information for the current year
    totalProd = 0
    for x in decInfo[16:21]:
        totalProd += x[year]
    prodHist[year-1] = totalProd * 100000
    
    prodHist = prodHist[:year]
    prodHist += [0 for x in range(6-len(prodHist))]
    return prodHist
            
#--------------------------------------------------------------------------
# INCOME STATEMENT FUNCTIONS
#--------------------------------------------------------------------------
def GetProdRev(decInfo, year, prodUnits):
    '''Finds the revenue generated by each product.'''
    priceList = []
    for x in decInfo[33:39]:
        priceList.append(x[year])
    prodRev = []
    for price, unitCt in zip(priceList, prodUnits):
        prodRev.append(int(price * unitCt))
    return prodRev

#--------------------------------------------------------------------------
def GetCOGS(decInfo, year, totalProdVol, soldVol):
    '''Finds the cost of goods sold for appropriate product / 
    ingrediant quality combination for the current year. '''
    cogs1 = Z_mrktInfo.getCOGS(year, totalProdVol)
    aleCol = decInfo[45][year] - 1
    lagerCol = decInfo[46][year] - 1
    cogs2 = []
    for x in cogs1:
        cogs2.append(x[aleCol])
    for x in cogs1:
        cogs2.append(x[lagerCol])
    packList = []
    for x in decInfo[39:45]:
        packList.append(x[year])

    rslt = []
    for cogs, lits in zip(cogs2, soldVol):
        rslt.append(int(cogs * lits))
        
    return rslt

#--------------------------------------------------------------------------
def GetOverProdCost(decInfo, year, adjProdVol, endSalesVol):
    '''Takes a Year, the ending, adjusted production volume for all
    products, the ending, and the adjusted sales volumens for all products.
    Returns the OverProduction Expense.'''
    # Get the COGS for the ending production volume
    aleProdVol = adjProdVol[0] + adjProdVol[1] + adjProdVol[2]
    lagerProdVol = adjProdVol[3] + adjProdVol[4] + adjProdVol[5]
    
    cogsX = Z_mrktInfo.getCOGS(year, aleProdVol + lagerProdVol)
    aleCol = decInfo[45][year] - 1
    lagerCol = decInfo[46][year] - 1
    cogs = []
    for x in cogsX:
        cogs.append(x[aleCol])
    for x in cogsX:
        cogs.append(x[lagerCol])
    
    # Find the difference between produced and sold volume
    volDiff = []
    for p, s in zip(adjProdVol, endSalesVol):
        volDiff.append(p - s)
    
    # Find the COGS of the volume difference
    rslt = []
    for d, c in zip(volDiff, cogs):
        rslt.append(int(d*c))
        
    overProdCost = 0
    for x in rslt:
        overProdCost += x
    return overProdCost

#--------------------------------------------------------------------------
def GetInvSpoil(decInfo, year, totCOGS, overProdExp):
    '''Finds the Inventory Spoilage Expense.'''
    inventory = GetInventory(decInfo, year, totCOGS, overProdExp)
    if inventory == 0:
        return 0
    else:
        return int((totCOGS + overProdExp)/365*daysOfFG - inventory)
    
#--------------------------------------------------------------------------
def GetGrossIncome(prodRev, prodCOGS):
    '''Finds the gross income.'''
    grossIncome = []
    for rev, cogs in zip(prodRev, prodCOGS):
        grossIncome.append(rev - cogs)
    return grossIncome

#--------------------------------------------------------------------------
def GetGrossMargin(prodGrossIncome, prodRev):
    '''Finds the gross margin.'''
    grossMargin = []
    for gi, rev in zip(prodGrossIncome, prodRev):
        try:
            grossMargin.append((round(float(gi) / float(rev), 4) * 100))
        except ZeroDivisionError:
            grossMargin.append(0)
    return grossMargin

# OPERATIONAL EXPENSES
#--------------------------------------------------------------------------
def GetHRExp(decInfo, year):
    '''Gets the total HR expense for the current year.'''
    posCosts = Z_mrktInfo.getHRCosts(year)
    decisions = decInfo[21:33]
    posCnts = []
    for x in decisions:
        posCnts.append(x[year])
    hrExp = 0
    for cost, cnts in zip(posCosts, posCnts):
        hrExp += int(cost * cnts)
    return hrExp

#--------------------------------------------------------------------------
def GetRentExp(decInfo, year, aleLbl, lagerLbl):
    '''Finds the total rental expense for the current decisions.'''
    # Gets the base price per foot for the current year
    basePPF = 5*(1.03)**(year-1)
    
    # Get Necessary Info 
    #----------------------------------------------------------------------
    # Get Max Production Capacity (Max # of Cycles)
    maxCycles = 0
    machCt = 0
    lagerPresent = False
    
    for m in decInfo[2:7]:
        if year < 4:
            if m[1] and m[3] == 1:
                maxCycles += 15
                machCt += 1
            elif m[1] and m[3] == 2:
                maxCycles += 9
                machCt += 1
                lagerPresent = True
        else:
            if m[2] and m[3] == 1:
                maxCycles += 15
                machCt += 1
            elif m[2] and m[3] == 2:
                maxCycles += 9
                machCt += 1
                lagerPresent = True
    
    # Calculate Rent
    #----------------------------------------------------------------------
    # Get Storage of RM Rental Costs
    sqFeetNeeded = int(X_utilities.roundup(maxCycles/12.0/2.0)*100000/16.0)
    rmRentExp = int(sqFeetNeeded * basePPF)
    
    # Get Brewing Floor Space Rental Costs
    sqFtPerBrewMachine = 1750
    minSqFtOffice = 1000
    sqFeetNeeded = machCt * sqFtPerBrewMachine + minSqFtOffice
    brRentExp = int(sqFeetNeeded * basePPF)
    
    # Get Storage of FG Rental Costs
    litersPerCycle = 100000
    storageLitersPerFt = 16.0
    if year < 4:
        percOfOutput = decInfo[10][1]/100.0
    else:
        percOfOutput = decInfo[10][2]/100.0
        
    sqFeetNeeded = (maxCycles * litersPerCycle) / storageLitersPerFt * percOfOutput
    if lagerPresent:
        pricePerFoot = basePPF * 1.5
    else:
        pricePerFoot = basePPF
        
    fgRentExp = int(sqFeetNeeded * pricePerFoot)
    
    return rmRentExp + brRentExp + fgRentExp

#--------------------------------------------------------------------------
def GetUtilExp(year, totCycles):
    '''Gets the total Utility expenses for the year.'''
    eBase = 10000 * 1.03 ** (year - 1)
    gBase = 10000 * 1.03 ** (year - 1)
    wBase = 10000 * 1.03 ** (year - 1)
    iBase = 300 * 1.03 ** (year - 1)
    pBase = 600 * 1.03 ** (year - 1)
    ePC = (1000 * 1.03 ** (year-1)) * totCycles
    gPC = (50 * 1.03 ** (year - 1)) * totCycles
    wPC = (50 * 1.03 ** (year - 1)) * totCycles
    return int(eBase + gBase + wBase + iBase + pBase + ePC + gPC + wPC)
  
#--------------------------------------------------------------------------
def GetUtilExpMod(year, adjOutput, plannedOutput):
    '''Gets the utility expense for the modified / scored calculation.
    This finds the Pro Forma utilities expense, scales the variable
    utility cost by the ration of adjOutput to plannedOutput, and
    adds the base cost.'''
    eBase = 10000 * 1.03 ** (year - 1)
    gBase = 10000 * 1.03 ** (year - 1)
    wBase = 10000 * 1.03 ** (year - 1)
    iBase = 300 * 1.03 ** (year - 1)
    pBase = 600 * 1.03 ** (year - 1)
    baseUtilExp = eBase+gBase+wBase+iBase+pBase
    if plannedOutput == 0:
        return baseUtilExp
    
    pfUtilExp = GetUtilExp(year, int(plannedOutput / 100000.0))
    varUtilExp = pfUtilExp - baseUtilExp
    varUtilExp = float(adjOutput)/float(plannedOutput)*varUtilExp
    
    return int(varUtilExp + baseUtilExp)

#--------------------------------------------------------------------------
def GetGasExp(totCycles):
    '''Finds the total fuel expense for the year.'''
    truckCap = 5000
    litersProd = int(totCycles) * 100000
    return litersProd / truckCap * 75

#--------------------------------------------------------------------------
def GetOtherExp(decInfo, year, totalRev):
    '''Finds the marketing, product development and other op exp for
    the current year.'''
    if year == 1:
        markExp = 15000
        prDvExp = 0
        othrExp = 5000
    else:
        markExp = (decInfo[47][year] / 100) * totalRev
        prDvExp = (decInfo[48][year] / 100) * totalRev
        othrExp = ((decInfo[49][year] / 100) + (decInfo[50][year] / 100)) * totalRev
    return [int(markExp), int(prDvExp), int(othrExp)]
    
# DEPRECIATION
#--------------------------------------------------------------------------
def GetPPESched(decInfo, year, ale_lbl, lager_lbl):
    '''Finds the PPE purchases for each year.'''
    data = Q_data.Data(None)
    
    # Get Equipment Purchases ---------------------------------------------
    eqPrchs = [50000, 0, 0, 0, 0, 0, 0]
    
    # Get Production Machinery Purchases ----------------------------------
    decHist = data.GetData1()
    
    y1MaPrchs, y2MaPrchs = 0, 0
    if year == 1:
        for x in decInfo[2:7]:
            if x[1] and x[3] == 1:
                y1MaPrchs += 150000
            elif x[1] and x[3] == 2:
                y1MaPrchs += 200000
        if decInfo[7][1]: y1MaPrchs += 30000
        if decInfo[8][1]: y1MaPrchs += 40000
        if decInfo[9][1]: y1MaPrchs += 40000
        y2MaPrchs = y1MaPrchs
    elif year == 2 or year == 3:
        for x in decHist[2:7]:
            if x[1] and x[3] == 1:
                y1MaPrchs += 150000
            elif x[1] and x[3] == 2:
                y1MaPrchs += 200000
        if decHist[7][1]: y1MaPrchs += 30000
        if decHist[8][1]: y1MaPrchs += 40000
        if decHist[9][1]: y1MaPrchs += 40000
        y2MaPrchs = y1MaPrchs
    elif year == 4:
        for x in decHist[2:7]:
            if x[1] and x[3] == 1:
                y1MaPrchs += 150000
            elif x[1] and x[3] == 2:
                y1MaPrchs += 200000
        if decHist[7][1]: y1MaPrchs += 30000
        if decHist[8][1]: y1MaPrchs += 40000
        if decHist[9][1]: y1MaPrchs += 40000
        
        for x in decInfo[2:7]:
            if x[2] and x[3] == 1:
                y2MaPrchs += 150000
            elif x[2] and x[3] == 2:
                y2MaPrchs += 200000
        if decInfo[7][2]: y2MaPrchs += 30000
        if decInfo[8][2]: y2MaPrchs += 40000
        if decInfo[9][2]: y2MaPrchs += 40000
    else:
        for x in decHist[2:7]:
            if x[1] and x[3] == 1:
                y1MaPrchs += 150000
            elif x[1] and x[3] == 2:
                y1MaPrchs += 200000
        if decHist[7][1]: y1MaPrchs += 30000
        if decHist[8][1]: y1MaPrchs += 40000
        if decHist[9][1]: y1MaPrchs += 40000
        
        for x in decHist[2:7]:
            if x[2] and x[3] == 1:
                y2MaPrchs += 150000
            elif x[2] and x[3] == 2:
                y2MaPrchs += 200000
        if decHist[7][2]: y2MaPrchs += 30000
        if decHist[8][2]: y2MaPrchs += 40000
        if decHist[9][2]: y2MaPrchs += 40000
    
    # If the machines were already purchased in year 1, they will have
    #   been double counted in year 4. So, y2MaPrchs = y2MaPrchs - y1MaPrchs
    y2MaPrchs = y2MaPrchs - y1MaPrchs
    maPrchs = [y1MaPrchs, 0, 0, y2MaPrchs, 0, 0]
    
    # Get Truck Purchases -------------------------------------------------
    prodHist = GetProdHistory(decInfo, year)
    
    trucks = 0
    trPrchs = []
    for x in prodHist:
        trucksNeeded = X_utilities.roundup(x/1800000.0)
        if trucksNeeded > trucks:
            trPrchs.append((trucksNeeded - trucks)*30000)
            trucks += trucksNeeded - trucks
        else:
            trPrchs.append(0)
    
    return [maPrchs, trPrchs, eqPrchs]
    
#--------------------------------------------------------------------------
def GetDeprSched(decInfo, year, ale_lbl, lager_lbl):
    '''Finds the depreciation for current year.'''
    trPrchs = GetPPESched(decInfo, year, ale_lbl, lager_lbl)[1]
    maPrchs = GetPPESched(decInfo, year, ale_lbl, lager_lbl)[0]
    y1MaPrchs = maPrchs[0]
    y2MaPrchs = maPrchs[3]
    
    # Make depreciation schedules & Total Depreciation for the year
    #----------------------------------------------------------------------
    # Add the depreciation for General Equipment
    eqDepSched = []
    eqDepSched.append([10000, 10000, 10000, 10000, 10000,0])
    for i in range(5):
        eqDepSched.append([0 for x in range(6)])
    
    trDepSched = []
    # Add the depreciation for Trucks
    yr = 1
    for x in trPrchs:
        depSched = []
        # Append leading zeros
        if yr == 1:
            depSched.append(0)
        else:
            for y in range(yr - 1):
                depSched.append(0)
        # Append the remaining Depr. ammounts for Capital Purchases per year
        for y in range(10):
            depSched.append(int(x / 10.0))
        depSched = depSched[:6]
        trDepSched.append(depSched)
        yr += 1
    
    # Add the depcreciation for Machines
    maDepSched = []
    maDepSched.append([0 for x in range(6)])
    maDepSched.append([0] + [y1MaPrchs/10 for x in range(5)])
    maDepSched.append([0 for x in range(6)])
    maDepSched.append([0 for x in range(3)]+[y2MaPrchs/10 for x in range(3)])
    maDepSched.append([0 for x in range(6)])
    maDepSched.append([0 for x in range(6)])
    
    # Summary List - Adds up the first six years.
    eqDepSum = []
    trDepSum = []
    maDepSum = []
    
    for yr in range(6):
        depTot = 0
        for sched in eqDepSched:
            depTot += sched[yr]
        eqDepSum.append(depTot)
        depTot = 0
        for sched in trDepSched:
            depTot += sched[yr]
        trDepSum.append(depTot)
        depTot = 0
        for sched in maDepSched:
            depTot += sched[yr]
        maDepSum.append(depTot)
    
    return [eqDepSum, trDepSum, maDepSum]
    
#--------------------------------------------------------------------------
def GetDepr(decInfo, year, ale_lbl, lager_lbl):
    '''Gets depreciation for the current year.'''
    eq, tr, ma = GetDeprSched(decInfo, year, ale_lbl, lager_lbl)
    
    return eq[year-1] + tr[year-1] + ma[year-1]

#--------------------------------------------------------------------------
def GetIntInc(year, sti, equity, y1LTD):
    '''Gets the interest income from the current balance of short term
    investments.'''
    data = Q_data.Data(None)
    if year == 1 and sti > 0:
        intInc = ((sti + (equity + y1LTD))/2)* 0.03
    elif year > 1:
        lastSTI = data.GetData1()[58][year-1]
        intInc = ((lastSTI + sti)/2) * 0.03
    else:
        intInc = 0
    return intInc
    
#--------------------------------------------------------------------------
def GetSTBIntExp(decInfo, year):
    '''Gets the total STB Interest Expense for the current year.'''
    stbAmt = decInfo[14][year]
    stbRate = decInfo[15][year] / 100.0
    return int(stbAmt * stbRate)
    
#--------------------------------------------------------------------------
def GetLTDIntExp(decInfo, year):
    '''Gets the total LTD Interest Expense for the current year.'''
    ltdInfo = GetLTDInfo(decInfo, year)
    l1int = ltdInfo[2][year-1]
    l2int = ltdInfo[6][year-1]
    return l1int + l2int

#--------------------------------------------------------------------------
def GetLoCIntExp(year, loc):
    '''Gets the line of credit expense for the current year.'''
    data = Q_data.Data(None)
    if year == 1:
        lastLoC = 0
    else:
        lastLoC = data.GetData1()[65][year-1]
    # Get old and new LoC rates
    rate1 = GetLoCRate(lastLoC)
    rate2 = GetLoCRate(loc)
    rslt = ((lastLoC + loc)/2) * ((rate1 + rate2)/2)
    
    return rslt
     
#--------------------------------------------------------------------------
def GetSharesOut(decInfo, year):
    '''Gets the number of shares outstanding for the current year.'''
    if year == 1:
        sharesOut = decInfo[12][1]
    else:
        data = Q_data.Data(None)
        sharesOut = data.GetData1()[12][1]
    return sharesOut
    
#==========================================================================
# BALANCE SHEET FUNCTIONS
#--------------------------------------------------------------------------
# ASSETS ------------------------------------------------------------------
def GetInventory(decInfo, year, cogs, overProd):
    '''Returns the Balance Sheet Inventory for the current round.'''
    fgSpace = decInfo[10][1]/100.0 if year <=3 else decInfo[10][2]/100.0
    allCogs = cogs + overProd # Total COGS + Overproduction Expense
    if allCogs / 365 * daysOfFG > allCogs * fgSpace:
        inv = allCogs * fgSpace
    else:
        inv = allCogs / 365 * daysOfFG
    return int(inv)

#--------------------------------------------------------------------------
def GetAR(totalRev):
    '''Returns the Accounts Receivable.'''
    daysOfSalesOut = 44.9256
    ar = (totalRev / 365) * daysOfSalesOut
    return int(ar)
    
#--------------------------------------------------------------------------
def GetGrossPPE(decInfo, year, ale_lbl, lager_lbl):
    '''Returns the gross PPE for the current year.'''
    PPE = GetPPESched(decInfo, year, ale_lbl, lager_lbl)
    grossPPE = 0
    for x in range(year):
        grossPPE += PPE[0][x] + PPE[1][x] + PPE[2][x]
    return grossPPE

#--------------------------------------------------------------------------
def GetAccumDep(decInfo, year, ale_lbl, lager_lbl):
    '''Returns the accumulated depreciation for the current year.'''
    eq, tr, ma = GetDeprSched(decInfo, year, ale_lbl, lager_lbl)
    accumDep = 0
    for i in range(year):
        accumDep += eq[i] + tr[i] + ma[i]
    return accumDep

# LIABILITIES -------------------------------------------------------------
def GetAP(totalCOGS, overProdExp):
    '''Returns the Accounts Payable.'''
    daysPayableOut = 68.6643
    ap = int(((totalCOGS + overProdExp) / 365) * daysPayableOut)
    return ap
    
#--------------------------------------------------------------------------
def GetSTB(decInfo, year):
    '''Returns the selected draw for Short Term Borrowing.'''
    if year < 3:
        return 0
    else:
        return decInfo[14][year]
        
#--------------------------------------------------------------------------
def GetLTDInfo(decInfo, year):
    '''Gets the total LTD Current Payment and interest expense for the
    current year.'''
    # Get LTD Info
    data = Q_data.Data(None)
    decHist = data.GetData1()
    if year == 1:
        amt1, rate1, per1 = decInfo[11][1:]
        amt2, rate2, per2 = 0, 0, 0
    elif year == 2 or year == 3:
        amt1, rate1, per1 = decHist[11][1:]
        amt2, rate2, per2 = 0, 0, 0
    elif year == 4:
        amt1, rate1, per1 = decHist[11][1:]
        amt2, rate2, per2 = decInfo[13][1:]
    else:
        amt1, rate1, per1 = decHist[11][1:]
        amt2, rate2, per2 = decHist[13][1:]
    
    rate1, rate2 = rate1/100.0, rate2/100.0
    
    # Get Principle Payment Schedules for each loan
    l1pmts = []
    l2pmts = [0, 0, 0]
    for x in range(per1):
        l1pmts.append(amt1/per1)
    for x in range(per2):
        l2pmts.append(amt2/per2)
    for x in range(6-len(l1pmts)):
        l1pmts.append(0)
    for x in range(6-len(l2pmts)):
        l2pmts.append(0)
    l2pmts = l2pmts[:6]
    
    # Get Interest Payment, Beg/End Balance Schedules for Loan 1
    l1int = []          # Loan 1 Interest Payments
    l1beg = []          # Loan 1 Beginning Balances
    l1end = []          # Loan 1 Ending Balances
    l1int.append(amt1 * rate1)
    l1beg.append(0)
    l1end.append(amt1)
    for x in range(1, 6):
        l1beg.append(l1end[x-1])
        end = 0 if l1beg[x] - l1pmts[x-1] == 1 else l1beg[x] - l1pmts[x-1]
        l1end.append(end)
        l1int.append(int(((l1beg[x] + l1end[x])/2) * rate1))
        
    # Get Interest Paymtent, Beg/End Balance Schedules for Loan 2
    l2int = [0, 0, 0]
    l2beg = [0, 0, 0]
    l2end = [0, 0, 0]
    l2int.append(amt2 * rate2)
    l2beg.append(0)
    l2end.append(amt2)
    for x in range(4, 6):
        l2beg.append(l2end[x-1])
        end = 0 if l2beg[x] - l2pmts[x-1] == 1 else l2beg[x] - l2pmts[x-1]
        l2end.append(end)
        l2int.append(int(((l2beg[x] + l2end[x])/2) * rate2))
    
    # Get Total Principle Payment Schedule
    pmts = []
    for x in range(6):
        pmts.append(l1pmts[x] + l2pmts[x])
        
    return [l1beg, l1pmts, l1int, l1end, l2beg, l2pmts, l2int, l2end]
    
#--------------------------------------------------------------------------
def GetCurrentLTD(decInfo, year):
    '''Gets the current portion of long term debt for the current year.'''
    ltdInfo = GetLTDInfo(decInfo, year)
    l1pmts = ltdInfo[1][year-1]
    l2pmts = ltdInfo[5][year-1]
    return l1pmts + l2pmts

#--------------------------------------------------------------------------
def GetLTD(decInfo, year):
    '''Gets the remaining Balance Sheet value of the LTD for the current
    year.'''
    ltdInfo = GetLTDInfo(decInfo, year)
    l1end = ltdInfo[3][year-1]
    l2end = ltdInfo[7][year-1]
    l1pmts = ltdInfo[1][year-1]
    l2pmts = ltdInfo[5][year-1]
    return (l1end - l1pmts) + (l2end - l2pmts)
    
#==========================================================================
# EQUITY FUNCTIONS
#--------------------------------------------------------------------------
def GetCS(decInfo, year):
    '''Returns the common stock for the Balance Sheet.'''
    if year == 1:
        equity = decInfo[12][1]
    else:
        data = Q_data.Data(None)
        equity = data.GetData1()[12][1]
    return int(equity *0.01)
    
#--------------------------------------------------------------------------
def GetCapSurplus(decInfo, year):
    '''Returns the capital surplus for the balance sheet.'''
    if year == 1:
        equity = decInfo[12][1]
    else:
        data = Q_data.Data(None)
        equity = data.GetData1()[12][1]
    return int(equity *0.99)
    
#--------------------------------------------------------------------------
def GetRE(year, netIncome):
    '''Gets the retained earnings for the current year.'''
    data = Q_data.Data(None)
    if year == 1:
        return netIncome
    else:
        lastRE = data.GetData1()[68][year-1]
        
    return lastRE + netIncome
    
#==========================================================================
# SCORING FUNCTIONS
#--------------------------------------------------------------------------
def BSPlug(year, ebit, ltdIE, stbIE, assets, liabilities, equity, stNI,
           y1LTD, sti= 0, loc = 0):
    '''(year, EBIT, LTD Int. Exp., STB Int. Exp., Assets less short-term inv.,
    liabilities less Line of Credit, equity (Common Stock + Capital Surplus),
    last year's Retained Earnings, LTD, short term investments, 
    Line of Credit)
    
    This is the plug for the balance sheet. If the accounting 
    equation doesn't hold (A = L + E), this finds the difference.
    
    If the difference is positive, the equation finds the amount
    of short term investments. This affects interest income => ebt =>
    tax => net income => retained earnings => bsPlug.
    
    If the difference is negative, the equation finds the amount of
    Line of Credit. This affects interest expense => ebt => tax =>
    net income => retained earnings => bsPlug.
    
    The function will call itself until the change in retained earnings 
    is lest than 1.'''
    data = Q_data.Data(None)
    # Get last year's Retained Earnings -----------------------------------
    if year == 1:
        lastRE = 0
    else:
        lastRE = data.GetData1()[68][year-1]
                                 
    # Get Assets and Liabilities ------------------------------------------
    a = assets + sti
    l = liabilities + loc
    
    # Get Interest Income -------------------------------------------------
    intInc = GetIntInc(year, sti, equity, y1LTD)
        
    # Get Interest Expense ------------------------------------------------
    locIE = GetLoCIntExp(year, loc)
    intExp = ltdIE + stbIE + locIE
    
    # Get Revised Retained Earnings ---------------------------------------
    ebt = ebit + intInc - intExp
    taxes = 0.30 * ebt if ebt > 0 else 0
    endNI = ebt - taxes
    newRE = lastRE + endNI
    
    # Get Equity for this round -------------------------------------------
    e = equity + newRE
    
    # Find Plug ----------------------------------------------------------
    plug = (l + e) - a
    if plug < 0:
        loc = loc + (-1 * plug)
    else:
        sti = sti + plug
    plug = -1 * plug if plug < 0 else plug
    
    if plug < 1 and plug > 0:
        return 1
    else:
        return plug + BSPlug(year, ebit, ltdIE, stbIE, assets, liabilities, equity, stNI,
           y1LTD, sti, loc)

#--------------------------------------------------------------------------
def GetLoCRate(loc):
    '''Gets the rate for the Line of Credit Draw.'''
    if loc == 0:
        locRate = 0
    elif loc > 0 and loc < 1000000:
        locRate = 0.07
    elif loc >= 1000000 and loc < 2000000:
        locRate = 0.10
    elif loc >= 2000000 and loc < 3000000:
        locRate = 0.13
    elif loc >= 3000000 and loc < 4000000:
        locRate = 0.16
    elif loc >= 4000000 and loc < 5000000:
        locRate = 0.19
    else:
        locRate = 0.22
    return locRate

#==========================================================================
# SCORING FUNCTIONS
#--------------------------------------------------------------------------
def ScoreF1(answer, bestCase, low, high):
    '''Returns a score between 0 and 1 given an answer, a best case answer, 
    a lower limit, and an upper limit.'''
    answer = float(answer)
    bestCase = float(bestCase)
    low = float(low)
    high = float(high)
    try:
        if answer < bestCase:
            rslt = math.fabs(bestCase - answer) / math.fabs(bestCase - low)
        elif answer > bestCase:
            rslt = math.fabs(answer - bestCase) / math.fabs(high - bestCase)
        else:
            rslt = 0
    except ZeroDivisionError:
        rslt = 0
    
    if rslt > 1: rslt = 1
    
    return rslt
    
#--------------------------------------------------------------------------
def OutputScore(decInfo, year, fcastRev, totalProdCycles):
    '''Returns the OutputScore for the current round. This is affected by
    HR decisions excluding Head of Marketing, Sales Reps, and Cust Service.
    Deviations from the best case result in a positive score between
    0 % and 100 %.'''
    bestHR = Z_mrktInfo.BestHR(fcastRev, totalProdCycles)
    
    weights = [0.0, 0.10, 0.10, 0.10, 0.0, 0.0, 
               0.0, 0.15, 0.20, 0.10, 0.10, 0.15]
    decHR = decInfo[21:33]
    indScores = []
    for ans, best, wght in zip(decHR, bestHR, weights):
        indScores.append(ScoreF1(ans[year], best, 0, best) * wght)
    score = 0
    for s in indScores:
        score += s
    return score

#--------------------------------------------------------------------------
def OutputAdjust(decInfo, year, outputScore, aleVol, lagerVol):
    '''Adjusts the production outputs based on the teams Output Score. 
    Returns the adjusted ale and lager total liters produced.'''
    mod = Z_mrktInfo.OutputMod(year)
    scoreXmod = outputScore * mod
    aleVol = aleVol + (aleVol * scoreXmod)
    lagerVol = lagerVol + (lagerVol * scoreXmod)
    
    return [aleVol, lagerVol]
    
#--------------------------------------------------------------------------
def ProductScores(decInfo, year):
    '''Returns the Product Score for the year.'''
    # Get an ordered list of the product decisions - Ing. Qlty., ASP, Pack.
    x = decInfo[45:47] + decInfo[33:45]
    prodDec = []
    for i in x:
        prodDec.append(i[year])
    # Get the Best Case product decisions
    if year <= 4:
        bestDec = Z_mrktInfo.BestProduct(year)
    else:
        bestDecA = Z_mrktInfo.BestProduct(year)
        # Best Case Ingrediend Quality
        ingQuality = bestDecA[:2]
        # Best Case Ale Prices for selected Quality
        if prodDec[0] == 1:
            alePrices = bestDecA[2][0][:3]
        elif prodDec[0] == 2:
            alePrices = bestDecA[2][1][:3]
        else:
            alePrices = bestDecA[2][2][:3]
        # Best Case Lager Prices for selected Quality
        if prodDec[1] == 1:
            lagerPrices = bestDecA[2][0][3:]
        elif prodDec[1] == 2:
            lagerPrices = bestDecA[2][1][3:]
        else:
            lagerPrices = bestDecA[2][2][3:]
        # Best Case Packaging Selections
        packaging = bestDecA[3:]
        # Create final "Best Decisions" list
        bestDec = ingQuality + alePrices + lagerPrices + packaging

    scores = []
    scores.append(ScoreF1(prodDec[0], bestDec[0], 1, 3))
    scores.append(ScoreF1(prodDec[1], bestDec[1], 1, 3))
    
    for i in range(2, 8):
        high = bestDec[i] + 0.2 * bestDec[i]
        scores.append(ScoreF1(prodDec[i], bestDec[i], bestDec[i], high))
        
    for i in range(8, 14):
        low = int(bestDec[i] - 0.3 * bestDec[i])
        scores.append(ScoreF1(prodDec[i], bestDec[i], low, bestDec[i]))
        
    if year < 4:
        return scores[8:]

    prodScores = []
    for i in range(6):
        if i < 3:
            iqScore = scores[0]
        else:
            iqScore = scores[1]
        prodScores.append((0.2*iqScore) + (0.5*scores[i+2]) + (0.3*scores[i+8]))
    return prodScores
    
#--------------------------------------------------------------------------
def SalesAdjust1(year, adjProdLit, prodScores):
    '''Takes the Product Scores and the adjusted Per-Product production
    in liters and returns the first sales adjustment.'''
    rslt = []
    mod = Z_mrktInfo.ProductMod(year)
    for vol, score in zip(adjProdLit, prodScores):
        rslt.append(int(score * mod * vol))
    return rslt

#--------------------------------------------------------------------------
def GenSalesScore(decInfo, year, fcastRev, totCycles):
    '''Finds the General Sales Score.'''
    if year < 2:
        return 0
    if year == 2:
        score = 0
        bestOther = Z_mrktInfo.BestOther(year)
        actualOther = decInfo[47:51]
        for best, actual in zip(bestOther, actualOther):
            score += 0.25 * ScoreF1(actual[year], best, 0, 2.5)
        return score
    
    # Find best case decisions
    bestHR = Z_mrktInfo.BestHR(fcastRev, totCycles)
    bestOther = Z_mrktInfo.BestOther(year)
    bestList = bestHR[4:7] + bestOther
    # Find Actual decisions
    actualList = decInfo[25:28] + decInfo[47:51]
    # Weights - 
    weights = [0.10, 0.20, 0.20, 0.25, 0.10, 0.075, 0.075]
    # Find the Score
    score = 0
    x = 0
    for answer, best, weight in zip(actualList, bestList, weights):
        if x >= 3:
            score += ScoreF1(answer[year], best, 0, 2.5) * weight
        else:
            score += ScoreF1(answer[year], best, 0, best) * weight
        x += 1
    
    return score
        
#--------------------------------------------------------------------------
def SalesAdjust2(year, adjProdLit, genScore):
    '''Takes the Gen. Sales Core and the adjusted Per-Product production
    in liters and returns sales adjustment 2.'''
    rslt = []
    mod = Z_mrktInfo.GenSalesMod(year)
    for vol in adjProdLit:
        rslt.append(int(genScore * mod * vol))
    return rslt
    
#--------------------------------------------------------------------------
def GetSalesVol(decInfo, year, soldProdVol1, salesAdj1, salesAdj2):
    '''Takes the adjusted production and subtracts sales adjustements
    1 and 2, then returns the actual ale/lager volume lilters sold.'''
    rsltVol = []
    kegVol = 64.0
    bottleVol = 1.0/2.0
    canVol = 1.0/3.0
    for prod, adj1, adj2 in zip(soldProdVol1, salesAdj1, salesAdj2):
        finalVol = int(prod + adj1 + adj2)
        rsltVol.append(finalVol)
    ak = int(rsltVol[0] / kegVol)
    ab = int(rsltVol[1] / bottleVol)
    ac = int(rsltVol[2] / canVol)
    lk = int(rsltVol[3] / kegVol)
    lb = int(rsltVol[4] / bottleVol)
    lc = int(rsltVol[5] / canVol)
    rsltUnit = [ak, ab, ac, lk, lb, lc]
    return [rsltVol, rsltUnit]
    
    
    
