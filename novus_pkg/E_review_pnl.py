#!python
# -*- encoding: utf-8 -*-

# E_review_pnl.py

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
                              + E_review_pnl.py

This module contains the Review Panel class code for the Novus 
Business and IT education program
'''

import wx
import wx.lib.scrolledpanel as scrolled
import Q_data
import X_styles, X_utilities
from Q_language import GetPhrase

#--------------------------------------------------------------------------
# DECISION ITEM PANEL
#--------------------------------------------------------------------------

class Decision_Pnl(wx.Panel):
    '''This class holds a small panel that shows the name of a decision
    and the decision's value.'''
    def __init__(self, parent, *args, **kwargs):
        super(Decision_Pnl, self).__init__(parent, *args, **kwargs)
    
        self.style = X_styles.NovusStyle(None)
        self.SetBackgroundColour(wx.WHITE)
        
        sizer = wx.BoxSizer()
        
        self.decName_st = wx.StaticText(self, -1, '')
        self.decValue_st = wx.StaticText(self, -1, '')
        self.decName_st.SetFont(self.style.h4_font)
        self.decValue_st.SetFont(self.style.h4_font)
        sizer.Add(self.decName_st, 2, wx.LEFT, 10)
        sizer.Add(self.decValue_st, 1)
        
        self.SetSizer(sizer)
     
    #----------------------------------------------------------------------    
    def SetName(self, name):
        '''Gives the decision panel a name'''
        self.decName_st.SetLabel(name)
    
    #----------------------------------------------------------------------     
    def SetValue(self, value):
        '''Gives the decision panel a value.'''
        self.decValue_st.SetLabel(value)
        
    #----------------------------------------------------------------------
    def BoldFont(self, boldFont=False):
        '''If the tag is sent to True, then this function switches the 
        static text fonts to bold.'''
        if boldFont:
            self.decName_st.SetFont(self.style.h4_b_font)
            self.decValue_st.SetFont(self.style.h4_b_font)
            self.decName_st.SetBackgroundColour(self.style.lightGrey)
            self.decValue_st.SetBackgroundColour(self.style.lightGrey)
        else:
            self.decName_st.SetFont(self.style.h4_font)
            self.decValue_st.SetFont(self.style.h4_font)
            self.decName_st.SetBackgroundColour(wx.WHITE)
            self.decValue_st.SetBackgroundColour(wx.WHITE)
  
#--------------------------------------------------------------------------
# PURCHASED MACHINES PANEL
#--------------------------------------------------------------------------  
                 
class Machines_Pnl(wx.Panel):
    '''Shows the manufacturing and packaging machines purchased
    during rounds 1 and 4.'''
    def __init__(self, parent, *args, **kwargs):
        super(Machines_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        self.currentInfo = []
        
        # Styles ----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.prodMach_lbl = GetPhrase('prodMach_lbl', lang)
        self.packMach_lbl = GetPhrase('packMach_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.keg_lbl = GetPhrase('keg_lbl', lang)
        self.bottle_lbl = GetPhrase('bottle_lbl', lang)
        self.can_lbl = GetPhrase('can_lbl', lang)
        self.purchased_lbl = GetPhrase('purchased_lbl', lang)
        self.notPurchased_lbl = GetPhrase('notPurchased_lbl', lang)
        self.fgSpace_lbl = GetPhrase('fgSpace_lbl', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Production Machines ---------------------------------------------
        box1 = wx.BoxSizer()
        self.mach1_st = wx.StaticText(self, -1, self.prodMach_lbl + ' 1')
        self.mach1Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box1.Add(self.mach1_st, 2, wx.LEFT, 10)
        box1.Add(self.mach1Buy_st, 1)
        sizer.Add(box1, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        box2 = wx.BoxSizer()
        self.mach2_st = wx.StaticText(self, -1, self.prodMach_lbl + ' 2')
        self.mach2Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box2.Add(self.mach2_st, 2, wx.LEFT, 10)
        box2.Add(self.mach2Buy_st, 1)
        sizer.Add(box2, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        box3 = wx.BoxSizer()
        self.mach3_st = wx.StaticText(self, -1, self.prodMach_lbl + ' 3')
        self.mach3Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box3.Add(self.mach3_st, 2, wx.LEFT, 10)
        box3.Add(self.mach3Buy_st, 1)
        sizer.Add(box3, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        box4 = wx.BoxSizer()
        self.mach4_st = wx.StaticText(self, -1, self.prodMach_lbl + ' 4')
        self.mach4Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box4.Add(self.mach4_st, 2, wx.LEFT, 10)
        box4.Add(self.mach4Buy_st, 1)
        sizer.Add(box4, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        box5 = wx.BoxSizer()
        self.mach5_st = wx.StaticText(self, -1, self.prodMach_lbl + ' 5')
        self.mach5Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box5.Add(self.mach5_st, 2, wx.LEFT, 10)
        box5.Add(self.mach5Buy_st, 1)
        sizer.Add(box5, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        # Packaging Machines ----------------------------------------------
        box6 = wx.BoxSizer()
        self.mach6_st = wx.StaticText(self, -1, self.packMach_lbl + ' - ' + self.keg_lbl)
        self.mach6Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box6.Add(self.mach6_st, 2, wx.LEFT, 10)
        box6.Add(self.mach6Buy_st, 1)
        sizer.Add(box6, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        box7 = wx.BoxSizer()
        self.mach7_st = wx.StaticText(self, -1, self.packMach_lbl + ' - ' + self.bottle_lbl)
        self.mach7Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box7.Add(self.mach7_st, 2, wx.LEFT, 10)
        box7.Add(self.mach7Buy_st, 1)
        sizer.Add(box7, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        box8 = wx.BoxSizer()
        self.mach8_st = wx.StaticText(self, -1, self.packMach_lbl + ' - ' + self.can_lbl)
        self.mach8Buy_st = wx.StaticText(self, -1, self.notPurchased_lbl)
        box8.Add(self.mach8_st, 2, wx.LEFT, 10)
        box8.Add(self.mach8Buy_st, 1)
        sizer.Add(box8, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        # Floor Space -----------------------------------------------------
        box9 = wx.BoxSizer()
        self.fgSpace_st = wx.StaticText(self, -1, self.fgSpace_lbl)
        self.fgSpacePerc_st = wx.StaticText(self, -1, '0 %')
        box9.Add(self.fgSpace_st, 2, wx.LEFT, 10)
        box9.Add(self.fgSpacePerc_st, 1)
        sizer.Add(box9, 0, wx.EXPAND|wx.BOTTOM, 5)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        #--#
        self.SetSizer(sizer)
        
        # Set all static text objects to the right font -------------------
        stObjList = [o for o in self.GetChildren() if o.GetClassName() == 'wxStaticText']
        for obj in stObjList:
            obj.SetFont(self.style.h4_font)
            
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets the self.year attribute the current year in the game.'''
        self.year = year
        
    #----------------------------------------------------------------------        
    def SetMachValues(self, year):
        '''Get the current machine / storage decisions and set
        them to the fields.'''
        if self.currentInfo and self.year == year:
            table = self.currentInfo
        else:
            table = self.data.GetData1()
        # Manufacturing Machines
        mCol = 1 if year < 4 else 2
        if table[2][mCol]:
            self.mach1_st.SetLabel(self.mach1_st.GetLabel().split('-')[0].strip() + ' - ' + self.GetBeerLabel(table[2][3]))
            self.mach1Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach1_st.SetLabel(self.prodMach_lbl + ' 1')
            self.mach1Buy_st.SetLabel(self.notPurchased_lbl)
        
        if table[3][mCol]:
            self.mach2_st.SetLabel(self.mach2_st.GetLabel().split('-')[0].strip() + ' - ' + self.GetBeerLabel(table[3][3]))
            self.mach2Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach2_st.SetLabel(self.prodMach_lbl + ' 2')
            self.mach2Buy_st.SetLabel(self.notPurchased_lbl)
        
        if table[4][mCol]:
            self.mach3_st.SetLabel(self.mach3_st.GetLabel().split('-')[0].strip() + ' - ' + self.GetBeerLabel(table[4][3]))
            self.mach3Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach3_st.SetLabel(self.prodMach_lbl + ' 3')
            self.mach3Buy_st.SetLabel(self.notPurchased_lbl)
        
        if table[5][mCol]:
            self.mach4_st.SetLabel(self.mach4_st.GetLabel().split('-')[0].strip() + ' - ' + self.GetBeerLabel(table[5][3]))
            self.mach4Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach4_st.SetLabel(self.prodMach_lbl + ' 4')
            self.mach4Buy_st.SetLabel(self.notPurchased_lbl)
        
        if table[6][mCol]:
            self.mach5_st.SetLabel(self.mach5_st.GetLabel().split('-')[0].strip() + ' - ' + self.GetBeerLabel(table[6][3]))
            self.mach5Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach5_st.SetLabel(self.prodMach_lbl + ' 5')
            self.mach5Buy_st.SetLabel(self.notPurchased_lbl)
            
        # Packaging Machines
        self.mach6_st.SetLabel(self.packMach_lbl + ' - ' + self.keg_lbl)
        if table[7][mCol]:
            self.mach6Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach6Buy_st.SetLabel(self.notPurchased_lbl)    
        
        self.mach7_st.SetLabel(self.packMach_lbl + ' - ' + self.bottle_lbl)
        if table[8][mCol]:
            self.mach7Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach7Buy_st.SetLabel(self.notPurchased_lbl)
            
        self.mach8_st.SetLabel(self.packMach_lbl + ' - ' + self.can_lbl)
        if table[9][mCol]:
            self.mach8Buy_st.SetLabel(self.purchased_lbl)
        else:
            self.mach8Buy_st.SetLabel(self.notPurchased_lbl)
            
        # Finished Gods Storage Space - 
        self.fgSpace_st.SetLabel(self.fgSpace_lbl)
        if table[10][mCol]:
            self.fgSpacePerc_st.SetLabel(str(table[10][mCol])+' %')
    
    #----------------------------------------------------------------------
    def GetBeerLabel(self, numType):
        '''Takes the values 0, 1, or 2 and returns the appropriate value'''
        if numType == 1:
            return self.ale_lbl
        else:
            return self.lager_lbl
    
    #----------------------------------------------------------------------
    def BoldFont(self, boldFont=False):
        '''if the boldFont tag is true, sets the font to bold.'''
        stObjList = [o for o in self.GetChildren() if o.GetClassName() == 'wxStaticText']
        for obj in stObjList:
            if boldFont:
                obj.SetFont(self.style.h4_b_font)
                obj.SetBackgroundColour(self.style.lightGrey)
            else:
                obj.SetFont(self.style.h4_font)
                obj.SetBackgroundColour(wx.WHITE)
            
    #----------------------------------------------------------------------
    def UpdateCurrentInfo(self, currentInfoList):
        '''Updates the decision info for the current round.'''
        self.currentInfo = currentInfoList
    
#--------------------------------------------------------------------------
# DECISION LIST PANEL
#--------------------------------------------------------------------------

class DecList_Pnl(scrolled.ScrolledPanel):
    '''This lists the round decisions for the selected round in the
    review panel.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        self.currentInfo = []
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        self.SetBackgroundColour(wx.WHITE)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.thisRoundDec_lbl = GetPhrase('thisRoundDec_lbl', lang)
        
        self.mach1Cycles_lbl = GetPhrase('mach1Cycles_lbl', lang)
        self.mach2Cycles_lbl = GetPhrase('mach3Cycles_lbl', lang)
        self.mach3Cycles_lbl = GetPhrase('mach3Cycles_lbl', lang)
        self.mach4Cycles_lbl = GetPhrase('mach4Cycles_lbl', lang)
        self.mach5Cycles_lbl = GetPhrase('mach5Cycles_lbl', lang)
        
        self.ceo_lbl = GetPhrase('ceo_lbl', lang)
        self.cfo_lbl = GetPhrase('cfo_lbl', lang)
        self.manager_lbl = GetPhrase('manager_lbl', lang)
        self.asstManager_lbl = GetPhrase('asstManager_lbl', lang)
        self.headMarketing_lbl = GetPhrase('headMarketing_lbl', lang)
        self.salesRep_lbl = GetPhrase('salesRep_lbl', lang)
        self.custService_lbl = GetPhrase('custService_lbl', lang)
        self.qualityCtrl_lbl = GetPhrase('qualityCtrl_lbl', lang)
        self.brewer_lbl = GetPhrase('brewer_lbl', lang)
        self.packager_lbl = GetPhrase('packager_lbl', lang)
        self.driver_lbl = GetPhrase('driver_lbl', lang)
        self.cleaner_lbl = GetPhrase('cleaner_lbl', lang)
        
        self.priceAK_lbl = GetPhrase('priceAK_lbl', lang)
        self.priceAB_lbl = GetPhrase('priceAB_lbl', lang)
        self.priceAC_lbl = GetPhrase('priceAC_lbl', lang)
        self.priceLK_lbl = GetPhrase('priceLK_lbl', lang)
        self.priceLB_lbl = GetPhrase('priceLB_lbl', lang)
        self.priceLC_lbl = GetPhrase('priceLC_lbl', lang)
        
        self.prodAK_lbl = GetPhrase('prodAK_lbl', lang)
        self.prodAB_lbl = GetPhrase('prodAB_lbl', lang)
        self.prodAC_lbl = GetPhrase('prodAC_lbl', lang)
        self.prodLK_lbl = GetPhrase('prodLK_lbl', lang)
        self.prodLB_lbl = GetPhrase('prodLB_lbl', lang)
        self.prodLC_lbl = GetPhrase('prodLC_lbl', lang)
        
        self.aleQuality_lbl = GetPhrase('aleQuality_lbl', lang)
        self.lagerQuality_lbl = GetPhrase('lagerQuality_lbl', lang)
        
        self.marketing_lbl = GetPhrase('mrktSpend_lbl', lang)
        self.prodDev_lbl = GetPhrase('prodDev_lbl', lang)
        self.contest_lbl = GetPhrase('contest_lbl', lang)
        self.charity_lbl = GetPhrase('charity_lbl', lang)
        
        self.low_lbl = GetPhrase('low_lbl', lang)
        self.medium_lbl = GetPhrase('medium_lbl', lang)
        self.high_lbl = GetPhrase('high_lbl', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((-1, 10))
        
        # Description -----------------------------------------------------
        self.thisRoundDec_st = wx.StaticText(self, -1, self.thisRoundDec_lbl)
        self.thisRoundDec_st.SetFont(self.styles.h3_b_font)
        self.thisRoundDec_st.SetBackgroundColour(self.styles.lightGrey)
        sizer.Add(self.thisRoundDec_st, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        # Machine Panel ---------------------------------------------------
        self.machines_pnl = Machines_Pnl(self, -1)
        sizer.Add(self.machines_pnl, 0, wx.EXPAND)
        
        # Decision Panels -------------------------------------------------
        self.mach1Cycles_pnl = Decision_Pnl(self, -1)
        self.mach2Cycles_pnl = Decision_Pnl(self, -1)
        self.mach3Cycles_pnl = Decision_Pnl(self, -1)
        self.mach4Cycles_pnl = Decision_Pnl(self, -1)
        self.mach5Cycles_pnl = Decision_Pnl(self, -1)
        self.machCycleList = [self.mach1Cycles_pnl, self.mach2Cycles_pnl,
                              self.mach3Cycles_pnl, self.mach4Cycles_pnl,
                              self.mach5Cycles_pnl]
        
        self.ceo_pnl = Decision_Pnl(self, -1)
        self.cfo_pnl = Decision_Pnl(self, -1)
        self.manager_pnl = Decision_Pnl(self, -1)
        self.asstManager_pnl = Decision_Pnl(self, -1)
        self.headMarketing_pnl = Decision_Pnl(self, -1)
        self.salesRep_pnl = Decision_Pnl(self, -1)
        self.custService_pnl = Decision_Pnl(self, -1)
        self.qualityCtrl_pnl = Decision_Pnl(self, -1)
        self.brewer_pnl = Decision_Pnl(self, -1)
        self.packager_pnl = Decision_Pnl(self, -1)
        self.driver_pnl = Decision_Pnl(self, -1)
        self.cleaner_pnl = Decision_Pnl(self, -1)
        self.hrList = [self.ceo_pnl, self.cfo_pnl, self.manager_pnl,
                       self.asstManager_pnl, self.headMarketing_pnl,
                       self.salesRep_pnl, self.custService_pnl,
                       self.qualityCtrl_pnl, self.brewer_pnl, self.packager_pnl,
                       self.driver_pnl, self.cleaner_pnl]
        
        self.priceAK_pnl = Decision_Pnl(self, -1)
        self.priceAB_pnl = Decision_Pnl(self, -1)
        self.priceAC_pnl = Decision_Pnl(self, -1)
        self.priceLK_pnl = Decision_Pnl(self, -1)
        self.priceLB_pnl = Decision_Pnl(self, -1)
        self.priceLC_pnl = Decision_Pnl(self, -1)
        self.priceList = [self.priceAK_pnl, self.priceAB_pnl, self.priceAC_pnl,
                          self.priceLK_pnl, self.priceLB_pnl, self.priceLC_pnl]
        
        self.prodAK_pnl = Decision_Pnl(self, -1)
        self.prodAB_pnl = Decision_Pnl(self, -1)
        self.prodAC_pnl = Decision_Pnl(self, -1)
        self.prodLK_pnl = Decision_Pnl(self, -1)
        self.prodLB_pnl = Decision_Pnl(self, -1)
        self.prodLC_pnl = Decision_Pnl(self, -1)
        self.prodList = [self.prodAK_pnl, self.prodAB_pnl, self.prodAC_pnl,
                         self.prodLK_pnl, self.prodLB_pnl, self.prodLC_pnl]
        
        self.aleQuality_pnl = Decision_Pnl(self, -1)
        self.lagerQuality_pnl = Decision_Pnl(self, -1)
        self.qualityList = [self.aleQuality_pnl, self.lagerQuality_pnl]
        
        self.marketing_pnl = Decision_Pnl(self, -1)
        self.prodDev_pnl = Decision_Pnl(self, -1)
        self.contest_pnl = Decision_Pnl(self, -1)
        self.charity_pnl = Decision_Pnl(self, -1)
        self.otherList = [self.marketing_pnl, self.prodDev_pnl,
                          self.contest_pnl, self.charity_pnl]
        
        lineCount = 0
        addLineList = (5, 17, 23, 29, 31)
        panels = [p for p in self.GetChildren() if p.GetClassName()=='wxPanel']
        for p in panels[1:]:
            lineCount += 1
            sizer.Add(p, 0, wx.EXPAND|wx.BOTTOM, 5)
            if lineCount in addLineList:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
            
        # Set Names -------------------------------------------------------
        self.mach1Cycles_pnl.SetName(self.mach1Cycles_lbl)
        self.mach2Cycles_pnl.SetName(self.mach2Cycles_lbl)
        self.mach3Cycles_pnl.SetName(self.mach3Cycles_lbl)
        self.mach4Cycles_pnl.SetName(self.mach4Cycles_lbl)
        self.mach5Cycles_pnl.SetName(self.mach5Cycles_lbl)
        
        self.ceo_pnl.SetName(self.ceo_lbl)
        self.cfo_pnl.SetName(self.cfo_lbl)
        self.manager_pnl.SetName(self.manager_lbl)
        self.asstManager_pnl.SetName(self.asstManager_lbl)
        self.headMarketing_pnl.SetName(self.headMarketing_lbl)
        self.salesRep_pnl.SetName(self.salesRep_lbl)
        self.custService_pnl.SetName(self.custService_lbl)
        self.qualityCtrl_pnl.SetName(self.qualityCtrl_lbl)
        self.brewer_pnl.SetName(self.brewer_lbl)
        self.packager_pnl.SetName(self.packager_lbl)
        self.driver_pnl.SetName(self.driver_lbl)
        self.cleaner_pnl.SetName(self.cleaner_lbl)
        
        self.priceAK_pnl.SetName(self.priceAK_lbl)
        self.priceAB_pnl.SetName(self.priceAB_lbl)
        self.priceAC_pnl.SetName(self.priceAC_lbl)
        self.priceLK_pnl.SetName(self.priceLK_lbl)
        self.priceLB_pnl.SetName(self.priceLB_lbl)
        self.priceLC_pnl.SetName(self.priceLC_lbl)
        
        self.prodAK_pnl.SetName(self.prodAK_lbl)
        self.prodAB_pnl.SetName(self.prodAB_lbl)
        self.prodAC_pnl.SetName(self.prodAC_lbl)
        self.prodLK_pnl.SetName(self.prodLK_lbl)
        self.prodLB_pnl.SetName(self.prodLB_lbl)
        self.prodLC_pnl.SetName(self.prodLC_lbl)
        
        self.aleQuality_pnl.SetName(self.aleQuality_lbl)
        self.lagerQuality_pnl.SetName(self.lagerQuality_lbl)
        
        self.marketing_pnl.SetName(self.marketing_lbl)
        self.prodDev_pnl.SetName(self.prodDev_lbl)
        self.contest_pnl.SetName(self.contest_lbl)
        self.charity_pnl.SetName(self.charity_lbl)
        
        #--#
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets the self.year attribute the current year in the game.'''
        self.year = year
        self.machines_pnl.Init(year)
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def YearSelect(self, year):
        '''Gets the decision data for the supplied year and inputs it
        into the decision value fields.'''
        if self.currentInfo and year == self.year:
            table = self.currentInfo
        else:
            table = self.data.GetData1()
        # Input data for cycles run on each machine
        for row, pnl in zip(table[16:21], self.machCycleList):
            pnl.SetValue(unicode(row[year]))
        # Input data for HR
        for row, pnl in zip(table[21:33], self.hrList):
            pnl.SetValue(unicode(row[year]))
        # Input data for Prices
        for row, pnl in zip(table[33:39], self.priceList):
            pnl.SetValue("$ %.2f" % (row[year],))
        # Input data for Production
        for row, pnl in zip(table[39:45], self.prodList):
            pnl.SetValue("%d %%" % (row[year],))
        # Input data for Quality
        for row, pnl in zip(table[45:47], self.qualityList):
            if row[year] == 1:
                pnl.SetValue(self.low_lbl)
            elif row[year] == 2:
                pnl.SetValue(self.medium_lbl)
            elif row[year] == 3:
                pnl.SetValue(self.high_lbl)
            else:
                pnl.SetValue("ERROR!!")
        # Input data for Other Spending
        for row, pnl in zip(table[47:51], self.otherList):
            pnl.SetValue("%.2f %%" % (row[year],))
        # Input data for machines_pnl
        self.machines_pnl.SetMachValues(year)
        # Set this year's decisions to bold
        self.BoldThisRnd(year)
    
    #----------------------------------------------------------------------
    def BoldThisRnd(self, year):
        '''Bolds the decisions that are made during the current round.'''
        allPnlList = [p for p in self.GetChildren() if p.GetClassName()=='wxPanel']
        # Decision list for each round
        y1BoldList = [self.machines_pnl]
        y2BoldList = self.machCycleList + self.prodList + self.otherList
        y3BoldList = self.machCycleList + self.hrList + self.prodList + self.otherList
        y4BoldList = [self.machines_pnl] + self.machCycleList + self.hrList + \
            self.prodList + self.otherList
        y5BoldList = self.machCycleList + self.hrList + self.priceList + \
            self.qualityList + self.prodList + self.otherList
        y6BoldList = y5BoldList
        
        if year == 1:
            boldList = y1BoldList
        elif year == 2:
            boldList = y2BoldList
        elif year == 3:
            boldList = y3BoldList
        elif year == 4:
            boldList = y4BoldList
        elif year == 5:
            boldList = y5BoldList
        elif year == 6:
            boldList = y6BoldList
        else:
            boldList = []
            
        # First, set everything to a normal font
        for p in allPnlList:
            p.BoldFont()
            
        # Set the boldList panels to bold
        for p in boldList:
            p.BoldFont(boldFont = True)

    #----------------------------------------------------------------------
    def UpdateCurrentInfo(self, currentInfoList):
        '''Updates the information for the current round.'''
        self.currentInfo = currentInfoList
        self.machines_pnl.UpdateCurrentInfo(self.currentInfo)
        
#--------------------------------------------------------------------------
# MAIN REVIEW PANEL
#--------------------------------------------------------------------------

class Review_Pnl(wx.Panel):
    '''This class holds the Review Panel for the Novus Business 
    and IT education program.'''
    def __init__(self, parent, *args, **kwargs):
        super(Review_Pnl, self).__init__(parent, *args, **kwargs)
        self.styles = X_styles.NovusStyle(self)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.reviewTitle_lbl = GetPhrase('review_title', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.complete_lbl = GetPhrase('complete_lbl', lang)
        self.back_lbl = GetPhrase('back_lbl', lang)
        self.yearChoice_lbl = GetPhrase('yearChoice_lbl', lang)
        self.submit_lbl = GetPhrase('submit_lbl', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        a_box = wx.BoxSizer(wx.HORIZONTAL)
        path = X_utilities.ImageFP('Novus_Game3_32.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.revw_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        self.reviewTitle_st = wx.StaticText(self, -1, self.reviewTitle_lbl)
        self.reviewTitle_st.SetFont(self.styles.h2_font)
        self.year_st = wx.StaticText(self, -1, self.year_lbl+' - ')
        self.year_st.SetFont(self.styles.h2_font)
        self.back_btn = wx.Button(self, wx.ID_BACKWARD, self.back_lbl, size=(150, -1))
        self.back_btn.SetBackgroundColour(self.styles.lightGrey)
        self.back_btn.SetForegroundColour(self.styles.brown)
        self.back_btn.SetFont(self.styles.h3_b_font)
        a_box.Add((11, -1))
        a_box.Add(self.revw_bm, 0, wx.RIGHT, 15)
        a_box.Add(self.reviewTitle_st, 0, wx.TOP, 5)
        a_box.Add((20, -1))
        a_box.Add(wx.StaticLine(self, -1, style=wx.VERTICAL), 0, wx.EXPAND|wx.RIGHT, 20)
        a_box.Add(self.year_st, 1, wx.TOP, 5)
        a_box.Add(self.back_btn, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Button Bar ------------------------------------------------------
        self.yearList = ['1', '2', '3', '4', '5', '6']
        b_box = wx.BoxSizer()
        self.yearChoice_st = wx.StaticText(self, -1, self.yearChoice_lbl+' - ')
        self.yearChoice_cb = wx.ComboBox(self, -1, choices=self.yearList,
                                         style=wx.CB_READONLY)
        self.submit_btn = wx.Button(self, wx.ID_APPLY, self.submit_lbl)
        self.yearChoice_st.SetFont(self.styles.h3_font)
        self.yearChoice_cb.SetFont(self.styles.h3_font)
        self.submit_btn.SetFont(self.styles.h3_b_font)
        self.submit_btn.SetBackgroundColour(self.styles.darkGreen)
        self.submit_btn.SetForegroundColour(self.styles.lightGrey)
        b_box.Add(wx.StaticText(self, -1), 0, wx.RIGHT, 10)
        b_box.Add(self.yearChoice_st, 0, wx.TOP|wx.RIGHT, 3)
        b_box.Add(self.yearChoice_cb, 0, wx.TOP, 2)
        b_box.Add(self.submit_btn, 0, wx.LEFT, 20)
        sizer.Add(b_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Decision List Panel ---------------------------------------------
        c_box = wx.BoxSizer()
        self.decList_pnl = DecList_Pnl(self)
        c_box.Add(wx.StaticText(self, -1), 1)
        c_box.Add(self.decList_pnl, 8, wx.EXPAND)
        c_box.Add(wx.StaticText(self, -1), 1)
        sizer.Add(c_box, 1, wx.EXPAND|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_COMBOBOX, self.YearSelect)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the game panels according to the year provided in the
        argument.'''
        self.year = year
        self.year_st.SetLabel(self.year_lbl + ' - ' + unicode(self.year))
        self.decList_pnl.Init(self.year)
        self.decList_pnl.YearSelect(self.year)
        self.SetYearList(self.year)
        self.YearSelect(None)
        
    #----------------------------------------------------------------------
    def SetYearList(self, year):
        '''Limits the year choice list between 1 and the current year.'''
        self.yearChoice_cb.Clear()
        newList = self.yearList[:year]
        for i in newList:
            self.yearChoice_cb.Append(i)
        self.yearChoice_cb.SetValue(unicode(year))
        
    #----------------------------------------------------------------------
    def YearSelect(self, evt):
        '''When a year is selected, this gets the team decision table 
        and the specific values for the supplied year.'''
        year = int(self.yearChoice_cb.GetValue())
        self.decList_pnl.YearSelect(year)
        
        # If the selected year is the same as as the current year, enable button
        if year == self.year:
            self.submit_btn.Enable()
        else:
            self.submit_btn.Disable()
        
    #----------------------------------------------------------------------
    def OnSubmit(self, evt):
        '''Commits the team's decisions and advances the round.'''
        evt.Skip()
        
    #----------------------------------------------------------------------
    def UpdateCurrentInfo(self, currentInfoList):
        '''Updates the Review panel's info for the current round every
        time a decision notebook page is changed or a list book page is 
        changed.'''
        self.decList_pnl.UpdateCurrentInfo(currentInfoList)
        self.YearSelect(None)
        
    #----------------------------------------------------------------------
    def EndState(self):
        '''Sets up the End State of the game.'''
        self.year_st.SetLabel(self.complete_lbl)
        self.yearChoice_cb.SetValue('1')
        self.YearSelect(None)
        