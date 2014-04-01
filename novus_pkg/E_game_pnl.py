#!python
# -*- encoding: utf-8 -*-

# E_game_pnl.py

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
                              + E_genInfo_pnl.py
                              + E_review_pnl.py
                              + E_finance_pnl.py +
                              |                  + F_incomeStmt_B_pnl.py
                              |                  + F_balanceSheet_B_pnl.py
                              |                  + F_cashFlow_B_pnl.py
                              |
                              + E_results_pnl.py +
                              |                  + F_balancedSC_A_pnl.py
                              |                  + F_incomeStmt_A_pnl.py
                              |                  + F_balanceSheet_A_pnl.py
                              |                  + F_cashFlow_A_pnl.py
                              | 
                              + E_decisions_pnl.py +
                                                   + G_equipment_pnl.py
                                                   + G_finance_pnl.py
                                                   + G_production_pnl.py
                                                   + G_hr_pnl.py
                                                   + G_other_pnl.py

This module contains the Game Panel class code for the Novus 
Business and IT education program
'''

import wx
import os
import Q_data
import X_utilities, X_styles, X_export
import Z_gameIO
from Q_language import GetPhrase

from X_listbook import *  

class Game_Pnl(wx.Panel):
    '''This class holds the List Control class that is used for playing
    the simulation game for the Novus Business and IT education program.'''
    def __init__(self, parent, *args, **kwargs):
        super(Game_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        self.gameOver = False
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.export_lbl = GetPhrase('export_lbl', lang)
        self.reset_lbl = GetPhrase('reset_lbl', lang)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Novus Banner and End State Controls -----------------------------
        a_box = wx.BoxSizer()
        
        # Banner
        path = X_utilities.ImageFP('Novus_Small.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.banner_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        a_box.Add(self.banner_bm, 0)
        a_box.Add(wx.StaticText(self, -1), 1)
        
        # Export Button
        self.export_btn = wx.Button(self, wx.ID_PRINT, self.export_lbl, size=(-1, 32))
        self.export_btn.SetBackgroundColour(self.styles.lightGreen)
        self.export_btn.SetForegroundColour(self.styles.lightGrey)
        self.export_btn.SetFont(self.styles.h3_b_font)
        a_box.Add(self.export_btn, 0, wx.RIGHT, 15)
        
        # Reset Button
        self.reset_btn = wx.Button(self, wx.ID_RESET, self.reset_lbl, size=(-1, 32))
        self.reset_btn.SetBackgroundColour(self.styles.lightGreen)
        self.reset_btn.SetForegroundColour(self.styles.lightGrey)
        self.reset_btn.SetFont(self.styles.h3_b_font)
        a_box.Add(self.reset_btn, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.BOTTOM|wx.TOP, 10)
        
        # Add in Listbook -------------------------------------------------
        self.listbook = Novus_Listbook(self, -1)
        sizer.Add(self.listbook, 1, wx.EXPAND)
        
        #--#
        self.SetSizer(sizer)
        
        #------------------------------------------------------------------
        self.TeacherModeOff()
        
        # Bindings --------------------------------------------------------
        self.listbook.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChange)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChange)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
    
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self):
        '''Sets up the game page, according to the year provided in the
        argument.'''
        self.year = self.data.GetData1()[0][1]
        if self.year < 7:
            self.listbook.Init(self.year)
            self.UpdateReview()
        else:
            self.EndState()
        
    #----------------------------------------------------------------------
    def OnPageChange(self, evt):
        '''Handles the page change event for the list book or the decisions
        notebook.'''
        if not self.gameOver:
            currentInfo = self.UpdateReview()
            self.listbook.finance_pnl.UpdateProForma(currentInfo)
            self.listbook.finance_pnl.UpdateResults(currentInfo)
        self.listbook.genInfo_pnl.SetContent()
            
    #----------------------------------------------------------------------
    def OnButton(self, evt):
        '''Passes the button event up to the Frame.'''
        evt.Skip()
    
    #----------------------------------------------------------------------
    def UpdateReview(self):
        '''Gets the current information from the decisions panel and
        sends it to the Review and Finance pages in the Game Listbook.'''
        if self.year == 1:
            self.listbook.decisions_pnl.production_pnl.Round1Setup()
        if self.year == 2:
            self.listbook.decisions_pnl.Round2Setup()
        if self.year == 3:
            self.listbook.decisions_pnl.production_pnl.Round3Setup()
        if self.year == 4:
            self.listbook.decisions_pnl.production_pnl.Round4Setup()
    
        eq = self.listbook.decisions_pnl.GetEquipInfo()
        fin = self.listbook.decisions_pnl.GetFinInfo()
        prod = self.listbook.decisions_pnl.GetProdInfo()
        hr = self.listbook.decisions_pnl.GetHRInfo()
        other = self.listbook.decisions_pnl.GetOtherInfo()
        
        # Create currentInfo list with formatting identical to that of 
        #       teamData1.csv
        currentInfo = []
        currentInfo += self.data.GetData1()[:2]
        currentInfo += eq
        currentInfo += fin
        currentInfo += prod[:5]
        currentInfo += hr
        currentInfo += prod[7:]
        currentInfo += prod[5:7]
        currentInfo += other
        if self.year < 7:
            currentInfo = self.data.CombineData1(currentInfo, self.year)
        self.listbook.review_pnl.UpdateCurrentInfo(currentInfo)
        self.listbook.decisions_pnl.production_pnl.UpdateAvailable(currentInfo)
        return currentInfo
    
    #----------------------------------------------------------------------
    def GetResults(self):
        '''Gets the team's results for the current round. This function
        takes the decision list, gets the gameIO financial results, and 
        appends them to the "Performance History" portion of the list[51:].
        Then sends the list the the self.data object to be written to the
        file. Also, updates the year in the "teamData1.csv" file and this
        "game" object. Sets the game up for the next round'''
        
        currentInfo = self.UpdateReview()
        
        results = Z_gameIO.GetFinanceOutput(currentInfo, self.year, self.ale_lbl, self.lager_lbl, mod=True)
        IncStmt, BalSheet, CashFlow, finRatio = results
        # Update the year
        currentInfo[0][1] = self.year+1
        
        # Add in the Performance History Section
        for i in range(6):
            currentInfo[51+i][self.year] = IncStmt[0][i]
        for i in range(4):
            currentInfo[57+i][self.year] = BalSheet[0][i]
        for i in range(2):
            currentInfo[61+i][self.year] = BalSheet[1][i]
        for i in range(4):
            currentInfo[63+i][self.year] = BalSheet[2][i]
        currentInfo[67][self.year] = BalSheet[3]
        currentInfo[68][self.year] = BalSheet[4][2]
        
        # Calculate and add the ending cash balance
        netIncome, depr, chRec, chInv, chPay = CashFlow[0]
        netOps = netIncome + depr + chRec + chInv + chPay
        eq, tr, ma = CashFlow[1]
        netInv = eq + tr + ma 
        chSTB, chLoC, incLTD, decLTD, incEq, divPaid = CashFlow[2]
        netFin = chSTB + chLoC + incLTD + decLTD + incEq + divPaid
        netAll = netOps + netInv + netFin
        begCB = CashFlow[3]
        endCB = begCB + netAll
        currentInfo[69][self.year] = endCB
        
        # Get the Managerial Effectiveness Score
        manEff = self.listbook.result_pnl.balancedSC_pnl.GetManager(self.year, useCurrentInfo=True, currentInfo=currentInfo)
        currentInfo[70][self.year] = int(manEff)
        return currentInfo

    #----------------------------------------------------------------------
    def Commit(self):
        '''Commits the team's decisions to the "teamData1.csv" file, 
        and updates the game panels.'''
        self.ExportForecast()
        
        finalDecList = self.GetResults()
        self.data.WriteData1(finalDecList)
        if finalDecList[0][1] < 7:
            self.Init()
        else:
            self.EndState()
            
    #----------------------------------------------------------------------
    def EndState(self):
        '''Sets the game up after the round 6 decisions are submitted.'''
        self.gameOver = True

        # Set the end state for the Results Panel.
        self.listbook.SetSelection(0)
        self.listbook.result_pnl.State1(None)
        self.listbook.result_pnl.EndState()
        
        # Set the end state for the Decisions Panel.
        self.listbook.decisions_pnl.Disable()
        self.listbook.decisions_pnl.EndState()
        
        # Set the end state for the Review Panel.
        self.listbook.review_pnl.EndState()
        
        # Set the end state for the Finance Panel.
        self.listbook.finance_pnl.Disable()
        self.listbook.finance_pnl.EndState()
        
    #----------------------------------------------------------------------
    def TeacherModeOn(self):
        '''Turns Teacher Mode On and shows the Actual results column.'''
        fin_list = [self.listbook.finance_pnl.incomeStmt_pnl,
                    self.listbook.finance_pnl.balanceSht_pnl,
                    self.listbook.finance_pnl.cashFlow_pnl]
        
        for f in fin_list:
            for p in [x for x in f.GetChildren() if x.GetClassName()=='wxPanel']:
                p.ShowActual()
    
    #----------------------------------------------------------------------
    def TeacherModeOff(self):
        '''Turns Teacher Mode Off, hiding the actual results column.'''
        fin_list = [self.listbook.finance_pnl.incomeStmt_pnl,
                    self.listbook.finance_pnl.balanceSht_pnl,
                    self.listbook.finance_pnl.cashFlow_pnl]
        
        for f in fin_list:
            for p in [x for x in f.GetChildren() if x.GetClassName()=='wxPanel']:
                p.HideActual()
    
    #----------------------------------------------------------------------
    def ExportForecast(self):
        '''When the round decisions are submitted, this exports a copy
        of the final pro forma and actual results to a spreadsheet.'''
        IS, BS, CF, FR, year = self.listbook.finance_pnl.ExportResults()
        X_export.Export(IS, BS, CF, FR, year=year)