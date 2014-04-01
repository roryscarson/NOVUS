#!python
# -*- encoding: utf-8 -*-

# E_genInfo_pnl.py

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
                              + E_genInfo_pnl.py

This module contains the Finance Panel class code for the Novus 
Business and IT education program. 
'''

import wx
import os
import urllib2
import webbrowser
import wx.lib.scrolledpanel as scrolled
from wx.lib.wordwrap import wordwrap
import wx.html
import G_summary
import X_styles, X_utilities, X_mediaCtrl
import Q_data
from Q_language import GetPhrase

# Custom IDs 
ID_GAME_OVERVIEW = wx.NewId()
ID_EQUIPMENT = wx.NewId()
ID_FINANCING = wx.NewId()
ID_PRODUCTION = wx.NewId()
ID_HR = wx.NewId()
ID_OTHER = wx.NewId()

class HowToBtn_Pnl(scrolled.ScrolledPanel):
    '''This panel holds the lesson buttons for the how to videos,
    which will sit to the right of the media ctrl.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(240, -1))

        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.lightGrey)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.noFileMsg = GetPhrase('noFileMsg', lang)
        self.noFileCap = GetPhrase('noFileCap', lang)
        self.gameOverview_lbl = GetPhrase('gameOverview_lbl', lang)
        self.equipment_lbl = GetPhrase('equipment_lbl', lang)
        self.financing_lbl = GetPhrase('financing_lbl', lang)
        self.production_lbl = GetPhrase('production_lbl', lang)
        self.hr_lbl = GetPhrase('hr_lbl', lang)
        self.other_lbl = GetPhrase('other_lbl', lang)
        
        lbl_list = [self.gameOverview_lbl, self.equipment_lbl, self.financing_lbl, 
                    self.production_lbl, self.hr_lbl, self.other_lbl]
           
        max_lines = 0
        for x in lbl_list:
            lines = len(list(x))//20 + 1
            if lines > max_lines:
                max_lines = lines
        height = max_lines * 25
        
        # Box Sizer -------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer.Add((-1, 10))
        self.gameOverview_btn = wx.Button(self, ID_GAME_OVERVIEW, 
                                       wordwrap(self.gameOverview_lbl, 165, wx.ClientDC(self)),
                                       size=(180, height))
        self.equipment_btn = wx.Button(self, ID_EQUIPMENT, 
                                       wordwrap(self.equipment_lbl, 165, wx.ClientDC(self)),
                                       size=(180, height))
        self.financing_btn = wx.Button(self, ID_FINANCING, 
                                       wordwrap(self.financing_lbl, 165, wx.ClientDC(self)),
                                       size=(180, height))
        self.production_btn = wx.Button(self, ID_PRODUCTION, 
                                        wordwrap(self.production_lbl, 165, wx.ClientDC(self)),
                                        size=(180, height))
        self.hr_btn = wx.Button(self, ID_HR, 
                                wordwrap(self.hr_lbl, 165, wx.ClientDC(self)),
                                size=(180, height))
        self.other_btn = wx.Button(self, ID_OTHER, 
                                   wordwrap(self.other_lbl, 165, wx.ClientDC(self)),
                                   size=(180, height))
       
        btnList = [b for b in self.GetChildren() if b.GetClassName()=='wxButton']
        for b in btnList:
            b.SetBackgroundColour(self.styles.darkGreen)
            b.SetForegroundColour(self.styles.lightGrey)
            b.SetFont(self.styles.h3_b_font)
            sizer.Add(b, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnBtn)
            
        #------------------------------------------------------------------
        self.SetSizer(sizer)
        self.Layout()
        self.SetupScrolling()
        
    #----------------------------------------------------------------------
    def OnBtn(self, evt):
        '''Passes the button event to the HowTo_Pnl parent object.'''
        evt.Skip()
        
#==========================================================================

class HowTo_Pnl(wx.Panel):
    '''This panel class allows the user to select and view the how
    to instructional videos for the game.'''
    def __init__(self, parent, *args, **kwargs):
        super(HowTo_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.lightGrey)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels --------------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('howTo_title', lang)
        self.vidFileFailMsg = GetPhrase('vidFileFailMsg', lang)
        self.vidFileFailCap = GetPhrase('vidFileFailCap', lang)
        self.searching_lbl = GetPhrase('searching_lbl', lang)
        
        # Box Sizer -------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
    
        #--#
        a_box = wx.BoxSizer()
        
        self.btn_pnl = HowToBtn_Pnl(self)
        self.vid_ctrl = X_mediaCtrl.VideoCtrl(self, -1)
        a_box.Add(self.btn_pnl, 0, wx.EXPAND|wx.RIGHT, 10)
        a_box.Add(self.vid_ctrl, 1, wx.EXPAND)
        
        sizer.Add(a_box, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnBtn)
        
    #----------------------------------------------------------------------
    def OnBtn(self, evt):
        '''Takes the EVT_BUTTON event from the btn_pnl object and
        loads the correct video into the vid_ctrl object.'''
        
        # Create the file name
        if evt.GetId() == ID_GAME_OVERVIEW:
            fileName = 'General Overview.wmv'
            fileNum = 1
        elif evt.GetId() == ID_EQUIPMENT:
            fileName = 'Equipment.wmv'
            fileNum = 2
        elif evt.GetId() == ID_FINANCING:
            fileName = 'Finance.wmv'
            fileNum = 3
        elif evt.GetId() == ID_PRODUCTION:
            fileName = 'Production.wmv'
            fileNum = 4
        elif evt.GetId() == ID_HR:
            fileName = 'HR.wmv'
            fileNum = 5
        else:
            fileName = 'Other Spending.wmv'
            fileNum = 6
            
        # Go to the correct directory
        dirName = os.path.abspath(os.path.dirname(X_utilities.yearDirFP()))
        fPath = os.path.join(dirName, 'howto', fileName)
        
        # Load from local HDD if file present, else try from internet
        busy = wx.BusyInfo(self.searching_lbl + '...')
        
        if os.path.isfile(fPath):
            busy.Destroy()
            self.vid_ctrl.Load(fPath)
        
        else:
            try:
                urllib2.urlopen("http://google.com", timeout=2)
                
                lang = self.data.GetData1()[1][1]
                
                eng_dic = {1: 'http://youtu.be/-jLhc1F_LE0',
                           2: 'http://youtu.be/4hjdlGL0MbE',
                           3: 'http://youtu.be/hwJsCaFdRR0', 
                           4: 'http://youtu.be/LTY2yJNvMMM',
                           5: 'http://youtu.be/KdgFW-vEiGA',
                           6: 'http://youtu.be/iAnv8lgIVlM'}
                
                arm_dic = {1: 'http://youtu.be/-jLhc1F_LE0',
                           2: 'http://youtu.be/4hjdlGL0MbE',
                           3: 'http://youtu.be/hwJsCaFdRR0', 
                           4: 'http://youtu.be/LTY2yJNvMMM',
                           5: 'http://youtu.be/KdgFW-vEiGA',
                           6: 'http://youtu.be/iAnv8lgIVlM'}
                
                yt_dic = {'English': eng_dic, 
                          'Armenian': arm_dic,}
                
                url = yt_dic[lang][fileNum]
                webbrowser.open(url, 1)
                
            except urllib2.URLError:
                wx.MessageBox(self.vidFileFailMsg, self.vidFileFailCap, 
                          style=wx.ICON_EXCLAMATION)
            
            finally:
                busy.Destroy()
            
#==========================================================================

class MrktInfo_Pnl(wx.Panel):
    '''This panel holds the market information title bar and content
    panel.'''
    def __init__(self, parent, *args, **kwargs):
        super(MrktInfo_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.lightGrey)
        self.year = 0
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.noFileMsg = GetPhrase('noFileMsg', lang)
        self.noFileCap = GetPhrase('noFileCap', lang)
        self.yearSelect_lbl = GetPhrase('yearSelect_lbl', lang)
        self.choices = [str(x) for x in range(1, 7)]
        
        # Sizer -----------------------------------------------------------
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        a_box = wx.BoxSizer()
        self.yearSelect_st = wx.StaticText(self, -1, self.yearSelect_lbl+': ')
        self.yearSelect_st.SetFont(self.styles.h4_b_font)
        self.yearSelect_cb = wx.ComboBox(self, -1, choices=self.choices,
                                         style=wx.CB_READONLY)
        self.yearSelect_cb.SetFont(self.styles.h4_font)
        
        a_box.Add(self.yearSelect_st, 0, wx.TOP, 3)
        a_box.Add(self.yearSelect_cb, 0, wx.LEFT, 5)
        self.sizer.Add(a_box, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        
        self.sl = wx.StaticLine(self)
        self.sizer.Add(self.sl, 0, wx.EXPAND)
        
        self.core = [self.yearSelect_st,
                     self.yearSelect_cb, self.sl]
    
        self.html_display = wx.html.HtmlWindow(self)
        self.html_display.SetFonts('Constantia', 'serif', 
                                  [12, 12, 12, 13, 14, 15, 18])
        self.sizer.Add(self.html_display, 1, wx.EXPAND)
        #--#
        self.SetSizer(self.sizer)
        
        #--#
        self.Bind(wx.EVT_COMBOBOX, self.OnYearSelect)
        
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Creates, Initializes and adds a content panel.'''
        self.year = year
        path = X_utilities.yearDirFP(year=self.year)
        file = 'genInfo_y'+str(self.year)+'.html'
        path = os.path.join(path, file)
        if os.path.isfile(path):
            self.html_display.LoadFile(path)
        else:
            pass
        
        # Set up the combobox
        self.yearSelect_cb.Clear()
        newList = self.choices[:self.year]
        for i in newList:
            self.yearSelect_cb.Append(i)
        self.yearSelect_cb.SetValue(unicode(self.year))
        
    #----------------------------------------------------------------------
    def OnYearSelect(self, evt):
        '''Loads the Market Information for the selected year.'''
        year = int(self.yearSelect_cb.GetValue())
        path = X_utilities.yearDirFP(year=year)
        file = 'genInfo_y'+str(year)+'.html'
        path = os.path.join(path, file)
        if os.path.isfile(path):
            self.html_display.LoadFile(path)
        else:
            wx.MessageBox(self.noFileMsg, self.noFileCap)
        
#==========================================================================

class GenInfo_Pnl(wx.Panel):
    '''This class holds the General Information panel class for
    the Novus program. It holds general info for the round.'''
    def __init__(self, parent, *args, **kwargs):
        super(GenInfo_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('genInfo_title', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.back_lbl = GetPhrase('back_lbl', lang)
        self.mrktInfo_lbl = GetPhrase('mrktInfo_title', lang)
        self.howTo_lbl = GetPhrase('howTo_title', lang)
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title -----------------------------------------------------------
        a_box = wx.BoxSizer(wx.HORIZONTAL)
        path = X_utilities.ImageFP('Novus_Game5_32.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.genInfo_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.styles.h2_font)
        self.year_st = wx.StaticText(self, -1, self.year_lbl+' - ')
        self.year_st.SetFont(self.styles.h2_font)
        self.back_btn = wx.Button(self, wx.ID_BACKWARD, self.back_lbl, size=(150, -1))
        self.back_btn.SetBackgroundColour(self.styles.lightGrey)
        self.back_btn.SetForegroundColour(self.styles.brown)
        self.back_btn.SetFont(self.styles.h3_b_font)
        a_box.Add((11, -1))
        a_box.Add(self.genInfo_bm, 0, wx.RIGHT, 15)
        a_box.Add(self.title_st, 0, wx.TOP, 5)
        a_box.Add((20, -1))
        a_box.Add(wx.StaticLine(self, -1, style=wx.VERTICAL), 0, wx.EXPAND|wx.RIGHT, 20)
        a_box.Add(self.year_st, 1, wx.TOP, 5)
        a_box.Add(self.back_btn, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        # Button Bar ------------------------------------------------------
        b_box = wx.BoxSizer(wx.HORIZONTAL)
        self.mrktInfo_btn = wx.Button(self, -1, self.mrktInfo_lbl)
        self.howTo_btn = wx.Button(self, -1, self.howTo_lbl)
        
        
        btnList = [b for b in self.GetChildren() if b.GetClassName()=='wxButton']
        for b in btnList[1:]:
            b.SetBackgroundColour(self.styles.darkGreen)
            b.SetForegroundColour(self.styles.lightGrey)
            b.SetFont(self.styles.h3_b_font)
            
        b_box.Add(self.mrktInfo_btn, 0, wx.LEFT|wx.RIGHT, 10)
        b_box.Add(self.howTo_btn, 0, wx.RIGHT, 10)
        
        sizer.Add(b_box, 0, wx.EXPAND|wx.BOTTOM, 10)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        
        # Panels ----------------------------------------------------------
        self.c_box = wx.BoxSizer()
        
        self.mrktInfo_pnl = MrktInfo_Pnl(self)
        self.howTo_pnl = HowTo_Pnl(self, -1)
        self.howTo_pnl.Hide()
        self.c_box.Add(self.mrktInfo_pnl, 1, wx.EXPAND)
        self.c_box.Add(self.howTo_pnl, 1, wx.EXPAND|wx.LEFT, 10)
        
        sizer.Add(self.c_box, 1, wx.EXPAND)
        
        #--#
        self.SetSizer(sizer)
        self.Layout()
        self.State1(None)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnBack)
        self.mrktInfo_btn.Bind(wx.EVT_BUTTON, self.State1)
        self.howTo_btn.Bind(wx.EVT_BUTTON, self.State2)
        
    #----------------------------------------------------------------------
    # FUNCTIONS AND EVENT HANDLERS
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the game panels according to the year provided in the
        argument.'''
        self.year = year
        if self.year < 7:
            self.year_st.SetLabel(self.year_lbl + ' - ' + unicode(self.year))
        else:
            self.year_st.SetLabel(self.complete_lbl)
            
    
    #----------------------------------------------------------------------
    def State1(self, evt):
        '''Shows the mrktInfo_pnl, hides the howTo_pnl.'''
        self.howTo_pnl.Hide()
        self.mrktInfo_pnl.Show()
        self.Layout()
        
        self.howTo_btn.SetBackgroundColour(self.styles.lightGrey)
        self.howTo_btn.SetForegroundColour(self.styles.darkGreen)
        self.mrktInfo_btn.SetBackgroundColour(self.styles.darkGreen)
        self.mrktInfo_btn.SetForegroundColour(self.styles.lightGrey)
        
    #----------------------------------------------------------------------
    def State2(self, evt):
        '''Shows the howTo_pnl and hides the mrktInfo_pnl.'''
        self.howTo_pnl.Show()
        self.mrktInfo_pnl.Hide()
        self.Layout()
        
        self.howTo_btn.SetBackgroundColour(self.styles.darkGreen)
        self.howTo_btn.SetForegroundColour(self.styles.lightGrey)
        self.mrktInfo_btn.SetBackgroundColour(self.styles.lightGrey)
        self.mrktInfo_btn.SetForegroundColour(self.styles.darkGreen)
        
    #----------------------------------------------------------------------
    def OnBack(self, evt):
        '''Handles the back button'''
        if evt.GetId() == wx.ID_BACKWARD:
            evt.Skip()
        
    #----------------------------------------------------------------------
    def EndState(self):
        '''Sets up the End State of the game.'''
        pass
   
    #----------------------------------------------------------------------
    def SetContent(self):
        '''Sets the game's general information content.'''
        if self.year > 0 and self.year < 7:
            self.mrktInfo_pnl.Init(self.year)
        else:
            self.mrktInfo_pnl.Init(6)
        