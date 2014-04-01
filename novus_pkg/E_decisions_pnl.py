#!python
# -*- encoding: utf-8 -*-

# E_decisions_pnl.py

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
                              + E_decisions_pnl.py +
                                                   + G_equipment_pnl.py
                                                   + G_finance_pnl.py
                                                   + G_production_pnl.py
                                                   + G_hr_pnl.py
                                                   + G_other_pnl.py

This module contains the Decisions Panel class code for the Novus 
Business and IT education program
'''

import wx
import G_equipment_pnl, G_finance_pnl, G_production_pnl
import G_hr_pnl, G_other_pnl
import X_styles, X_utilities
import Q_data
from Q_language import GetPhrase

class Decisions_Pnl(wx.Panel):
    '''This class holds the Decisions Panel for the Novus Business 
    and IT education program.'''
    def __init__(self, parent, *args, **kwargs):
        super(Decisions_Pnl, self).__init__(parent, *args, **kwargs)
        self.styles = X_styles.NovusStyle(self)
        
         # Attributes ------------------------------------------------------
        self.year = 0
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.descTitle_lbl = GetPhrase('decisions_lbl', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.complete_lbl = GetPhrase('complete_lbl', lang)
        self.back_lbl = GetPhrase('back_lbl', lang)
        self.equipment_lbl = GetPhrase('equipment_lbl', lang)
        self.financing_lbl = GetPhrase('financing_lbl', lang)
        self.production_lbl = GetPhrase('production_lbl', lang)
        self.product_lbl = GetPhrase('product_lbl', lang)
        self.hr_lbl = GetPhrase('hr_lbl', lang)
        self.other_lbl = GetPhrase('other_lbl', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        a_box = wx.BoxSizer(wx.HORIZONTAL)
        path = X_utilities.ImageFP('Novus_Game2_32.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.desc_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        self.descTitle_st = wx.StaticText(self, -1, self.descTitle_lbl)
        self.descTitle_st.SetFont(self.styles.h2_font)
        self.year_st = wx.StaticText(self, -1, self.year_lbl+' - ')
        self.year_st.SetFont(self.styles.h2_font)
        self.back_btn = wx.Button(self, wx.ID_BACKWARD, self.back_lbl, size=(150, -1))
        self.back_btn.SetBackgroundColour(self.styles.lightGrey)
        self.back_btn.SetForegroundColour(self.styles.brown)
        self.back_btn.SetFont(self.styles.h3_b_font)
        a_box.Add((11, -1))
        a_box.Add(self.desc_bm, 0, wx.RIGHT, 15)
        a_box.Add(self.descTitle_st, 0, wx.TOP, 5)
        a_box.Add((20, -1))
        a_box.Add(wx.StaticLine(self, -1, style=wx.VERTICAL), 0, wx.EXPAND|wx.RIGHT, 20)
        a_box.Add(self.year_st, 1, wx.TOP, 5)
        a_box.Add(self.back_btn, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Notebook --------------------------------------------------------
        self.notebook = wx.Notebook(self, -1)
        
        # Manufacturing Equipment Purchasing Panels -----------------------
        self.equipment_pnl = G_equipment_pnl.Equipment_Pnl(self.notebook, -1)
        self.notebook.AddPage(self.equipment_pnl, self.equipment_lbl)
        
        # Finance Panel ---------------------------------------------------
        self.finance_pnl = G_finance_pnl.Finance_Pnl(self.notebook)
        self.notebook.AddPage(self.finance_pnl, self.financing_lbl)
        
        # Production Panel ------------------------------------------------
        self.production_pnl = G_production_pnl.Production_Pnl(self.notebook)
        self.notebook.AddPage(self.production_pnl, self.production_lbl)
        
        # Human Resources Panel -------------------------------------------
        self.hr_pnl = G_hr_pnl.HR_Pnl(self.notebook)
        self.notebook.AddPage(self.hr_pnl, self.hr_lbl)
        
        # Other Spending Panel --------------------------------------------
        self.other_pnl = G_other_pnl.Other_Pnl(self.notebook)
        self.notebook.AddPage(self.other_pnl, self.other_lbl)
        
        sizer.Add(self.notebook, 1, wx.EXPAND)
        
        #--#
        self.SetSizer(sizer)
        
        # Event Handlers --------------------------------------------------
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChange)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the game panels according to the year provided in the
        argument.'''
        self.year = year
        self.year_st.SetLabel(self.year_lbl + ' - ' + unicode(self.year))
        self.equipment_pnl.Init(self.year)
        self.finance_pnl.Init(self.year)
        self.production_pnl.Init(self.year)
        self.hr_pnl.Init(self.year)
        self.other_pnl.Init(self.year)
            
    #----------------------------------------------------------------------
    def OnPageChange(self, evt):
        if self.notebook.GetCurrentPage() == self.other_pnl:
            fcastRev = self.production_pnl.GetRevenue()
            self.other_pnl.UpdateFcast(fcastRev)
        elif self.notebook.GetCurrentPage() == self.finance_pnl and self.year in (1, 4):
            manu_exp, pack_exp = self.equipment_pnl.GetCapExp()
            self.finance_pnl.SetCapExp(manu_exp, pack_exp)
        evt.Skip()
        
    #----------------------------------------------------------------------
    def GetEquipInfo(self):
        '''Gets the updated decisions for the Capital Equipment Purchasing
        and returns them as a list.'''
        return self.equipment_pnl.ReturnInfo()
        
    #----------------------------------------------------------------------
    def GetFinInfo(self):
        '''Gets the updated Finance decisions and returns them as a list.'''
        return self.finance_pnl.ReturnInfo()
        
    #----------------------------------------------------------------------
    def GetProdInfo(self):
        '''Gets the updated Production decisions and returns them as
        a list.'''
        return self.production_pnl.ReturnInfo()
        
    #----------------------------------------------------------------------
    def GetHRInfo(self):
        '''Gets the updated HR decisions and returns them as a list.'''
        return self.hr_pnl.ReturnInfo()
        
    #----------------------------------------------------------------------
    def GetOtherInfo(self):
        '''Gets the updated Other Spending Info and returns it as a list.'''
        return self.other_pnl.ReturnInfo()
        
    #----------------------------------------------------------------------
    def Round2Setup(self):
        '''Sets up the HR decisions for round 2.'''
        fcastRev = self.production_pnl.GetRevenue()
        cycles = self.production_pnl.GetCycles()
        self.hr_pnl.Round2HRSetup(fcastRev, cycles[0], cycles[1])
        self.production_pnl.Round2Setup()
        
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the game.'''
        self.equipment_pnl.Reset()
        self.production_pnl.Reset()
        
    #----------------------------------------------------------------------
    def EndState(self):
        '''Sets up the End State of the game.'''
        self.year_st.SetLabel(self.complete_lbl)
        self.notebook.SetSelection(0)
        
