#!python
# -*- encoding: utf-8 -*-

# B_yearList_pnl.py

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
The module contains the code for the Year List Panel class for the
Novus program.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import Q_data, Q_language
import X_styles

class YearList_Pnl(scrolled.ScrolledPanel):
    '''This class allows the user's to select the year for the program.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.darkGreen)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.yearSelect_lbl = Q_language.GetPhrase('yearSelect_lbl', lang)
        self.yearsComplete_lbl = Q_language.GetPhrase('yearsComplete_lbl', lang)
        self.year_lbl = Q_language.GetPhrase('year_lbl', lang)
        self.complete_lbl = Q_language.GetPhrase('complete_lbl', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #--#
        self.yearSelect_st = wx.StaticText(self, -1, self.yearSelect_lbl + ' -')
        self.yearSelect_st.SetFont(self.styles.h1_font)
        self.yearSelect_st.SetForegroundColour(self.styles.lightGrey)
        sizer.Add(self.yearSelect_st, 0, wx.LEFT|wx.TOP, 15)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        #--#
        self.yearsComplete_st = wx.StaticText(self, -1, self.yearsComplete_lbl+': ')
        self.yearsComplete_st.SetFont(self.styles.h2_font)
        self.yearsComplete_st.SetForegroundColour(self.styles.lightGrey)
        sizer.Add(self.yearsComplete_st, 0, wx.LEFT, 45)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add((-1, 10)) 
        
        #--#
        self.y1_btn = wx.Button(self, -1, label=self.year_lbl+' 1', size=(200, 50))
        self.y2_btn = wx.Button(self, -1, label=self.year_lbl+' 2', size=(200, 50))
        self.y3_btn = wx.Button(self, -1, label=self.year_lbl+' 3', size=(200, 50))
        self.y4_btn = wx.Button(self, -1, label=self.year_lbl+' 4', size=(200, 50))
        self.y5_btn = wx.Button(self, -1, label=self.year_lbl+' 5', size=(200, 50))
        self.y6_btn = wx.Button(self, -1, label=self.year_lbl+' 6', size=(200, 50))
        
        self.btnList = [b for b in self.GetChildren() if b.GetClassName()=='wxButton']
        
        for btn in self.btnList:
            btn.SetBackgroundColour(self.styles.brown)
            btn.SetForegroundColour(self.styles.lightGrey)
            btn.SetFont(self.styles.h3_b_font)
            sizer.Add(btn, 0, wx.LEFT, 40)
            sizer.Add((-1, 15))
        
        #--#
        self.SetSizer(sizer)
        self.SetupScrolling()
        
        self.SetYear()
        
    #----------------------------------------------------------------------
    def SetYear(self):
        '''Sets up the year static text to indicate the current year in the
        game.'''
        year = str(self.data.GetData1()[0][1])
        if int(year) < 7:
            self.yearsComplete_st.SetLabel(self.yearsComplete_lbl+': '+year)
        else:
            self.yearsComplete_st.SetLabel(self.complete_lbl)
