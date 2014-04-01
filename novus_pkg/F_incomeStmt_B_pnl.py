#!python
# -*- encoding: utf-8 -*-

# F_incomeStmt_B_pnl.py

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
                              + E_finance_pnl.py +
                                                 + F_incomeStmt_B_pnl.py
                                                 + F_balanceSheet_B_pnl.py
                                                 + F_cashFlow_B_pnl.py

This module contains the Income Statement "B" Panel class code for the Novus 
Business and IT education program. The "B" panel show the 
pro forma results for this year, and, after the submission of decisions,
the actual results for the round.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import X_styles, X_miscPnls
import Q_data
from Q_language import GetPhrase

class IncomeStmt_B_Pnl(scrolled.ScrolledPanel):
    '''This class holds the Income Statement panel for the Novus Business and IT 
    education program.'''
    def __init__(self, parent, *args, **kwargs):
        scrolled.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        self.SetBackgroundColour(wx.WHITE)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.incomeStmt_lbl = GetPhrase('incomeStmt_lbl', lang)
        self.detail_lbl = GetPhrase('detail_lbl', lang)
        self.forecast_lbl = GetPhrase('forecast_lbl', lang)
        self.actual_lbl = GetPhrase('actual_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.keg_lbl = GetPhrase('keg_lbl', lang)
        self.bottle_lbl = GetPhrase('bottle_lbl', lang)
        self.can_lbl = GetPhrase('can_lbl', lang)
        self.revenue_lbl = GetPhrase('revenue_lbl', lang)
        self.totalRevenue_lbl = GetPhrase('totalRevenue_lbl', lang)
        self.cogs_lbl = GetPhrase('cogs_lbl', lang)
        self.totalCogs_lbl = GetPhrase('totalCogs_lbl', lang)
        
        # Special COGS
        self.invSpoilExp_lbl = GetPhrase('invSpoilExp_lbl', lang)
        self.overProdExp_lbl = GetPhrase('overProdExp_lbl', lang)
        
        # Adjusted COGS
        self.adjCogs_lbl = GetPhrase('adjCogs_lbl', lang)
        self.totalAdjCogs_lbl = GetPhrase('totalAdjCogs_lbl', lang)
        
        self.grossIncome_lbl = GetPhrase('grossIncome_lbl', lang)
        self.totalGrossIncome_lbl = GetPhrase('totalGrossIncome_lbl', lang)
        self.grossMargin_lbl = GetPhrase('grossMargin_lbl', lang)
        self.totalGrossMargin_lbl = GetPhrase('totalGrossMargin_lbl', lang)
        self.opExp_lbl = GetPhrase('opExp_lbl', lang)
        self.totalOpExp_lbl = GetPhrase('totalOpExp_lbl', lang)
        self.salaryWages_lbl = GetPhrase('salaryWages_lbl', lang)
        self.rent_lbl = GetPhrase('rent_lbl', lang)
        self.utilities_lbl = GetPhrase('utilities_lbl', lang)
        self.fuelExp_lbl = GetPhrase('fuelExp_lbl', lang)
        self.marketingExp_lbl = GetPhrase('marketingExp_lbl', lang)
        self.prodDevExp_lbl = GetPhrase('prodDevExp_lbl', lang)
        self.otherExp_lbl = GetPhrase('otherExp_lbl', lang)
        self.ebitda_lbl = GetPhrase('ebitda_lbl', lang)
        self.depAmt_lbl = GetPhrase('depAmt_lbl', lang)
        self.ebit_lbl = GetPhrase('ebit_lbl', lang)
        self.intIncome_lbl = GetPhrase('intIncome_lbl', lang)
        self.intExp_lbl = GetPhrase('intExp_lbl', lang)
        self.ebt_lbl = GetPhrase('ebt_lbl', lang)
        self.taxes_lbl = GetPhrase('taxes_lbl', lang)
        self.netIncome_lbl = GetPhrase('netIncome_lbl', lang)
        self.sharesOut_lbl = GetPhrase('sharesOut_lbl', lang)
        self.eps_lbl = GetPhrase('eps_lbl', lang)
        
        
        # Create Income Statement List Objects: Eash list corresponds to 
        #       a single IS line item, with 7 items: a title and one value
        #       for each year
        #------------------------------------------------------------------
        self.yearList = [self.incomeStmt_lbl, self.forecast_lbl, self.actual_lbl]
        # Revenue --
        self.revenue_list = [self.revenue_lbl, '', '']
        self.rev_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-']
        self.rev_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-']
        self.rev_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-']
        self.rev_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-']
        self.rev_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-']
        self.rev_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-']
        self.totalRevenue_list = [self.totalRevenue_lbl, '-', '-']
        
        # COGS --
        self.cogs_list = [self.cogs_lbl, '', '']
        self.cogs_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-']
        self.cogs_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-']
        self.cogs_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-']
        self.cogs_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-']
        self.cogs_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-']
        self.cogs_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-']
        self.totalCogs_list = [self.totalCogs_lbl, '-', '-']
        
        # Special COGS
        self.invSpoilExp_list = ['   '+self.invSpoilExp_lbl, '-', '-']
        self.overProdExp_list = ['   '+self.overProdExp_lbl, '-', '-']
        
        # Adjusted COGS --
        self.adjCogs_list = [self.adjCogs_lbl, '', '']
        self.adjCogs_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-']
        self.adjCogs_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-']
        self.adjCogs_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-']
        self.adjCogs_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-']
        self.adjCogs_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-']
        self.adjCogs_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-']
        self.totalAdjCogs_list = [self.totalAdjCogs_lbl, '-', '-']
        
        # Gross Income --
        self.grossIncome_list = [self.grossIncome_lbl, '', '']
        self.grossIncome_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-']
        self.grossIncome_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-']
        self.grossIncome_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-']
        self.grossIncome_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-']
        self.grossIncome_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-']
        self.grossIncome_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-']
        self.totalGrossIncome_list = [self.totalGrossIncome_lbl, '-', '-']
        
        # Gross Margin --
        self.grossMargin_list = [self.grossMargin_lbl, '', '']
        self.grossMargin_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-']
        self.grossMargin_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-']
        self.grossMargin_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-']
        self.grossMargin_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-']
        self.grossMargin_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-']
        self.grossMargin_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-']
        self.totalGrossMargin_list = [self.totalGrossMargin_lbl, '-', '-']
        
        # Operating Expenses -- 
        self.salaryWages_list = ['   '+self.salaryWages_lbl, '-', '-']
        self.rent_list = ['   '+self.rent_lbl, '-', '-']
        self.utilities_list = ['   '+self.utilities_lbl, '-', '-']
        self.fuelExp_list = ['   '+self.fuelExp_lbl,'-', '-', '-', '-', '-', '-']
        self.marketingExp_list = ['   '+self.marketingExp_lbl, '-', '-']
        self.prodDevExp_list = ['   '+self.prodDevExp_lbl, '-', '-']
        self.otherExp_list = ['   '+self.otherExp_lbl, '-', '-']
        self.totalOpExp_list = [self.totalOpExp_lbl, '-', '-']
        
        # EBITDA, EBIT, EBT, NI --
        self.ebitda_list = [self.ebitda_lbl, '-', '-']
        self.depAmt_list = ['   '+self.depAmt_lbl, '-', '-']
        self.ebit_list = [self.ebit_lbl, '-', '-']
        self.intIncome_list = ['   '+self.intIncome_lbl, '-', '-']
        self.intExp_list = ['   '+self.intExp_lbl, '-', '-']
        self.ebt_list = [self.ebt_lbl, '-', '-']
        self.taxes_list = ['   '+self.taxes_lbl, '-', '-']
        self.netIncome_list = [self.netIncome_lbl, '-', '-']
        self.sharesOut_list = [self.sharesOut_lbl, '-', '-']
        self.eps_list = [self.eps_lbl, '-', '-']
        
        self.IS_fields = [self.yearList, self.revenue_list, self.rev_AK_list, self.rev_AB_list, self.rev_AC_list,
                        self.rev_LK_list, self.rev_LB_list, self.rev_LC_list, self.totalRevenue_list,
                        self.cogs_list, self.cogs_AK_list, self.cogs_AB_list, self.cogs_AC_list,
                        self.cogs_LK_list, self.cogs_LB_list, self.cogs_LC_list, self.totalCogs_list,
                        # Special COGS
                        self.invSpoilExp_list, self.overProdExp_list,
                        # Adjusted COGS
                        self.adjCogs_list, self.adjCogs_AK_list, self.adjCogs_AB_list, self.adjCogs_AC_list,
                        self.adjCogs_LK_list, self.adjCogs_LB_list, self.adjCogs_LC_list, self.totalAdjCogs_list,
                        
                        self.grossIncome_list, self.grossIncome_AK_list, self.grossIncome_AB_list, self.grossIncome_AC_list,
                        self.grossIncome_LK_list, self.grossIncome_LB_list, self.grossIncome_LC_list, self.totalGrossIncome_list,
                        self.grossMargin_list, self.grossMargin_AK_list, self.grossMargin_AB_list, self.grossMargin_AC_list,
                        self.grossMargin_LK_list, self.grossMargin_LB_list, self.grossMargin_LC_list, self.totalGrossMargin_list,
                        self.salaryWages_list, self.rent_list, self.utilities_list, self.fuelExp_list,
                        self.marketingExp_list, self.prodDevExp_list, self.otherExp_list, self.totalOpExp_list,
                        self.ebitda_list, self.depAmt_list, self.ebit_list, self.intIncome_list, self.intExp_list,
                        self.ebt_list, self.taxes_list, self.netIncome_list,
                        self.sharesOut_list, self.eps_list]
        
        # Formatting Lists ------------------------------------------------
        self.bold_list = [self.revenue_list, self.totalRevenue_list, self.cogs_list, self.totalCogs_list,
                          self.adjCogs_list, self.totalAdjCogs_list,
                        self.grossIncome_list, self.totalGrossIncome_list, self.grossMargin_list, 
                        self.totalGrossMargin_list, self.totalOpExp_list, self.ebitda_list, self.ebit_list, 
                        self.ebt_list, self.netIncome_list]
        
        self.italic_list = [self.rev_AK_list, self.rev_AB_list, self.rev_AC_list, self.rev_LK_list, 
                        self.rev_LB_list, self.rev_LC_list, self.cogs_AK_list, self.cogs_AB_list, 
                        self.cogs_AC_list, self.cogs_LK_list, self.cogs_LB_list, self.cogs_LC_list,
                        self.adjCogs_AK_list, self.adjCogs_AB_list, self.adjCogs_AC_list,
                        self.adjCogs_LK_list, self.adjCogs_LB_list, self.adjCogs_LC_list, 
                        self.grossIncome_AK_list, self.grossIncome_AB_list, self.grossIncome_AC_list, self.grossIncome_LK_list, 
                        self.grossIncome_LB_list, self.grossIncome_LC_list, self.grossMargin_AK_list, self.grossMargin_AB_list, 
                        self.grossMargin_AC_list, self.grossMargin_LK_list, self.grossMargin_LB_list, self.grossMargin_LC_list, 
                        self.eps_list]
        
        #------------------------------------------------------------------
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        self.detail_cb = wx.CheckBox(self, -1, self.detail_lbl, size=(120, -1),
                                     pos=(15, 15))
        self.detail_cb.SetFont(self.styles.h4_font)
        self.detail_cb.SetValue(False)
        self.incomeStmt_st = wx.StaticText(self, -1, self.incomeStmt_lbl)
        self.incomeStmt_st.SetFont(self.styles.h1_font)
        sizer.Add(self.incomeStmt_st, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        
        # Add in Income Statement Fields (IS_fields) ----------------------
        self.year_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.revenue_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rev_AK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rev_AB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rev_AC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rev_LK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rev_LB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rev_LC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.totalRevenue_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        
        self.cogs_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.cogs_AK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.cogs_AB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.cogs_AC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.cogs_LK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.cogs_LB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.cogs_LC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.totalCogs_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        
        self.invSpoilExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.overProdExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        
        self.adjCogs_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.adjCogs_AK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.adjCogs_AB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.adjCogs_AC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.adjCogs_LK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.adjCogs_LB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.adjCogs_LC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.totalAdjCogs_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        
        self.grossIncome_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossIncome_AK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossIncome_AB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossIncome_AC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossIncome_LK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossIncome_LB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossIncome_LC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.totalGrossIncome_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_AK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_AB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_AC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_LK_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_LB_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.grossMargin_LC_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.totalGrossMargin_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        
        self.salaryWages_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.rent_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.utilities_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.fuelExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.marketingExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.prodDevExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.otherExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.totalOpExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.ebitda_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.depAmt_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.ebit_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.intIncome_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.intExp_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.ebt_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.taxes_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.netIncome_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.sharesOut_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        self.eps_pnl = X_miscPnls.Report2_Row_Pnl(self, -1)
        
        self.IS_pnls = [p for p in self.GetChildren() if p.GetClassName()=='wxPanel']
        
        # self.detail_list includes the product breakdown panels ----------
        self.detail_list = [self.rev_AK_pnl, self.rev_AB_pnl, self.rev_AC_pnl, self.rev_LK_pnl, 
                        self.rev_LB_pnl, self.rev_LC_pnl, self.cogs_AK_pnl, self.cogs_AB_pnl, 
                        self.cogs_AC_pnl, self.cogs_LK_pnl, self.cogs_LB_pnl, self.cogs_LC_pnl, 
                        self.grossIncome_AK_pnl, self.grossIncome_AB_pnl, self.grossIncome_AC_pnl, self.grossIncome_LK_pnl, 
                        self.grossIncome_LB_pnl, self.grossIncome_LC_pnl, self.grossMargin_AK_pnl, self.grossMargin_AB_pnl, 
                        self.grossMargin_AC_pnl, self.grossMargin_LK_pnl, self.grossMargin_LB_pnl, self.grossMargin_LC_pnl,
                        self.revenue_pnl, self.cogs_pnl, self.grossIncome_pnl, self.grossMargin_pnl,
                        self.adjCogs_pnl, self.adjCogs_AK_pnl, self.adjCogs_AB_pnl, self.adjCogs_AC_pnl,
                        self.adjCogs_LK_pnl, self.adjCogs_LB_pnl, self.adjCogs_LC_pnl]
        
        # Panel Lists for Updating Info -----------------------------------
        self.revPnls = [self.rev_AK_pnl, self.rev_AB_pnl, self.rev_AC_pnl,
                        self.rev_LK_pnl, self.rev_LB_pnl, self.rev_LC_pnl]
        
        self.cogsPnls = [self.cogs_AK_pnl, self.cogs_AB_pnl, self.cogs_AC_pnl,
                        self.cogs_LK_pnl, self.cogs_LB_pnl, self.cogs_LC_pnl]
        
        self.adjCogsPnls = [self.adjCogs_AK_pnl, self.adjCogs_AB_pnl, self.adjCogs_AC_pnl,
                            self.adjCogs_LK_pnl, self.adjCogs_LB_pnl, self.adjCogs_LC_pnl]
        
        
        self.grossIncomePnls = [self.grossIncome_AK_pnl, self.grossIncome_AB_pnl, self.grossIncome_AC_pnl,
                                self.grossIncome_LK_pnl, self.grossIncome_LB_pnl, self.grossIncome_LC_pnl]
        
        self.grossMarginPnls = [self.grossMargin_AK_pnl, self.grossMargin_AB_pnl, self.grossMargin_AC_pnl,
                                self.grossMargin_LK_pnl, self.grossMargin_LB_pnl, self.grossMargin_LC_pnl]
        
        self.opExpPnls = [self.salaryWages_pnl, self.rent_pnl, self.utilities_pnl,
                          self.fuelExp_pnl, self.marketingExp_pnl, self.prodDevExp_pnl,
                          self.otherExp_pnl]
        
        # Add in the panels -----------------------------------------------
        lineCount = 0
        addSL_list = (0, 8, 16, 18, 26, 34, 42, 50, 58) # Indicates where to insert a static line
        for pnl, fld in zip(self.IS_pnls, self.IS_fields):
            bold, italic = False, False
            if fld in self.bold_list:
                bold = True
            if fld in self.italic_list:
                italic = True
            pnl.Init(fld, bold, italic)
            sizer.Add(pnl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if lineCount in addSL_list:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            if lineCount % 2 != 0:
                pnl.SetBackgroundColour(self.styles.lightGrey)
            lineCount += 1
            
            
        self.SetSizer(sizer)
        self.SetupScrolling()
        
        # Bindings
        #------------------------------------------------------------------
        self.detail_cb.Bind(wx.EVT_CHECKBOX, self.OnDetail)
        
        # Function Calls
        #------------------------------------------------------------------
        self.OnDetail(None)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def OnDetail(self, evt):
        '''If the self.detail_cb box is checked, show the product breakdown
        panels for revenue, cogs, gross income and gross margin'''
        if not self.detail_cb.GetValue():
            for pnl in self.detail_list:
                pnl.Hide()
        else:
            for pnl in self.detail_list:
                pnl.Show()
        self.Layout()
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def UpdateIS(self, isList, isPF=True):
        '''Takes and Income Statement list from the Z_gameIO module and
        inserts the values into the Income Statement.'''
        insCol = 1 if isPF else 0
        # Revenue
        totalRev = 0
        for rev, pnl in zip(isList[0], self.revPnls):
            totalRev += rev
            pnl.AddVal(rev, insCol)
        self.totalRevenue_pnl.AddVal(totalRev, insCol)
        # COGS
        totalCOGS = 0
        for cogs, pnl in zip(isList[1], self.cogsPnls):
            totalCOGS += cogs
            pnl.AddVal(cogs, insCol)
        self.totalCogs_pnl.AddVal(totalCOGS, insCol)
        # Inventory Spoilage and Overproduction Expense
        self.invSpoilExp_pnl.AddVal(isList[3], insCol)
        self.overProdExp_pnl.AddVal(isList[2], insCol)
        # Adjusted COGS
        totalAdjCOGS = 0
        for cogs, pnl in zip(isList[4], self.adjCogsPnls):
            totalAdjCOGS += cogs
            pnl.AddVal(cogs, insCol)
        self.totalAdjCogs_pnl.AddVal(totalAdjCOGS, insCol)
        # Gross Income
        totalGI = 0
        for gi, pnl in zip(isList[5], self.grossIncomePnls):
            totalGI += gi
            pnl.AddVal(gi, insCol)
        self.totalGrossIncome_pnl.AddVal(totalGI, insCol)
        # Gross Margin
        for gm, pnl in zip(isList[6], self.grossMarginPnls):
            pnl.AddVal(gm, insCol, isCur=False, isPerc=True)
        try:
            totalGM = float(totalGI)/float(totalRev)* 100.0
        except ZeroDivisionError:
            totalGM = 0
        self.totalGrossMargin_pnl.AddVal(totalGM, insCol, isCur=False, isPerc=True)
        # Operating Expenses
        totalOpExp = 0
        for oe, pnl in zip(isList[7], self.opExpPnls):
            totalOpExp += oe
            pnl.AddVal(oe, insCol)
        self.totalOpExp_pnl.AddVal(totalOpExp, insCol)
        # EBITDA
        ebitda = totalGI - totalOpExp
        self.ebitda_pnl.AddVal(ebitda, insCol)
        # Depreciation
        depreciation = isList[8]
        self.depAmt_pnl.AddVal(depreciation, insCol)
        # EBIT
        ebit = ebitda - depreciation
        self.ebit_pnl.AddVal(ebit, insCol)
        # Interest Income / Expense
        intInc = int(isList[9])
        intExp = int(isList[10])
        self.intIncome_pnl.AddVal(intInc, insCol)
        self.intExp_pnl.AddVal(intExp, insCol)
        # EBT
        ebt = ebit + intInc - intExp
        self.ebt_pnl.AddVal(ebt, insCol)
        # Taxes
        taxes = 0 if ebt < 0 else int(0.30*ebt)
        self.taxes_pnl.AddVal(taxes, insCol)
        # Net Income
        ni = ebt - taxes
        self.netIncome_pnl.AddVal(ni, insCol)
        # Shares out / EPS
        sharesOut = isList[11]
        self.sharesOut_pnl.AddVal(sharesOut, insCol, isCur=False, isPerc=False)
        try:
            eps = (float(ni) / float(sharesOut))
        except ZeroDivisionError:
            eps = 0
        if isPF:
            self.eps_pnl.forecast.SetLabel('$ %.2f' % (eps,))
        else:
            self.eps_pnl.actual.SetLabel('$ %.2f' % (eps,))
        
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def ExportIS(self):
        '''Exports the current Income Statement.'''
        incStmt = []
        for p in self.IS_pnls:
            incStmt.append(p.ExportRow())
        return incStmt