#!python
# -*- encoding: utf-8 -*-

# F_balanceSheet_A_pnl.py

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
E_results_pnl.py +
                 + F_balancedSC_A_pnl.py
                 + F_incomeStmt_A_pnl.py
                 + F_balanceSheet_A_pnl.py
                 + F_cashFlow_A_pnl.py

This module contains the Balance Sheet "A" Panel class code for the Novus 
Business and IT education program. The "A" panel show the 
results for every year, up to the present year provided to the "Init"
function.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import X_styles, X_miscPnls
import Q_data
from Q_language import GetPhrase

class BalanceSheet_A_Pnl(scrolled.ScrolledPanel):
    '''This class holds the Balance Sheet panel for the Novus Business and IT 
    education program.'''
    def __init__(self, parent, *args, **kwargs):
        scrolled.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        self.SetBackgroundColour(wx.WHITE)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.balanceSht_lbl = GetPhrase('balanceSht_lbl', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.assets_lbl = GetPhrase('assets_lbl', lang)
        self.cash_lbl = GetPhrase('cash_lbl', lang)
        self.shtTermInv_lbl = GetPhrase('shtTermInv_lbl', lang)
        self.ar_lbl = GetPhrase('ar_lbl', lang)
        self.inventory_lbl = GetPhrase('inventory_lbl', lang)
        self.totalCA_lbl = GetPhrase('totalCA_lbl', lang)
        self.ppeGrosss_lbl = GetPhrase('ppeGross_lbl', lang)
        self.accumDep_lbl = GetPhrase('accumDep_lbl', lang)
        self.ppeNet_lbl = GetPhrase('ppeNet_lbl', lang)
        self.totalAssets_lbl = GetPhrase('totalAssets_lbl', lang)
        self.liabilities_lbl = GetPhrase('liabilities_lbl', lang)
        self.ap_lbl = GetPhrase('ap_lbl', lang)
        self.stf_lbl = GetPhrase('stf_lbl', lang)
        self.LoC_lbl = GetPhrase('LoC_lbl', lang)
        self.currentLTD_lbl = GetPhrase('currentLTD_lbl', lang)
        self.totalCL_lbl = GetPhrase('totalCL_lbl', lang)
        self.ltd_lbl = GetPhrase('ltd_lbl', lang)
        self.totalLiabilities_lbl = GetPhrase('totalLiabilities_lbl', lang)
        self.equity_lbl = GetPhrase('equity_lbl', lang)
        self.commonStock_lbl = GetPhrase('commonStock_lbl', lang)
        self.share_lbl = GetPhrase('share_lbl', lang)
        self.capitalSurplus_lbl = GetPhrase('capitalSurplus_lbl', lang)
        self.retainedEarnings_lbl = GetPhrase('retainedEarnings_lbl', lang)
        self.totalEquity_lbl = GetPhrase('totalEquity_lbl', lang)
        self.totalLiabEquity_lbl = GetPhrase('totalLiabEquity_lbl', lang)
        self.shareInfo_lbl = GetPhrase('shareInfo_lbl', lang)
        self.commonSharesOut_lbl = GetPhrase('commonSharesOut_lbl', lang)
        
        # BS List Objects 
        #------------------------------------------------------------------
        self.yearList = [self.balanceSht_lbl, self.year_lbl+' 1', self.year_lbl+' 2',
                         self.year_lbl+' 3', self.year_lbl+' 4', self.year_lbl+' 5',
                         self.year_lbl+' 6']
        
        self.cash_list = ['   '+self.cash_lbl, '-', '-', '-', '-', '-', '-']
        self.shtTermInv_list = ['   '+self.shtTermInv_lbl, '-', '-', '-', '-', '-', '-']
        self.ar_list = ['   '+self.ar_lbl, '-', '-', '-', '-', '-', '-']
        self.inventory_list = ['   '+self.inventory_lbl, '-', '-', '-', '-', '-', '-']
        self.totalCA_list = [self.totalCA_lbl, '-', '-', '-', '-', '-', '-']
        self.ppeGrosss_list = ['   '+self.ppeGrosss_lbl, '-', '-', '-', '-', '-', '-']
        self.accumDep_list = ['   '+self.accumDep_lbl, '-', '-', '-', '-', '-', '-']
        self.ppeNet_list = ['   '+self.ppeNet_lbl, '-', '-', '-', '-', '-', '-']
        self.totalAssets_list = [self.totalAssets_lbl, '-', '-', '-', '-', '-', '-']
        self.ap_list = ['   '+self.ap_lbl, '-', '-', '-', '-', '-', '-']
        self.stf_list = ['   '+self.stf_lbl, '-', '-', '-', '-', '-', '-']
        self.LoC_list = ['   '+self.LoC_lbl, '-', '-', '-', '-', '-', '-']
        self.currentLTD_list = ['   '+self.currentLTD_lbl, '-', '-', '-', '-', '-', '-']
        self.totalCL_list = [self.totalCL_lbl, '-', '-', '-', '-', '-', '-']
        self.ltd_list = ['   '+self.ltd_lbl, '-', '-', '-', '-', '-', '-']
        self.totalLiabilities_list = [self.totalLiabilities_lbl, '-', '-', '-', '-', '-', '-']
        self.commonStock_list = ['   '+self.commonStock_lbl+' ($0.01 / '+self.share_lbl+')', '-', '-', '-', '-', '-', '-']
        self.capitalSurplus_list = ['   '+self.capitalSurplus_lbl, '-', '-', '-', '-', '-', '-']
        self.retainedEarnings_list = ['   '+self.retainedEarnings_lbl, '-', '-', '-', '-', '-', '-']
        self.totalEquity_list = [self.totalEquity_lbl, '-', '-', '-', '-', '-', '-']
        self.totalLiabEquity_list = [self.totalLiabEquity_lbl, '-', '-', '-', '-', '-', '-']
        self.commonSharesOut_list = [self.commonSharesOut_lbl, '-', '-', '-', '-', '-', '-']
        
        self.asset_fields = [self.cash_list, self.shtTermInv_list, self.ar_list,
                          self.inventory_list, self.totalCA_list,
                          self.ppeGrosss_list, self.accumDep_list, self.ppeNet_list,
                          self.totalAssets_list]
        
        self.liability_fields = [self.ap_list, self.stf_list, self.LoC_list, 
                               self.currentLTD_list, self.totalCL_list, 
                               self.ltd_list, self.totalLiabilities_list]
        
        self.equity_fields = [self.commonStock_list, self.capitalSurplus_list,
                          self.retainedEarnings_list, self.totalEquity_list, 
                          self.totalLiabEquity_list]
        
        
        # Formatting
        #------------------------------------------------------------------
        self.bold_list = [self.totalCA_list, self.totalAssets_list, 
                          self.totalCL_list, self.totalLiabilities_list,
                          self.totalEquity_list, self.totalLiabEquity_list]
        
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        self.balanceSht_st = wx.StaticText(self, -1, self.balanceSht_lbl)
        self.balanceSht_st.SetFont(self.styles.h1_font)
        sizer.Add(self.balanceSht_st, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.TOP, 5)
        
        self.year_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        # Asset Panels:
        self.cash_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.shtTermInv_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.ar_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.inventory_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.totalCA_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.ppeGrosss_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.accumDep_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.ppeNet_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.totalAssets_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        # Assets Panel List
        self.asset_pnls = [self.cash_pnl, self.shtTermInv_pnl, self.ar_pnl,
                          self.inventory_pnl, self.totalCA_pnl,
                          self.ppeGrosss_pnl, self.accumDep_pnl, self.ppeNet_pnl,
                          self.totalAssets_pnl]
        
        # Liability Panels:
        self.ap_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.stf_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.LoC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.currentLTD_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.totalCL_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.ltd_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.totalLiabilities_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        # Liabilities Panel List
        self.liability_pnls = [self.ap_pnl, self.stf_pnl, self.LoC_pnl, 
                               self.currentLTD_pnl, self.totalCL_pnl, 
                               self.ltd_pnl, self.totalLiabilities_pnl]
        
        # Equity Panels:
        self.commonStock_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.capitalSurplus_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.retainedEarnings_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.totalEquity_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.totalLiabEquity_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        # Equity Panel List
        self.equity_pnls = [self.commonStock_pnl, self.capitalSurplus_pnl,
                          self.retainedEarnings_pnl, self.totalEquity_pnl, 
                          self.totalLiabEquity_pnl]
        
        # Share Info Panel:
        self.commonSharesOut_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Add in the Year Panel -------------------------------------------
        self.year_pnl.Init(self.yearList)
        sizer.Add(self.year_pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        # Add in the Asset Panels -----------------------------------------
        self.asset_st = wx.StaticText(self, -1, self.assets_lbl)
        self.asset_st.SetFont(self.styles.h4_b_font)
        sizer.Add(self.asset_st, 0, wx.LEFT|wx.BOTTOM, 5)
        
        lineCount = 0
        addSL_list = (4, 8) # Indicates where to insert a static line
        for pnl, fld in zip(self.asset_pnls, self.asset_fields):
            bold = False
            if fld in self.bold_list:
                bold = True
            pnl.Init(fld, bold)
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if lineCount in addSL_list:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            if lineCount % 2 == 0:
                pnl.SetBackgroundColour(self.styles.lightGrey)
            lineCount += 1
            
        # Add in the Liability Panel --------------------------------------
        sizer.Add((-1, 10))
        self.liabilities_st = wx.StaticText(self, -1, self.liabilities_lbl)
        self.liabilities_st.SetFont(self.styles.h4_b_font)
        sizer.Add(self.liabilities_st, 0, wx.LEFT|wx.BOTTOM, 5)
        
        lineCount = 0
        addSL_list = (4, 6) # Indicates where to insert a static line
        for pnl, fld in zip(self.liability_pnls, self.liability_fields):
            
            bold = False
            if fld in self.bold_list:
                bold = True
            pnl.Init(fld, bold)
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if lineCount in addSL_list:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            if lineCount % 2 == 0:
                pnl.SetBackgroundColour(self.styles.lightGrey)
            lineCount += 1
            
        # Add in the Equity Panels ----------------------------------------
        sizer.Add((-1, 10))
        self.equity_st = wx.StaticText(self, -1, self.equity_lbl)
        self.equity_st.SetFont(self.styles.h4_b_font)
        sizer.Add(self.equity_st, 0, wx.LEFT|wx.BOTTOM, 5)
        
        lineCount = 0
        addSL_list = (3,) # Indicates where to insert a static line
        for pnl, fld in zip(self.equity_pnls, self.equity_fields):
            bold = False
            if fld in self.bold_list:
                bold = True
            pnl.Init(fld, bold)
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if lineCount in addSL_list:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            if lineCount % 2 == 0:
                pnl.SetBackgroundColour(self.styles.lightGrey)
            lineCount += 1
            
        # Add in the Share Info Panel -------------------------------------
        sizer.Add((-1, 10))
        self.shareInfo_st = wx.StaticText(self, -1, self.shareInfo_lbl)
        self.shareInfo_st.SetFont(self.styles.h4_b_font)
        sizer.Add(self.shareInfo_st, 0, wx.LEFT|wx.BOTTOM, 5)
        self.commonSharesOut_pnl.Init(self.commonSharesOut_list, italic = True)
        sizer.Add(self.commonSharesOut_pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
            
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def UpdateBS(self, bsList, year):
        '''Takes a balance sheet list from the Z_gameIO module and adds
        the values to the balance sheet in the correct column.'''
        insCol = year
        # Current Assets
        cash, sti, ar, inv = bsList[0]
        self.cash_pnl.AddVal(cash, insCol)
        self.shtTermInv_pnl.AddVal(sti, insCol)
        self.ar_pnl.AddVal(ar, insCol)
        self.inventory_pnl.AddVal(inv, insCol)
        totalCA = cash + sti + ar + inv
        self.totalCA_pnl.AddVal(totalCA, insCol)
        # Gross PPE, Accumulated Depreciation and Net PPE
        grossPPE, accumDep, netPPE = bsList[1]
        self.ppeGrosss_pnl.AddVal(grossPPE, insCol)
        self.accumDep_pnl.AddVal(-1 * accumDep, insCol)
        self.ppeNet_pnl.AddVal(netPPE, insCol)
        totalAssets = totalCA + netPPE
        self.totalAssets_pnl.AddVal(totalAssets, insCol)
        # Current Liabilities
        ap, stb, loc, cLTD = bsList[2]
        self.ap_pnl.AddVal(ap, insCol)
        self.stf_pnl.AddVal(stb, insCol)
        self.LoC_pnl.AddVal(loc, insCol)
        self.currentLTD_pnl.AddVal(cLTD, insCol)
        totalCL = ap + stb + loc + cLTD
        self.totalCL_pnl.AddVal(totalCL, insCol)
        # LTD & Total Liabilities
        ltd = bsList[3]
        self.ltd_pnl.AddVal(ltd, insCol)
        totalLiabilities = ap + stb + loc + cLTD + ltd
        self.totalLiabilities_pnl.AddVal(totalLiabilities, insCol)
        # Equity
        cs, capSurplus, re = bsList[4]
        self.commonStock_pnl.AddVal(cs, insCol)
        self.capitalSurplus_pnl.AddVal(capSurplus, insCol)
        self.retainedEarnings_pnl.AddVal(re, insCol)
        totalEquity = cs + capSurplus + re
        self.totalEquity_pnl.AddVal(totalEquity, insCol)
        totalEandL = totalLiabilities + totalEquity
        self.totalLiabEquity_pnl.AddVal(totalEandL, insCol)
        # Shares Out
        sharesOut = bsList[5]
        self.commonSharesOut_pnl.AddVal(sharesOut, insCol, isCur=False, isPerc=False)
        
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the results Balance Sheet.'''
        for pnl, fld in zip(self.asset_pnls, self.asset_fields):
            bold = False
            if fld in self.bold_list:
                bold = True
            pnl.Init(fld, bold)
            
        for pnl, fld in zip(self.liability_pnls, self.liability_fields):
            bold = False
            if fld in self.bold_list:
                bold = True
            pnl.Init(fld, bold)
            
        for pnl, fld in zip(self.equity_pnls, self.equity_fields):
            bold = False
            if fld in self.bold_list:
                bold = True
            pnl.Init(fld, bold)
            
        self.commonSharesOut_pnl.Init(self.commonSharesOut_list, italic = True)
        
    #----------------------------------------------------------------------
    def ExportBS(self):
        '''Exports the balance sheet.'''
        bs = []
        allPnls = [self.year_pnl] + self.asset_pnls + \
            self.liability_pnls + self.equity_pnls + [self.commonSharesOut_pnl]
        for p in allPnls:
            bs.append(p.ExportRow())
            
        # Insert BS Headers
        bs.insert(1, [self.assets_lbl])
        bs.insert(11, [self.liabilities_lbl])
        bs.insert(19, [self.equity_lbl])
        bs.insert(24, [])
        bs.insert(26, [])
        return bs
    