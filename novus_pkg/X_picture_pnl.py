#!python
# -*- encoding: utf-8 -*-

# X_picture_pnl.py

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
The module contains the Picture Panel class for the
Novus program.
'''

import wx
import os, random
import X_styles, X_utilities

class Picture_Pnl(wx.Panel):
    '''This class shows pictures.'''
    def __init__(self, parent, *args, **kwargs):
        super(Picture_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.brown)
        
        # Sizer 
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.upperBuffer = wx.StaticText(self, -1)
        sizer.Add(self.upperBuffer, 1)
        
        #--#
        picDir = os.path.split(X_utilities.ImageFP('col_1.jpg'))[0]
        picDir = os.path.abspath(picDir)
        self.pics = [p for p in os.listdir(picDir) if p[:3]=="col"]
        self.path = X_utilities.ImageFP(random.choice(self.pics))
        self.pic = wx.Bitmap(self.path, wx.BITMAP_TYPE_ANY)
        self.collage_bm = wx.StaticBitmap(self, -1, bitmap=self.pic)
        sizer.Add(self.collage_bm, 0, wx.ALIGN_CENTER)
        
        #--#
        self.lowerBuffer = wx.StaticText(self, -1)
        sizer.Add(self.lowerBuffer, 1)
        
        #--#
        self.SetSizer(sizer)
    