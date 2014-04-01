#!python
# -*- encoding: utf-8 -*-

# X_listbook.py

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
E_game_pnl.py -+
               |
               + X_listbook.py

This module contains the listbook class used for the Novus
Business and IT Education Program.
'''

import wx
import E_genInfo_pnl, E_results_pnl, E_decisions_pnl, E_review_pnl, E_finance_pnl
import X_utilities, X_styles
import Q_data
from Q_language import GetPhrase

ID_RSLT_PNL = wx.NewId()
ID_INFO_PNL = wx.NewId()
ID_DESC_PNL = wx.NewId()
ID_REVW_PNL = wx.NewId()
ID_FNCE_PNL = wx.NewId()

class Novus_Listbook(wx.Listbook):
    def __init__(self, parent, *args, **kwargs):
        super(Novus_Listbook, self).__init__(parent, *args, **kwargs)
        
        # Style -----------------------------------------------------------
        self.style = X_styles.NovusStyle(self)
        self.SetBackgroundColour(self.style.lightGrey)
        
        # Data -------------------------------------------------------------
        self.data = Q_data.Data(None) 
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.lastRound_lbl = GetPhrase('rslt_title', lang)
        self.genInfo_lbl = GetPhrase('genInfo_title', lang)
        self.decisions_lbl = GetPhrase('decisions_lbl', lang)
        self.review_lbl = GetPhrase('review_title', lang)
        self.finance_lbl = GetPhrase('pfFinance_title', lang)
        
        # Create Imagelist ------------------------------------------------
        image_list = wx.ImageList(64, 64)
        pics = ['Novus_Game1_64.png', 'Novus_Game5_64.png', 
                'Novus_Game2_64.png', 'Novus_Game3_64.png',
                'Novus_Game4_64.png']
        
        for p in pics:
            path = X_utilities.ImageFP(p)
            pic = wx.Image(path, type=wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            index = image_list.Add(pic)
        
        self.AssignImageList(image_list)
        
        # Create Panels and Labels ----------------------------------------
        self.result_pnl = E_results_pnl.Results_Pnl(self, ID_RSLT_PNL)
        self.genInfo_pnl = E_genInfo_pnl.GenInfo_Pnl(self, ID_INFO_PNL)
        self.decisions_pnl = E_decisions_pnl.Decisions_Pnl(self, ID_DESC_PNL)
        self.review_pnl = E_review_pnl.Review_Pnl(self, ID_REVW_PNL)
        self.finance_pnl = E_finance_pnl.Finance_Pnl(self, ID_FNCE_PNL)
        
        panelList = [(self.result_pnl, self.lastRound_lbl),
                     (self.genInfo_pnl, self.genInfo_lbl),
                     (self.decisions_pnl, self.decisions_lbl),
                     (self.review_pnl, self.review_lbl),
                     (self.finance_pnl, self.finance_lbl)]
        
        #Add Pages --------------------------------------------------------
        indexCount = 0
        for p, l in panelList:
            self.AddPage(p, l, True, indexCount)
            indexCount += 1
            
        self.SetSelection(0)
        
        # Method Calls ----------------------------------------------------
        
    #----------------------------------------------------------------------
    # Functions and Event Handlers
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the game panels according to the year provided in the
        argument.'''
        self.result_pnl.Init(year)
        self.genInfo_pnl.Init(year)
        self.decisions_pnl.Init(year)
        self.review_pnl.Init(year)
        self.finance_pnl.Init(year)
        self.SetSelection(0)
        
    #----------------------------------------------------------------------
#    def UpdateLanguage(self):
#        '''Updates the language labels for all of the game objects.'''
#        self.decisions_pnl.UpdateLanguage()
#        self.result_pnl.UpdateLanguage()
#        self.genInfo_pnl.UpdateLanguage()
#        self.review_pnl.UpdateLanguage()
#        self.finance_pnl.UpdateLanguage()