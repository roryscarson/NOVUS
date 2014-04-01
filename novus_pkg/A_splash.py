#!python
# -*- encoding: utf-8 -*-

# A_splash.py

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
This module contains the Splash class for the Novus program.
'''

import wx
import X_utilities

class Novus_Splash(wx.SplashScreen):
    '''The Splash class for the Novus program.'''
    def __init__(self, parent, *args, **kwargs):
        
        path = X_utilities.ImageFP('Novus_Splash.png')
        pic = wx.Image(path, type=wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        style = wx.SPLASH_CENTER_ON_SCREEN|wx.SPLASH_TIMEOUT|wx.BORDER_DEFAULT
        time = 1500
        
        super(Novus_Splash, self).__init__(pic, style, time, parent)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def OnClose(self, evt):
        '''
        Destroys the splash.
        '''
        self.Destroy()
        
        
        
        