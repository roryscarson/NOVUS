#!python
# -*- encoding: utf-8 -*-

# E_finance_pnl.py

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
E_game_pnl.py +
              + X_listbook.py +
                              + E_finance_pnl.py +
                                                 + F_incomeStmt_B_pnl.py
                                                 + F_balanceSheet_B_pnl.py
                                                 + F_cashFlow_B_pnl.py

This module contains the Finance Panel class code for the Novus 
Business and IT education program. 
'''

import wx
import F_incomeStmt_B_pnl, F_balanceSheet_B_pnl, F_cashFlow_B_pnl
import X_styles, X_utilities
import Z_gameIO
import Q_data
from Q_language import GetPhrase 

class Finance_Pnl(wx.Panel):
    '''This class holds the Finance Panel for the Novus Business 
    and IT education program. It shows both the Pro Forma reports, and,
    after the submission of decisions, the actual reports.'''
    def __init__(self, parent, *args, **kwargs):
        super(Finance_Pnl, self).__init__(parent, *args, **kwargs)
        self.styles = X_styles.NovusStyle(self)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
       
        self.financeTitle_lbl = GetPhrase('pfFinance_title', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.complete_lbl = GetPhrase('complete_lbl', lang)
        self.incomeStmt_lbl = GetPhrase('incomeStmt_lbl', lang)
        self.balanceSht_lbl = GetPhrase('balanceSht_lbl', lang)
        self.cashFlow_lbl = GetPhrase('cashFlow_lbl', lang)
        self.back_lbl = GetPhrase('back_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        a_box = wx.BoxSizer(wx.HORIZONTAL)
        path = X_utilities.ImageFP('Novus_Game4_32.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.fnce_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        self.financeTitle_st = wx.StaticText(self, -1, self.financeTitle_lbl)
        self.financeTitle_st.SetFont(self.styles.h2_font)
        self.year_st = wx.StaticText(self, -1, self.year_lbl+' - ')
        self.year_st.SetFont(self.styles.h2_font)
        self.back_btn = wx.Button(self, wx.ID_BACKWARD, self.back_lbl, size=(150, -1))
        self.back_btn.SetBackgroundColour(self.styles.lightGrey)
        self.back_btn.SetForegroundColour(self.styles.brown)
        self.back_btn.SetFont(self.styles.h3_b_font)
        a_box.Add((11, -1))
        a_box.Add(self.fnce_bm, 0, wx.RIGHT, 15)
        a_box.Add(self.financeTitle_st, 0, wx.TOP, 5)
        a_box.Add((20, -1))
        a_box.Add(wx.StaticLine(self, -1, style=wx.VERTICAL), 0, wx.EXPAND|wx.RIGHT, 20)
        a_box.Add(self.year_st, 1, wx.TOP, 5)
        a_box.Add(self.back_btn, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Button Bar ------------------------------------------------------
        b_box = wx.BoxSizer(wx.HORIZONTAL)
        self.incomeStmt_btn = wx.Button(self, -1, self.incomeStmt_lbl)
        self.balanceSht_btn = wx.Button(self, -1, self.balanceSht_lbl)
        self.cashFlow_btn = wx.Button(self, -1, self.cashFlow_lbl)
        
        btnList = [b for b in self.GetChildren() if b.GetClassName()=='wxButton']
        for b in btnList[1:]:
            b.SetBackgroundColour(self.styles.darkGreen)
            b.SetForegroundColour(self.styles.lightGrey)
            b.SetFont(self.styles.h3_b_font)
            
        b_box.Add(self.incomeStmt_btn, 0, wx.LEFT|wx.RIGHT, 10)
        b_box.Add(self.balanceSht_btn, 0, wx.RIGHT, 10)
        b_box.Add(self.cashFlow_btn, 0)
        
        sizer.Add(b_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        
        # Add Panels ------------------------------------------------------
        self.incomeStmt_pnl = F_incomeStmt_B_pnl.IncomeStmt_B_Pnl(self, -1)
        self.balanceSht_pnl = F_balanceSheet_B_pnl.BalanceSheet_B_Pnl(self, -1)
        self.cashFlow_pnl = F_cashFlow_B_pnl.CashFlow_B_Pnl(self, -1)
        
        c_box = wx.BoxSizer(wx.HORIZONTAL)
        c_box.Add(wx.StaticText(self, -1, size=(20, -1)), 0)
        c_box.Add(self.incomeStmt_pnl, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        c_box.Add(self.balanceSht_pnl, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        c_box.Add(self.cashFlow_pnl, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, 5)
        c_box.Add(wx.StaticText(self, -1, size=(20, -1)), 0)
        sizer.Add(c_box, 1, wx.EXPAND|wx.TOP, 5)
        
        self.incomeStmt_pnl.Hide()
        self.balanceSht_pnl.Hide()
        self.cashFlow_pnl.Hide()
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.incomeStmt_btn.Bind(wx.EVT_BUTTON, self.State1)
        self.balanceSht_btn.Bind(wx.EVT_BUTTON, self.State2)
        self.cashFlow_btn.Bind(wx.EVT_BUTTON, self.State4)
        self.Bind(wx.EVT_BUTTON, self.OnBack)
        
        # Function Calls --------------------------------------------------
        self.State1(None)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the game panels according to the year provided in the
        argument.'''
        self.year = year
        if self.year < 7:
            self.year_st.SetLabel(self.year_lbl + ' - ' + unicode(self.year))
        else:
            self.year_st.SetLabel(self.complete_lbl)
    
    #----------------------------------------------------------------------
    def State1(self, evt):
        '''Activates the Income Statement.'''
        # Set up panels
        self.incomeStmt_pnl.Show()
        self.balanceSht_pnl.Hide()
        self.cashFlow_pnl.Hide()
        
        # Set Button Colors
        self.incomeStmt_btn.SetBackgroundColour(self.styles.darkGreen)
        self.incomeStmt_btn.SetForegroundColour(self.styles.lightGrey)
        self.balanceSht_btn.SetBackgroundColour(self.styles.lightGrey)
        self.balanceSht_btn.SetForegroundColour(self.styles.darkGreen)
        self.cashFlow_btn.SetBackgroundColour(self.styles.lightGrey)
        self.cashFlow_btn.SetForegroundColour(self.styles.darkGreen)
        
        self.Layout()
        
    #----------------------------------------------------------------------
    def State2(self, evt):
        '''Activates the Balance Sheet.'''
        # Set up panels
        self.incomeStmt_pnl.Hide()
        self.balanceSht_pnl.Show()
        self.cashFlow_pnl.Hide()
        
        # Set Button Colors
        self.incomeStmt_btn.SetBackgroundColour(self.styles.lightGrey)
        self.incomeStmt_btn.SetForegroundColour(self.styles.darkGreen)
        self.balanceSht_btn.SetBackgroundColour(self.styles.darkGreen)
        self.balanceSht_btn.SetForegroundColour(self.styles.lightGrey)
        self.cashFlow_btn.SetBackgroundColour(self.styles.lightGrey)
        self.cashFlow_btn.SetForegroundColour(self.styles.darkGreen)
        
        self.Layout()
        
    #----------------------------------------------------------------------
    def State4(self, evt):
        '''Activates the Cash Flow Statement.'''
        # Set up panels
        self.incomeStmt_pnl.Hide()
        self.balanceSht_pnl.Hide()
        self.cashFlow_pnl.Show()
        
        # Set Button Colors
        self.incomeStmt_btn.SetBackgroundColour(self.styles.lightGrey)
        self.incomeStmt_btn.SetForegroundColour(self.styles.darkGreen)
        self.balanceSht_btn.SetBackgroundColour(self.styles.lightGrey)
        self.balanceSht_btn.SetForegroundColour(self.styles.darkGreen)
        self.cashFlow_btn.SetBackgroundColour(self.styles.darkGreen)
        self.cashFlow_btn.SetForegroundColour(self.styles.lightGrey)
        
        self.Layout()
        
    #----------------------------------------------------------------------
    def OnBack(self, evt):
        '''Handles the back button'''
        if evt.GetId() == wx.ID_BACKWARD:
            evt.Skip()
            
    #----------------------------------------------------------------------
    def UpdateProForma(self, currentInfo):
        '''Updates the Pro Forma Income Statement, Balance Sheet and 
        Cash Flow Statement.'''
        # Income Statement Part 1
        proForma = Z_gameIO.GetFinanceOutput(currentInfo, self.year, self.ale_lbl, self.lager_lbl)
        IncStmt, BalSheet, CashFlow, finRatio = proForma
        self.incomeStmt_pnl.UpdateIS(IncStmt)
        self.balanceSht_pnl.UpdateBS(BalSheet)
        self.cashFlow_pnl.UpdateCF(CashFlow)
        self.cashFlow_pnl.UpdateFR(finRatio)
        
    #-----------------------------------------------------------------------
    def UpdateResults(self, currentInfo):
        '''Updates the results for the round given the team's current
        decisions.'''
        results = Z_gameIO.GetFinanceOutput(currentInfo, self.year, self.ale_lbl, self.lager_lbl, mod=True)
        IncStmt, BalSheet, CashFlow, finRatio = results
        self.incomeStmt_pnl.UpdateIS(IncStmt, isPF=False)
        self.balanceSht_pnl.UpdateBS(BalSheet, isPF=False)
        self.cashFlow_pnl.UpdateCF(CashFlow, isPF=False)
        self.cashFlow_pnl.UpdateFR(finRatio, isPF=False)
        
    #----------------------------------------------------------------------
    def EndState(self):
        '''Sets up the End State of the game.'''
        self.year_st.SetLabel(self.complete_lbl)
        self.State1(None)
        self.incomeStmt_pnl.Hide()
        
    #----------------------------------------------------------------------
    def ExportResults(self):
        '''Scrapes the Income Statement, Balance Sheet, Cash Flows, and
        Financial Ratio panels, and then returns them as four lists.'''
        # Get All Reports
        incStmt = self.incomeStmt_pnl.ExportIS()
        balSht = self.balanceSht_pnl.ExportBS()
        cashFlow = self.cashFlow_pnl.ExportCF()
        finRatio = self.cashFlow_pnl.ExportFR()
        
        return [incStmt, balSht, cashFlow, finRatio, self.year]