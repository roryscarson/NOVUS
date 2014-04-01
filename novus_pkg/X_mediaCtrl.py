#!python
# -*- encoding: utf-8 -*-

# X_mediaCtrl.py

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
This is the (pretty much unnecessary) media control class.
'''

import wx
import wx.media

class VideoCtrl(wx.media.MediaCtrl):
    '''The main media control class for VidDemo.py'''
    def __init__(self, parent, *args, **kwargs):
        super(VideoCtrl, self).__init__(parent, *args, **kwargs)
        
        self.ShowPlayerControls()
        
    def LoadFile(self, fName):
        '''Loads the selected file into the video player and starts playback.'''
        self.Load(fName)