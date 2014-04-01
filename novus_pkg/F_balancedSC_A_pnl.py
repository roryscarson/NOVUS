#!python
# -*- encoding: utf-8 -*-

# F_balancedSC_A_pnl.py

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
E_results_pnl.py +
                 + F_balancedSC_A_pnl.py
                 + F_incomeStmt_A_pnl.py
                 + F_balanceSheet_A_pnl.py
                 + F_cashFlow_A_pnl.py

This module contains the Balanced Score Card "A" Panel class code for 
the Novus Business and IT education program. The "A" panel show the 
results for every year, up to the present year provided to the "Init"
function.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import Q_data
import X_styles, X_miscPnls
import Z_gameIO, Z_mrktInfo
from Q_language import GetPhrase

class BalancedSC_A_Pnl(scrolled.ScrolledPanel):
    '''This class holds the Balanced Score Card panel for the Novus Business 
    and IT education program.'''
    def __init__(self, parent, *args, **kwargs):
        scrolled.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        self.SetBackgroundColour(wx.WHITE)
        
        # Data -----------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels 
        #------------------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.balancedSC_lbl = GetPhrase('balancedSC_lbl', lang)
        self.detail_lbl = GetPhrase('detail_lbl', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.ale_lbl = GetPhrase('ale_lbl', lang)
        self.lager_lbl = GetPhrase('lager_lbl', lang)
        self.keg_lbl = GetPhrase('keg_lbl', lang)
        self.bottle_lbl = GetPhrase('bottle_lbl', lang)
        self.can_lbl = GetPhrase('can_lbl', lang)
        self.units_lbl = GetPhrase('units_lbl', lang)
        # Production Effectiveness Labels
        self.prodEff_lbl = GetPhrase('prodEff_lbl', lang)
        self.realProd_lbl = GetPhrase('realProd_lbl', lang)
        self.realTotProd_lbl = GetPhrase('realTotProd_lbl', lang)
        self.planProd_lbl = GetPhrase('planProd', lang)
        self.planTotProd_lbl = GetPhrase('planTotProd_lbl', lang)
        self.prodEffScore_lbl = GetPhrase('prodEffScore_lbl', lang)
        # Sales Performance Labels
        self.salesPerf_lbl = GetPhrase('salesPerf_lbl', lang)
        self.realSales_lbl = GetPhrase('realSales_lbl', lang)
        self.realTotSales_lbl = GetPhrase('realTotSales', lang)
        self.planSales_lbl = GetPhrase('planSales_lbl', lang)
        self.planTotSales_lbl = GetPhrase('planTotSales_lbl', lang)
        self.bestSales_lbl = GetPhrase('bestSales_lbl', lang)
        self.bestTotSales_lbl = GetPhrase('bestTotSales_lbl', lang)
        self.realMS_lbl = GetPhrase('realMS_lbl', lang)
        self.realTotMS_lbl = GetPhrase('realTotMS_lbl', lang)
        self.planMS_lbl = GetPhrase('planMS_lbl', lang)
        self.planTotMS_lbl = GetPhrase('planTotMS', lang)
        self.bestMS_lbl = GetPhrase('bestMS_lbl', lang)
        self.bestTotalMS_lbl = GetPhrase('bestTotMS_lbl', lang)
        self.salesPerfScore_lbl = GetPhrase('salesPerfScore_lbl', lang)
        # Financial Health Score
        self.keyFinRatios_lbl = GetPhrase('keyFinRatios_lbl', lang)
        self.debtEquity_lbl = GetPhrase('debtEquity_lbl', lang)
        self.currentRatio_lbl = GetPhrase('currentRatio_lbl', lang)
        self.RoA_lbl = GetPhrase('RoA_lbl', lang)
        self.RoE_lbl = GetPhrase('RoE_lbl', lang)
        self.timesInt_lbl = GetPhrase('timesInt_lbl', lang)
        self.finHealthScore_lbl = GetPhrase('finHealthScore_lbl', lang)
        # Employee Moral Labels
        self.employeeMoralScore_lbl = GetPhrase('employeeMoraleScore_lbl', lang)
        # Working Capital Management Labels
        self.wcmScore_lbl = GetPhrase('wcmScore_lbl', lang)
        # Brand Strentgh Labels
        self.brandStr_lbl = GetPhrase('brandStr_lbl', lang)
        self.otherSpending_lbl = GetPhrase('otherSpending_lbl', lang)
        self.packagingDec_lbl = GetPhrase('packagingDec_lbl', lang)
        self.priceToQuality_lbl = GetPhrase('priceToQuality_lbl', lang)
        self.brandConsistency_lbl = GetPhrase('brandConsistency_lbl', lang)
        self.brandStrScore_lbl = GetPhrase('brandStrScore_lbl', lang)
        # Managerial Effectiveness Labels
        self.manEffScore_lbl = GetPhrase('manEffScore_lbl', lang)
        
        # Object Content Lists
        #------------------------------------------------------------------
        self.yearList = [self.balancedSC_lbl, self.year_lbl+' 1', self.year_lbl+' 2',
                         self.year_lbl+' 3', self.year_lbl+' 4', self.year_lbl+' 5',
                         self.year_lbl+' 6']
        
        # Production Effectiveness Content Lists
        self.prodEff_list = [self.prodEff_lbl, '', '', '', '', '', '']
        
        self.realProd_list = [self.realProd_lbl+' - '+self.units_lbl, '', '', '', '', '', '']
        self.realProd_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.realProd_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.realProd_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.realProd_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.realProd_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.realProd_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.realTotProd_list = [self.realTotProd_lbl+' - '+self.units_lbl, '-', '-', '-', '-', '-', '-']
        
        self.planProd_list = [self.planProd_lbl+' - '+self.units_lbl, '', '', '', '', '', '']
        self.planProd_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.planProd_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.planProd_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.planProd_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.planProd_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.planProd_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.planTotProd_list = [self.planTotProd_lbl+' - '+self.units_lbl, '-', '-', '-', '-', '-', '-']
        
        self.prodEffScore_list = [self.prodEffScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Sales Performance Object Content Lists
        self.salesPerf_list = [self.salesPerf_lbl, '', '', '', '', '', '']
        
        self.realSales_list = [self.realSales_lbl, '', '', '', '', '', '']
        self.realSales_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.realSales_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.realSales_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.realSales_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.realSales_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.realSales_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.realTotSales_list = [self.realTotSales_lbl, '-', '-', '-', '-', '-', '-']
        
        self.planSales_list = [self.planSales_lbl, '', '', '', '', '', '']
        self.planSales_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.planSales_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.planSales_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.planSales_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.planSales_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.planSales_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.planTotSales_list = [self.planTotSales_lbl, '-', '-', '-', '-', '-', '-']
        
        self.bestSales_list = [self.bestSales_lbl, '', '', '', '', '', '']
        self.bestSales_AK_list = ['   '+self.ale_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.bestSales_AB_list = ['   '+self.ale_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.bestSales_AC_list = ['   '+self.ale_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.bestSales_LK_list = ['   '+self.lager_lbl+' - '+self.keg_lbl, '-', '-', '-', '-', '-', '-']
        self.bestSales_LB_list = ['   '+self.lager_lbl+' - '+self.bottle_lbl, '-', '-', '-', '-', '-', '-']
        self.bestSales_LC_list = ['   '+self.lager_lbl+' - '+self.can_lbl, '-', '-', '-', '-', '-', '-']
        self.bestTotSales_list = [self.bestTotSales_lbl, '-', '-', '-', '-', '-', '-']
        
        self.realMS_list = [self.realMS_lbl, '', '', '', '', '', '']
        self.realAleMS_list = ['   '+self.ale_lbl, '-', '-', '-', '-', '-', '-']
        self.realLagerMS_list = ['   '+self.lager_lbl, '-', '-', '-', '-', '-', '-']
        self.realTotMS_list = [self.realTotMS_lbl, '-', '-', '-', '-', '-', '-']
        
        self.planMS_list = [self.planMS_lbl, '', '', '', '', '', '']
        self.planAleMS_list = ['   '+self.ale_lbl, '-', '-', '-', '-', '-', '-']
        self.planLagerMS_list = ['   '+self.lager_lbl, '-', '-', '-', '-', '-', '-']
        self.planTotMS_list = [self.planTotMS_lbl, '-', '-', '-', '-', '-', '-']
        
        self.bestMS_list = [self.bestMS_lbl, '', '', '', '', '', '']
        self.bestAleMS_list = ['   '+self.ale_lbl, '-', '-', '-', '-', '-', '-']
        self.bestLagerMS_list = ['   '+self.lager_lbl, '-', '-', '-', '-', '-', '-']
        self.bestTotalMS_list = [self.bestTotalMS_lbl, '-', '-', '-', '-', '-', '-']
        
        self.salesPerfScore_list = [self.salesPerfScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Financial Health Score
        self.keyFinRatios_list = [self.keyFinRatios_lbl, '', '', '', '', '', '']
        self.debtEquity_list = ['   '+self.debtEquity_lbl, '-', '-', '-', '-', '-', '-']
        self.currentRatio_list = ['   '+self.currentRatio_lbl, '-', '-', '-', '-', '-', '-']
        self.RoA_list = ['   '+self.RoA_lbl, '-', '-', '-', '-', '-', '-']
        self.RoE_list = ['   '+self.RoE_lbl, '-', '-', '-', '-', '-', '-']
        self.timesInt_list = ['   '+self.timesInt_lbl, '-', '-', '-', '-', '-', '-']
        self.finHealthScore_list = [self.finHealthScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Employee Moral Labels
        self.employeeMoralScore_list = [self.employeeMoralScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Working Capital Management Labels
        self.wcmScore_list = [self.wcmScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Brand Strentgh Labels
        self.brandStr_list = [self.brandStr_lbl, '', '', '', '', '', '']
        self.otherSpending_list = ['   '+self.otherSpending_lbl, '-', '-', '-', '-', '-', '-']
        self.packagingDec_list = ['   '+self.packagingDec_lbl, '-', '-', '-', '-', '-', '-']
        self.priceToQuality_list = ['   '+self.priceToQuality_lbl, '-', '-', '-', '-', '-', '-']
        self.brandConsistency_list = ['   '+self.brandConsistency_lbl, '-', '-', '-', '-', '-', '-']
        self.brandStrScore_list = [self.brandStrScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Managerial Effectiveness Labels
        self.manEffScore_list = [self.manEffScore_lbl, '-', '-', '-', '-', '-', '-']
        
        # Formatting Lists
        #------------------------------------------------------------------
        self.big_list = [self.prodEff_list, self.salesPerf_list, self.keyFinRatios_list,
                         self.brandStr_list]
        
        self.bigBold_list = [self.prodEffScore_list, self.salesPerfScore_list,
                             self.finHealthScore_list,
                             self.employeeMoralScore_list, self.wcmScore_list,
                             self.brandStrScore_list, self.manEffScore_list]
        
        self.italic_list = [self.realProd_AK_list, self.realProd_AB_list, self.realProd_AC_list, 
                            self.realProd_LK_list, self.realProd_LB_list, self.realProd_LC_list,
                            self.planProd_AK_list, self.planProd_AB_list, self.planProd_AC_list, 
                            self.planProd_LK_list, self.planProd_LB_list, self.planProd_LC_list,
                            self.realSales_AK_list, self.realSales_AB_list, self.realSales_AC_list, 
                            self.realSales_LK_list, self.realSales_LB_list, self.realSales_LC_list,
                            self.planSales_AK_list, self.planSales_AB_list, self.planSales_AC_list, 
                            self.planSales_LK_list, self.planSales_LB_list, self.planSales_LC_list,
                            self.bestSales_AK_list, self.bestSales_AB_list, self.bestSales_AC_list, 
                            self.bestSales_LK_list, self.bestSales_LB_list, self.bestSales_LC_list,
                            self.realAleMS_list, self.realLagerMS_list, 
                            self.planAleMS_list, self.planLagerMS_list, 
                            self.bestAleMS_list, self.bestLagerMS_list, 
                            self.debtEquity_list, self.currentRatio_list, 
                            self.RoA_list, self.RoE_list, self.timesInt_list,
                            self.otherSpending_list, self.packagingDec_list,
                            self.priceToQuality_list, self.brandConsistency_list]
        
        self.allFields = [self.yearList, self.prodEff_list, 
                          self.realProd_list,
                          self.realProd_AK_list, self.realProd_AB_list, self.realProd_AC_list, 
                          self.realProd_LK_list, self.realProd_LB_list, self.realProd_LC_list,
                          self.realTotProd_list,
                          self.planProd_list,
                          self.planProd_AK_list, self.planProd_AB_list, self.planProd_AC_list, 
                          self.planProd_LK_list, self.planProd_LB_list, self.planProd_LC_list,
                          self.planTotProd_list,
                          self.prodEffScore_list,
                          self.salesPerf_list,
                          self.realSales_list,
                          self.realSales_AK_list, self.realSales_AB_list, self.realSales_AC_list, 
                          self.realSales_LK_list, self.realSales_LB_list, self.realSales_LC_list,
                          self.realTotSales_list,
                          self.planSales_list,
                          self.planSales_AK_list, self.planSales_AB_list, self.planSales_AC_list, 
                          self.planSales_LK_list, self.planSales_LB_list, self.planSales_LC_list,
                          self.planTotSales_list,
                          self.bestSales_list,
                          self.bestSales_AK_list, self.bestSales_AB_list, self.bestSales_AC_list, 
                          self.bestSales_LK_list, self.bestSales_LB_list, self.bestSales_LC_list,
                          self.bestTotSales_list,
                          self.realMS_list,
                          self.realAleMS_list, self.realLagerMS_list, 
                          self.realTotMS_list,
                          self.planMS_list,
                          self.planAleMS_list, self.planLagerMS_list, 
                          self.planTotMS_list,
                          self.bestMS_list,
                          self.bestAleMS_list, self.bestLagerMS_list, 
                          self.bestTotalMS_list,
                          self.salesPerfScore_list,
                          self.keyFinRatios_list, self.debtEquity_list, self.currentRatio_list, 
                          self.RoA_list, self.RoE_list, self.timesInt_list, self.finHealthScore_list,
                          self.employeeMoralScore_list, self.wcmScore_list,
                          self.brandStr_list, self.otherSpending_list, self.packagingDec_list,
                          self.priceToQuality_list, self.brandConsistency_list,
                          self.brandStrScore_list, self.manEffScore_list]
        
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        self.detail_cb = wx.CheckBox(self, -1, self.detail_lbl, size=(120, -1),
                                     pos=(15, 15))
        self.detail_cb.SetFont(self.styles.h4_font)
        self.detail_cb.SetValue(False)
        self.balancedSC_st = wx.StaticText(self, -1, self.balancedSC_lbl)
        self.balancedSC_st.SetFont(self.styles.h1_font)
        sizer.Add(self.balancedSC_st, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.TOP, 5)
        
        # Balanced Score Card Panels --------------------------------------
        self.year_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Production Effectiveness Content Lists
        self.prodEff_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.realProd_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realProd_AK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realProd_AB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realProd_AC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realProd_LK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realProd_LB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realProd_LC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realTotProd_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.planProd_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planProd_AK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planProd_AB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planProd_AC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planProd_LK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planProd_LB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planProd_LC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planTotProd_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.prodEffScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Sales Performance Object Content Lists
        self.salesPerf_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.realSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realSales_AK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realSales_AB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realSales_AC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realSales_LK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realSales_LB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realSales_LC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realTotSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.planSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planSales_AK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planSales_AB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planSales_AC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planSales_LK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planSales_LB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planSales_LC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planTotSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.bestSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestSales_AK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestSales_AB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestSales_AC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestSales_LK_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestSales_LB_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestSales_LC_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestTotSales_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.realMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realAleMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realLagerMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.realTotMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.planMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planAleMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planLagerMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.planTotMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.bestMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestAleMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestLagerMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.bestTotalMS_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.salesPerfScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Financial Health Score
        self.keyFinRatios_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.debtEquity_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.currentRatio_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.RoA_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.RoE_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.timesInt_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.finHealthScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Employee Moral Labels
        self.employeeMoralScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Working Capital Management Labels
        self.wcmScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Brand Strentgh Labels
        self.brandStr_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.otherSpending_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.packagingDec_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.priceToQuality_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.brandConsistency_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        self.brandStrScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        # Managerial Effectiveness Labels
        self.manEffScore_pnl = X_miscPnls.Report1_Row_Pnl(self, -1)
        
        self.detail_list = [self.prodEff_pnl, self.realProd_pnl, self.realProd_AK_pnl, 
                            self.realProd_AB_pnl, self.realProd_AC_pnl, self.realProd_LK_pnl, 
                            self.realProd_LB_pnl, self.realProd_LC_pnl, 
                            self.planProd_pnl,
                            self.planProd_AK_pnl, self.planProd_AB_pnl, self.planProd_AC_pnl, 
                            self.planProd_LK_pnl, self.planProd_LB_pnl, self.planProd_LC_pnl,
                            self.salesPerf_pnl,
                            self.realSales_pnl,
                            self.realSales_AK_pnl, self.realSales_AB_pnl, self.realSales_AC_pnl, 
                            self.realSales_LK_pnl, self.realSales_LB_pnl, self.realSales_LC_pnl,
                            self.planSales_pnl,
                            self.planSales_AK_pnl, self.planSales_AB_pnl, self.planSales_AC_pnl, 
                            self.planSales_LK_pnl, self.planSales_LB_pnl, self.planSales_LC_pnl,
                            self.bestSales_pnl,
                            self.bestSales_AK_pnl, self.bestSales_AB_pnl, self.bestSales_AC_pnl, 
                            self.bestSales_LK_pnl, self.bestSales_LB_pnl, self.bestSales_LC_pnl,
                            self.realMS_pnl,
                            self.realAleMS_pnl, self.realLagerMS_pnl,
                            self.planMS_pnl,
                            self.planAleMS_pnl, self.planLagerMS_pnl,
                            self.bestMS_pnl,
                            self.bestAleMS_pnl, self.bestLagerMS_pnl,
                            self.keyFinRatios_pnl, self.debtEquity_pnl, self.currentRatio_pnl, 
                            self.RoA_pnl, self.RoE_pnl,self.timesInt_pnl,
                            self.otherSpending_pnl, self.packagingDec_pnl,
                            self.priceToQuality_pnl, self.brandConsistency_pnl,
                            self.brandStr_pnl]
        
        self.allPanels = [p for p in self.GetChildren() if p.GetClassName() =='wxPanel']
        
        # Add Panels to Sizer ---------------------------------------------
        rowCount = 1
        addLine_list = (1, 10, 18, 19, 28, 36, 44, 48, 52, 56, 57, 64, 65, 66, 
                        72, 73)
        addSpace_list = (1, 19, 57, 64, 65, 66, 72, 73)
        
        for panel, field in zip(self.allPanels, self.allFields):
            if field in self.big_list:
                panel.Init(field, bold=False, italic=False, big=True)
            elif field in self.bigBold_list:
                panel.Init(field, bold=True, italic=False, big=True)
            elif field in self.italic_list:
                panel.Init(field, bold=False, italic=True, big=False)
            else:
                panel.Init(field, bold=False, italic=False, big=True)
            
            sizer.Add(panel, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            
            if rowCount in addLine_list:
                sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
            if rowCount in addSpace_list:
                sizer.Add((-1, 10))
            if rowCount % 2 != 0 and rowCount != 1:
                panel.SetBackgroundColour(self.styles.lightGrey)   
            
            rowCount += 1
            
        # Special Formatting for Managerial Effectiveness panel
        self.manEffScore_pnl.UltraBig()
        
        #--
        self.SetSizer(sizer)
        self.SetupScrolling()
        
        # Bindings --------------------------------------------------------
        self.detail_cb.Bind(wx.EVT_CHECKBOX, self.OnDetail)
        
        # Function Calls --------------------------------------------------
        self.OnDetail(None)
        
    #----------------------------------------------------------------------
    def OnDetail(self, evt):
        '''Shows / Hides the panels in the self.detail list when the 
        self.detail_cb box is checked.'''
        for pnl in self.detail_list:
            if self.detail_cb.GetValue():
                pnl.Show()
            else:
                pnl.Hide()
        self.Layout()
        self.SetupScrolling()
            
    #----------------------------------------------------------------------
    def UpdateBSC(self, year):
        '''Updates the Balanced Score Card on the Results page.'''
        insCol = year
        # PRODUCTION EFFECTIVENESS 
        #------------------------------------------------------------------
        # Get Values
        aPU, tAPU, pPU, tPPU, peScore = self.GetPEScore(year)
        
        # Add the values to the Production Efficiency panels
        self.realProd_AK_pnl.AddVal(aPU[0], insCol, isCur=False)
        self.realProd_AB_pnl.AddVal(aPU[1], insCol, isCur=False)
        self.realProd_AC_pnl.AddVal(aPU[2], insCol, isCur=False)
        self.realProd_LK_pnl.AddVal(aPU[3], insCol, isCur=False)
        self.realProd_LB_pnl.AddVal(aPU[4], insCol, isCur=False)
        self.realProd_LC_pnl.AddVal(aPU[5], insCol, isCur=False)
        self.realTotProd_pnl.AddVal(tAPU, insCol, isCur=False)
        
        self.planProd_AK_pnl.AddVal(pPU[0], insCol, isCur=False)
        self.planProd_AB_pnl.AddVal(pPU[1], insCol, isCur=False)
        self.planProd_AC_pnl.AddVal(pPU[2], insCol, isCur=False)
        self.planProd_LK_pnl.AddVal(pPU[3], insCol, isCur=False)
        self.planProd_LB_pnl.AddVal(pPU[4], insCol, isCur=False)
        self.planProd_LC_pnl.AddVal(pPU[5], insCol, isCur=False)
        self.planTotProd_pnl.AddVal(tPPU, insCol, isCur=False)
        
        self.prodEffScore_pnl.AddVal(peScore, insCol, isCur=False)
        
        # SALES PERFORMANCE SCORE
        #------------------------------------------------------------------
        # Get Values 
        salesPerfInfo = self.GetSPScore(year)
        
        # Add the values to the Sales Performance panels
        actual = salesPerfInfo[0]
        self.realSales_AK_pnl.AddVal(actual[0], insCol)
        self.realSales_AB_pnl.AddVal(actual[1], insCol)
        self.realSales_AC_pnl.AddVal(actual[2], insCol)
        self.realSales_LK_pnl.AddVal(actual[3], insCol)
        self.realSales_LB_pnl.AddVal(actual[4], insCol)
        self.realSales_LC_pnl.AddVal(actual[5], insCol)
        self.realTotSales_pnl.AddVal(salesPerfInfo[1], insCol)
        
        planned = salesPerfInfo[2]
        self.planSales_AK_pnl.AddVal(planned[0], insCol)
        self.planSales_AB_pnl.AddVal(planned[1], insCol)
        self.planSales_AC_pnl.AddVal(planned[2], insCol)
        self.planSales_LK_pnl.AddVal(planned[3], insCol)
        self.planSales_LB_pnl.AddVal(planned[4], insCol)
        self.planSales_LC_pnl.AddVal(planned[5], insCol)
        self.planTotSales_pnl.AddVal(salesPerfInfo[3], insCol)
        
        best = salesPerfInfo[4]
        self.bestSales_AK_pnl.AddVal(best[0], insCol)
        self.bestSales_AB_pnl.AddVal(best[1], insCol)
        self.bestSales_AC_pnl.AddVal(best[2], insCol)
        self.bestSales_LK_pnl.AddVal(best[3], insCol)
        self.bestSales_LB_pnl.AddVal(best[4], insCol)
        self.bestSales_LC_pnl.AddVal(best[5], insCol)
        self.bestTotSales_pnl.AddVal(salesPerfInfo[5], insCol)
        
        actual = salesPerfInfo[6]
        self.realAleMS_pnl.AddVal(actual[0], insCol, isCur=False, isPerc=True)
        self.realLagerMS_pnl.AddVal(actual[1], insCol, isCur=False, isPerc=True)
        self.realTotMS_pnl.AddVal(actual[2], insCol, isCur=False, isPerc=True)
        
        planned = salesPerfInfo[7]
        self.planAleMS_pnl.AddVal(planned[0], insCol, isCur=False, isPerc=True)
        self.planLagerMS_pnl.AddVal(planned[1], insCol, isCur=False, isPerc=True)
        self.planTotMS_pnl.AddVal(planned[2], insCol, isCur=False, isPerc=True)
        
        best = salesPerfInfo[8]
        self.bestAleMS_pnl.AddVal(best[0], insCol, isCur=False, isPerc=True)
        self.bestLagerMS_pnl.AddVal(best[1], insCol, isCur=False, isPerc=True)
        self.bestTotalMS_pnl.AddVal(best[2], insCol, isCur=False, isPerc=True)
        
        self.salesPerfScore_pnl.AddVal(salesPerfInfo[9], insCol, isCur=False)
        spScore = salesPerfInfo[9]
        
        # FINANCIAL HEALTH
        #------------------------------------------------------------------
        frList, frScore = self.GetKeyFR(year)
        
        self.debtEquity_pnl.AddFloat(frList[0], insCol)
        self.currentRatio_pnl.AddFloat(frList[1], insCol)
        self.RoA_pnl.AddFloat(frList[2], insCol)
        self.RoE_pnl.AddFloat(frList[3], insCol)
        self.timesInt_pnl.AddFloat(frList[4], insCol)
        self.finHealthScore_pnl.AddVal(frScore, insCol, isCur=False)
        
        # EMPLOYEE MORAL
        #------------------------------------------------------------------
        morale = self.GetMorale(year, peScore, spScore)
        self.employeeMoralScore_pnl.AddVal(morale, insCol, isCur=False)
        
        # WORKING CAPITAL MANAGEMENT
        #------------------------------------------------------------------
        wcm = self.GetWCScore(year)
        self.wcmScore_pnl.AddVal(wcm, insCol, isCur=False)
        
        # BRAND STRENGTH
        #------------------------------------------------------------------
        spendScore, paScore, paqScore, pcScore, brandScore = self.GetBrand(year)
        self.otherSpending_pnl.AddVal(spendScore, insCol, isCur=False)
        self.packagingDec_pnl.AddVal(paScore, insCol, isCur=False)
        self.priceToQuality_pnl.AddVal(paqScore, insCol, isCur=False)
        self.brandConsistency_pnl.AddVal(pcScore, insCol, isCur=False)
        self.brandStrScore_pnl.AddVal(brandScore, insCol, isCur=False)
        
        # MANAGERIAL EFFECTIVENESS 
        #------------------------------------------------------------------
        x = [peScore, spScore, frScore, morale, wcm, brandScore]
        mngrEff = self.GetManager(year, scoreList=x)
        self.manEffScore_pnl.AddVal(mngrEff, insCol, isCur=False)
        
        self.Scroll(0, 0)
        
    #----------------------------------------------------------------------
    def GetPEScore(self, year, useCurrentInfo=False, currentInfo=[]):
        '''Returns a list of actual production (units), total actual
        production (units), a list of planned production (units), total 
        planned production (units),  and the Production Effectiveness 
        Score.'''
        # Get Information
        if useCurrentInfo:
            decList = currentInfo
        else:
            decList = self.data.GetData1()
        isList, bsList, cfList, frList  = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl, mod=True)
        
        # Get Actual Production (Units) 
        prodRev = isList[0]
        actualProdUnits = []
        totActualProdUnits = 0
        for price, rev in zip(decList[33:39], prodRev):
            try:
                actualProdUnits.append(int(rev / price[year]))
            except ZeroDivisionError:
                actualProdUnits.append(0)
            totActualProdUnits += actualProdUnits[-1]
        
        # Get Planned Production (Units) 
        mTypes = Z_gameIO.GetManMachTypes(decList, self.ale_lbl, self.lager_lbl)
        mCycles = Z_gameIO.GetManMachCycles(decList, year)
        aleVol, lagerVol = Z_gameIO.GetProdVol(mTypes, mCycles)
        plannedProdUnits = Z_gameIO.GetProdUnits(decList, year, aleVol, lagerVol)
        totPlannedProdUnits = 0
        for x in plannedProdUnits:
            totPlannedProdUnits += x
            
        # Get Production Effectiveness Score - 
        try:
            peScore = int(totActualProdUnits / float(totPlannedProdUnits) * 100.0)
        except ZeroDivisionError:
            peScore = 0
        
        # Special Case for Round 1
        if totPlannedProdUnits == 0 and totActualProdUnits == 0:
            peScore = 100
        
        return [actualProdUnits, totActualProdUnits,
                plannedProdUnits, totPlannedProdUnits, 
                peScore]
        
    #----------------------------------------------------------------------
    def GetSPScore(self, year, useCurrentInfo=False, currentInfo=[]):
        '''Gets the Sales Performance info and score. Returns a list of
        actual sales per product, total actual sales, planned sales per 
        product, total planned sales, best case sales per product, total
        best case sales, actual market share per product, total actual
        MS, planned MS per product, total planned MS, best case MS per product,
        total best case MS, and the Sales Performance Score.'''
        # Get Information
        if useCurrentInfo:
            decList = currentInfo
        else:
            decList = self.data.GetData1()
        isList, bsList, cfList, frList  = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl, mod=True)
        pfISList, pfBSList, pfCFList, pfFRList = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl)
        
        # ACTUAL vs. PLANNED vs. BEST SALES
        #------------------------------------------------------------------
        aSales = isList[0]
        pSales = pfISList[0]
        bSales = Z_mrktInfo.GetBestRev(year)
        
        tAS, tPS, tBS = 0, 0, 0
        for i in range(6):
            tAS += aSales[i]
            tPS += pSales[i]
            tBS += bSales[i]
            
        # GET MARKET SHARE INFORMATION
        #------------------------------------------------------------------
        # Get Actual Ale Production (Units) => Liters => Total Liters
        prodRev = isList[0]
        aLiters = []
        for price, rev in zip(decList[33:39], prodRev):
            try:
                if prodRev.index(rev) == 0 or prodRev.index(rev) == 3:
                    aLiters.append(int(rev / price[year] * 64))
                elif prodRev.index(rev) == 1 or prodRev.index(rev) == 4:
                    aLiters.append(int(rev / price[year] * (1/2.0)))
                else:
                    aLiters.append(int(rev / price[year] * (1/3.0)))
            except ZeroDivisionError:
                aLiters.append(0)
                
        # Get Actual Lager Production (Units) => Liters => Total Liters
        prodRev = pfISList[0]
        pLiters = []
        for price, rev in zip(decList[33:39], prodRev):
            try:
                if prodRev.index(rev) == 0 or prodRev.index(rev) == 3:
                    pLiters.append(int(rev / price[year] * 64))
                elif prodRev.index(rev) == 1 or prodRev.index(rev) == 4:
                    pLiters.append(int(rev / price[year] * (1/2.0)))
                else:
                    pLiters.append(int(rev / price[year] * (1/3.0)))
            except ZeroDivisionError:
                pLiters.append(0)
                
        # Get the Actual / Planned / Best case Ale and Liter sales
        aAleLit = aLiters[0] + aLiters[1] + aLiters[2]
        aLagerLit = aLiters[3] + aLiters[4] + aLiters[5]
        pAleLit = pLiters[0] + pLiters[1] + pLiters[2]
        pLagerLit = pLiters[3] + pLiters[4] + pLiters[5]
        bAleLit = Z_mrktInfo.BestOutput(year)[0] 
        bLagerLit = Z_mrktInfo.BestOutput(year)[1]
        
        # Get the Ale, Lager, and Total Market Share for Actual/Planned/Best
        mrktAle, mrktLager = Z_mrktInfo.GetMarketLiters(year)
        
        aAleMS = aAleLit / float(mrktAle) * 100
        aLagerMS = aLagerLit / float(mrktLager) * 100
        tAMS = (aAleLit + aLagerLit) / float(mrktAle + mrktLager) * 100
        aMSInfo = (aAleMS, aLagerMS, tAMS)
        
        pAleMS = pAleLit / float(mrktAle) * 100
        pLagerMS = pLagerLit / float(mrktLager) * 100
        tPMS = (pAleLit + pLagerLit) / float(mrktAle + mrktLager) * 100
        pMSInfo = (pAleMS, pLagerMS, tPMS)
        
        bAleMS = bAleLit / float(mrktAle) * 100
        bLagerMS = bLagerLit / float(mrktLager) * 100
        tBMS = (bAleLit + bLagerLit) / float(mrktAle + mrktLager) * 100
        bMSInfo = (bAleMS, bLagerMS, tBMS)
        
        # Get Sales Performance Score
        #------------------------------------------------------------------
        try:
            score1 = tAS/float(tPS)
        except ZeroDivisionError:
            score1 = 0
        
        try:
            score2 = tAS/float(tBS)
        except ZeroDivisionError:
            score2 = 0
            
        spScore = int((.5*score1 + .5*score2) * 100)
            
        # Special Case for Round 1
        if tBS == 0 and tAS == 0 and tPS == 0:
            spScore = 100
            
        return [aSales, tAS, 
                pSales, tPS, 
                bSales, tBS, 
                aMSInfo, pMSInfo, bMSInfo,
                spScore]
        
    #----------------------------------------------------------------------
    def GetKeyFR(self, year, useCurrentInfo=False, currentInfo=[]):
        '''Gets the key financial ratios (D/E, Current, RoA, RoE, 
        Interest Coverage), and finds the Financial Health Score.'''
        # Get Finacial Ratios
        if useCurrentInfo:
            decList = currentInfo
        else:
            decList = self.data.GetData1()
        frList  = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl, mod=True)[-1]
        d2e = frList[18]
        current = frList[7]
        roa = frList[14]
        roe = frList[15]
        intCov = frList[19]
        actual = [d2e, current, roa, roe, intCov]
        
        # Get Industry Averages
        d2e_ind = 0.5           # Deviation > is penalized
        current_ind = 1.1       # Deviation < is penalized
        roa_ind = 0.0           # Deviation < is penalized
        roe_ind = 0.1           # Deviation < is penalized
        intCov_ind = 5.4        # Deviation < is penalized
        ind = [d2e_ind, current_ind, roa_ind, roe_ind, intCov_ind]
        
        # Financial Health Score: Actual vs. Industry
        score = 0
        score += 0.2 * Z_gameIO.ScoreF1(d2e, d2e_ind, d2e_ind, 1.5)
        
        for act, ind in zip(actual[1:], ind[1:]):
            score += 0.2 * Z_gameIO.ScoreF1(act, ind, 0, ind)
        score = 100 - 100 * score
        return [actual, score]
            
    #----------------------------------------------------------------------
    def GetMorale(self, year, peScore, spScore, useCurrentInfo=False, currentInfo=[]):
        '''Gets the employee moral score.'''
        # Get Info
        if useCurrentInfo:
            decList = currentInfo
        else:
            decList = self.data.GetData1()
        pfISList = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl)[0]
        
        # Get Revenue Forecast and Total Planned Cycles
        fcastRev = 0
        for x in pfISList[0]:
            fcastRev += x
           
        mTypes = Z_gameIO.GetManMachTypes(decList, self.ale_lbl, self.lager_lbl)
        mCycles = Z_gameIO.GetManMachCycles(decList, year)
        totalCycles = 0
        for x in mCycles:
            totalCycles += x
            
        # Get Best Case Employee Hires
        bestHR = Z_mrktInfo.BestHR(fcastRev, totalCycles)
        bestTotal = 0
        for b in bestHR:
            bestTotal += b

        # Get the Actual Employee Hires
        actualHR = decList[21:33]
        actualTotal = 0
        for a, b in zip(actualHR, bestHR):
            if a[year] <= b:
                actualTotal += a[year]
            else:
                actualTotal += b
        
        # Get the Employee Moral Score
        moraleScore = int(actualTotal / float(bestTotal) * 100)
        
        moraleScore = 0.6*moraleScore + 0.2*peScore + 0.2*spScore
        
        return moraleScore
    
    #----------------------------------------------------------------------
    def GetWCScore(self, year, useCurrentInfo=False, currentInfo=[]):
        '''Returns the Working Capital Management Score for the 
        current year. This is a function of whether or not the 
        company had to draw on the LoC.'''
        # Get Finacial Ratios
        if useCurrentInfo:
            decList = currentInfo
        else:
            decList = self.data.GetData1()
        bsList  = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl, mod=True)[1]
        
        # Get the LoC score
        loc = bsList[2][2]
        if loc <= 0:
            locScore = 0
        elif loc > 0 and loc < 25000:
            locScore = 0.1
        elif loc >=25000 and loc < 50000:
            locScore = 0.2
        elif loc >= 50000 and loc < 75000:
            locScore = 0.3
        elif loc >= 75000 and loc < 100000:
            locScore = 0.5
        elif loc >= 100000 and loc < 150000:
            locScore = 0.6
        elif loc >= 150000 and loc < 200000:
            locScore = 0.7
        elif loc >= 200000 and loc < 300000:
            locScore = 0.8
        elif loc >= 300000 and loc < 750000:
            locScore = 0.9
        else:
            locScore = 1
        
        return 100 - 100 * locScore
        
    #----------------------------------------------------------------------
    def GetBrand(self, year, useCurrentInfo=False, currentInfo=[]):
        '''Calculates and returns the Brand Strength Score for the given
        year. This is affected by a minimal spending amount in Marketing,
        consistent packaging allocation, pricing appropriately according
        to ingredient quality, product consistency (price / quality),
        and the disparity between lager and ale.'''
        # Get Info
        if useCurrentInfo:
            decList = currentInfo
        else:
            decList = self.data.GetData1()
        pfISList = Z_gameIO.GetFinanceOutput(decList, year, self.ale_lbl, self.lager_lbl)[0]
        
        # Get Marketing Spending Score ------------------------------------
        mrktSpend = decList[47][year]
        prdvSpend = decList[48][year]
        pracSpend = decList[49][year]
        cmdvSpend = decList[50][year]
        
        # Best Case Spending
        bcSpend = [[0, 0, 0, 0],
                   [1.25, 1.25, 1.25, 0.25],
                   [1.25, 1.00, 1.25, 0.50],
                   [1.25, 0.75, 1.25, 0.75],
                   [1.00, 0.50, 1.00, 1.00],
                   [1.00, 0.50, 0.75, 1.25]]
        mrktBest, prdvBest, pracBest, cmdvBest = bcSpend[year-1]
        
        mrktScore = Z_gameIO.ScoreF1(mrktSpend, mrktBest, 0, mrktBest)
        prdvScore = Z_gameIO.ScoreF1(prdvSpend, prdvBest, 0, prdvBest)
        pracScore = Z_gameIO.ScoreF1(pracSpend, pracBest, 0, pracBest)
        cmdvScore = Z_gameIO.ScoreF1(cmdvSpend, cmdvBest, 0, cmdvBest)
        
        spendScore = 0.25*(mrktScore + prdvScore + pracScore + cmdvScore) 
        

        # Get Packaging Allocation Score ----------------------------------
        if year < 3:
            paScore = 0
        else:
            paScore = 0
            # Get the best packaging allocations
            bestPkg = Z_mrktInfo.BestProduct(year)[-6:]
            for x, y in zip(range(39, 45), bestPkg):
                low = y * 0.25
                if y - low < 0.10:
                    if y - 0.10 < 0:
                        low = 0
                    else:
                        low = y - 0.10
                high = y 
                z = decList[x][year]

                paScore += (1/6.0) * Z_gameIO.ScoreF1(z, y, low, high)

        
        # Pricing According to Quality Score ------------------------------
        bestProdInfo = Z_mrktInfo.BestProduct(year)
        if year < 5:
            paqScore = 0
        else:
            lowPr = Z_mrktInfo.BestProduct(year)[2][0]
            medPr = Z_mrktInfo.BestProduct(year)[2][1]
            highPr = Z_mrktInfo.BestProduct(year)[2][2]
            
            aleQuality = decList[45][year]
            lagerQuality = decList[46][year]
            
            if aleQuality == 1:
                aleBestPr = lowPr[:3]
            elif aleQuality == 2:
                aleBestPr = medPr[:3]
            else:
                aleBestPr = highPr[:3]
                
            if lagerQuality == 1:
                lagerBestPr = lowPr[3:]
            elif lagerQuality == 2:
                lagerBestPr = medPr[3:]
            else:
                lagerBestPr = medPr[3:]
                
            bestPrices = aleBestPr + lagerBestPr

            paqScore = 0
            for actual, best in zip(decList[33:39], bestPrices):
                low = .25 * best
                high = 1.75 * best
                paqScore += (1/6.0) * Z_gameIO.ScoreF1(actual[year], best, low, high)

        # Positioning Consistency -----------------------------------------
        # Get last year's quality ratings
        if year < 5:
            pcScore = 0
        else:
            lastAQ = decList[45][year-1]
            lastLQ = decList[46][year-1]

            pcScore = 0
            if lastAQ != aleQuality:
                pcScore += .2
            
            if lastLQ != lagerQuality:
                pcScore += .2
           
            # Measure the relative changes between the team's prices 
            #   and the changes between the industry products.
            
            # These are the average price changes for each product for all
            #   ingredient qualities
            if year == 5:
                bestChgs = [0.0141, -0.019, 0.0, 0.0536, 0.0325, 0.0366]
            else:
                bestChgs = [0.0097, 0.0, 0.0, 0.0299, 0.0315, 0.0353]
            
            actualChgs = []
            for x in range(33, 39):
                delta = (decList[x][year] - decList[x][year-1])/decList[x][year-1]
                actualChgs.append(delta)
           
            for x in range(6):
                if bestChgs[x] <= 0.02 and bestChgs[x] >= -0.02:
                    low = -0.02
                    high = 0.02
                else:
                    low = bestChgs[x] * 0.25
                    high = bestChgs[x] * 1.75
                pcScore += .1 * Z_gameIO.ScoreF1(actualChgs[x], bestChgs[x], low, high)
  
        # Calculate Brand Score -------------------------------------------
        brandScore = 100 - ((100*spendScore + paScore + paqScore + pcScore)*.25)
        spendScore = 100 - (100 * spendScore)
        paScore = 100 - (100 * paScore)
        paqScore = 100 - (100 * paqScore)
        pcScore = 100 - (100 * pcScore)
        return [spendScore, paScore, paqScore, pcScore, brandScore]
    
    #----------------------------------------------------------------------
    def CombineScores(self, year, useCurrentInfo=False, currentInfo=[]):
        '''This function gets and weights the individual BSC scores, excluding
        Managerial Effectiveness.'''
        peScore = self.GetPEScore(year, useCurrentInfo, currentInfo)
        spScore = self.GetSPScore(year, useCurrentInfo, currentInfo)
        kfrScore = self.GetKeyFR(year, useCurrentInfo, currentInfo)
        moraleScore = self.GetMorale(year, peScore[-1], spScore[-1], useCurrentInfo, currentInfo)
        wcmScore = self.GetWCScore(year, useCurrentInfo, currentInfo)
        brandScore = self.GetBrand(year, useCurrentInfo, currentInfo)
        
        return peScore[-1]*0.2 + spScore[-1]*0.25 + kfrScore[-1]*0.05 + \
            moraleScore*0.05 + wcmScore*0.2 + brandScore[-1]*0.25
        
    #----------------------------------------------------------------------
    def GetManager(self, year, scoreList=[], useCurrentInfo=False, currentInfo=[]):
        '''Gets the Managerial Effectiveness Score. This is composite of
        past Managerial Effectiveness Score, as well as the individual
        scores for the current round.'''
        if scoreList:
            peScore, spScore, kfrScore, moraleScore, wcmScore, brandScore = scoreList
        
        if year == 1:
            lastYear = 100
        else:
            lastYear = self.data.GetData1()[70][year-1]
            
        if useCurrentInfo:
            currentCmb = self.CombineScores(year, True, currentInfo)
        else:
            currentCmb = peScore*0.2 + spScore*0.25 + kfrScore*0.05 + \
                moraleScore*0.05 + wcmScore * 0.2 + brandScore*0.25
            
        mngrEff = 0.4 * lastYear + 0.6 * currentCmb
        
        return mngrEff
    
    #----------------------------------------------------------------------
    def Reset(self):
        '''Resets the game's input fields.'''
        for panel, field in zip(self.allPanels, self.allFields):
            if field in self.big_list:
                panel.Init(field, bold=False, italic=False, big=True)
            elif field in self.bigBold_list:
                panel.Init(field, bold=True, italic=False, big=True)
            elif field in self.italic_list:
                panel.Init(field, bold=False, italic=True, big=False)
            else:
                panel.Init(field, bold=False, italic=False, big=True)
                
    #----------------------------------------------------------------------
    def ExportBSC(self):
        '''Exports the Balanced Score Card.'''
        bsc = []
        for p in self.allPanels:
            bsc.append(p.ExportRow())
        return bsc
        