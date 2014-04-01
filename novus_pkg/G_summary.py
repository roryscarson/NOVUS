#!python
# -*- encoding: utf-8 -*-

'''
G_summary.py

This module contains panel class for the market summary content
for a particular decision. The 
'''

import os, sys
import wx
import wx.lib.scrolledpanel as scrolled
import wx.html
import X_utilities
import Q_data
from Q_language import GetPhrase

class Summary_Pnl(scrolled.ScrolledPanel):
    '''This panel holds market information for the current decision
    panel.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(460, -1))
        
        self.data = Q_data.Data(None)
        
        # Messages --------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.noFileMsg = GetPhrase('noFileMsg', lang)
        self.noFileCap = GetPhrase('noFileCap', lang)
        
        # Box Sizer -------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.html_display = wx.html.HtmlWindow(self)
        self.html_display.SetFonts('Constantia', 'serif', 
                                  [12, 12, 12, 13, 14, 15, 18])
        sizer.Add(self.html_display, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def Init(self, year, panel):
        '''Loads the correct html file to the panel.'''
        path = X_utilities.yearDirFP(year=year)
        file = 'panel_'+unicode(panel)+'_y'+unicode(year)+'.html'
        path = os.path.join(path, file)
        if os.path.isfile(path):
            self.html_display.LoadFile(path)
        else:
            wx.MessageBox(self.noFileMsg, self.noFileCap)
        
    