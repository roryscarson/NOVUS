#!python
# -*- encoding: utf-8 -*-

# B_lessonSelect_pnl.py

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
The module contains the code for the lesson Panel for the
Novus program.
'''

import wx
import wx.lib.scrolledpanel as scrolled
import C_lessonList_pnl, X_picture_pnl
import X_styles, X_utilities

class LessonSelect_Pnl(wx.Panel):
    '''This class is for the Intro Panel object for the Novus program.'''
    def __init__(self, parent, *args, **kwargs):
        super(LessonSelect_Pnl, self).__init__(parent, *args, **kwargs)
        
        self.year = 0
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.lightGrey)
        
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Novus Banner ----------------------------------------------------
        path = X_utilities.ImageFP('Novus_Small.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.banner_bm = wx.StaticBitmap(self, -1, bitmap=pic)
        sizer.Add(self.banner_bm, 0)
        
        # H-Box -----------------------------------------------------------
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self.lesson_pnl = C_lessonList_pnl.LessonList_Pnl(self)
        h_box.Add(self.lesson_pnl, 5, wx.EXPAND|wx.RIGHT, 15)
        
        # Right Side ------------------------------------------------------
        self.pic_pnl = X_picture_pnl.Picture_Pnl(self, -1)
        h_box.Add(self.pic_pnl, 4, wx.EXPAND)
        
        sizer.Add(h_box, 1, wx.EXPAND)
        
        # Set Sizer -------------------------------------------------------
        self.SetSizer(sizer)
        
        # Bindings --------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        
    #----------------------------------------------------------------------
    # Event Handlers 
    #----------------------------------------------------------------------
    def Init(self, year):
        '''Passes the selected year to the Lesson panel.'''
        self.year = year
        self.lesson_pnl.Init(year)
        
    #----------------------------------------------------------------------
    def OnButton(self, evt):
        '''Handles all the button events for the intro panel.'''
        evt.Skip()      
