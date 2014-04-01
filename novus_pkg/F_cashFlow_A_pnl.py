#!python
# -*- encoding: utf-8 -*-

# F_cashFlow_A_pnl.py

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

This module contains the Cash Flow Statement "A" Panel class code for the Novus 
Business and IT education program. The "A" panel show the 
results for every year, up to the present year provided to the "Init"
function.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import X_styles, X_miscPnls
import Q_data
from Q_language import GetPhrase

class CashFlow_A_Pnl(scrolled.ScrolledPanel):
    '''This class holds the Cash Flow Statement panel for the Novus 
    Business and IT education program.'''
    def __init__(self, parent, *args, **kwargs):
        scrolled.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        self.SetBackgroundColour(wx.WHITE)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels
        #------------------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.cashFlowAndRatio_lbl = GetPhrase('cashFlow_lbl', lang) + ' / ' + GetPhrase('financialRatios_lbl', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        
        # Cash Flow Labels ------------------------------------------------
        self.cashFlowStmt_lbl = GetPhrase('cashFlow_lbl', lang)
        self.opActivities_lbl = GetPhrase('opActivities_lbl', lang)
        self.netIncome_lbl = GetPhrase('netIncome_lbl', lang)
        self.depreciation_lbl = GetPhrase('depreciation_lbl', lang)
        self.chgInAR_lbl = GetPhrase('chgInAR_lbl', lang)
        self.chgInInv_lbl = GetPhrase('chgInInv_lbl', lang)
        self.chgInAP_lbl = GetPhrase('chgInAP_lbl', lang)
        self.NetCashFlowOps_lbl = GetPhrase('NetCashFlowOps_lbl', lang)
        self.investingActivities_lbl = GetPhrase('investingActivities_lbl', lang)
        self.capExp_lbl = GetPhrase('capExp_lbl', lang)
        self.addGFA_lbl = GetPhrase('addGFA_lbl', lang)
        self.addTrucks_lbl = GetPhrase('addTrucks_lbl', lang)
        self.addMach_lbl = GetPhrase('addMach_lbl', lang)
        self.netCashFlowInv_lbl = GetPhrase('netCashFlowInv_lbl', lang)
        self.FinancingActivities_lbl = GetPhrase('FinancingActivities_lbl', lang)
        self.chgShortTermFin_lbl = GetPhrase('chgShortTermFin_lbl', lang)
        self.chgShortTermLoC_lbl = GetPhrase('chgShortTermLoC_lbl', lang)
        self.incLTD_lbl = GetPhrase('incLTD_lbl', lang)
        self.decLTD_lbl = GetPhrase('decLTD_lbl', lang)
        self.proceedsFromStock_lbl = GetPhrase('proceedsFromStock_lbl', lang)
        self.cashDivPaid_lbl = GetPhrase('cashDivPaid_lbl', lang)
        self.netCashFlowFin_lbl = GetPhrase('netCashFlowFin_lbl', lang)
        self.netCashFlowAll_lbl = GetPhrase('netCashFlowAll_lbl', lang)
        self.begCashBal_lbl = GetPhrase('begCashBal_lbl', lang)
        self.endCashBal_lbl = GetPhrase('endCashBal_lbl', lang)
        
        # Ratio Labels ----------------------------------------------------
        self.financialRatios_lbl = GetPhrase('financialRatios_lbl', lang)
        self.y2yGrowth_lbl = GetPhrase('y2yGrowth_lbl', lang)
        self.grossMargin_lbl = GetPhrase('grossMargin_lbl', lang)
        self.SGAofSales_lbl = GetPhrase('SGAofSales_lbl', lang)
        self.EBITDAOpMarg_lbl = GetPhrase('EBITDAOpMarg_lbl', lang)
        self.EBITOpMarg_lbl = GetPhrase('EBITOpMarg_lbl', lang)
        self.taxRate_lbl = GetPhrase('taxRate_lbl', lang)
        self.netProfMarg_lbl = GetPhrase('netProfMarg_lbl', lang)
        self.currentRatio_lbl = GetPhrase('currentRatio_lbl', lang)
        self.quickRatio_lbl = GetPhrase('quickRatio_lbl', lang)
        self.cashRatio_lbl = GetPhrase('cashRatio_lbl', lang)
        self.daysInvOut_lbl = GetPhrase('daysInvOut_lbl', lang)
        self.daysSalesOut_lbl = GetPhrase('daysSalesOut_lbl', lang)
        self.daysPayablesOut_lbl = GetPhrase('daysPayablesOut_lbl', lang)
        self.ccc_lbl = GetPhrase('ccc_lbl', lang)
        self.roa_lbl = GetPhrase('RoA_lbl', lang)
        self.roe_lbl = GetPhrase('RoE_lbl', lang)
        self.roi_lbl = GetPhrase('roi_lbl', lang)
        self.estIR_lbl = GetPhrase('estIR_lbl', lang)
        self.debtEquity_lbl = GetPhrase('debtEquity_lbl', lang)
        self.ebitdaToIntExp_lbl = GetPhrase('timesInt_lbl', lang)
        
        # Cash Flow List Objects 
        #------------------------------------------------------------------
        self.opActivities_list = [self.opActivities_lbl, '', '', '', '', '', '']
        self.netIncome_list = ['   '+self.netIncome_lbl, '-', '-', '-', '-', '-', '-']
        self.depreciation_list = ['   ( + )'+self.depreciation_lbl, '-', '-', '-', '-', '-', '-']
        self.chgInAR_list = ['   (+/-)'+self.chgInAR_lbl, '-', '-', '-', '-', '-', '-']
        self.chgInInv_list = ['   (+/-)'+self.chgInInv_lbl, '-', '-', '-', '-', '-', '-']
        self.chgInAP_list = ['   (+/-)'+self.chgInAP_lbl, '-', '-', '-', '-', '-', '-']
        self.NetCashFlowOps_list = [self.NetCashFlowOps_lbl, '-', '-', '-', '-', '-', '-']
        self.investingActivities_list = [self.investingActivities_lbl, '', '', '', '', '', '']
        self.addGFA_list = ['   '+self.capExp_lbl+' - '+self.addGFA_lbl, '-', '-', '-', '-', '-', '-']
        self.addTrucks_list = ['   '+self.capExp_lbl+' - '+self.addTrucks_lbl, '-', '-', '-', '-', '-', '-']
        self.addMach_list = ['   '+self.capExp_lbl+' - '+self.addMach_lbl, '-', '-', '-', '-', '-', '-']
        self.netCashFlowInv_list = [self.netCashFlowInv_lbl, '-', '-', '-', '-', '-', '-']
        self.FinancingActivities_list = [self.FinancingActivities_lbl, '', '', '', '', '', '']
        self.chgShortTermFin_list = ['   '+self.chgShortTermFin_lbl, '-', '-', '-', '-', '-', '-']
        self.chgShortTermLoC_list = ['   '+self.chgShortTermLoC_lbl, '-', '-', '-', '-', '-', '-']
        self.incLTD_list = ['   '+self.incLTD_lbl, '-', '-', '-', '-', '-', '-']
        self.decLTD_list = ['   '+self.decLTD_lbl, '-', '-', '-', '-', '-', '-']
        self.proceedsFromStock_list = ['   '+self.proceedsFromStock_lbl, '-', '-', '-', '-', '-', '-']
        self.cashDivPaid_list = ['   '+self.cashDivPaid_lbl, '-', '-', '-', '-', '-', '-']
        self.netCashFlowFin_list = [self.netCashFlowFin_lbl, '-', '-', '-', '-', '-', '-']
        self.netCashFlowAll_list = [self.netCashFlowAll_lbl, '-', '-', '-', '-', '-', '-']
        self.begCashBal_list = [self.begCashBal_lbl, '-', '-', '-', '-', '-', '-']
        self.endCashBal_list = [self.endCashBal_lbl, '-', '-', '-', '-', '-', '-']
        
        self.cf_fields = [self.opActivities_list, self.netIncome_list, self.depreciation_list,
                          self.chgInAR_list, self.chgInInv_list, self.chgInAP_list, 
                          self.NetCashFlowOps_list, self.investingActivities_list, 
                          self.addGFA_list, self.addTrucks_list, self.addMach_list, 
                          self.netCashFlowInv_list, self.FinancingActivities_list, 
                          self.chgShortTermFin_list, self.chgShortTermLoC_list, 
                          self.incLTD_list, self.decLTD_list, self.proceedsFromStock_list, 
                          self.cashDivPaid_list, self.netCashFlowFin_list, self.netCashFlowAll_list, 
                          self.begCashBal_list, self.endCashBal_list]
        
        # Financial Ratio List Objects
        #------------------------------------------------------------------
        self.y2yGrowth_list = [self.y2yGrowth_lbl, '-', '-', '-', '-', '-', '-']
        self.grossMargin_list = [self.grossMargin_lbl, '-', '-', '-', '-', '-', '-']
        self.SGAofSales_list = [self.SGAofSales_lbl, '-', '-', '-', '-', '-', '-']
        self.EBITDAOpMarg_list = [self.EBITDAOpMarg_lbl, '-', '-', '-', '-', '-', '-']
        self.EBITOpMarg_list = [self.EBITOpMarg_lbl, '-', '-', '-', '-', '-', '-']
        self.taxRate_list = [self.taxRate_lbl, '-', '-', '-', '-', '-', '-']
        self.netProfMarg_list = [self.netProfMarg_lbl, '-', '-', '-', '-', '-', '-']
        self.currentRatio_list = [self.currentRatio_lbl, '-', '-', '-', '-', '-', '-']
        self.quickRatio_list = [self.quickRatio_lbl, '-', '-', '-', '-', '-', '-']
        self.cashRatio_list = [self.cashRatio_lbl, '-', '-', '-', '-', '-', '-']
        self.daysInvOut_list = [self.daysInvOut_lbl, '-', '-', '-', '-', '-', '-']
        self.daysSalesOut_list = [self.daysSalesOut_lbl, '-', '-', '-', '-', '-', '-']
        self.daysPayablesOut_list = [self.daysPayablesOut_lbl, '-', '-', '-', '-', '-', '-']
        self.ccc_list = [self.ccc_lbl, '-', '-', '-', '-', '-', '-']
        self.roa_list = [self.roa_lbl, '-', '-', '-', '-', '-', '-']
        self.roe_list = [self.roe_lbl, '-', '-', '-', '-', '-', '-']
        self.roi_list = [self.roi_lbl, '-', '-', '-', '-', '-', '-']
        self.estIR_list = [self.estIR_lbl, '-', '-', '-', '-', '-', '-']
        self.debtEquity_list = [self.debtEquity_lbl, '-', '-', '-', '-', '-', '-']
        self.ebitdaToIntExp_list = [self.ebitdaToIntExp_lbl, '-', '-', '-', '-', '-', '-']
        
        self.fr_fields = [self.y2yGrowth_list, self.grossMargin_list, self.SGAofSales_list, 
                          self.EBITDAOpMarg_list, self.EBITOpMarg_list, self.taxRate_list, 
                          self.netProfMarg_list, self.currentRatio_list, self.quickRatio_list, 
                          self.cashRatio_list, 
                          self.daysInvOut_list, self.daysSalesOut_list, self.daysPayablesOut_list, 
                          self.ccc_list, self.roa_list, self.roe_list, 
                          self.roi_list, self.estIR_list, self.debtEquity_list,
                          self.ebitdaToIntExp_list]
        
        # Formatting ------------------------------------------------------
        self.bold_list = [self.opActivities_list, self.NetCashFlowOps_list,
                     self.investingActivities_list, self.netCashFlowInv_list,
                     self.FinancingActivities_list, self.netCashFlowFin_list,
                     self.netCashFlowAll_list, self.begCashBal_list,
                     self.endCashBal_list]
        
        self.italic_list = []
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        self.cashFlowAndRatio_st = wx.StaticText(self, -1, self.cashFlowAndRatio_lbl)
        self.cashFlowAndRatio_st.SetFont(self.styles.h1_font)
        sizer.Add(self.cashFlowAndRatio_st, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        
        # Cash Flow Panels ------------------------------------------------
        self.opActivities_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.netIncome_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.depreciation_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.chgInAR_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.chgInInv_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.chgInAP_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.NetCashFlowOps_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.investingActivities_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.addGFA_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.addTrucks_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.addMach_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.netCashFlowInv_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.FinancingActivities_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.chgShortTermFin_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.chgShortTermLoC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.incLTD_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.decLTD_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.proceedsFromStock_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.cashDivPaid_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.netCashFlowFin_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.netCashFlowAll_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.begCashBal_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.endCashBal_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        
        self.cf_pnls = [self.opActivities_pnl, self.netIncome_pnl, self.depreciation_pnl,
                          self.chgInAR_pnl, self.chgInInv_pnl, self.chgInAP_pnl, 
                          self.NetCashFlowOps_pnl, self.investingActivities_pnl, 
                          self.addGFA_pnl, self.addTrucks_pnl, self.addMach_pnl, 
                          self.netCashFlowInv_pnl , self.FinancingActivities_pnl, 
                          self.chgShortTermFin_pnl, self.chgShortTermLoC_pnl, 
                          self.incLTD_pnl, self.decLTD_pnl, self.proceedsFromStock_pnl, 
                          self.cashDivPaid_pnl, self.netCashFlowFin_pnl , self.netCashFlowAll_pnl, 
                          self.begCashBal_pnl, self.endCashBal_pnl]
        
        # Financial Ratio Panels ------------------------------------------
        self.y2yGrowth_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.grossMargin_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.SGAofSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.EBITDAOpMarg_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.EBITOpMarg_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.taxRate_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.netProfMarg_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.currentRatio_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.quickRatio_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.cashRatio_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.daysInvOut_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.daysSalesOut_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.daysPayablesOut_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.ccc_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.roa_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.roe_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.roi_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.estIR_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        self.debtEquity_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.ebitdaToIntExp_pnl = X_miscPnls.Report1_Row_Pnl(self, -1) 
        
        self.fr_pnls = [self.y2yGrowth_pnl , self.grossMargin_pnl , self.SGAofSales_pnl , 
                          self.EBITDAOpMarg_pnl , self.EBITOpMarg_pnl , self.taxRate_pnl , 
                          self.netProfMarg_pnl , self.currentRatio_pnl , self.quickRatio_pnl , 
                          self.cashRatio_pnl, 
                          self.daysInvOut_pnl , self.daysSalesOut_pnl , self.daysPayablesOut_pnl , 
                          self.ccc_pnl , self.roa_pnl , self.roe_pnl , 
                          self.roi_pnl , self.estIR_pnl , self.debtEquity_pnl,
                          self.ebitdaToIntExp_pnl]
        
        # Add Cash Flow Panels to Sizer -----------------------------------
        self.cashFlowStmt_list = [self.cashFlowStmt_lbl, self.year_lbl+' 1', self.year_lbl+' 2',
                         self.year_lbl+' 3', self.year_lbl+' 4', self.year_lbl+' 5',
                         self.year_lbl+' 6']
        self.cashFlowStmt_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.cashFlowStmt_pnl.Init(self.cashFlowStmt_list)
        sizer.Add(self.cashFlowStmt_pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        lineCount = 0
        addSL_list = (6, 11, 19, 22) # Indicates where to insert a static line
        for pnl, fld in zip(self.cf_pnls, self.cf_fields):
            bold, italic = False, False
            if fld in self.bold_list:
                bold = True
            if fld in self.italic_list:
                italic = True
            pnl.Init(fld, bold, italic)
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if lineCount in addSL_list:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            if lineCount % 2 == 0:
                pnl.SetBackgroundColour(self.styles.lightGrey)
            if lineCount == 20:
                sizer.Add((-1, 10))
            lineCount += 1
            
        # Add Financial Ratios --------------------------------------------
        sizer.Add((-1, 20))
        self.financialRatios_list = [self.financialRatios_lbl, self.year_lbl+' 1', self.year_lbl+' 2',
                         self.year_lbl+' 3', self.year_lbl+' 4', self.year_lbl+' 5',
                         self.year_lbl+' 6']
        self.financialRatios_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.financialRatios_pnl.Init(self.financialRatios_list)
        sizer.Add(self.financialRatios_pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        
        lineCount = 0
        for pnl, fld in zip(self.fr_pnls, self.fr_fields):
            bold, italic = False, False
            if fld in self.bold_list:
                bold = True
            if fld in self.italic_list:
                italic = True
            pnl.Init(fld, bold, italic)
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if lineCount % 2 == 0:
                pnl.SetBackgroundColour(self.styles.lightGrey)
                
            lineCount += 1
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def UpdateCF(self, cfList, year):
        '''Adds values to the Cash Flow statement.'''
        insCol = year
        # Net Cash Flows from Operations Activities
        netIncome, depr, chRec, chInv, chPay = cfList[0]
        self.netIncome_pnl.AddVal(netIncome, insCol)
        self.depreciation_pnl.AddVal(depr, insCol)
        self.chgInAR_pnl.AddVal(chRec, insCol)
        self.chgInInv_pnl.AddVal(chInv, insCol)
        self.chgInAP_pnl.AddVal(chPay, insCol)
        netOps = netIncome + depr + chRec + chInv + chPay
        self.NetCashFlowOps_pnl.AddVal(netOps, insCol)
        # Net Cash Flows from Investing Activities
        eq, tr, ma = cfList[1]
        self.addGFA_pnl.AddVal(eq, insCol)
        self.addTrucks_pnl.AddVal(tr, insCol)
        self.addMach_pnl.AddVal(ma, insCol)
        netInv = eq + tr + ma 
        self.netCashFlowInv_pnl.AddVal(netInv, insCol)
        # Net Cash Flows from Financing Activities
        chSTB, chLoC, incLTD, decLTD, incEq, divPaid = cfList[2]
        self.chgShortTermFin_pnl.AddVal(chSTB, insCol)
        self.chgShortTermLoC_pnl.AddVal(chLoC, insCol)
        self.incLTD_pnl.AddVal(incLTD, insCol)
        self.decLTD_pnl.AddVal(decLTD, insCol)
        self.proceedsFromStock_pnl.AddVal(incEq, insCol)
        self.cashDivPaid_pnl.AddVal(divPaid, insCol)
        netFin = chSTB + chLoC + incLTD + decLTD + incEq + divPaid
        self.netCashFlowFin_pnl.AddVal(netFin, insCol)
        netAll = netOps + netInv + netFin
        self.netCashFlowAll_pnl.AddVal(netAll, insCol)
        # Beginning and ending cash balance
        begCB = cfList[3]
        endCB = begCB + netAll
        self.begCashBal_pnl.AddVal(begCB, insCol)
        self.endCashBal_pnl.AddVal(endCB, insCol)   
        
    #----------------------------------------------------------------------
    def UpdateFR(self, frList, year):
        '''Adds the financial ratios to the cash flow / ratio panel.'''
        insCol = year
        self.y2yGrowth_pnl.AddVal(frList[0], insCol, isCur=False, isPerc=True)
        self.grossMargin_pnl.AddVal(frList[1], insCol, isCur=False, isPerc=True)
        self.SGAofSales_pnl.AddVal(frList[2], insCol, isCur=False, isPerc=True)
        self.EBITDAOpMarg_pnl.AddVal(frList[3], insCol, isCur=False, isPerc=True)
        self.EBITOpMarg_pnl.AddVal(frList[4], insCol, isCur=False, isPerc=True)
        self.taxRate_pnl.AddVal(frList[5], insCol, isCur=False, isPerc=True)
        self.netProfMarg_pnl.AddVal(frList[6], insCol, isCur=False, isPerc=True)
        self.currentRatio_pnl.AddFloat(frList[7], insCol)
        self.quickRatio_pnl.AddFloat(frList[8], insCol)
        self.cashRatio_pnl.AddFloat(frList[9], insCol)
        self.daysInvOut_pnl.AddFloat(frList[10], insCol)
        self.daysSalesOut_pnl.AddFloat(frList[11], insCol)
        self.daysPayablesOut_pnl.AddFloat(frList[12], insCol)
        self.ccc_pnl.AddFloat(frList[13], insCol)
        self.roa_pnl.AddFloat(frList[14], insCol)
        self.roe_pnl.AddFloat(frList[15], insCol)
        self.roi_pnl.AddFloat(frList[16], insCol)
        self.estIR_pnl.AddVal(frList[17], insCol, isCur=False, isPerc=True)
        self.debtEquity_pnl.AddFloat(frList[18], insCol)
        self.ebitdaToIntExp_pnl.AddFloat(frList[19], insCol)
        
        self.Scroll(0, 0)
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the result Cash Flow statement and Financial ratios.'''
        for pnl, fld in zip(self.cf_pnls, self.cf_fields):
            bold, italic = False, False
            if fld in self.bold_list:
                bold = True
            if fld in self.italic_list:
                italic = True
            pnl.Init(fld, bold, italic)
            
        for pnl, fld in zip(self.fr_pnls, self.fr_fields):
            bold, italic = False, False
            if fld in self.bold_list:
                bold = True
            if fld in self.italic_list:
                italic = True
            pnl.Init(fld, bold, italic)
            
    #----------------------------------------------------------------------
    def ExportCF(self):
        '''Exports the statement of cash flows'''
        cf = []
        for p in [self.cashFlowStmt_pnl]+self.cf_pnls:
            cf.append(p.ExportRow())
        return cf
    
    #----------------------------------------------------------------------
    def ExportFR(self):
        '''Exports the financial ratios.'''
        fr = []
        for p in [self.financialRatios_pnl]+self.fr_pnls:
            fr.append(p.ExportRow())
        return fr
        