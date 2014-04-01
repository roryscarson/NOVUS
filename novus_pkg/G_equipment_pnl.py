#!python
# -*- encoding: utf-8 -*-

# G_equipment_pnl.py

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
E_decisions_pnl.py +
                   + G_equipment_pnl.py
                   + G_finance_pnl.py
                   + G_production_pnl.py
                   + G_hr_pnl.py
                   + G_other_pnl.py
                   
This module contains panel class for the manufacturing
equipment purchasing decisions for rounds 1 and 4 of the 
Novus Business Simulator.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import G_summary
import Q_data
import X_styles, X_utilities
from Q_language import GetPhrase

#--------------------------------------------------------------------------
# MANUFACTURING
#--------------------------------------------------------------------------
class ManSlot_Pnl(wx.Panel):
    '''A mini panel class used to select machine type and then to
    select to purchase said machine.'''
    def __init__(self, parent, *args, **kwargs):
        super(ManSlot_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.styles = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.purchase_lbl = GetPhrase('purchased_lbl', lang)
        self.alePrice_lbl = '$ 150,000'
        self.lagerPrice_lbl = '$ 200,000'
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.index_st = wx.StaticText(self, -1, 'x)')
        self.index_st.SetFont(self.styles.h4_font)
        sizer.Add(self.index_st, 0, wx.TOP, 3)
        
        self.type_choices = [self.ale_lbl, self.lager_lbl]
        self.type_cb = wx.ComboBox(self, -1, choices=self.type_choices,
                                   size = (80, -1), style=wx.CB_READONLY)
        sizer.Add(self.type_cb, 0, wx.LEFT|wx.RIGHT, 10)
        
        self.buy_cb = wx.CheckBox(self, -1, self.purchase_lbl)
        self.buy_cb.SetFont(self.styles.h4_font)
        sizer.Add(self.buy_cb, 0, wx.TOP, 3)
        
        self.price_st = wx.StaticText(self, -1, '$ 0')
        self.price_st.SetFont(self.styles.h4_font)
        sizer.Add((25, -1))
        sizer.Add(self.price_st, 1, wx.TOP, 3)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnBuy)
        self.Bind(wx.EVT_COMBOBOX, self.OnBuy)
    
        self.SetSizer(sizer)
        
    #----------------------------------------------------------------------    
    def Init(self, index):
        '''Sets up the index number'''
        self.index_st.SetLabel(unicode(index, 'utf-8')+') ')
        self.type_cb.SetValue(self.ale_lbl)
    
    #----------------------------------------------------------------------
    def CurrentPrice(self):
        '''Returns the current purchase price of the panel.'''
        price = self.price_st.GetLabel().split(' ')[-1]
        if price == '0':
            return 0
        else:
            return int(price.replace(',', ''))
    
    #---------------------------------------------------------------------- 
    def OnBuy(self, evt):
        '''Changes the price static text to the correct value.'''
        buy = self.buy_cb.GetValue()
        if buy:
            type = self.type_cb.GetValue()
            if type == self.ale_lbl:
                self.price_st.SetLabel(self.alePrice_lbl)
            elif type == self.lager_lbl:
                self.price_st.SetLabel(self.lagerPrice_lbl)
            else:
                self.price_st.SetLabel('$ 0')
        else:
            self.price_st.SetLabel('$ 0')
            
        evt.Skip()
        
    #----------------------------------------------------------------------
    def GetState(self):
        '''Returns a tuple of boolean values. The first boolean indicates
        that a machine has been bought. The second boolean indicates
        that the machine was an ale.'''
        if self.buy_cb.GetValue():
            if self.type_cb.GetValue() == self.ale_lbl:
                return (True, True)
            else:
                return (True, False)
        else:
            return (False, False)
            
    #----------------------------------------------------------------------
    def SetState(self, isAle = False, purchased = False):
        '''Indicates that the machine has already been purchased, and 
        disables the controls.'''
        if purchased:
            if isAle:
                self.type_cb.SetValue(self.ale_lbl)
            else:
                self.type_cb.SetValue(self.lager_lbl)
            self.buy_cb.SetValue(True)
            self.price_st.SetLabel('$ 0')
            self.type_cb.Disable()
            self.buy_cb.Disable()

#--------------------------------------------------------------------------

class ManEquip_Pnl(wx.Panel):
    '''This panel allows the user to select which manufacturing equipment 
    they want to buy, and shows the total cost.'''
    def __init__(self, parent, *args, **kwargs):
        super(ManEquip_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 0
        
        # Style ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.manEquip_lbl = GetPhrase('manufacturingEquip_lbl', lang)
        self.total_lbl = GetPhrase('totalME_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.manEquip_lbl)
        self.title_st.SetFont(self.styles.h2_font)
        sizer.Add(self.title_st, 0, wx.TOP|wx.LEFT, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        self.slot1_pnl = ManSlot_Pnl(self, -1)
        self.slot2_pnl = ManSlot_Pnl(self, -1)    
        self.slot3_pnl = ManSlot_Pnl(self, -1)
        self.slot4_pnl = ManSlot_Pnl(self, -1)
        self.slot5_pnl = ManSlot_Pnl(self, -1)
        self.slotList = [self.slot1_pnl, self.slot2_pnl, self.slot3_pnl,
                         self.slot4_pnl, self.slot5_pnl]
        for p in self.slotList:
            p.Init(str(self.slotList.index(p)+1))
            sizer.Add(p, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
            
        total_box = wx.BoxSizer()    
        self.total_st = wx.StaticText(self, -1, self.total_lbl + ' - ')
        self.total_st.SetFont(self.styles.h4_b_font)
        self.totalAmount_st = wx.StaticText(self, -1, '$ 0')
        self.totalAmount_st.SetFont(self.styles.h4_b_font)
        total_box.Add(self.total_st, 0)
        total_box.Add(self.totalAmount_st, 0)
        sizer.Add(total_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnBuy)
        self.Bind(wx.EVT_COMBOBOX, self.OnBuy)
    
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the Packaging Panel.'''
        self.year = year
        self.OnBuy(None)
        
    #----------------------------------------------------------------------
    def OnBuy(self, evt):
        '''Calculates the total amount of capital purchases every time
        a machine is purchased.'''
        manSlots = [p for p in self.GetChildren() if p.GetClassName() == 'wxPanel']
        total = 0
        for p in manSlots:
            if p.type_cb.IsEnabled():
                total += p.CurrentPrice()
        total = format(total, ',d')
        self.totalAmount_st.SetLabel('$ ' + total)
        
        try:
            evt.Skip()
        except AttributeError:
            pass
    
    #----------------------------------------------------------------------
    def GetCapacity(self):
        '''Returns the current number of machines purchased and the 
        total brewing capacity (max # of cycles) as a tuple.'''
        # Get # of machines and their type
        manSlots = [p for p in self.GetChildren() if p.GetClassName() == 'wxPanel']
        ale = 0
        lager = 0
        for s in manSlots:
            state = s.GetState()
            if state[0] and state[1]:
                ale += 1
            elif state[0] and not state[1]:
                lager += 1
        machines = ale + lager
        capacity = ale * 15 + lager * 9
        return (ale, lager, capacity)
            
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current manufacturing equipment decisions.'''
        manuDesc = []
        for i in [p for p in self.GetChildren() if p.GetClassName() == 'wxPanel']:
            rslt = i.GetState()
            manuDesc.append((rslt[0], rslt[1]))
        # Adjust Machines so that the first slots are filled first
        rslt = []
        for mach in manuDesc:
            if mach[0]:
                rslt.append(mach)
        for i in range(5-len(rslt)):
            rslt.append((False, False))
        return rslt
    
    #----------------------------------------------------------------------
    def RoundSetup(self):
        '''If Round 4, shows which machines have already been purchased,
        set the price to 0, and disable the purchase / type controls.'''
        machineInfo = self.data.GetData1()[2:7]
        for slot, info in zip(self.slotList, machineInfo):
            isAle = True if info[3] == 1 else False
            purchased = True if info[1] == 1 else False
            slot.SetState(isAle, purchased)
            
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the manufacturing equipment panel.'''
        pnls = [p for p in self.GetChildren() if p.GetClassName() == 'wxPanel']
        
    
#--------------------------------------------------------------------------
# PACKAGING EQUIPMENT PANEL
#--------------------------------------------------------------------------

class PackagingEquip_Pnl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(PackagingEquip_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.styles = X_styles.NovusStyle(None)
        self.data = Q_data.Data(None)
        self.year = 0
        
        # labels --------------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.packaging_lbl = GetPhrase('packagingEquip_lbl', lang)
        self.kegging_lbl = GetPhrase('kegging_lbl', lang)
        self.bottling_lbl = GetPhrase('bottling_lbl', lang)
        self.canning_lbl = GetPhrase('canning_lbl', lang)
        self.purchase_lbl = GetPhrase('purchased_lbl', lang)
        self.total_lbl = GetPhrase('totalPE_lbl', lang)
        
        # Sizer ---------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.packaging_lbl)
        self.title_st.SetFont(self.styles.h2_font)
        sizer.Add(self.title_st, 0, wx.TOP|wx.LEFT, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        a_box = wx.BoxSizer()
        self.kegging_st = wx.StaticText(self, -1, self.kegging_lbl, size=(200, -1))
        self.kegCost_st = wx.StaticText(self, -1, '$ 30,000', size=(100, -1))
        self.kegBuy_cb = wx.CheckBox(self, -1, self.purchase_lbl, size=(120, -1))
        self.kegging_st.SetFont(self.styles.h4_font)
        self.kegCost_st.SetFont(self.styles.h4_font)
        self.kegBuy_cb.SetFont(self.styles.h4_font)
        a_box.Add(self.kegging_st, 0, wx.RIGHT, 10)
        a_box.Add(self.kegCost_st, 0)
        a_box.Add(self.kegBuy_cb, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        b_box = wx.BoxSizer()
        self.bottling_st = wx.StaticText(self, -1, self.bottling_lbl, size=(200, -1))
        self.bottleCost_st = wx.StaticText(self, -1, '$ 40,000', size=(100, -1))
        self.bottleBuy_cb = wx.CheckBox(self, -1, self.purchase_lbl, size=(120, -1))
        self.bottling_st.SetFont(self.styles.h4_font)
        self.bottleCost_st.SetFont(self.styles.h4_font)
        self.bottleBuy_cb.SetFont(self.styles.h4_font)
        b_box.Add(self.bottling_st, 0, wx.RIGHT, 10)
        b_box.Add(self.bottleCost_st, 0)
        b_box.Add(self.bottleBuy_cb, 0)
        
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        c_box = wx.BoxSizer()
        self.canning_st = wx.StaticText(self, -1, self.canning_lbl, size=(200, -1))
        self.canCost_st = wx.StaticText(self, -1, '$ 40,000', size=(100, -1))
        self.canBuy_cb = wx.CheckBox(self, -1, self.purchase_lbl, size=(120, -1))
        self.canning_st.SetFont(self.styles.h4_font)
        self.canCost_st.SetFont(self.styles.h4_font)
        self.canBuy_cb.SetFont(self.styles.h4_font)
        c_box.Add(self.canning_st, 0, wx.RIGHT, 10)
        c_box.Add(self.canCost_st, 0)
        c_box.Add(self.canBuy_cb, 0)
        
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        d_box = wx.BoxSizer()
        self.total_st = wx.StaticText(self, -1, self.total_lbl + ' - ')
        self.totalAmount_st = wx.StaticText(self, -1, '$ 0')
        self.total_st.SetFont(self.styles.h4_b_font)
        self.totalAmount_st.SetFont(self.styles.h4_b_font)
        d_box.Add(self.total_st, 0)
        d_box.Add(self.totalAmount_st, 0)
        
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        #--
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_CHECKBOX, self.OnBuy)
    
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the Packaging Panel.'''
        self.year = year
        if self.year == 1:
            self.kegBuy_cb.SetValue(True)
        self.OnBuy(None)
            
    #----------------------------------------------------------------------
    def OnBuy(self, evt):
        '''Calculates the total packaging equipment cost every time a
        purchase checkbox is checked or unchecked.'''
        kegBuy = self.kegBuy_cb.GetValue() if self.kegBuy_cb.IsEnabled() else False
        bottleBuy = self.bottleBuy_cb.GetValue() if self.bottleBuy_cb.IsEnabled() else False
        canBuy = self.canBuy_cb.GetValue() if self.canBuy_cb.IsEnabled() else False
        
        total = 0
        if kegBuy: total += 30000
        if bottleBuy: total += 40000
        if canBuy: total += 40000
        
        total = '$ ' + format(total, ',d')
        self.totalAmount_st.SetLabel(total)
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        kegBuy = self.kegBuy_cb.GetValue()
        bottleBuy = self.bottleBuy_cb.GetValue()
        canBuy = self.canBuy_cb.GetValue()
        return [kegBuy, bottleBuy, canBuy]
        
    #----------------------------------------------------------------------
    def RoundSetup(self):
        '''Sets up the round 4 equipment purchases by showing which 
        machines have already been purchased, setting the price to $0,
        and disabling the controls.'''
        machineInfo = self.data.GetData1()[7:10]
        if machineInfo[0][1]:
            self.kegBuy_cb.SetValue(True)
            self.kegBuy_cb.Disable()
            self.kegCost_st.SetLabel('$ 0')
        if machineInfo[1][1]:
            self.bottleBuy_cb.SetValue(True)
            self.bottleBuy_cb.Disable()
            self.bottleCost_st.SetLabel('$ 0')
        if machineInfo[2][1]:
            self.canBuy_cb.SetValue(True)
            self.canBuy_cb.Disable()
            self.canCost_st.SetLabel('$ 0')
    
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the packaging values.'''
        self.kegBuy_cb.SetValue(True)
        self.bottleBuy_cb.SetValue(False)
        self.canBuy_cb.SetValue(False)
        self.OnBuy(False)
        
#--------------------------------------------------------------------------
# RENT PANEL
#--------------------------------------------------------------------------

class Rent_Pnl(wx.Panel):
    '''This panel class shows the team their rental costs for
    raw material storage, brewing floor space, and finished goods
    storage space. It also allows them to select the amount of 
    finished goods storage space.'''
    def __init__(self, parent, *args, **kwargs):
        super(Rent_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # labels --------------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.rent_lbl = GetPhrase('rental_lbl', lang)
        self.rawMat_lbl = GetPhrase('rawMat_lbl', lang)
        self.brewing_lbl = GetPhrase('brewing_lbl', lang)
        self.finishedGoods_lbl = GetPhrase('finishedGoods_lbl', lang)
        self.percOfOutput_lbl = GetPhrase('percOfOutput_lbl', lang)
        self.feetNeeded_lbl = GetPhrase('feetNeeded_lbl', lang)
        self.costPerFoot_lbl = GetPhrase('costPerFoot_lbl', lang)
        self.annualRent_lbl = GetPhrase('annualRent_lbl', lang)
        self.total_lbl = GetPhrase('totalRent_lbl', lang)
        
        self.spaceChoices = ['2 %', '4 %', '6 %', '8 %', '10 %']
        
        # Sizer ---------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.rent_lbl)
        self.title_st.SetFont(self.styles.h2_font)
        sizer.Add(self.title_st, 0, wx.TOP|wx.LEFT, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        a_box = wx.BoxSizer()
        self.blank_st = wx.StaticText(self, -1, '')
        self.rawMat_st = wx.StaticText(self, -1, self.rawMat_lbl, style=wx.ALIGN_CENTER)
        self.brewing_st = wx.StaticText(self, -1, self.brewing_lbl, style=wx.ALIGN_CENTER)
        self.finishedGoods_st = wx.StaticText(self, -1, self.finishedGoods_lbl, style=wx.ALIGN_CENTER)
        self.rawMat_st.SetFont(self.styles.h5_iu_font)
        self.brewing_st.SetFont(self.styles.h5_iu_font)
        self.finishedGoods_st.SetFont(self.styles.h5_iu_font)
        a_box.Add(self.blank_st, 1, wx.RIGHT, 10)
        a_box.Add(self.rawMat_st, 1, wx.RIGHT, 10)
        a_box.Add(self.brewing_st, 1, wx.RIGHT, 10)
        a_box.Add(self.finishedGoods_st, 1)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        b_box = wx.BoxSizer()
        self.percOfOutput_st = wx.StaticText(self, -1, self.percOfOutput_lbl)
        self.percOfOutput_cb = wx.ComboBox(self, -1, choices=self.spaceChoices, style=wx.BORDER|wx.CB_READONLY)
        self.percOfOutput_cb.SetValue(self.spaceChoices[0])
        self.blank2_st = wx.StaticText(self, -1, '')
        self.percOfOutput_st.SetFont(self.styles.h5_font)
        self.percOfOutput_cb.SetFont(self.styles.h5_font)
        b_box.Add(self.percOfOutput_st, 1, wx.RIGHT, 10)
        b_box.Add(self.blank2_st, 2, wx.RIGHT, 10)
        b_box.Add(self.percOfOutput_cb, 1)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        c_box = wx.BoxSizer()
        self.feetNeeded_st = wx.StaticText(self, -1, self.feetNeeded_lbl)
        self.feetRM_st = wx.StaticText(self, -1, '0', style=wx.ALIGN_RIGHT)
        self.feetBR_st = wx.StaticText(self, -1, '0', style=wx.ALIGN_RIGHT)
        self.feetFG_st = wx.StaticText(self, -1, '0', style=wx.ALIGN_RIGHT)
        self.feetNeeded_st.SetFont(self.styles.h5_font)
        self.feetRM_st.SetFont(self.styles.h5_font)
        self.feetBR_st.SetFont(self.styles.h5_font)
        self.feetFG_st.SetFont(self.styles.h5_font)
        c_box.Add(self.feetNeeded_st, 1, wx.RIGHT, 10)
        c_box.Add(self.feetRM_st, 1, wx.RIGHT, 10)
        c_box.Add(self.feetBR_st, 1, wx.RIGHT, 10)
        c_box.Add(self.feetFG_st, 1)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        d_box = wx.BoxSizer()
        self.costPerFoot_st = wx.StaticText(self, -1, self.costPerFoot_lbl)
        self.perFootRM_st = wx.StaticText(self, -1, '$ -', style=wx.ALIGN_RIGHT)
        self.perFootBR_st = wx.StaticText(self, -1, '$ -', style=wx.ALIGN_RIGHT)
        self.perFootFG_st = wx.StaticText(self, -1, '$ -', style=wx.ALIGN_RIGHT)
        self.costPerFoot_st.SetFont(self.styles.h5_font)
        self.perFootRM_st.SetFont(self.styles.h5_font)
        self.perFootBR_st.SetFont(self.styles.h5_font)
        self.perFootFG_st.SetFont(self.styles.h5_font)
        d_box.Add(self.costPerFoot_st, 1, wx.RIGHT, 10)
        d_box.Add(self.perFootRM_st, 1, wx.RIGHT, 10)
        d_box.Add(self.perFootBR_st, 1, wx.RIGHT, 10)
        d_box.Add(self.perFootFG_st, 1)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        e_box = wx.BoxSizer()
        self.annualRent_st = wx.StaticText(self, -1, self.annualRent_lbl)
        self.rentRM_st = wx.StaticText(self, -1, '$ 0', style=wx.ALIGN_RIGHT)
        self.rentBR_st = wx.StaticText(self, -1, '$ 0', style=wx.ALIGN_RIGHT)
        self.rentFG_st = wx.StaticText(self, -1, '$ 0', style=wx.ALIGN_RIGHT)
        self.annualRent_st.SetFont(self.styles.h5_font)
        self.rentRM_st.SetFont(self.styles.h5_font)
        self.rentBR_st.SetFont(self.styles.h5_font)
        self.rentFG_st.SetFont(self.styles.h5_font)
        e_box.Add(self.annualRent_st, 1, wx.RIGHT, 10)
        e_box.Add(self.rentRM_st, 1, wx.RIGHT, 10)
        e_box.Add(self.rentBR_st, 1, wx.RIGHT, 10)
        e_box.Add(self.rentFG_st, 1)
        sizer.Add(e_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        f_box = wx.BoxSizer()
        self.total_st = wx.StaticText(self, -1, self.total_lbl + ' - ')
        self.totalAmount_st = wx.StaticText(self, -1, '$ 0')
        self.total_st.SetFont(self.styles.h4_b_font)
        self.totalAmount_st.SetFont(self.styles.h4_b_font)
        f_box.Add(self.total_st, 0, wx.LEFT, 10)
        f_box.Add(self.totalAmount_st, 0)
        sizer.Add(f_box, 0, wx.EXPAND|wx.ALL, 10)
                  
        #--
        self.SetSizer(sizer)
        
        #------------------------------------------------------------------
        self.Bind(wx.EVT_COMBOBOX, self.OnPercent)
        
    #----------------------------------------------------------------------
    def PriceFoot(self, year):
        '''Takes a year in the game and returns a baseline price per foot
        for rent adjusting for inflation.'''
        return 5*(1.03)**(year-1)
    
    #----------------------------------------------------------------------
    def RawMatRent(self, maxCapacity, year):
        '''Gets the sq. ft. needed for raw materials, 
        the price per sq. ft., and the annual rent.'''
        sqFeetNeeded = int(X_utilities.roundup(maxCapacity/12.0/2.0)*100000.0/16.0)
        if sqFeetNeeded < 5000: sqFeetNeeded = 5000
        pricePerFoot = self.PriceFoot(year)
        annualRent = int(sqFeetNeeded * pricePerFoot)
        
        self.feetRM_st.SetLabel(format(sqFeetNeeded, ',d'))
        self.perFootRM_st.SetLabel('$ %.2f' % (pricePerFoot,))
        self.rentRM_st.SetLabel('$ ' + format(annualRent, ',d'))
        
    #----------------------------------------------------------------------
    def BrewRent(self, machines, year):
        '''Gets the sq. ft. needed for brewing space, the price per
        sq. ft., and the annual rent.'''
        sqFtPerBrewMachine = 1750
        minSqFtOffice = 1000
        sqFeetNeeded = machines * sqFtPerBrewMachine + minSqFtOffice
        pricePerFoot = self.PriceFoot(year)
        annualRent = int(sqFeetNeeded * pricePerFoot)
        
        self.feetBR_st.SetLabel(format(sqFeetNeeded, ',d'))
        self.perFootBR_st.SetLabel('$ %.2f' % (pricePerFoot,))
        self.rentBR_st.SetLabel('$ ' + format(annualRent, ',d'))
    
    #----------------------------------------------------------------------
    def FinGoodsRent(self, lagerMachines, capacity, year):
        '''Gets the rent requirements and cost for storing finished
        goods.'''
        litersPerCycle = 100000
        storageLitersPerFt = 16
        percOfOutput = float(self.percOfOutput_cb.GetValue().split(' ')[0])/100
        sqFeetNeeded = (capacity * litersPerCycle / storageLitersPerFt)* percOfOutput
        
        if lagerMachines >= 1:
            pricePerFoot = self.PriceFoot(year) * 1.5
        else:
            pricePerFoot = self.PriceFoot(year)
            
        annualRent = int(sqFeetNeeded * pricePerFoot)
        
        self.feetFG_st.SetLabel(format(int(sqFeetNeeded), ',d'))
        self.perFootFG_st.SetLabel('$ %.2f' % (pricePerFoot,))
        self.rentFG_st.SetLabel('$ ' + format(annualRent, ',d'))
    
    #----------------------------------------------------------------------
    def OnPercent(self, evt):
        '''Sends the combo box event to the parent panel to recalculate
        the finished goods rent.'''
        evt.Skip()
    
    #----------------------------------------------------------------------
    def TotalRent(self):
        '''Calculates the total rent.'''
        rmRent = self.rentRM_st.GetLabel().split(' ')[-1]
        rmRent = rmRent.replace(',', '')
        brRent = self.rentBR_st.GetLabel().split(' ')[-1]
        brRent = brRent.replace(',', '')
        fgRent = self.rentFG_st.GetLabel().split(' ')[-1]
        fgRent = fgRent.replace(',', '')
        
        totalRent = int(rmRent) + int(brRent) + int(fgRent)
        self.totalAmount_st.SetLabel('$ ' + format(totalRent, ',d'))
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current decision for the finished goods storage
        space.'''
        return [int(self.percOfOutput_cb.GetValue().split(' ')[0])]
    
    #----------------------------------------------------------------------
    def RoundSetup(self):
        '''Sets the amount of finished goods storage space to the level
        chosen in round 1 or round 4.'''
        fgsp = self.data.GetData1()[10][1]
        self.percOfOutput_cb.SetValue(str(fgsp)+' %')
        
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the rent panel.'''
        self.percOfOutput_cb.SetValue('2 %')
        self.TotalRent(self)
    
#--------------------------------------------------------------------------
# Equipment Tools PANEL
#--------------------------------------------------------------------------

class EquipTools_Pnl(scrolled.ScrolledPanel):
    '''This panel allows the team to make their manufacturing and
    putchasing equipment purchasing decision for round 1, as
    well as finished goods storage space.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        self.year = 1
        self.panelNum = 1
        
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Manufacturing Equipment -----------------------------------------
        self.manEquip_pnl = ManEquip_Pnl(self, -1)
        sizer.Add(self.manEquip_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Packaging Equipment Cost ----------------------------------------
        self.packagingEquip_pnl = PackagingEquip_Pnl(self, -1)
        sizer.Add(self.packagingEquip_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Rental Costs ----------------------------------------------------
        self.rent_pnl = Rent_Pnl(self, -1)
        sizer.Add(self.rent_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        self.SetSizer(sizer)
        self.SetupScrolling()
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_CHECKBOX, self.OnBuy)
        self.Bind(wx.EVT_COMBOBOX, self.OnBuy)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the panel with the correct content for the 
        year and panel number.'''
        self.year = year
        
        self.manEquip_pnl.Init(self.year)
        self.packagingEquip_pnl.Init(self.year)
        if self.year > 1:
            self.manEquip_pnl.RoundSetup()
            self.packagingEquip_pnl.RoundSetup()
            self.rent_pnl.RoundSetup()
        
        self.manEquip_pnl.Hide()
        self.packagingEquip_pnl.Hide()
        self.rent_pnl.Hide()
        
        if year == 1 or year == 4:
            self.manEquip_pnl.Show()
            self.packagingEquip_pnl.Show()
            self.rent_pnl.Show()
        
        self.Layout()
        self.SetupScrolling()
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def OnBuy(self, evt):
        '''When production equipment is purchased, this gets the 
        number of machines purchased and the total capacity
        (max number of cycles) so the rents can be calculated.'''
        ale, lager, maxCycles = self.manEquip_pnl.GetCapacity()
        self.rent_pnl.RawMatRent(maxCycles, self.year)
        self.rent_pnl.BrewRent(ale+lager, self.year)
        self.rent_pnl.FinGoodsRent(lager, maxCycles, self.year)
        self.rent_pnl.TotalRent()
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current Equipment Decision configuration.'''
        manu = self.manEquip_pnl.ReturnInfo()
        pack = self.packagingEquip_pnl.ReturnInfo()
        fgsp = self.rent_pnl.ReturnInfo()
        # Format List to TeamData1.csv format scheme
        # Manufacturing Machines
        m1 = ['Machine 1 Purchased, Type']
        m2 = ['Machine 2 Purchased, Type']
        m3 = ['Machine 3 Purchased, Type']
        m4 = ['Machine 4 Purchased, Type']
        m5 = ['Machine 5 Purchased, Type']
        machines = [m1, m2, m3, m4, m5]
        manu2 = []
        for info, mach in zip(manu, machines):
            if not info[0]:
                mach += [0, 0, '']
            elif info[0] and info[1]:
                mach += [1, 1, 1]
            else:
                mach += [1, 1, 2]
        # Packaging Machines
        mp1 = ['Kegging Machine']
        mp2 = ['Bottling Machine']
        mp3 = ['Canning Machine']
        machines = [mp1, mp2, mp3]
        pack2 = []
        for info, mach in zip(pack, machines):
            if info:
                mach += [1, 1]
            else:
                mach += [0, 0]
        # Finished Goods Storage Space
        fgsp2 = ['Finished Goods Storage', fgsp[0], fgsp[0]]
        
        return [m1, m2, m3, m4, m5, 
                mp1, mp2, mp3, fgsp2]
        
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the Equipment Panel.'''
        self.manEquip_pnl.Reset()
        self.packagingEquip_pnl.Reset()
        self.rent_pnl.Reset()
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def GetCapExp(self):
        '''Returns the current total capital expenditures.'''
        manu_exp = self.manEquip_pnl.totalAmount_st.GetLabel()
        manu_exp = manu_exp.split(' ')[-1]
        manu_exp = int(manu_exp.replace(',', ''))
        
        pack_exp = self.packagingEquip_pnl.totalAmount_st.GetLabel()
        pack_exp = pack_exp.split(' ')[-1]
        pack_exp = int(pack_exp.replace(',', ''))
        
        return manu_exp, pack_exp
    
#--------------------------------------------------------------------------
# MAIN EQUIPMENT PANEL
#--------------------------------------------------------------------------
        
class Equipment_Pnl(wx.Panel):
    '''This combines the summary panel and the tools panel.'''
    def __init__(self, parent, *args, **kwargs):
        super(Equipment_Pnl, self).__init__(parent, *args, **kwargs)
    
        self.year = 1
        self.panelNum = 1
        
        sizer = wx.BoxSizer()
        
        self.summary = G_summary.Summary_Pnl(self)
        sizer.Add(self.summary, 0, wx.EXPAND|wx.RIGHT, 10)
        
        self.equip = EquipTools_Pnl(self)
        sizer.Add(self.equip, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
    def Init(self, year):
        self.year = year
        self.summary.Init(self.year, self.panelNum)
        self.equip.Init(year)
        
    def ReturnInfo(self):
        return self.equip.ReturnInfo()
        
    def GetCapExp(self):
        return self.equip.GetCapExp()
        
    def Reset(self):
        self.equip.Reset()
        
        
    