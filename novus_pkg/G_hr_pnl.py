#!python
# -*- encoding: utf-8 -*-

# G_hr_pnl.py

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
                   
This module contains panel class for the human resources
decisions for the Novus Business Simulator.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import G_summary
import Q_data
import X_styles, X_utilities
import Z_mrktInfo
from Q_language import GetPhrase

#--------------------------------------------------------------------------
# HR Slot Panel
#--------------------------------------------------------------------------

class HRSlot_Pnl(wx.Panel):
    '''This panel holds individual HR decision slots.'''
    def __init__(self, parent, *args, **kwargs):
        super(HRSlot_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.totPP = 0          # The total yearly cost of hiring one person 
                                #       for this position
                        
        # Style -----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer()
        
        self.position_st = wx.StaticText(self, -1, '-')
        self.quantity_sc = wx.SpinCtrl(self, -1, value='0', min=0, max=20,
                                       size = (80, 18))
        self.totPP_st = wx.StaticText(self, -1, '-')
        self.totalYear_st = wx.StaticText(self, -1, '-')
        
        # Set Styles ------------------------------------------------------
        for x in [i for i in self.GetChildren()]:
            x.SetFont(self.style.h5_font)
        
        sizer.Add(self.position_st, 1, wx.LEFT, 10)
        sizer.Add(self.quantity_sc, 0, wx.LEFT|wx.RIGHT, 10)
        sizer.Add(self.totPP_st, 1, wx.LEFT, 10)
        sizer.Add(self.totalYear_st, 1, wx.LEFT, 10)
        
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SPINCTRL, self.OnHire)
        
    #----------------------------------------------------------------------
    def Init(self, pos='', sal=0):
        '''Init(self, string pos='', int sal=0)
        
        Initializes the HRSlot panel. Requires a position title, and a  
        per person salary for the position'''
        self.position_st.SetLabel(pos)
        self.totPP = sal 
        self.totPP_st.SetLabel("$ "+format(self.totPP, ',d'))
    
    #----------------------------------------------------------------------
    def SetCEO(self):
        '''Sets the CEO amount to 0 and disable the quantity spin ctrl.'''
        self.quantity_sc.SetValue(1)
        self.OnHire(None)
        self.quantity_sc.Disable()
    
    #----------------------------------------------------------------------
    def OnHire(self, evt):
        '''Calculates the total annual cost based on the number of hires'''
        hires = int(self.quantity_sc.GetValue())
        totalYear = hires * self.totPP
        self.totalYear_st.SetLabel('$ ' + format(totalYear, ',d'))

#--------------------------------------------------------------------------
# HR Decisions Panel
#--------------------------------------------------------------------------

class HRDesc_Pnl(wx.Panel):
    '''This panel holds all of the individual HR decision slots.'''
    def __init__(self, parent, *args, **kwargs):
        super(HRDesc_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Style -----------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        self.ForecastedRev = 0
        self.cyclesRun = 0
        self.staffLevel = 0
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('hr_lbl', lang)
        self.position_lbl = GetPhrase('position_lbl', lang)
        self.quantity_lbl = GetPhrase('quantity_lbl', lang)
        self.totAnnualCostPP_lbl = GetPhrase('totAnnualCostPP_lbl', lang)
        self.totAnnualCost_lbl = GetPhrase('totAnnualCost_lbl', lang)
        self.totHrCost_lbl = GetPhrase('totHrCost_lbl', lang)
        
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
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        # Column Headers 
        a_box = wx.BoxSizer()
        self.pos_st = wx.StaticText(self, -1, self.position_lbl)
        self.quantity_st = wx.StaticText(self, -1, self.quantity_lbl, size=(80, -1))
        self.totAnnualCostPP_st = wx.StaticText(self, -1, self.totAnnualCostPP_lbl)
        self.totAnnualCost_st = wx.StaticText(self, -1, self.totAnnualCost_lbl)
        for x in [i for i in self.GetChildren() if i.GetClassName()=='wxStaticText'][1:]:
            x.SetFont(self.style.h5_iu_font)
        a_box.Add(self.pos_st, 1, wx.LEFT, 10)
        a_box.Add(self.quantity_st, 0, wx.LEFT|wx.RIGHT, 10)
        a_box.Add(self.totAnnualCostPP_st, 1, wx.LEFT, 10)
        a_box.Add(self.totAnnualCost_st, 1, wx.LEFT, 10)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        # Add HR slot panels --
        self.ceo_pnl = HRSlot_Pnl(self, -1)
        self.cfo_pnl = HRSlot_Pnl(self, -1)
        self.manager_pnl = HRSlot_Pnl(self, -1)
        self.asstManager_pnl = HRSlot_Pnl(self, -1)
        self.headMarketing_pnl = HRSlot_Pnl(self, -1)
        self.salesRep_pnl = HRSlot_Pnl(self, -1)
        self.custService_pnl = HRSlot_Pnl(self, -1)
        self.qualityCtrl_pnl = HRSlot_Pnl(self, -1)
        self.brewer_pnl = HRSlot_Pnl(self, -1)
        self.packager_pnl = HRSlot_Pnl(self, -1)
        self.driver_pnl = HRSlot_Pnl(self, -1)
        self.cleaner_pnl = HRSlot_Pnl(self, -1)
        
        self.hrSlotPanels = [p for p in self.GetChildren() if p.GetClassName()=='wxPanel']
        
        # Pos / Salary List --
        self.posLblList = [self.ceo_lbl, self.cfo_lbl, self.manager_lbl, 
                           self.asstManager_lbl, self.headMarketing_lbl,
                           self.salesRep_lbl, self.custService_lbl, 
                           self.qualityCtrl_lbl, self.brewer_lbl, self.packager_lbl, 
                           self.driver_lbl, self.cleaner_lbl]
        self.posSalaryList = Z_mrktInfo.getHRCosts(self.year)
        
        # Add HR Slot Panels to sizer and initialize
        for pnl, pos, sal in zip(self.hrSlotPanels, self.posLblList, self.posSalaryList):
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
            sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
            pnl.Init(pos, sal)
            
        # Set Hiring Spin Controls to appropriate limits
        self.cfo_pnl.quantity_sc.SetRange(0, 1)
        self.headMarketing_pnl.quantity_sc.SetRange(0, 1)
        self.custService_pnl.quantity_sc.SetRange(0, 1)
        self.qualityCtrl_pnl.quantity_sc.SetRange(0, 1)
        self.packager_pnl.quantity_sc.SetRange(0, 3)
        
        #--#
        self.SetSizer(sizer)
        
        self.ceo_pnl.SetCEO()
        
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Initializes the HRDesc Panel.'''
        self.year = year
        # Set the per person expenses to the correct level
        self.posSalaryList = Z_mrktInfo.getHRCosts(self.year)
        for pnl, salary in zip(self.hrSlotPanels, self.posSalaryList):
            pnl.totPP = salary
            pnl.totPP_st.SetLabel("$ "+format(salary, ',d'))
        self.ceo_pnl.SetCEO()
        
        # If year != 1, make sure they have at least 1 packager
        if year != 1 and self.packager_pnl.quantity_sc.GetValue() == 0:
                self.packager_pnl.quantity_sc.SetRange(1, 3)
                self.packager_pnl.quantity_sc.SetValue(1)
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current HR decisions.'''
        rslt = []
        for pnl in self.hrSlotPanels:
            rslt.append(pnl.quantity_sc.GetValue())
        return rslt
     
    #----------------------------------------------------------------------
    def SetHires(self):
        '''Sets up the quantity values to the hiring decisions for last round,
        or zero for the first round.'''
        if self.year == 1:
            for x in self.hrSlotPanels[1:]:
                x.quantity_sc.SetValue(0)
                x.OnHire(None)
        else:
            hires = self.data.GetData1()[22:33]
            for pos, qt in zip(self.hrSlotPanels[1:], hires):
                pos.quantity_sc.SetValue(qt[self.year-1])
                pos.OnHire(None)
        
#--------------------------------------------------------------------------
# HUMAN RESOURCES TOOLS PANEL
#--------------------------------------------------------------------------

class HRTools_Pnl(scrolled.ScrolledPanel):
    '''This panel shows the market summary information for the 
    Human Resources Decision, and holds the HR Decisions Panel'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        self.year = 1
        self.panelNum = 4
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Production Decisions Box Sizer ----------------------------------
        self.hrDesc_pnl = HRDesc_Pnl(self, -1)
        sizer.Add(self.hrDesc_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        self.Layout()
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the panel with the correct content for the 
        year and panel number.'''
        self.year = year
        self.hrDesc_pnl.Init(self.year)
        self.hrDesc_pnl.SetHires()
        
        self.hrDesc_pnl.Hide()
        if year > 2:
            self.hrDesc_pnl.Show()
        self.Layout()
        self.SetupScrolling()
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def Round2HRSetup(self, fcastRev, aleCycs, lagerCycs):
        '''Automates the HR decisions for round 2.'''
        totalCycles = aleCycs + lagerCycs
        hrNums = Z_mrktInfo.BestHR(fcastRev, totalCycles)
        for slot, num in zip(self.hrDesc_pnl.hrSlotPanels, hrNums):
            slot.quantity_sc.SetValue(num)
            slot.OnHire(None)
    
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current HR decisions.'''
        hr =  self.hrDesc_pnl.ReturnInfo()
        
        ceo = ['CEOs', hr[0], hr[0], hr[0], hr[0], hr[0], hr[0]]
        cfo = ['CFO/Accountants', hr[1], hr[1], hr[1], hr[1], hr[1], hr[1]]
        manager = ['Managers', hr[2], hr[2], hr[2], hr[2], hr[2], hr[2]]
        asstManager = ['Asst. Managers', hr[3], hr[3], hr[3], hr[3], hr[3], hr[3]]
        headMarketing = ['Head of Marketings', hr[4], hr[4], hr[4], hr[4], hr[4], hr[4]]
        salesRep = ['Sales Reps', hr[5], hr[5], hr[5], hr[5], hr[5], hr[5]]
        custService = ['Customer Service Specs.', hr[6], hr[6], hr[6], hr[6], hr[6], hr[6]]
        qualityCtrl = ['Quality Ctrl. Specs.', hr[7], hr[7], hr[7], hr[7], hr[7], hr[7]]
        brewer = ['Brewers', hr[8], hr[8], hr[8], hr[8], hr[8], hr[8]]
        packager = ['Packagers', hr[9], hr[9], hr[9], hr[9], hr[9], hr[9]]
        driver = ['Drivers', hr[10], hr[10], hr[10], hr[10], hr[10], hr[10]]
        cleaner = ['Cleaners', hr[11], hr[11], hr[11], hr[11], hr[11], hr[11]]
        
        return [ceo, cfo, manager, asstManager, headMarketing, salesRep,
                custService, qualityCtrl, brewer, packager, driver, cleaner]
    
#--------------------------------------------------------------------------
# MAIN HUMAN RESOURCES PANEL
#--------------------------------------------------------------------------

class HR_Pnl(wx.Panel):
    '''This class combines the summary panel and the HRTools for the 
    HR panel.'''
    def __init__(self, parent, *args, **kwargs):
        super(HR_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        self.panelNum = 4
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.summary = G_summary.Summary_Pnl(self)
        sizer.Add(self.summary, 0, wx.EXPAND|wx.RIGHT, 10)
        
        self.hr = HRTools_Pnl(self)
        sizer.Add(self.hr, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
    #----------------------------------------------------------------------
    def Init(self, year):
        self.year = year
        self.summary.Init(self.year, self.panelNum)
        self.hr.Init(year)
        
    def Round2HRSetup(self, fcastRev, aleCycs, lagerCycs):
        self.hr.Round2HRSetup(fcastRev, aleCycs, lagerCycs)
        
    def ReturnInfo(self):
        return self.hr.ReturnInfo()