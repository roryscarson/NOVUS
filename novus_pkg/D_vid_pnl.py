#!python
# -*- encoding: utf-8 -*-

# D_vid_pnl.py

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
This module contains the VidPnl class code for the Novus 
Business and IT education program
'''

import wx
import wx.media
import os, sys
import webbrowser
import urllib2
import Q_data
import X_styles, X_utilities, X_mediaCtrl
from Q_language import GetPhrase

class Video_Pnl(wx.Panel):
    '''The video player panel class for the Novus program.'''
    def __init__(self, parent, *args, **kwargs):
        super(Video_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(self)
        self.SetBackgroundColour(self.styles.lightGrey)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.wrongFileMsg = GetPhrase('wrongFileMsg', lang)
        self.wrongFileCap = GetPhrase('wrongFileCap', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.lesson_lbl = GetPhrase('lesson_lbl', lang)
        self.lessonTitle_lbl = ('-')
        self.back_lbl = GetPhrase('back_lbl', lang)
        self.searching_lbl = GetPhrase('searching_lbl', lang)
        
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Novus Banner ----------------------------------------------------
        path = X_utilities.ImageFP('Novus_Small.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.banner_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        sizer.Add(self.banner_bm, 0)
        
        # Lesson Information and Back Button ------------------------------
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        a_box = wx.BoxSizer(wx.HORIZONTAL)
        self.year_st = wx.StaticText(self, -1, self.year_lbl)
        self.lesson_st = wx.StaticText(self, -1, self.lesson_lbl)
        self.lessonTitle_st = wx.StaticText(self, -1, self.lessonTitle_lbl)
        self.back_btn = wx.Button(self, -1, self.back_lbl, size=(150, -1))
        self.back_btn.SetBackgroundColour(self.styles.lightGrey)
        
        self.stuffList = [s for s in self.GetChildren() if s.GetClassName() in ('wxStaticText', 'wxButton')]
        for s in self.stuffList:
            s.SetForegroundColour(self.styles.brown)
            s.SetFont(self.styles.h3_b_font)
        
        a_box.Add(self.year_st, 0, wx.RIGHT|wx.TOP, 5)
        a_box.Add(wx.StaticLine(self, -1, style=wx.VERTICAL), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        a_box.Add(self.lesson_st, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        a_box.Add(wx.StaticLine(self, -1, style=wx.VERTICAL), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        a_box.Add(self.lessonTitle_st, 1, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        a_box.Add(self.back_btn, 0)
        
        sizer.Add(a_box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)
        
        # Video Player ----------------------------------------------------
        self.vidPlayer = X_mediaCtrl.VideoCtrl(self, -1)
        sizer.Add(self.vidPlayer, 1, wx.EXPAND)
        
        #--#
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnBack)
        
        # Method Calls ----------------------------------------------------
        
    #----------------------------------------------------------------------
    # Event Handlers
    #----------------------------------------------------------------------
    def Init(self, year, lessonNum, lessonTitle):
        '''Sets up the panel with the correct title and loads the correct
        video.'''
        # Set up the video information
        self.year_st.SetLabel(self.year_lbl + ' ' + year)
        self.lesson_st.SetLabel(self.lesson_lbl + ' ' + unicode(lessonNum))
        self.lessonTitle_st.SetLabel(lessonTitle)
        # Get the correct video path:
        path = X_utilities.yearDirFP(int(year))
        file = 'LessonVid_y'+year+'_'+unicode(lessonNum)+'.mov'
        vidFile = os.path.join(path, file)
        
        # CHECK 1: LOAD FROM HDD
        #------------------------------------------------------------------
        if os.path.isfile(vidFile):
            # FOR LITE VERSION ONLY -- LOAD STRAIGHT FROM INTERNET
            self.vidPlayer.LoadFile(vidFile)
            return 1
        
        
        # IF LOAD FROM HDD FAIL => DLG: SELECT FILE LOCATION or YOUTUBE
        else:
#            busy = wx.BusyInfo(self.searching_lbl+'...')
            
            # Check the internet connection -------------------------------
            self.inet_connected = True
            try:
                urllib2.urlopen("http://google.com", timeout=2)
            except urllib2.URLError:
                self.inet_connected = False
                return 0
#                path = self.OpenFile(file)
#                if path:
#                    self.vidPlayer.LoadFile(path)
#                    return 1
#                else:
#                    return 2
            finally:
                busy=None
                
            # TEMPORARY - FOR LITE VERSION ONLY
            self.OpenURL(year, lessonNum)
            return 2
            
            
#            dlg = SourceSelectDialog(self, -1)
#            rslt = dlg.ShowModal()
#            if rslt == wx.ID_OK:
#                if dlg.GetChoice():
#                    path = self.OpenFile(file)
#                    if path:
#                        self.vidPlayer.LoadFile(path)
#                        return 1
#                    else:
#                        return 2
#                else:
#                    self.OpenURL(year, lessonNum)
#                    return 2
#            else:
#                return 0
#            dlg.Destroy()

    #----------------------------------------------------------------------
    def OpenFile(self, fileName):
        '''Takes the file name and allows the user to manually select the
        path of the video file on the hard drive. The name of the video
        must match the lesson selected.'''
        if sys.platform == 'win32':
            wildcard = 'WMV files (*.wmv)|*.wmv'
        else:
            wildcard = '*'
        dlg = wx.FileDialog(self, message="Select the Video File",
                            defaultDir=os.curdir, defaultFile=fileName,
                            wildcard=wildcard,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            if sys.platform != 'win32' and path[-3:] != '.wmv':
                wx.Bell()
                return False
            
            if os.path.split(path)[-1] != fileName:
                wx.MessageBox(self.wrongFileMsg+": "+fileName, self.wrongFileCap)
                return False
            
            return path
        
    #----------------------------------------------------------------------
    def OpenURL(self, year, lessonNum):
        '''Takes the year (int) and the lessonNum(int) and loads the correct
        YouTube.com url from the language specific library.'''
        language = self.data.GetData1()[1][1]
        lessonIndex = (int(year)-1)*6 + lessonNum
        
        # Lesson URLs
        engUrl = {
                  1: 'https://vimeo.com/42603298', #L1
                  2: 'https://vimeo.com/42447637', #L2
                  3: 'https://vimeo.com/42453754', #L3
                  4: 'https://vimeo.com/43670738', #L4
                  5: 'https://vimeo.com/43422678', #Excel 1: Excel Basics
                  6: 'https://vimeo.com/43835208', #PowerPoint 1: PowerPoint Basics
                  7: 'https://vimeo.com/42539792', #L5
                  8: 'https://vimeo.com/43667261', #L6
                  9: 'https://vimeo.com/42695072', #L7
                  10: 'https://vimeo.com/43775403', #L8
                  11: 'https://vimeo.com/43853565', #Excel 2
                  12: 'https://vimeo.com/43903586', #Word 1
                  13: 'https://vimeo.com/42532829', #L9
                  14: 'https://vimeo.com/42533108', #L10
                  15: 'https://vimeo.com/43296452', #L11
                  16: 'https://vimeo.com/44443841', #L12
                  17: 'https://vimeo.com/43947191', #Word 2
                  18: 'https://vimeo.com/45081268', #PowerPoint 2
                  19: 'https://vimeo.com/43296457', #L13
                  20: 'https://vimeo.com/43296849', #L14
                  21: 'https://vimeo.com/42541379', #L15
                  22: 'https://vimeo.com/47121884', #L16
                  23: 'https://vimeo.com/45147514', #Excel 3
                  24: 'https://vimeo.com/45264393', #Word 3
                  25: 'https://vimeo.com/42694103', #L17
                  26: 'https://vimeo.com/42533401', #L18
                  27: 'https://vimeo.com/43774489', #L19
                  28: 'https://vimeo.com/47250055', #L20
                  29: 'https://vimeo.com/45317387', #Excel 4
                  30: 'https://vimeo.com/45474330', #Word 4
                  31: 'https://vimeo.com/42533831', #L21
                  32: 'https://vimeo.com/43773892', #L22
                  33: 'https://vimeo.com/44311536', #L23
                  34: 'https://vimeo.com/44309561', #L24
                  35: 'https://vimeo.com/45334497', #PowerPoint 3
                  36: 'https://vimeo.com/44374765' #Armenian Business Resources
                  }
        
        armUrl = {
                  1: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  2: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  3: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  4: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  5: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  6: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  7: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  8: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  9: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  10: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  11: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  12: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  13: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  14: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  15: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  16: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  17: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  18: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  19: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  20: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  21: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  22: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  23: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  24: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  25: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  26: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  27: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  28: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  29: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  30: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  31: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  32: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  33: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  34: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  35: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/',
                  36: 'https://sourceforge.net/p/novus/wiki/Video%20Lessons/'
                  }
        
        # Language Dictionary
        langDic = {'English': engUrl,
                   'Armenian': armUrl}
        
        # Select the Correct URL
        trgtDic = langDic[language]
        trgtURL = trgtDic[lessonIndex]
        webbrowser.open(trgtURL)
        
    #----------------------------------------------------------------------
    def OnBack(self, evt):
        '''Passes the back button event to the parent frame.'''
        evt.Skip()
        
    #----------------------------------------------------------------------
#    def UpdateLanguage(self):
#        '''Updates the languages labels for the object.'''
#        self.wrongFileMsg = GetPhrase('wrongFileMsg')
#        self.wrongFileCap = GetPhrase('wrongFileCap')
#        self.year_lbl = GetPhrase('year_lbl')
#        self.lesson_lbl = GetPhrase('lesson_lbl')
#        self.back_lbl = GetPhrase('back_lbl')
#        self.searching_lbl = GetPhrase('searching_lbl')
        
#        self.year_st.SetLabel(self.year_lbl)
#        self.lesson_st.SetLabel(self.lesson_lbl)
#        self.back_btn.SetLabel(self.back_lbl)
        
#        self.Refresh()
#        self.Layout()
        
#==========================================================================

class SourceSelectDialog(wx.Dialog):
    '''When the selected video file is not present in the installation
    directory, this dialog pops up to prompt the user to select a source
    option: from a different location on the hard drive, or the internet.'''
    def __init__(self, parent, *args, **kwargs):
        super(SourceSelectDialog, self).__init__(parent, title='Video File Selection')
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.title_lbl = GetPhrase('sourceSelect_title', lang)
        self.open_lbl = GetPhrase('openVid_lbl', lang)
        self.inet_lbl = GetPhrase('inetVid_lbl', lang)
        
        # Box Sizer -------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.title_st = wx.StaticText(self, -1, self.title_lbl)
        self.title_st.SetFont(self.styles.h3_font)
        sizer.Add(self.title_st, 0, wx.CENTER|wx.ALL, 10)
        
        self.open_rb = wx.RadioButton(self, -1, self.open_lbl, style=wx.RB_GROUP)
        sizer.Add(self.open_rb, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        self.inet_rb = wx.RadioButton(self, -1, self.inet_lbl)
        sizer.Add(self.inet_rb, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        self.open_rb.SetValue(True)
        
        x = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        
        sizer.Add(x, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        self.SetSizer(sizer)
        self.SetSize(self.BestSize)
        self.Layout()
    
    #----------------------------------------------------------------------
    def GetChoice(self):
        '''Returns the user selection.'''
        if self.open_rb.GetValue():
            return True
        else:
            return False
        