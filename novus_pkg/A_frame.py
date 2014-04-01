#!python
# -*- encoding: utf-8 -*-

# A_frame.py

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
The main frame class for the Novus Business
and IT education program.
'''

import wx
import os, sys
import A_menu
import B_yearSelect_pnl, C_lessonSelect_pnl, D_vid_pnl, E_game_pnl
import Q_data
import Q_about_dlg
import X_styles, X_utilities
import Y_makeTeamData1

from Q_language import GetPhrase

class Novus_Frame(wx.Frame):
    '''The main Frame class for the Novus program.'''
    def __init__(self, parent, *args, **kwargs):
        super(Novus_Frame, self).__init__(parent, *args, **kwargs)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Messages and Captions -------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.submitMsg = GetPhrase('submitMsg', lang)
        self.submitCap = GetPhrase('submitCap', lang)
        self.exitMsg = GetPhrase('exitMsg', lang)
        self.exitCap = GetPhrase('exitCap', lang)
        self.resetMsg = GetPhrase('resetMsg', lang)
        self.resetCap = GetPhrase('resetCap', lang)
        self.resetSuccessMsg = GetPhrase('resetSuccessMsg', lang)
        self.resetSuccessCap = GetPhrase('resetSuccessCap', lang)
        self.tmMsg = GetPhrase('tmMsg', lang)
        self.tmCap = GetPhrase('tmCap', lang)
        self.pcFailMsg = GetPhrase('pcFailMsg', lang)
        self.vidFileFailMsg = GetPhrase('vidFileFailMsg', lang)
        self.vidFileFailCap = GetPhrase('vidFileFailCap', lang)
        self.canResetMsg = GetPhrase('canResetMsg', lang)
        self.translating_lbl = GetPhrase('translating_lbl', lang)
        self.langWarningMsg = GetPhrase('langWarningMsg', lang)
        self.langWarningCap = GetPhrase('langWarningCap', lang)
        
        # Set Icon --------------------------------------------------------
        path = X_utilities.ImageFP('Novus_16.png')
        icon = wx.Icon(path, type= wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        
        # Add Menubar -----------------------------------------------------
        self.menu = A_menu.Menu(-1)
        self.SetMenuBar(self.menu)
        
        # Style -----------------------------------------------------------
        self.Size = (900,600)
        self.Style = wx.VSCROLL
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.lightGrey)
        
        # Add Panels ------------------------------------------------------
        self.intro_pnl = B_yearSelect_pnl.YearSelect_Pnl(self, -1)
        self.lessonSelect_pnl = C_lessonSelect_pnl.LessonSelect_Pnl(self, -1)
        self.vid_pnl = D_vid_pnl.Video_Pnl(self, -1)
        self.game_pnl = E_game_pnl.Game_Pnl(self, -1)
        
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add Panels to Sizer ---------------------------------------------
        sizer.Add(self.intro_pnl, 1, wx.EXPAND|wx.ALL, 15)
        sizer.Add(self.lessonSelect_pnl, 1, wx.EXPAND|wx.ALL, 15)
        self.lessonSelect_pnl.Hide()
        sizer.Add(self.vid_pnl, 1, wx.EXPAND|wx.ALL, 15)
        self.vid_pnl.Hide()
        sizer.Add(self.game_pnl, 1, wx.EXPAND|wx.ALL, 15)
        self.game_pnl.Hide()
        
        # Set Sizer -------------------------------------------------------
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.intro_pnl.Bind(wx.EVT_BUTTON, self.OnYearBtn)
        self.lessonSelect_pnl.Bind(wx.EVT_BUTTON, self.OnLessonBtn)
        self.vid_pnl.Bind(wx.EVT_BUTTON, self.OnVidBtn)
        self.game_pnl.Bind(wx.EVT_BUTTON, self.OnGameBtn)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        
    #----------------------------------------------------------------------
    # EVENT HANDLERS
    #----------------------------------------------------------------------
    def OnYearBtn(self, evt):
        '''Handles the button events from the intro panel.'''
        obj = evt.GetEventObject()
        year = int(obj.GetLabel().split(' ')[-1])
        self.intro_pnl.Hide()
        self.lessonSelect_pnl.Init(year)
        self.lessonSelect_pnl.Show()
        self.Layout()
        
    #----------------------------------------------------------------------
    def OnLessonBtn(self, evt):
        '''Handles the button eventsfrom the Lesson Select panel.'''
        id = evt.GetId()
        if id == wx.ID_BACKWARD:
            self.lessonSelect_pnl.Hide()
            self.intro_pnl.Show()
        elif id == wx.ID_FORWARD:
            self.lessonSelect_pnl.Hide()
            # Get the year from the lessonSelect_pnl
            self.game_pnl.Init()
            self.game_pnl.Show()
        else:
            # Get Year
            year = self.lessonSelect_pnl.year
            btnPressed = evt.GetEventObject()
            # Get Lesson Number
            btnID = evt.GetId()
            if btnID == wx.ID_FILE1:
                lessonNum = 1
            elif btnID == wx.ID_FILE2:
                lessonNum = 2
            elif btnID == wx.ID_FILE3:
                lessonNum = 3
            elif btnID == wx.ID_FILE4:
                lessonNum = 4
            elif btnID == wx.ID_FILE5:
                lessonNum = 5
            else:
                lessonNum = 6
            # Get Lesson Name
            lessonName = btnPressed.GetLabel()
            lessonName = lessonName.replace('\n', '')
            
            # Set up the vid_pnl
            x = self.vid_pnl.Init(unicode(year), lessonNum, lessonName)
            if x == 1:
                self.lessonSelect_pnl.Hide()
                self.vid_pnl.Show()
            elif x == 2:
                pass
            else:
                wx.MessageBox(self.vidFileFailMsg, self.vidFileFailCap)
            
        self.Layout()
        
    #----------------------------------------------------------------------
    def OnVidBtn(self, evt):
        '''Handles the "Back" button on the video panel.'''
        self.vid_pnl.Hide()
        self.lessonSelect_pnl.Show()
        self.Layout()
        
    #----------------------------------------------------------------------
    def OnGameBtn(self, evt):
        '''Handles the "Back" button on the game panel.'''
        if evt.GetId() == wx.ID_BACKWARD:
            self.game_pnl.Hide()
            self.lessonSelect_pnl.Show()
            self.Layout()
            self.game_pnl.listbook.SetSelection(0)
            self.game_pnl.listbook.decisions_pnl.notebook.SetSelection(0)
        
        elif evt.GetId() == wx.ID_APPLY:
            # Submit the team decisions
            dlg = wx.MessageDialog(None, self.submitMsg, self.submitCap, 
                                   style=wx.ICON_QUESTION|wx.YES_NO)
            if dlg.ShowModal() == wx.ID_YES:
                self.game_pnl.Commit()
                self.game_pnl.listbook.finance_pnl.State1(None)
                self.game_pnl.listbook.SetSelection(0)
                self.game_pnl.listbook.result_pnl.State3(None)
                self.game_pnl.listbook.decisions_pnl.notebook.SetSelection(0)
                self.intro_pnl.year_pnl.SetYear()
            dlg.Destroy()
        elif evt.GetId() == wx.ID_RESET:
            # Reset the game
            self.ShowResetPW()
            
        elif evt.GetId() == wx.ID_PRINT:
            # Export the current game results
            self.game_pnl.listbook.result_pnl.ExportResults()
            
    #----------------------------------------------------------------------
    def OnMenu(self, evt):
        '''Handles the events from the menubar.'''
        id = evt.GetId()
        
        if id == wx.ID_RESET:
            self.ShowResetPW()
            
        elif id == wx.ID_EXIT:
            dlg = wx.MessageDialog(None, self.exitMsg, self.exitCap, wx.ICON_EXCLAMATION|wx.YES_NO)
            if dlg.ShowModal() == wx.ID_YES:
                sys.exit()
            dlg.Destroy()
        
        elif id == wx.ID_ABOUT:
            dlg = Q_about_dlg.About_Dlg(self)
            dlg.Show()
        
        elif id == wx.ID_HIGHEST:
            dlg = wx.PasswordEntryDialog(self, self.tmMsg, self.tmCap)
            dlg.SetValue("")
            if dlg.ShowModal() == wx.ID_OK:
                input = dlg.GetValue()
                if input == 'NOVu$':
                    self.game_pnl.TeacherModeOn()
                else:
                    wx.MessageBox(self.pcFailMsg, self.pcFailMsg, style=wx.ICON_ASTERISK)
            dlg.Destroy()
        
        else:
            langDict = self.menu.GetLanguageInfo()
            selectedLang = ''
            for key, lang in langDict.iteritems():
                if self.menu.languages.IsChecked(key):
                    selectedLang = langDict[key]
            self.data.ChangeLanguage(selectedLang)
            # Reset Program
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    #----------------------------------------------------------------------
    def ShowResetPW(self):
        '''Shows a password entry dialog when the user tries to reset
        the game.'''
        # TEMPORARY -- NO PASSWORD, JUST RESETS
        self.ResetGame()
    
#        dlg = wx.PasswordEntryDialog(self, self.canResetMsg, self.canResetMsg)
#        dlg.SetValue('')
#        if dlg.ShowModal() == wx.ID_OK:
#            input = dlg.GetValue()
#            if input == 'newNovus':
#                self.ResetGame()
#            else:
#                wx.MessageBox(self.pcFailMsg, self.pcFailMsg, style=wx.ICON_ASTERISK)
#        dlg.Destroy()
    
    #----------------------------------------------------------------------
    def ResetGame(self):
        '''Resets the game / program.'''
        dlg = wx.MessageDialog(None, self.resetMsg, self.resetCap, wx.ICON_QUESTION|wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            # Maintain the selected language
            selectedLang = self.data.GetData1()[1][1]
            Y_makeTeamData1.MakeTeamData1()
            self.data.ChangeLanguage(selectedLang)
            # Go back to the intro panel
            self.lessonSelect_pnl.Hide()
            self.vid_pnl.Hide()
            self.game_pnl.Hide()
            self.intro_pnl.Show()
            self.Layout()
            # Reset the year
            self.intro_pnl.year_pnl.SetYear()
            python = sys.executable
            os.execl(python, python, *sys.argv)
        dlg.Destroy()
        