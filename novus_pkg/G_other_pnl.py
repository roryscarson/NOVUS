#!python
# -*- encoding: utf-8 -*-

# G_other_pnl.py

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
                   
This module contains panel class for the marketing expenditure,
product development expenditure, contests and prizes, and
local charity spending for the Novus Business Simulator.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import G_summary
import X_styles, X_utilities
import Q_data
from Q_language import GetPhrase

#--------------------------------------------------------------------------
# PRODUCTION DECISION PANEL
#--------------------------------------------------------------------------

class OtherDesc_Pnl(wx.Panel):
    '''Allows the team to make decisions for marketing, product development,
    contest and prizes and local charity spending.'''
    def __init__(self, parent, *args, **kwargs):
        super(OtherDesc_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Style ---------------------------------------------------------------
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Attributes ----------------------------------------------------------
        self.year = 0
        self.fcastRev = 0
        self.percChoices = ['0.00 %', '0.25 %', '0.50 %', '0.75 %', '1.00 %',
                            '1.25 %']
        self.percVals = [0.0000, 0.0025, 0.0050, 0.0075, 0.0100, 0.0125]
        
        # Labels --------------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('other_lbl', lang)
        self.fcastRev_lbl = GetPhrase('fcastRev_lbl', lang)
        self.percOfRev_lbl = GetPhrase('percOfRev_lbl', lang)
        self.amount_lbl = GetPhrase('amount_lbl', lang)
        self.totalAmt_lbl = GetPhrase('totalAmt_lbl', lang)
        self.marketing_lbl = GetPhrase('mrktSpend_lbl', lang)
        self.prodDev_lbl = GetPhrase('prodDev_lbl', lang)
        self.contestPrize_lbl = GetPhrase('contest_lbl', lang)
        self.charity_lbl = GetPhrase('charity_lbl', lang)

        # Sizer ---------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
            
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        self.fcastRev_st = wx.StaticText(self, -1, self.fcastRev_lbl)
        self.fcastRev_st.SetFont(self.style.h4_bi_font)
        sizer.Add(self.fcastRev_st, 0, wx.LEFT|wx.BOTTOM, 20)
        
        a_box = wx.BoxSizer()
        self.percOfRev_st = wx.StaticText(self, -1, self.percOfRev_lbl)
        self.amount_st = wx.StaticText(self, -1, self.amount_lbl)
        self.percOfRev_st.SetFont(self.style.h4_iu_font)
        self.amount_st.SetFont(self.style.h4_iu_font)
        a_box.Add(wx.StaticText(self, -1), 1, wx.LEFT|wx.RIGHT, 30)
        a_box.Add(self.percOfRev_st, 1, wx.RIGHT, 10)
        a_box.Add(self.amount_st, 1)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        
        b_box = wx.BoxSizer()
        self.marketing_st = wx.StaticText(self, -1, self.marketing_lbl)
        self.markPerc_cb = wx.ComboBox(self, -1, value='0.00 %', 
                                       choices=self.percChoices, size=(80, -1),
                                       style=wx.CB_READONLY)
        self.markAmt_st = wx.StaticText(self, -1, '$ 0')
        self.marketing_st.SetFont(self.style.h4_font)
        self.markPerc_cb.SetFont(self.style.h4_font)
        self.markAmt_st.SetFont(self.style.h4_font)
        b_box.Add(self.marketing_st, 1, wx.LEFT|wx.RIGHT, 10)
        b_box.Add(self.markPerc_cb, 1, wx.RIGHT, 30)
        b_box.Add(self.markAmt_st, 1)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        
        c_box = wx.BoxSizer()
        self.prodDev_st = wx.StaticText(self, -1, self.prodDev_lbl)
        self.prodDevPerc_cb = wx.ComboBox(self, -1, value='0.00 %', 
                                       choices=self.percChoices, size=(80, -1),
                                       style=wx.CB_READONLY)
        self.prodDevAmt_st = wx.StaticText(self, -1, '$ 0')
        self.prodDev_st.SetFont(self.style.h4_font)
        self.prodDevPerc_cb.SetFont(self.style.h4_font)
        self.prodDevAmt_st.SetFont(self.style.h4_font)
        c_box.Add(self.prodDev_st, 1, wx.LEFT|wx.RIGHT, 10)
        c_box.Add(self.prodDevPerc_cb, 1, wx.RIGHT, 30)
        c_box.Add(self.prodDevAmt_st, 1)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        
        d_box = wx.BoxSizer()
        self.contestPrize_st = wx.StaticText(self, -1, self.contestPrize_lbl)
        self.contestPrize_cb = wx.ComboBox(self, -1, value='0.00 %', 
                                       choices=self.percChoices, size=(80, -1),
                                       style=wx.CB_READONLY)
        self.contestPrizeAmt_st = wx.StaticText(self, -1, '$ 0')
        self.contestPrize_st.SetFont(self.style.h4_font)
        self.contestPrize_cb.SetFont(self.style.h4_font)
        self.contestPrizeAmt_st.SetFont(self.style.h4_font)
        d_box.Add(self.contestPrize_st, 1, wx.LEFT|wx.RIGHT, 10)
        d_box.Add(self.contestPrize_cb, 1, wx.RIGHT, 30)
        d_box.Add(self.contestPrizeAmt_st, 1)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        
        e_box = wx.BoxSizer()
        self.charity_st = wx.StaticText(self, -1, self.charity_lbl)
        self.charity_cb = wx.ComboBox(self, -1, value='0.00 %',
                                      choices = self.percChoices, size=(80, -1),
                                       style=wx.CB_READONLY)
        self.charityAmt_st = wx.StaticText(self, -1, '$ 0')
        self.charity_st.SetFont(self.style.h4_font)
        self.charity_cb.SetFont(self.style.h4_font)
        self.charityAmt_st.SetFont(self.style.h4_font)
        e_box.Add(self.charity_st, 1, wx.LEFT|wx.RIGHT, 10)
        e_box.Add(self.charity_cb, 1, wx.RIGHT, 30)
        e_box.Add(self.charityAmt_st, 1)
        sizer.Add(e_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        
        sizer.Add((-1, 10))
        
        f_box = wx.BoxSizer()
        self.total_st = wx.StaticText(self, -1, self.totalAmt_lbl+' - ')
        self.totalAmt_st = wx.StaticText(self, -1, '$ 0')
        self.total_st.SetFont(self.style.h4_b_font)
        self.totalAmt_st.SetFont(self.style.h4_b_font)
        f_box.Add(self.total_st, 0, wx.LEFT|wx.RIGHT, 10)
        f_box.Add(self.totalAmt_st, 0)
        sizer.Add(f_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_COMBOBOX, self.OnPerc)
        
    #----------------------------------------------------------------------
    def Init(self, year, fcastRev):
        '''Initializes the OtherDesc_Pnl, by setting the current year
        and forecasted revenue attributes.'''
        self.year = year
        self.UpdateFcast(fcastRev)
        
        
    #----------------------------------------------------------------------
    def UpdateFcast(self, fcastRev):
        '''Updates the forecasted revenue.'''
        self.fcastRev = int(fcastRev)
        self.fcastRev_st.SetLabel(self.fcastRev_lbl + ' - $ ' + format(self.fcastRev, ',d'))
    
    #----------------------------------------------------------------------
    def OnPerc(self, evt):
        '''When a percentage is changed, updates the amount and total amount.'''
        fieldDic = {self.markPerc_cb: self.markAmt_st, 
                    self.prodDevPerc_cb: self.prodDevAmt_st,
                    self.contestPrize_cb: self.contestPrizeAmt_st,
                    self.charity_cb: self.charityAmt_st}
        percent = evt.GetEventObject().GetValue()
        percent = self.percVals[self.percChoices.index(percent)]
        amount = int(self.fcastRev * percent)
        fieldDic[evt.GetEventObject()].SetLabel('$ '+format(amount, ',d'))
        self.UpdateTotal()
        
    #----------------------------------------------------------------------
    def UpdateTotal(self):
        '''Calculates the total "Other Spending" and sets the label for
        total other spending.'''
        m = int(self.markAmt_st.GetLabel().split(' ')[-1].replace(',', ''))
        pd = int(self.prodDevAmt_st.GetLabel().split(' ')[-1].replace(',', ''))
        cp = int(self.contestPrizeAmt_st.GetLabel().split(' ')[-1].replace(',', ''))
        ch = int(self.charityAmt_st.GetLabel().split(' ')[-1].replace(',', ''))
        total = m + pd + cp + ch
        self.totalAmt_st.SetLabel('$ '+format(total, ',d'))
        
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets all the other spending fields to 0.00 %'''
        self.markPerc_cb.SetValue('0.00 %')
        self.prodDevPerc_cb.SetValue('0.00 %')
        self.contestPrize_cb.SetValue('0.00 %')
        self.charity_cb.SetValue('0.00 %')
        self.markAmt_st.SetLabel('$ 0')
        self.prodDevAmt_st.SetLabel('$ 0')
        self.contestPrizeAmt_st.SetLabel('$ 0')
        self.charityAmt_st.SetLabel('$ 0')
        self.totalAmt_st.SetLabel('$ 0')
                                      
#--------------------------------------------------------------------------
# OTHER SPENDING TOOLS PANEL
#--------------------------------------------------------------------------

class OtherTools_Pnl(scrolled.ScrolledPanel):
    '''This panel allows the team to make their marketing,
    product development, contests and prizes, and local charity
    spending decisions for rounds 2 - 6.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        self.year = 1
        self.panelNum = 5
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.otherDesc_pnl = OtherDesc_Pnl(self, -1)
        sizer.Add(self.otherDesc_pnl, 0, wx.EXPAND)
        
        #--#
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the panel with the correct content for the 
        year and panel number.'''
        self.year = year
        self.otherDesc_pnl.Reset()
        self.otherDesc_pnl.Hide()
        if year > 1:
            self.otherDesc_pnl.Show()
        self.Layout()
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def UpdateFcast(self, Fcast):
        '''Updates the Forecasted Revenue.'''
        self.otherDesc_pnl.UpdateFcast(Fcast)
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current Other Spending decisions.'''
        mk = float(self.otherDesc_pnl.markPerc_cb.GetValue().split(' ')[0])
        pd = float(self.otherDesc_pnl.prodDevPerc_cb.GetValue().split(' ')[0])
        cp = float(self.otherDesc_pnl.contestPrize_cb.GetValue().split(' ')[0])
        lc = float(self.otherDesc_pnl.charity_cb.GetValue().split(' ')[0])
        mk2 = ['Marketing', mk, mk, mk, mk, mk, mk]
        pd2 = ['Product Development', pd, pd, pd, pd, pd, pd]
        cp2 = ['Promotional Activity', cp, cp, cp, cp, cp, cp]
        lc2 = ['Community Development', lc, lc, lc, lc, lc, lc]
        return [mk2, pd2, cp2, lc2]
        
#--------------------------------------------------------------------------
# OTHER SPENDING PANEL
#--------------------------------------------------------------------------

class Other_Pnl(wx.Panel):
    '''This class combines the summary panel and the other spending
    tools panel.'''
    def __init__(self, parent, *args, **kwargs):
        super(Other_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        self.panelNum = 5
        
        sizer = wx.BoxSizer()
        
        self.summary = G_summary.Summary_Pnl(self)
        sizer.Add(self.summary, 0, wx.EXPAND|wx.RIGHT, 10)
        
        self.other = OtherTools_Pnl(self)
        sizer.Add(self.other, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
    def Init(self, year):
        self.year = year
        self.summary.Init(self.year, self.panelNum)
        self.other.Init(self.year)
        
    def UpdateFcast(self, Fcast):
        self.other.UpdateFcast(Fcast)
        
    def ReturnInfo(self):
        return self.other.ReturnInfo()