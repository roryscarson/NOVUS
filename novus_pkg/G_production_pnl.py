#!python
# -*- encoding: utf-8 -*-

# G_production_pnl.py

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
                   
This module contains panel class for the production decisions, 
including cycles run, packaging, pricing and ingredient quality
for the Novus Business Simulator.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import G_summary
import Q_data
import X_styles, X_utilities, X_miscPnls
import Z_mrktInfo
from Q_language import GetPhrase

class ProdMachSlot_Pnl(wx.Panel):
    '''Used when a production machine slot is filled, shows what type
    of beer the machine is used to produce, and has a spin control that
    allows the user to select the number of production cycles for the 
    machine for the current year.'''
    def __init__(self, parent, *args, **kwargs):
        super(ProdMachSlot_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.type = 0
        
        # Styles ----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.machine_lbl = GetPhrase('machine_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.maxCycles_lbl = GetPhrase('maxCycles_lbl', lang)
        self.cycles_lbl = GetPhrase('cycles_lbl', lang)
        
        # Sizer ----------------------------------------------------------
        sizer = wx.BoxSizer()

        self.machine_st = wx.StaticText(self, -1, self.machine_lbl)
        self.maxCycles_st = wx.StaticText(self, -1, self.maxCycles_lbl)
        self.cycles_st = wx.StaticText(self, -1, self.cycles_lbl+' - ')
        self.cycles_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=9,
                                     size=(80, -1))
        
        self.machine_st.SetFont(self.style.h4_font)
        self.maxCycles_st.SetFont(self.style.h4_font)
        self.cycles_st.SetFont(self.style.h4_font)
        self.cycles_sc.SetFont(self.style.h4_font)
        
        sizer.Add(self.machine_st, 1, wx.ALL, 5)
        sizer.Add(self.maxCycles_st, 1, wx.TOP|wx.RIGHT|wx.BOTTOM, 5)
        sizer.Add((10, -1))
        sizer.Add(self.cycles_st, 0, wx.TOP|wx.RIGHT|wx.BOTTOM, 5)
        sizer.Add(self.cycles_sc, 0, wx.TOP|wx.BOTTOM, 5)
        
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SPINCTRL, self.OnCycle)
        
    # FUNCTIONS -----------------------------------------------------------
    def Init(self, machNum=1, machType=0):
        '''Init(self, int machNum=1, int machType=0)
        
        This function initializes the ProdMachSlot_Pnl by supplying the
        machine's number and the type of beer it produces(0 = Ale,
        1 = Lager).'''
        if machType == 0:
            type = self.ale_lbl
            self.type = 0
            max = 15
        else:
            type = self.lager_lbl
            self.type = 1
            max = 9
        
        self.machine_st.SetLabel(self.machine_lbl+' '+str(machNum)+' - '+type)
        self.maxCycles_st.SetLabel(self.maxCycles_lbl + ' - ' + str(max))
        self.cycles_sc.SetRange(0, max)
        
    #----------------------------------------------------------------------
    def ReturnVal(self):
        '''Returns the machine type and number of cycles selected by the 
        team.'''
        return [self.type, int(self.cycles_sc.GetValue())]
        
    #----------------------------------------------------------------------
    def OnCycle(self, evt):
        '''When the user changes the number of cycles, passes the event
        up to the main Production Cycles Panel.'''
        evt.Skip()
        
        
#--------------------------------------------------------------------------
# PRODUCTION CYCLES PANEL
#--------------------------------------------------------------------------

class ProdCycles_Pnl(wx.Panel):
    '''Allows the teams to decide how many cycles they want to run
    on each manufacturing machine.'''
    def __init__(self, parent, *args, **kwargs):
        super(ProdCycles_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        
        # Style -----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.prod_lbl = GetPhrase('prodCycles_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.totAle_lbl = GetPhrase('totAle_lbl', lang)
        self.totLager_lbl = GetPhrase('totLager_lbl', lang)
        self.total_lbl = GetPhrase('totalProduction_lbl', lang)
        self.cycles_lbl = GetPhrase('cycles_lbl', lang)
        self.liters_lbl = GetPhrase('liters_lbl', lang)
        self.mrktShare_lbl = GetPhrase('mrktShare_lbl', lang)
        self.abrvLit_lbl = GetPhrase('abrvLit_lbl', lang)

        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.prod_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        # Add Machines ----------------------------------------------------
        self.prodMachInfo = self.data.GetData1()[2:7]
        
        self.mach1_pnl = ProdMachSlot_Pnl(self, -1)
        self.mach2_pnl = ProdMachSlot_Pnl(self, -1)
        self.mach3_pnl = ProdMachSlot_Pnl(self, -1)
        self.mach4_pnl = ProdMachSlot_Pnl(self, -1)
        self.mach5_pnl = ProdMachSlot_Pnl(self, -1) 
        self.panel_list = [p for p in self.GetChildren() if p.GetClassName()=='wxPanel']
        
        machNum = 1
        for machInfo, machPnl in zip(self.prodMachInfo, self.panel_list):
            sizer.Add(machPnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
            sizer.Add((-1, 5))
            if machInfo[1]:
                beer = 0 if machInfo[3] == 1 else 1
                machPnl.Init(machNum=machNum, machType=beer)
            else:
                machPnl.Hide()
            machNum += 1
        
        sizer.Add((-1, 10))

        # Production Totals -----------------------------------------------
        a_box = wx.BoxSizer()
        self.cycles_st = wx.StaticText(self, -1, self.cycles_lbl)
        self.liters_st = wx.StaticText(self, -1, self.liters_lbl)
        self.mrktShare_st = wx.StaticText(self, -1, self.mrktShare_lbl)
        self.cycles_st.SetFont(self.style.h4_iu_font)
        self.liters_st.SetFont(self.style.h4_iu_font)
        self.mrktShare_st.SetFont(self.style.h4_iu_font)
        a_box.Add(wx.StaticText(self, -1), 2, wx.LEFT, 10)
        a_box.Add(self.cycles_st, 1)
        a_box.Add(self.liters_st, 1)
        a_box.Add(self.mrktShare_st, 1, wx.RIGHT, 20)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        b_box = wx.BoxSizer()
        self.totAle_st = wx.StaticText(self, -1, self.totAle_lbl)
        self.totAleAmt_st = wx.StaticText(self, -1, '-')
        self.totAleLit_st = wx.StaticText(self, -1, '-')
        self.totAleMS_st = wx.StaticText(self, -1, '-')
        self.totAle_st.SetFont(self.style.h4_font)
        self.totAleAmt_st.SetFont(self.style.h4_font)
        self.totAleLit_st.SetFont(self.style.h4_font)
        self.totAleMS_st.SetFont(self.style.h4_font)
        b_box.Add(self.totAle_st, 2, wx.LEFT, 10)
        b_box.Add(self.totAleAmt_st, 1)
        b_box.Add(self.totAleLit_st, 1)
        b_box.Add(self.totAleMS_st, 1, wx.RIGHT, 20)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        c_box = wx.BoxSizer()
        self.totLager_st = wx.StaticText(self, -1, self.totLager_lbl)
        self.totLagerAmt_st = wx.StaticText(self, -1, '-')
        self.totLagerLit_st = wx.StaticText(self, -1, '-')
        self.totLagerMS_st = wx.StaticText(self, -1, '-')
        self.totLager_st.SetFont(self.style.h4_font)
        self.totLagerAmt_st.SetFont(self.style.h4_font)
        self.totLagerLit_st.SetFont(self.style.h4_font)
        self.totLagerMS_st.SetFont(self.style.h4_font)
        c_box.Add(self.totLager_st, 2, wx.LEFT, 10)
        c_box.Add(self.totLagerAmt_st, 1)
        c_box.Add(self.totLagerLit_st, 1)
        c_box.Add(self.totLagerMS_st, 1, wx.RIGHT, 20)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
      
        d_box = wx.BoxSizer()
        self.total_st = wx.StaticText(self, -1, self.total_lbl)
        self.totalAmt_st = wx.StaticText(self, -1, '-')
        self.totalLit_st = wx.StaticText(self, -1, '-')
        self.totalMS_st = wx.StaticText(self, -1, '-')
        self.total_st.SetFont(self.style.h4_b_font)
        self.totalAmt_st.SetFont(self.style.h4_b_font)
        self.totalLit_st.SetFont(self.style.h4_b_font)
        self.totalMS_st.SetFont(self.style.h4_b_font)
        d_box.Add(self.total_st, 2, wx.LEFT, 10)
        d_box.Add(self.totalAmt_st, 1)
        d_box.Add(self.totalLit_st, 1)
        d_box.Add(self.totalMS_st, 1, wx.RIGHT, 20)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SPINCTRL, self.OnChange)
        
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Initializes the manufacturing production panel.'''
        self.year = year
        for x in self.panel_list:
            x.cycles_sc.SetValue(0)
        machNum = 1
        self.prodMachInfo = self.data.GetData1()[2:7]
        for machInfo, machPnl in zip(self.prodMachInfo, self.panel_list):
            machSlot = 1 if self.year <=4 else 2
            if machInfo[machSlot]:
                beer = 0 if machInfo[3] == 1 else 1
                machPnl.Init(machNum=machNum, machType=beer)
                machPnl.Show()
            else:
                machPnl.Hide()
            machNum += 1
        self.Layout()
    
    #----------------------------------------------------------------------
    def OnChange(self, evt):
        '''When the team changes the number of production cycles, this
        updates the totals metrics.'''
        aleTotal, lagerTotal = 0, 0
        
        for pnl in self.panel_list:
            if pnl.ReturnVal()[0] == 0:
                aleTotal += pnl.ReturnVal()[1]
            else:
                lagerTotal += pnl.ReturnVal()[1]
                
        self.totAleAmt_st.SetLabel(str(aleTotal))
        self.totAleLit_st.SetLabel(format((aleTotal * 100000), ',d')+' '+self.abrvLit_lbl)
        self.totLagerAmt_st.SetLabel(str(lagerTotal))
        self.totLagerLit_st.SetLabel(format((lagerTotal * 100000), ',d')+' '+self.abrvLit_lbl)
        self.totalAmt_st.SetLabel(str(aleTotal + lagerTotal))
        self.totalLit_st.SetLabel(format(((aleTotal+lagerTotal) * 100000), ',d')+' '+self.abrvLit_lbl)
        
        # Calculate the production market shares and update the labels. 
        aleSize, lagerSize = Z_mrktInfo.GetMarketLiters(self.year)
        
        aleMS = (aleTotal * 100000) / float(aleSize) * 100.0
        lagerMS = (lagerTotal * 100000) / float(lagerSize) * 100.0
        totalMS = ((aleTotal+lagerTotal) * 100000) / float(aleSize+lagerSize) * 100.0
        
        self.totAleMS_st.SetLabel("%.2f %%" % aleMS)
        self.totLagerMS_st.SetLabel("%.2f %%" % lagerMS)
        self.totalMS_st.SetLabel("%.2f %%" % totalMS)
        
        evt.Skip()
        
    #----------------------------------------------------------------------
    def ReturnProduction(self):
        '''Returns the current volume of ale and lager production in 
        liters.'''
        try:
            aleLiters = int(self.totAleAmt_st.GetLabel()) * 100000
        except ValueError:
            aleLiters = 0
            
        try:
            lagerLiters = int(self.totLagerAmt_st.GetLabel()) * 100000
        except ValueError:
            lagerLiters = 0
        return [aleLiters, lagerLiters]
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current production cycles decision for each machine.'''
        rslt = []
        for pnl in self.panel_list:
            if pnl.IsShown():
                rslt.append(pnl.ReturnVal()[1])
            else:
                rslt.append(0)
        return rslt
    
    #----------------------------------------------------------------------
    def UpdateAvailable(self, currentInfoList):
        '''In round 4, make any purchased machines available for 
        production.'''
        if self.year == 4:
            prodMachInfo = currentInfoList[2:7]
            machNum = 1
            for machInfo, machPnl in zip(prodMachInfo, self.panel_list):
                if machInfo[2]:
                    if machInfo[3] == 1:
                        beer = 0
                    else:
                        beer = 1
                    machPnl.Init(machNum=machNum, machType=beer)
                    machPnl.Show()
                else:
                    machPnl.Hide()
                machNum += 1
                    
            self.Layout()
            
#--------------------------------------------------------------------------
# PACKAGING PANEL
#--------------------------------------------------------------------------

class Packaging_Pnl(wx.Panel):
    '''Shows the packaging options, enables the packaging options for the 
    machines purchased and allows the team's to allocate between different
    packaging options (Kegs, Bottles, and Cans)'''
    def __init__(self, parent, *args, **kwargs):
        super(Packaging_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        self.kegYes = False
        self.bottleYes = False
        self.canYes = False
        self.case1 = False # Keg / Bottle
        self.case2 = False # Keg / Can
        self.case3 = False # Bottle / Can
        self.case4 = False # Keg / Bottle / Can
        self.aleLiters = 0      # Ale Liters Produced
        self.lagerLiters = 0    # Lager Liters Produced
        
        # Style -----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('packaging_lbl', lang)
        self.keg_lbl = GetPhrase('keg_lbl', lang)
        self.bottle_lbl = GetPhrase('bottle_lbl', lang)
        self.can_lbl = GetPhrase('can_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.units_lbl = GetPhrase('units_lbl', lang)
        self.total_lbl = GetPhrase('total_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        # Add Machines ----------------------------------------------------
        a_box = wx.BoxSizer()
        self.keg_st = wx.StaticText(self, -1, self.keg_lbl+' (%)', style=wx.ALIGN_CENTER)
        self.bottle_st = wx.StaticText(self, -1, self.bottle_lbl+' (%)', style=wx.ALIGN_CENTER)
        self.can_st = wx.StaticText(self, -1, self.can_lbl+' (%)', style=wx.ALIGN_CENTER)
        self.keg_st.SetFont(self.style.h4_iu_font)
        self.bottle_st.SetFont(self.style.h4_iu_font)
        self.can_st.SetFont(self.style.h4_iu_font)
        a_box.Add(wx.StaticText(self, -1), 1, wx.LEFT, 10)
        a_box.Add(self.keg_st, 1, wx.RIGHT, 20)
        a_box.Add(self.bottle_st, 1, wx.RIGHT, 20)
        a_box.Add(self.can_st, 1)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        b_box = wx.BoxSizer()
        self.ale_st = wx.StaticText(self, -1, self.ale_lbl)
        self.aleKeg_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=100, size=(80, -1))
        self.aleBottle_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=100, size=(80, -1))
        self.aleCan_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=100, size=(80, -1))
        self.aleWarning_st = wx.StaticText(self, -1, ' ! ')
        self.ale_st.SetFont(self.style.h4_font)
        self.aleKeg_sc.SetFont(self.style.h4_font)
        self.aleBottle_sc.SetFont(self.style.h4_font)
        self.aleCan_sc.SetFont(self.style.h4_font)
        self.aleWarning_st.SetBackgroundColour(wx.RED)
        self.aleWarning_st.SetForegroundColour(wx.WHITE)
        self.aleWarning_st.SetFont(self.style.h4_b_font)
        b_box.Add(self.ale_st, 1, wx.LEFT, 10)
        b_box.Add(self.aleKeg_sc, 1, wx.RIGHT, 20)
        b_box.Add(self.aleBottle_sc, 1, wx.RIGHT, 20)
        b_box.Add(self.aleCan_sc, 1, wx.RIGHT, 10)
        b_box.Add(self.aleWarning_st, 0)
        self.aleWarning_st.Hide()
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        c_box = wx.BoxSizer()
        self.lager_st = wx.StaticText(self, -1, self.lager_lbl)
        self.lagerKeg_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=100, size=(80, -1))
        self.lagerBottle_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=100, size=(80, -1))
        self.lagerCan_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=100, size=(80, -1))
        self.lagerWarning_st = wx.StaticText(self,-1, ' ! ')
        self.lager_st.SetFont(self.style.h4_font)
        self.lagerKeg_sc.SetFont(self.style.h4_font)
        self.lagerBottle_sc.SetFont(self.style.h4_font)
        self.lagerCan_sc.SetFont(self.style.h4_font)
        self.lagerWarning_st.SetBackgroundColour(wx.RED)
        self.lagerWarning_st.SetForegroundColour(wx.WHITE)
        self.lagerWarning_st.SetFont(self.style.h4_b_font)
        c_box.Add(self.lager_st, 1, wx.LEFT, 10)
        c_box.Add(self.lagerKeg_sc, 1, wx.RIGHT, 20)
        c_box.Add(self.lagerBottle_sc, 1, wx.RIGHT, 20)
        c_box.Add(self.lagerCan_sc, 1, wx.RIGHT, 10)
        c_box.Add(self.lagerWarning_st, 0)
        self.lagerWarning_st.Hide()
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        sizer.Add((-1, 10))
        
        d_box = wx.BoxSizer()
        self.aleUnit_st = wx.StaticText(self, -1, self.ale_lbl+' - '+self.units_lbl)
        self.aleKegUnit_st = wx.StaticText(self, -1, '-')
        self.aleBottleUnit_st = wx.StaticText(self, -1, '-')
        self.aleCanUnit_st = wx.StaticText(self, -1, '-')
        self.aleUnit_st.SetFont(self.style.h4_font)
        self.aleKegUnit_st.SetFont(self.style.h4_font)
        self.aleBottleUnit_st.SetFont(self.style.h4_font)
        self.aleCanUnit_st.SetFont(self.style.h4_font)
        d_box.Add(self.aleUnit_st, 1, wx.LEFT, 10)
        d_box.Add(self.aleKegUnit_st, 1, wx.RIGHT, 20)
        d_box.Add(self.aleBottleUnit_st, 1, wx.RIGHT, 20)
        d_box.Add(self.aleCanUnit_st, 1)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        e_box = wx.BoxSizer()
        self.lagerUnit_st = wx.StaticText(self, -1, self.lager_lbl+' - '+self.units_lbl)
        self.lagerKegUnit_st = wx.StaticText(self, -1, '-')
        self.lagerBottleUnit_st = wx.StaticText(self, -1, '-')
        self.lagerCanUnit_st = wx.StaticText(self, -1, '-')
        self.lagerUnit_st.SetFont(self.style.h4_font)
        self.lagerKegUnit_st.SetFont(self.style.h4_font)
        self.lagerBottleUnit_st.SetFont(self.style.h4_font)
        self.lagerCanUnit_st.SetFont(self.style.h4_font)
        e_box.Add(self.lagerUnit_st, 1, wx.LEFT, 10)
        e_box.Add(self.lagerKegUnit_st, 1, wx.RIGHT, 20)
        e_box.Add(self.lagerBottleUnit_st, 1, wx.RIGHT, 20)
        e_box.Add(self.lagerCanUnit_st, 1)
        sizer.Add(e_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        f_box = wx.BoxSizer()
        self.totalUnit_st = wx.StaticText(self, -1, self.total_lbl+' - '+self.units_lbl)
        self.totalKegUnit_st = wx.StaticText(self, -1, '-')
        self.totalBottleUnit_st = wx.StaticText(self, -1, '-')
        self.totalCanUnit_st = wx.StaticText(self, -1, '-')
        self.totalUnit_st.SetFont(self.style.h4_b_font)
        self.totalKegUnit_st.SetFont(self.style.h4_b_font)
        self.totalBottleUnit_st.SetFont(self.style.h4_b_font)
        self.totalCanUnit_st.SetFont(self.style.h4_b_font)
        f_box.Add(self.totalUnit_st, 1, wx.LEFT, 10)
        f_box.Add(self.totalKegUnit_st, 1, wx.RIGHT, 20)
        f_box.Add(self.totalBottleUnit_st, 1, wx.RIGHT, 20)
        f_box.Add(self.totalCanUnit_st, 1)
        sizer.Add(f_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin)
        
        # Groupings ------------------------------------------------------
        self.aleSpinCtrls = [self.aleKeg_sc, self.aleBottle_sc, self.aleCan_sc]
        self.lagerSpinCtrls = [self.lagerKeg_sc, self.lagerBottle_sc, 
                               self.lagerCan_sc]
        
    # Functions and Event Handlers ----------------------------------------
    def Init(self, year, useCurrentInfo = False, currentInfo = []):
        '''Sets up the panel. Specifically, finds out which packaging
        machines are available and enables / disables the controls
        accordingly.'''
        self.year = year
        
        mCol = 1 if self.year < 4 else 2
        if not useCurrentInfo:
            self.kegYes = True if self.data.GetData1()[7][mCol] else False
            self.bottleYes = True if self.data.GetData1()[8][mCol] else False
            self.canYes = True if self.data.GetData1()[9][mCol] else False
        else:
            self.kegYes = True if currentInfo[7][mCol] else False
            self.bottleYes = True if currentInfo[8][mCol] else False
            self.canYes = True if currentInfo[9][mCol] else False
        
        if not self.kegYes:
            self.aleKeg_sc.Disable()
            self.lagerKeg_sc.Disable()
        else:
            self.aleKeg_sc.Enable()
            self.lagerKeg_sc.Enable()
        if not self.bottleYes:
            self.aleBottle_sc.Disable()
            self.lagerBottle_sc.Disable()
        else:
            self.aleBottle_sc.Enable()
            self.lagerBottle_sc.Enable()
        if not self.canYes:
            self.aleCan_sc.Disable()
            self.lagerCan_sc.Disable()
        else:
            self.aleCan_sc.Enable()
            self.lagerCan_sc.Enable()
            
        # Set the correct starting values
        self.case1 = False
        self.case2 = False
        self.case3 = False
        self.case4 = False
        # One machine purchased
        if self.kegYes and not self.bottleYes and not self.canYes:
            self.aleKeg_sc.SetValue(100)
            self.aleKeg_sc.Disable()
            self.lagerKeg_sc.SetValue(100)
            self.lagerKeg_sc.Disable()
            self.aleBottle_sc.SetValue(0)
            self.lagerBottle_sc.SetValue(0)
            self.aleCan_sc.SetValue(0)
            self.lagerCan_sc.SetValue(0)
        elif self.bottleYes and not self.kegYes and not self.canYes:
            self.aleBottle_sc.SetValue(100)
            self.aleBottle_sc.Disable()
            self.lagerBottle_sc.SetValue(100)
            self.lagerBottle_sc.Disable()
            self.aleKeg_sc.SetValue(0)
            self.lagerKeg_sc.SetValue(0)
            self.aleCan_sc.SetValue(0)
            self.lagerCan_sc.SetValue(0)
        elif self.canYes and not self.kegYes and not self.bottleYes:
            self.aleCan_sc.SetValue(100)
            self.aleCan_sc.Disable()
            self.lagerCan_sc.SetValue(100)
            self.lagerCan_sc.Disable()
            self.aleKeg_sc.SetValue(0)
            self.lagerKeg_sc.SetValue(0)
            self.aleBottle_sc.SetValue(0)
            self.lagerBottle_sc.SetValue(0)
            
        # Two machines purchased
        aleSum = self.aleKeg_sc.GetValue() + self.aleBottle_sc.GetValue() + self.aleCan_sc.GetValue()
        lagerSum = self.lagerKeg_sc.GetValue() + self.lagerBottle_sc.GetValue() + self.lagerCan_sc.GetValue()
        if self.kegYes and self.bottleYes and not self.canYes:
            if not useCurrentInfo or aleSum == 0:    
                self.aleKeg_sc.SetValue(50)
                self.aleBottle_sc.SetValue(50)
                self.aleCan_sc.SetValue(0)
            if not useCurrentInfo or lagerSum == 0:    
                self.lagerKeg_sc.SetValue(50)
                self.lagerBottle_sc.SetValue(50)
                self.lagerCan_sc.SetValue(0)
            self.case1 = True
        elif self.kegYes and self.canYes and not self.bottleYes:
            if not useCurrentInfo or aleSum == 0:
                self.aleKeg_sc.SetValue(50)
                self.aleCan_sc.SetValue(50)
                self.aleBottle_sc.SetValue(0)
            if not useCurrentInfo or lagerSum == 0:
                self.lagerKeg_sc.SetValue(50)
                self.lagerCan_sc.SetValue(50)
                self.lagerBottle_sc.SetValue(0)
            self.case2 = True
        elif self.canYes and self.bottleYes and not self.kegYes:
            if not useCurrentInfo or aleSum == 0:
                self.aleBottle_sc.SetValue(50)
                self.aleCan_sc.SetValue(50)
                self.aleKeg_sc.SetValue(0)
            if not useCurrentInfo or lagerSum == 0:
                self.lagerBottle_sc.SetValue(50)
                self.lagerCan_sc.SetValue(50)
                self.lagerKeg_sc.SetValue(0)
            self.case3 = True
            
        # All three machines purchased
        if self.kegYes and self.bottleYes and self.canYes:
            if not useCurrentInfo or aleSum == 0:
                self.aleKeg_sc.SetValue(40)
                self.aleBottle_sc.SetValue(30)
                self.aleCan_sc.SetValue(30)
            if not useCurrentInfo or lagerSum == 0:
                self.lagerKeg_sc.SetValue(40)
                self.lagerBottle_sc.SetValue(30)
                self.lagerCan_sc.SetValue(30)
            self.case4 = True
            
        # Case 4 100 % total check 
        if self.case4:
            if aleSum != 100:
                self.aleKeg_sc.SetValue(40)
                self.aleBottle_sc.SetValue(30)
                self.aleCan_sc.SetValue(30)
                self.aleWarning_st.Hide()
            if lagerSum != 100:
                self.lagerKeg_sc.SetValue(40)
                self.lagerBottle_sc.SetValue(30)
                self.lagerCan_sc.SetValue(30)
                self.lagerWarning_st.Hide()
            
    #----------------------------------------------------------------------
    def OnSpin(self, evt):
        '''Autocalculates the values of the spin controls when any value is 
        changed.'''
        isAle = True if evt.GetEventObject() in self.aleSpinCtrls else False
        if isAle:
            kegVal = int(self.aleKeg_sc.GetValue())
            bottleVal = int(self.aleBottle_sc.GetValue())
            canVal = int(self.aleCan_sc.GetValue())
            kegCtrl = self.aleKeg_sc
            bottleCtrl = self.aleBottle_sc
            canCtrl = self.aleCan_sc
            warning = self.aleWarning_st
        else:
            kegVal = int(self.lagerKeg_sc.GetValue())
            bottleVal = int(self.lagerBottle_sc.GetValue())
            canVal = int(self.lagerCan_sc.GetValue())
            kegCtrl = self.lagerKeg_sc
            bottleCtrl = self.lagerBottle_sc
            canCtrl = self.lagerCan_sc
            warning = self.lagerWarning_st
        
        if self.case1:
            if evt.GetEventObject() == kegCtrl:
                bottleCtrl.SetValue(100-kegVal)
            else:
                kegCtrl.SetValue(100-bottleVal)
        elif self.case2:
            if evt.GetEventObject() == kegCtrl:
                canCtrl.SetValue(100-kegVal)
            else:
                kegCtrl.SetValue(100-canVal)
        elif self.case3:
            if evt.GetEventObject() == bottleCtrl:
                canCtrl.SetValue(100-bottleVal)
            else:
                bottleCtrl.SetValue(100-canVal)
        elif self.case4:
            total = kegVal + bottleVal + canVal
            if total != 100:
                warning.SetLabel(' ! '+str(total)+' % ')
                warning.Show()
            else:
                warning.Hide()
                
        self.Layout()
        
        self.CalculateUnits()
        
        evt.Skip()
        
    #----------------------------------------------------------------------
    def UpdateProduction(self, aleProd, lagerProd):
        '''Updates the self.aleLiters and self.lagerLiters attributes
        every time the number of production cycles is changed.'''
        self.aleLiters = aleProd
        self.lagerLiters = lagerProd
        self.CalculateUnits()
        
    #----------------------------------------------------------------------
    def CalculateUnits(self):
        '''Finds the units of production for each product, give the 
        production output and packaging allocations.'''
        kegVol = 64
        bottleVol = (1.0/2.0)
        canVol = (1.0/3.0)
        
        aleKeg = self.aleLiters * self.aleKeg_sc.GetValue()/100/kegVol
        aleBottle = int(self.aleLiters * self.aleBottle_sc.GetValue()/100/bottleVol)
        aleCan = int(self.aleLiters * self.aleCan_sc.GetValue()/100/canVol)
        lagerKeg = self.lagerLiters * self.lagerKeg_sc.GetValue()/100/kegVol
        lagerBottle = int(self.lagerLiters * self.lagerBottle_sc.GetValue()/100/bottleVol)
        lagerCan = int(self.lagerLiters * self.lagerCan_sc.GetValue()/100/canVol)
        
        self.aleKegUnit_st.SetLabel(format(aleKeg, ',d'))
        self.aleBottleUnit_st.SetLabel(format(aleBottle, ',d'))
        self.aleCanUnit_st.SetLabel(format(aleCan, ',d'))
        self.lagerKegUnit_st.SetLabel(format(lagerKeg, ',d'))
        self.lagerBottleUnit_st.SetLabel(format(lagerBottle, ',d'))
        self.lagerCanUnit_st.SetLabel(format(lagerCan, ',d'))
        self.totalKegUnit_st.SetLabel(format(aleKeg+lagerKeg, ',d'))
        self.totalBottleUnit_st.SetLabel(format(aleBottle+lagerBottle, ',d'))
        self.totalCanUnit_st.SetLabel(format(aleCan+lagerCan, ',d'))
        
        return [aleKeg, aleBottle, aleCan, lagerKeg, lagerBottle, lagerCan]
    
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current packaging allocation decisions.'''
        ak = self.aleKeg_sc.GetValue()
        ab = self.aleBottle_sc.GetValue()
        ac = self.aleCan_sc.GetValue()
        lk = self.lagerKeg_sc.GetValue()
        lb = self.lagerBottle_sc.GetValue()
        lc = self.lagerCan_sc.GetValue()
        
        # If self.case4, make sure that the total == 100
        if self.case4:
            # Check the ale total
            if ak + ab + ac != 100:
                diff = 100 - (ak + ab + ac)
                ak += int((1.0/3.0) * diff)
                ab += int((1.0/3.0) * diff)
                ac = 100 - ak - ab
            if lk + lb + lc != 100:
                diff = 100 - (lk + lb + lc)
                lk += int((1.0/3.0) * diff)
                lb += int((1.0/3.0) * diff)
                lc = 100 - lk - lb
            
        return [ak, ab, ac, lk, lb, lc]
        
    #----------------------------------------------------------------------
    def UpdateAvailable(self, currentInfoList):
        '''In round 4, make any purchased machines available for 
        packaging.'''
        if self.year == 4:
            self.Init(self.year, True, currentInfoList)
        self.Layout()
        
    #----------------------------------------------------------------------
    def Round1Setup(self):
        '''Sets up the packaging for round 1.'''
        self.aleKeg_sc.SetValue(0)
        self.aleBottle_sc.SetValue(0)
        self.aleCan_sc.SetValue(0)
        self.lagerKeg_sc.SetValue(0)
        self.lagerBottle_sc.SetValue(0)
        self.lagerCan_sc.SetValue(0)
        
#--------------------------------------------------------------------------
# PRICE AND QUALITY PANEL
#--------------------------------------------------------------------------

class PriceQuality_Pnl(wx.Panel):
    '''Allows the user to change the quality of ingredients and the 
    product prices. Displays product COGS and gross margin.'''
    def __init__(self, parent, *args, **kwargs):
        super(PriceQuality_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.aleLiters = 0      # Selected Volume of Ale Prod.
        self.lagerLiters = 0    # Selected Volumen of Lager Prod.
        self.year = 0
        
        # Style -----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('priceQuality_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.keg_lbl = GetPhrase('keg_lbl', lang)
        self.low_lbl = GetPhrase('low_lbl', lang)
        self.medium_lbl = GetPhrase('medium_lbl', lang)
        self.high_lbl = GetPhrase('high_lbl', lang)
        self.bottle_lbl = GetPhrase('bottle_lbl', lang)
        self.can_lbl = GetPhrase('can_lbl', lang)
        self.ingQuality_lbl = GetPhrase('ingredientQuality_lbl', lang)
        self.price_lbl = GetPhrase('price_lbl', lang)
        self.cogs_lbl = GetPhrase('cogs_lbl', lang)
        self.margin_lbl = GetPhrase('grossMargin_lbl', lang)
        self.unit_lbl = GetPhrase('unit_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        #--#
        a_box = wx.BoxSizer()
        self.ale_st = wx.StaticText(self, -1, self.ale_lbl, style=wx.ALIGN_CENTER)
        self.lager_st = wx.StaticText(self, -1, self.lager_lbl, style=wx.ALIGN_CENTER)
        self.ale_st.SetFont(self.style.h4_iu_font)
        self.lager_st.SetFont(self.style.h4_iu_font)
        a_box.Add((10, -1))
        a_box.Add(wx.StaticText(self, -1), 1, wx.TOP, 3)
        a_box.Add((10, -1))
        a_box.Add(self.ale_st, 1, wx.RIGHT, 20)
        a_box.Add(self.lager_st, 1, wx.RIGHT, 10)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        #--#
        self.qualityChoices = [self.low_lbl, self.medium_lbl, self.high_lbl]
        b_box = wx.BoxSizer()
        self.ingQuality_st = wx.StaticText(self, -1, self.ingQuality_lbl)
        self.aleIQ_cb = wx.ComboBox(self, -1, value=self.medium_lbl, 
                                    choices=self.qualityChoices,
                                    style=wx.CB_READONLY)
        self.lagerIQ_cb = wx.ComboBox(self, -1, value=self.medium_lbl,
                                      choices=self.qualityChoices,
                                      style=wx.CB_READONLY)
        self.ingQuality_st.SetFont(self.style.h4_font)
        self.aleIQ_cb.SetFont(self.style.h4_font)
        self.lagerIQ_cb.SetFont(self.style.h4_font)
        b_box.Add((10, -1))
        b_box.Add(self.ingQuality_st, 1, wx.TOP, 3)
        b_box.Add((10, -1))
        b_box.Add(self.aleIQ_cb, 1, wx.RIGHT, 20)
        b_box.Add(self.lagerIQ_cb, 1, wx.RIGHT, 10)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        sizer.Add((-1, 5))
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 30)
        sizer.Add((-1, 15))
        
        #--#
        c_box = wx.BoxSizer()
        self.kegPr_st = wx.StaticText(self, -1, self.keg_lbl+' '+self.price_lbl+' ($)')
        self.aleKegPr_tc = X_miscPnls.Currency_TC(self, -1)
        self.lagerKegPr_tc = X_miscPnls.Currency_TC(self, -1)
        self.kegPr_st.SetFont(self.style.h4_font)
        c_box.Add((10, -1))
        c_box.Add(self.kegPr_st, 1, wx.TOP, 3)
        c_box.Add((10, -1))
        c_box.Add(self.aleKegPr_tc, 1, wx.RIGHT, 20)
        c_box.Add(self.lagerKegPr_tc, 1, wx.RIGHT, 10)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        
        c1_box = wx.BoxSizer()
        self.kegCOGS_st = wx.StaticText(self, -1, self.cogs_lbl+' ('+self.unit_lbl+')')
        self.aleKegCOGS_st = wx.StaticText(self,-1, '-')
        self.lagerKegCOGS_st = wx.StaticText(self, -1, '-')
        self.kegCOGS_st.SetFont(self.style.h5_i_font)
        self.aleKegCOGS_st.SetFont(self.style.h5_i_font)
        self.lagerKegCOGS_st.SetFont(self.style.h5_i_font)
        c1_box.Add((10, -1))
        c1_box.Add(self.kegCOGS_st, 1, wx.LEFT|wx.RIGHT, 10)
        c1_box.Add((20, -1))
        c1_box.Add(self.aleKegCOGS_st, 1, wx.RIGHT, 20)
        c1_box.Add(self.lagerKegCOGS_st, 1, wx.RIGHT, 10)
        sizer.Add(c1_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        c2_box = wx.BoxSizer()
        self.kegGM_st = wx.StaticText(self, -1, self.margin_lbl+' ('+self.unit_lbl+')')
        self.aleKegGM_st = wx.StaticText(self,-1, '-')
        self.lagerKegGM_st = wx.StaticText(self, -1, '-')
        self.kegGM_st.SetFont(self.style.h5_i_font)
        self.aleKegGM_st.SetFont(self.style.h5_i_font)
        self.lagerKegGM_st.SetFont(self.style.h5_i_font)
        c2_box.Add((10, -1))
        c2_box.Add(self.kegGM_st, 1, wx.LEFT|wx.RIGHT, 10)
        c2_box.Add((20, -1))
        c2_box.Add(self.aleKegGM_st, 1, wx.RIGHT, 20)
        c2_box.Add(self.lagerKegGM_st, 1, wx.RIGHT, 10)
        sizer.Add(c2_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        sizer.Add((-1, 5))
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 30)
        sizer.Add((-1, 15))
        
        #--#
        d_box = wx.BoxSizer()
        self.bottlePr_st = wx.StaticText(self, -1, self.bottle_lbl+' '+self.price_lbl+' ($)')
        self.aleBottlePr_tc = X_miscPnls.Currency_TC(self, -1)
        self.lagerBottlePr_tc = X_miscPnls.Currency_TC(self, -1)
        self.bottlePr_st.SetFont(self.style.h4_font)
        d_box.Add((10, -1))
        d_box.Add(self.bottlePr_st, 1, wx.TOP, 3)
        d_box.Add((10, -1))
        d_box.Add(self.aleBottlePr_tc, 1, wx.RIGHT, 20)
        d_box.Add(self.lagerBottlePr_tc, 1, wx.RIGHT, 10)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        d1_box = wx.BoxSizer()
        self.bottleCOGS_st = wx.StaticText(self, -1, self.cogs_lbl+' ('+self.unit_lbl+')')
        self.aleBottleCOGS_st = wx.StaticText(self,-1, '-')
        self.lagerBottleCOGS_st = wx.StaticText(self, -1, '-')
        self.bottleCOGS_st.SetFont(self.style.h5_i_font)
        self.aleBottleCOGS_st.SetFont(self.style.h5_i_font)
        self.lagerBottleCOGS_st.SetFont(self.style.h5_i_font)
        d1_box.Add((10, -1))
        d1_box.Add(self.bottleCOGS_st, 1, wx.LEFT|wx.RIGHT, 10)
        d1_box.Add((20, -1))
        d1_box.Add(self.aleBottleCOGS_st, 1, wx.RIGHT, 20)
        d1_box.Add(self.lagerBottleCOGS_st, 1, wx.RIGHT, 10)
        sizer.Add(d1_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        d2_box = wx.BoxSizer()
        self.bottleGM_st = wx.StaticText(self, -1, self.margin_lbl+' ('+self.unit_lbl+')')
        self.aleBottleGM_st = wx.StaticText(self,-1, '-')
        self.lagerBottleGM_st = wx.StaticText(self, -1, '-')
        self.bottleGM_st.SetFont(self.style.h5_i_font)
        self.aleBottleGM_st.SetFont(self.style.h5_i_font)
        self.lagerBottleGM_st.SetFont(self.style.h5_i_font)
        d2_box.Add((10, -1))
        d2_box.Add(self.bottleGM_st, 1, wx.LEFT|wx.RIGHT, 10)
        d2_box.Add((20, -1))
        d2_box.Add(self.aleBottleGM_st, 1, wx.RIGHT, 20)
        d2_box.Add(self.lagerBottleGM_st, 1, wx.RIGHT, 10)
        sizer.Add(d2_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        sizer.Add((-1, 5))
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 30)
        sizer.Add((-1, 15))
        
        #--#
        e_box = wx.BoxSizer()
        self.canPr_st = wx.StaticText(self, -1, self.can_lbl+' '+self.price_lbl+' ($)')
        self.aleCanPr_tc = X_miscPnls.Currency_TC(self, -1)
        self.lagerCanPr_tc = X_miscPnls.Currency_TC(self, -1)
        self.canPr_st.SetFont(self.style.h4_font)
        e_box.Add((10, -1))
        e_box.Add(self.canPr_st, 1, wx.TOP, 3)
        e_box.Add((10, -1))
        e_box.Add(self.aleCanPr_tc, 1, wx.RIGHT, 20)
        e_box.Add(self.lagerCanPr_tc, 1, wx.RIGHT, 10)
        sizer.Add(e_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        e1_box = wx.BoxSizer()
        self.canCOGS_st = wx.StaticText(self, -1, self.cogs_lbl+' ('+self.unit_lbl+')')
        self.aleCanCOGS_st = wx.StaticText(self,-1, '-')
        self.lagerCanCOGS_st = wx.StaticText(self, -1, '-')
        self.canCOGS_st.SetFont(self.style.h5_i_font)
        self.aleCanCOGS_st.SetFont(self.style.h5_i_font)
        self.lagerCanCOGS_st.SetFont(self.style.h5_i_font)
        e1_box.Add((10, -1))
        e1_box.Add(self.canCOGS_st, 1, wx.LEFT|wx.RIGHT, 10)
        e1_box.Add((20, -1))
        e1_box.Add(self.aleCanCOGS_st, 1, wx.RIGHT, 20)
        e1_box.Add(self.lagerCanCOGS_st, 1, wx.RIGHT, 10)
        sizer.Add(e1_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        e2_box = wx.BoxSizer()
        self.canGM_st = wx.StaticText(self, -1, self.margin_lbl+' ('+self.unit_lbl+')')
        self.aleCanGM_st = wx.StaticText(self,-1, '-')
        self.lagerCanGM_st = wx.StaticText(self, -1, '-')
        self.canGM_st.SetFont(self.style.h5_i_font)
        self.aleCanGM_st.SetFont(self.style.h5_i_font)
        self.lagerCanGM_st.SetFont(self.style.h5_i_font)
        e2_box.Add((10, -1))
        e2_box.Add(self.canGM_st, 1, wx.LEFT|wx.RIGHT, 10)
        e2_box.Add((20, -1))
        e2_box.Add(self.aleCanGM_st, 1, wx.RIGHT, 20)
        e2_box.Add(self.lagerCanGM_st, 1, wx.RIGHT, 10)
        sizer.Add(e2_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_TEXT, self.OnPrice)
        self.Bind(wx.EVT_COMBOBOX, self.OnQuality)
        
        # Other -----------------------------------------------------------
        self.textCtrlObjs = [o for o in self.GetChildren() if o.GetClassName()=='wxTextCtrl']
        
    #----------------------------------------------------------------------
    def Init(self, year, useCurrentInfo = False, currentInfo = []):
        '''Sets the beginning quality and prices. Only enables
        Product Lines that are available.'''
        avgPrices = Z_mrktInfo.getAvgUnitPrices(year)
        totalPrice = 0
        for x in self.textCtrlObjs:
            try:
                totalPrice += float(x.GetValue())
            except ValueError:
                totalPrice += 0
                
        if not useCurrentInfo or totalPrice == 0:
            self.aleKegPr_tc.SetLabel("%.2f" % (avgPrices[0],))
            self.lagerKegPr_tc.SetLabel("%.2f" % (avgPrices[0],))
            self.aleBottlePr_tc.SetLabel("%.2f" % (avgPrices[1],))
            self.lagerBottlePr_tc.SetLabel("%.2f" % (avgPrices[1],))
            self.aleCanPr_tc.SetLabel("%.2f" % (avgPrices[2],))
            self.lagerCanPr_tc.SetLabel("%.2f" % (avgPrices[2],))
        
        self.year = year
        
        # Set price ranges for years 5 and 6:
        if self.year == 5:
            self.aleKegPr_tc.SetRange(54.09, 76.93)
            self.lagerKegPr_tc.SetRange(67.61, 96.16)
            self.aleBottlePr_tc.SetRange(0.44, 0.67)
            self.lagerBottlePr_tc.SetRange(0.55, 0.84)
            self.aleCanPr_tc.SetRange(0.39, 0.58)
            self.lagerCanPr_tc.SetRange(0.49, 0.72)
            
        elif self.year == 6:
            self.aleKegPr_tc.SetRange(55.71, 79.24)
            self.lagerKegPr_tc.SetRange(69.64, 99.04)
            self.aleBottlePr_tc.SetRange(0.46, 0.69)
            self.lagerBottlePr_tc.SetRange(0.57, 0.87)
            self.aleCanPr_tc.SetRange(0.41, 0.59)
            self.lagerCanPr_tc.SetRange(0.51, 0.74)
        
        mCol = 1 if self.year < 4 else 2
        if not useCurrentInfo:
            kegYes = True if self.data.GetData1()[7][mCol] else False
            bottleYes = True if self.data.GetData1()[8][mCol] else False
            canYes = True if self.data.GetData1()[9][mCol] else False
        else:
            kegYes = True if currentInfo[7][mCol] else False
            bottleYes = True if currentInfo[8][mCol] else False
            canYes = True if currentInfo[9][mCol] else False
        
        if not kegYes:
            self.aleKegPr_tc.Disable()
            self.lagerKegPr_tc.Disable()
            self.kegCOGS_st.Hide()
            self.aleKegCOGS_st.Hide()
            self.lagerKegCOGS_st.Hide()
            self.kegGM_st.Hide()
            self.aleKegGM_st.Hide()
            self.lagerKegGM_st.Hide()
        else:
            self.aleKegPr_tc.Enable()
            self.lagerKegPr_tc.Enable()
            self.kegCOGS_st.Show()
            self.aleKegCOGS_st.Show()
            self.lagerKegCOGS_st.Show()
            self.kegGM_st.Show()
            self.aleKegGM_st.Show()
            self.lagerKegGM_st.Show()
        
        if not bottleYes:
            self.aleBottlePr_tc.Disable()
            self.lagerBottlePr_tc.Disable()
            self.bottleCOGS_st.Hide()
            self.aleBottleCOGS_st.Hide()
            self.lagerBottleCOGS_st.Hide()
            self.bottleGM_st.Hide()
            self.aleBottleGM_st.Hide()
            self.lagerBottleGM_st.Hide()
        else:
            self.aleBottlePr_tc.Enable()
            self.lagerBottlePr_tc.Enable()
            self.bottleCOGS_st.Show()
            self.aleBottleCOGS_st.Show()
            self.lagerBottleCOGS_st.Show()
            self.bottleGM_st.Show()
            self.aleBottleGM_st.Show()
            self.lagerBottleGM_st.Show()
            
        if not canYes:
            self.aleCanPr_tc.Disable()
            self.lagerCanPr_tc.Disable()
            self.canCOGS_st.Hide()
            self.aleCanCOGS_st.Hide()
            self.lagerCanCOGS_st.Hide()
            self.canGM_st.Hide()
            self.aleCanGM_st.Hide()
            self.lagerCanGM_st.Hide()
        else:
            self.aleCanPr_tc.Enable()
            self.lagerCanPr_tc.Enable()
            self.canCOGS_st.Show()
            self.aleCanCOGS_st.Show()
            self.lagerCanCOGS_st.Show()
            self.canGM_st.Show()
            self.aleCanGM_st.Show()
            self.lagerCanGM_st.Show()
        
        self.Layout()
        
    #----------------------------------------------------------------------
    def UpdateProduction(self, aleProd, lagerProd):
        '''Updates the self.aleLiters and self.lagerLiters attributes
        every time the number of production cycles is changed.'''
        self.aleLiters = aleProd
        self.lagerLiters = lagerProd
        self.GetCOGS()
                                
    #----------------------------------------------------------------------
    def OnPrice(self, evt):
        '''When a price is entered, runs the update routine for caluclating
        the COGS and gross margin.'''
        # Only execute when the calling object is a TextCtrl
        if evt.GetEventObject() in self.textCtrlObjs and \
            evt.GetEventObject().GetValue():
            self.GetCOGS()
            evt.Skip()
        
    #----------------------------------------------------------------------
    def OnQuality(self, evt):
        '''When product quality is selected, runs the update routine
        for calculating the COGS and gross margin.'''
        self.GetCOGS()
        
    #----------------------------------------------------------------------
    def GetCOGS(self):
        '''Gets the COGS table from the Z_mrktInfo.getCOGS function,
        changes from COGS / Liter to COGS / Unit,and calls the 
        setAleInfo and setLagerInfo functions.'''
        cogsPerLitTable = Z_mrktInfo.getCOGS(self.year, self.aleLiters+self.lagerLiters)
        kegVol = 64
        bottleVol = (1.0/2.0)
        canVol = (1.0/3.0)
        # Convert table to COGS / Unit
        rowCount = 0
        cogsPerUnitTable = []
        for x in cogsPerLitTable:
            # Get the right unit conversion volume
            if rowCount==0:
                prodVol = kegVol
            elif rowCount==1:
                prodVol = bottleVol
            else:
                prodVol = canVol
            rowCount += 1
            # Append the product COGS row to the COGS / Unit table
            cogsPerUnitTable.append((round(x[0]*prodVol, 3), 
                                    round(x[1]*prodVol, 3), 
                                    round(x[2]*prodVol, 3)))
        # Call the SetProdInfo for Ales and Lagers
        self.SetProdInfo(cogsPerUnitTable, isAle=True)
        self.SetProdInfo(cogsPerUnitTable, isAle=False)
        
    #----------------------------------------------------------------------
    def SetProdInfo(self, cogsPerUnitTable, isAle):
        '''Takes a COGS per Unit table, and if the product is Ale.
        Then calculates and sets the label for COGS and gross margin.'''
        # Set the function's lists
        if isAle:
            qualityCB = self.aleIQ_cb
            priceStList = [self.aleKegPr_tc, self.aleBottlePr_tc, self.aleCanPr_tc]
            cogsStList = [self.aleKegCOGS_st, self.aleBottleCOGS_st, self.aleCanCOGS_st]
            gmStList = [self.aleKegGM_st, self.aleBottleGM_st, self.aleCanGM_st]
        else:
            qualityCB = self.lagerIQ_cb
            priceStList = [self.lagerKegPr_tc, self.lagerBottlePr_tc, self.lagerCanPr_tc]
            cogsStList = [self.lagerKegCOGS_st, self.lagerBottleCOGS_st, self.lagerCanCOGS_st]
            gmStList = [self.lagerKegGM_st, self.lagerBottleGM_st, self.lagerCanGM_st]
        # Get the column in the COGS table, determined by the selected
        #       quality
        cogsCol = 0
        if qualityCB.GetValue() == self.low_lbl:
            cogsCol = 0
        elif qualityCB.GetValue() == self.high_lbl:
            cogsCol = 2
        else:
            cogsCol = 1
        # Extract a COGS / Unit list => [kegCOGS, bottleCOGS, canCOGS]
        cogsList = []
        for x in cogsPerUnitTable:
            cogsList.append(x[cogsCol])
        # Set labels for the product COGS StaticText objects
        for val, st in zip(cogsList, cogsStList):
            st.SetLabel("$ %.2f" % (val,))
        # Create a Price List
        priceList = []
        for x in priceStList:
            try:
                price = float(x.GetValue())
            except ValueError, e:
                price = 0
            priceList.append(price)
                
        # Create Gross Margin List
        gmList = []
        for cogs, pr in zip(cogsList, priceList):
            gmList.append(pr-cogs)
        # Set Labels for the Gross Margins
        for cogs, price, st in zip(cogsList, priceList, gmStList):
            try:
                gmPercent = (price-cogs)/price * 100
                gm = price-cogs
                st.SetLabel("$ %.2f   (%.2f %%)" % (gm, gmPercent,))
            except ZeroDivisionError:
                st.SetLabel("$ -%.2f   (-100 %%)" % (cogs,))
                
    #----------------------------------------------------------------------
    def GetPrices(self):
        '''Returns a tuple of the current prices for all of the products.'''
        ak = float(self.aleKegPr_tc.GetValue())
        ab = float(self.aleBottlePr_tc.GetValue())
        ac = float(self.aleCanPr_tc.GetValue())
        lk = float(self.lagerKegPr_tc.GetValue())
        lb = float(self.lagerBottlePr_tc.GetValue())
        lc = float(self.lagerCanPr_tc.GetValue())
        return [ak, ab, ac, lk, lb, lc]
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current quality and price decisions.'''
        rslt = []
        if self.aleIQ_cb.GetValue() == self.low_lbl:
            rslt.append(1)
        elif self.aleIQ_cb.GetValue() == self.high_lbl:
            rslt.append(3)
        else:
            rslt.append(2)
        
        if self.lagerIQ_cb.GetValue() == self.low_lbl:
            rslt.append(1)
        elif self.lagerIQ_cb.GetValue() == self.high_lbl:
            rslt.append(3)
        else:
            rslt.append(2)
            
        return rslt + self.GetPrices()
    
    #----------------------------------------------------------------------
    def UpdateAvailable(self, currentInfoList):
        '''In round 4, make any purchased machines available for 
        packaging.'''
        if self.year == 4:
            self.Init(self.year, True, currentInfoList)
        self.Layout()
        
    
    #----------------------------------------------------------------------
    def Round1Setup(self):
        '''Sets up the prices and ingredient quality for round 1.'''
        self.aleIQ_cb.SetValue(self.medium_lbl)
        self.lagerIQ_cb.SetValue(self.medium_lbl)
        self.aleKegPr_tc.SetValue('0.00')
        self.aleBottlePr_tc.SetValue('0.00')
        self.aleCanPr_tc.SetValue('0.00')
        self.lagerKegPr_tc.SetValue('0.00')
        self.lagerBottlePr_tc.SetValue('0.00')
        self.lagerCanPr_tc.SetValue('0.00')
    
    #----------------------------------------------------------------------
    def Round2Setup(self):
        '''Sets up the prices and ingredient quality for round 2.'''
        self.aleIQ_cb.SetValue(self.medium_lbl)
        self.lagerIQ_cb.SetValue(self.high_lbl)
        self.aleKegPr_tc.SetValue('55.51')
        self.aleBottlePr_tc.SetValue('0.48')
        self.aleCanPr_tc.SetValue('0.42')
        self.lagerKegPr_tc.SetValue('70.97')
        self.lagerBottlePr_tc.SetValue('0.63')
        self.lagerCanPr_tc.SetValue('0.54')
            
    #----------------------------------------------------------------------
    def Round3Setup(self):
        '''Sets up the prices and ingredient quality for round 3.'''
        self.aleIQ_cb.SetValue(self.medium_lbl)
        self.lagerIQ_cb.SetValue(self.high_lbl)
        self.aleKegPr_tc.SetValue('59.00')
        self.aleBottlePr_tc.SetValue('0.51')
        self.aleCanPr_tc.SetValue('0.45')
        self.lagerKegPr_tc.SetValue('75.43')
        self.lagerBottlePr_tc.SetValue('0.66')
        self.lagerCanPr_tc.SetValue('0.58')
        
    #----------------------------------------------------------------------
    def Round4Setup(self):
        '''Sets up the prices and ingredient quality for round 3.'''
        self.aleIQ_cb.SetValue(self.medium_lbl)
        self.lagerIQ_cb.SetValue(self.high_lbl)
        self.aleKegPr_tc.SetValue('61.69')
        self.aleBottlePr_tc.SetValue('0.53')
        self.aleCanPr_tc.SetValue('0.46')
        self.lagerKegPr_tc.SetValue('78.90')
        self.lagerBottlePr_tc.SetValue('0.69')
        self.lagerCanPr_tc.SetValue('0.60')
        
#--------------------------------------------------------------------------
# PRODUCTION TOOLS PANEL
#--------------------------------------------------------------------------

class ProdTools_Pnl(scrolled.ScrolledPanel):
    '''This panel allows the team to make their production
    decisions for rounds 2 - 6.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        self.year = 1
        self.panelNum = 3
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Production Cycles Panel -----------------------------------------
        self.prodCycles_pnl = ProdCycles_Pnl(self, -1)
        sizer.Add(self.prodCycles_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Packaging Panel -------------------------------------------------
        self.packaging_pnl = Packaging_Pnl(self, -1)
        sizer.Add(self.packaging_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Price and Quality Panel -----------------------------------------
        self.priceQuality_pnl = PriceQuality_Pnl(self, -1)
        sizer.Add(self.priceQuality_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the panel with the correct content for the 
        year and panel number.'''
        self.year = year
        self.prodCycles_pnl.Init(self.year)
        self.packaging_pnl.Init(self.year)
        self.priceQuality_pnl.Init(self.year)
        
        self.prodCycles_pnl.Hide()
        self.packaging_pnl.Hide()
        self.priceQuality_pnl.Hide()
        if year > 1:
            self.prodCycles_pnl.Show()
            self.packaging_pnl.Show()
        if year > 4:
            self.priceQuality_pnl.Show()
        self.Layout()
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def OnSpin(self, evt):
        '''Handles wx.EVT_SPINCTRL events that are propogated up from the
        children panels.'''
        # When the production amount is changed, send the production 
        #       volumes to the packaging panel
        if evt.GetEventObject().GetParent().GetParent() == self.prodCycles_pnl:
            aleLiters = self.prodCycles_pnl.ReturnProduction()[0]
            lagerLiters = self.prodCycles_pnl.ReturnProduction()[1]
            self.packaging_pnl.UpdateProduction(aleLiters, lagerLiters)
            self.priceQuality_pnl.UpdateProduction(aleLiters, lagerLiters)
        
    #----------------------------------------------------------------------
    def GetRevenue(self):
        '''Gets the current forecasted revenue, based off of production,
        packaging, and pricing decisions.'''
        unitTuple = self.packaging_pnl.CalculateUnits()
        priceTuple = self.priceQuality_pnl.GetPrices()
        total = 0
        for units, price in zip(unitTuple, priceTuple):
            total += (units * price)
        return int(total)
        
    #----------------------------------------------------------------------
    def GetCycles(self):
        '''Returns the number of production cycles.'''
        aleCyc = self.prodCycles_pnl.ReturnProduction()[0]/100000
        lagerCyc = self.prodCycles_pnl.ReturnProduction()[1]/100000
        return [aleCyc, lagerCyc]
    
    #----------------------------------------------------------------------
    def UpdateAvailable(self, currentInfoList):
        '''When additional machines are purchased in round 4, make
        available for production.'''
        self.prodCycles_pnl.UpdateAvailable(currentInfoList)
        self.packaging_pnl.UpdateAvailable(currentInfoList)
        self.priceQuality_pnl.UpdateAvailable(currentInfoList)
        self.Layout()
        self.SetupScrolling()
    
    #----------------------------------------------------------------------
    def Round1Setup(self):
        '''Sets up the input fields for round 2.'''
        self.packaging_pnl.Round1Setup()
        self.priceQuality_pnl.Round1Setup()
        
    #----------------------------------------------------------------------
    def Round2Setup(self):
        '''Sets up the input fields for round 2.'''
        self.priceQuality_pnl.Round2Setup()
        
    #----------------------------------------------------------------------
    def Round3Setup(self):
        '''Sets up the input fields for round 3.'''
        self.priceQuality_pnl.Round3Setup()
    
    #----------------------------------------------------------------------
    def Round4Setup(self):
        '''Sets up the input fields for round 4.'''
        self.priceQuality_pnl.Round4Setup()
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current production decisions.'''
        cycles = self.prodCycles_pnl.ReturnInfo()
        pack = self.packaging_pnl.ReturnInfo()
        prices = self.priceQuality_pnl.ReturnInfo()
        
        # Reformat the lists to coincide with the teamData1.csv formatting
        m1Cycs = ['Machine 1 Cycles Run', cycles[0], cycles[0], cycles[0], cycles[0], cycles[0], cycles[0]]
        m2Cycs = ['Machine 2 Cycles Run', cycles[1], cycles[1], cycles[1], cycles[1], cycles[1], cycles[1]]
        m3Cycs = ['Machine 3 Cycles Run', cycles[2], cycles[2], cycles[2], cycles[2], cycles[2], cycles[2]]
        m4Cycs = ['Machine 4 Cycles Run', cycles[3], cycles[3], cycles[3], cycles[3], cycles[3], cycles[3]]
        m5Cycs = ['Machine 5 Cycles Run', cycles[4], cycles[4], cycles[4], cycles[4], cycles[4], cycles[4]]
        
        aleQ = ['Ale Quality', prices[0], prices[0], prices[0], prices[0], prices[0], prices[0]]
        lagerQ = ['Lager Quality', prices[1], prices[1], prices[1], prices[1], prices[1], prices[1]]    
                
        akPr = ['Ale - Keg ASP', prices[2], prices[2], prices[2], prices[2], prices[2], prices[2]]
        abPr = ['Ale - Bottle ASP', prices[3], prices[3], prices[3], prices[3], prices[3], prices[3]]
        acPr = ['Ale - Can ASP', prices[4], prices[4], prices[4], prices[4], prices[4], prices[4]]
        lkPr = ['Lager - Keg ASP', prices[5], prices[5], prices[5], prices[5], prices[5], prices[5]]
        lbPr = ['Lager - Bottle ASP', prices[6], prices[6], prices[6], prices[6], prices[6], prices[6]]
        lcPr = ['Lager - Can ASP', prices[7], prices[7], prices[7], prices[7], prices[7], prices[7]]
        
        akPa = ['Ale - Keg Prod.', pack[0], pack[0], pack[0], pack[0], pack[0], pack[0]]
        abPa = ['Ale - Bottle Prod.', pack[1], pack[1], pack[1], pack[1], pack[1], pack[1]]
        acPa = ['Ale - Can Prod.', pack[2], pack[2], pack[2], pack[2], pack[2], pack[2]]
        lkPa = ['Lager - Keg Prod.', pack[3], pack[3], pack[3], pack[3], pack[3], pack[3]]
        lbPa = ['Lager - Bottle Prod.', pack[4], pack[4], pack[4], pack[4], pack[4], pack[4]]
        lcPa = ['Lager - Can Prod.', pack[5], pack[5], pack[5], pack[5], pack[5], pack[5]]
        
        return [m1Cycs, m2Cycs, m3Cycs, m4Cycs, m5Cycs,
                aleQ, lagerQ,
                akPr, abPr, acPr, lkPr, lbPr, lcPr,
                akPa, abPa, acPa, lkPa, lbPa, lcPa]
        
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the production panel.'''
        self.Init(year)
   
#--------------------------------------------------------------------------
# PRODUCTION TOOLS PANEL
#--------------------------------------------------------------------------

class Production_Pnl(wx.Panel):
    '''This combines the production tools panel and the summary page
    for the production decision point.'''
    def __init__(self, parent, *args, **kwargs):
        super(Production_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        self.panelNum = 3
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Summary Panel 
        self.summary = G_summary.Summary_Pnl(self)
        sizer.Add(self.summary, 0, wx.EXPAND|wx.RIGHT, 10)
        
        # Production Tools Panel
        self.prodTools = ProdTools_Pnl(self)
        sizer.Add(self.prodTools, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
    #----------------------------------------------------------------------
    def Init(self, year):
        self.year = year
        self.summary.Init(self.year, self.panelNum)
        self.prodTools.Init(self.year)
        
    def GetRevenue(self):
        return self.prodTools.GetRevenue()
        
    def GetCycles(self):
        return self.prodTools.GetCycles()
        
    def UpdateAvailable(self, currentInfoList):
        self.prodTools.UpdateAvailable(currentInfoList)
        
    def Round1Setup(self):
        self.prodTools.packaging_pnl.Round1Setup()
        self.prodTools.priceQuality_pnl.Round1Setup()
        
    def Round2Setup(self):
        self.prodTools.priceQuality_pnl.Round2Setup()
        
    def Round3Setup(self):
        self.prodTools.priceQuality_pnl.Round3Setup()
    
    def Round4Setup(self):
        self.prodTools.priceQuality_pnl.Round4Setup()
        
    def ReturnInfo(self):
        return self.prodTools.ReturnInfo()
        
    def Reset(self):
        self.prodTools.Reset()
        