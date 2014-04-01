#!python
# -*- encoding: utf-8 -*-

# G_finance_pnl.py

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
                   
This module contains panel class for the finance
decisions for the Novus Business Simulator.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import G_summary
import Q_data
import X_styles, X_utilities
import Z_gameIO
from Q_language import GetPhrase

#--------------------------------------------------------------------------
# LONG TERM DEBT PANEL
#--------------------------------------------------------------------------

class LTD_Pnl(wx.Panel):
    '''Allows the user to enter an amount of long term debt.'''
    def __init__(self, parent, *args, **kwargs):
        super(LTD_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        
        self.style = X_styles.NovusStyle(None)
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('ltd_lbl', lang)
        self.amount_lbl = GetPhrase('amountBorrowed_lbl', lang)
        self.interest_lbl = GetPhrase('interestRate_lbl', lang)
        self.period_lbl = GetPhrase('paybackPeriod_lbl', lang)
        self.years_lbl = GetPhrase('years_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        a_box = wx.BoxSizer()
        self.debt_st = wx.StaticText(self, -1, self.amount_lbl+' ($)')
        self.amount_st = wx.StaticText(self, -1, '$ 0')
        self.debt_st.SetFont(self.style.h4_font)
        self.amount_st.SetFont(self.style.h4_b_font)
        a_box.Add(self.debt_st, 1, wx.RIGHT, 10)
        a_box.Add(self.amount_st, 1, wx.RIGHT, 10)
        a_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        sizer.Add((-1, 10))
        
        b_box = wx.BoxSizer()
        self.slider = wx.Slider(self, -1, value=0, minValue=0, maxValue=2000000)
        b_box.Add(self.slider, 2, wx.RIGHT, 10)
        b_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        sizer.Add((-1, 10))
        
        c_box = wx.BoxSizer()
        self.interest_st = wx.StaticText(self, -1, self.interest_lbl + ' - ')
        self.rate_st = wx.StaticText(self, -1)
        self.interest_st.SetFont(self.style.h4_font)
        self.rate_st.SetFont(self.style.h4_font)
        c_box.Add(self.interest_st, 1, wx.RIGHT, 10)
        c_box.Add(self.rate_st, 1, wx.RIGHT, 10)
        c_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        d_box = wx.BoxSizer()
        self.period_st = wx.StaticText(self, -1, self.period_lbl + ' - ')
        self.time_st = wx.StaticText(self, -1)
        self.period_st.SetFont(self.style.h4_font)
        self.time_st.SetFont(self.style.h4_font)
        d_box.Add(self.period_st, 1, wx.RIGHT, 10)
        d_box.Add(self.time_st, 1, wx.RIGHT, 10)
        d_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SLIDER, self.OnBorrow)
    
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the long term debt panel.'''
        self.year = year
        self.slider.SetValue(0)
        self.amount_st.SetLabel('$ 0')
    
    #----------------------------------------------------------------------
    def OnBorrow(self, evt):
        '''Calculates the interest rate and the payback period when the 
        user selects a borrowing amount.'''
        amount = X_utilities.roundto(self.slider.GetValue(), 250)
        if self.year < 4:
            self.amount_st.SetLabel('$ ' + format(amount, ',d'))
            if amount <= 500000:
                self.rate_st.SetLabel('8 %')
                self.time_st.SetLabel('3 ' + self.years_lbl)
            elif amount > 500000 and amount <=1000000:
                self.rate_st.SetLabel('10 %')
                self.time_st.SetLabel('5 ' + self.years_lbl)
            elif amount > 1000000 and amount <=1500000:
                self.rate_st.SetLabel('12 %')
                self.time_st.SetLabel('7 ' + self.years_lbl)
            elif amount > 1500000 and amount <=2000000:
                self.rate_st.SetLabel('14 %')
                self.time_st.SetLabel('9 ' + self.years_lbl)
            else:
                self.rate_st.SetLabel('')
                self.time_st.SetLabel('')
        
        else:
            # Get the average LoC rate for Years 1 - 3
            avgLoc = 0
            for x in self.data.GetData1()[65][1:4]:
                avgLoc += (1/3.0) * Z_gameIO.GetLoCRate(x) * 100.0
    
            self.amount_st.SetLabel('$ ' + format(amount, ',d'))
            
            if amount <= 500000:
                r = avgLoc + 5.0
                self.rate_st.SetLabel("%.2f %%" % r)
                self.time_st.SetLabel('5 ' + self.years_lbl)
            elif amount > 500000 and amount <=1000000:
                r = avgLoc + 7.50
                self.rate_st.SetLabel("%.2f %%" % r)
                self.time_st.SetLabel('6 ' + self.years_lbl)
            elif amount > 1000000 and amount <=1500000:
                r = avgLoc + 10.00
                self.rate_st.SetLabel("%.2f %%" % r)
                self.time_st.SetLabel('7 ' + self.years_lbl)
            elif amount > 1500000 and amount <=2000000:
                r = avgLoc + 12.50
                self.rate_st.SetLabel("%.2f %%" % r)
                self.time_st.SetLabel('8 ' + self.years_lbl)
            else:
                self.rate_st.SetLabel('')
                self.time_st.SetLabel('')
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current LTD decision.'''
        draw = X_utilities.roundto(self.slider.GetValue(), 250)
        if self.rate_st.GetLabel():
            rate = float(self.rate_st.GetLabel().split(' ')[0])
        else:
            rate = 0
        if self.time_st.GetLabel():
            time = float(self.time_st.GetLabel().split(' ')[0])
        else:
            time = 0
        return [draw, rate, int(time)]
        
#--------------------------------------------------------------------------
# EQUITY PANEL
#--------------------------------------------------------------------------

class Equity_Pnl(wx.Panel):
    '''Allows the user to enter an amount of Equity financing.'''
    def __init__(self, parent, *args, **kwargs):
        super(Equity_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        
        self.style = X_styles.NovusStyle(None)
        
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('equity_title', lang)
        self.amount_lbl = GetPhrase('equityAmount_lbl', lang)
        self.shares_lbl = GetPhrase('shares_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        a_box = wx.BoxSizer()
        self.equity_st = wx.StaticText(self, -1, self.amount_lbl+' ($)')
        self.amount_st = wx.StaticText(self, -1, '$ 0')
        self.equity_st.SetFont(self.style.h4_font)
        self.amount_st.SetFont(self.style.h4_b_font)
        a_box.Add(self.equity_st, 1, wx.RIGHT, 10)
        a_box.Add(self.amount_st, 1, wx.RIGHT, 10)
        a_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        sizer.Add((-1, 10))
        
        b_box = wx.BoxSizer()
        self.slider = wx.Slider(self, -1, value=0, minValue=0, maxValue=1000000)
        b_box.Add(self.slider, 2, wx.RIGHT, 10)
        b_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        sizer.Add((-1, 10))
        
        c_box = wx.BoxSizer()
        self.shares_st = wx.StaticText(self, -1, self.shares_lbl + ' - ')
        self.shareNum_st = wx.StaticText(self, -1, '-')
        self.shares_st.SetFont(self.style.h4_font)
        self.shareNum_st.SetFont(self.style.h4_font)
        c_box.Add(self.shares_st, 1, wx.RIGHT, 10)
        c_box.Add(self.shareNum_st, 1, wx.RIGHT, 10)
        c_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SLIDER, self.OnEquity)
    
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the long term debt panel.'''
        self.year = year
        self.slider.SetValue(0)

    #----------------------------------------------------------------------
    def OnEquity(self, evt):
        '''Gets the current value from the slider and sets the value
        of the equity amount label.'''
        equity = self.slider.GetValue()
        equity = X_utilities.roundto(equity, 250)
        self.shareNum_st.SetLabel(format(equity, ',d'))
        self.amount_st.SetLabel('$ ' + format(equity, ',d'))
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current Equity decision.'''
        return [X_utilities.roundto(self.slider.GetValue(), 250)]
    
#--------------------------------------------------------------------------
# SHORT TERM DEBT PANEL
#--------------------------------------------------------------------------

class STD_Pnl(wx.Panel):
    '''Allows the user to enter an amount of short term debt.'''
    def __init__(self, parent, *args, **kwargs):
        super(STD_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        self.drawLimit = 0
        self.rate = 0
        self.style = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('shortTermDebt_lbl', lang)
        self.limit_lbl = GetPhrase('borrowLimit_lbl', lang)
        self.draw_lbl = GetPhrase('drawdown_lbl', lang)
        self.interest_lbl = GetPhrase('interestRate_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.style.h2_font)
        sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        a_box = wx.BoxSizer()
        self.limit_st = wx.StaticText(self, -1, self.limit_lbl+' ($)')
        self.limitVal_st = wx.StaticText(self, -1, '$ -')
        self.limit_st.SetFont(self.style.h4_font)
        self.limitVal_st.SetFont(self.style.h4_font)
        a_box.Add(self.limit_st, 1, wx.RIGHT, 10)
        a_box.Add(self.limitVal_st, 1, wx.RIGHT, 10)
        a_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        b_box = wx.BoxSizer()
        self.draw_st = wx.StaticText(self, -1, self.draw_lbl + ' - ')
        self.drawVal_st = wx.StaticText(self, -1, '$ 0')
        self.draw_st.SetFont(self.style.h4_font)
        self.drawVal_st.SetFont(self.style.h4_b_font)
        b_box.Add(self.draw_st, 1, wx.RIGHT, 10)
        b_box.Add(self.drawVal_st, 1, wx.RIGHT, 10)
        b_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        sizer.Add((-1, 10))
        
        c_box = wx.BoxSizer()
        self.slider = wx.Slider(self, -1, value=0, minValue=0, maxValue=2000000)
        c_box.Add(self.slider, 2, wx.RIGHT, 10)
        c_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        sizer.Add((-1, 10))
        
        d_box = wx.BoxSizer()
        self.interest_st = wx.StaticText(self, -1, self.interest_lbl + ' - ')
        self.rate_st = wx.StaticText(self, -1)
        self.interest_st.SetFont(self.style.h4_font)
        self.rate_st.SetFont(self.style.h4_font)
        d_box.Add(self.interest_st, 1, wx.RIGHT, 10)
        d_box.Add(self.rate_st, 1, wx.RIGHT, 10)
        d_box.Add(wx.StaticText(self, -1), 2)
        sizer.Add(d_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)
        
        #--#
        self.SetSizer(sizer)    

        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_SLIDER, self.OnBorrow)
        
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the short term finance panel.'''
        self.year = year
        if year < 3:
            self.slider.SetRange(0, 0)
            self.limitVal_st.SetLabel('$ 0')
            return False
        
        # Get AR, Inventory and Net Fixed Assets
        accountsRec = self.data.GetData1()[59][self.year-1]
        inventory = self.data.GetData1()[60][self.year-1]
        grossFixedAssets = self.data.GetData1()[61][self.year-1]
        depreciation = self.data.GetData1()[62][self.year-1]
        netFixedAssets = grossFixedAssets - depreciation
        self.drawLimit = int(accountsRec*0.5+inventory*0.25+netFixedAssets*0.1)
        self.drawLimit = X_utilities.roundto(self.drawLimit, 100)
        self.slider.SetRange(0, self.drawLimit)
        self.limitVal_st.SetLabel("$ " + format(self.drawLimit, ',d'))
        
        # Get Starting STB Amount
        lastDraw = self.data.GetData1()[14][year-1]
        
        # If the starting STB amount is greater than the draw limit,
        #       set the limit to the maximum allowed. Otherwise, set
        #       the draw to the previous year's amount.
        if lastDraw < self.drawLimit:
            self.slider.SetValue(lastDraw)
        else:
            self.slider.SetValue(self.drawLimit)
        
        self.OnBorrow(None)
        
    #----------------------------------------------------------------------
    def OnBorrow(self, evt):
        '''Gets a borrowing amount and sets the borrowing label.'''
        draw = X_utilities.roundto(self.slider.GetValue(), 100)
        self.drawVal_st.SetLabel('$ ' + format(draw, ',d'))
        if draw >= self.drawLimit*0.5:
            self.rate = 6.50
        elif draw > 0 and draw < self.drawLimit*0.5:
            self.rate = 3.50
        else:
            self.rate = 0
        self.rate_st.SetLabel("%.2f %%" % (self.rate,))
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns the current STD decision.'''
        draw = X_utilities.roundto(self.slider.GetValue(), 100)
        if self.rate_st.GetLabel():
            rate = float(self.rate_st.GetLabel().split(' ')[0])
        else:
            rate = 0
        return [draw, rate]
        
#--------------------------------------------------------------------------
# TOTAL CAPITAL PURCHASES
#--------------------------------------------------------------------------
class CapPurchTotal_Pnl(wx.Panel):
    '''This panel shows the total amount of capital purchases for the current
    round. If the total capital purchases equal zero, then the panel will
    hide itself. If the total capital pruchases are greater than zero, the
    panel will show itself.'''
    def __init__(self, parent, *args, **kwargs):
        super(CapPurchTotal_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('capExp_title', lang)
        self.totalME_lbl = GetPhrase('totalME_lbl', lang)
        self.totalPE_lbl = GetPhrase('totalPE_lbl', lang)
        self.totalCP_lbl = GetPhrase('totalCP_lbl', lang)
        
        # Sizer -----------------------------------------------------------
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.styles.h2_font)
        
        self.totalME_st = wx.StaticText(self, -1, self.totalME_lbl)
        self.totalPE_st = wx.StaticText(self, -1, self.totalPE_lbl)
        self.totalCP_st = wx.StaticText(self, -1, self.totalCP_lbl)
        
        self.totalME_st.SetFont(self.styles.h3_font)
        self.totalPE_st.SetFont(self.styles.h3_font)
        self.totalCP_st.SetFont(self.styles.h3_b_font)
        
        self.me_amt = wx.StaticText(self, -1, '$ 0')
        self.pe_amt = wx.StaticText(self, -1, '$ 0')
        self.cp_amt = wx.StaticText(self, -1, '$ 0')
        
        self.me_amt.SetFont(self.styles.h3_font)
        self.pe_amt.SetFont(self.styles.h3_font)
        self.cp_amt.SetFont(self.styles.h3_b_font)
                                    
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        a_box = wx.BoxSizer()
        a_box.Add(self.totalME_st, 1, wx.RIGHT, 10)
        a_box.Add(self.me_amt, 0)
        a_box.AddStretchSpacer(1)
        
        b_box = wx.BoxSizer()
        b_box.Add(self.totalPE_st, 1, wx.RIGHT, 10)
        b_box.Add(self.pe_amt, 0)
        b_box.AddStretchSpacer(1)
        
        c_box = wx.BoxSizer()
        c_box.Add(self.totalCP_st, 1, wx.RIGHT, 10)
        c_box.Add(self.cp_amt, 0)
        c_box.AddStretchSpacer(1)
        
        self.sizer.Add(self.title_st, 0, wx.LEFT|wx.TOP, 10)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        self.sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        self.sizer.Add(b_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
        self.sizer.Add(c_box, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
            
        self.SetSizer(self.sizer)
    
    #----------------------------------------------------------------------
    def SetCapExp(self, manEquip, packEquip):
        '''Init(int manEquip, int packEquip)
        This will take the manufacturing equipment and packaging 
        equipment expenditures for the round and initialize the panel.'''
        
        total = manEquip + packEquip
        self.me_amt.SetLabel('$ ' + format(manEquip, ','))
        self.pe_amt.SetLabel('$ ' + format(packEquip, ','))
        self.cp_amt.SetLabel('$ ' + format(total, ','))
    
#--------------------------------------------------------------------------
# FINANCE TOOLS PANEL
#--------------------------------------------------------------------------

class FinanceTools_Pnl(scrolled.ScrolledPanel):
    '''This panel shows the long term debt, equity, and short
    term financing options for the game.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        self.year = 1
        self.panelNum = 2
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Total Capital Purchases -----------------------------------------
        self.cpt_pnl = CapPurchTotal_Pnl(self, -1)
        sizer.Add(self.cpt_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Long Term Debt Panel --------------------------------------------
        self.ltd_pnl = LTD_Pnl(self, -1)
        sizer.Add(self.ltd_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Equity Panel ----------------------------------------------------
        self.equity_pnl = Equity_Pnl(self, -1)
        sizer.Add(self.equity_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Short Term Borrowing Panel --------------------------------------
        self.std_pnl = STD_Pnl(self, -1)
        sizer.Add(self.std_pnl, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        #--#
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the panels for the Main Finance panel.'''
        self.year = year
        self.ltd_pnl.Init(year)
        self.equity_pnl.Init(year)
        self.std_pnl.Init(year)
        
        self.cpt_pnl.Hide()
        self.ltd_pnl.Hide()
        self.equity_pnl.Hide()
        self.std_pnl.Hide()
        
        if year == 1 or year == 4:
            self.ltd_pnl.Show()
            self.cpt_pnl.Show()
        if year == 1:
            self.equity_pnl.Show()
        if year > 2:
            self.std_pnl.Show()
        self.Layout()
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def ReturnInfo(self):
        '''Returns a list of the current finance decisions.'''
        ltd = self.ltd_pnl.ReturnInfo()
        eqi = self.equity_pnl.ReturnInfo()
        std = self.std_pnl.ReturnInfo()
        
        # Reformat the lists to conform with the TeamData1.csv file formatting
        ltd2 = ['Year 1 Debt, Rate, Payback', ltd[0], ltd[1], ltd[2]]
        eqi2 = ['Year 1 Equity, Shares', eqi[0], eqi[0]]
        ltd3 = ['Year 4 Debt, Rate, Payback', ltd[0], ltd[1], ltd[2]]
        std2 = ['Short Term Borrowing Draw', std[0], std[0], std[0], std[0], std[0], std[0]]
        std3 = ['Short Term Borrowing Rate', std[1], std[1], std[1], std[1], std[1], std[1]]
        return [ltd2, eqi2, ltd3, std2, std3]
        
#--------------------------------------------------------------------------
# FINANCE TOOLS PANEL
#--------------------------------------------------------------------------

class Finance_Pnl(wx.Panel):
    '''Contains the finance tools panel and the finance summary panel.'''
    def __init__(self, parent, *args, **kwargs):
        super(Finance_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 1
        self.panelNum = 2
        
        sizer = wx.BoxSizer()
        
        self.summary = G_summary.Summary_Pnl(self)
        sizer.Add(self.summary, 0, wx.EXPAND|wx.RIGHT, 10)
        
        self.finance = FinanceTools_Pnl(self)
        sizer.Add(self.finance, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
    def Init(self, year):
        self.year = year
        self.summary.Init(self.year, self.panelNum)
        self.finance.Init(self.year)
    
    def ReturnInfo(self):
        return self.finance.ReturnInfo()
        
    def SetCapExp(self, manu_exp, pack_exp):
        self.finance.cpt_pnl.SetCapExp(manu_exp, pack_exp)