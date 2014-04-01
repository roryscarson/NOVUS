#!python
# -*- encoding: utf-8 -*-

# A_app.py

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
The main application class for the Novus Business
and IT education program.
'''

import wx
import A_frame, A_splash
import X_utilities

class Novus_App(wx.App):
    '''The primary App class for the Novus program.'''
    def OnInit(self):
        self.splash = A_splash.Novus_Splash(None)
        X_utilities.teamDataCheck()
        X_utilities.teamDataCheck2()
        
        self.title_lbl = "Entrepreneurship Traning Program"
        self.frame = A_frame.Novus_Frame(None, -1,  title="Novus " + self.title_lbl)
        
#        wx.Sleep(1)
        self.frame.Center()
        self.SetTopWindow(self.frame)
        self.frame.Maximize()
        self.frame.Show()
        
        return True
    
#---------------------------------------------------------------------

def run():
    '''Scrpt that runs the program.'''
    app = Novus_App(False)
    app.MainLoop()
    
#---------------------------------------------------------------------

if __name__ == '__main__':
    app = Novus_App(False)
    app.MainLoop()
        