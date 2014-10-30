#!python
# -*- encoding: utf-8 -*-

# A_menu.py

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
This is the menu class used by the Novus Business
and IT Education program.
'''

import wx
import os
import Q_data
import X_utilities
from Q_language import GetPhrase

class Menu(wx.MenuBar):
    def __init__(self, parent, *args, **kwargs):
        super(Menu, self).__init__(parent, *args, **kwargs)
        
        self.file = wx.Menu()
        self.languages = wx.Menu()
        self.help = wx.Menu()
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.file_lbl = GetPhrase('file_lbl', lang)
        self.reset_lbl = GetPhrase('reset_lbl', lang)
        self.exit_lbl = GetPhrase('exit_lbl', lang)
        self.languages_lbl = GetPhrase('languages_lbl', lang)
        self.help_lbl = GetPhrase('help_lbl', lang)
        self.about_lbl = GetPhrase('about_lbl', lang)
        self.tm_lbl = GetPhrase('tm_lbl', lang)
        
        # Tools Menu ------------------------------------------------------
        self.file.Append(wx.ID_RESET, self.reset_lbl)
        self.file.Append(wx.ID_EXIT, self.exit_lbl)
        
        # Languages Menu --------------------------------------------------
        # Get a list of the availabel langauges
        langs = ['English', 'Armenian']
        
        # Add them to the "Languages" menu
        for l in langs:
            self.languages.Append(-1, l, '', wx.ITEM_RADIO)
            
        # Set the correct Language
        self.data = Q_data.Data(None)
        currentLang = self.data.GetData1()[1][1]
        menuItems = self.languages.GetMenuItems()
        idToCheck = False
        for x in menuItems:
            if x.GetItemLabel() == currentLang:
                idToCheck = x.GetId()
        
        # If there's an error finding the correct language, default to English
        if not idToCheck:
            for x in menuItems:
                if x.GetItemLabel() == 'English':
                    idToCheck = x.GetId()
        self.languages.Check(idToCheck, True)
        
        # Help Menu -------------------------------------------------------
        self.help.Append(wx.ID_ABOUT, self.about_lbl, '')
        self.help.Append(wx.ID_HIGHEST, self.tm_lbl, '')
        
        # Add Menus -------------------------------------------------------
        self.Append(self.file, self.file_lbl)
        # TEMPORARY -- OMIT LANGUAGES FROM MENUBAR
        #TODO Selecting Armenian language crashes program and changes language
        # upon restart
        self.Append(self.languages, self.languages_lbl)
        self.Append(self.help, self.help_lbl)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_MENU, self.OnMenu)
        
    #----------------------------------------------------------------------
    def OnMenu(self, evt):
        evt.Skip()
        
    #----------------------------------------------------------------------
    def GetLanguageInfo(self):
        '''Returns a dictionary of language ids: labels'''
        langDic = {}
        for x in self.languages.GetMenuItems():
            langDic[x.GetId()] = x.GetItemLabel()
        return langDic
        